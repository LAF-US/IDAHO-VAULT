#!/usr/bin/env python3
"""
date_tagger.py — tag article/source notes with their publish date (YYYY/MM/DD).

Source of truth: the YYYY-MM-DD prefix in the filename.
  - This is the publish/record date, NOT date created or date modified.
  - Filename date is treated as authoritative. Notes where a frontmatter
    `date:` field conflicts with the filename date are flagged for review
    and never auto-tagged.

Handles three frontmatter states:
  1. Block tags (tags:\\n  - item) — appends date tag to the list
  2. No tags field               — inserts tags: block before closing ---
  3. No frontmatter              — prepends minimal frontmatter

Skips:
  - Exact daily notes (YYYY-MM-DD.md)
  - Files already carrying the YYYY/MM/DD tag
  - Files whose frontmatter date: conflicts with filename date (REVIEW)

Usage:
    python3 .github/scripts/date_tagger.py [--dry-run] [--show-skipped]
"""

import argparse
import re
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]

DAILY_NOTE_RE   = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
DATE_PREFIX_RE  = re.compile(r'^(\d{4}-\d{2}-\d{2})[^T]')  # excludes YYYY-MM-DDTHHMM
FM_DATE_RE      = re.compile(r'^date(?:\s+published)?:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)
BLOCK_TAGS_RE   = re.compile(r'^(tags:\s*\n(?:  - .+\n)+)', re.MULTILINE)
INLINE_TAGS_RE  = re.compile(r'^(tags:\s*\[.+\])', re.MULTILINE)
FM_CLOSE_RE     = re.compile(r'\n---\n', )


def has_fm(content: str) -> bool:
    return content.startswith('---')


def inject_into_block_tags(content: str, tag: str) -> str:
    """Append tag to an existing multi-line tags block."""
    def replacer(m):
        block = m.group(1).rstrip('\n')
        return block + f'\n  - {tag}\n'
    return BLOCK_TAGS_RE.sub(replacer, content, count=1)


def inject_tags_field(content: str, tag: str) -> str:
    """Add a tags: block just before the closing --- of frontmatter."""
    # Find the closing --- of frontmatter
    m = FM_CLOSE_RE.search(content, 3)  # skip opening ---
    if not m:
        return content
    insert_pos = m.start()
    return content[:insert_pos] + f'\ntags:\n  - {tag}' + content[insert_pos:]


def prepend_frontmatter(content: str, tag: str) -> str:
    """Add minimal frontmatter to a file with none."""
    return f'---\ntags:\n  - {tag}\n---\n\n' + content.lstrip()


def tag_file(f: Path, file_date: str, tag: str) -> str:
    content = f.read_text(errors='replace')

    if not has_fm(content):
        return prepend_frontmatter(content, tag)

    if BLOCK_TAGS_RE.search(content):
        return inject_into_block_tags(content, tag)

    if INLINE_TAGS_RE.search(content):
        # Convert inline to block and append — rare but handled
        def to_block(m):
            items = re.findall(r'[\w/]+', m.group(1).split('[', 1)[1].split(']')[0])
            lines = ''.join(f'  - {i}\n' for i in items)
            return f'tags:\n{lines}'
        content = INLINE_TAGS_RE.sub(to_block, content, count=1)
        return inject_into_block_tags(content, tag)

    # Frontmatter exists but no tags field
    return inject_tags_field(content, tag)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag article notes with YYYY/MM/DD publish date")
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--show-skipped', action='store_true')
    args = parser.parse_args()

    tagged, skipped, review = [], [], []

    for f in sorted(VAULT_ROOT.glob('*.md')):
        if DAILY_NOTE_RE.match(f.name):
            if args.show_skipped:
                print(f"  skip (daily note): {f.name}")
            continue

        m = DATE_PREFIX_RE.match(f.name)
        if not m:
            if args.show_skipped:
                print(f"  skip (no date prefix): {f.name}")
            continue

        file_date = m.group(1)

        try:
            date.fromisoformat(file_date)
        except ValueError:
            review.append((f.name, file_date, 'INVALID DATE'))
            continue

        tag       = file_date.replace('-', '/')
        content   = f.read_text(errors='replace')

        # Already tagged
        if tag in content:
            skipped.append(f.name)
            if args.show_skipped:
                print(f"  skip (already tagged): {f.name}")
            continue

        # Frontmatter date conflict check
        fm_date = FM_DATE_RE.search(content)
        if fm_date and fm_date.group(1) != file_date:
            review.append((f.name, file_date, fm_date.group(1)))
            continue

        new_content = tag_file(f, file_date, tag)

        if args.dry_run:
            # Show just the frontmatter diff
            old_fm_end = content.find('\n---\n', 3) + 5 if '---' in content[3:10] else 0
            new_fm_end = new_content.find('\n---\n', 3) + 5 if '---' in new_content[3:10] else 0
            print(f"\n  {f.name}")
            print(f"  + {tag}")
        else:
            f.write_text(new_content)

        tagged.append(f.name)

    print(f"\n{'Dry run — ' if args.dry_run else ''}tagged: {len(tagged)}, "
          f"already done: {len(skipped)}, review: {len(review)}")

    if review:
        invalid = [(n, fd, r) for n, fd, r in review if r == 'INVALID DATE']
        conflicts = [(n, fd, r) for n, fd, r in review if r != 'INVALID DATE']
        if invalid:
            print("\n\u26a0 REVIEW \u2014 invalid date in filename (not auto-tagged):")
            for name, fd, _ in invalid:
                print(f"  filename={fd}  \u2192  {name}")
        if conflicts:
            print("\n\u26a0 REVIEW \u2014 filename date vs frontmatter date conflict (not auto-tagged):")
            for name, fd, fmd in conflicts:
                print(f"  filename={fd}  frontmatter={fmd}  \u2192  {name}")


if __name__ == "__main__":
    main()
