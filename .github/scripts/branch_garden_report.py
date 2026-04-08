#!/usr/bin/env python3
"""Generate a weekly branch garden report."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_text(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def run_json(cmd: list[str]) -> object:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def branch_age_days(branch: str) -> int:
    ts = run_text(["git", "log", "-1", "--format=%ct", f"origin/{branch}"])
    now = datetime.now(timezone.utc).timestamp()
    return int((now - int(ts)) // 86400)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument("--stale-days", type=int, default=7)
    parser.add_argument("--stale-behind", type=int, default=100)
    args = parser.parse_args()

    branches_raw = run_text(["git", "ls-remote", "--heads", "origin"])
    branches = []
    for line in branches_raw.splitlines():
        if not line.strip():
            continue
        _, ref = line.split("\t", 1)
        branch = ref.replace("refs/heads/", "")
        if branch == "main":
            continue
        branches.append(branch)

    open_prs = run_json(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--json",
            "number,headRefName,title,url",
        ]
    )
    pr_by_head = {pr["headRefName"]: pr for pr in open_prs}

    findings: list[str] = []
    inventory: list[str] = []
    for branch in sorted(branches):
        ahead = int(run_text(["git", "rev-list", f"origin/main..origin/{branch}", "--count"]) or "0")
        behind = int(run_text(["git", "rev-list", f"origin/{branch}..origin/main", "--count"]) or "0")
        age_days = branch_age_days(branch)
        pr = pr_by_head.get(branch)
        if pr:
            inventory.append(
                f"- `{branch}` — open PR #{pr['number']}, {ahead} ahead / {behind} behind, {age_days}d old"
            )
            continue

        inventory.append(f"- `{branch}` — no PR, {ahead} ahead / {behind} behind, {age_days}d old")
        if ahead == 0:
            findings.append(f"- `{branch}` is a zombie branch: no PR and 0 commits ahead of `main`.")
        elif behind >= args.stale_behind:
            findings.append(
                f"- `{branch}` is far behind `main`: {behind} commits behind with no PR."
            )
        elif age_days >= args.stale_days:
            findings.append(f"- `{branch}` is stale: no PR and {age_days} days old.")

    lines = [
        "# Branch Garden Report",
        "",
        f"Remote branches outside trunk: {len(branches)}",
        "",
    ]
    if findings:
        lines.extend(["## Findings", "", *findings, ""])
    else:
        lines.extend(["No branch-garden findings. The tree is tidy.", ""])

    if inventory:
        lines.extend(["## Inventory", "", *inventory, ""])

    args.report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"has_findings={'true' if bool(findings) else 'false'}\n")
            fh.write(f"branch_count={len(branches)}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
