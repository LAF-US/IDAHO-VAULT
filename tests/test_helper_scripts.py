from __future__ import annotations

import importlib.util
import types
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


run_checks = _load_module("run_checks_test_module", "run_checks.py")
check_syntax = _load_module("check_syntax_test_module", "__check_syntax__.py")


class HelperScriptsTest(unittest.TestCase):
    def test_run_checks_uses_repo_root_for_syntax_checks(self) -> None:
        with patch.object(run_checks, "collect_syntax_files", return_value=[".github/scripts/example.py"]), patch.object(
            run_checks.subprocess,
            "run",
            return_value=types.SimpleNamespace(returncode=0, stdout="", stderr=""),
        ) as mock_run:
            status = run_checks.run_syntax_checks("python")

        self.assertEqual(status, 0)
        mock_run.assert_called_once_with(
            ["python", "-m", "py_compile", ".github/scripts/example.py"],
            cwd=run_checks.REPO_ROOT,
            capture_output=True,
            text=True,
        )

    def test_check_syntax_compiles_from_repo_root_and_runs_tests_there(self) -> None:
        with patch.object(check_syntax.py_compile, "compile") as mock_compile, patch.object(
            check_syntax.subprocess,
            "run",
            return_value=types.SimpleNamespace(returncode=0, stdout="", stderr=""),
        ) as mock_run:
            status = check_syntax.main()

        self.assertEqual(status, 0)
        self.assertEqual(mock_compile.call_count, len(check_syntax.FILES_TO_CHECK))
        compiled_paths = [call.args[0] for call in mock_compile.call_args_list]
        self.assertEqual(
            compiled_paths,
            [str(check_syntax.REPO_ROOT / file_path) for file_path in check_syntax.FILES_TO_CHECK],
        )
        mock_run.assert_called_once_with(
            ["python", "-m", "unittest", check_syntax.UNITTEST_TARGET, "-v"],
            cwd=check_syntax.REPO_ROOT,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
