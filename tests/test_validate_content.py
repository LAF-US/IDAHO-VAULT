from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def _load_validate_content_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "validate_content.py"
    spec = importlib.util.spec_from_file_location("validate_content_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_content = _load_validate_content_module()


class ScopeDirectoryTest(unittest.TestCase):
    """A scope is a lane declaring where its own output goes -- not a claim
    over files it has never opened."""

    def test_inbox_scope_accepts_inbox_markdown(self) -> None:
        errors = validate_content.validate_directory(
            Path("INBOX/SWARM-MVP/process-document-123-1.md"),
            "inbox",
        )
        self.assertEqual(errors, [])

    def test_inbox_scope_rejects_non_inbox_markdown(self) -> None:
        target = Path("!/SWARM-MVP/process-document-123-1.md")
        errors = validate_content.validate_directory(target, "inbox")
        self.assertEqual(
            errors,
            [f"{target}: File outside allowed directories for scope 'inbox': ['INBOX/']"],
        )


class ContentSafetyTest(unittest.TestCase):
    def test_script_tag_is_flagged(self) -> None:
        target = Path("INBOX/capture.md")
        errors = validate_content.validate_content_safety(
            target, "intro\n<script>alert(1)</script>\n"
        )
        self.assertEqual(errors, [f"{target}: Dangerous pattern found: '<script'"])

    def test_ordinary_prose_passes(self) -> None:
        errors = validate_content.validate_content_safety(
            Path("INBOX/capture.md"), "A committee hearing on the budget bill.\n"
        )
        self.assertEqual(errors, [])


class PeriodicSurfaceTest(unittest.TestCase):
    def test_weekly_note_filename_is_periodic(self) -> None:
        self.assertTrue(validate_content.is_periodic_surface(Path("2026-W32.md"), None))

    def test_period_frontmatter_marks_a_periodic_surface(self) -> None:
        # 1000.md is the reason yearly notes are matched on `period:` rather
        # than on a bare four-digit filename.
        self.assertTrue(
            validate_content.is_periodic_surface(Path("1000.md"), {"period": "year"})
        )

    def test_note_template_is_never_periodic(self) -> None:
        self.assertFalse(
            validate_content.is_periodic_surface(Path("WEEKLY NOTE TEMPLATE.md"), None)
        )


class TemplatePlaceholderTest(unittest.TestCase):
    def test_templater_placeholder_is_flagged(self) -> None:
        target = Path("2026-05-01.md")
        errors = validate_content.validate_template_placeholders(
            target, "# Friday\n<% tp.date.now() %>\n"
        )
        self.assertEqual(
            errors, [f"{target}:2: unrendered Templater placeholder (<% ... %>)"]
        )

    def test_brace_placeholder_is_flagged(self) -> None:
        target = Path("TO DO LIST.md")
        errors = validate_content.validate_template_placeholders(target, "{{date}}\n")
        self.assertEqual(
            errors,
            [str(target) + ":1: unrendered template placeholder ({{...}})"],
        )

    def test_fenced_block_is_ignored(self) -> None:
        errors = validate_content.validate_template_placeholders(
            Path("2026-05-01.md"), "```\n<% tp.date.now() %>\n```\n"
        )
        self.assertEqual(errors, [])

    def test_note_template_is_not_scanned(self) -> None:
        errors = validate_content.validate_template_placeholders(
            Path("DAILY NOTE TEMPLATE.md"), "<% tp.date.now() %>\n"
        )
        self.assertEqual(errors, [])


class SponsorNameTest(unittest.TestCase):
    def test_sponsor_with_digits_is_flagged(self) -> None:
        target = Path("GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/H0001.md")
        content = "sponsor:\n  - Rep. Smith\n  - Rep. 0wned\n"
        errors = validate_content.validate_sponsor_names(target, content)
        self.assertEqual(errors, [f"{target}: Suspicious sponsor name: 'Rep. 0wned'"])


if __name__ == "__main__":
    unittest.main()
