#!/usr/bin/env python3
"""
tag_stubs.py — Finds 1-line markdown files missing frontmatter and tags them.

Usage:
    python3 .github/scripts/tag_stubs.py [--dry-run] [--tag TAG]
"""

import argparse
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]

def main() -> int:
    parser = argparse.ArgumentParser(description="Tag 1-line stub files missing frontmatter")
    parser.add_argument('--dry-run', action='store_true', help="Print files that would be tagged without modifying them")
    parser.add_argument('--tag', type=str, default='vault/stub', help="The tag to apply to stub files (default: vault/stub)")
    args = parser.parse_args()

    tagged_count = 0
    
    print(f"🔍 Scanning {VAULT_ROOT} for 1-line stubs to tag with '{args.tag}'...")

    for filepath in VAULT_ROOT.rglob("*.md"):
        # Skip system zones and github actions
        if "!\\" in str(filepath) or "!/" in str(filepath) or ".github" in str(filepath):
            continue
            
        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
            
        # Skip if it already has frontmatter
        if content.startswith("---"):
            continue
            
        # Count non-empty lines
        lines = [line for line in content.splitlines() if line.strip()]
        
        if len(lines) == 1:
            if args.dry_run:
                print(f"  [DRY RUN] Would tag: {filepath.relative_to(VAULT_ROOT)}")
            else:
                new_content = f"---\ntags:\n  - {args.tag}\n---\n{content}"
                filepath.write_text(new_content, encoding="utf-8")
                print(f"  ✅ Tagged: {filepath.relative_to(VAULT_ROOT)}")
            
            tagged_count += 1

    mode_str = "Dry run complete." if args.dry_run else "Finished!"
    print(f"\n✨ {mode_str} Tagged {tagged_count} stub files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
