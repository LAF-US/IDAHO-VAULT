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
# Recursive: a nested action (.github/actions/vendor/pr-agent/action.yml) is
# just as capable of naming a mutable image as a top-level one, and a one-level
# glob left it unscanned.
ACTION_GLOBS = (".github/actions/**/action.yml", ".github/actions/**/action.yaml")

# Capture the whole value, not `\S+`. A value containing spaces —
# `uses: ${{ matrix.action }}` — failed to match the old pattern at all, and an
# unmatched line was treated as safe. Anything this guard cannot resolve to a
# literal must be reported, not skipped.
USES_PATTERN = re.compile(r"^\s*(?:-\s*)?uses:\s*(.+?)\s*$")
EXPRESSION_PATTERN = re.compile(r"\$\{\{")
FULL_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

# A `uses:` SHA pins the repository, not the container that repository builds.
# A Docker action can name its image directly, and a tag there is mutable —
# which is exactly how `the-pr-agent/pr-agent` slipped a mutable
# `pragent/pr-agent:github_action` past a 40-char pin (see
# .github/actions/pr-agent/action.yml). So `image:` gets checked too, and for a
# digest rather than a SHA: registries address content by sha256, not by commit.
IMAGE_PATTERN = re.compile(r"""^\s*image:\s*(.+?)\s*$""")
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
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines, start=1):
        match = USES_PATTERN.match(line)
        if not match:
            continue
        ref = _scalar(match.group(1))
        if EXPRESSION_PATTERN.search(ref):
            findings.append((lineno, f"{ref} (expression; cannot be resolved to a pinned ref)"))
            continue
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

    for lineno, line in enumerate(lines, start=1):
        match = IMAGE_PATTERN.match(line)
        if not match:
            continue
        image = _scalar(match.group(1))
        if EXPRESSION_PATTERN.search(image):
            findings.append((lineno, f"{image} (expression; cannot be resolved to a digest)"))
            continue
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


def _scalar(raw: str) -> str:
    """The literal value of a `uses:`/`image:` line, minus trailing comment.

    Only a comment introduced by whitespace is stripped, so a `#` inside the
    value survives. Digests and action refs contain no `#`, so this is exact
    for everything the guard evaluates.
    """
    value = re.split(r"\s+#", raw, maxsplit=1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def _logical_lines(text: str) -> list[tuple[int, str]]:
    """Dockerfile instructions with continuations joined.

    `FROM alpine:latest \\` + `AS build` is one instruction to Docker and two
    physical lines to a regex, so matching physical lines skipped the base
    entirely — fail-open on a mutable image. Honours the `# escape=` parser
    directive, which may only appear before any instruction and only sets `\\`
    or a backtick.
    """
    lines = text.splitlines()
    escape = "\\"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("#"):
            break
        directive = re.match(r"#\s*escape\s*=\s*(\S)\s*$", stripped, re.IGNORECASE)
        if directive and directive.group(1) in ("\\", "`"):
            escape = directive.group(1)
            break

    out: list[tuple[int, str]] = []
    buffer = ""
    start = 0
    for lineno, line in enumerate(lines, start=1):
        # A comment carries no instruction, and must not be treated as
        # continued — the `# escape=\`` directive line ends with the escape
        # character itself, which would otherwise swallow the FROM after it.
        if not buffer and line.strip().startswith("#"):
            continue
        if not buffer:
            start = lineno
        body = line
        continued = body.rstrip().endswith(escape)
        if continued:
            body = body.rstrip()[: -len(escape)]
        buffer = f"{buffer} {body.strip()}" if buffer else body.strip()
        if not continued:
            out.append((start, buffer))
            buffer = ""
    if buffer:
        out.append((start, buffer))
    return out


def _resolve_in_repo(base: Path, rel: str) -> Path | None:
    """Resolve `rel` against `base`, refusing anything outside the repository.

    These paths come out of YAML that lives in the repo, so this is not a trust
    boundary in the usual sense. It is still wrong for a guard to be pointable
    at an arbitrary file by an `image:` line — `image: ../../../../etc/passwd`
    satisfies the Dockerfile heuristic — so containment is checked rather than
    assumed.
    """
    try:
        candidate = (base / rel).resolve()
        candidate.relative_to(REPO_ROOT)
    except (ValueError, OSError):
        return None
    return candidate


def local_action_files(path: Path) -> list[Path]:
    """Action metadata reachable through `uses: ./…` from this file.

    `./` refs are skipped as pin targets — a path in this repo has no SHA to
    pin — but the action they point at can still name a mutable image, and it
    may sit outside ACTION_GLOBS entirely. Follow them instead of trusting them.
    Note `uses: ./x` is resolved from the REPOSITORY ROOT, not the caller.
    """
    found: list[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = USES_PATTERN.match(line)
        if not match:
            continue
        # _scalar() first, exactly as unpinned_refs() does. Testing the raw
        # value made `uses: "./x"` and `uses: ./x # note` local to one function
        # and not the other: flagged as local there, not followed here — so an
        # action outside ACTION_GLOBS kept its mutable image unscanned.
        ref = _scalar(match.group(1))
        if not ref.startswith("./"):
            continue
        target = _resolve_in_repo(REPO_ROOT, ref)
        if target is None:
            continue
        for name in ("action.yml", "action.yaml"):
            candidate = target / name
            if candidate.is_file():
                found.append(candidate)
    return found


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
    dockerfile = _resolve_in_repo(action_path.parent, image)
    if dockerfile is None:
        return [(image_lineno, f"{image} (path escapes the repository)")]
    try:
        text = dockerfile.read_text(encoding="utf-8")
    except OSError:
        # Fail closed: an action pointing at a Dockerfile we cannot read is
        # not something to wave through.
        return [(image_lineno, f"{image} (Dockerfile not readable; cannot verify FROM)")]

    findings: list[tuple[int, str]] = []
    stages: set[str] = set()
    for lineno, line in _logical_lines(text):
        match = FROM_PATTERN.match(line)
        if not match:
            continue
        base, stage = match.group(1), match.group(2)
        # Classify the base BEFORE registering this line's own alias. Adding it
        # first lets a stage exempt itself: `FROM alpine AS alpine` would match
        # `base in stages` and skip the digest check on a mutable image. Only
        # aliases from EARLIER FROM lines are real stage references.
        exempt = base.lower() == "scratch" or base.lower() in stages
        if not exempt and not IMAGE_DIGEST_PATTERN.search(base):
            rel = dockerfile.relative_to(REPO_ROOT).as_posix()
            findings.append(
                (image_lineno, f"{image} -> {rel}:{lineno} FROM {base} (needs @sha256:<64 hex>)")
            )
        if stage:
            stages.add(stage.lower())
    return findings


def main() -> int:
    targets = scan_targets()
    if not targets:
        print("action-pin guard: no workflow or action files found", file=sys.stderr)
        return 2

    findings: list[str] = []
    # Worklist rather than a flat pass: a scanned file can point at a local
    # action that ACTION_GLOBS does not reach, and that action can point at
    # another. `seen` keeps a cycle (a -> b -> a) from spinning.
    queue = list(targets)
    seen: set[Path] = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        rel = path.relative_to(REPO_ROOT).as_posix()
        # Check what will actually be read BEFORE reading it. This guard runs
        # trusted code against PR-head content, so a PR can plant
        # .github/actions/x/action.yml as a symlink. Pointed at a character
        # device (/dev/zero) read_text() never returns and the gate hangs
        # instead of failing — a fail-closed check turned into a stall. Pointed
        # outside the repo it reads something that is not vault content.
        # Reject the symlink itself rather than resolve-and-recheck. Checking
        # the RESOLVED path was not enough: a link whose target lands inside
        # the repo — another tracked file, or a device/FIFO under the tree —
        # passes both containment and is_file() and then gets read anyway, and
        # is_file() to read_text() is two syscalls with a window between them.
        # is_symlink() does not follow the link. No action.yml in this
        # repository is a symlink, so rejecting outright costs nothing.
        if path.is_symlink():
            findings.append(f"{rel}: symlink; not read")
            continue
        resolved = _resolve_in_repo(path.parent, path.name)
        if resolved is None:
            findings.append(f"{rel}: resolves outside the repository; not read")
            continue
        if not resolved.is_file():
            findings.append(f"{rel}: not a regular file ({resolved}); not read")
            continue
        queue.extend(local_action_files(path))
        for lineno, ref in unpinned_refs(path):
            findings.append(f"{rel}:{lineno}: {ref}")
    findings.sort()

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
