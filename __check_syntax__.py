#!/usr/bin/env python3
"""Syntax check script for repo-owned helper Python files."""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
FILES_TO_CHECK = [
    "scripts/render_flatten_attribution.py",
    "doctrinal_flatten.py",
    "sort_audit.py",
    "main.py",
]
UNITTEST_TARGET = "!\\tests\\test_app.py"


def run_syntax_checks() -> bool:
    all_passed = True
    for file_path in FILES_TO_CHECK:
        full_path = REPO_ROOT / file_path
        try:
            py_compile.compile(str(full_path), doraise=True)
            print(f"✓ {file_path} - PASSED")
        except py_compile.PyCompileError as exc:
            print(f"✗ {file_path} - FAILED")
            print(f"  Error: {exc}")
            all_passed = False
    return all_passed


def run_unittests(python_executable: str = sys.executable) -> int:
    result = subprocess.run(
        [python_executable, "-m", "unittest", UNITTEST_TARGET, "-v"],
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
    print("PYTHON SYNTAX CHECKS")
    print("=" * 60)
    all_passed = run_syntax_checks()

    print()
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    test_status = run_unittests()

    return 0 if all_passed and test_status == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
