#!/usr/bin/env python3
"""
Phone Link Intake — moves files from the Phone Link download folder
into the vault's INBOX/phone-link/ staging area.

Usage:
    python .github/scripts/phone_link_intake.py [OPTIONS]

Options:
    --source PATH     Override the Phone Link folder path
    --dry-run         Show what would happen without moving files
    --copy            Copy instead of move (preserve originals)
    --git-add         Stage ingested files with git add
    --include-large   Include files over 50 MB (skipped by default)

Designed for local use on Logan's Windows laptop.
"""

import argparse
import hashlib
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Default Phone Link path on Logan's machine
DEFAULT_SOURCE = Path(r"C:\Users\loganf\Downloads\Phone Link")

# Vault-relative destination
INBOX_BASE = "INBOX/phone-link"

# Size threshold for "large" files (50 MB)
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024

# Extension → subfolder routing
EXTENSION_MAP = {
    # Images
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".heic": "images",
    ".webp": "images",
    ".gif": "images",
    # Audio
    ".m4a": "audio",
    ".ogg": "audio",
    ".mp3": "audio",
    ".wav": "audio",
    ".aac": "audio",
    ".opus": "audio",
    # Video
    ".mp4": "video",
    ".mov": "video",
    ".3gp": "video",
    ".webm": "video",
    ".mkv": "video",
    # Documents
    ".pdf": "docs",
    ".docx": "docs",
    ".doc": "docs",
    ".txt": "docs",
    ".xlsx": "docs",
    ".csv": "docs",
    ".pptx": "docs",
}


def get_vault_root() -> Path:
    """Find the vault root by walking up from this script's location."""
    script_dir = Path(__file__).resolve().parent
    # Script lives at .github/scripts/ — vault root is two levels up
    vault_root = script_dir.parent.parent
    if not (vault_root / ".git").exists():
        print(f"Warning: no .git found at {vault_root}, proceeding anyway")
    return vault_root


def classify_file(filepath: Path) -> str:
    """Route a file to the appropriate subfolder based on extension and name."""
    ext = filepath.suffix.lower()
    name_lower = filepath.name.lower()

    # Screenshots heuristic: PNG files with "screenshot" in the name
    if ext == ".png" and "screenshot" in name_lower:
        return "screenshots"

    return EXTENSION_MAP.get(ext, "other")


def normalize_filename(filepath: Path, timestamp: str) -> str:
    """Normalize filename: date prefix, lowercase, hyphens for spaces."""
    name = filepath.stem
    ext = filepath.suffix.lower()

    # Clean up the name
    normalized = name.lower().strip()
    normalized = normalized.replace(" ", "-")
    normalized = normalized.replace("_", "-")

    # Remove consecutive hyphens
    while "--" in normalized:
        normalized = normalized.replace("--", "-")

    # Add date prefix if not already date-prefixed
    if not normalized[:10].replace("-", "").isdigit():
        normalized = f"{timestamp}-{normalized}"

    return f"{normalized}{ext}"


def file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash of a file for dedup."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description="Phone Link → Vault intake")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help="Phone Link folder path")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without moving files")
    parser.add_argument("--copy", action="store_true",
                        help="Copy instead of move")
    parser.add_argument("--git-add", action="store_true",
                        help="Stage ingested files with git add")
    parser.add_argument("--include-large", action="store_true",
                        help="Include files over 50 MB")
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.exists():
        print(f"Source folder not found: {source}")
        print("Is Phone Link installed and has files been transferred?")
        sys.exit(1)

    if not source.is_dir():
        print(f"Source is not a directory: {source}")
        sys.exit(1)

    vault_root = get_vault_root()
    inbox_path = vault_root / INBOX_BASE
    timestamp = datetime.now().strftime("%Y-%m-%d")
    batch_id = datetime.now().strftime("%Y-%m-%dT%H%M%S")

    # Collect files (non-recursive — Phone Link uses a flat folder)
    files = sorted(f for f in source.iterdir() if f.is_file())

    if not files:
        print("No files found in Phone Link folder.")
        sys.exit(0)

    print(f"Found {len(files)} file(s) in {source}")
    print(f"Vault root: {vault_root}")
    print(f"Destination: {inbox_path}")
    if args.dry_run:
        print("--- DRY RUN ---")
    print()

    moved = []
    skipped_large = []
    skipped_dup = []

    for filepath in files:
        size = filepath.stat().st_size
        category = classify_file(filepath)
        dest_dir = inbox_path / category
        new_name = normalize_filename(filepath, timestamp)
        dest_file = dest_dir / new_name

        # Large file check
        if size > LARGE_FILE_THRESHOLD and not args.include_large:
            size_mb = size / (1024 * 1024)
            print(f"  SKIP (large, {size_mb:.1f} MB): {filepath.name}")
            skipped_large.append(filepath.name)
            continue

        # Dedup: if destination exists with same hash, skip
        if dest_file.exists():
            if file_hash(filepath) == file_hash(dest_file):
                print(f"  SKIP (duplicate): {filepath.name}")
                skipped_dup.append(filepath.name)
                continue
            # Name collision but different content — append hash fragment
            fhash = file_hash(filepath)
            stem = dest_file.stem
            ext = dest_file.suffix
            dest_file = dest_dir / f"{stem}-{fhash}{ext}"

        if args.dry_run:
            action = "COPY" if args.copy else "MOVE"
            print(f"  {action}: {filepath.name} → {category}/{new_name}")
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            if args.copy:
                shutil.copy2(filepath, dest_file)
                print(f"  COPIED: {filepath.name} → {category}/{new_name}")
            else:
                shutil.move(str(filepath), str(dest_file))
                print(f"  MOVED: {filepath.name} → {category}/{new_name}")

        moved.append({
            "source": filepath.name,
            "dest": f"{category}/{new_name}",
            "size": size,
            "category": category,
        })

    # Summary
    print()
    print(f"Processed: {len(moved)} file(s)")
    if skipped_large:
        print(f"Skipped (large): {len(skipped_large)} — use --include-large to override")
    if skipped_dup:
        print(f"Skipped (duplicate): {len(skipped_dup)}")

    # Write intake log
    if moved and not args.dry_run:
        log_path = inbox_path / "intake-log.md"
        log_entry = f"\n## Batch {batch_id}\n\n"
        log_entry += f"Source: `{source}`\n"
        log_entry += f"Files: {len(moved)}\n\n"
        log_entry += "| File | Category | Size |\n"
        log_entry += "| --- | --- | --- |\n"
        for item in moved:
            size_str = f"{item['size'] / 1024:.1f} KB"
            if item["size"] > 1024 * 1024:
                size_str = f"{item['size'] / (1024 * 1024):.1f} MB"
            log_entry += f"| `{item['dest']}` | {item['category']} | {size_str} |\n"

        # Append or create
        if log_path.exists():
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        else:
            inbox_path.mkdir(parents=True, exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("---\ntitle: Phone Link Intake Log\n")
                f.write("updated: " + timestamp + "\n")
                f.write("status: active\n")
                f.write("tags:\n  - infrastructure/intake\n---\n\n")
                f.write("# Phone Link Intake Log\n\n")
                f.write("Batch records of files ingested from Phone Link.\n")
                f.write(log_entry)
        print(f"Intake log updated: {log_path}")

    # Git add if requested
    if args.git_add and moved and not args.dry_run:
        import subprocess
        result = subprocess.run(
            ["git", "add", str(inbox_path)],
            cwd=str(vault_root),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"Staged {INBOX_BASE}/ for commit")
        else:
            print(f"git add failed: {result.stderr}")


if __name__ == "__main__":
    main()
