"""Benchmarks for the vault-wide tag normalizer.

`normalize_tags.py` walks every Markdown file in the vault, so the per-note
parse/rewrite pipeline runs tens of thousands of times per sweep. These
benchmarks exercise that pipeline in memory, without touching disk.
"""

from __future__ import annotations

import normalize_tags as nt


def test_parse_frontmatter(benchmark, vault_note):
    """Split a note into frontmatter, body, and newline convention."""
    parsed = benchmark(lambda: nt.parse_frontmatter(vault_note))

    assert parsed is not None


def test_parse_tags_block(benchmark, vault_note):
    """Read the canonical `tags:` block out of the frontmatter."""
    frontmatter, _, _, _ = nt.parse_frontmatter(vault_note)

    tags, start, end = benchmark(lambda: nt.parse_tags_block(frontmatter))

    assert tags and start is not None and end is not None


def test_remove_standalone_tag_lines(benchmark, vault_note):
    """Strip inline tag-only lines from the body and promote them."""
    _, body, _, _ = nt.parse_frontmatter(vault_note)

    cleaned, promoted, removed = benchmark(lambda: nt.remove_standalone_tag_lines(body))

    assert removed == len(promoted) > 0
    assert len(cleaned) < len(body)


def test_normalize_and_dedupe_tags(benchmark, vault_note):
    """Lowercase, strip wrapping, and dedupe the collected tag set."""
    frontmatter, body, _, _ = nt.parse_frontmatter(vault_note)
    frontmatter_tags, _, _ = nt.parse_tags_block(frontmatter)
    _, inline_tags, _ = nt.remove_standalone_tag_lines(body)
    raw_tags = frontmatter_tags + inline_tags

    deduped = benchmark(lambda: nt.dedupe_preserve_order(nt.normalize_tags(raw_tags)))

    assert len(deduped) < len(raw_tags)


def test_reconstruct_note(benchmark, vault_note):
    """Rebuild the whole note around a rewritten frontmatter tag block."""
    frontmatter, body, newline, closing_after = nt.parse_frontmatter(vault_note)
    frontmatter_tags, _, _ = nt.parse_tags_block(frontmatter)
    cleaned_body, inline_tags, _ = nt.remove_standalone_tag_lines(body)
    tags = nt.dedupe_preserve_order(nt.normalize_tags(frontmatter_tags + inline_tags))

    rebuilt = benchmark(
        lambda: nt.reconstruct_file(frontmatter, cleaned_body, newline, closing_after, tags)
    )

    assert rebuilt.startswith("---")
