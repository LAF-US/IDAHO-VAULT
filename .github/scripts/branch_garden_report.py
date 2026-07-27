#!/usr/bin/env python3
"""Generate an idempotent Arborscape branch garden report."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

CLASSIFICATIONS = (
    "SALVAGE",
    "CHERRY-PICK",
    "PRUNE",
    "LIVING_WORKTREE",
    "IDENTICAL",
    "FOREIGN_HISTORY",
)


@dataclass(frozen=True)
class BranchState:
    branch: str
    classification: str
    recommendation: str
    age_days: int
    pr_number: int | None = None
    pr_url: str | None = None
    pr_title: str | None = None
    ahead: int | None = None
    behind: int | None = None
    has_merge_base: bool = True
    living_worktree: bool = False


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


def run_text(cmd: list[str]) -> str:
    return _run(cmd).strip()


def run_json(cmd: list[str]) -> object:
    output = _run(cmd)
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{cmd[0]} produced invalid JSON: {exc}") from exc


def branch_age_days(branch: str) -> int:
    ts = run_text(["git", "log", "-1", "--format=%ct", f"origin/{branch}"])
    now = datetime.now(timezone.utc).timestamp()
    return int((now - int(ts)) // 86400)


def branch_has_merge_base(branch: str) -> bool:
    try:
        run_text(["git", "merge-base", "origin/main", f"origin/{branch}"])
    except subprocess.CalledProcessError as exc:
        if exc.returncode == 1:
            return False
        raise
    return True


def living_worktree_branches() -> set[str]:
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (subprocess.TimeoutExpired, OSError):
        return set()
    if result.returncode != 0:
        return set()

    branches: set[str] = set()
    for line in result.stdout.splitlines():
        if not line.startswith("branch "):
            continue
        ref = line.removeprefix("branch ").strip()
        if ref.startswith("refs/heads/"):
            branches.add(ref.removeprefix("refs/heads/"))
    return branches


def classify_branch(
    *,
    branch: str,
    pr: dict | None,
    age_days: int,
    has_merge_base: bool,
    ahead: int | None,
    behind: int | None,
    checked_out: bool,
    stale_days: int,
    stale_behind: int,
) -> BranchState:
    if checked_out:
        return BranchState(
            branch=branch,
            classification="LIVING_WORKTREE",
            recommendation="Inventory only; a checked-out branch is live local state.",
            age_days=age_days,
            pr_number=int(pr["number"]) if pr else None,
            pr_url=pr.get("url") if pr else None,
            pr_title=pr.get("title") if pr else None,
            ahead=ahead,
            behind=behind,
            has_merge_base=has_merge_base,
            living_worktree=True,
        )

    if not has_merge_base:
        return BranchState(
            branch=branch,
            classification="FOREIGN_HISTORY",
            recommendation="Quarantine for SALVAGE review; do not decide by ahead/behind counts.",
            age_days=age_days,
            pr_number=int(pr["number"]) if pr else None,
            pr_url=pr.get("url") if pr else None,
            pr_title=pr.get("title") if pr else None,
            has_merge_base=False,
        )

    if ahead == 0 and pr:
        return BranchState(
            branch=branch,
            classification="IDENTICAL",
            recommendation="Open PR branch is equivalent to main; mark superseded instead of re-salvaging.",
            age_days=age_days,
            pr_number=int(pr["number"]),
            pr_url=pr.get("url"),
            pr_title=pr.get("title"),
            ahead=ahead,
            behind=behind,
        )

    if ahead == 0:
        return BranchState(
            branch=branch,
            classification="PRUNE",
            recommendation="No unique payload detected; deletion still requires Logan approval.",
            age_days=age_days,
            ahead=ahead,
            behind=behind,
        )

    if pr:
        return BranchState(
            branch=branch,
            classification="SALVAGE",
            recommendation="Open PR is the active salvage path; verify checks, reviews, and signing.",
            age_days=age_days,
            pr_number=int(pr["number"]),
            pr_url=pr.get("url"),
            pr_title=pr.get("title"),
            ahead=ahead,
            behind=behind,
        )

    if behind is not None and behind >= stale_behind:
        return BranchState(
            branch=branch,
            classification="CHERRY-PICK",
            recommendation="No PR and far behind main; isolate useful payload onto trunk-directed work.",
            age_days=age_days,
            ahead=ahead,
            behind=behind,
        )

    return BranchState(
        branch=branch,
        classification="SALVAGE",
        recommendation=(
            "No PR carries this payload; attach it to a PR"
            if age_days >= stale_days
            else "No PR yet; keep visible until the next census"
        ),
        age_days=age_days,
        ahead=ahead,
        behind=behind,
    )


def state_line(state: BranchState) -> str:
    pr_state = f"open PR #{state.pr_number}" if state.pr_number else "no PR"
    if not state.has_merge_base:
        distance = "no merge base with `main`"
    else:
        distance = f"{state.ahead} ahead / {state.behind} behind"
    return (
        f"- `{state.branch}` - {state.classification}; {pr_state}; "
        f"{distance}; {state.age_days}d old; {state.recommendation}"
    )


def finding_line(state: BranchState, stale_days: int) -> str | None:
    if state.classification == "FOREIGN_HISTORY":
        return (
            f"- `{state.branch}` is FOREIGN_HISTORY: require SALVAGE review "
            "before any prune decision."
        )
    if state.classification == "IDENTICAL":
        return (
            f"- `{state.branch}` is IDENTICAL to main while PR #{state.pr_number} "
            "is still open; supersede rather than re-salvage."
        )
    if state.classification == "PRUNE":
        return (
            f"- `{state.branch}` is PRUNE-candidate: no PR and 0 commits ahead of main; "
            "deletion remains gated."
        )
    if state.classification == "CHERRY-PICK":
        return (
            f"- `{state.branch}` is CHERRY-PICK-candidate: {state.behind} commits "
            "behind main with no PR."
        )
    if (
        state.classification == "SALVAGE"
        and state.pr_number is None
        and state.age_days >= stale_days
    ):
        return f"- `{state.branch}` is SALVAGE-candidate: no PR and {state.age_days} days old."
    return None


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
    worktree_heads = living_worktree_branches()

    findings: list[str] = []
    inventory: list[str] = []
    states: list[BranchState] = []
    for branch in sorted(branches):
        age_days = branch_age_days(branch)
        pr = pr_by_head.get(branch)
        has_merge_base = branch_has_merge_base(branch)
        ahead: int | None = None
        behind: int | None = None
        if has_merge_base:
            ahead = int(run_text(["git", "rev-list", f"origin/main..origin/{branch}", "--count"]) or "0")
            behind = int(run_text(["git", "rev-list", f"origin/{branch}..origin/main", "--count"]) or "0")

        state = classify_branch(
            branch=branch,
            pr=pr,
            age_days=age_days,
            has_merge_base=has_merge_base,
            ahead=ahead,
            behind=behind,
            checked_out=branch in worktree_heads,
            stale_days=args.stale_days,
            stale_behind=args.stale_behind,
        )
        states.append(state)
        inventory.append(state_line(state))
        finding = finding_line(state, args.stale_days)
        if finding:
            findings.append(finding)

    counts = Counter(state.classification for state in states)
    lines = [
        "# Branch Garden Report",
        "",
        f"Remote branches outside trunk: {len(branches)}",
        "",
        "## Arborscape Protocol",
        "",
        "- Scope: remote branches and open PR heads only.",
        "- Default action ladder: SALVAGE -> CHERRY-PICK -> PRUNE.",
        "- This report does not merge, close, or delete branches.",
        "- Branch deletion remains gated by Logan approval unless a branch is already merged/closed and proven payload-free.",
        "",
        "## Classification Summary",
        "",
        *(f"- {name}: {counts.get(name, 0)}" for name in CLASSIFICATIONS),
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
            for name in CLASSIFICATIONS:
                output_name = name.lower().replace("-", "_")
                fh.write(f"classification_{output_name}={counts.get(name, 0)}\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as exc:
        print(f"branch_garden_report: {exc}", file=sys.stderr)
        sys.exit(1)
