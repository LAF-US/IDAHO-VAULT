"""Metadata-standard regression tests for the 2026-10-20 CI sweep audit (#1113)."""

import importlib.util
import re
from pathlib import Path

_ROOT = Path(__file__).parents[1]
_DOC = _ROOT / "!" / "AUDIT-CI-FAILURE-SWEEP-2026-10-20.md"
_SCRIPT = _ROOT / "scripts_scripts" / "validate_content.py"

_spec = importlib.util.spec_from_file_location("validate_content", _SCRIPT)
validate_content = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_content)

ALLOWED_STATUS = {"draft", "active", "superseded", "archived"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _frontmatter():
    """Load the audit's frontmatter through the shared vault parser."""
    text = _DOC.read_text(encoding="utf-8")
    fm, errors = validate_content.parse_frontmatter(_DOC, text)
    assert errors == [], errors
    assert fm is not None
    return fm


def _footer_fields(text):
    """Return the DOCUMENT METADATA footer's `**Field:** value` pairs."""
    sections = text.split("## DOCUMENT METADATA", 1)
    assert len(sections) == 2, "missing ## DOCUMENT METADATA footer"
    return dict(re.findall(r"^- \*\*(.+?):\*\*\s*(.+)$", sections[1], re.MULTILINE))


def test_status_is_in_allowed_enum():
    """The audit's `status` must be one of the standard's lifecycle values."""
    assert _frontmatter()["status"] in ALLOWED_STATUS


def test_required_header_fields_present():
    """The audit carries every required frontmatter field from the standard."""
    fm = _frontmatter()
    for field in ("title", "updated", "status", "authority"):
        assert field in fm, f"missing required field: {field}"


def test_dates_are_iso_date_only():
    """`created` and `updated` use the standard's YYYY-MM-DD date format."""
    fm = _frontmatter()
    for field in ("created", "updated"):
        assert DATE_RE.match(str(fm[field])), f"{field} is not YYYY-MM-DD"


def test_authors_is_a_nonempty_list():
    """The audit records its contributor as a populated `authors` list."""
    authors = _frontmatter()["authors"]
    assert isinstance(authors, list) and authors


def test_footer_mirrors_header_lifecycle_fields():
    """The footer repeats the header's dates, status, and authority."""
    fm = _frontmatter()
    footer = _footer_fields(_DOC.read_text(encoding="utf-8"))
    assert footer["Created"] == str(fm["created"])
    assert footer["Last Updated"] == str(fm["updated"])
    assert footer["Status"].lower() == fm["status"]
    assert footer["Authority"] == fm["authority"]
