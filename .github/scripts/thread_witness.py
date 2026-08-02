#!/usr/bin/env python3
"""GitHub PR looker/witness — the read/classify/report side."""
# Extracted from review_feedback_loop.py on 2026-07-25 (Logan's decision: the looker is its
# own system — see REVIEW-MERGE-ENGINE-STATUS-2026-07-25.md). This module holds only the
# READ side: it resolves nothing and writes nothing.
#
# - list-unlooked  : print the unresolved-thread worklist across open PRs.
# - looker-walk    : classify every open PR into a looker lane (clear / machine-disposable
# / would-cascade / needs-human) plus a stale flag.
# - render-worklist: render a looker-walk JSON report as a markdown triage surface.
#
# The write side (attest-resolve / engage-outdated / reconcile-witness) and the shared
# plumbing still live in review_feedback_loop.py; this module imports the three engine-side
# helpers it needs (`_list_open_pr_numbers`, `_parse_iso_datetime`, `_positive_int`)
# one-directionally, so there is no import cycle. Consolidating the shared plumbing into a
# library both import is the next extraction step.

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

from pr_github import _fetch_pr
from pr_threads import (  # shared thread-analysis vocabulary (#600 §5)
    BARE_RESOLVABLE_DISPOSITIONS,
    _thread_authors,
    _thread_has_attested_look,
    _thread_is_bot_only,
    _thread_resolution_disposition,
)
from review_feedback_loop import (
    _list_open_pr_numbers,
    _parse_iso_datetime,
    _positive_int,
)


def _build_looker_queue(pr: dict) -> list[dict[str, object]]:
    """Read-only worklist of unresolved threads on one PR for a looker."""
    # Resolves nothing. Each entry carries what a looker needs to look: the
    # thread id, its comment authors, whether the anchor is outdated, whether a
    # look has already been attested, and a link.
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


# Layer C (#399): the deterministic walk. `_classify_pr_for_looker` is the pure
# routing core — it reads one PR and sorts it into a lane WITHOUT writing anything.
# The brownfield (orphaned PRs, agents gone, auto-merge armed under the maintainer
# identity) is the spec: the looker drains it *with* judgment, never past it.
#
# Lanes (by the PR's unresolved review threads):
#   - clear            : no unresolved threads.
#   - machine-disposable: every unresolved thread is bot-authored and provable, the
#                         review is not CHANGES_REQUESTED, and auto-merge is NOT armed
#                         — safe for the looker to attest-and-resolve (clears threads,
#                         never merges).
#   - would-cascade    : as machine-disposable, but auto-merge IS armed — clearing the
#                         last blocking thread could shove the PR through the barrier;
#                         hold for a deliberate signal (Layer-C apply must skip these).
#   - needs-human      : any human-authored thread, a CHANGES_REQUESTED review, or a
#                         thread whose comment page is truncated (bot-only unprovable).
# `stale` is an orthogonal abandonment flag (no activity for >= stale_days): a stale PR
# is never a safe-drain candidate regardless of lane — abandoned work needs a person.
LOOKER_STALE_DAYS = 14


def _thread_disposition(thread: dict) -> str:
    """Classify one unresolved thread. Pure. One of: human, unprovable, looked-open, bot-disposable."""
    # Split out of `_classify_pr_for_looker` so the per-thread decision is independently
    # testable and the classifier's own branching stays low.
    page_info = (thread.get("comments") or {}).get("pageInfo")
    # An explicit "complete" page is hasNextPage is False; anything else (truncated
    # OR unknown/missing) is conservatively incomplete.
    page_complete = isinstance(page_info, dict) and page_info.get("hasNextPage") is False
    if not _thread_is_bot_only(thread):
        # A human on the page we DO have is definitive — truncated or not.
        return "human"
    if not page_complete:
        # Bot-only on the visible page, but a human could lie beyond an incomplete
        # one; bot-only must be proven from the full author list, so: unprovable.
        return "unprovable"
    if _thread_has_attested_look(thread):
        return "looked-open"  # attested but unresolved (recoverable)
    return "bot-disposable"


def _select_lane(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    *,
    threads_truncated: bool,
    review_decision: str,
    human: int,
    unprovable: int,
    unresolved_count: int,
    machine_clearable: int,
    auto_merge_armed: bool,
) -> str:
    """Pick the looker lane from the tallied thread dispositions. Pure."""
    # Split out of `_classify_pr_for_looker` so lane selection is independently testable.
    if threads_truncated or review_decision == "CHANGES_REQUESTED" or human or unprovable:
        return "needs-human"
    if unresolved_count == 0:
        return "clear"
    if machine_clearable == unresolved_count:
        return "would-cascade" if auto_merge_armed else "machine-disposable"
    return "needs-human"  # defensive; every unresolved thread is classified above


def _tally_thread_plan(
    unresolved: list[dict],
) -> tuple[list[dict[str, object]], dict[str, int]]:
    """Disposition each unresolved thread into a plan + per-lane counts. Pure."""
    # Split out of `_classify_pr_for_looker` so the per-thread tally is independently
    # testable and the classifier's own branching stays low.
    plan: list[dict[str, object]] = []
    counts = {"human": 0, "unprovable": 0, "looked-open": 0, "bot-disposable": 0}
    for thread in unresolved:
        disposition = _thread_disposition(thread)
        counts[disposition] += 1
        plan.append(
            {
                "thread_id": thread.get("id"),
                "disposition": disposition,
                "resolution": _thread_resolution_disposition(thread),
                "authors": sorted(_thread_authors(thread)),
            }
        )
    return plan, counts


def _tally_resolution_counts(plan: list[dict[str, object]]) -> dict[str, int]:
    """Count plan entries by their bare-resolution disposition. Pure."""
    resolution_counts: dict[str, int] = {}
    for entry in plan:
        key = str(entry["resolution"])
        resolution_counts[key] = resolution_counts.get(key, 0) + 1
    return resolution_counts


def _looker_pr_signals(pr: dict, *, now: datetime, stale_days: int) -> dict[str, object]:
    """Derive the PR-level lane signals (review decision, arming, staleness). Pure."""
    last_activity = _parse_iso_datetime(pr.get("updatedAt") or pr.get("createdAt"))
    return {
        "review_decision": pr.get("reviewDecision") or "",
        "auto_merge_armed": bool((pr.get("autoMergeRequest") or {}).get("enabledAt")),
        "stale": bool(
            last_activity and (now - last_activity) >= timedelta(days=stale_days)
        ),
    }


def _is_safe_to_drain(lane: str, *, stale: bool, plan: list[dict[str, object]]) -> bool:
    """Report whether a PR is a bare-drainable apply-pass candidate. Pure."""
    # A bare attest-and-resolve could clear every thread WITHOUT a fix, so this demands
    # more than the coarse machine-disposable lane: the PR must not be stale, and every
    # thread must be bare-resolvable (outdated/looked). A needs-fix or apply-suggestion
    # thread is NOT bare-drainable. (codex on #529.)
    return (
        lane == "machine-disposable"
        and not stale
        and all(entry["resolution"] in BARE_RESOLVABLE_DISPOSITIONS for entry in plan)
    )


def _classify_pr_for_looker(
    pr: dict, *, now: datetime | None = None, stale_days: int = LOOKER_STALE_DAYS
) -> dict:
    """Sort one PR into a looker lane. Pure and read-only — resolves nothing."""
    now = now or datetime.now(timezone.utc)
    review_threads = pr.get("reviewThreads") or {}
    threads = review_threads.get("nodes") or []
    # The thread list itself is fetched first: 100. If it is truncated, a blocking
    # human/unprovable thread may lie beyond the page — the PR is never safe to drain.
    threads_truncated = bool((review_threads.get("pageInfo") or {}).get("hasNextPage"))
    unresolved = [t for t in threads if not t.get("isResolved")]

    plan, counts = _tally_thread_plan(unresolved)
    resolution_counts = _tally_resolution_counts(plan)
    machine_clearable = counts["bot-disposable"] + counts["looked-open"]
    signals = _looker_pr_signals(pr, now=now, stale_days=stale_days)

    lane = _select_lane(
        threads_truncated=threads_truncated,
        review_decision=signals["review_decision"],
        human=counts["human"],
        unprovable=counts["unprovable"],
        unresolved_count=len(unresolved),
        machine_clearable=machine_clearable,
        auto_merge_armed=signals["auto_merge_armed"],
    )

    return {
        "pr": pr.get("number"),
        "url": pr.get("url"),
        "lane": lane,
        "stale": signals["stale"],
        "safe_to_drain": _is_safe_to_drain(lane, stale=signals["stale"], plan=plan),
        "auto_merge_armed": signals["auto_merge_armed"],
        "review_decision": signals["review_decision"] or None,
        "is_draft": bool(pr.get("isDraft")),
        "threads_truncated": threads_truncated,
        "unresolved_threads": len(unresolved),
        "machine_clearable": machine_clearable,
        "human_threads": counts["human"],
        "unprovable_threads": counts["unprovable"],
        "resolution_counts": resolution_counts,
        "threads": plan,
    }


def list_unlooked(args: argparse.Namespace) -> int:
    """Print the looker queue across open PRs. Read-only: resolves nothing."""
    # Layer A of the look-then-resolve design (#399). Surfaces unresolved review
    # threads that still need a looker, without touching any thread. Coverage is
    # bounded by `_fetch_pr` (up to the first 100 threads and 100 comments per
    # PR); deep cursor pagination is a follow-up if any PR exceeds those bounds.
    # Each thread carries a `looked` flag, so consumers can filter the queue.
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


def looker_walk(args: argparse.Namespace) -> int:
    """Walk every open PR and print the looker triage report. Read-only — resolves nothing."""
    # Layer C of the look-then-resolve design (#399): turns the open-PR backlog into a
    # classified worklist (clear / machine-disposable / would-cascade / needs-human, plus a
    # stale/abandonment flag) so the backlog drains *with* judgment. This command WRITES
    # NOTHING; the guarded disposition path is `attest-resolve` (B2), gated separately. The
    # `safe_to_drain` list names the PRs a deterministic apply pass could clear without a
    # cascade or touching a human thread.
    now = datetime.now(timezone.utc)
    reports = [
        _classify_pr_for_looker(
            _fetch_pr(args.owner, args.repo, pr_number),
            now=now,
            stale_days=args.stale_days,
        )
        for pr_number in _list_open_pr_numbers(args.owner, args.repo)
    ]
    by_lane: dict[str, int] = {}
    by_resolution: dict[str, int] = {}
    for report in reports:
        by_lane[str(report["lane"])] = by_lane.get(str(report["lane"]), 0) + 1
        for key, count in (report.get("resolution_counts") or {}).items():
            by_resolution[key] = by_resolution.get(key, 0) + int(count)
    print(
        json.dumps(
            {
                "open_prs": len(reports),
                "by_lane": by_lane,
                # backlog-wide thread breakdown by how each gets resolved: how much
                # the engine can auto-apply vs. what needs a real agent fix vs. human.
                "by_resolution": by_resolution,
                "stale": sum(1 for report in reports if report["stale"]),
                "safe_to_drain": [report["pr"] for report in reports if report["safe_to_drain"]],
                "reports": reports,
            }
        )
    )
    return 0


def _fmt_counts(mapping: dict) -> str:
    """Format a {key: count} mapping as a compact ` · `-joined string. Pure."""
    return " · ".join(f"{key}: {value}" for key, value in sorted(mapping.items())) or "none"


def _pr_worklist_row(r: dict) -> str:
    """Render one actionable PR as a markdown worklist row (with flag suffix). Pure."""
    flags = [
        flag
        for flag, on in (
            ("stale", r.get("stale")),
            ("auto-merge-armed", r.get("auto_merge_armed")),
            ("threads-truncated", r.get("threads_truncated")),
        )
        if on
    ]
    flag_s = f" _({', '.join(flags)})_" if flags else ""
    return (
        f"- **#{r.get('pr')}** — lane `{r.get('lane')}` · "
        f"{int(r.get('unresolved_threads') or 0)} unresolved "
        f"({_fmt_counts(r.get('resolution_counts') or {})}){flag_s}"
    )


def _worklist_header(report: dict) -> list[str]:
    """Build the summary header block (totals, by-lane/by-resolution, safe_to_drain). Pure."""
    open_prs = int(report.get("open_prs") or 0)
    stale = int(report.get("stale") or 0)
    safe = report.get("safe_to_drain") or []
    lines = [
        "## Looker Worklist — review-thread triage (read-only)",
        "",
        "> Deterministic census of open PRs. **No threads resolved, no PRs merged.**",
        "> The gated apply pass (`attest-resolve --apply`) is a separate decision.",
        "",
        f"- **Open PRs:** {open_prs} · **stale:** {stale}",
        f"- **By lane:** {_fmt_counts(report.get('by_lane') or {})}",
        f"- **By resolution:** {_fmt_counts(report.get('by_resolution') or {})}",
        "",
        "### `safe_to_drain` — bare-resolvable, non-stale (a gated apply pass could clear)",
    ]
    lines.extend([f"- #{pr}" for pr in safe] or ["- none"])
    return lines


def _worklist_body(reports: list) -> list[str]:
    """Build the per-PR worklist rows for every PR not in the `clear` lane. Pure."""
    # Filter on lane, NOT visible unresolved count: a PR whose thread list is truncated
    # past page 1 is lane `needs-human` with possibly 0 *visible* unresolved threads — it
    # must still surface, because the census cannot prove it is clear. (codex on #531.)
    actionable = sorted(
        (r for r in reports if r.get("lane") != "clear"),
        key=lambda r: int(r.get("pr") or 0),
    )
    if not actionable:
        return ["- none — every open PR is in the `clear` lane."]
    return [_pr_worklist_row(r) for r in actionable]


def render_looker_worklist(report: dict) -> str:
    """Render a looker-walk report (the `looker_walk` JSON) as a markdown worklist. Pure."""
    # A read-only triage surface for a durable issue: the open-PR backlog grouped by lane
    # and by resolution disposition, so a looker can drain it with judgment. Resolves
    # nothing and decides nothing — it only makes the deterministic census legible.
    lines = _worklist_header(report)
    lines.append("")
    lines.append("### Per-PR worklist (PRs not in the `clear` lane)")
    lines.extend(_worklist_body(report.get("reports") or []))
    lines.append("")
    return "\n".join(lines)


def render_worklist(args: argparse.Namespace) -> int:  # pylint: disable=unused-argument
    """Read a looker-walk JSON report from stdin and print the markdown worklist."""
    # stdin is the ONLY input: the shell's own redirect (`render-worklist < report.json`)
    # covers the file case, so the tool takes no path argument at all — no user-controlled
    # path, nothing to open, nothing to sanitize.
    raw = sys.stdin.read()
    print(render_looker_worklist(json.loads(raw or "{}")))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for the looker's read-only subcommands."""
    parser = argparse.ArgumentParser(prog="thread_witness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    unlooked = subparsers.add_parser("list-unlooked")
    unlooked.add_argument("--owner", required=True)
    unlooked.add_argument("--repo", required=True)

    walk = subparsers.add_parser("looker-walk")
    walk.add_argument("--owner", required=True)
    walk.add_argument("--repo", required=True)
    walk.add_argument(
        "--stale-days",
        type=_positive_int,
        default=LOOKER_STALE_DAYS,
        help="days of inactivity before a PR is flagged stale (positive int)",
    )

    subparsers.add_parser("render-worklist")
    return parser


def main() -> int:
    """Dispatch the parsed read-only looker subcommand."""
    args = build_parser().parse_args()
    if args.command == "list-unlooked":
        return list_unlooked(args)
    if args.command == "looker-walk":
        return looker_walk(args)
    if args.command == "render-worklist":
        return render_worklist(args)
    raise SystemExit(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
