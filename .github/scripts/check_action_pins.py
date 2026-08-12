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
WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")
# GitHub's composite-action convention: exactly action.yml or action.yaml at
# the action's root (never a different filename), matched explicitly rather
# than "any *.yml" to avoid both false coverage of unrelated files and any
# ambiguity about whether the standard filenames are actually scanned.
ACTION_GLOBS = (".github/actions/*/action.yml", ".github/actions/*/action.yaml")

USES_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)\s*(?:#.*)?$")
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

# A `uses:` SHA pins the repository, not the container that repository builds.
# A Docker action can name its image directly, and a tag there is mutable —
# which is exactly how `the-pr-agent/pr-agent` slipped a mutable
# `pragent/pr-agent:github_action` past a 40-char pin (see
# .github/actions/pr-agent/action.yml). So `image:` gets checked too, and for a
# digest rather than a SHA: registries address content by sha256, not by commit.
IMAGE_PATTERN = re.compile(r"""^\s*image:\s*['"]?(\S+?)['"]?\s*(?:#.*)?$""")
IMAGE_DIGEST_PATTERN = re.compile(r"@sha256:[0-9a-f]{64}$")
# `FROM <base> [AS <stage>]`, case-insensitive, --platform= flags tolerated.
FROM_PATTERN = re.compile(
    r"^\s*FROM\s+(?:--\S+\s+)*(\S+)(?:\s+AS\s+(\S+))?\s*$", re.IGNORECASE
)


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
        if ref.startswith("./"):
            continue
        if ref.startswith("docker://"):
            # Skipped as a `uses:` ref, but still a container: hold it to the
            # same digest rule as an `image:` line rather than waving it past.
            if not IMAGE_DIGEST_PATTERN.search(ref):
                findings.append((lineno, f"{ref} (docker ref needs @sha256:<64 hex>)"))
            continue
        if "@" not in ref:
            findings.append((lineno, ref))
            continue
        _, _, sha = ref.rpartition("@")
        if not FULL_SHA_PATTERN.match(sha):
            findings.append((lineno, ref))

    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = IMAGE_PATTERN.match(line)
        if not match:
            continue
        image = match.group(1)
        if _looks_like_dockerfile(image):
            # NOT a free pass. `image: Dockerfile.github_action_dockerhub` is
            # how the original hole worked: a repository SHA freezes the
            # Dockerfile TEXT, and that text says `FROM <mutable tag>`, which
            # resolves at build time to whatever the tag points at today. So
            # follow the file and hold its FROM lines to the digest rule.
            findings.extend(_unpinned_from_lines(path, image, lineno))
            continue
        if not IMAGE_DIGEST_PATTERN.search(image):
            findings.append((lineno, f"{image} (image needs @sha256:<64 hex>)"))
    return findings


def _looks_like_dockerfile(image: str) -> bool:
    """A build context path rather than a registry reference."""
    if image.startswith("docker://"):
        return False
    return "Dockerfile" in image or image.startswith("./") or image.startswith("../")


def _unpinned_from_lines(
    action_path: Path, image: str, image_lineno: int
) -> list[tuple[int, str]]:
    """Every FROM in the referenced Dockerfile must name a digest.

    Exceptions, both legitimate: `scratch` (the empty base, which has no
    digest) and a reference to an earlier build stage declared with `AS`.
    """
    dockerfile = (action_path.parent / image).resolve()
    try:
        text = dockerfile.read_text(encoding="utf-8")
    except OSError:
        # Fail closed: an action pointing at a Dockerfile we cannot read is
        # not something to wave through.
        return [(image_lineno, f"{image} (Dockerfile not readable; cannot verify FROM)")]

    findings: list[tuple[int, str]] = []
    stages: set[str] = set()
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = FROM_PATTERN.match(line)
        if not match:
            continue
        base, stage = match.group(1), match.group(2)
        if stage:
            stages.add(stage.lower())
        if base.lower() == "scratch" or base.lower() in stages:
            continue
        if not IMAGE_DIGEST_PATTERN.search(base):
            rel = dockerfile.relative_to(REPO_ROOT).as_posix()
            findings.append(
                (image_lineno, f"{image} -> {rel}:{lineno} FROM {base} (needs @sha256:<64 hex>)")
            )
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
        print(
            "action-pin guard: unpinned reference "
            "(actions need a full 40-char SHA; images and Dockerfile FROM lines "
            "need @sha256:<64 hex>):",
            file=sys.stderr,
        )
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1

    print("action-pin guard: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
