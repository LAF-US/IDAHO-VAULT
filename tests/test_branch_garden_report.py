from __future__ import annotations

import importlib.util
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path


def _load_branch_garden_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "branch_garden_report.py"
    spec = importlib.util.spec_from_file_location("branch_garden_report_test_module", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


branch_garden = _load_branch_garden_module()


class BranchGardenReportTest(unittest.TestCase):
    def test_no_merge_base_branch_requires_salvage_review_without_distance_claims(self) -> None:
        branch = "preserved/pre-purge-history"

        def run_text(cmd: list[str]) -> str:
            if cmd == ["git", "ls-remote", "--heads", "origin"]:
                return (
                    "a" * 40 + "\trefs/heads/main\n"
                    + "b" * 40
                    + f"\trefs/heads/{branch}"
                )
            if cmd[:2] == ["git", "merge-base"]:
                raise subprocess.CalledProcessError(1, cmd)
            if cmd[:2] == ["git", "rev-list"]:
                return "500"
            raise AssertionError(f"unexpected git call: {cmd}")

        with tempfile.TemporaryDirectory() as tempdir:
            report_path = Path(tempdir) / "branch-garden-report.md"
            with (
                mock.patch.object(branch_garden, "run_text", side_effect=run_text),
                mock.patch.object(branch_garden, "run_json", return_value=[]),
                mock.patch.object(branch_garden, "branch_age_days", return_value=120),
                mock.patch.object(
                    sys,
                    "argv",
                    ["branch_garden_report.py", "--report-path", str(report_path)],
                ),
            ):
                self.assertEqual(branch_garden.main(), 0)
            report = report_path.read_text(encoding="utf-8")

        self.assertIn("no merge base with `main`", report)
        self.assertIn("SALVAGE review", report)
        self.assertNotIn("500 ahead", report)
        self.assertNotIn("far behind", report)
        self.assertNotIn("is stale", report)

    def test_run_json_fails_closed_when_git_could_not_run(self) -> None:
        with mock.patch.object(
            branch_garden.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(RuntimeError) as exc:
                branch_garden.run_json(["git", "log"])

        self.assertIn("could not run", str(exc.exception))

    def test_run_text_fails_closed_on_timeout(self) -> None:
        with mock.patch.object(
            branch_garden.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(cmd="git", timeout=60),
        ):
            with self.assertRaises(RuntimeError) as exc:
                branch_garden.run_text(["git", "log"])

        self.assertIn("timed out", str(exc.exception))

    def test_run_json_fails_closed_on_invalid_json(self) -> None:
        with mock.patch.object(
            branch_garden.subprocess, "run", return_value=mock.Mock(stdout="not json")
        ):
            with self.assertRaises(RuntimeError) as exc:
                branch_garden.run_json(["gh", "pr", "list"])

        self.assertIn("invalid JSON", str(exc.exception))

    def test_living_worktree_branches_degrades_to_empty_set_when_git_missing(self) -> None:
        with mock.patch.object(
            branch_garden.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            self.assertEqual(branch_garden.living_worktree_branches(), set())


if __name__ == "__main__":
    unittest.main()
