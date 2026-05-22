#!/usr/bin/env python3
"""NETWEB path portability guard for changed files.

Checks changed paths for Windows/macOS/Linux portability hazards and checks the
whole tracked tree for case-insensitive collisions.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


RESERVED_NAMES = {"AUX", "CON", "NUL", "PRN"}
RESERVED_NAMES.update({f"COM{i}" for i in range(10)})
RESERVED_NAMES.update({f"LPT{i}" for i in range(10)})
ILLEGAL_CHARS = set('<>:"|?*')
MAX_PORTABLE_PATH = 218


def git_tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-tree", "-r", "HEAD", "--name-only"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def normalize(path: str) -> str:
    return path.replace("\\", "/").casefold()


def case_collisions(paths: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        grouped[normalize(path)].append(path)
    return {
        key: sorted(values)
        for key, values in grouped.items()
        if len({value.replace("\\", "/") for value in values}) > 1
    }


def path_violations(path: str) -> list[str]:
    findings: list[str] = []
    parts = path.replace("\\", "/").split("/")
    for part in parts:
        if not part:
            continue
        name_no_ext = part.split(".", 1)[0].upper()
        if name_no_ext in RESERVED_NAMES:
            findings.append(f"RESERVED NAME: {path} (component: {part})")
        if part.endswith(".") or part.endswith(" "):
            findings.append(f"TRAILING PERIOD/SPACE: {path}")
        if any(char in ILLEGAL_CHARS for char in part):
            findings.append(f'ILLEGAL CHARACTER: {path} (contains < > : " | ? or *)')
    if len(path) > MAX_PORTABLE_PATH:
        findings.append(f"PATH TOO LONG: {path} ({len(path)} chars, max {MAX_PORTABLE_PATH})")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths-from-stdin", action="store_true")
    args = parser.parse_args()

    changed = [line for line in sys.stdin.read().splitlines() if line] if args.paths_from_stdin else []
    tracked = git_tracked_files()
    collisions = case_collisions(tracked)
    collision_members = {member for members in collisions.values() for member in members}

    findings: list[str] = []
    for path in changed:
        findings.extend(path_violations(path))
        if path in collision_members:
            peers = ", ".join(collisions[normalize(path)])
            findings.append(f"CASE COLLISION: {path} (conflicts with: {peers})")

    if findings:
        print("NETWEB: Cross-platform path violations detected", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("All paths are cross-platform portable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
