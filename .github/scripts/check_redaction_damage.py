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

Carried vs. new (Logan's 2026-07-08 ruling on PR #803: the fragments are the
"known rt_ garble (tracked)"): a mechanical rewrite of a line -- e.g. the
NORMALIZATION encoding sweep re-encoding other bytes on it -- re-presents the
file's own pre-existing damage to the diff as an added line. That is carried
damage, not new damage: when the identical damage fragment (with its ASCII
context) already exists in the BASE version of the SAME file, the match is
suppressed. Damage appearing in a file whose base lacks that fragment --
including propagation from one file to another -- still fails.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
from dataclasses import dataclass
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

# Resolved once at import time so run_git() never invokes a bare "git" by
# partial name (Bandit B607) -- falls back to the literal name only if
# shutil.which can't find it (e.g. an unusual local PATH), same as before.
_GIT_EXECUTABLE = shutil.which("git") or "git"

# The marker is built from three literal fragments so this file's own source
# never contains the touching-both-sides shape it is designed to detect.
_MARKER = "*" * 3 + "REMOVED" + "*" * 3
DAMAGE_PATTERN = re.compile(
    r"[A-Za-z0-9]" + re.escape(_MARKER) + r"[A-Za-z0-9]"
)

HUNK_HEADER_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

# The CI failure sweep audit reports document this guard's own findings by
# quoting a worked example of the touching-both-sides shape -- e.g. the
# fragments "sho" and "description" glued directly onto the marker with no
# separator, the same way "sta" and "time" glue together elsewhere in this
# file's own docstring. That's a documentation reference to the pattern, not
# a new instance of it. Every such report trips this guard on the commit
# that introduces it (confirmed on the 2026-07-09 report, run 28993994883),
# so this one well-known, narrowly-named path is exempt from scanning.
# Everything else -- including every other file these reports might touch --
# still scans every added line.
_EXEMPT_PATH_RE = re.compile(r"^!/AUDIT-CI-FAILURE-SWEEP-\d{4}-\d{2}-\d{2}\.md$")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    snippet: str


def run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_GIT_EXECUTABLE, *args],
        cwd=repo_root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=30,
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


def _ascii_context(text: str, start: int, end: int, radius: int = 30) -> str:
    """Extend a match to the surrounding printable-ASCII run (bounded).

    The damage marker and its glued fragments are pure ASCII, so this context
    reads identically out of the base file even when the base bytes are in a
    legacy encoding elsewhere on the line (read with errors="replace").
    """
    lo = start
    while lo > 0 and start - lo < radius and 0x20 <= ord(text[lo - 1]) <= 0x7E:
        lo -= 1
    hi = end
    while hi < len(text) and hi - end < radius and 0x20 <= ord(text[hi]) <= 0x7E:
        hi += 1
    return text[lo:hi]


def findings_for_added_lines(
    by_file: dict[str, list[tuple[int, str]]],
    base_loader=None,
) -> list[Finding]:
    """
    Flag damage on added lines; suppress fragments carried from the same file.

    base_loader(path) -> str | None returns the base-version content of the
    file (None if it has no base version). Without a loader, every match
    flags -- the pre-refinement behavior.
    """
    findings: list[Finding] = []
    base_cache: dict[str, str | None] = {}
    for path, lines in by_file.items():
        if _EXEMPT_PATH_RE.match(path):
            continue
        for line_number, text in lines:
            for match in DAMAGE_PATTERN.finditer(text):
                if base_loader is not None:
                    if path not in base_cache:
                        base_cache[path] = base_loader(path)
                    base_text = base_cache[path]
                    context = _ascii_context(text, match.start(), match.end())
                    if base_text is not None and context in base_text:
                        continue  # carried from this file's own base: tracked debt, not new damage
                findings.append(Finding(path=path, line=line_number, snippet=text.strip()[:120]))
                break  # one finding per line is enough
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base commit/ref of the diff")
    parser.add_argument("--head", required=True, help="head commit/ref of the diff")
    args = parser.parse_args()

    def base_loader(path: str) -> str | None:
        result = run_git(REPO_ROOT, ["show", f"{args.base}:{path}"])
        return result.stdout if result.returncode == 0 else None

    by_file = added_lines_by_file_at(REPO_ROOT, args.base, args.head)
    findings = findings_for_added_lines(by_file, base_loader)

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
