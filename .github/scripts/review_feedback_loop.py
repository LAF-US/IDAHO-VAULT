#!/usr/bin/env python3
"""GitHub PR review-state automation helpers.

Modes:
  - ensure-labels: create/update the labels used by the review lifecycle.
  - acknowledge-apply: observe a trusted `@copilot apply changes` request and
    mark the PR as waiting on follow-up commits.
  - sync-pr: recompute review-derived state after PR updates land, auto-resolve
    outdated advisory bot threads, and synchronize projection labels.
  - review-submitted: recompute review-derived state after a submitted review
    and pause auto-merge only when a non-author changes-requested review creates
    a real merge block.
  - promote-ready: compatibility alias for scheduled reconciliation.
  - reconcile-open-prs: rescan open PR truth and repair drifted review labels.
    Agent-PR auto-merge arming is RE-ENABLED (2026-06-17, reversing the #521/#527
    fail-close) now that `main` lands through the GitHub merge queue — the queue +
    branch protection are the trust gate that arming waited on (ARBORSCAPE IF 12),
    so arming a low-risk, thread-clear PR means only "merge once the required
    checks/reviews/threads pass," not "a human approved." Arming is gated by the
    conservative eligibility (risk/low + grace + no blocking threads). Protected paths
    are no longer vetoed here — the CODEOWNERS hard gate enforces that. Dependabot keeps
    its own verified lane.
  - enable-auto-merge: arms an eligible PR for the merge queue.
    See AGENT-AUTOMERGE-REENABLED-2026-06-17.md for the recorded reversal.
  - verify-claim: compare an agent completion-claim comment against the PR's
    current `mergeable`, `mergeStateStatus`, draft state, and check rollup.
    Post a divergence comment if the claim disagrees with the institutional
    state. Addresses IF 7 from !/ARBORSCAPE-PR-EXPANSION-2026-05-22.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pr_threads import (  # shared thread-analysis vocabulary (#600 §5)
    ATTESTATION_DECISIONS,
    BARE_RESOLVABLE_DISPOSITIONS,
    _count_committable_suggestion_threads,
    _thread_authors,
    _thread_has_attested_look,
    _thread_is_bot_only,
    _thread_resolution_disposition,
    _thread_resolved_by,
)

# Note: `_author_is_bot` and `_thread_has_committable_suggestion` also live in
# pr_threads but are NOT imported here — the engine reaches them only transitively
# (through `_thread_resolution_disposition`), so the engine's surface stays honest
# to what it uses. Their unit tests reference them from pr_threads directly.

from gh_cli import run as _run
from pr_github import _fetch_pr, _graphql, _viewer_login


APPLY_RE = re.compile(r"@copilot\b[\s\S]*?\bapply changes\b", re.IGNORECASE)
DEFAULT_GRACE_MINUTES = 30
# Re-enabled 2026-06-17 (reverses the #521/#527 fail-close). The retirement waited on
# a trust gate distinct from author-login (#398 signing identity); the GitHub merge
# queue now IS that gate — a PR only merges once its required checks, reviews, and
# thread-resolution pass, regardless of who armed it (ARBORSCAPE IF 12 satisfied).
# Arming stays conservative: eligibility below requires risk/low + grace + no blocking
# threads. Protected-path gating moved to the CODEOWNERS hard gate (a merge can't land on
# an owned path without owner review), so the engine no longer vetoes it. This flag
# is the kill-switch — set False to fail-close arming again.
AGENT_AUTO_MERGE_ENABLED = True

# IF 7 (brass-mouth reliability is per-utterance, not per-agent) per
# !/ARBORSCAPE-PR-EXPANSION-2026-05-22.md. The verify-claim subcommand watches
# for agent completion-claim phrases in PR comments and posts a divergence note
# if GitHub's institutional state disagrees with the claim.
VERIFY_CLAIM_MARKER = "<!-- verify-claim:1 -->"

CLAIM_PATTERNS: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"\bready (?:to merge|for review|for termination|for archive)\b",
        r"\bclean(?:,| and)? pushed\b",
        r"\b(?:CODEX|CLAUDE|BROTHER|SISTER|GEMINI|COPILOT|MOXIE|MOGGET) COMPLETE\b",
        r"\bno further action pending\b",
        r"\bthe patient survived\b",
        r"\bwork finished\b",
    )
)

# Known-noise checks: failures here are not real signal per IF 1 in
# !/ARBORSCAPE-COMPLETION-REPORT-2026-05-17.md and the related Codex carve-out.
KNOWN_NOISE_CHECKS: frozenset[str] = frozenset(
    {
        "submit-pypi",
        "Automatic Dependency Submission (Python)",
    }
)

DEFAULT_REVIEW_REQUIRED_LABEL = "review/required"
DEFAULT_THREAD_LABEL = "review/threads-open"
DEFAULT_PENDING_LABEL = "merge/copilot-apply-pending"
DEFAULT_REVIEW_PENDING_LABEL = "review/pending"
DEFAULT_AUTO_MERGE_LABEL = "merge/auto"
DEFAULT_SUGGESTIONS_LABEL = "review/suggestions-ready"
RISK_LOW_LABEL = "risk/low"
RISK_MED_LABEL = "risk/med"
RISK_HIGH_LABEL = "risk/high"
RISK_NOPE_LABEL = "risk/nope"

# K6/#632 (flat schema, norm set by Logan): the risk vocabulary is four flat labels across
# two independent axes — each stamped ONLY when its axis fires. There are no prefixes, no
# explicit `—` labels, and no separate clear marker.
#   FILETYPE axis: risk/low (Machine Doc / inert assets) | risk/med (Computer Code — executes)
#   FILEDEPTH axis: risk/high (path inside the "!/" tree) | risk/nope (path in the inner
#                   "!/!/__!__/!/" region and below — never auto-merges)
# A PR carries AT MOST one filetype value AND at most one filedepth value (0–2 labels total).
# `—` on an axis is the ABSENCE of that axis's label; `—/—` (clear) is NO risk/* label at all.
# Flags are TRANSIENT ROUTING STATE, never a verdict: the classifier restamps them on
# synchronize (labels mirror the current diff), and when the lane's review completes the
# engine clears the fired flag (removes it) and the PR flows. risk/nope is never
# auto-cleared — it always requires a human merge.
FILETYPE_RISK_LABELS = {"low": RISK_LOW_LABEL, "med": RISK_MED_LABEL}
DEPTH_RISK_LABELS = {"high": RISK_HIGH_LABEL, "nope": RISK_NOPE_LABEL}
RISK_FLAG_LABELS = frozenset(
    {RISK_LOW_LABEL, RISK_MED_LABEL, RISK_HIGH_LABEL, RISK_NOPE_LABEL}
)
AUTO_MERGE_AUTHZ_FRAGMENTS = (
    "Pull request User is not authorized for this protected branch "
    "(enablePullRequestAutoMerge)",
    "Resource not accessible by integration (enablePullRequestAutoMerge)",
)

# Protected-path gating is no longer done here. A hand-maintained glob list was one of
# three drifting, fail-open re-implementations of "these paths need a human" (K1/#627,
# K2/#628). The single source of that truth is now CODEOWNERS, enforced as a HARD GATE by
# the branch ruleset (`require_code_owner_review: true`, set by Logan): GitHub blocks the
# merge of any owned-path PR until the owner reviews — un-bypassable, regardless of whether
# this engine armed it. So the engine no longer second-guesses protection; arming a
# protected PR is harmless because the gate, not a soft list, decides what actually merges.

LABEL_SPECS: dict[str, tuple[str, str]] = {
    DEFAULT_AUTO_MERGE_LABEL: (
        "0E8A16",
        "Legacy agent auto-merge marker; removed during reconciliation.",
    ),
    DEFAULT_REVIEW_REQUIRED_LABEL: (
        "D93F0B",
        "A merge-blocking review state currently exists.",
    ),
    DEFAULT_THREAD_LABEL: (
        "FBCA04",
        "Current unresolved review threads still need attention before merge.",
    ),
    DEFAULT_PENDING_LABEL: (
        "5319E7",
        "Waiting for a GitHub Copilot apply-changes follow-up push.",
    ),
    DEFAULT_REVIEW_PENDING_LABEL: (
        "BFD4F2",
        "Low-risk PR awaits review; automatic agent merge is disabled.",
    ),
    DEFAULT_SUGGESTIONS_LABEL: (
        "1D76DB",
        "Has bot review threads with committable ```suggestion blocks ready to apply.",
    ),
    # Flat 4-value risk schema — two axes, each label stamped only when its axis fires.
    RISK_LOW_LABEL: (
        "C2E0C6",
        "Filetype: low (machine documentation / inert assets).",
    ),
    RISK_MED_LABEL: (
        "F9D0C4",
        "Filetype: med (computer code — executes).",
    ),
    RISK_HIGH_LABEL: (
        "E99695",
        "Filedepth: high (path inside the \"!/\" tree).",
    ),
    RISK_NOPE_LABEL: (
        "B60205",
        "Filedepth: nope (inner \"!/!/__!__/!/\" region and below; never auto-merges).",
    ),
}


def _auto_merge_state(owner: str, repo: str, pr_number: int) -> tuple[bool, bool]:
    """Return ``(auto_merge_enabled, in_merge_queue)`` for the PR.

    Fail-open to ``(False, False)``: if the state can't be read, the caller
    behaves exactly as it did before this guard existed (a plain ``--auto``
    enable) — never worse than the old code, and a transient read error never
    evicts a queued PR."""
    try:
        data = _graphql(
            """
            query($owner:String!, $name:String!, $number:Int!) {
              repository(owner: $owner, name: $name) {
                pullRequest(number: $number) {
                  autoMergeRequest { enabledAt }
                  mergeQueueEntry { id }
                }
              }
            }
            """,
            owner=owner,
            name=repo,
            number=pr_number,
        )
    except (RuntimeError, ValueError):
        # RuntimeError: gh/_graphql failure or GraphQL errors.
        # ValueError: a malformed JSON payload (json.JSONDecodeError subclasses it).
        # Both fail open so the arming path keeps its pre-guard behavior.
        return (False, False)
    pull = (data.get("repository") or {}).get("pullRequest") or {}
    enabled = bool((pull.get("autoMergeRequest") or {}).get("enabledAt"))
    queued = bool((pull.get("mergeQueueEntry") or {}).get("id"))
    return (enabled, queued)


def _merge_state_status(owner: str, repo: str, pr_number: int) -> str:
    """The PR's current ``mergeStateStatus`` (``CLEAN``/``UNSTABLE``/``BEHIND``/``BLOCKED``/
    ``DIRTY``/``UNKNOWN``/...). Fail-open to ``"UNKNOWN"`` on a read failure — the caller's
    BEHIND-only branch-update path then simply does not fire this cycle, exactly as if the
    PR were not yet BEHIND; a later sync-pr/reconcile-open-prs pass re-reads it."""
    try:
        data = _graphql(
            """
            query($owner:String!, $name:String!, $number:Int!) {
              repository(owner: $owner, name: $name) {
                pullRequest(number: $number) { mergeStateStatus }
              }
            }
            """,
            owner=owner,
            name=repo,
            number=pr_number,
        )
    except (RuntimeError, ValueError):
        return "UNKNOWN"
    pull = (data.get("repository") or {}).get("pullRequest") or {}
    return pull.get("mergeStateStatus") or "UNKNOWN"


def _pr_node_id(owner: str, repo: str, pr_number: int) -> str | None:
    """The PR's GraphQL node id (required by enqueuePullRequest). None if it can't be read
    (fail-open: the caller then skips the explicit enqueue and relies on armed auto-merge)."""
    try:
        data = _graphql(
            """
            query($owner:String!, $name:String!, $number:Int!) {
              repository(owner: $owner, name: $name) {
                pullRequest(number: $number) { id }
              }
            }
            """,
            owner=owner,
            name=repo,
            number=pr_number,
        )
    except (RuntimeError, ValueError):
        return None
    return ((data.get("repository") or {}).get("pullRequest") or {}).get("id")


def _enqueue_pr(node_id: str) -> tuple[bool, str | None]:
    """Add the PR to the merge queue via the ``enqueuePullRequest`` mutation — the action that
    actually puts a PR in the queue, DISTINCT from ``enablePullRequestAutoMerge`` ("merge when
    ready"). Best-effort: never raises.

    Returns a tri-state ``(enqueued, error)`` so the caller can tell a benign delay from a real
    failure:

      * ``(True, None)``  — enqueued (a merge-queue entry id came back).
      * ``(False, None)`` — benign: the PR is not yet queue-ready (required checks still running,
        not mergeable, or the base branch has no merge queue). GitHub returns no entry; the armed
        auto-merge enqueues it when it goes green. NOT an error.
      * ``(False, str)``  — a real failure (auth/permission/API error from the mutation), worth
        surfacing because an armed PR that silently never enqueues is exactly the bug this fixes."""
    try:
        data = _graphql(
            "mutation($pr:ID!){ enqueuePullRequest(input:{pullRequestId:$pr})"
            " { mergeQueueEntry { id } } }",
            pr=node_id,
        )
    except (RuntimeError, ValueError) as exc:
        return (False, str(exc))
    entry = (((data.get("enqueuePullRequest") or {}).get("mergeQueueEntry")) or {}).get("id")
    if entry:
        return (True, None)
    return (False, None)  # not queue-ready yet — benign; armed auto-merge enqueues it when green


def _update_branch(owner: str, repo: str, pr_number: int) -> tuple[bool, str | None]:
    """Merge the base branch into the PR head via the ``update-branch`` REST endpoint — the
    automated form of the "Update branch" button, and the same call
    ``batch-arm-merge-queue.yml`` already uses on a BEHIND PR (that manual bulk sweep's proven
    fix; this brings the same recovery to the event-driven engine, which previously just left
    a BEHIND PR waiting indefinitely for someone else to push). Best-effort: never raises.

    Returns ``(updated, error)``:
      * ``(True, None)`` — the request succeeded; a merge commit landed on the PR head, CI
        re-runs, and a later pass re-reads ``mergeStateStatus`` once it recomputes to CLEAN.
      * ``(False, str)`` — the request failed (e.g. a real conflict surfaced as DIRTY by the
        time this ran, or a workflows-permission error on a workflow-touching PR — the same
        failure mode ``is_wf_perm_failure`` buckets separately in the bash sweep)."""
    try:
        _run(
            [
                "gh",
                "api",
                "--method",
                "PUT",
                f"repos/{owner}/{repo}/pulls/{pr_number}/update-branch",
            ]
        )
    except RuntimeError as exc:
        return (False, str(exc))
    return (True, None)


def _arm_auto_merge(owner: str, repo: str, pr_number: int) -> tuple[bool, str | None]:
    """Arm auto-merge for the PR, update its branch if BEHIND, AND add it to the merge queue —
    three DISTINCT GitHub actions:

      1. **enablePullRequestAutoMerge** (`gh pr merge --auto`) — records "merge when ready."
         On a merge-queue repo this ALONE does not put the PR in the queue.
      2. **update-branch** (REST) — when the head is BEHIND base, neither arming nor enqueuing
         can make the PR CLEAN; merging base in is what lets it recompute. Without this, a
         BEHIND PR just sits waiting for an unrelated event to nudge it (previously only
         `batch-arm-merge-queue.yml`'s manual bulk sweep did this).
      3. **enqueuePullRequest** (GraphQL) — the action that actually adds the PR to the merge
         queue. This is the half that was missing: arming-only left a ready PR sitting
         un-queued (the #508 symptom) because nothing ever called enqueue.

    Returns ``(armed, error)``. ``armed`` is True once auto-merge is on (the floor). Both the
    update-branch and enqueue steps are best-effort and folded into ``error`` as an
    informational note when they don't succeed outright — neither is treated as arming having
    failed, since a not-yet-ready or still-BEHIND PR is expected to need another pass."""
    enabled, queued = _auto_merge_state(owner, repo, pr_number)
    if queued:
        # Already in the queue — re-enqueuing would be a no-op (or an unwanted jump); leave it.
        return (True, None)
    notes: list[str] = []
    if _merge_state_status(owner, repo, pr_number) == "BEHIND":
        # DIRTY (a real conflict) is a different state and never reaches here, so update-branch
        # is only attempted when it can actually succeed. Checked regardless of `enabled`: a PR
        # can already be armed and still fall BEHIND later.
        updated, update_error = _update_branch(owner, repo, pr_number)
        notes.append(
            "branch updated (was BEHIND)"
            if updated
            else f"branch update (BEHIND) failed: {update_error}"
        )
    if not enabled:
        try:
            # K5/#631 (norm set 2026-07-06): the merge QUEUE's configured method is the
            # single merge-method norm. gh syntax requires a method flag, but on a
            # merge-queue repo the queue overrides it — `--merge` is the one canonical,
            # inert spelling everywhere (test_workflow_security_invariants enforces it).
            # NO --delete-branch: gh rejects it outright on merge-queue repos
            # ("Cannot use `-d` or `--delete-branch` when merge queue enabled"),
            # which crashed every arm attempt. Head-branch cleanup belongs to the
            # repo's delete-on-merge behavior / branch-cleanup workflow, not here.
            _run(["gh", "pr", "merge", str(pr_number), "--merge", "--auto"])
        except RuntimeError as exc:
            if not any(fragment in str(exc) for fragment in AUTO_MERGE_AUTHZ_FRAGMENTS):
                raise
            notes.insert(
                0,
                "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
            )
            return (False, "; ".join(notes))
    # Arming is only half the job — explicitly add it to the merge queue now.
    node_id = _pr_node_id(owner, repo, pr_number)
    if node_id:
        enqueued, enqueue_error = _enqueue_pr(node_id)
        if not enqueued and enqueue_error:
            # Armed, but the explicit enqueue hit a REAL error (auth/API) — distinct from the
            # benign "not queue-ready yet" case (which returns no error and is left for the
            # armed auto-merge to enqueue when green). Surface it so the "armed but never
            # queued" failure this PR fixes can't recur silently. Still armed=True.
            notes.append(f"enqueue was rejected: {enqueue_error}")
    # node_id None (fail-open) or benign not-ready: armed; auto-merge enqueues it when green.
    return (True, "; ".join(notes)) if notes else (True, None)


def _maybe_arm_auto_merge(
    owner: str, repo: str, pr_number: int, state: dict[str, object]
) -> dict[str, object]:
    """Guarded arm: enable merge-queue auto-merge for a PR ONLY when it is eligible
    (risk/low + grace + no blocking threads, per evaluate_review_state). Returns a small
    report; never raises for the ordinary not-eligible or not-authorized cases. Protected
    paths are NOT vetoed here — the CODEOWNERS hard gate (require_code_owner_review) blocks
    their merge regardless of arming; the merge queue + branch protection are the actual
    merge gate, and this only presses the button."""
    if not bool(state.get("eligible_for_auto_merge")):
        return {"armed": False, "reason": "not eligible for auto-merge"}
    armed, arm_error = _arm_auto_merge(owner, repo, pr_number)
    if armed:
        # Tag the PR `merge/auto` so the disable path (apply_review_state_projection,
        # which keys disablement on this label) can later un-arm it if a new thread or a
        # CHANGES_REQUESTED review makes it merge_blocked. Without the label an
        # event-armed PR could stay armed while the engine's own state said "blocked."
        # Fail closed: if the label write fails, the disable path could never un-arm it,
        # so disable the auto-merge we just enabled and report failure rather than leave
        # an un-trackable armed PR.
        try:
            _run(["gh", "pr", "edit", str(pr_number), "--add-label", DEFAULT_AUTO_MERGE_LABEL])
        except RuntimeError as exc:
            _disable_auto_merge(pr_number)
            return {
                "armed": False,
                "reason": (
                    f"auto-merge armed but `{DEFAULT_AUTO_MERGE_LABEL}` label write failed; "
                    f"disabled auto-merge to avoid an un-trackable armed PR: {exc}"
                ),
            }
    # Pass arm_error through even when armed: a clean arm reports None, but an armed PR whose
    # explicit enqueue was rejected carries that note so "armed but never queued" isn't silent.
    return {"armed": armed, "reason": arm_error}


def _resolve_thread(thread_id: str) -> None:
    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { id isResolved }
      }
    }
    """
    _graphql(mutation, threadId=thread_id)


# Look-then-resolve design (#399): nothing is dismissed or resolved until a
# looker (agent or human) has looked. A looker records the look as an in-thread
# attestation comment of this canonical shape:
#   <!-- looked: by=<login>; at=<iso8601>; decision=<addressed|advisory|wontfix>; v=1 -->
# Detection requires the structured marker AND that `by` matches the comment's
# own author, so a pasted or forged marker attributed to someone else cannot
# fake a look. This layer RESOLVES NOTHING.
LOOK_ATTESTATION_MARKER = "<!-- looked:"


def _build_attestation(
    looker: str,
    decision: str,
    rationale: str,
    *,
    now: datetime | None = None,
) -> str:
    """Build the canonical in-thread attestation body a looker leaves on resolve.

    Round-trips through `_thread_has_attested_look`: detected only when posted as a
    comment whose author login equals `looker`. The `looker` must match the detector's
    `by=` grammar — `[A-Za-z0-9][A-Za-z0-9-]*` with an optional trailing `[bot]` — so
    both a plain login (`claude-code-bot`, `coderabbitai`) and a GitHub App identity
    (`github-actions[bot]`) are accepted (the B2 standing/identity decision: a looker
    may sign under its native CI identity). A malformed login is rejected here rather
    than producing an attestation the detector can never match.
    """
    if decision not in ATTESTATION_DECISIONS:
        raise ValueError(
            f"decision {decision!r} is not one of {sorted(ATTESTATION_DECISIONS)}"
        )
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*(?:\[bot\])?", looker):
        raise ValueError(
            f"looker {looker!r} must match the attestation grammar "
            r"[A-Za-z0-9][A-Za-z0-9-]*(\[bot\])? (a plain login or an App "
            "identity such as github-actions[bot])"
        )
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:  # treat a naive datetime as UTC, never as local
        moment = moment.replace(tzinfo=timezone.utc)
    stamp = moment.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    marker = f"<!-- looked: by={looker}; at={stamp}; decision={decision}; v=1 -->"
    return f"Looked by `{looker}` — **{decision}**. {rationale}\n\n{marker}"


# Layer B2 (#399): the guarded disposition core. `attest_and_resolve` is the ONLY
# resolve path a looker uses — it records an attested look (a thread reply) and then
# resolves that one thread.
#
# Cascade-safety contract (see #399 looker spec): this NEVER merges and NEVER enables
# auto-merge. Most of the open-PR backlog was opened by agents that are no longer
# active, often under the maintainer identity, and auto-merge is armed on those PRs —
# so clearing a thread must not be able to shove abandoned work through the merge
# barrier. The rule "do not clear the LAST blocking thread on an auto-merge-armed PR
# without a deliberate signal" is the orchestrator's (Layer C) job, not this function's.
def _add_thread_reply(thread_id: str, body: str) -> None:
    """Post a reply on a review thread — the looker's recorded, auditable attestation."""
    mutation = """
    mutation($threadId: ID!, $body: String!) {
      addPullRequestReviewThreadReply(
        input: {pullRequestReviewThreadId: $threadId, body: $body}
      ) {
        comment { id }
      }
    }
    """
    _graphql(mutation, threadId=thread_id, body=body)


def _fetch_thread(thread_id: str) -> dict | None:
    """Fetch one review thread node directly by GraphQL ID.

    A fallback for when an explicit target thread sits beyond `_fetch_pr`'s
    `reviewThreads(first: 100)` window (a PR with >100 threads), so a valid id is
    not falsely reported missing. Returns the same node shape as the PR query.
    """
    query = """
    query($id: ID!) {
      node(id: $id) {
        ... on PullRequestReviewThread {
          id
          isResolved
          isOutdated
          comments(first: 100) {
            pageInfo { hasNextPage }
            nodes { author { login __typename } body url }
          }
        }
      }
    }
    """
    data = _graphql(query, id=thread_id)
    node = data.get("node") or {}
    # A node id that exists but is not a review thread yields {} (the inline fragment
    # doesn't apply) — treat that as missing, not as a thread with no id.
    return node if node.get("id") else None


def attest_and_resolve(
    pr: dict,
    thread: dict,
    looker: str,
    decision: str,
    rationale: str,
    *,
    apply: bool = False,
    now: datetime | None = None,
) -> dict:
    """Disposition ONE bot-authored review thread: resolve it, then record the attested look.

    Writes nothing unless `apply=True`. NEVER merges and NEVER enables auto-merge — it
    resolves that single thread and posts the looker's attestation as a thread reply,
    nothing else (the cascade-safety contract above).

    Order matters: the resolve runs FIRST, and the "thread cleared" attestation is posted
    only after it succeeds. The attestation asserts a clearing; if the resolve fails
    (e.g. `resolveReviewThread` is FORBIDDEN for the integration token — the live #398
    boundary), a comment claiming the thread was cleared would be a FALSE witness. A true
    witness that is sometimes absent beats a witness that is sometimes a lie, so we never
    attest a clearing we did not actually perform.

    Eligibility is reported, never raised. A thread is eligible when the PR's review is
    not CHANGES_REQUESTED, every author is a bot (`_thread_is_bot_only` — never a human
    thread, and only when the comment page is complete enough to prove it), and the
    thread is not already resolved. An eligible thread that already carries an attested
    look but is still open is resolved WITHOUT re-posting (partial-success recovery); a
    fully resolved thread is a no-op.

    Returns a result dict: {thread_id, eligible, applied, reason, attestation?}.
    """
    thread_id = thread.get("id")
    result: dict[str, object] = {
        "thread_id": thread_id,
        "eligible": False,
        "applied": False,
        "reason": "",
    }

    if not thread_id:
        result["reason"] = "thread has no id"
        return result
    if (pr.get("reviewDecision") or "") == "CHANGES_REQUESTED":
        result["reason"] = "pr review is CHANGES_REQUESTED"
        return result
    if thread.get("isResolved"):
        result["reason"] = "thread already resolved"
        return result
    # Bot-only authorship must be proven from the FULL comment list. If the page is
    # truncated, a human past the first page could hide behind the bot-only guard —
    # refuse rather than resolve on incomplete evidence.
    if ((thread.get("comments") or {}).get("pageInfo") or {}).get("hasNextPage"):
        result["reason"] = "thread comments are paginated; cannot prove bot-only authorship"
        return result
    if not _thread_is_bot_only(thread):
        result["reason"] = "thread is not bot-authored only"
        return result
    # "Resolve, then look" is two separate mutations. An already-attested but still
    # OPEN thread is a partial success from a PRIOR ordering (the reply landed, the
    # resolve did not) — recover by resolving without posting a duplicate attestation,
    # rather than no-op'ing and leaving the thread blocking forever. The fully-done case
    # (attested AND resolved) is already short-circuited by the isResolved guard above.
    already_looked = _thread_has_attested_look(thread)

    # Build (and thereby validate looker/decision) before any write.
    body = _build_attestation(looker, decision, rationale, now=now)
    result["eligible"] = True
    result["attestation"] = body
    if not apply:
        result["reason"] = (
            "dry-run: attested look already present, would resolve"
            if already_looked
            else "dry-run: would resolve and record attested look"
        )
        return result

    # Validate the looker/actor match BEFORE touching the thread: the look is
    # self-attested (the marker says by={looker}, but the reply posts as the
    # authenticated actor). If they differ we cannot write a truthful witness, so we
    # must not resolve either — clearing a thread we cannot witness is the unwitnessed
    # ending we are built to avoid. Skip the check when no new attestation will be
    # posted (already_looked recovery path).
    if not already_looked:
        actor = _viewer_login()
        if actor != looker:
            result["eligible"] = False
            result["reason"] = (
                f"looker {looker!r} does not match the authenticated actor {actor!r}"
            )
            return result

    # Resolve FIRST. If this raises (e.g. FORBIDDEN for the integration token), it
    # propagates to the caller and NO attestation is posted — the thread keeps its
    # honest unresolved state instead of gaining a false "cleared" claim.
    _resolve_thread(thread_id)
    # The clearing succeeded; now the "thread cleared" attestation is true. Skip the
    # post on the recovery path (the attestation is already present from a prior run).
    if not already_looked:
        _add_thread_reply(thread_id, body)
    result["applied"] = True
    result["reason"] = (
        "existing attested look; thread resolved"
        if already_looked
        else "thread resolved; attested look recorded"
    )
    return result


def backfill_witness(
    pr: dict,
    thread: dict,
    looker: str,
    rationale: str,
    *,
    apply: bool = False,
    now: datetime | None = None,
) -> dict:
    """Backfill a missing attestation on a thread WE resolved but never witnessed.

    The unwitnessed-ending repair. A resolve that succeeds while its attestation post
    does not (the resolve-first ordering's partial failure, or any interrupted run)
    leaves a thread *resolved with no recorded look* — exactly the blind resolution the
    engine exists to prevent. This repairs that ONE case and only that case:

      - the thread is already resolved (otherwise use `attest-resolve`/`engage-outdated`);
      - it carries NO attestation yet (nothing to repair otherwise);
      - every author is a bot, proven from a complete comment page;
      - and `resolvedBy` is the looker itself — *we* resolved it.

    It posts the missing attestation and does NOTHING else: it never resolves (already
    resolved) and never unresolves. The `resolvedBy == looker` gate is the truthfulness
    line — we never mint a witness for a resolve performed by a human or another actor.

    Writes nothing unless `apply=True`. Returns {thread_id, eligible, applied, reason,
    attestation?}.
    """
    thread_id = thread.get("id")
    result: dict[str, object] = {
        "thread_id": thread_id,
        "eligible": False,
        "applied": False,
        "reason": "",
    }
    if not thread_id:
        result["reason"] = "thread has no id"
        return result
    if not thread.get("isResolved"):
        result["reason"] = "thread is not resolved (nothing to backfill; use attest-resolve)"
        return result
    if _thread_has_attested_look(thread):
        result["reason"] = "thread already carries an attested look"
        return result
    if ((thread.get("comments") or {}).get("pageInfo") or {}).get("hasNextPage"):
        result["reason"] = "thread comments are paginated; cannot prove bot-only authorship"
        return result
    if not _thread_is_bot_only(thread):
        result["reason"] = "thread is not bot-authored only"
        return result
    resolver = _thread_resolved_by(thread)
    if resolver != looker:
        # The truthfulness line: only backfill a witness for OUR OWN resolve.
        result["reason"] = (
            f"thread resolved by {resolver!r}, not the looker {looker!r} — "
            "refusing to witness another identity's resolve"
        )
        return result

    # Build (and thereby validate looker) before any write. The decision is `advisory`:
    # the look records that the resolution stands, not that a fix was applied.
    body = _build_attestation(looker, "advisory", rationale, now=now)
    result["eligible"] = True
    result["attestation"] = body
    if not apply:
        result["reason"] = "dry-run: would backfill the missing attestation"
        return result

    # Self-attestation guard: the marker says by={looker}; it must equal the actor that
    # actually posts, or the attestation is undetectable.
    actor = _viewer_login()
    if actor != looker:
        result["eligible"] = False
        result["reason"] = (
            f"looker {looker!r} does not match the authenticated actor {actor!r}"
        )
        return result
    _add_thread_reply(thread_id, body)
    result["applied"] = True
    result["reason"] = "missing attestation backfilled (thread already resolved)"
    return result


def _ensure_label(name: str, color: str, description: str) -> None:
    _run(
        [
            "gh",
            "label",
            "create",
            name,
            "--color",
            color,
            "--description",
            description,
            "--force",
        ]
    )


def ensure_labels() -> None:
    for label, (color, description) in LABEL_SPECS.items():
        _ensure_label(label, color, description)


def _edit_label(pr_number: int, *, add: str | None = None, remove: str | None = None) -> None:
    if add:
        _run(["gh", "pr", "edit", str(pr_number), "--add-label", add], check=False)
    if remove:
        _run(["gh", "pr", "edit", str(pr_number), "--remove-label", remove], check=False)


def _disable_auto_merge(pr_number: int, *, check: bool = False) -> None:
    _run(["gh", "pr", "merge", str(pr_number), "--disable-auto"], check=check)


def _comment(pr_number: int, body: str) -> None:
    _run(["gh", "pr", "comment", str(pr_number), "--body", body])


def _csv_env(name: str, default: str = "") -> set[str]:
    raw = os.environ.get(name, default)
    return {item.strip() for item in raw.split(",") if item.strip()}


def _parse_iso_datetime(raw: str | None) -> datetime | None:
    if not raw:
        return None
    normalized = raw
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _parse_body_marker_value(body: str, marker: str) -> str | None:
    lines = body.splitlines()
    needle = marker.strip().lower()
    for index, line in enumerate(lines):
        if line.strip().lower() != needle:
            continue
        for candidate in lines[index + 1:]:
            stripped = candidate.strip()
            if not stripped:
                continue
            return stripped.strip("`").strip().lower()
    return None


class RiskMarkerInvariantError(ValueError):
    """A per-axis risk-marker invariant was violated: two values on a single axis.

    A dedicated type (not a bare ValueError) so callers can catch EXACTLY this breach
    and never mistake an unrelated ValueError from the evaluate path for an invariant
    violation. Subclasses ValueError so existing broad handlers still degrade safely."""


def _assert_risk_marker_exclusive(labels: set[str]) -> None:
    """Fail loud on the one state the flat schema forbids: two values on a single axis.

    Each axis carries AT MOST one flat label — risk/low XOR risk/med on the filetype
    axis, risk/high XOR risk/nope on the filedepth axis. Both values on one axis is a
    producer/backfill bug, not a routing decision — raise so it can never silently route
    a PR whose axis is self-contradictory."""
    if RISK_LOW_LABEL in labels and RISK_MED_LABEL in labels:
        raise RiskMarkerInvariantError(
            f"risk-marker invariant violated: the filetype axis carries both "
            f"{RISK_LOW_LABEL} and {RISK_MED_LABEL}. Each axis carries at most ONE "
            f"value, never both."
        )
    if RISK_HIGH_LABEL in labels and RISK_NOPE_LABEL in labels:
        raise RiskMarkerInvariantError(
            f"risk-marker invariant violated: the filedepth axis carries both "
            f"{RISK_HIGH_LABEL} and {RISK_NOPE_LABEL}. Each axis carries at most ONE "
            f"value, never both."
        )


def _risk_pair_for_pr(labels: set[str]) -> tuple[str | None, str | None, bool]:
    """(filetype_flag, depth_flag, classified) — the lane, read off the flat labels.

    ``filetype_flag`` is "med"/"low"/None; ``depth_flag`` is "nope"/"high"/None.
    ``classified`` is True iff ANY risk/* flag is present — no flag present means we
    cannot confirm the PR was classified from labels alone (an all-absent PR is NOT
    classified-clear: it holds until an affirmative verdict says otherwise)."""
    filetype_flag = (
        "med" if RISK_MED_LABEL in labels
        else "low" if RISK_LOW_LABEL in labels
        else None
    )
    depth_flag = (
        "nope" if RISK_NOPE_LABEL in labels
        else "high" if RISK_HIGH_LABEL in labels
        else None
    )
    classified = bool(labels & RISK_FLAG_LABELS)
    return (filetype_flag, depth_flag, classified)


def _validate_pair(filetype_flag: str | None, depth_flag: str | None) -> None:
    """Fail loud (RiskMarkerInvariantError) on an out-of-vocabulary axis flag, so a caller
    typo (e.g. "medium" for "med") gets a deterministic, domain-specific error instead of a
    silent misroute (`_tier_from_pair`) or a raw KeyError (`restamp_risk_pair`)."""
    if filetype_flag not in (None, "low", "med"):
        raise RiskMarkerInvariantError(
            f"invalid filetype_flag {filetype_flag!r}: expected None, 'low', or 'med'"
        )
    if depth_flag not in (None, "high", "nope"):
        raise RiskMarkerInvariantError(
            f"invalid depth_flag {depth_flag!r}: expected None, 'high', or 'nope'"
        )


def _tier_from_pair(filetype_flag: str | None, depth_flag: str | None, marked: bool) -> str:
    """Collapse a lane pair to the single-tier vocabulary (nope>high>med>low>clear);
    an incompletely marked PR is `unknown` and HOLDS. Fails loud on an out-of-vocabulary
    flag (e.g. a caller-supplied `verdict` typo like "medium") instead of letting it fall
    through to `clear` and misroute the PR."""
    _validate_pair(filetype_flag, depth_flag)
    if not marked:
        return "unknown"
    if depth_flag == "nope":
        return "nope"
    if depth_flag == "high":
        return "high"
    if filetype_flag == "med":
        return "med"
    if filetype_flag == "low":
        return "low"
    return "clear"


def _classify_pr_pair(owner: str, repo: str, pr_number: int) -> tuple[str | None, str | None]:
    """Run the two parallel analyses (classify_paths) over the PR's changed files.

    The classifier is the SINGLE source of both axes (K1/K2); this is the engine-side
    bridge that lets the restamp mirror the current diff on synchronize. Raises on any
    API/import failure — callers fail SAFE by keeping the existing labels (a PR is never
    armed off a failed classification; an unmarked PR holds)."""
    import classify_paths  # sibling module; scripts dir is on sys.path in script + test runs

    result = _run(
        [
            "gh", "api", "--paginate",
            f"repos/{owner}/{repo}/pulls/{pr_number}/files",
            "--jq", ".[].filename",
        ]
    )
    paths = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    filetype = None
    depth = None
    for path in paths:
        ft, dp = classify_paths.classify_file(path)
        filetype = classify_paths.riskiest(filetype, ft)
        depth = classify_paths.riskiest(depth, dp)
    return (filetype, depth)


def restamp_risk_pair(
    pr_number: int,
    labels: set[str],
    filetype_flag: str | None,
    depth_flag: str | None,
) -> list[str]:
    """Make the PR's risk labels mirror the classifier's verdict — the 'restamp'.

    ``desired`` is the flat label for each fired axis: the filetype label if
    ``filetype_flag`` is set, plus the filedepth label if ``depth_flag`` is set. A `—/—`
    verdict (both None) yields an EMPTY desired set — a clear verdict stamps nothing and
    removes any stale risk/* label. ``managed`` is the full flat set, so managed-not-desired
    labels are removed. Mutates ``labels`` in place and returns the actions taken."""
    _validate_pair(filetype_flag, depth_flag)
    actions: list[str] = []
    desired: set[str] = set()
    if filetype_flag is not None:
        desired.add(FILETYPE_RISK_LABELS[filetype_flag])
    if depth_flag is not None:
        desired.add(DEPTH_RISK_LABELS[depth_flag])
    managed = set(RISK_FLAG_LABELS)
    for label in sorted(desired - labels):
        _edit_label(pr_number, add=label)
        labels.add(label)
        actions.append(f"add:{label}")
    for label in sorted((labels & managed) - desired):
        _edit_label(pr_number, remove=label)
        labels.discard(label)
        actions.append(f"remove:{label}")
    return actions


def evaluate_review_state(
    pr: dict,
    *,
    now: datetime | None = None,
    grace_minutes: int = DEFAULT_GRACE_MINUTES,
    auto_resolve_reviewers: set[str] | None = None,
    verdict: tuple[str | None, str | None] | None = None,
) -> dict[str, object]:
    """Return one machine-readable view of the PR's current review state.

    ``verdict`` is an optional caller-supplied ``(filetype_flag, depth_flag)`` straight
    from the classifier — passed by the POST-classify evaluate calls so a `—/—` verdict
    is affirmatively clear even with zero labels. Without a verdict the flags are read off
    the labels, and an all-absent PR is ``unknown`` and HOLDS (never armed) — the safety
    property that absence of a label is not the clear state."""

    label_names = {
        node["name"]
        for node in (pr.get("labels") or {}).get("nodes") or []
        if node.get("name")
    }
    auto_resolve_reviewers = auto_resolve_reviewers or set()

    current_unresolved = 0
    outdated_unresolved = 0
    auto_resolvable_outdated = 0

    for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
        if thread.get("isResolved"):
            continue

        authors = _thread_authors(thread)
        if thread.get("isOutdated"):
            outdated_unresolved += 1
            if authors and authors.issubset(auto_resolve_reviewers):
                auto_resolvable_outdated += 1
            continue

        current_unresolved += 1

    created_at = _parse_iso_datetime(pr.get("createdAt"))
    current_time = now or datetime.now(timezone.utc)
    grace_elapsed = False
    if created_at is not None:
        grace_elapsed = (current_time - created_at).total_seconds() >= grace_minutes * 60

    review_decision = pr.get("reviewDecision")
    draft = bool(pr.get("isDraft"))
    blocking_review = review_decision == "CHANGES_REQUESTED"
    _assert_risk_marker_exclusive(label_names)
    # The lane is the flat (filetype, depth) pair. A caller-supplied verdict (the classifier's
    # fresh reading) is authoritative and always "marked" — so a `—/—` verdict is affirmatively
    # clear even with zero labels. Without a verdict the flags are read off the labels, and an
    # all-absent PR is NOT marked (unknown, holds — absence of a label is not the clear state).
    if verdict is not None:
        filetype_flag, depth_flag = verdict
        pair_marked = True
    else:
        filetype_flag, depth_flag, pair_marked = _risk_pair_for_pr(label_names)
    risk_tier = _tier_from_pair(filetype_flag, depth_flag, pair_marked)
    is_clear = pair_marked and filetype_flag is None and depth_flag is None
    low_risk = risk_tier == "low"
    merge_blocked = draft or blocking_review or current_unresolved > 0
    # K6 lane completion — flags are transient routing state, consumed as the PR clears
    # its lane: an approving review with no current threads completes the lane, the engine
    # clears the fired flag (the projection removes the fired flat risk/* label), and the PR
    # flows. depth:nope is NEVER auto-cleared — it always requires a human merge.
    lane_complete = (
        review_decision == "APPROVED" and current_unresolved == 0 and not draft
    )
    flag_clearable = (
        pair_marked
        and depth_flag != "nope"
        and (filetype_flag is not None or depth_flag is not None)
    )
    # K3/#629 + K6: the `—/—` pair arms on open; a flagged lane arms once its review
    # completes (the flag is consumed). nope and any unmarked PR HOLD, always.
    eligible_for_auto_merge = (
        AGENT_AUTO_MERGE_ENABLED
        and grace_elapsed
        and not merge_blocked
        and (is_clear or (lane_complete and flag_clearable))
    )
    should_have_agent_review_pending = (
        AGENT_AUTO_MERGE_ENABLED
        and low_risk
        and DEFAULT_AUTO_MERGE_LABEL not in label_names
        and not eligible_for_auto_merge
    )

    blocking_reasons: list[str] = []
    if draft:
        blocking_reasons.append("draft")
    if blocking_review:
        blocking_reasons.append("changes-requested")
    if current_unresolved > 0:
        blocking_reasons.append("current-review-threads")

    return {
        "number": pr.get("number"),
        "url": pr.get("url"),
        "labels": sorted(label_names),
        "risk_tier": risk_tier,
        "low_risk": low_risk,
        "is_clear": is_clear,
        "pair": {"filetype": filetype_flag, "depth": depth_flag},
        "pair_marked": pair_marked,
        "lane_complete": lane_complete,
        "flag_clearable": flag_clearable,
        "draft": draft,
        "review_decision": review_decision,
        "blocking_review": blocking_review,
        "current_unresolved_threads": current_unresolved,
        "outdated_unresolved_threads": outdated_unresolved,
        "auto_resolvable_outdated_threads": auto_resolvable_outdated,
        "committable_suggestion_threads": _count_committable_suggestion_threads(pr),
        "merge_blocked": merge_blocked,
        "blocking_reasons": blocking_reasons,
        "grace_elapsed": grace_elapsed,
        "eligible_for_auto_merge": eligible_for_auto_merge,
        "should_have_agent_review_pending": should_have_agent_review_pending,
        "has_copilot_apply_pending": DEFAULT_PENDING_LABEL in label_names,
    }


def apply_review_state_projection(
    pr_number: int,
    state: dict[str, object],
    *,
    clear_apply_pending: bool = False,
) -> list[str]:
    """Synchronize projection labels so they reflect the evaluated review state."""

    current_labels = set(state.get("labels") or [])
    actions: list[str] = []

    desired_labels = {
        DEFAULT_REVIEW_REQUIRED_LABEL: bool(state["blocking_review"]),
        DEFAULT_THREAD_LABEL: int(state["current_unresolved_threads"]) > 0,
        DEFAULT_REVIEW_PENDING_LABEL: bool(state["should_have_agent_review_pending"]),
        # Propose-only (#3): flag PRs that have committable suggestions ready to apply.
        # Add/remove is idempotent, so no comment spam; the signal mirrors to Linear.
        DEFAULT_SUGGESTIONS_LABEL: int(state.get("committable_suggestion_threads") or 0) > 0,
    }

    for label, wanted in desired_labels.items():
        has_label = label in current_labels
        if wanted and not has_label:
            _edit_label(pr_number, add=label)
            actions.append(f"add:{label}")
            current_labels.add(label)
        elif not wanted and has_label:
            _edit_label(pr_number, remove=label)
            actions.append(f"remove:{label}")
            current_labels.discard(label)

    if clear_apply_pending and DEFAULT_PENDING_LABEL in current_labels:
        _edit_label(pr_number, remove=DEFAULT_PENDING_LABEL)
        actions.append(f"remove:{DEFAULT_PENDING_LABEL}")
        current_labels.discard(DEFAULT_PENDING_LABEL)

    # Clear-on-completion: the lane's review completed, so the fired flag is CONSUMED —
    # restamp to `—/—`, removing every risk/* flag (a clear verdict stamps none). The next
    # synchronize (new code) restamps from the classifier and re-enters the lane; with no
    # new code the cleared (label-free) PR becomes eligible and flows once the grace window
    # elapses. nope is never flag_clearable.
    if bool(state.get("lane_complete")) and bool(state.get("flag_clearable")):
        actions.extend(
            restamp_risk_pair(pr_number, current_labels, None, None)
        )

    if (
        DEFAULT_AUTO_MERGE_LABEL in current_labels
        and (
            bool(state["merge_blocked"])
            or not bool(state["eligible_for_auto_merge"])
        )
    ):
        _disable_auto_merge(pr_number)
        _edit_label(pr_number, remove=DEFAULT_AUTO_MERGE_LABEL)
        actions.append(f"remove:{DEFAULT_AUTO_MERGE_LABEL}")
        current_labels.discard(DEFAULT_AUTO_MERGE_LABEL)

    return actions


def _resolve_outdated_resolvable_threads(
    pr: dict, looker: str | None = None, *, apply: bool = True
) -> list[dict[str, object]]:
    """Attest-resolve every OUTDATED-RESOLVABLE thread on `pr` — bot-only and
    GitHub-outdated (the commented lines no longer exist in the diff) — witnessed by
    `looker` via `attest_and_resolve`. This is the same narrowest-safe slice the
    engage-outdated backlog walk uses, factored so the on-push `sync-pr` event can clear
    stale bot threads AS THEY GO OUTDATED — not only on a manual engage-outdated dispatch.

    `looker` is who the resolution is witnessed as. Pass it when the caller already knows
    the actor (engage-outdated resolves it once for the whole backlog walk). When omitted
    (the sync-pr event path), it is resolved LAZILY via `_viewer_login()` only if an
    outdated-resolvable thread is actually found — so a push with no stale threads (the
    common case) costs no extra GraphQL round-trip.

    Disposition-driven (`_thread_resolution_disposition`), so it covers any bot reviewer
    (CodeRabbit/Codex/Copilot), unlike the legacy allowlist resolver. needs-fix /
    apply-suggestion / needs-human / looked threads are never touched — a substantive
    finding is a caught error to fix, not to dispose of. Never merges. Returns one result
    dict per considered thread."""
    results: list[dict[str, object]] = []
    for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
        if thread.get("isResolved"):
            continue
        if _thread_resolution_disposition(thread) != "outdated-resolvable":
            continue
        # Defensive belt-and-suspenders: the `outdated-resolvable` disposition already
        # requires GitHub-outdated, but re-assert it here so the implementation can never
        # drift from the docstring's contract (only GitHub-outdated threads are touched)
        # if `_thread_resolution_disposition` ever regresses.
        if not thread.get("isOutdated"):
            continue
        # Lazy witness resolution: only pay for _viewer_login() once we have real work.
        if looker is None:
            looker = _viewer_login()
        try:
            result = attest_and_resolve(
                pr,
                thread,
                looker,
                "advisory",
                "Outdated: the commented lines no longer exist in the current diff; "
                "bot-only thread cleared under the outdated-only engaged policy.",
                apply=apply,
            )
        except RuntimeError as exc:
            # One thread's transient gh/GraphQL failure must not abort the pass. Surface
            # it on stderr too (not only in the returned dict) so sync-driven failures are
            # observable in workflow logs, not just to the JSON report consumer.
            print(
                f"Failed to attest-resolve outdated thread {thread.get('id')}: {exc}",
                file=sys.stderr,
            )
            result = {
                "thread_id": thread.get("id"),
                "eligible": False,
                "applied": False,
                "reason": f"failed to process thread: {exc}",
            }
        results.append(result)
    return results


def _list_open_pr_numbers(owner: str, repo: str) -> list[int]:
    open_prs = json.loads(
        _run(
            [
                "gh",
                "pr",
                "list",
                "--repo",
                f"{owner}/{repo}",
                "--state",
                "open",
                "--limit",
                "1000",
                "--json",
                "number",
            ]
        ).stdout
        or "[]"
    )
    return [int(pr_row["number"]) for pr_row in open_prs]


def _build_reconciliation_report(
    owner: str,
    repo: str,
    *,
    now: datetime | None = None,
    grace_minutes: int = DEFAULT_GRACE_MINUTES,
    auto_resolve_reviewers: set[str] | None = None,
) -> dict[str, object]:
    evaluated: list[dict[str, object]] = []
    promoted: list[int] = []
    rearmed: list[int] = []
    auto_merge_authorization_blocked: list[int] = []
    invariant_violations: list[dict[str, object]] = []
    total_resolved_outdated_threads = 0
    # Resolve the looker once for the whole batch walk (the engage-outdated pattern): the
    # witness names whoever actually ran the scheduled reconcile — the authenticated actor.
    # This is the same WITNESSED, disposition-driven resolver the event path uses, so the
    # reconcile lane is no longer the one place that resolved threads blindly (#399).
    looker = _viewer_login()

    for pr_number in _list_open_pr_numbers(owner, repo):
        pr = _fetch_pr(owner, repo, pr_number)
        outdated_results = _resolve_outdated_resolvable_threads(pr, looker, apply=True)
        resolved_count = sum(1 for r in outdated_results if r.get("applied"))
        total_resolved_outdated_threads += resolved_count
        if resolved_count:
            pr = _fetch_pr(owner, repo, pr_number)

        try:
            state = evaluate_review_state(
                pr,
                now=now,
                grace_minutes=grace_minutes,
                auto_resolve_reviewers=auto_resolve_reviewers,
            )
            # K6 restamp (#632) — this sweep IS the backfill automation: every open PR's
            # risk labels are re-mirrored from the one classifier, so unmarked/stale-labeled
            # in-flight PRs migrate without a hand-sweep. The verdict is always fetched; only
            # the restamp is skipped once the lane completed (its flag was consumed). A
            # classification error skips the restamp and leaves labels as-is; the PR is then
            # evaluated on its existing labels, so an unmarked PR reads `unknown` and fails
            # CLOSED — the projection disarms it. Intentional: a transient failure self-heals
            # on the next clean sweep; a persistent one correctly holds the PR.
            restamp_actions: list[str] = []
            try:
                ft_flag, dp_flag = _classify_pr_pair(owner, repo, pr_number)
            except Exception as exc:  # noqa: BLE001 — "do not restamp", never abort
                print(
                    f"::warning::K6 restamp skipped for #{pr_number}: {exc}",
                    file=sys.stderr,
                )
            else:
                # Restamp only when the lane has NOT completed (a completed lane's flag is
                # consumed by the projection; re-stamping would re-add it).
                if not state.get("lane_complete"):
                    label_set = {
                        node["name"]
                        for node in (pr.get("labels") or {}).get("nodes") or []
                        if node.get("name")
                    }
                    restamp_actions = restamp_risk_pair(pr_number, label_set, ft_flag, dp_flag)
                    pr["labels"] = {"nodes": [{"name": name} for name in sorted(label_set)]}
                # Re-evaluate with the verdict when the diff was (re)stamped, OR when a
                # lane-complete PR carries NO risk/* flag (first-pass risk_tier == "unknown")
                # — the consumed-clear (—/—) case, which must read affirmatively clear (not
                # `unknown`) so it isn't wrongly disarmed. A lane-complete PR that STILL has a
                # stale flag keeps its label-derived state so the projection consumes it; a
                # verdict override there would leave the stale flag orphaned.
                if not state.get("lane_complete") or state.get("risk_tier") == "unknown":
                    state = evaluate_review_state(
                        pr,
                        now=now,
                        grace_minutes=grace_minutes,
                        auto_resolve_reviewers=auto_resolve_reviewers,
                        verdict=(ft_flag, dp_flag),
                    )
        except RiskMarkerInvariantError as exc:
            # The K4/K6 mutual-exclusion invariant tripped on THIS PR. Fail loud — record
            # it and surface a non-zero exit — but do NOT abort the sweep: one mis-labeled
            # PR must not starve every other open PR of reconciliation. Scoped to the
            # dedicated type so an unrelated ValueError still fails the run normally.
            print(f"::error title=risk-marker invariant::PR #{pr_number}: {exc}", file=sys.stderr)
            invariant_violations.append({"number": pr_number, "error": str(exc)})
            evaluated.append({"number": pr_number, "invariant_violation": str(exc)})
            continue

        actions = apply_review_state_projection(pr_number, state)
        actions.extend(restamp_actions)
        current_labels = set(state["labels"])
        auto_merge_enabled = bool((pr.get("autoMergeRequest") or {}).get("enabledAt"))
        arm_error = None
        # Protected paths are not vetoed here anymore — the CODEOWNERS hard gate blocks
        # their merge regardless of label/arm (K1/#627, K2/#628 retired in favor of the
        # single, enforced source). Promotion keys only on eligibility + no merge block.
        if (
            AGENT_AUTO_MERGE_ENABLED
            and
            state["eligible_for_auto_merge"]
            and not bool(state["merge_blocked"])
            and DEFAULT_AUTO_MERGE_LABEL not in current_labels
        ):
            if DEFAULT_REVIEW_PENDING_LABEL in current_labels:
                current_labels.discard(DEFAULT_REVIEW_PENDING_LABEL)
            current_labels.add(DEFAULT_AUTO_MERGE_LABEL)
            _edit_label(pr_number, add=DEFAULT_AUTO_MERGE_LABEL)
            actions.append(f"add:{DEFAULT_AUTO_MERGE_LABEL}")
            _comment(
                pr_number,
                f"⏱️ Agent review grace period ({grace_minutes} min) elapsed "
                f"with no blocking feedback. Promoting to `auto-merge`.",
            )
            promoted.append(pr_number)
            auto_merge_enabled = False

        if (
            AGENT_AUTO_MERGE_ENABLED
            and
            DEFAULT_AUTO_MERGE_LABEL in current_labels
            and bool(state["eligible_for_auto_merge"])
            and not bool(state["merge_blocked"])
        ):
            # No `and not auto_merge_enabled` guard: an already-armed PR may be
            # armed-but-not-queued (the stuck case), and _arm_auto_merge is
            # state-aware — it no-ops a queued PR and toggles a stuck one.
            auto_merge_enabled, arm_error = _arm_auto_merge(owner, repo, pr_number)
            if auto_merge_enabled:
                rearmed.append(pr_number)
            else:
                auto_merge_authorization_blocked.append(pr_number)

        evaluated.append(
            {
                "number": pr_number,
                "eligible_for_auto_merge": state["eligible_for_auto_merge"],
                "low_risk": state["low_risk"],
                "merge_blocked": state["merge_blocked"],
                "blocking_reasons": state["blocking_reasons"],
                "resolved_outdated_threads": resolved_count,
                "auto_merge_enabled": auto_merge_enabled,
                "auto_merge_arm_error": arm_error,
                "actions": actions,
            }
        )

    return {
        "checked_prs": len(evaluated),
        "promoted_prs": promoted,
        "rearmed_prs": rearmed,
        "auto_merge_authorization_blocked": auto_merge_authorization_blocked,
        "invariant_violations": invariant_violations,
        "resolved_outdated_threads": total_resolved_outdated_threads,
        "evaluated": evaluated,
    }


def acknowledge_apply(args: argparse.Namespace) -> int:
    ensure_labels()

    if not APPLY_RE.search(args.comment_body or ""):
        print("Comment does not match an @copilot apply request; nothing to do.")
        return 0

    trusted = _csv_env("TRUSTED_COMMENT_ASSOCIATIONS", "OWNER,MEMBER,COLLABORATOR")
    if args.author_association not in trusted:
        print(
            f"Comment author association {args.author_association!r} is not trusted; "
            "skipping acknowledgement."
        )
        return 0

    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    labels = {node["name"] for node in (pr.get("labels") or {}).get("nodes") or []}

    if DEFAULT_PENDING_LABEL not in labels:
        _edit_label(args.pr_number, add=DEFAULT_PENDING_LABEL)
        _comment(
            args.pr_number,
            (
                f"Observed a Copilot apply request from @{args.comment_author}. "
                f"Marked this PR as `{DEFAULT_PENDING_LABEL}` while follow-up "
                "changes are expected."
            ),
        )
    else:
        print(f"{DEFAULT_PENDING_LABEL} already present; acknowledgement is already in place.")

    return 0


def sync_pr(args: argparse.Namespace) -> int:
    ensure_labels()

    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    completion_actors = _csv_env(
        "APPLY_COMPLETION_ACTORS",
        "Copilot,copilot-swe-agent[bot]",
    )

    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    # Event-driven outdated-resolve: clear bot-only, GitHub-outdated threads as they go
    # stale on this push — witnessed by the authenticated actor (the same narrowest-safe
    # slice as engage-outdated, now firing on the event instead of only manual dispatch).
    # The looker is resolved lazily inside the helper (only if there's a stale thread to
    # clear), so a push with nothing to resolve costs no extra _viewer_login() round-trip.
    outdated_results = _resolve_outdated_resolvable_threads(
        pr, getattr(args, "looker", None), apply=True
    )
    resolved_count = sum(1 for r in outdated_results if r.get("applied"))
    if resolved_count:
        pr = _fetch_pr(args.owner, args.repo, args.pr_number)

    state = evaluate_review_state(
        pr,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )

    # K6 restamp-on-sync (#632): risk labels mirror the CURRENT diff from the one classifier.
    # The verdict is always fetched (so a consumed-clear lane reads clear, not unknown); only
    # the restamp is skipped once the lane completed (its flag was consumed). A classification
    # error skips the restamp and leaves labels as-is; the PR is then evaluated on its existing
    # labels, so an unmarked PR reads `unknown` and fails CLOSED — the projection disarms it.
    # Intentional: a transient failure self-heals on the next clean sweep; a persistent one holds.
    restamp_actions: list[str] = []
    try:
        ft_flag, dp_flag = _classify_pr_pair(args.owner, args.repo, args.pr_number)
    except Exception as exc:  # noqa: BLE001 — any failure means "do not restamp"
        print(
            f"::warning::K6 restamp skipped for #{args.pr_number} "
            f"(classification failed; labels left as-is): {exc}",
            file=sys.stderr,
        )
    else:
        # Restamp only when the lane has NOT completed (a completed lane's flag is consumed
        # by the projection; re-stamping would re-add it).
        if not state.get("lane_complete"):
            label_set = {
                node["name"]
                for node in (pr.get("labels") or {}).get("nodes") or []
                if node.get("name")
            }
            restamp_actions = restamp_risk_pair(args.pr_number, label_set, ft_flag, dp_flag)
            pr["labels"] = {"nodes": [{"name": name} for name in sorted(label_set)]}
        # Re-evaluate with the verdict when the diff was (re)stamped, OR when a lane-complete
        # PR carries NO risk/* flag (first-pass risk_tier == "unknown") — the consumed-clear
        # (—/—) case, which must read affirmatively clear (not `unknown`) so it isn't wrongly
        # disarmed. A lane-complete PR that STILL has a stale flag keeps its label-derived
        # state so the projection consumes it; a verdict override there would orphan the flag.
        if not state.get("lane_complete") or state.get("risk_tier") == "unknown":
            state = evaluate_review_state(
                pr,
                grace_minutes=args.grace_minutes,
                auto_resolve_reviewers=auto_resolve_reviewers,
                verdict=(ft_flag, dp_flag),
            )

    clear_pending = (
        args.sync_actor in completion_actors and bool(state["has_copilot_apply_pending"])
    )
    label_actions = apply_review_state_projection(
        args.pr_number,
        state,
        clear_apply_pending=clear_pending,
    )

    # Engine/label-driven arming: if this update cleared the last blocking thread on a
    # low-risk PR, arm it for the merge queue (guarded against protected paths). The
    # queue + branch protection remain the actual merge gate.
    arm_result = _maybe_arm_auto_merge(args.owner, args.repo, args.pr_number, state)

    print(
        json.dumps(
            {
                "resolved_outdated_threads": resolved_count,
                "current_unresolved_threads": state["current_unresolved_threads"],
                "outdated_unresolved_threads": state["outdated_unresolved_threads"],
                "blocking_review": state["blocking_review"],
                "eligible_for_auto_merge": state["eligible_for_auto_merge"],
                "auto_merge_armed": arm_result["armed"],
                "auto_merge_arm_reason": arm_result["reason"],
                "label_actions": label_actions,
                "restamp_actions": restamp_actions,
                "cleared_copilot_apply_pending": clear_pending,
            }
        )
    )
    return 0


def review_submitted(args: argparse.Namespace) -> int:
    ensure_labels()

    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    state = evaluate_review_state(
        pr,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )

    blocking_event = (
        args.review_state == "changes_requested"
        and args.review_author != args.pr_author
        and bool(state["blocking_review"])
    )
    if blocking_event:
        _disable_auto_merge(args.pr_number)
        review_url = f"{args.pr_url}#pullrequestreview-{args.review_id}"
        _comment(
            args.pr_number,
            (
                f"Acknowledged review by @{args.review_author} "
                f"({args.review_state}). Auto-merge paused until the blocking "
                f"review state clears. [Review link]({review_url})"
            ),
        )

    label_actions = apply_review_state_projection(args.pr_number, state)

    # If the submitted review left the PR eligible (e.g. it cleared the last block on a
    # low-risk PR), arm it for the merge queue (guarded against protected paths). A
    # blocking review makes the PR ineligible, so this self-no-ops in that case.
    arm_result = _maybe_arm_auto_merge(args.owner, args.repo, args.pr_number, state)

    print(
        json.dumps(
            {
                "blocking_event": blocking_event,
                "blocking_review": state["blocking_review"],
                "current_unresolved_threads": state["current_unresolved_threads"],
                "auto_merge_armed": arm_result["armed"],
                "auto_merge_arm_reason": arm_result["reason"],
                "label_actions": label_actions,
            }
        )
    )
    return 0


def promote_ready(args: argparse.Namespace) -> int:
    ensure_labels()
    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    report = _build_reconciliation_report(
        args.owner,
        args.repo,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )
    print(json.dumps(report))
    # Fail loud on any risk-marker invariant violation (see reconcile_open_prs).
    return 1 if report.get("invariant_violations") else 0


def reconcile_open_prs(args: argparse.Namespace) -> int:
    ensure_labels()
    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    report = _build_reconciliation_report(
        args.owner,
        args.repo,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )
    print(json.dumps(report))
    # Fail loud: any risk-marker invariant violation turns the reconcile run red so a
    # mis-labeled PR can't rot unnoticed. The sweep still processed every other PR above.
    return 1 if report.get("invariant_violations") else 0


def enable_auto_merge(args: argparse.Namespace) -> int:
    ensure_labels()
    auto_resolve_reviewers = _csv_env(
        "AUTO_RESOLVE_REVIEWERS",
        "copilot-pull-request-reviewer",
    )
    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    state = evaluate_review_state(
        pr,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )
    label_actions = apply_review_state_projection(args.pr_number, state)
    labels = set(state["labels"])

    enabled = False
    arm_error = None
    if (
        AGENT_AUTO_MERGE_ENABLED
        and
        DEFAULT_AUTO_MERGE_LABEL in labels
        and bool(state["eligible_for_auto_merge"])
        and not bool(state["merge_blocked"])
    ):
        enabled, arm_error = _arm_auto_merge(args.owner, args.repo, args.pr_number)

    print(
        json.dumps(
            {
                "enabled": enabled,
                "arm_error": arm_error,
                "merge_blocked": state["merge_blocked"],
                "blocking_reasons": state["blocking_reasons"],
                "label_actions": label_actions,
            }
        )
    )
    return 0


def _matches_claim(body: str) -> bool:
    if not body:
        return False
    return any(pattern.search(body) for pattern in CLAIM_PATTERNS)


def _fetch_pr_merge_state(owner: str, repo: str, pr_number: int) -> dict:
    """Fetch the institutional state fields we compare claims against."""
    cmd = [
        "gh",
        "pr",
        "view",
        str(pr_number),
        "--repo",
        f"{owner}/{repo}",
        "--json",
        "mergeable,mergeStateStatus,statusCheckRollup,isDraft,number",
    ]
    result = _run(cmd)
    return json.loads(result.stdout or "{}")


def _list_pr_comment_bodies(owner: str, repo: str, pr_number: int) -> list[str]:
    """Return raw comment bodies for the PR (issue-style comments)."""
    cmd = [
        "gh",
        "api",
        f"repos/{owner}/{repo}/issues/{pr_number}/comments",
        "--paginate",
    ]
    try:
        result = _run(cmd)
    except RuntimeError:
        return []
    try:
        payload = json.loads(result.stdout or "[]")
    except json.JSONDecodeError:
        return []
    return [item.get("body") or "" for item in payload if isinstance(item, dict)]


def _has_prior_verify_comment(owner: str, repo: str, pr_number: int) -> bool:
    return any(VERIFY_CLAIM_MARKER in body for body in _list_pr_comment_bodies(owner, repo, pr_number))


def verify_claim(args: argparse.Namespace) -> int:
    body = args.comment_body or ""

    # Recursion guard: skip if the trigger comment IS a prior verification comment.
    if VERIFY_CLAIM_MARKER in body:
        print("Comment contains verify-claim marker (recursion guard); skipping.")
        return 0

    # Narrow filter: only act on agent completion-claim phrases.
    if not _matches_claim(body):
        print("Comment does not match a known agent completion-claim pattern; nothing to do.")
        return 0

    # Idempotency: one verification per PR until something material changes.
    if _has_prior_verify_comment(args.owner, args.repo, args.pr_number):
        print(
            f"A prior verify-claim comment already exists on PR #{args.pr_number}; "
            "skipping to avoid duplicate noise."
        )
        return 0

    state = _fetch_pr_merge_state(args.owner, args.repo, args.pr_number)

    mergeable = state.get("mergeable") or "UNKNOWN"
    merge_state = state.get("mergeStateStatus") or "UNKNOWN"
    is_draft = bool(state.get("isDraft"))
    checks = state.get("statusCheckRollup") or []

    failing_real: list[str] = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        name = check.get("name") or check.get("context") or "<unknown>"
        result = check.get("conclusion") or check.get("state") or ""
        if result == "FAILURE" and name not in KNOWN_NOISE_CHECKS:
            failing_real.append(name)

    divergent_reasons: list[str] = []
    if mergeable != "MERGEABLE":
        divergent_reasons.append(f"`mergeable` is `{mergeable}`, not `MERGEABLE`")
    if merge_state in {"DIRTY", "BLOCKED", "BEHIND", "UNKNOWN"}:
        divergent_reasons.append(f"`mergeStateStatus` is `{merge_state}`")
    if is_draft:
        divergent_reasons.append("the PR is still marked as draft")
    if failing_real:
        formatted = ", ".join(f"`{name}`" for name in failing_real)
        divergent_reasons.append(f"failing checks (excluding known noise): {formatted}")

    if not divergent_reasons:
        print(
            f"Claim matches institutional state on PR #{args.pr_number}; "
            "no divergence comment needed."
        )
        return 0

    author = args.comment_author or "an agent"
    body_lines = [
        "> **verify-claim**",
        "",
        f"A recent comment from @{author} read as an agent completion claim. "
        "Verifying against current GitHub state:",
        "",
    ]
    for reason in divergent_reasons:
        body_lines.append(f"- {reason}")
    body_lines.extend(
        [
            "",
            "The claim and the institutional state appear to diverge. Surfacing the "
            "loop closure before merge, per IF 7 in "
            "`!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md`.",
            "",
            VERIFY_CLAIM_MARKER,
        ]
    )
    _comment(args.pr_number, "\n".join(body_lines))
    print(f"Posted verify-claim divergence comment on PR #{args.pr_number}.")
    return 0


def _thread_belongs_to_pr(thread: dict, owner: str, repo: str, pr_number: int) -> bool:
    """True if a thread's comment links place it on owner/repo PR #pr_number.

    `_fetch_thread` resolves a *global* node id, so a stray or hostile id could point at
    a thread on a different PR/repo; membership is verified before acting on it.
    """
    expected = f"/{owner}/{repo}/pull/{pr_number}".lower()
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        if expected in (comment.get("url") or "").lower():
            return True
    return False


def attest_resolve(args: argparse.Namespace) -> int:
    """Disposition one explicit bot-authored thread (Layer B2). Dry-run unless --apply.

    Bounded by design: targets a single PR + thread id, so it cannot walk the backlog
    or cascade. The deterministic walk + cascade-safety orchestration is Layer C.
    """
    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    threads = (pr.get("reviewThreads") or {}).get("nodes") or []
    thread = next((t for t in threads if t.get("id") == args.thread_id), None)
    if thread is None:
        # Beyond _fetch_pr's first-100 window. node(id:) is global, so confirm the
        # fetched thread is actually on THIS PR before touching it.
        fetched = _fetch_thread(args.thread_id)
        if fetched is not None and _thread_belongs_to_pr(
            fetched, args.owner, args.repo, args.pr_number
        ):
            thread = fetched
    if thread is None:
        print(
            json.dumps(
                {
                    "thread_id": args.thread_id,
                    "eligible": False,
                    "applied": False,
                    "reason": "thread not found on PR",
                }
            )
        )
        return 1
    # Default the looker to the authenticated actor, so the recorded witness always names
    # whoever actually ran the resolve (agent-driven or CI-bot), and the self-attestation
    # actor-match check in attest_and_resolve is satisfied by construction.
    looker = args.looker or _viewer_login()
    result = attest_and_resolve(
        pr,
        thread,
        looker,
        args.decision,
        args.rationale,
        apply=args.apply,
    )
    print(json.dumps(result))
    return 0


def _positive_int(value: str) -> int:
    """argparse type: a strictly positive integer (e.g. --stale-days).

    A non-positive staleness window misclassifies every PR (<=0 marks all stale,
    making nothing safe to drain), so it is rejected at parse time.
    """
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def engage_outdated(args: argparse.Namespace) -> int:
    """Engage the queue on the OUTDATED subset: attest-resolve every outdated-resolvable
    thread across open PRs. Dry-run unless --apply.

    The first 'engage' step (Logan: the queue runs by default; reviewer comments are what
    keep a PR hanging). Scope is deliberately the narrowest safe slice — ONLY threads whose
    resolution disposition is `outdated-resolvable` (bot-only, GitHub-outdated: the
    commented lines no longer exist in the diff). Each is cleared via `attest_and_resolve`
    with a recorded attestation by the looker — the `--looker` value, defaulting to the
    authenticated actor (`_viewer_login()`) — so it is a *witnessed* resolution,
    not the blind reconciler. needs-fix / apply-suggestion / looked / human threads are
    never touched — needs-fix is the reviewer gate that keeps a PR hanging. This NEVER
    merges; if clearing the last thread lets an armed PR flow, that is GitHub's auto-merge,
    by design (the engaged queue).

    --pr scopes the pass to a single PR number (the guinea-pig case: prove one PR clean
    before widening to the whole backlog); default is every open PR.
    """
    considered: list[dict[str, object]] = []
    # Resolve the looker once: default to the authenticated actor so the witness names
    # whoever actually ran the engine (agent token or CI bot), truthfully.
    looker = args.looker or _viewer_login()
    only_pr = getattr(args, "pr", None)
    # `is not None`, not truthiness: --pr is parsed by _positive_int (0/negative
    # rejected at parse time), so any value that reaches here is a real PR number
    # and must scope the pass — never silently fall back to the full backlog walk.
    pr_numbers = [only_pr] if only_pr is not None else _list_open_pr_numbers(args.owner, args.repo)
    for pr_number in pr_numbers:
        pr = _fetch_pr(args.owner, args.repo, pr_number)
        # The backlog walk only ever yields OPEN PRs (_list_open_pr_numbers). A --pr
        # scope can name any existing PR, so hold the same invariant: engage-outdated
        # acts only on the open queue — a closed/merged PR is refused, not engaged.
        if only_pr is not None and (pr.get("state") or "").upper() != "OPEN":
            raise SystemExit(
                f"--pr {only_pr} is {pr.get('state')!r}, not OPEN; engage-outdated "
                "acts only on the open queue."
            )
        # Same narrowest-safe slice as the on-push sync path (shared helper): attest-resolve
        # every outdated-resolvable thread, witnessed by the looker.
        for result in _resolve_outdated_resolvable_threads(pr, looker, apply=args.apply):
            considered.append({"pr": pr_number, **result})
    print(
        json.dumps(
            {
                "apply": args.apply,
                "scope_pr": only_pr,
                "outdated_threads": len(considered),
                "resolved": sum(1 for r in considered if r.get("applied")),
                "results": considered,
            }
        )
    )
    return 0


def reconcile_witness(args: argparse.Namespace) -> int:
    """Backfill missing attestations on resolved-but-unwitnessed threads WE resolved.

    The repair pass for the unwitnessed ending (#399): a resolve can land while its
    attestation does not, leaving a thread resolved with no recorded look. This walks
    resolved, bot-only threads that carry no attestation and whose `resolvedBy` is the
    looker, and posts the look that is owed — via `backfill_witness`, which NEVER resolves
    or unresolves and refuses any thread a different identity resolved. Dry-run unless
    --apply. The looker defaults to the authenticated actor, so the backfilled witness
    truthfully names who actually resolved it. `--pr` scopes to one PR.
    """
    looker = args.looker or _viewer_login()
    rationale = args.rationale or (
        "Witness backfilled: this thread was resolved under the engaged policy but the "
        "attestation had not landed; recording the look now."
    )
    considered: list[dict[str, object]] = []
    only_pr = getattr(args, "pr", None)
    pr_numbers = [only_pr] if only_pr else _list_open_pr_numbers(args.owner, args.repo)
    for pr_number in pr_numbers:
        pr = _fetch_pr(args.owner, args.repo, pr_number)
        for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
            # Pre-filter to the realistic candidate set: resolved, not yet witnessed,
            # bot-only. backfill_witness then applies the resolvedBy == looker gate.
            if not thread.get("isResolved"):
                continue
            if _thread_has_attested_look(thread):
                continue
            if not _thread_is_bot_only(thread):
                continue
            try:
                result = backfill_witness(pr, thread, looker, rationale, apply=args.apply)
            except RuntimeError as exc:
                result = {
                    "thread_id": thread.get("id"),
                    "eligible": False,
                    "applied": False,
                    "reason": f"failed to process thread: {exc}",
                }
            considered.append({"pr": pr_number, **result})
    print(
        json.dumps(
            {
                "looker": looker,
                "apply": args.apply,
                "scope_pr": only_pr,
                "candidates": len(considered),
                "backfilled": sum(1 for r in considered if r.get("applied")),
                "results": considered,
            }
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ensure-labels")

    ack = subparsers.add_parser("acknowledge-apply")
    ack.add_argument("--owner", required=True)
    ack.add_argument("--repo", required=True)
    ack.add_argument("--pr-number", required=True, type=int)
    ack.add_argument("--comment-author", default="")
    ack.add_argument("--author-association", default="")
    ack.add_argument("--comment-body", default="")

    sync = subparsers.add_parser("sync-pr")
    sync.add_argument("--owner", required=True)
    sync.add_argument("--repo", required=True)
    sync.add_argument("--pr-number", required=True, type=int)
    sync.add_argument("--sync-actor", default="")
    sync.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

    review = subparsers.add_parser("review-submitted")
    review.add_argument("--owner", required=True)
    review.add_argument("--repo", required=True)
    review.add_argument("--pr-number", required=True, type=int)
    review.add_argument("--pr-author", required=True)
    review.add_argument("--pr-url", required=True)
    review.add_argument("--review-author", required=True)
    review.add_argument("--review-id", required=True)
    review.add_argument("--review-state", required=True)
    review.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

    promote = subparsers.add_parser("promote-ready")
    promote.add_argument("--owner", required=True)
    promote.add_argument("--repo", required=True)
    promote.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

    reconcile = subparsers.add_parser("reconcile-open-prs")
    reconcile.add_argument("--owner", required=True)
    reconcile.add_argument("--repo", required=True)
    reconcile.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

    enable = subparsers.add_parser("enable-auto-merge")
    enable.add_argument("--owner", required=True)
    enable.add_argument("--repo", required=True)
    enable.add_argument("--pr-number", required=True, type=int)
    enable.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

    verify = subparsers.add_parser("verify-claim")
    verify.add_argument("--owner", required=True)
    verify.add_argument("--repo", required=True)
    verify.add_argument("--pr-number", required=True, type=int)
    verify.add_argument("--comment-author", default="")
    verify.add_argument("--comment-body", default="")


    attest = subparsers.add_parser("attest-resolve")
    attest.add_argument("--owner", required=True)
    attest.add_argument("--repo", required=True)
    attest.add_argument("--pr-number", required=True, type=int)
    attest.add_argument("--thread-id", required=True)
    attest.add_argument(
        "--looker",
        default=None,
        help="attesting identity recorded in the look marker; default: the authenticated "
        "actor (whoever the token posts as), so the witness always names who actually ran it",
    )
    attest.add_argument("--decision", required=True, choices=sorted(ATTESTATION_DECISIONS))
    attest.add_argument("--rationale", default="")
    attest.add_argument(
        "--apply",
        action="store_true",
        help="actually post the attestation and resolve (default: dry-run)",
    )

    engage = subparsers.add_parser("engage-outdated")
    engage.add_argument("--owner", required=True)
    engage.add_argument("--repo", required=True)
    engage.add_argument(
        "--looker",
        default=None,
        help="attesting identity recorded in the look marker; default: the authenticated "
        "actor (whoever the token posts as), so the witness always names who actually ran it",
    )
    engage.add_argument(
        "--pr",
        type=_positive_int,
        default=None,
        help="scope the pass to a single open PR number (default: every open PR)",
    )
    engage.add_argument(
        "--apply",
        action="store_true",
        help="actually post attestations and resolve outdated threads (default: dry-run)",
    )

    witness = subparsers.add_parser("reconcile-witness")
    witness.add_argument("--owner", required=True)
    witness.add_argument("--repo", required=True)
    witness.add_argument(
        "--looker",
        default=None,
        help="identity whose resolved-but-unwitnessed threads to backfill; default: the "
        "authenticated actor (_viewer_login). Only threads this identity resolved are touched.",
    )
    witness.add_argument(
        "--pr",
        type=_positive_int,
        default=None,
        help="scope the pass to a single PR number (default: every open PR). Backfill is a "
        "record repair — it only posts the missing attestation, never resolves or merges — "
        "so it is safe on any PR; the default whole-backlog walk covers open PRs only.",
    )
    witness.add_argument("--rationale", default="")
    witness.add_argument(
        "--apply",
        action="store_true",
        help="actually backfill the missing attestations (default: dry-run)",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "ensure-labels":
        ensure_labels()
        return 0
    if args.command == "acknowledge-apply":
        return acknowledge_apply(args)
    if args.command == "sync-pr":
        return sync_pr(args)
    if args.command == "review-submitted":
        return review_submitted(args)
    if args.command == "promote-ready":
        return promote_ready(args)
    if args.command == "reconcile-open-prs":
        return reconcile_open_prs(args)
    if args.command == "verify-claim":
        return verify_claim(args)
    if args.command == "attest-resolve":
        return attest_resolve(args)
    if args.command == "engage-outdated":
        return engage_outdated(args)
    if args.command == "reconcile-witness":
        return reconcile_witness(args)
    return enable_auto_merge(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"review_feedback_loop.py failed: {exc}", file=sys.stderr)
        raise
