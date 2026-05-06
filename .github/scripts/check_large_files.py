#!/usr/bin/env python3
"""Pre-commit/CI guard for large file policy.

GitHub LFS has a hard per-file ceiling. The vault may keep media as source
documents, but files above that ceiling need an external storage reference
instead of a Git object or LFS object.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MB = 1024 * 1024
GB = 1024 * MB

DEFAULT_LFS_REQUIRED_BYTES = 100 * MB
DEFAULT_LFS_MAX_BYTES = 5 * GB


@dataclass(frozen=True)
class Candidate:
    status: str
    path: Path
    size: int


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def parse_porcelain_line(line: str) -> tuple[str, str] | None:
    if not line:
        return None
    status = line[:2]
    path_text = line[3:].strip().strip('"')
    if " -> " in path_text:
        path_text = path_text.split(" -> ", 1)[1]
    return status, path_text


def git_ls_files_candidates() -> list[Candidate]:
    result = run_git(["ls-files", "-z"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files failed")

    candidates: list[Candidate] = []
    for path_text in result.stdout.split("\0"):
        if not path_text:
            continue
        path = REPO_ROOT / path_text
        if path.is_file():
            candidates.append(Candidate(status="tracked", path=path, size=path.stat().st_size))
    return candidates


def stdin_path_candidates() -> list[Candidate]:
    candidates: list[Candidate] = []
    for raw_path in sys.stdin.buffer.read().split(b"\0"):
        if not raw_path:
            continue
        path_text = raw_path.decode("utf-8", errors="replace")
        path = REPO_ROOT / path_text
        if path.is_file():
            candidates.append(Candidate(status="changed", path=path, size=path.stat().st_size))
    return candidates


def changed_candidates(staged_only: bool) -> list[Candidate]:
    args = ["diff", "--cached", "--name-status", "--diff-filter=ACMR"] if staged_only else ["status", "--porcelain=v1"]
    result = run_git(args)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")

    candidates: list[Candidate] = []
    for line in result.stdout.splitlines():
        if staged_only:
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status, path_text = parts[0], parts[-1]
        else:
            parsed = parse_porcelain_line(line)
            if parsed is None:
                continue
            status, path_text = parsed
            if "D" in status:
                continue

        path = REPO_ROOT / path_text
        if not path.is_file():
            continue
        candidates.append(Candidate(status=status, path=path, size=path.stat().st_size))
    return candidates


def lfs_filter_for(path: Path) -> str | None:
    rel = path.relative_to(REPO_ROOT).as_posix()
    result = run_git(["check-attr", "filter", "--", rel])
    if result.returncode != 0:
        return None
    # Format: path: filter: lfs
    line = result.stdout.strip()
    if line.endswith(": filter: lfs"):
        return "lfs"
    return None


def human_size(size: int) -> str:
    if size >= GB:
        return f"{size / GB:.2f} GB"
    return f"{size / MB:.2f} MB"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="check only staged files")
    parser.add_argument("--all-tracked", action="store_true", help="check all tracked files")
    parser.add_argument("--paths-from-stdin", action="store_true", help="check NUL-delimited paths from stdin")
    parser.add_argument(
        "--lfs-required-mb",
        type=int,
        default=int(os.environ.get("VAULT_LFS_REQUIRED_MB", DEFAULT_LFS_REQUIRED_BYTES // MB)),
        help="files above this size must be tracked by LFS",
    )
    parser.add_argument(
        "--lfs-max-gb",
        type=float,
        default=float(os.environ.get("VAULT_LFS_MAX_GB", DEFAULT_LFS_MAX_BYTES / GB)),
        help="files above this size cannot be committed to GitHub LFS",
    )
    args = parser.parse_args()

    lfs_required = int(args.lfs_required_mb * MB)
    lfs_max = int(args.lfs_max_gb * GB)
    mode_count = sum(1 for enabled in (args.staged, args.all_tracked, args.paths_from_stdin) if enabled)
    if mode_count > 1:
        parser.error("--staged, --all-tracked, and --paths-from-stdin are mutually exclusive")

    if args.all_tracked:
        candidates = git_ls_files_candidates()
    elif args.paths_from_stdin:
        candidates = stdin_path_candidates()
    else:
        candidates = changed_candidates(staged_only=args.staged)

    too_large: list[Candidate] = []
    missing_lfs: list[Candidate] = []

    for candidate in candidates:
        if candidate.size > lfs_max:
            too_large.append(candidate)
            continue
        if candidate.size > lfs_required and lfs_filter_for(candidate.path) != "lfs":
            missing_lfs.append(candidate)

    if not too_large and not missing_lfs:
        print("large-file guard: OK")
        return 0

    if too_large:
        print(
            f"large-file guard: files over {args.lfs_max_gb:g} GB cannot be committed to GitHub LFS:",
            file=sys.stderr,
        )
        for item in sorted(too_large, key=lambda c: c.size, reverse=True):
            print(f"  {human_size(item.size)}  {item.path.relative_to(REPO_ROOT).as_posix()}", file=sys.stderr)
        print("Use external storage and commit a vault note/manifest reference instead.", file=sys.stderr)

    if missing_lfs:
        print(
            f"large-file guard: files over {args.lfs_required_mb} MB need LFS attributes:",
            file=sys.stderr,
        )
        for item in sorted(missing_lfs, key=lambda c: c.size, reverse=True):
            print(f"  {human_size(item.size)}  {item.path.relative_to(REPO_ROOT).as_posix()}", file=sys.stderr)
        print("Add the file type to .gitattributes before committing.", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
