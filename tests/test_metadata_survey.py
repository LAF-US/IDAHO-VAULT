from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import textwrap
import unittest
from pathlib import Path
from unittest import mock


def _load_module(module_name: str, script_name: str):
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


metadata_survey = _load_module("metadata_survey_test_module", "metadata_survey.py")


class MetadataSurveyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.root = self.project_root / "tests" / "_tmp_metadata_survey_case"
        shutil.rmtree(self.root, ignore_errors=True)
        self.root.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def test_survey_vault_reports_frontmatter_health_and_schema_drift(self) -> None:
        (self.root / "governed-good.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Governed Good
                updated: 2026-04-18
                status: active
                authority: LOGAN
                related:
                  - AGENTS
                doc_class: report
                template_id: tpl-report-v1
                template_version: v1
                ---

                body
                """
            ),
            encoding="utf-8",
        )
        (self.root / "governed-missing.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Governed Missing
                status: draft
                ---

                body
                """
            ),
            encoding="utf-8",
        )
        (self.root / "no-frontmatter.md").write_text("plain body\n", encoding="utf-8")
        (self.root / "broken.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Broken
                status: [oops

                body
                """
            ),
            encoding="utf-8",
        )
        (self.root / "2026-04-18.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: 2026-04-18
                aliases:
                  - 2026-04-18
                yesterday: 2026-04-17
                tomorrow: 2026-04-19
                weekday:
                  - Friday
                date created: Friday, April 18th 2026, 12:00:00 am
                ---

                [[TO DO LIST]]
                """
            ),
            encoding="utf-8",
        )

        private_dir = self.root / "_private"
        private_dir.mkdir()
        (private_dir / "private-note.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Private Note
                updated: 2026-04-18
                status: archived
                authority: LOGAN
                ---

                body
                """
            ),
            encoding="utf-8",
        )

        plugins_dir = self.root / ".obsidian" / "plugins" / "fake-plugin"
        plugins_dir.mkdir(parents=True)
        (plugins_dir / "README.md").write_text("# plugin docs\n", encoding="utf-8")

        summary = metadata_survey.survey_vault(self.root)

        self.assertEqual(summary["scanned_files"], 5)
        self.assertEqual(summary["frontmatter"]["valid"], 3)
        self.assertEqual(summary["frontmatter"]["missing"], 1)
        self.assertEqual(summary["frontmatter"]["malformed"], 1)
        self.assertEqual(summary["daily_notes"]["count"], 1)
        self.assertEqual(summary["daily_notes"]["valid_frontmatter"], 1)
        self.assertEqual(summary["daily_notes"]["missing_expected_fields"]["linter-yaml-title-alias"], 1)
        self.assertEqual(summary["daily_notes"]["legacy_field_usage"]["date created"], 1)
        self.assertEqual(summary["non_daily_notes"]["count"], 4)
        self.assertEqual(summary["non_daily_notes"]["valid_frontmatter"], 2)
        self.assertEqual(summary["non_daily_notes"]["missing_required_fields"]["authority"], 1)
        self.assertEqual(summary["non_daily_notes"]["missing_required_fields"]["updated"], 1)
        self.assertEqual(summary["non_daily_notes"]["with_template_fields"]["doc_class"], 1)
        self.assertEqual(summary["non_daily_notes"]["status_values"]["active"], 1)
        self.assertEqual(summary["examples"]["missing_frontmatter"], ["no-frontmatter.md"])
        self.assertEqual(summary["examples"]["malformed_frontmatter"], ["broken.md"])

        summary_with_private = metadata_survey.survey_vault(self.root, include_private=True)
        self.assertEqual(summary_with_private["scanned_files"], 6)
        self.assertEqual(summary_with_private["non_daily_notes"]["count"], 5)

    def test_main_writes_markdown_report(self) -> None:
        (self.root / "governed.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Governed
                updated: 2026-04-18
                status: active
                authority: LOGAN
                ---

                body
                """
            ),
            encoding="utf-8",
        )

        output = self.root / "survey.md"
        with mock.patch.object(
            sys,
            "argv",
            [
                "metadata_survey.py",
                "--root",
                str(self.root),
                "--format",
                "markdown",
                "--output",
                str(output),
            ],
        ):
            metadata_survey.main()

        rendered = output.read_text(encoding="utf-8")
        self.assertIn("# Metadata Survey", rendered)
        self.assertIn("- Scanned markdown files: `1`", rendered)

    def test_main_prints_json_by_default(self) -> None:
        (self.root / "governed.md").write_text(
            textwrap.dedent(
                """\
                ---
                title: Governed
                updated: 2026-04-18
                status: active
                authority: LOGAN
                ---

                body
                """
            ),
            encoding="utf-8",
        )

        with mock.patch.object(sys, "argv", ["metadata_survey.py", "--root", str(self.root)]), mock.patch(
            "builtins.print"
        ) as mock_print:
            metadata_survey.main()

        printed = mock_print.call_args.args[0]
        parsed = json.loads(printed)
        self.assertEqual(parsed["scanned_files"], 1)
        self.assertEqual(parsed["frontmatter"]["valid"], 1)


if __name__ == "__main__":
    unittest.main()
