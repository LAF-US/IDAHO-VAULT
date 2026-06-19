#!/usr/bin/env python3
"""
Chain Zettel notes together by adding component links.

For any file matching /^[A-Za-z0-9]+\.md$/ with length >= 2,
adds wikilinks to each character: ABC.md -> [[A]][[B]][[C]]

Usage: python chain_zettels.py
"""

import os
import re
from pathlib import Path

# Pattern: files with only letters/numbers, .md extension, length >= 2
FILE_PATTERN = re.compile(r'^[A-Za-z0-9]+\.md$')

def get_component_links(filename):
    """Generate component wikilinks for a filename."""
    base = filename.replace('.md', '')
    if len(base) < 2:
        return None
    return ''.join(f'[[{c}]]' for c in base)

def has_frontmatter(content):
    """Check if content has Obsidian frontmatter."""
    return content.startswith('---') and '---' in content[3:]

def add_links_to_content(content, links):
    """Add component links to content, preserving existing content."""
    if not links:
        return content
    
    if links in content:
        return content  # Already has links
    
    if has_frontmatter(content):
        # Find end of frontmatter (second ---)
        first_dash = content.find('---')
        second_dash = content.find('---', first_dash + 3)
        if first_dash >= 0 and second_dash >= 0:
            end = second_dash + 3
            return content[:end] + '

' + links + ('

' + content[end:] if content[end:] else '')
    
    # Add at beginning
    return links + ('

' + content if content else '')

def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = filepath.name
    links = get_component_links(filename)
    
    if not links:
        return False  # Skip single-character files
    
    new_content = add_links_to_content(content, links)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def main():
    """Process all matching markdown files in current directory and subdirectories."""
    repo_root = Path('.')
    processed = 0
    skipped = 0
    
    for md_file in repo_root.rglob('*.md'):
        if FILE_PATTERN.match(md_file.name):
            if process_file(md_file):
                processed += 1
                print(f'Updated: {md_file}')
            else:
                skipped += 1
    
    print(f'\nDone. Processed: {processed}, Skipped: {skipped}')

if __name__ == '__main__':
    main()
