#!/usr/bin/env python3
"""
expand_date_aliases.py — one-off: add full date alias set to all daily notes.

Replaces the aliases: block in each YYYY-MM-DD.md with the canonical 5-format
set. Touches only the aliases field; all other frontmatter and body preserved.

Usage:
    python3 .github/scripts/expand_date_aliases.py [--dry-run]
"""

import argparse
import re
from datetime import date
from pathlib import Path
import sys

# Keep in sync with daily_rollover.py: date_aliases()
sys.path.insert(0, str(Path(__file__).parent))
from daily_rollover import date_aliases

VAULT_ROOT = Path(__file__).resolve().parents[2]
DAILY_NOTE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})\.md$')

# Matches the full aliases: block inside frontmatter (between --- delimiters)
# Handles any number of existing alias lines.
ALIASES_BLOCK_RE = re.compile(
    r'^aliases:\n(?:  - .+\n)+',
    re.MULTILINE,
)


def expanded_aliases_block(d: date) -> str:
    lines = "".join(f"  - {a}\n" for a in date_aliases(d))
    return f"aliases:\n{lines}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    updated = 0
    skipped = 0

    for f in sorted(VAULT_ROOT.glob("*.md")):
        m = DAILY_NOTE_RE.match(f.name)
        if not m:
            continue
        d = date.fromisoformat(m.group(1))
        content = f.read_text()

        # Only touch files that have a frontmatter aliases block
        if not ALIASES_BLOCK_RE.search(content):
            print(f"  skip (no aliases block): {f.name}")
            skipped += 1
            continue

        new_content = ALIASES_BLOCK_RE.sub(expanded_aliases_block(d), content, count=1)

        if new_content == content:
            skipped += 1
            continue

        if args.dry_run:
            print(f"\n{'─'*50}")
            print(f"  {f.name}")
            # Show just the aliases diff
            old_block = ALIASES_BLOCK_RE.search(content).group()
            new_block = expanded_aliases_block(d)
            print(f"  BEFORE:\n{''.join('    ' + l for l in old_block.splitlines(keepends=True))}")
            print(f"  AFTER:\n{''.join('    ' + l for l in new_block.splitlines(keepends=True))}")
        else:
            f.write_text(new_content)
            print(f"  ✓ {f.name}")
        updated += 1

    print(f"\n{'Dry run — ' if args.dry_run else ''}updated: {updated}, skipped: {skipped}")


if __name__ == "__main__":
    main()
