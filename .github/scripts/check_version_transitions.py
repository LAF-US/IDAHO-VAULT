#!/usr/bin/env python3
"""Require a durable transition record for governed version changes.

Authenticated Dependabot PRs that change only requirements.txt are exempt
because the pull request and mandatory dependency-resolution check are their
durable record. Other version transitions must add a record row to
VERSION-TRANSITIONS.md in the same pull request.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = "VERSION-TRANSITIONS.md"
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{7,40}$")
RECORD_PATTERN = re.compile(r"^\+\|\s*20\d{2}-\d{2}-\d{2}\s*\|")
PYPROJECT_PATTERN = re.compile(
    r"""(?x)
    ^\s*(?:version|requires-python)\s*=
    |
    ^\s*"[^"]*(?:==|~=|>=|<=|!=|>|<)[^"]*"\s*,?\s*$
    """
)
JSON_VERSION_PATTERN = re.compile(r'"(?:version|registry_version|crewai_version)"\s*:')
AUTOMATION_VERSION_PATTERN = re.compile(
    r"""(?ix)
    \buses:\s*[^\s]+@
    |
    \bpython-version\s*:
    |
    \bversions?\s*:
    |
    \bpip(?:3)?\s+install\b[^\n]*(?:==|~=|>=|<=)
    """
)


def changed_lines(patch: str) -> list[str]:
    return [
        line[1:]
        for line in patch.splitlines()
        if line[:1] in {"+", "-"} and not line.startswith(("+++", "---"))
    ]


def is_version_transition(path: str, patch: str) -> bool:
    normalized = path.replace("\\", "/")
    lines = changed_lines(patch)
    if not lines or normalized == LEDGER_PATH:
        return False
    if normalized == ".python-version":
        return True
    if normalized == "requirements.txt":
        return any(line.strip() and not line.lstrip().startswith("#") for line in lines)
    if normalized == "pyproject.toml":
        return any(PYPROJECT_PATTERN.search(line) for line in lines)
    if normalized in {"swarm.json", ".crewai/manifest.json", "manifest.json"}:
        return any(JSON_VERSION_PATTERN.search(line) for line in lines)
    if normalized.startswith(".obsidian/plugins/") and normalized.endswith("/manifest.json"):
        return any(JSON_VERSION_PATTERN.search(line) for line in lines)
    if normalized == ".github/dependabot.yml":
        return any(AUTOMATION_VERSION_PATTERN.search(line) for line in lines)
    if normalized.startswith((".github/workflows/", ".github/actions/")) and normalized.endswith(
        (".yml", ".yaml")
    ):
        return any(AUTOMATION_VERSION_PATTERN.search(line) for line in lines)
    return False


def has_transition_record(patches: dict[str, str]) -> bool:
    return any(RECORD_PATTERN.match(line) for line in patches.get(LEDGER_PATH, "").splitlines())


def is_dependabot_lock_only(patches: dict[str, str], *, actor: str) -> bool:
    return actor == "dependabot[bot]" and set(patches) == {"requirements.txt"}


def findings_for_patches(patches: dict[str, str], *, actor: str) -> list[str]:
    governed = sorted(path for path, patch in patches.items() if is_version_transition(path, patch))
    if not governed or has_transition_record(patches):
        return []
    if governed == ["requirements.txt"] and is_dependabot_lock_only(patches, actor=actor):
        return []
    return governed


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def diff_patches(base: str, head: str) -> dict[str, str]:
    for value in (base, head):
        if not SHA_PATTERN.fullmatch(value):
            raise ValueError("base and head must be git commit SHAs")
    paths_result = run_git(["diff", "--name-only", "--diff-filter=ACMRD", "-z", base, head])
    if paths_result.returncode != 0:
        raise RuntimeError(paths_result.stderr.strip() or "git diff failed")
    paths = [path for path in paths_result.stdout.split("\0") if path]
    patches: dict[str, str] = {}
    for path in paths:
        diff_result = run_git(["diff", "--unified=0", "--no-color", base, head, "--", path])
        if diff_result.returncode != 0:
            raise RuntimeError(diff_result.stderr.strip() or f"git diff failed for {path}")
        patches[path] = diff_result.stdout
    return patches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base commit SHA")
    parser.add_argument("--head", required=True, help="head commit SHA")
    parser.add_argument("--actor", required=True, help="pull request author login")
    args = parser.parse_args()

    try:
        findings = findings_for_patches(diff_patches(args.base, args.head), actor=args.actor)
    except (RuntimeError, ValueError) as exc:
        print(f"version-transition guard: {exc}", file=sys.stderr)
        return 2

    if not findings:
        print("version-transition guard: OK")
        return 0

    print("version-transition guard: unrecorded governed version change.", file=sys.stderr)
    for path in findings:
        print(f"  {path}", file=sys.stderr)
    print(
        f"Add a compatibility/rationale row to {LEDGER_PATH}, or keep a "
        "Dependabot PR limited to requirements.txt and let required resolution checks decide it.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
