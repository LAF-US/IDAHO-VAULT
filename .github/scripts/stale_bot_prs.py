#!/usr/bin/env python3
"""Close stale, conflicted bot PRs.

This is intentionally conservative:
- only bot-authored PRs are considered
- only non-clean PRs are considered
- only PRs older than the configured age threshold are closed
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from pr_lifecycle import ensure_labels, set_state

BOT_LOGINS = {"app/dependabot", "app/github-actions", "dependabot[bot]", "github-actions[bot]"}
STALE_LIFECYCLE_STATE = "abandoned"


def run_json(cmd: list[str]) -> object:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def run_text(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--age-days", type=int, default=2)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument(
        "--comment",
        default=(
            "Closing automatically: stale bot PR, not merge-clean, and older than the allowed age threshold. "
            "A fresh bot PR can be regenerated later if the update is still desired."
        ),
    )
    return parser.parse_args()


def find_stale_bot_prs(
    open_prs: list[dict[str, object]],
    *,
    now: datetime,
    age_days: int,
    merge_state_by_number: dict[int, str],
) -> list[dict[str, object]]:
    stale: list[dict[str, object]] = []
    for pr in open_prs:
        author = (pr.get("author") or {}).get("login")
        if author not in BOT_LOGINS:
            continue

        updated_at = datetime.fromisoformat(str(pr["updatedAt"]).replace("Z", "+00:00"))
        pr_number = int(pr["number"])
        pr_age_days = (now - updated_at).days
        merge_state = merge_state_by_number.get(pr_number, "UNKNOWN")

        if merge_state == "CLEAN" or pr_age_days < age_days:
            continue

        stale.append(
            {
                "number": pr_number,
                "title": pr["title"],
                "url": pr["url"],
                "head": pr["headRefName"],
                "author": author,
                "age_days": pr_age_days,
                "merge_state": merge_state,
                "lifecycle_state": STALE_LIFECYCLE_STATE,
            }
        )

    return stale


def main() -> int:
    args = parse_args()
    now = datetime.now(timezone.utc)
    open_prs = run_json(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,url,author,updatedAt,headRefName",
        ]
    )

    merge_state_by_number: dict[int, str] = {}
    for pr in open_prs:
        author = (pr.get("author") or {}).get("login")
        if author not in BOT_LOGINS:
            continue

        merge_info = run_json(["gh", "pr", "view", str(pr["number"]), "--json", "mergeStateStatus"])
        merge_state_by_number[int(pr["number"])] = str(merge_info["mergeStateStatus"])

    stale = find_stale_bot_prs(
        open_prs,
        now=now,
        age_days=args.age_days,
        merge_state_by_number=merge_state_by_number,
    )

    if args.apply:
        ensure_labels()
        for pr in stale:
            set_state(int(pr["number"]), str(pr["lifecycle_state"]))
            subprocess.run(
                [
                    "gh",
                    "pr",
                    "close",
                    str(pr["number"]),
                    "--delete-branch",
                    "--comment",
                    args.comment,
                ],
                check=True,
            )

    lines = [
        "# Stale Bot PR Cleanup",
        "",
        f"Mode: {'APPLY' if args.apply else 'REPORT'}",
        f"Age threshold: {args.age_days} days",
        "",
    ]
    if stale:
        lines.extend(["## PRs closed" if args.apply else "## PRs to close", ""])
        for pr in stale:
            lines.append(
                f"- PR #{pr['number']} `{pr['head']}` — {pr['merge_state']}, {pr['age_days']}d old"
            )
            lines.append(f"  {pr['title']}")
            lines.append(f"  lifecycle/{pr['lifecycle_state']}")
            lines.append(f"  {pr['url']}")
    else:
        lines.append("No stale conflicted bot PRs found.")

    args.report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"stale_count={len(stale)}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
