from __future__ import annotations

import importlib.util
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


def _load_stale_bot_prs_module():
    project_root = Path(__file__).resolve().parents[1]
    script_dir = project_root / ".github" / "scripts"
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    script_path = script_dir / "stale_bot_prs.py"
    spec = importlib.util.spec_from_file_location("stale_bot_prs_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


stale_bot_prs = _load_stale_bot_prs_module()


class StaleBotPrsTest(unittest.TestCase):
    def test_find_stale_bot_prs_filters_to_conflicted_old_bot_prs(self) -> None:
        now = datetime(2026, 4, 17, 2, 0, tzinfo=timezone.utc)
        stale = stale_bot_prs.find_stale_bot_prs(
            [
                {
                    "number": 11,
                    "title": "Bump requests",
                    "url": "https://example.test/pr/11",
                    "author": {"login": "dependabot[bot]"},
                    "updatedAt": "2026-04-12T12:00:00Z",
                    "headRefName": "dependabot/pip/requests",
                },
                {
                    "number": 12,
                    "title": "Bump urllib3",
                    "url": "https://example.test/pr/12",
                    "author": {"login": "dependabot[bot]"},
                    "updatedAt": "2026-04-16T18:00:00Z",
                    "headRefName": "dependabot/pip/urllib3",
                },
                {
                    "number": 13,
                    "title": "Human patch",
                    "url": "https://example.test/pr/13",
                    "author": {"login": "loganf"},
                    "updatedAt": "2026-04-10T12:00:00Z",
                    "headRefName": "codex/manual-fix",
                },
            ],
            now=now,
            age_days=2,
            merge_state_by_number={
                11: "DIRTY",
                12: "DIRTY",
                13: "DIRTY",
            },
        )

        self.assertEqual(len(stale), 1)
        self.assertEqual(stale[0]["number"], 11)
        self.assertEqual(stale[0]["lifecycle_state"], "abandoned")

    def test_main_sets_lifecycle_before_closing_stale_prs(self) -> None:
        report_path = Path(__file__).resolve().parent / "_tmp_stale_bot_prs_report.md"
        args = SimpleNamespace(
            age_days=2,
            apply=True,
            report_path=report_path,
            comment="closing stale bot pr",
        )
        events: list[object] = []

        def _record_close(*call_args, **call_kwargs):
            events.append(("close", call_args[0], call_kwargs))
            return mock.Mock(returncode=0)

        try:
            with mock.patch.object(stale_bot_prs, "parse_args", return_value=args), mock.patch.object(
                stale_bot_prs,
                "run_json",
                side_effect=[
                    [
                        {
                            "number": 21,
                            "title": "Bump pyyaml",
                            "url": "https://example.test/pr/21",
                            "author": {"login": "dependabot[bot]"},
                            "updatedAt": "2026-04-10T12:00:00Z",
                            "headRefName": "dependabot/pip/pyyaml",
                        }
                    ],
                    {"mergeStateStatus": "DIRTY"},
                ],
            ), mock.patch.object(
                stale_bot_prs,
                "ensure_labels",
                side_effect=lambda: events.append(("ensure-labels",)),
            ), mock.patch.object(
                stale_bot_prs,
                "set_state",
                side_effect=lambda pr_number, state: events.append(("set-state", pr_number, state)),
            ), mock.patch.object(stale_bot_prs.subprocess, "run", side_effect=_record_close):
                result = stale_bot_prs.main()

            self.assertEqual(result, 0)
            self.assertEqual(
                events,
                [
                    ("ensure-labels",),
                    ("set-state", 21, "abandoned"),
                    (
                        "close",
                        [
                            "gh",
                            "pr",
                            "close",
                            "21",
                            "--delete-branch",
                            "--comment",
                            "closing stale bot pr",
                        ],
                        {"check": True},
                    ),
                ],
            )
            self.assertTrue(report_path.exists())
            self.assertIn("lifecycle/abandoned", report_path.read_text(encoding="utf-8"))
        finally:
            report_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
