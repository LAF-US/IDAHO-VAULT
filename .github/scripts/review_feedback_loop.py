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
    Agent-authored PR auto-merge is retired; Dependabot has its own verified lane.
  - enable-auto-merge: legacy compatibility path that removes stale agent
    auto-merge state rather than arming it.
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
import subprocess
import sys
from datetime import datetime, timezone


APPLY_RE = re.compile(r"@copilot\b[\s\S]*?\bapply changes\b", re.IGNORECASE)
DEFAULT_GRACE_MINUTES = 30
AGENT_AUTO_MERGE_ENABLED = False

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
RISK_LOW_LABEL = "risk/low"
RISK_HIGH_LABEL = "risk/high"
AUTO_MERGE_AUTHZ_FRAGMENTS = (
    "Pull request User is not authorized for this protected branch "
    "(enablePullRequestAutoMerge)",
    "Resource not accessible by integration (enablePullRequestAutoMerge)",
)

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
    RISK_LOW_LABEL: (
        "C2E0C6",
        "Risk tier: low (only low-risk paths changed).",
    ),
    RISK_HIGH_LABEL: (
        "E99695",
        "Risk tier: high (at least one high-risk path changed).",
    ),
}


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(cmd)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def _arm_auto_merge(pr_number: int) -> tuple[bool, str | None]:
    try:
        _run(
            [
                "gh",
                "pr",
                "merge",
                str(pr_number),
                "--squash",
                "--delete-branch",
                "--auto",
            ]
        )
    except RuntimeError as exc:
        if not any(fragment in str(exc) for fragment in AUTO_MERGE_AUTHZ_FRAGMENTS):
            raise
        return (
            False,
            "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
        )
    return True, None


def _graphql(query: str, **variables: object) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])
    result = _run(cmd)
    payload = json.loads(result.stdout or "{}")
    errors = payload.get("errors")
    if errors:
        raise RuntimeError(f"GraphQL error(s): {json.dumps(errors, indent=2)}")
    return payload.get("data", {})


def _fetch_pr(owner: str, name: str, number: int) -> dict:
    query = """
    query($owner:String!, $name:String!, $number:Int!) {
      repository(owner: $owner, name: $name) {
        pullRequest(number: $number) {
          number
          url
          body
          createdAt
          isDraft
          reviewDecision
          autoMergeRequest {
            enabledAt
          }
          labels(first: 50) {
            nodes { name }
          }
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              isOutdated
              comments(first: 100) {
                pageInfo { hasNextPage }
                nodes {
                  author { login __typename }
                  body
                  url
                }
              }
            }
          }
        }
      }
    }
    """
    data = _graphql(query, owner=owner, name=name, number=number)
    repo = data.get("repository") or {}
    pr = repo.get("pullRequest")
    if not pr:
        raise RuntimeError(f"Pull request #{number} was not found in {owner}/{name}.")
    return pr


def _resolve_thread(thread_id: str) -> None:
    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { id isResolved }
      }
    }
    """
    _graphql(mutation, threadId=thread_id)


def _is_forbidden_integration_error(exc: RuntimeError) -> bool:
    text = str(exc)
    return "FORBIDDEN" in text or "Resource not accessible by integration" in text


# Look-then-resolve design (#399): nothing is dismissed or resolved until a
# looker (agent or human) has looked. A looker records the look as an in-thread
# attestation comment of this canonical shape:
#   <!-- looked: by=<login>; at=<iso8601>; decision=<addressed|advisory|wontfix>; v=1 -->
# Detection requires the structured marker AND that `by` matches the comment's
# own author, so a pasted or forged marker attributed to someone else cannot
# fake a look. This layer RESOLVES NOTHING.
LOOK_ATTESTATION_MARKER = "<!-- looked:"
LOOK_ATTESTATION_RE = re.compile(
    r"<!--\s*looked:\s*by=(?P<by>[A-Za-z0-9][A-Za-z0-9-]*(?:\[bot\])?)\s*;[^>]*-->"
)


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


def _build_looker_queue(pr: dict) -> list[dict[str, object]]:
    """Read-only worklist of unresolved threads on one PR for a looker.

    Resolves nothing. Each entry carries what a looker needs to look: the
    thread id, its comment authors, whether the anchor is outdated, whether a
    look has already been attested, and a link.
    """
    items: list[dict[str, object]] = []
    for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
        if thread.get("isResolved"):
            continue
        comments = (thread.get("comments") or {}).get("nodes") or []
        first = comments[0] if comments else {}
        items.append(
            {
                "pr": pr.get("number"),
                "thread_id": thread.get("id"),
                "authors": sorted(_thread_authors(thread)),
                "is_outdated": bool(thread.get("isOutdated")),
                "looked": _thread_has_attested_look(thread),
                "url": first.get("url") or "",
            }
        )
    return items


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


def _viewer_login() -> str:
    """The login of the authenticated actor the GraphQL calls post as.

    The attestation is *self*-attested: the detector requires the marker's `by=`
    to equal the comment's own author. Since `_add_thread_reply` posts as this
    actor, a `looker` that differs from it would yield an undetectable attestation,
    so the resolve path verifies them against each other before writing.
    """
    viewer = _graphql("query { viewer { login } }").get("viewer") or {}
    login = (viewer.get("login") or "").strip()
    if not login:
        raise RuntimeError("Could not determine the authenticated GitHub actor.")
    return login


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
    return data.get("node")


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
    """Disposition ONE bot-authored review thread: record an attested look, then resolve.

    Writes nothing unless `apply=True`. NEVER merges and NEVER enables auto-merge — it
    posts the looker's attestation as a thread reply and resolves that single thread,
    nothing else (the cascade-safety contract above).

    Eligibility is reported, never raised. A thread is eligible only when: the PR's
    review is not CHANGES_REQUESTED; every author of the thread is a bot
    (`_thread_is_bot_only` — never a human thread); the thread is not already resolved;
    and it does not already carry an attested look (idempotent — a re-run is a no-op).

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
    # "Look, then resolve" is two separate mutations. An already-attested but still
    # OPEN thread is a partial success (the reply landed, the resolve did not) — recover
    # by resolving without posting a duplicate attestation, rather than no-op'ing and
    # leaving the thread blocking forever. The fully-done case (attested AND resolved)
    # is already short-circuited by the isResolved guard above.
    already_looked = _thread_has_attested_look(thread)

    # Build (and thereby validate looker/decision) before any write.
    body = _build_attestation(looker, decision, rationale, now=now)
    result["eligible"] = True
    result["attestation"] = body
    if not apply:
        result["reason"] = (
            "dry-run: attested look already present, would resolve"
            if already_looked
            else "dry-run: would record attested look and resolve"
        )
        return result

    if not already_looked:
        # The look is self-attested: the marker says by={looker}, but the reply posts
        # as the authenticated actor. If they differ, the attestation is undetectable —
        # refuse rather than write a broken audit record.
        actor = _viewer_login()
        if actor != looker:
            result["eligible"] = False
            result["reason"] = (
                f"looker {looker!r} does not match the authenticated actor {actor!r}"
            )
            return result
        _add_thread_reply(thread_id, body)
    _resolve_thread(thread_id)
    result["applied"] = True
    result["reason"] = (
        "existing attested look; thread resolved"
        if already_looked
        else "attested look recorded; thread resolved"
    )
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


def _disable_auto_merge(pr_number: int) -> None:
    _run(["gh", "pr", "merge", str(pr_number), "--disable-auto"], check=False)


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


def _thread_authors(thread: dict) -> set[str]:
    authors: set[str] = set()
    for comment in (thread.get("comments") or {}).get("nodes") or []:
        author = (comment.get("author") or {}).get("login")
        if author:
            authors.add(author)
    return authors


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


def _risk_tier_for_pr(body: str, labels: set[str]) -> str:
    # Label is canonical: survives body rewrites by human or agent editors.
    if RISK_HIGH_LABEL in labels:
        return "high"
    if RISK_LOW_LABEL in labels:
        return "low"
    # Fallback for older PRs or states where risk is not yet labeled.
    if DEFAULT_REVIEW_PENDING_LABEL in labels:
        return "low"
    return "unknown"


def evaluate_review_state(
    pr: dict,
    *,
    now: datetime | None = None,
    grace_minutes: int = DEFAULT_GRACE_MINUTES,
    auto_resolve_reviewers: set[str] | None = None,
) -> dict[str, object]:
    """Return one machine-readable view of the PR's current review state."""

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
    risk_tier = _risk_tier_for_pr(pr.get("body") or "", label_names)
    low_risk = risk_tier == "low"
    merge_blocked = draft or blocking_review or current_unresolved > 0
    eligible_for_auto_merge = (
        AGENT_AUTO_MERGE_ENABLED and low_risk and grace_elapsed and not merge_blocked
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
        "draft": draft,
        "review_decision": review_decision,
        "blocking_review": blocking_review,
        "current_unresolved_threads": current_unresolved,
        "outdated_unresolved_threads": outdated_unresolved,
        "auto_resolvable_outdated_threads": auto_resolvable_outdated,
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


def _resolve_outdated_advisory_threads(pr: dict, auto_resolve_reviewers: set[str]) -> int:
    resolved_count = 0
    for thread in (pr.get("reviewThreads") or {}).get("nodes") or []:
        if thread.get("isResolved") or not thread.get("isOutdated"):
            continue

        authors = _thread_authors(thread)
        if authors and authors.issubset(auto_resolve_reviewers):
            try:
                _resolve_thread(thread["id"])
                resolved_count += 1
            except RuntimeError as exc:
                if _is_forbidden_integration_error(exc):
                    print(
                        f"Skipping auto-resolve for thread {thread['id']}: token lacks permission.",
                        file=sys.stderr,
                    )
                else:
                    raise
    return resolved_count


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
    total_resolved_outdated_threads = 0

    for pr_number in _list_open_pr_numbers(owner, repo):
        pr = _fetch_pr(owner, repo, pr_number)
        resolved_count = _resolve_outdated_advisory_threads(pr, auto_resolve_reviewers or set())
        total_resolved_outdated_threads += resolved_count
        if resolved_count:
            pr = _fetch_pr(owner, repo, pr_number)

        state = evaluate_review_state(
            pr,
            now=now,
            grace_minutes=grace_minutes,
            auto_resolve_reviewers=auto_resolve_reviewers,
        )

        actions = apply_review_state_projection(pr_number, state)
        current_labels = set(state["labels"])
        auto_merge_enabled = bool((pr.get("autoMergeRequest") or {}).get("enabledAt"))
        arm_error = None
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
            and not auto_merge_enabled
        ):
            auto_merge_enabled, arm_error = _arm_auto_merge(pr_number)
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
    resolved_count = _resolve_outdated_advisory_threads(pr, auto_resolve_reviewers)
    if resolved_count:
        pr = _fetch_pr(args.owner, args.repo, args.pr_number)

    state = evaluate_review_state(
        pr,
        grace_minutes=args.grace_minutes,
        auto_resolve_reviewers=auto_resolve_reviewers,
    )
    clear_pending = (
        args.sync_actor in completion_actors and bool(state["has_copilot_apply_pending"])
    )
    label_actions = apply_review_state_projection(
        args.pr_number,
        state,
        clear_apply_pending=clear_pending,
    )

    print(
        json.dumps(
            {
                "resolved_outdated_threads": resolved_count,
                "current_unresolved_threads": state["current_unresolved_threads"],
                "outdated_unresolved_threads": state["outdated_unresolved_threads"],
                "blocking_review": state["blocking_review"],
                "eligible_for_auto_merge": state["eligible_for_auto_merge"],
                "label_actions": label_actions,
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
    print(
        json.dumps(
            {
                "blocking_event": blocking_event,
                "blocking_review": state["blocking_review"],
                "current_unresolved_threads": state["current_unresolved_threads"],
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
    return 0


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
    return 0


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
        enabled, arm_error = _arm_auto_merge(args.pr_number)

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


def list_unlooked(args: argparse.Namespace) -> int:
    """Print the looker queue across open PRs. Read-only: resolves nothing.

    Layer A of the look-then-resolve design (#399). Surfaces unresolved review
    threads that still need a looker, without touching any thread. Coverage is
    bounded by `_fetch_pr` (up to the first 100 threads and 100 comments per
    PR); deep cursor pagination is a follow-up if any PR exceeds those bounds.
    Each thread carries a `looked` flag, so consumers can filter the queue.
    """
    threads: list[dict[str, object]] = []
    for pr_number in _list_open_pr_numbers(args.owner, args.repo):
        threads.extend(_build_looker_queue(_fetch_pr(args.owner, args.repo, pr_number)))
    unlooked = [item for item in threads if not item["looked"]]
    print(
        json.dumps(
            {
                "open_threads": len(threads),
                "unlooked_threads": len(unlooked),
                "threads": threads,
            }
        )
    )
    return 0


def attest_resolve(args: argparse.Namespace) -> int:
    """Disposition one explicit bot-authored thread (Layer B2). Dry-run unless --apply.

    Bounded by design: targets a single PR + thread id, so it cannot walk the backlog
    or cascade. The deterministic walk + cascade-safety orchestration is Layer C.
    """
    pr = _fetch_pr(args.owner, args.repo, args.pr_number)
    threads = (pr.get("reviewThreads") or {}).get("nodes") or []
    thread = next((t for t in threads if t.get("id") == args.thread_id), None)
    if thread is None:
        thread = _fetch_thread(args.thread_id)  # beyond _fetch_pr's first-100 window
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
    result = attest_and_resolve(
        pr,
        thread,
        args.looker,
        args.decision,
        args.rationale,
        apply=args.apply,
    )
    print(json.dumps(result))
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

    unlooked = subparsers.add_parser("list-unlooked")
    unlooked.add_argument("--owner", required=True)
    unlooked.add_argument("--repo", required=True)

    attest = subparsers.add_parser("attest-resolve")
    attest.add_argument("--owner", required=True)
    attest.add_argument("--repo", required=True)
    attest.add_argument("--pr-number", required=True, type=int)
    attest.add_argument("--thread-id", required=True)
    attest.add_argument("--looker", required=True)
    attest.add_argument("--decision", required=True, choices=sorted(ATTESTATION_DECISIONS))
    attest.add_argument("--rationale", default="")
    attest.add_argument(
        "--apply",
        action="store_true",
        help="actually post the attestation and resolve (default: dry-run)",
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
    if args.command == "list-unlooked":
        return list_unlooked(args)
    if args.command == "attest-resolve":
        return attest_resolve(args)
    return enable_auto_merge(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"review_feedback_loop.py failed: {exc}", file=sys.stderr)
        raise
