#!/usr/bin/env python3
"""Render a PR-loop reconciliation report into issue-friendly markdown."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def build_report(report: dict[str, object]) -> tuple[str, bool]:
    blocked = list(report.get("auto_merge_authorization_blocked") or [])
    evaluated = list(report.get("evaluated") or [])
    promoted = list(report.get("promoted_prs") or [])
    rearmed = list(report.get("rearmed_prs") or [])
    resolved_threads = int(report.get("resolved_outdated_threads") or 0)
    checked_prs = int(report.get("checked_prs") or 0)
    has_findings = bool(blocked)

    lines = [
        "# PR Loop Watchdog",
        "",
        f"Open PRs checked: **{checked_prs}**",
        f"Promoted to `auto-merge`: **{len(promoted)}**",
        f"Auto-merge re-armed: **{len(rearmed)}**",
        f"Outdated advisory threads resolved: **{resolved_threads}**",
        "",
    ]

    if has_findings:
        lines.extend(
            [
                "## Findings",
                "",
                "The self-healing reconciliation loop ran, but some PRs still could not be re-armed for auto-merge:",
                "",
            ]
        )
        for item in evaluated:
            number = item.get("number")
            if number not in blocked:
                continue
            arm_error = item.get("auto_merge_arm_error") or "Unknown arm error."
            lines.append(f"- PR #{number}: {arm_error}")
        lines.extend(
            [
                "",
                "These findings usually point to repository settings or branch protection drift rather than PR review-state drift.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "No unresolved PR-loop blockers remain after reconciliation.",
                "",
            ]
        )

    if evaluated:
        lines.extend(["## Evaluated PRs", ""])
        for item in evaluated:
            number = item.get("number")
            blocking_reasons = list(item.get("blocking_reasons") or [])
            actions = list(item.get("actions") or [])
            summary = [
                f"eligible={item.get('eligible_for_auto_merge')}",
                f"merge_blocked={item.get('merge_blocked')}",
                f"auto_merge_enabled={item.get('auto_merge_enabled')}",
            ]
            lines.append(f"- PR #{number} — {', '.join(summary)}")
            if blocking_reasons:
                lines.append(f"  - blocking reasons: {', '.join(str(reason) for reason in blocking_reasons)}")
            if actions:
                lines.append(f"  - actions: {', '.join(str(action) for action in actions)}")
            arm_error = item.get("auto_merge_arm_error")
            if arm_error:
                lines.append(f"  - arm error: {arm_error}")
        lines.append("")

    return "\n".join(lines) + "\n", has_findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--report-path", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = json.loads(args.report_json.read_text(encoding="utf-8"))
    markdown, has_findings = build_report(report)
    args.report_path.write_text(markdown, encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"has_findings={'true' if has_findings else 'false'}\n")
            fh.write(f"checked_prs={int(report.get('checked_prs') or 0)}\n")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - workflow-facing failure path
        print(f"pr_loop_watchdog.py failed: {exc}", file=sys.stderr)
        raise
