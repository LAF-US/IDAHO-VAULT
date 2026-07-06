#!/usr/bin/env python3
"""CI guard against recurrence of the redaction-damage bug (issue #739).

Commit b05b53ae ("Clean history - secrets purged", 2026-04-22) ran a secret
redaction tool that matched the bare two-letter sequence "rt" plus a
following separator (underscore, hyphen, or space) far too broadly, and
stamped a literal marker string over it wherever that sequence appeared --
not just inside actual secrets. The unambiguous signature of that bug is the
marker directly touching a letter or digit on BOTH sides, with no separator
in between -- for example the fragments `sta`, the marker, and `time` glued
together with nothing separating them, where the original text read
"start_time". A marker used elsewhere in the vault as a genuine, deliberate
redaction notice is normally set off by punctuation or whitespace and does
not match this shape, so it is not flagged.

This guard only scans lines ADDED by a diff, never whole-file content, so it
cannot retroactively fail on the ~237 pre-existing occurrences tracked in
issue #739 -- it exists solely to catch a NEW occurrence of the same failure
mode landing in a future change (e.g. running the same broken redaction tool
again, or copy-pasting already-corrupted text forward).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# Runner-controlled, not attacker-controlled (GITHUB_WORKSPACE is set by the
# Actions runner itself) — but validated by shape anyway: an absolute POSIX
# path in a plain charset, with no ".." traversal segment, before it's ever
# turned into a Path. This is a strict allowlist guard on the raw string,
# not a check on values derived from it, so it doesn't multiply into new
# sinks the way validating the resolved Path object would.
_WORKSPACE_SHAPE = re.compile(r"^/[\w.-]+(?:/[\w.-]+)*$")


def _validated_workspace(workspace: str) -> str:
    if not _WORKSPACE_SHAPE.fullmatch(workspace) or "/../" in f"/{workspace}/":
        raise SystemExit(f"GITHUB_WORKSPACE has an unexpected shape: {workspace!r}")
    return workspace


def _repo_root() -> Path:
    # Same GITHUB_WORKSPACE-vs-own-checkout split as check_secret_patterns.py:
    # in CI this script runs from a base-ref checkout while the diff is
    # computed against the primary workspace (PR head / merge-group tree).
    if os.environ.get("GITHUB_ACTIONS") == "true":
        workspace = os.environ.get("GITHUB_WORKSPACE", "")
        root = Path(_validated_workspace(workspace)).resolve() if workspace else None
        if root is None or not root.is_dir():
            raise SystemExit(f"GITHUB_WORKSPACE is not a directory: {workspace!r}")
        return root
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()

# The marker is built from three literal fragments so this file's own source
# never contains the touching-both-sides shape it is designed to detect.
_MARKER = "*" * 3 + "REMOVED" + "*" * 3
DAMAGE_PATTERN = re.compile(
    r"[A-Za-z0-9]" + re.escape(_MARKER) + r"[A-Za-z0-9]"
)

HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    snippet: str


def run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def added_lines_by_file_at(
    repo_root: Path, base: str, head: str
) -> dict[str, list[tuple[int, str]]]:
    """Return {path: [(new_line_number, line_text), ...]} for lines a diff adds."""
    result = run_git(repo_root, ["diff", "--unified=0", "--diff-filter=ACMR", base, head])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git diff failed")

    by_file: dict[str, list[tuple[int, str]]] = {}
    current_path: str | None = None
    next_line_number = 0

    for raw_line in result.stdout.splitlines():
        if raw_line.startswith("+++ "):
            path = raw_line[4:]
            current_path = None if path == "/dev/null" else path[2:] if path.startswith("b/") else path
            continue
        if raw_line.startswith("@@ "):
            match = HUNK_HEADER_RE.match(raw_line)
            if match:
                next_line_number = int(match.group(1))
            continue
        if current_path is None:
            continue
        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            by_file.setdefault(current_path, []).append((next_line_number, raw_line[1:]))
            next_line_number += 1
        elif not raw_line.startswith("-"):
            # Context line (only appears with non-zero unified context; kept
            # for robustness even though --unified=0 shouldn't emit these).
            next_line_number += 1

    return by_file


def findings_for_added_lines(by_file: dict[str, list[tuple[int, str]]]) -> list[Finding]:
    findings: list[Finding] = []
    for path, lines in by_file.items():
        for line_number, text in lines:
            if DAMAGE_PATTERN.search(text):
                findings.append(Finding(path=path, line=line_number, snippet=text.strip()[:120]))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base commit/ref of the diff")
    parser.add_argument("--head", required=True, help="head commit/ref of the diff")
    args = parser.parse_args()

    by_file = added_lines_by_file_at(REPO_ROOT, args.base, args.head)
    findings = findings_for_added_lines(by_file)

    if not findings:
        print("redaction-damage guard: OK")
        return 0

    print("redaction-damage guard: new redaction-damage signature detected.", file=sys.stderr)
    print(
        "A marker is glued directly to a letter/digit on both sides in an added line --",
        file=sys.stderr,
    )
    print("the exact corruption shape from issue #739. See:", file=sys.stderr)
    for finding in sorted(set(findings), key=lambda item: (item.path, item.line)):
        print(f"  {finding.path}:{finding.line}  {finding.snippet}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
