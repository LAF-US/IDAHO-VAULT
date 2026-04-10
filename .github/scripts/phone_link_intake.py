#!/usr/bin/env python3
"""
Phone Link Intake — moves files from the Phone Link download folder
into the vault's standardized !/INBOX staging area.

Usage:
    python .github/scripts/phone_link_intake.py [OPTIONS]

Options:
    --source PATH     Override the Phone Link folder path
    --live-write      Explicitly allow moving files to the vault
    --copy            Copy instead of move (preserve originals)
    --git-add         Stage ingested files with git add
    --include_large   Include files over 50 MB (skipped by default)

Designed for local use on Logan's Windows laptop.
"""

import argparse
import hashlib
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Try to import guardrails from the same directory
try:
    import mcp_guardrails as guard
except ImportError:
    # Fallback if run from root
    sys.path.append(os.path.join(os.getcwd(), ".github", "scripts"))
    import mcp_guardrails as guard

# Default Phone Link path on Logan's machine
DEFAULT_SOURCE = Path(r"C:\Users\loganf\Downloads\Phone Link")

# Vault-relative destination (Infrastructure style)
INBOX_BASE = Path("!") / "INBOX"

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
    script_path = Path(__file__).resolve()
    # Script lives at .github/scripts/phone_link_intake.py
    # Vault root is 3 levels up from the file itself
    return script_path.parents[2]


def classify_file(filepath: Path) -> str:
    """Route a file to the appropriate subfolder based on extension and name."""
    ext = filepath.suffix.lower()
    name_lower = filepath.name.lower()

    # Screenshots heuristic: PNG files with "screenshot" in the name
    if ext == ".png" and "screenshot" in name_lower:
        return "screenshots"

    return EXTENSION_MAP.get(ext, "other")


def normalize_filename(filepath: Path, date_prefix: str) -> str:
    """Normalize filename: date prefix, lowercase, hyphens for spaces (NETWEB)."""
    name = filepath.stem
    ext = filepath.suffix.lower()

    # Clean up the name
    normalized = name.lower().strip()
    normalized = normalized.replace(" ", "-")
    normalized = normalized.replace("_", "-")

    # Remove consecutive hyphens
    while "--" in normalized:
        normalized = normalized.replace("--", "-")

    # Add date prefix if not already date-prefixed (YYYY-MM-DD-)
    if not normalized[:10].replace("-", "").isdigit():
        normalized = f"{date_prefix}-{normalized}"

    return f"{normalized}{ext}"


def file_hash(filepath: Path) -> str:
    """Compute SHA-256 hash fragment for dedup/collisions."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description="Phone Link → Vault Intake (Flattened)")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help="Phone Link folder path")
    parser.add_argument("--live-write", action="store_true",
                        help="Allow file movements (fails closed without this)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Synonym for not passing --live-write (preview only)")
    parser.add_argument("--copy", action="store_true",
                        help="Copy instead of move (preserve originals)")
    parser.add_argument("--git-add", action="store_true",
                        help="Stage ingested files with git add")
    parser.add_argument("--include-large", action="store_true",
                        help="Include files over 50 MB")
    args = parser.parse_args()

    # Resolve live_write status via guardrails
    is_live = guard.resolve_live_write(args.live_write)
    
    source = args.source.resolve()
    if not source.exists():
        print(f"ERROR: Source folder not found: {source}")
        sys.exit(1)

    vault_root = get_vault_root()
    inbox_path = vault_root / INBOX_BASE
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    batch_timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Collect files (flat only)
    files = sorted(f for f in source.iterdir() if f.is_file())

    if not files:
        print(f"INFO: No files found in {source}")
        sys.exit(0)

    print(f"STABILIZING: {len(files)} file(s) from Phone Link")
    print(f"DESTINATION: {inbox_path}")
    if not is_live:
        print("!!! PREVIEW MODE (Run with --live-write to execute) !!!")
    print()

    processed_items = []
    
    for filepath in files:
        size = filepath.stat().st_size
        category = classify_file(filepath)
        dest_dir = inbox_path / category
        new_name = normalize_filename(filepath, date_prefix)
        dest_file = dest_dir / new_name

        # Large file check
        if size > LARGE_FILE_THRESHOLD and not args.include_large:
            print(f"  SKIP (large): {filepath.name}")
            continue

        # Check for duplication (hash-based)
        if dest_file.exists():
            if file_hash(filepath) == file_hash(dest_file):
                print(f"  EXISTS (duplicate): {filepath.name}")
                continue
            # Collision but unique: append hash
            fhash = file_hash(filepath)
            dest_file = dest_dir / f"{dest_file.stem}-{fhash}{dest_file.suffix}"

        # Prepare Action Context for Logging
        context = guard.MCPActionContext(
            action_type="move_phone_link" if not args.copy else "copy_phone_link",
            system_or_resource_id="local_phone_link",
            initiating_agent="Gemini", 
            related_ref=f"Downloads/Phone Link/{filepath.name}",
            payload={"dest": str(dest_file.relative_to(vault_root))},
            live_write=is_live
        )

        try:
            if is_live:
                dest_dir.mkdir(parents=True, exist_ok=True)
                if args.copy:
                    shutil.copy2(filepath, dest_file)
                else:
                    shutil.move(str(filepath), str(dest_file))
                outcome = "success"
                processed_items.append({"source": filepath.name, "dest": str(dest_file.relative_to(inbox_path)), "size": size})
            else:
                outcome = "success" # Dry run is a 'success' in planning
                print(f"  [WOULD {('COPY' if args.copy else 'MOVE')}]: {filepath.name} -> {category}/{dest_file.name}")
            
            # Emit structured action log to stdout
            # (Note: for mass batching, we might want to emit once at end, 
            # but guardrails design usually favors per-action atomic logs)
            # In this refactor, we emit per file for maximal auditability.
            guard.emit_action_log(context, outcome=outcome)
            
        except Exception as e:
            print(f"  ERROR: {filepath.name} failed: {e}")
            guard.emit_action_log(context, outcome="failure")

    # Update the human-readable intake-log.md
    if processed_items and is_live:
        log_path = inbox_path / "intake-log.md"
        log_entry = f"\n## Batch {batch_timestamp}\n\n"
        log_entry += f"Source: `Phone Link`\n"
        log_entry += "| File | Size |\n"
        log_entry += "| --- | --- |\n"
        for item in processed_items:
            log_entry += f"| `{item['dest']}` | {item['size']} B |\n"
            
        if not log_path.exists():
            header = f"---\ntitle: INBOX Intake Log\nstatus: active\nauthority: LOGAN\n---\n# INBOX Intake Log\n\nOperational record of ingested files.\n"
            log_path.write_text(header + log_entry, encoding="utf-8")
        else:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)

    if args.git_add and processed_items and is_live:
        import subprocess
        subprocess.run(["git", "add", "!"], cwd=str(vault_root))
        print("INFO: Staged `!` folder for commit.")

if __name__ == "__main__":
    main()
