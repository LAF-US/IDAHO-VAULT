from __future__ import annotations

import importlib.util
import io
import sys
import unittest
import unittest.mock
from contextlib import redirect_stderr
from pathlib import Path


def _load_large_file_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_large_files.py"
    spec = importlib.util.spec_from_file_location("large_file_checker_test_module", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


large_file_checker = _load_large_file_checker()


class LargeFileCheckerTest(unittest.TestCase):
    def test_run_git_fails_closed_when_git_missing(self) -> None:
        with unittest.mock.patch.object(
            large_file_checker.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(RuntimeError) as exc:
                large_file_checker.run_git(["ls-files", "-z"])
        self.assertIn("could not run", str(exc.exception))

    def test_run_git_fails_closed_on_timeout(self) -> None:
        with unittest.mock.patch.object(
            large_file_checker.subprocess,
            "run",
            side_effect=large_file_checker.subprocess.TimeoutExpired(cmd="git", timeout=30),
        ):
            with self.assertRaises(RuntimeError) as exc:
                large_file_checker.run_git(["status"])
        self.assertIn("timed out", str(exc.exception))

    def test_main_fails_closed_when_git_missing(self) -> None:
        with unittest.mock.patch.object(
            large_file_checker.subprocess, "run", side_effect=FileNotFoundError("git")
        ), unittest.mock.patch.object(
            large_file_checker.sys, "argv", ["check_large_files.py", "--all-tracked"]
        ), redirect_stderr(io.StringIO()) as captured_stderr:
            status = large_file_checker.main()

        self.assertEqual(status, 1)
        self.assertIn("could not run", captured_stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
