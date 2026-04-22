#!/usr/bin/env python3
"""
CHAINFIRE — Scorched-earth wipe of Obsidian-specific syntax.

Burns:
  - tags: frontmatter (all files)
  - aliases: frontmatter (all files)
  - [[ ]] wikilinks in body text (EXCEPT files under !/ exclusion zone)

Preserves:
  - All content text
  - All empty stubs (0-byte files skipped)
  - All other frontmatter fields
  - Wikilinks in !/ directory (anchor points for Crawler Crew)

Post-burn lifecycle:
  CHAINFIRE (burn) → Crawler-Linker Crew (regrowth) → Linter (groundskeeper)
  Crawler-Linker rebuilds tags/frontmatter; Linter formats what Crawler creates.

Usage:
  python chainfire.py                 # Dry run (default)
  python chainfire.py --execute       # Execute the burn
  python chainfire.py --report-only   # Stats only, no file details

LINUX }!{ — targets Linux-native execution (WSL, Git Bash, CI runners).
"""

import argparse
import os
import re
import sys
from pathlib import Path


def find_vault_root():
    """Walk up from script location to find vault root (has CLAUDE.md or .git)."""
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir
    for _ in range(10):
        if (candidate / ".git").exists():
            return candidate
        candidate = candidate.parent
    # Fallback: two levels up from .github/scripts/
    return script_dir.parent.parent


def parse_frontmatter(content):
    """Split content into (frontmatter_str, body_str, has_frontmatter).

    Frontmatter is between the first two '---' lines.
    Returns raw strings — caller handles modification.
    """
    if not content.startswith("---"):
        return "", content, False

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        # No closing --- found
        return "", content, False

    end_pos = 3 + end_match.end()
    frontmatter = content[:end_pos]
    body = content[end_pos:]
    return frontmatter, body, True


def remove_yaml_key(frontmatter, key):
    """Remove a YAML key and its value from frontmatter string.

    Handles:
      - key: [inline, list]
      - key: "inline value"
      - key:
          - list
          - items
    Returns (new_frontmatter, removed_value_or_None).
    """
    lines = frontmatter.split("\n")
    new_lines = []
    removed_lines = []
    skip_block = False
    found = False

    for line in lines:
        # Check if this line starts the target key
        key_match = re.match(rf"^{re.escape(key)}\s*:", line)
        if key_match:
            found = True
            skip_block = True
            removed_lines.append(line)
            continue

        if skip_block:
            # Continue skipping indented continuation lines (list items)
            if line.startswith("  ") or line.startswith("\t"):
                removed_lines.append(line)
                continue
            else:
                # Non-indented line — stop skipping
                skip_block = False

        new_lines.append(line)

    if not found:
        return frontmatter, None

    result = "\n".join(new_lines)

    # Clean up empty frontmatter (just --- and ---)
    stripped = result.replace("---", "").strip()
    if not stripped:
        result = "---\n---\n"

    return result, "\n".join(removed_lines)


def strip_wikilinks(text):
    """Replace [[target|display]] with display, [[target]] with target.

    Handles nested content carefully — non-greedy matching.
    """
    # First: piped wikilinks [[target|display]] → display
    text = re.sub(r"\[\[([^\[\]|]+)\|([^\[\]]+)\]\]", r"\2", text)
    # Then: simple wikilinks [[target]] → target (including empty [[]])
    text = re.sub(r"\[\[([^\[\]]*)\]\]", r"\1", text)
    return text


def is_in_exclusion_zone(filepath, vault_root):
    """Check if a file is under the !/ directory (exclusion zone for wikilinks)."""
    try:
        rel = filepath.relative_to(vault_root)
        parts = rel.parts
        # Check if any parent directory starts with !
        # The ! directory is a top-level dir named exactly "!"
        if parts and parts[0] == "!":
            return True
        # Also check for paths starting with "!" in various forms
        for part in parts[:-1]:  # exclude filename itself
            if part.startswith("!"):
                return True
    except ValueError:
        pass
    return False


def is_excluded_directory(filepath, vault_root):
    """Check if file is in a directory we should skip entirely."""
    try:
        rel = filepath.relative_to(vault_root)
        parts = rel.parts
        skip_dirs = {".git", ".github", ".claude", ".gemini", ".codex",
                     ".perplexity", ".obsidian", ".op", ".venv", ".crewai",
                     "node_modules", ".remember"}
        for part in parts:
            if part in skip_dirs:
                return True
    except ValueError:
        pass
    return False


def process_file(filepath, vault_root, execute=False):
    """Process a single .md file. Returns dict of changes or None if no changes."""
    # Skip 0-byte files
    if filepath.stat().st_size == 0:
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError) as e:
        return {"error": str(e)}

    original = content
    changes = {
        "path": str(filepath.relative_to(vault_root)),
        "tags_removed": None,
        "aliases_removed": None,
        "wikilinks_stripped": 0,
    }

    frontmatter, body, has_fm = parse_frontmatter(content)

    # --- Burn tags and aliases from frontmatter (ALL files) ---
    if has_fm:
        frontmatter, tags_val = remove_yaml_key(frontmatter, "tags")
        if tags_val:
            changes["tags_removed"] = tags_val.strip()

        frontmatter, aliases_val = remove_yaml_key(frontmatter, "aliases")
        if aliases_val:
            changes["aliases_removed"] = aliases_val.strip()

    # --- Strip wikilinks inside frontmatter values (e.g., authority: "[[LOGAN]]") ---
    # Only for files OUTSIDE the !/ exclusion zone
    in_exclusion = is_in_exclusion_zone(filepath, vault_root)
    if has_fm and not in_exclusion:
        fm_wikilinks = len(re.findall(r"\[\[[^\[\]]*\]\]", frontmatter))
        if fm_wikilinks > 0:
            frontmatter = strip_wikilinks(frontmatter)
            changes["wikilinks_stripped"] = changes.get("wikilinks_stripped", 0) + fm_wikilinks

    # --- Strip wikilinks from body (EXCEPT !/ exclusion zone) ---
    if not in_exclusion:
        wikilink_count = len(re.findall(r"\[\[[^\[\]]*\]\]", body))
        if wikilink_count > 0:
            body = strip_wikilinks(body)
            changes["wikilinks_stripped"] = wikilink_count

    # Reassemble
    new_content = frontmatter + body if has_fm else body

    # Check if anything changed
    if new_content == original:
        return None

    changes["changed"] = True

    if execute:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return changes


def safe_print(text):
    """Print with fallback for non-ASCII chars on Windows consoles."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def main():
    parser = argparse.ArgumentParser(
        description="CHAINFIRE — Scorched-earth wipe of Obsidian-specific syntax"
    )
    parser.add_argument(
        "--execute", action="store_true",
        help="Actually modify files (default is dry run)"
    )
    parser.add_argument(
        "--report-only", action="store_true",
        help="Print summary stats only, no per-file details"
    )
    args = parser.parse_args()

    vault_root = find_vault_root()
    print(f"CHAINFIRE — {'EXECUTING' if args.execute else 'DRY RUN'}")
    print(f"Vault root: {vault_root}")
    print(f"Exclusion zone: {vault_root / '!'} (wikilinks preserved)")
    print("=" * 60)

    # Gather all .md files
    md_files = sorted(vault_root.rglob("*.md"))
    total_files = len(md_files)
    skipped_empty = 0
    skipped_excluded = 0
    files_changed = 0
    total_tags_removed = 0
    total_aliases_removed = 0
    total_wikilinks_stripped = 0
    errors = []
    change_log = []

    for filepath in md_files:
        # Skip excluded directories
        if is_excluded_directory(filepath, vault_root):
            skipped_excluded += 1
            continue

        # Skip empty files
        if filepath.stat().st_size == 0:
            skipped_empty += 1
            continue

        result = process_file(filepath, vault_root, execute=args.execute)

        if result is None:
            continue

        if "error" in result:
            errors.append(result)
            continue

        files_changed += 1
        change_log.append(result)

        if result.get("tags_removed"):
            total_tags_removed += 1
        if result.get("aliases_removed"):
            total_aliases_removed += 1
        total_wikilinks_stripped += result.get("wikilinks_stripped", 0)

        if not args.repo***REMOVED***only:
            rel_path = result["path"]
            parts = []
            if result.get("tags_removed"):
                parts.append("tags")
            if result.get("aliases_removed"):
                parts.append("aliases")
            wl = result.get("wikilinks_stripped", 0)
            if wl > 0:
                parts.append(f"{wl} wikilinks")
            safe_print(f"  {'BURN' if args.execute else 'WOULD BURN'}: {rel_path} [{', '.join(parts)}]")

    # Summary
    print()
    print("=" * 60)
    print(f"CHAINFIRE {'COMPLETE' if args.execute else 'DRY RUN REPORT'}")
    print(f"  Total .md files scanned:    {total_files}")
    print(f"  Skipped (empty/0-byte):     {skipped_empty}")
    print(f"  Skipped (excluded dirs):    {skipped_excluded}")
    print(f"  Files {'modified' if args.execute else 'to modify'}:         {files_changed}")
    print(f"  Tags blocks removed:        {total_tags_removed}")
    print(f"  Aliases blocks removed:     {total_aliases_removed}")
    print(f"  Wikilinks stripped:         {total_wikilinks_stripped}")
    if errors:
        print(f"  Errors:                     {len(errors)}")
        for e in errors:
            print(f"    {e}")
    print("=" * 60)

    if not args.execute:
        print("\nThis was a DRY RUN. No files were modified.")
        print("Run with --execute to burn for real.")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
