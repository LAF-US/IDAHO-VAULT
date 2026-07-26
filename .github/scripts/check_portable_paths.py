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


RESERVED_NAMES = {"AUX", "CON", "NUL", "PRN"}
RESERVED_NAMES.update({f"COM{i}" for i in range(10)})
RESERVED_NAMES.update({f"LPT{i}" for i in range(10)})
ILLEGAL_CHARS = set('<>:"|?*')
MAX_PORTABLE_PATH = 218


def git_tracked_files() -> list[str]:
    """Return every path tracked at HEAD, with non-ASCII names left unquoted."""
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotePath=false", "ls-tree", "-r", "HEAD", "--name-only"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("git ls-tree timed out after 30s") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError((exc.stderr or "").strip() or "git ls-tree failed") from exc
    return [line for line in result.stdout.splitlines() if line]


def normalize(path: str) -> str:
    """Fold a path to its case-insensitive, separator-agnostic comparison key."""
    return path.replace("\\", "/").casefold()


def case_collisions(paths: list[str]) -> dict[str, list[str]]:
    """Group paths that differ only by case (a hazard on case-insensitive filesystems)."""
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in paths:
        grouped[normalize(path)].append(path)
    return {
        key: sorted(values)
        for key, values in grouped.items()
        if len({value.replace("\\", "/") for value in values}) > 1
    }


def path_violations(path: str) -> list[str]:
    """Return cross-platform portability problems for a single path (empty if clean)."""
    findings: list[str] = []
    # A literal backslash in a tracked path is itself the hazard: on Windows git
    # treats it as a separator, so a name like `C:\Users\...` becomes an absolute
    # path and `git checkout` aborts ("invalid path"). Flag it before normalizing.
    if "\\" in path:
        findings.append(f"BACKSLASH IN PATH: {path} (illegal on Windows; breaks checkout)")
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
    """Gate changed paths (fail) and report pre-existing tree violations (warn)."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths-from-stdin", action="store_true")
    args = parser.parse_args()

    changed = [line for line in sys.stdin.read().splitlines() if line] if args.paths_from_stdin else []
    try:
        tracked = git_tracked_files()
    except RuntimeError as exc:
        print(f"check_portable_paths: {exc}", file=sys.stderr)
        return 1
    collisions = case_collisions(tracked)
    collision_members = {member for members in collisions.values() for member in members}

    # Changed-files pass: these are the only findings that FAIL the gate. A PR is
    # responsible for what it introduces, so a new portability-hostile path here
    # is a hard error.
    findings: list[str] = []
    for path in changed:
        findings.extend(path_violations(path))
        if path in collision_members:
            peers = ", ".join(collisions[normalize(path)])
            findings.append(f"CASE COLLISION: {path} (conflicts with: {peers})")

    # Whole-tree sweep: REPORT-ONLY. The changed-files pass only sees a PR's diff,
    # so a portability-hostile path already on main stays invisible while it can
    # silently break Windows checkout. Surfacing it here makes the debt visible —
    # but pre-existing offenders are not this PR's fault, so they only warn; they
    # must not fail unrelated PRs. Removing a tracked illegal path is a destructive
    # Git-control-surface change and is governed by GIT-CONTROL-SURFACES-2026-05-17
    # ("remove files from history [only] with Logan's explicit instruction").
    changed_set = set(changed)
    tree_warnings: list[str] = []
    for path in tracked:
        if path in changed_set:
            continue
        tree_warnings.extend(path_violations(path))

    if tree_warnings:
        print(
            f"NETWEB (report-only): {len(tree_warnings)} pre-existing tracked-path "
            "violation(s) — not failing this PR; disposition is Logan's call:",
            file=sys.stderr,
        )
        for warning in tree_warnings:
            print(f"  [warn] {warning}", file=sys.stderr)

    if findings:
        print("NETWEB: Cross-platform path violations detected in changed paths", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("All changed paths are cross-platform portable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
