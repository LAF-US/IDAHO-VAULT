#!/usr/bin/env python3
"""
Phone Link Intake - moves files from the Phone Link download folder
directly into the vault root.

Usage:
    python .github/scripts/phone_link_intake.py [OPTIONS]

Options:
    --source PATH      Override the Phone Link folder path
    --vault-root PATH  Override the destination vault root
    --dry-run          Show what would happen without moving files
    --copy             Copy instead of move (preserve originals)
    --git-add          Stage ingested files with git add

Designed for local use on Logan's Windows laptop.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


DEFAULT_SOURCE = Path(r"C:\Users\loganf\Downloads\Phone Link")
TRUSTED_SOURCE_ROOT = DEFAULT_SOURCE.parent
TRUSTED_VAULT_ROOT = Path(__file__).resolve().parents[2]


def normalized_path(path: Path) -> str:
    """Normalize a configured path lexically, without accessing the filesystem."""
    return os.path.normcase(os.path.normpath(os.fspath(path)))


def resolve_phone_link_source(path: Path) -> Path:
    """Resolve an existing Phone Link source within the Downloads boundary."""
    trusted_root = os.path.normcase(os.path.realpath(os.fspath(TRUSTED_SOURCE_ROOT)))
    candidate = os.path.normcase(os.path.realpath(os.fspath(path)))
    if not candidate.startswith(trusted_root + os.sep):
        raise RuntimeError(f"Phone Link source must be within {trusted_root}")

    resolved = Path(candidate)
    if not resolved.exists():
        raise RuntimeError(f"Phone Link source does not exist: {resolved}")
    if not resolved.is_dir():
        raise RuntimeError(f"Phone Link source is not a directory: {resolved}")
    return resolved


def safe_child_path(parent: Path, relative_path: str) -> Path:
    """Return a normalized child path only when it remains below ``parent``."""
    root = os.path.normcase(os.path.realpath(os.fspath(parent)))
    candidate = os.path.normcase(os.path.realpath(os.path.join(root, relative_path)))
    if not candidate.startswith(root + os.sep):
        raise RuntimeError(f"Path escapes its permitted directory: {relative_path}")
    return Path(candidate)


def get_vault_root(explicit_root: Path | None = None) -> Path:
    """Use the repository containing this script as the only vault destination."""
    trusted = normalized_path(TRUSTED_VAULT_ROOT)
    if explicit_root is not None:
        if normalized_path(explicit_root) != trusted:
            raise RuntimeError(f"Vault root must be the script repository: {trusted}")
    else:
        env_root = os.environ.get("IDAHO_VAULT_ROOT")
        if env_root and normalized_path(Path(env_root)) != trusted:
            raise RuntimeError(f"IDAHO_VAULT_ROOT must be the script repository: {trusted}")

    if not TRUSTED_VAULT_ROOT.is_dir():
        raise RuntimeError(f"Script vault root does not exist: {TRUSTED_VAULT_ROOT}")
    return TRUSTED_VAULT_ROOT


def file_hash(filepath: Path) -> str:
    """Compute a short SHA-256 hash for deduplication and collision suffixes."""
    h = hashlib.sha256()
    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def resolve_destination(filepath: Path, vault_root: Path) -> tuple[Path | None, str]:
    """Resolve a root-level destination path for an incoming file."""
    dest_file = safe_child_path(vault_root, filepath.name)
    if not dest_file.exists():
        return dest_file, "direct"

    if file_hash(filepath) == file_hash(dest_file):
        return None, "duplicate"

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return (
        dest_file.with_name(
            f"{dest_file.stem}-{timestamp}-{file_hash(filepath)}{dest_file.suffix}"
        ),
        "collision",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phone Link -> Vault intake")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Phone Link folder path")
    parser.add_argument("--vault-root", type=Path, help="Destination vault root")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    parser.add_argument("--copy", action="store_true", help="Copy instead of move")
    parser.add_argument("--git-add", action="store_true", help="Stage ingested files with git add")
    args = parser.parse_args(argv)

    try:
        source = resolve_phone_link_source(args.source)
        vault_root = get_vault_root(args.vault_root)
    except RuntimeError:
        print("Configuration error")
        return 1
    files = sorted(f for f in source.iterdir() if f.is_file())

    if not files:
        print("No files found in Phone Link folder.")
        return 0

    print(f"Found {len(files)} file(s)")
    print("Vault destination confirmed")
    if args.dry_run:
        print("--- DRY RUN ---")
    print()

    moved_paths: list[Path] = []
    skipped_dup: list[str] = []

    for filepath in files:
        dest_file, disposition = resolve_destination(filepath, vault_root)
        if dest_file is None:
            print("  SKIP (duplicate)")
            skipped_dup.append(filepath.name)
            continue

        action = "COPY" if args.copy else "MOVE"
        if args.dry_run:
            print(f"  {action}")
            continue

        if args.copy:
            shutil.copy2(filepath, dest_file)
        else:
            shutil.move(str(filepath), str(dest_file))
        print(f"  {action}D")
        moved_paths.append(dest_file)

    print()
    print(f"Processed: {len(moved_paths)} file(s)")
    if skipped_dup:
        print(f"Skipped (duplicate): {len(skipped_dup)}")

    if args.git_add and moved_paths and not args.dry_run:
        try:
            result = subprocess.run(
                ["git", "add", "--", *[str(path) for path in moved_paths]],
                cwd=str(vault_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print("git add timed out after 30s; files were moved but not staged")
        except OSError:
            print("git add could not run; files were moved but not staged")
        else:
            if result.returncode == 0:
                print(f"Staged {len(moved_paths)} ingested file(s) for commit")
            else:
                print("git add failed; files were moved but not staged")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
