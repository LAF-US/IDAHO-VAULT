from __future__ import annotations

import importlib.util
import shutil
import sys
import textwrap
import unittest
from pathlib import Path
from unittest import mock


def _load_daily_rollover_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "daily_rollover.py"
    spec = importlib.util.spec_from_file_location("daily_rollover_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


daily_rollover = _load_daily_rollover_module()


class DailyRolloverTest(unittest.TestCase):
    def test_ensure_daily_frontmatter_adds_missing_canonical_list_fields(self) -> None:
        content = textwrap.dedent(
            """\
            ---
            title: 2026-04-16
            yesterday:
            tomorrow:
            ---

            [[TO DO LIST]]
            """
        )

        repaired = daily_rollover.ensure_daily_frontmatter(content, daily_rollover.date.fromisoformat("2026-04-16"))

        self.assertIn("aliases:", repaired)
        self.assertIn("linter-yaml-title-alias: 2026-04-16", repaired)
        self.assertIn("weekday:\n  - Thursday", repaired)
        self.assertIn("cssclasses:\n  - roygbiv-thu", repaired)
        self.assertIn("tags:\n  - today\n  - 2026/04/16\n  - dailynote", repaired)

    def test_extract_todo_section_respects_marker_inside_named_carryforward_section(self) -> None:
        content = textwrap.dedent(
            """\
            ---
            title: 2026-04-19
            ---

            ## Day planner

            - [ ] 08:00 Morning startup

            ## Carryforward From [[TO DO LIST]]

            [[TO DO LIST]]

            - WORK
            - [ ] Restore the real marker
            - VAULT
            - [ ] Keep rollover truthful

            ## Habits

            - [ ] Startup
            """
        )

        todo_lines = daily_rollover.extract_todo_section(content)

        self.assertEqual(
            todo_lines,
            [
                "",
                "- WORK",
                "- [ ] Restore the real marker",
                "- VAULT",
                "- [ ] Keep rollover truthful",
                "",
            ],
        )

    def test_build_backlog_lines_uses_source_as_authority_and_drops_placeholders(self) -> None:
        source_lines = [
            "- WORK",
            "- [x] finished in source",
            "- [ ] fresh work",
            "\t- [x] done child",
            "\t- [ ] open child",
            "- PERSONAL",
            "- []",
            "- [ ] ",
            "- VAULT",
            "- [ ] vault task",
        ]
        active_lines = [
            "- WORK",
            "- [ ] finished in source",
            "- [ ] backlog work",
            "- PERSONAL",
            "- [x] stale completion",
            "- []",
            "- VAULT",
            "- [ ] backlog vault",
        ]

        backlog = daily_rollover.build_backlog_lines(source_lines, active_lines)

        self.assertEqual(
            backlog,
            [
                "- WORK",
                "- [ ] fresh work",
                "\t- [ ] open child",
                "- [ ] backlog work",
                "- VAULT",
                "- [ ] vault task",
                "- [ ] backlog vault",
            ],
        )

    def test_task_keys_normalize_spacing_around_punctuation(self) -> None:
        keys = daily_rollover.todo_task_keys(
            [
                "- [ ] FIX DAILY NOTE SYNCING/CARRYFORWARD",
                "- [ ] fix daily note syncing / carryforward",
                "- [ ] Fix  daily note syncing  /  carryforward",
            ]
        )

        self.assertEqual(keys, {"fix daily note syncing/carryforward"})

    def test_main_reconciles_today_from_todo_list_when_yesterday_is_missing(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        vault_root = project_root / "tests" / "_tmp_daily_rollover_reconcile_case"
        shutil.rmtree(vault_root, ignore_errors=True)
        vault_root.mkdir(parents=True, exist_ok=True)
        try:
            today_file = vault_root / "2026-04-16.md"
            todo_file = vault_root / "TO DO LIST.md"

            today_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-16
                    cssclasses:
                      - roygbiv-Wed
                    yesterday: 2026-04-15
                    tomorrow: 2026-04-17
                    ---

                    [[TO DO LIST]]

                    *(no incomplete items carried forward)*
                    """
                ),
                encoding="utf-8",
            )

            todo_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: TO DO LIST
                    ---

                    ## Active

                    - WORK
                    - [ ] FIX DAILY NOTE SYNCING/CARRYFORWARD
                    - [ ] fix daily note syncing / carryforward
                    - VAULT
                    - [ ] FMLA PAPERWORK
                    """
                ),
                encoding="utf-8",
            )

            with mock.patch.object(daily_rollover, "VAULT_ROOT", vault_root), mock.patch.object(
                daily_rollover, "TODO_LIST_FILE", todo_file
            ), mock.patch.object(
                sys,
                "argv",
                ["daily_rollover.py", "--date", "2026-04-16"],
            ):
                daily_rollover.main()

            today_text = today_file.read_text(encoding="utf-8")
            todo_text = todo_file.read_text(encoding="utf-8")

            self.assertIn("cssclasses:\n  - roygbiv-thu", today_text)
            self.assertEqual(today_text.count("FIX DAILY NOTE SYNCING/CARRYFORWARD"), 1)
            self.assertNotIn("fix daily note syncing / carryforward", today_text)
            self.assertIn("FMLA PAPERWORK", today_text)
            self.assertNotIn("*(no incomplete items carried forward)*", today_text)

            self.assertEqual(todo_text.count("FIX DAILY NOTE SYNCING/CARRYFORWARD"), 1)
            self.assertNotIn("fix daily note syncing / carryforward", todo_text)
        finally:
            shutil.rmtree(vault_root, ignore_errors=True)

    def test_main_rewrites_today_and_active_backlog_without_duplicate_sections(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        vault_root = project_root / "tests" / "_tmp_daily_rollover_case"
        shutil.rmtree(vault_root, ignore_errors=True)
        vault_root.mkdir(parents=True, exist_ok=True)
        try:
            yesterday_file = vault_root / "2026-04-15.md"
            today_file = vault_root / "2026-04-16.md"
            todo_file = vault_root / "TO DO LIST.md"

            yesterday_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-15
                    ---

                    [[TO DO LIST]]
                    - WORK
                    - []
                    - PERSONAL
                    - []
                    - VAULT
                    - []
                    """
                ),
                encoding="utf-8",
            )

            today_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-16
                    yesterday: 2026-04-15
                    tomorrow: 2026-04-17
                    ---

                    [[TO DO LIST]]

                    - [ ] LEGACY BACKLOG TASK
                    - VAULT
                    - [ ] FIX DAILY NOTE SYNCING/CARRYFORWARD
                    \t- [ ] Tasks completed on a DAY were not checked off here.
                    \t- [ ] Tasks uncomplete on a DAY were not added to here.
                    - WORK
                    - [ ] FMLA PAPERWORK
                    - PERSONAL
                    - [ ] 
                    - VAULT
                    - [x] A250 REVISON WRITING
                    - PERSONAL
                    - [x] RESET Obsidian Sync Vault
                    """
                ),
                encoding="utf-8",
            )

            todo_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: TO DO LIST
                    ---

                    *Persistent list — incomplete items should carry forward daily. Link daily notes here.*

                    ## Active

                    - [ ] LEGACY BACKLOG TASK
                    - VAULT
                    - [ ] FIX DAILY NOTE SYNCING/CARRYFORWARD
                    \t- [ ] Tasks completed on a DAY were not checked off here.
                    \t- [ ] Tasks uncomplete on a DAY were not added to here.
                    - WORK
                    - [ ] FMLA PAPERWORK
                    - PERSONAL
                    - [ ] 
                    - VAULT
                    - [x] A250 REVISON WRITING
                    - PERSONAL
                    - [x] RESET Obsidian Sync Vault
                    - WORK
                    - []
                    - PERSONAL
                    - VAULT
                    """
                ),
                encoding="utf-8",
            )

            with mock.patch.object(daily_rollover, "VAULT_ROOT", vault_root), mock.patch.object(
                daily_rollover, "TODO_LIST_FILE", todo_file
            ), mock.patch.object(
                sys,
                "argv",
                ["daily_rollover.py", "--date", "2026-04-16"],
            ):
                daily_rollover.main()

            today_text = today_file.read_text(encoding="utf-8")
            todo_text = todo_file.read_text(encoding="utf-8")

            self.assertEqual(today_text.count("FIX DAILY NOTE SYNCING/CARRYFORWARD"), 1)
            self.assertEqual(today_text.count("FMLA PAPERWORK"), 1)
            self.assertNotIn("\n- []\n", today_text)
            self.assertNotIn("\n- [ ] \n", today_text)
            self.assertIn("A250 REVISON WRITING", today_text)
            self.assertIn("RESET Obsidian Sync Vault", today_text)

            self.assertEqual(todo_text.count("FIX DAILY NOTE SYNCING/CARRYFORWARD"), 1)
            self.assertEqual(todo_text.count("FMLA PAPERWORK"), 1)
            self.assertNotIn("A250 REVISON WRITING", todo_text)
            self.assertNotIn("RESET Obsidian Sync Vault", todo_text)
            self.assertNotIn("\n- []\n", todo_text)
            self.assertNotIn("\n- [ ] \n", todo_text)

            # Regression: ensure carryforward never propagates ALLCAPS date
            # placeholder tokens, even if a daily note or the persistent list
            # contains them. See _add_block + DATE_PLACEHOLDER_RE in
            # daily_rollover.py.
            self.assertNotIn("[[YESTERDAY]]", today_text)
            self.assertNotIn("[[TOMORROW]]", today_text)
            self.assertNotIn("[[TODAY]]", today_text)
            self.assertNotIn("[[YESTERDAY]]", todo_text)
            self.assertNotIn("[[TOMORROW]]", todo_text)
            self.assertNotIn("[[TODAY]]", todo_text)
        finally:
            shutil.rmtree(vault_root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
