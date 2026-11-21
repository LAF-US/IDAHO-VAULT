"""Tests for scripts_scripts/validate_content.py (#252)."""

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).parents[1] / "scripts_scripts" / "validate_content.py"
_spec = importlib.util.spec_from_file_location("validate_content", _SCRIPT)
validate_content = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_content)

parse = validate_content.parse_frontmatter
P = Path("note.md")


def test_dashes_inside_value_are_not_a_fence():
    """A `---` inside a quoted value must not end the frontmatter."""
    content = '---\nsource: "https://x.example/capabilities---securebio"\n---\nbody\n'
    fm, errors = parse(P, content)
    assert errors == []
    assert fm == {"source": "https://x.example/capabilities---securebio"}


def test_plain_frontmatter_parses():
    """Ordinary frontmatter parses to its mapping."""
    fm, errors = parse(P, "---\ntitle: A\n---\nbody\n")
    assert errors == []
    assert fm == {"title": "A"}


def test_crlf_frontmatter_parses():
    """CRLF line endings are accepted on both fences."""
    fm, errors = parse(P, "---\r\ntitle: A\r\n---\r\nbody\r\n")
    assert errors == []
    assert fm == {"title": "A"}


def test_empty_frontmatter_is_empty_mapping():
    """An empty fence pair yields an empty mapping."""
    fm, errors = parse(P, "---\n---\nbody\n")
    assert errors == []
    assert fm == {}


def test_unclosed_frontmatter_is_an_error():
    """An unclosed frontmatter block produces an error."""
    fm, errors = parse(P, "---\ntitle: A\nbody\n")
    assert fm is None
    assert any("missing closing ---" in e for e in errors)


def test_no_frontmatter_is_skipped():
    """Files without frontmatter are not parsed."""
    assert parse(P, "just text\n") == (None, [])


def _dangerous(text):
    return any(p.search(text) for p in validate_content.DANGEROUS_PATTERNS)


def test_event_handler_attributes_are_still_dangerous():
    """Real inline handlers keep failing validation."""
    for text in ('<img src=x onerror=alert(1)>', '<a onclick="x()">', "<p\nonload=x>"):
        assert _dangerous(text), text


def test_words_ending_in_on_equals_are_not_handlers():
    """`content=`, `month=` and similar mid-word matches are not handlers."""
    for text in ("https://x.example/?content=1", "month=10", "<video controls=true>"):
        assert not _dangerous(text), text
