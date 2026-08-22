#!/usr/bin/env python3
"""Verify .python-version satisfies pyproject.toml's requires-python range.

Structural replacement for one branch of the deleted VERSION-TRANSITIONS.md
ledger: instead of asking a human to remember and hand-attest that a
`.python-version` bump is still compatible with the package's declared
`requires-python` range, this derives the fact and checks it on every run.

If pyproject.toml declares no `requires-python`, there is no range to satisfy
and the check is skipped with an explicit message and exit 0 — see
read_requires_python(). Exit codes: 0 pass or skip, 1 pin violates the declared
range, 2 the guard could not run (unreadable file, unparseable version or clause).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


def _repo_root() -> Path:
    # In CI this script executes from the trusted base-branch checkout
    # (trusted-main/), while the content under test is the PRIMARY checkout —
    # which is exactly the run step's working directory: every policy workflow
    # invokes this script with cwd at the primary checkout and never sets a
    # working-directory override. Using the process cwd keeps the
    # trusted-validator split (trusted code, PR-head content) without deriving
    # any filesystem path from environment data — there is no tainted-path
    # flow left for a scanner to model, and no hard-coded runner path to break
    # on self-hosted runners or a repo rename. Local (pre-commit) runs fall
    # back to the script's own repository.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return Path.cwd()
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()
PYTHON_VERSION_PATH = REPO_ROOT / ".python-version"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"

REQUIRES_PYTHON_PATTERN = re.compile(r'^\s*requires-python\s*=\s*"([^"]+)"\s*$', re.MULTILINE)
CLAUSE_PATTERN = re.compile(r"(==|!=|>=|<=|~=|>|<)\s*([0-9][0-9.]*)")


def parse_version(text: str) -> tuple[int, ...]:
    parts = text.strip().split(".")
    if not parts or not all(part.isdigit() for part in parts):
        raise ValueError(f"not a dotted numeric version: {text!r}")
    return tuple(int(part) for part in parts)


def pad(version: tuple[int, ...], length: int) -> tuple[int, ...]:
    return version + (0,) * (length - len(version))


def padded_pair(pinned: tuple[int, ...], constraint: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    width = max(len(pinned), len(constraint))
    return pad(pinned, width), pad(constraint, width)


def compatible_release(pinned: tuple[int, ...], constraint: tuple[int, ...]) -> bool:
    """PEP 440 ~=: pinned >= constraint, matching all but the constraint's last segment."""
    if len(constraint) < 2:
        raise ValueError(f"~= requires at least two version segments: {constraint}")
    p, c = padded_pair(pinned, constraint)
    return p >= c and p[: len(constraint) - 1] == constraint[:-1]


OPERATORS = {
    "==": lambda p, c: padded_pair(p, c)[0] == padded_pair(p, c)[1],
    "!=": lambda p, c: padded_pair(p, c)[0] != padded_pair(p, c)[1],
    ">=": lambda p, c: padded_pair(p, c)[0] >= padded_pair(p, c)[1],
    "<=": lambda p, c: padded_pair(p, c)[0] <= padded_pair(p, c)[1],
    ">": lambda p, c: padded_pair(p, c)[0] > padded_pair(p, c)[1],
    "<": lambda p, c: padded_pair(p, c)[0] < padded_pair(p, c)[1],
    "~=": compatible_release,
}


def compare(pinned: tuple[int, ...], operator: str, constraint: tuple[int, ...]) -> bool:
    return OPERATORS[operator](pinned, constraint)


def read_requires_python(pyproject_text: str) -> str | None:
    # Absence is not a violation. This guard exists to catch a `.python-version`
    # bump that leaves the declared range behind; with no range declared there is
    # no constraint for the pin to contradict, so there is nothing to check and
    # nothing to fail. Returning None (rather than raising) keeps that case out
    # of main()'s error path, which reports 2 for a guard that could not run.
    #
    # This deliberately does NOT assert that requires-python must exist. Nothing
    # delegated that to this script, and inventing the requirement here would put
    # a range back by the side door — the same move the file's own history is a
    # record of going wrong. The skip is announced on stdout rather than silent,
    # so an accidental removal is visible in the log instead of reading as OK.
    match = REQUIRES_PYTHON_PATTERN.search(pyproject_text)
    if not match:
        return None
    return match.group(1)


def unsatisfied_clauses(pinned: tuple[int, ...], requires_python: str) -> list[str]:
    clauses = [clause.strip() for clause in requires_python.split(",") if clause.strip()]
    if not clauses:
        raise RuntimeError(f"requires-python has no clauses: {requires_python!r}")

    unsatisfied = []
    for clause in clauses:
        match = CLAUSE_PATTERN.match(clause)
        if not match:
            raise RuntimeError(f"unsupported requires-python clause: {clause!r}")
        operator, constraint_text = match.groups()
        constraint = parse_version(constraint_text)
        if not compare(pinned, operator, constraint):
            unsatisfied.append(clause)
    return unsatisfied


def main() -> int:
    try:
        pinned_text = PYTHON_VERSION_PATH.read_text(encoding="utf-8").strip()
        pinned = parse_version(pinned_text)
        requires_python = read_requires_python(PYPROJECT_PATH.read_text(encoding="utf-8"))
        if requires_python is None:
            print(
                "python-version-pin guard: SKIPPED — pyproject.toml declares no "
                f"requires-python, so .python-version ({pinned_text}) has no range "
                "to satisfy. Nothing to check."
            )
            return 0
        unsatisfied = unsatisfied_clauses(pinned, requires_python)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"python-version-pin guard: {exc}", file=sys.stderr)
        return 2

    if unsatisfied:
        print(
            f"python-version-pin guard: .python-version ({pinned_text}) violates "
            f"pyproject.toml's requires-python ({requires_python}):",
            file=sys.stderr,
        )
        for clause in unsatisfied:
            print(f"  {clause}", file=sys.stderr)
        return 1

    print("python-version-pin guard: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
