from __future__ import annotations

from datetime import date
import shutil
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.operator_context import (
    BOOT_CHAIN_SURFACES,
    OPERATOR_FRONT_DOOR_SURFACES,
    _tracked_files,
    evaluate_evidence_refs,
    load_operator_context,
)


class OperatorContextTest(unittest.TestCase):
    def test_load_operator_context_resolves_daily_note_and_backlog(self) -> None:
        root = PROJECT_ROOT / "tests" / "_tmp_operator_context_case"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True, exist_ok=True)
        try:
            for relpath in (*BOOT_CHAIN_SURFACES, *OPERATOR_FRONT_DOOR_SURFACES):
                path = root / relpath
                path.parent.mkdir(parents=True, exist_ok=True)
                if path.suffix == ".json":
                    if path.name == "daily-notes.json":
                        path.write_text('{"template":"DAILY NOTE TEMPLATE","folder":""}', encoding="utf-8")
                    elif path.name == "data.json":
                        path.write_text(
                            (
                                '{"daily":{"format":"YYYY-MM-DD","template":"DAILY NOTE TEMPLATE",'
                                '"folder":"","enabled":true}}'
                            ),
                            encoding="utf-8",
                        )
                    else:
                        path.write_text("{}", encoding="utf-8")
                else:
                    path.write_text("placeholder", encoding="utf-8")

            (root / "2026-04-17.md").write_text("# daily note", encoding="utf-8")
            (root / "TO DO LIST.md").write_text(
                "\n".join(
                    [
                        "---",
                        "title: TO DO LIST",
                        "---",
                        "",
                        "## Active",
                        "",
                        "- WORK",
                        "- [ ] Ship the front-door validator",
                        "- [ ] Wire the threshold runner",
                    ]
                ),
                encoding="utf-8",
            )

            context = load_operator_context(root=root, target_date=date(2026, 4, 17))
        finally:
            shutil.rmtree(root, ignore_errors=True)

        self.assertTrue(context.boot_chain_ok)
        self.assertTrue(context.front_door_ok)
        self.assertTrue(context.current_daily_note_ok)
        self.assertEqual(context.daily_note_path, "2026-04-17.md")
        self.assertEqual(
            context.open_backlog_items,
            (
                "- [ ] Ship the front-door validator",
                "- [ ] Wire the threshold runner",
            ),
        )

    def test_evaluate_evidence_refs_reports_missing_and_untracked_refs(self) -> None:
        root = PROJECT_ROOT / "tests" / "_tmp_operator_context_evidence"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True, exist_ok=True)
        try:
            present = root / "present.md"
            present.write_text("present", encoding="utf-8")

            statuses = evaluate_evidence_refs(
                ["present.md", "missing.md", "present.md#L12"],
                root=root,
                tracked_files={"missing.md"},
            )
        finally:
            shutil.rmtree(root, ignore_errors=True)

        self.assertEqual(len(statuses), 2)
        self.assertTrue(statuses[0].exists)
        self.assertFalse(statuses[0].tracked)
        self.assertFalse(statuses[1].exists)
        self.assertTrue(statuses[1].tracked)

    def test_tracked_files_returns_none_when_git_is_unavailable(self) -> None:
        with patch("idaho_vault.operator_context.subprocess.run", side_effect=FileNotFoundError):
            self.assertIsNone(_tracked_files(PROJECT_ROOT))


if __name__ == "__main__":
    unittest.main()
