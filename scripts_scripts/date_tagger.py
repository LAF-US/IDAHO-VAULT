#!/usr/bin/env python3
"""
date_tagger.py - tag article/source notes with their publish date (YYYY/MM/DD).

Source of truth: the YYYY-MM-DD prefix in the filename.
  - This is the publish/record date, NOT date created or date modified.
  - Filename date is treated as authoritative. Notes where a frontmatter
    `date:` field conflicts with the filename date are flagged for review
    and never auto-tagged.

Handles three frontmatter states:
  1. Block tags (tags:\n  - item) - appends date tag to the list
  2. No tags field               - inserts tags: block before closing ---
  3. No frontmatter              - prepends minimal frontmatter

Skips:
  - Exact daily notes (YYYY-MM-DD.md)
  - Files already carrying the YYYY/MM/DD tag in frontmatter
  - Files whose frontmatter date: conflicts with filename date (REVIEW)

Usage:
    python3 .github/scripts/date_tagger.py [--dry-run] [--show-skipped]
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]

DAILY_NOTE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
DATE_PREFIX_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})[^T]')
FM_DATE_RE = re.compile(r'^date(?:\s+published)?:\s*(\d{4}-\d{2}-\d{2})', re.MULTILINE)
BLOCK_TAGS_RE = re.compile(r'^(tags:\s*\n(?:  - .+\n)+)', re.MULTILINE)
INLINE_TAGS_RE = re.compile(r'^(tags:\s*\[.+\])', re.MULTILINE)
FM_CLOSE_RE = re.compile(r'\n---\n')


def log(message: str = "") -> None:
    """Write stdout safely on terminals that cannot encode all Unicode glyphs."""
    text = f"{message}\n"
    encoding = sys.stdout.encoding or "utf-8"
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(text.encode(encoding, errors="backslashreplace"))
        sys.stdout.buffer.flush()
    else:
        sys.stdout.write(text)


def has_fm(content: str) -> bool:
    return content.startswith('---')


def get_frontmatter(content: str) -> str:
    if not has_fm(content):
        return ""
    match = FM_CLOSE_RE.search(content, 3)
    if not match:
        return ""
    # Keep the newline before the closing fence so trailing block-style tags
    # still match when tags are the last frontmatter field.
    return content[:match.start() + 1]


def has_frontmatter_tag(content: str, tag: str) -> bool:
    frontmatter = get_frontmatter(content)
    if not frontmatter:
        return False

    block = BLOCK_TAGS_RE.search(frontmatter)
    if block and re.search(rf'(?m)^  - {re.escape(tag)}$', block.group(1)):
        return True

    inline = INLINE_TAGS_RE.search(frontmatter)
    if not inline:
        return False

    raw_items = inline.group(1).split('[', 1)[1].rsplit(']', 1)[0]
    items = [item.strip().strip("'\"") for item in raw_items.split(',') if item.strip()]
    return tag in items


def inject_into_block_tags(content: str, tag: str) -> str:
    """Append tag to an existing multi-line tags block."""

    def replacer(match):
        block = match.group(1).rstrip('\n')
        return block + f'\n  - {tag}\n'

    return BLOCK_TAGS_RE.sub(replacer, content, count=1)


def inject_tags_field(content: str, tag: str) -> str:
    """Add a tags: block just before the closing --- of frontmatter."""
    match = FM_CLOSE_RE.search(content, 3)
    if not match:
        return content
    insert_pos = match.start()
    return content[:insert_pos] + f'\ntags:\n  - {tag}' + content[insert_pos:]


def prepend_frontmatter(content: str, tag: str) -> str:
    """Add minimal frontmatter to a file with none."""
    return f'---\ntags:\n  - {tag}\n---\n\n' + content.lstrip()


def tag_file(path: Path, tag: str) -> str:
    content = path.read_text(encoding="utf-8", errors="replace")

    if not has_fm(content):
        return prepend_frontmatter(content, tag)

    if BLOCK_TAGS_RE.search(content):
        return inject_into_block_tags(content, tag)

    if INLINE_TAGS_RE.search(content):
        def to_block(match):
            items = re.findall(r'[\w/]+', match.group(1).split('[', 1)[1].split(']')[0])
            lines = ''.join(f'  - {item}\n' for item in items)
            return f'tags:\n{lines}'

        content = INLINE_TAGS_RE.sub(to_block, content, count=1)
        return inject_into_block_tags(content, tag)

    return inject_tags_field(content, tag)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tag article notes with YYYY/MM/DD publish date")
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--show-skipped', action='store_true')
    args = parser.parse_args()

    tagged, skipped, review = [], [], []

    for path in sorted(VAULT_ROOT.glob('*.md')):
        if DAILY_NOTE_RE.match(path.name):
            if args.show_skipped:
                log(f"  skip (daily note): {path.name}")
            continue

        match = DATE_PREFIX_RE.match(path.name)
        if not match:
            if args.show_skipped:
                log(f"  skip (no date prefix): {path.name}")
            continue

        file_date = match.group(1)

        try:
            date.fromisoformat(file_date)
        except ValueError:
            review.append((path.name, file_date, 'INVALID DATE'))
            continue

        tag = file_date.replace('-', '/')
        content = path.read_text(encoding="utf-8", errors="replace")

        if has_frontmatter_tag(content, tag):
            skipped.append(path.name)
            if args.show_skipped:
                log(f"  skip (already tagged): {path.name}")
            continue

        fm_date = FM_DATE_RE.search(content)
        if fm_date and fm_date.group(1) != file_date:
            review.append((path.name, file_date, fm_date.group(1)))
            continue

        new_content = tag_file(path, tag)

        if args.dry_run:
            log(f"\n  {path.name}")
            log(f"  + {tag}")
        else:
            path.write_text(new_content, encoding="utf-8")

        tagged.append(path.name)

    prefix = "Dry run - " if args.dry_run else ""
    log(f"\n{prefix}tagged: {len(tagged)}, already done: {len(skipped)}, review: {len(review)}")

    if review:
        invalid = [(name, fd, reason) for name, fd, reason in review if reason == 'INVALID DATE']
        conflicts = [(name, fd, reason) for name, fd, reason in review if reason != 'INVALID DATE']

        if invalid:
            log("\nREVIEW - invalid date in filename (not auto-tagged):")
            for name, fd, _ in invalid:
                log(f"  filename={fd} -> {name}")

        if conflicts:
            log("\nREVIEW - filename date vs frontmatter date conflict (not auto-tagged):")
            for name, fd, fmd in conflicts:
                log(f"  filename={fd}  frontmatter={fmd}  -> {name}")


if __name__ == "__main__":
    main()
