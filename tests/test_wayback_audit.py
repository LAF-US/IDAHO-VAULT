from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


def _load_wayback_audit():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "wayback_audit.py"
    spec = importlib.util.spec_from_file_location("wayback_audit_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


wayback_audit = _load_wayback_audit()


class ExtractFrontmatterTest(unittest.TestCase):
    def test_standard_frontmatter(self) -> None:
        content = "---\ntitle: test\nURL: https://example.com/real\n---\nbody\n"
        self.assertEqual(
            wayback_audit.extract_frontmatter(content),
            "title: test\nURL: https://example.com/real",
        )

    def test_no_leading_fence_returns_empty(self) -> None:
        content = "# Just a heading\n\nURL: https://example.com/should-not-count\n"
        self.assertEqual(wayback_audit.extract_frontmatter(content), "")

    def test_unclosed_fence_returns_empty(self) -> None:
        content = "---\ntitle: test\nURL: https://example.com/no-close\nno closing fence here"
        self.assertEqual(wayback_audit.extract_frontmatter(content), "")

    def test_leading_bom_is_tolerated(self) -> None:
        content = "﻿---\ntitle: test\nURL: https://example.com/bom-case\n---\nbody\n"
        self.assertIn("URL: https://example.com/bom-case", wayback_audit.extract_frontmatter(content))

    def test_four_dash_line_is_not_a_closing_fence(self) -> None:
        content = "---\nURL: https://example.com/real\n----\nmore: stuff\n---\nbody\n"
        self.assertEqual(
            wayback_audit.extract_frontmatter(content),
            "URL: https://example.com/real\n----\nmore: stuff",
        )

    def test_dashes_with_trailing_text_are_not_a_closing_fence(self) -> None:
        content = "---\nURL: https://example.com/real\n--- not-a-fence\nmore: stuff\n---\nbody\n"
        self.assertEqual(
            wayback_audit.extract_frontmatter(content),
            "URL: https://example.com/real\n--- not-a-fence\nmore: stuff",
        )

    def test_closing_fence_with_trailing_whitespace_is_recognized(self) -> None:
        content = "---\r\nURL: https://example.com/crlf-case\r\n---  \r\nbody\r\n"
        self.assertIn("URL: https://example.com/crlf-case", wayback_audit.extract_frontmatter(content))


class ExtractUrlTest(unittest.TestCase):
    def test_extracts_url_from_frontmatter(self) -> None:
        content = "---\ntitle: test\nURL: https://example.com/real\n---\nbody\n"
        self.assertEqual(wayback_audit.extract_url(content), "https://example.com/real")

    def test_ignores_url_shaped_line_in_fenced_body_example(self) -> None:
        # The exact VAULT-CONVENTIONS.md-shaped false positive this PR fixes:
        # a doc-convention example URL inside a fenced ```yaml block in the body.
        content = (
            "---\ntitle: conventions\n---\n\n"
            "News articles:\n\n```yaml\nauthor: \"Reporter Name\"\nURL: https://...\n```\n"
        )
        self.assertIsNone(wayback_audit.extract_url(content))

    def test_ignores_url_shaped_line_with_no_frontmatter_at_all(self) -> None:
        content = "# Wayback Patches\n\n```\nURL: https://example.com/proposed-patch\n```\n"
        self.assertIsNone(wayback_audit.extract_url(content))

    def test_no_frontmatter_returns_none(self) -> None:
        content = "just prose with URL: https://example.com/fake in the body\n"
        self.assertIsNone(wayback_audit.extract_url(content))

    def test_null_and_na_values_return_none(self) -> None:
        self.assertIsNone(wayback_audit.extract_url("---\nURL: null\n---\n"))
        self.assertIsNone(wayback_audit.extract_url("---\nURL: N/A\n---\n"))

    def test_archive_org_url_is_ignored(self) -> None:
        content = "---\nURL: https://web.archive.org/web/2020/https://example.com/x\n---\n"
        self.assertIsNone(wayback_audit.extract_url(content))


class ExtractWaybackFieldTest(unittest.TestCase):
    def test_extracts_wayback_field_from_frontmatter(self) -> None:
        content = (
            "---\nURL: https://example.com/x\n"
            "wayback: https://web.archive.org/web/2020/https://example.com/x\n---\n"
        )
        self.assertEqual(
            wayback_audit.extract_wayback_field(content),
            "https://web.archive.org/web/2020/https://example.com/x",
        )

    def test_ignores_wayback_shaped_line_outside_frontmatter(self) -> None:
        content = "---\nURL: https://example.com/x\n---\n\nSee also wayback: https://example.com/not-real\n"
        self.assertIsNone(wayback_audit.extract_wayback_field(content))

    def test_missing_field_returns_none(self) -> None:
        content = "---\nURL: https://example.com/x\n---\n"
        self.assertIsNone(wayback_audit.extract_wayback_field(content))


if __name__ == "__main__":
    unittest.main()
