#!/usr/bin/env python3
"""Close stale, conflicted bot PRs.

This is intentionally conservative:
- only verified automation-owned branch prefixes are considered
- only explicitly conflicted (DIRTY) PRs are considered
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
BOT_BRANCH_PREFIXES = {
    "app/dependabot": ("dependabot/",),
    "dependabot[bot]": ("dependabot/",),
    "app/github-actions": ("automation/", "bot/"),
    "github-actions[bot]": ("automation/", "bot/"),
}
STALE_LIFECYCLE_STATE = "abandoned"


def _run(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{cmd[0]} timed out after 60s") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError((exc.stderr or "").strip() or f"{cmd[0]} failed") from exc
    except OSError as exc:
        raise RuntimeError(f"{cmd[0]} could not run: {exc}") from exc
    return result.stdout


def run_json(cmd: list[str]) -> object:
    output = _run(cmd)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{cmd[0]} produced invalid JSON: {exc}") from exc


def run_text(cmd: list[str]) -> str:
    return _run(cmd).strip()


CLOSE_COMMENT = (
    "Closing automatically: stale bot PR, not merge-clean, and older than the allowed age threshold. "
    "A fresh bot PR can be regenerated later if the update is still desired."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--age-days", type=int, default=2)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report-path", type=Path, required=True)
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
        head = str(pr["headRefName"])
        if not head.startswith(BOT_BRANCH_PREFIXES[author]):
            continue

        updated_at = datetime.fromisoformat(str(pr["updatedAt"]).replace("Z", "+00:00"))
        pr_number = int(pr["number"])
        pr_age_days = (now - updated_at).days
        merge_state = merge_state_by_number.get(pr_number, "UNKNOWN")

        if merge_state != "DIRTY" or pr_age_days < age_days:
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

        # int-coerce BEFORE argv: makes "the PR number is digits, never
        # option-shaped" a type-enforced invariant rather than trust in the API.
        pr_number = int(pr["number"])
        merge_info = run_json(["gh", "pr", "view", str(pr_number), "--json", "mergeStateStatus"])
        merge_state_by_number[pr_number] = str(merge_info["mergeStateStatus"])

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
            run_text(
                [
                    "gh",
                    "pr",
                    "close",
                    str(pr["number"]),
                    "--comment",
                    CLOSE_COMMENT,
                ]
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
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"stale_bot_prs: {exc}", file=sys.stderr)
        sys.exit(1)
