#!/usr/bin/env python3
"""Lightweight portability guardrail for core runtime/governance surfaces.

Detects hardcoded user paths (Windows, macOS, Linux home directories) in the
runtime/governance surfaces that have to load identically on any of Logan's
machines. Distinct from check_portable_paths.py which guards against NETWEB
(Windows-reserved filename) collisions.

Two modes:
- report (default): print findings, exit 0 — non-blocking signal
- --strict: exit 1 on any finding — blocking gate, used by the cross-platform
  smoke workflow on pull_request events

Recovered from #310 (closed 2026-05-22, codex/greet-user-with-a-friendly-message)
with start_SPARKSEED.py reference dropped per current AGENTS.md doctrine
("Startup is OS-agnostic. No local Bash, WSL, Sparkseed, or launcher execution
is required").
"""

from __future__ import annotations

from pathlib import Path
import argparse
import re


CHECK_FILES = [
    "AGENTS.md",
    "!/WAKEUP.md",
    "!/README.md",
    "swarm.json",
    ".github/workflows/cross-platform-smoke.yml",
    ".github/workflows/sync-dependencies.yml",
]

PORTABILITY_PATTERNS = {
    "hardcoded_windows_user_path": re.compile(r"[A-Za-z]:\\\\Users\\\\", re.IGNORECASE),
    "hardcoded_macos_user_path": re.compile(r"/Users/[^/]+"),
    "hardcoded_linux_home_path": re.compile(r"/home/[^/]+"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="MESHNETWEB portability check")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when issues are found",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    failures: list[str] = []

    for rel_path in CHECK_FILES:
        file_path = repo_root / rel_path
        if not file_path.exists():
            failures.append(f"[missing] required file not found: {rel_path}")
            continue

        text = file_path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PORTABILITY_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"[{label}] {rel_path}")

    if failures:
        print("MESHNETWEB portability findings:")
        for item in failures:
            print(f" - {item}")
        if args.strict:
            print("Strict mode enabled: failing check.")
            return 1
        print("Non-strict mode: reporting only.")
        return 0

    print("MESHNETWEB portability check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
