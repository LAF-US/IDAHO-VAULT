"""Pure thread-analysis vocabulary shared by the review/merge engine's concerns.

The review-state projector (concerns A/B/C) and the looker/attestation subsystem
(concern D) both reason over the same GitHub review-thread shape: is a thread
bot-only, has a look been attested, what is its resolution disposition. Those
predicates are pure — they read a thread/PR dict and decide; they perform no
GitHub I/O and resolve nothing. They lived in ``review_feedback_loop.py`` only
because both concerns needed them; per #600 §5 ("shared lib … imported by both,
duplicated by neither") they live here so the looker can be extracted whole
without dragging the engine, and the engine can keep its review-state logic
without importing the looker. Moved verbatim from ``review_feedback_loop.py`` —
no behavior change.
"""

from __future__ import annotations

import re

# Detection requires the structured marker AND that `by` matches the comment's
# own author, so a pasted or forged marker attributed to someone else cannot
# fake a look. This layer RESOLVES NOTHING.
LOOK_ATTESTATION_RE = re.compile(
    r"<!--\s*looked:\s*by=(?P<by>[A-Za-z0-9][A-Za-z0-9-]*(?:\[bot\])?)\s*;[^>]*-->"
)

# A GitHub committable suggestion is a fenced ```suggestion block in a review
# comment body. It is the ONE reviewer finding a machine can apply deterministically
# (via the applyReviewSuggestion mutation); everything else is prose that needs a
# real fix. This detector is the engine's "can this be auto-applied?" signal.
SUGGESTION_BLOCK_RE = re.compile(r"(?m)^\s*`{3,}\s*suggestion\b")


def _thread_has_attested_look(thread: dict) -> bool:
    """True if a looker has recorded a self-attested look in the thread.

    Requires a structured attestation marker whose `by=` equals the comment's
    own author, so incidental or forged marker text cannot spoof a look.
    """
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        login = ((comment.get("author") or {}).get("login") or "").strip()
        match = LOOK_ATTESTATION_RE.search(comment.get("body") or "")
        if match and login and match.group("by") == login:
            return True
    return False


# Layer B (#399): an agent's resolution is legitimate only if it carries a
# recorded attestation. These are the pure building blocks of that act — the
# bot-only eligibility predicate and the attestation-body builder. They WRITE
# NOTHING and are not invoked anywhere; the resolve-capable wiring lands later.
#
# Standing model: any direct-write agent may attest-and-resolve a thread whose
# every author is a bot (advisory OR signal — no denylist), never a human-authored
# thread, and never on a CHANGES_REQUESTED review. The PR-level CHANGES_REQUESTED
# guard belongs with the future resolve path; bot-only eligibility lives here.
ATTESTATION_DECISIONS: frozenset[str] = frozenset({"addressed", "advisory", "wontfix"})


def _author_is_bot(author: dict) -> bool:
    """True when a review-comment author is a GitHub App / bot actor, not a human."""
    if (author.get("__typename") or "") == "Bot":
        return True
    return (author.get("login") or "").endswith("[bot]")


def _thread_is_bot_only(thread: dict) -> bool:
    """True when every author of the thread is a bot (>=1 author, no human).

    Eligibility for agent attest-and-resolve under the standing model: bot-authored
    threads only. A single human participant — or no participants — is ineligible.
    """
    comments = (thread.get("comments") or {}).get("nodes") or []
    authors = [(comment.get("author") or {}) for comment in comments]
    if not authors:
        return False
    return all(_author_is_bot(author) for author in authors)


def _thread_resolved_by(thread: dict) -> str:
    """Login of the actor who resolved the thread, or '' if unresolved/unknown.

    GitHub exposes `PullRequestReviewThread.resolvedBy`, so a backfill can tell whether
    *this engine's identity* resolved a thread — and never witness another actor's resolve.
    """
    actor = thread.get("resolvedBy") or {}
    return (actor.get("login") or "").strip()


def _thread_has_committable_suggestion(thread: dict) -> bool:
    """True if any comment in the thread carries a GitHub ```suggestion block.

    These are the only reviewer findings applyable deterministically — GitHub commits
    the suggested diff directly, no generative interpretation. Everything else is prose.
    """
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        if SUGGESTION_BLOCK_RE.search(comment.get("body") or ""):
            return True
    return False


# Resolution disposition (#399 engine): route ONE unresolved thread to *how it gets
# resolved* — never "dispose of a bot thread." Reviewer threads are caught errors; the
# gate exists to make agents fix them before main, so a bare attest-and-resolve of a
# substantive bot finding is the rubber-stamp the gate exists to prevent.
#   - needs-human        : a human authored it, OR bot-only proof is incomplete (a human
#                          may lie beyond a truncated comment page) — judgment required.
#   - looked             : a sealed attestation is already present (recoverable).
#   - outdated-resolvable: bot-only and GitHub marks it outdated (referenced lines moved)
#                          — a genuine look may attest-and-resolve it as stale.
#   - apply-suggestion   : carries a committable ```suggestion — apply deterministically.
#   - needs-fix          : bot-only substantive finding, no mechanical fix — the authoring
#                          agent must fix it for real (dispatch), never stamp it closed.
def _thread_resolution_disposition(thread: dict) -> str:
    """Route one unresolved thread to its deterministic resolution disposition. Pure."""
    page_info = (thread.get("comments") or {}).get("pageInfo")
    page_complete = isinstance(page_info, dict) and page_info.get("hasNextPage") is False
    if not _thread_is_bot_only(thread):
        return "needs-human"
    if not page_complete:
        return "needs-human"  # bot-only unprovable: a human could lie beyond the page
    if _thread_has_attested_look(thread):
        return "looked"
    if thread.get("isOutdated"):
        return "outdated-resolvable"  # referenced lines moved; can't apply a suggestion
    if _thread_has_committable_suggestion(thread):
        return "apply-suggestion"
    return "needs-fix"


# Dispositions a bare attest-and-resolve apply pass may clear WITHOUT a fix:
# genuinely stale (outdated) or already-attested. needs-fix and apply-suggestion are
# NOT here — they require a real fix / an applied suggestion, not a bare resolve.
BARE_RESOLVABLE_DISPOSITIONS: frozenset[str] = frozenset({"outdated-resolvable", "looked"})


def _count_committable_suggestion_threads(pr: dict) -> int:
    """Number of unresolved threads on `pr` whose disposition is `apply-suggestion` —
    bot-only, page-complete, current (not outdated), carrying a committable ```suggestion.

    This is the PROPOSE-ONLY signal (Logan's #3 decision, 2026-06-19): the engine surfaces
    these — GitHub has no public apply-suggestion API, so committing the diff would mean the
    engine rewriting files on a contributor branch, which we deliberately do NOT do here.
    It only flags that ready-to-apply suggestions exist; a human or the authoring agent
    applies them (one-click "Commit suggestion" in the UI), then the witnessed resolve
    clears the thread on the next event. Surfacing is safe on every path (no write), so it
    is NOT protected-path-gated."""
    count = 0
    for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
        if thread.get("isResolved"):
            continue
        if _thread_resolution_disposition(thread) == "apply-suggestion":
            count += 1
    return count


def _thread_authors(thread: dict) -> set[str]:
    """Set of distinct comment-author logins on a thread (empty if none)."""
    authors: set[str] = set()
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        author = (comment.get("author") or {}).get("login")
        if author:
            authors.add(author)
    return authors
