#!/usr/bin/env python3
"""Run syntax checks and pytest against repo-owned automation files."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
TEST_FILES = [
    "tests/test_topology_census.py",
    "tests/test_stale_bot_prs.py",
    "tests/test_review_feedback_loop.py",
    "tests/test_metadata_survey.py",
    "tests/test_backfill_daily_notes.py",
    "tests/test_daily_rollover.py",
]


def collect_syntax_files() -> list[str]:
    files: set[str] = set()
    for pattern in (".github/scripts/*.py", ".github/swarm/tools/*.py"):
        files.update(str(path.relative_to(REPO_ROOT)) for path in REPO_ROOT.glob(pattern))
    return sorted(files)


def run_syntax_checks(python_executable: str = sys.executable) -> int:
    syntax_files = collect_syntax_files()
    if not syntax_files:
        print("No Python files found to check")
        return 0

    for file_path in syntax_files:
        result = subprocess.run(
            [python_executable, "-m", "py_compile", file_path],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"ERROR in {file_path}:")
            print(result.stderr)
            return 1

    print(f"Syntax OK - {len(syntax_files)} files checked")
    return 0


def run_pytest(python_executable: str = sys.executable) -> int:
    result = subprocess.run(
        [python_executable, "-m", "pytest", *TEST_FILES, "-v"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode


def main() -> int:
    print("=" * 60)
    print("SYNTAX CHECKS")
    print("=" * 60)
    syntax_status = run_syntax_checks()
    if syntax_status != 0:
        return syntax_status

    print("\n" + "=" * 60)
    print("PYTEST")
    print("=" * 60)
    return run_pytest()


if __name__ == "__main__":
    raise SystemExit(main())
