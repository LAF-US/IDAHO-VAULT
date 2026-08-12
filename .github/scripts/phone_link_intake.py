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


def require_existing_dir(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.exists():
        raise RuntimeError(f"{label} does not exist: {resolved}")
    if not resolved.is_dir():
        raise RuntimeError(f"{label} is not a directory: {resolved}")
    return resolved


def get_vault_root(explicit_root: Path | None = None) -> Path:
    """Resolve the vault root from explicit config, env var, then script location."""
    if explicit_root is not None:
        return require_existing_dir(explicit_root, "Vault root")

    env_root = os.environ.get("IDAHO_VAULT_ROOT")
    if env_root:
        return require_existing_dir(Path(env_root), "IDAHO_VAULT_ROOT")

    script_dir = Path(__file__).resolve().parent
    vault_root = require_existing_dir(script_dir.parent.parent, "Fallback vault root")
    if not (vault_root / ".git").exists():
        print(f"Warning: no .git found at {vault_root}, proceeding anyway")
    return vault_root


def file_hash(filepath: Path) -> str:
    """Compute a short SHA-256 hash for deduplication and collision suffixes."""
    h = hashlib.sha256()
    with filepath.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def resolve_destination(filepath: Path, vault_root: Path) -> tuple[Path | None, str]:
    """Resolve a root-level destination path for an incoming file."""
    dest_file = vault_root / filepath.name
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

    source = args.source.resolve()
    if not source.exists():
        print(f"Source folder not found: {source}")
        print("Is Phone Link installed and has files been transferred?")
        return 1

    if not source.is_dir():
        print(f"Source is not a directory: {source}")
        return 1

    try:
        vault_root = get_vault_root(args.vault_root)
    except RuntimeError as exc:
        print(f"Vault root error: {exc}")
        return 1
    files = sorted(f for f in source.iterdir() if f.is_file())

    if not files:
        print("No files found in Phone Link folder.")
        return 0

    print(f"Found {len(files)} file(s) in {source}")
    print(f"Vault root: {vault_root}")
    print(f"Destination: {vault_root}")
    if args.dry_run:
        print("--- DRY RUN ---")
    print()

    moved_paths: list[Path] = []
    skipped_dup: list[str] = []

    for filepath in files:
        dest_file, disposition = resolve_destination(filepath, vault_root)
        if dest_file is None:
            print(f"  SKIP (duplicate): {filepath.name}")
            skipped_dup.append(filepath.name)
            continue

        action = "COPY" if args.copy else "MOVE"
        if args.dry_run:
            print(f"  {action}: {filepath.name} -> {dest_file.name}")
            continue

        if args.copy:
            shutil.copy2(filepath, dest_file)
        else:
            shutil.move(str(filepath), str(dest_file))
        print(f"  {action}D: {filepath.name} -> {dest_file.name}")
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
        except OSError as exc:
            print(f"git add could not run ({exc}); files were moved but not staged")
        else:
            if result.returncode == 0:
                print(f"Staged {len(moved_paths)} ingested file(s) for commit")
            else:
                print(f"git add failed: {result.stderr}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
