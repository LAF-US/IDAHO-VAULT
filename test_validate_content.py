"""Tests for scripts_scripts/validate_content.py::parse_frontmatter (#252)."""

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).parent / "scripts_scripts" / "validate_content.py"
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
    """Adjacent fences yield an empty mapping."""
    fm, errors = parse(P, "---\n---\nbody\n")
    assert errors == []
    assert fm == {}


def test_unclosed_frontmatter_is_an_error():
    """A missing closing fence is reported."""
    fm, errors = parse(P, "---\ntitle: A\nbody\n")
    assert fm is None
    assert any("missing closing ---" in e for e in errors)


def test_no_frontmatter_is_skipped():
    """Content without frontmatter is skipped silently."""
    assert parse(P, "just text\n") == (None, [])
