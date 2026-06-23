#!/usr/bin/env python3
"""
Idempotent Zettel component link chainer.
Usage: python chain_zettels.py
"""

import re
from pathlib import Path

FILE_PATTERN = re.compile(r'^[0-9A-Za-z]+\.md$')


def get_links(filename: str) -> str:
    base = filename.replace('.md', '')
    return ''.join(f'[[{c}]]' for c in base) if len(base) >= 2 else ''


def has_links(content: str, links: str) -> bool:
    return links in content


def insert_links(content: str, links: str) -> str:
    frontmatter_match = re.search(r'^---\n.*?\n---', content, re.DOTALL)
    if frontmatter_match:
        end = frontmatter_match.end()
        after_fm = content[end:]
        return content[:end] + '\n\n' + links + '\n\n' + after_fm.lstrip()
    return links + '\n\n' + content


def process_file(path: Path) -> bool:
    if not FILE_PATTERN.match(path.name):
        return False
    links = get_links(path.name)
    if not links:
        return False
    try:
        content = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        print(f'Skipping {path} (read error)')
        return False
    if has_links(content, links):
        return False
    try:
        path.write_text(insert_links(content, links), encoding='utf-8')
        print(f'Updated: {path}')
        return True
    except OSError as e:
        print(f'Error writing {path}: {e}')
        return False


if __name__ == '__main__':
    processed = sum(1 for f in Path('.').rglob('*.md') if process_file(f))
    print(f'\nDone. Updated: {processed} files')
