from __future__ import annotations

import importlib.util
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
    spec.loader.exec_module(module)
    return module


backfill_daily_notes = _load_module("backfill_daily_notes_test_module", "backfill_daily_notes.py")
daily_rollover = _load_module("daily_rollover_for_backfill_test_module", "daily_rollover.py")


class BackfillDailyNotesTest(unittest.TestCase):
    def test_main_repairs_historical_gap_without_touching_todo_list(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        vault_root = project_root / "tests" / "_tmp_backfill_daily_notes_case"
        shutil.rmtree(vault_root, ignore_errors=True)
        vault_root.mkdir(parents=True, exist_ok=True)

        try:
            (vault_root / "2026-04-09.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-09
                    yesterday: 2026-04-08
                    tomorrow: 2026-04-10
                    ---

                    [[TO DO LIST]]

                    - [ ] [[YESTERDAY]]
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

            for note_name in ("2026-04-10.md", "2026-04-11.md"):
                (vault_root / note_name).write_text(
                    textwrap.dedent(
                        f"""\
                        ---
                        title: {note_name[:-3]}
                        yesterday:
                        tomorrow:
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

            (vault_root / "2026-04-12.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-12
                    yesterday: 2026-04-11
                    tomorrow: 2026-04-13
                    TQ_show_urgency: false
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

            (vault_root / "2026-04-13.md").write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: 2026-04-13
                    yesterday: 2026-04-12
                    tomorrow: 2026-04-14
                    ---

                    [[TO DO LIST]]
                    - WORK
                    - []
                    - PERSONAL
                    - []
                    - VAULT
                    - []
                    \t- [[CODEX]] explores the [[VAULT]]...
                    """
                ),
                encoding="utf-8",
            )

            todo_file = vault_root / "TO DO LIST.md"
            todo_file.write_text(
                textwrap.dedent(
                    """\
                    ---
                    title: TO DO LIST
                    ---

                    ## Active

                    - [ ] CURRENT LIVE TASK
                    """
                ),
                encoding="utf-8",
            )

            with mock.patch.object(backfill_daily_notes.daily_rollover, "VAULT_ROOT", vault_root), mock.patch.object(
                backfill_daily_notes.daily_rollover, "TODO_LIST_FILE", todo_file
            ), mock.patch.object(
                sys,
                "argv",
                ["backfill_daily_notes.py", "--start", "2026-04-10", "--end", "2026-04-13"],
            ):
                backfill_daily_notes.main()

            for note_name in ("2026-04-10.md", "2026-04-11.md", "2026-04-12.md", "2026-04-13.md"):
                note_text = (vault_root / note_name).read_text(encoding="utf-8")
                self.assertNotIn("\n- []\n", note_text)
                self.assertNotIn("\n- [ ] \n", note_text)
                self.assertIn("FIX DAILY NOTE SYNCING/CARRYFORWARD", note_text)
                self.assertIn("FMLA PAPERWORK", note_text)

            april_12_text = (vault_root / "2026-04-12.md").read_text(encoding="utf-8")
            self.assertIn("title: 2026-04-12", april_12_text)
            self.assertIn("yesterday: 2026-04-11", april_12_text)
            self.assertIn("tomorrow: 2026-04-13", april_12_text)
            self.assertIn("TQ_show_urgency: false", april_12_text)

            april_13_text = (vault_root / "2026-04-13.md").read_text(encoding="utf-8")
            self.assertIn("[[CODEX]] explores the [[VAULT]]...", april_13_text)

            todo_text = todo_file.read_text(encoding="utf-8")
            self.assertEqual(
                todo_text,
                textwrap.dedent(
                    """\
                    ---
                    title: TO DO LIST
                    ---

                    ## Active

                    - [ ] CURRENT LIVE TASK
                    """
                ),
            )
        finally:
            shutil.rmtree(vault_root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
