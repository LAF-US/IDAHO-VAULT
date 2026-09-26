#!/usr/bin/env python3
"""Run syntax checks against repo-owned automation files."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


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
        try:
            result = subprocess.run(
                [python_executable, "-m", "py_compile", file_path],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print(f"ERROR: py_compile timed out after 30s on {file_path}")
            return 1
        if result.returncode != 0:
            print(f"ERROR in {file_path}:")
            print(result.stderr)
            return 1

    print(f"Syntax OK - {len(syntax_files)} files checked")
    return 0


def main() -> int:
    print("=" * 60)
    print("SYNTAX CHECKS")
    print("=" * 60)
    return run_syntax_checks()


if __name__ == "__main__":
    raise SystemExit(main())
