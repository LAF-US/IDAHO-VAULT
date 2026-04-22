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
  - promote-ready: scan open PRs and promote low-risk PRs to `auto-merge` only
    when the grace window has elapsed and derived state says they are ready.
  - enable-auto-merge: perform one final derived-state safety check before
    arming GitHub auto-merge for a PR labeled `auto-merge`.
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

DEFAULT_REVIEW_REQUIRED_LABEL = "review-required"
DEFAULT_THREAD_LABEL = "review-threads-open"
DEFAULT_PENDING_LABEL = "copilot-apply-pending"
DEFAULT_REVIEW_PENDING_LABEL = "agent-review-pending"
DEFAULT_AUTO_MERGE_LABEL = "auto-merge"
RISK_LOW_LABEL = "risk/low"
RISK_HIGH_LABEL = "risk/high"

LABEL_SPECS: dict[str, tuple[str, str]] = {
    DEFAULT_AUTO_MERGE_LABEL: (
        "0E8A16",
        "Low-risk PR is currently eligible for auto-merge.",
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
        "Low-risk PR is not yet eligible for auto-merge promotion.",
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
          labels(first: 50) {
            nodes { name }
          }
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              isOutdated
              comments(first: 20) {
                nodes {
                  author { login }
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
    if RISK_LOW_LABEL in labels:
        return "low"
    if RISK_HIGH_LABEL in labels:
        return "high"
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
    eligible_for_auto_merge = low_risk and grace_elapsed and not merge_blocked
    should_have_agent_review_pending = (
        low_risk
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

    if bool(state["merge_blocked"]) and DEFAULT_AUTO_MERGE_LABEL in current_labels:
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


def _build_gate_report(
    owner: str,
    repo: str,
    *,
    now: datetime | None = None,
    grace_minutes: int = DEFAULT_GRACE_MINUTES,
    auto_resolve_reviewers: set[str] | None = None,
) -> dict[str, object]:
    # The cron is a gardener, not a re-gater. It scans only PRs already in
    # `agent-review-pending` and performs the single forward-advance transition
    # (pending -> auto-merge) when the grace window has elapsed and nothing is
    # blocking. The full five-axis label projection lives in event-driven
    # workflows (push/comment/review) where there is actually new information
    # to react to; a 30-minute tick is not new information.
    open_prs = json.loads(
        _run(
            [
                "gh",
                "pr",
                "list",
                "--state",
                "open",
                "--label",
                DEFAULT_REVIEW_PENDING_LABEL,
                "--json",
                "number",
            ]
        ).stdout
        or "[]"
    )

    evaluated: list[dict[str, object]] = []
    promoted: list[int] = []
    for pr_row in open_prs:
        pr_number = int(pr_row["number"])
        pr = _fetch_pr(owner, repo, pr_number)
        state = evaluate_review_state(
            pr,
            now=now,
            grace_minutes=grace_minutes,
            auto_resolve_reviewers=auto_resolve_reviewers,
        )

        actions: list[str] = []
        current_labels = set(state["labels"])
        if (
            state["eligible_for_auto_merge"]
            and not bool(state["merge_blocked"])
            and DEFAULT_AUTO_MERGE_LABEL not in current_labels
        ):
            if DEFAULT_REVIEW_PENDING_LABEL in current_labels:
                _edit_label(pr_number, remove=DEFAULT_REVIEW_PENDING_LABEL)
                actions.append(f"remove:{DEFAULT_REVIEW_PENDING_LABEL}")
            _edit_label(pr_number, add=DEFAULT_AUTO_MERGE_LABEL)
            actions.append(f"add:{DEFAULT_AUTO_MERGE_LABEL}")
            _comment(
                pr_number,
                f"⏱️ Agent review grace period ({grace_minutes} min) elapsed "
                f"with no blocking feedback. Promoting to `auto-merge`.",
            )
            promoted.append(pr_number)

        evaluated.append(
            {
                "number": pr_number,
                "eligible_for_auto_merge": state["eligible_for_auto_merge"],
                "low_risk": state["low_risk"],
                "merge_blocked": state["merge_blocked"],
                "blocking_reasons": state["blocking_reasons"],
                "actions": actions,
            }
        )

    return {
        "checked_prs": len(evaluated),
        "promoted_prs": promoted,
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
    report = _build_gate_report(
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
    if DEFAULT_AUTO_MERGE_LABEL in labels and not bool(state["merge_blocked"]):
        _run(
            [
                "gh",
                "pr",
                "merge",
                str(args.pr_number),
                "--squash",
                "--delete-branch",
                "--auto",
            ]
        )
        enabled = True

    print(
        json.dumps(
            {
                "enabled": enabled,
                "merge_blocked": state["merge_blocked"],
                "blocking_reasons": state["blocking_reasons"],
                "label_actions": label_actions,
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

    enable = subparsers.add_parser("enable-auto-merge")
    enable.add_argument("--owner", required=True)
    enable.add_argument("--repo", required=True)
    enable.add_argument("--pr-number", required=True, type=int)
    enable.add_argument("--grace-minutes", type=int, default=DEFAULT_GRACE_MINUTES)

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
    return enable_auto_merge(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"review_feedback_loop.py failed: {exc}", file=sys.stderr)
        raise
