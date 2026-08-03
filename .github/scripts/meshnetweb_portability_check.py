#!/usr/bin/env python3
"""Lightweight portability guardrail for core runtime/governance surfaces.

Detects hardcoded user paths (Windows, macOS, Linux home directories) in the
runtime/governance surfaces that have to load identically on any of Logan's
machines. Distinct from check_portable_paths.py which guards against NETWEB
(Windows-reserved filename) collisions.

Coverage is a *sweep*, not a list. It used to name six files, which meant the
checker could only ever find what someone had already thought to enumerate —
and it was, in fact, missing live violations sitting at the repository root
(`final_test_runner.py`, `run_all_tests.py` and their duplicates all begin
`os.chdir(r"C:\\Users\\loganf\\Documents\\IDAHO-VAULT")`). A guard whose
coverage is a hand-written list finds only what its author already knew.

Two scopes, because they warrant different verdicts:

- GATED: the startup surfaces plus everything under `.github/` — the code
  that actually has to run on any machine. A finding here fails --strict.
- SWEPT: every other tracked script and workflow. Reported always, never
  fatal. Root-level debris is a real problem but not this gate's to enforce,
  and a gate that cannot pass on the day it ships teaches people to ignore it.

Two modes:
- report (default): print findings, exit 0 — non-blocking signal
- --strict: exit 1 on findings in GATED scope, used by the cross-platform
  smoke workflow on pull_request events

Recovered from #310 (closed 2026-05-22, codex/greet-user-with-a-friendly-message)
with start_SPARKSEED.py reference dropped per current AGENTS.md doctrine
("Startup is OS-agnostic. No local Bash, WSL, Sparkseed, or launcher execution
is required").
"""

from __future__ import annotations

from pathlib import Path
import argparse
import os
import re
import sys

from startup_surfaces import candidates, resolve_rel

# Startup surfaces are named, not located: each is resolved to wherever it
# currently lives (canonical path, NETWEB `_PREFIX` alias, or root form).
# Moving one is the Architect's prerogative and must not break this check.
SURFACE_NAMES = ["AGENTS", "WAKEUP", "NEST_README", "SWARM"]

SCAN_SUFFIXES = {".py", ".ps1", ".sh", ".bash", ".yml", ".yaml"}

# Vendored, generated, or transient trees. Shell snapshots are point-in-time
# captures of a developer's environment: they contain home paths by nature and
# are not a runtime surface.
EXCLUDED_PREFIXES = (
    ".obsidian/",
    "node_modules/",
    ".venv/",
    "venv/",
    "trusted-main/",
    ".claude/shell-snapshots/",
    ".claude/plugins/",
    ".serena/",
    ".git/",
)

# These two *define* the patterns; their own source necessarily contains them.
SELF_REFERENTIAL = (
    ".github/scripts/meshnetweb_portability_check.py",
    ".github/scripts/check_portable_paths.py",
)

GATED_PREFIXES = (".github/",)

PORTABILITY_PATTERNS = {
    "hardcoded_windows_user_path": re.compile(r"[A-Za-z]:\\+Users\\+", re.IGNORECASE),
    "hardcoded_macos_user_path": re.compile(r"/Users/[^/\s\"']+"),
    "hardcoded_linux_home_path": re.compile(r"/home/[^/\s\"']+"),
}


def scan_targets(repo_root: Path) -> list[str]:
    """Scriptable surfaces worth scanning, excluding vendored/transient trees.

    Walks the working tree rather than shelling out to `git ls-files`. The
    filesystem hands back `str` paths already decoded by Python, which sidesteps
    the locale question entirely — the git subprocess had to be decoded by hand
    because `text=True` used cp1252 on Windows runners and died on the vault's
    curly-quoted filenames. In a CI checkout the two listings are equivalent,
    and on a developer machine walking the tree is the more honest answer for a
    portability sweep: an untracked script with a hardcoded home path is still
    a script with a hardcoded home path.
    """
    targets = []
    for dirpath, dirnames, filenames in os.walk(repo_root):
        rel_dir = Path(dirpath).relative_to(repo_root).as_posix()
        prefix = "" if rel_dir == "." else rel_dir + "/"
        # Prune excluded trees in place so os.walk never descends into them.
        dirnames[:] = [
            d for d in dirnames
            if not f"{prefix}{d}/".startswith(EXCLUDED_PREFIXES)
        ]
        for name in filenames:
            rel = f"{prefix}{name}"
            if rel in SELF_REFERENTIAL:
                continue
            if Path(name).suffix.lower() in SCAN_SUFFIXES:
                targets.append(rel)
    return sorted(targets)


def findings_for(repo_root: Path, rel_path: str) -> list[str]:
    """Portability labels triggered by one file."""
    path = repo_root / rel_path
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return [
        label for label, pattern in PORTABILITY_PATTERNS.items()
        if pattern.search(text)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="MESHNETWEB portability check")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when issues are found in the gated scope",
    )
    args = parser.parse_args()

    # A Windows runner's console defaults to cp1252. Any finding whose path
    # contains a character outside that set would kill the report on print,
    # after the scan had already succeeded.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    repo_root = Path(__file__).resolve().parents[2]
    gated: list[str] = []
    swept: list[str] = []

    # Startup surfaces, resolved by name, are always gated.
    surface_paths: list[str] = []
    for name in SURFACE_NAMES:
        rel = resolve_rel(name, repo_root)
        if rel is None:
            gated.append(
                f"[missing] startup surface {name} not found at any of: "
                + ", ".join(candidates(name))
            )
        else:
            surface_paths.append(rel)

    for rel_path in sorted(set(surface_paths) | set(scan_targets(repo_root))):
        is_gated = rel_path in surface_paths or rel_path.startswith(GATED_PREFIXES)
        for label in findings_for(repo_root, rel_path):
            (gated if is_gated else swept).append(f"[{label}] {rel_path}")

    if gated:
        print("MESHNETWEB portability findings (gated scope):")
        for item in gated:
            print(f" - {item}")
    else:
        print("MESHNETWEB portability check passed (gated scope clean).")

    if swept:
        print(f"\nReport-only findings outside the gated scope ({len(swept)}):")
        for item in swept:
            print(f" - {item}")
        print(
            "\nThese are not fatal. They are mostly root-level scripts carrying a "
            "single developer's absolute paths; cleaning them up is a separate "
            "matter from this gate."
        )

    if gated and args.strict:
        print("\nStrict mode enabled: failing check on gated-scope findings.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
