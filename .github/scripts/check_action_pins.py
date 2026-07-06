#!/usr/bin/env python3
"""Verify every external GitHub Action reference is pinned to a full commit SHA.

Structural replacement for the workflow-action-pin branch of the deleted
VERSION-TRANSITIONS.md ledger: floating tags (``@v4``, ``@main``) are a
worm-watch supply-chain risk because the upstream owner can repoint them to
malicious content after the fact (see PR #378, which SHA-pinned every action
in this repo). Rather than asking a human to remember to check this on every
workflow edit, this derives and verifies it directly from the tracked files.
"""

from __future__ import annotations

import os
import re
import sys
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
    # In CI this script executes from the trusted base-branch checkout
    # (trusted-main/), while the workflows under test are the PR head's.
    # Scan GITHUB_WORKSPACE (the primary checkout) instead of the script's
    # own tree, or a newly-added unpinned workflow would be invisible.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        workspace = os.environ.get("GITHUB_WORKSPACE", "")
        root = Path(_validated_workspace(workspace)).resolve() if workspace else None
        if root is None or not root.is_dir():
            raise SystemExit(f"GITHUB_WORKSPACE is not a directory: {workspace!r}")
        return root
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
# GitHub's composite-action convention: exactly action.yml or action.yaml at
# the action's root (never a different filename), matched explicitly rather
# than "any *.yml" to avoid both false coverage of unrelated files and any
# ambiguity about whether the standard filenames are actually scanned.
ACTION_GLOBS = (".github/actions/*/action.yml", ".github/actions/*/action.yaml")

USES_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)\s*(?:#.*)?$")
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def scan_targets() -> list[Path]:
    paths: list[Path] = []
    for pattern in (*WORKFLOW_GLOBS, *ACTION_GLOBS):
        paths.extend(sorted(REPO_ROOT.glob(pattern)))
    return paths


def unpinned_refs(path: Path) -> list[tuple[int, str]]:
    findings = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = USES_PATTERN.match(line)
        if not match:
            continue
        ref = match.group(1)
        if ref.startswith("./") or ref.startswith("docker://"):
            continue
        if "@" not in ref:
            findings.append((lineno, ref))
            continue
        _, _, sha = ref.rpartition("@")
        if not FULL_SHA_PATTERN.match(sha):
            findings.append((lineno, ref))
    return findings


def main() -> int:
    targets = scan_targets()
    if not targets:
        print("action-pin guard: no workflow or action files found", file=sys.stderr)
        return 2

    findings: list[str] = []
    for path in targets:
        for lineno, ref in unpinned_refs(path):
            rel = path.relative_to(REPO_ROOT).as_posix()
            findings.append(f"{rel}:{lineno}: {ref}")

    if findings:
        print("action-pin guard: unpinned action reference (require a full 40-char SHA):", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("action-pin guard: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
