from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


run_checks = _load_module("run_checks_test_module", "run_checks.py")
check_syntax = _load_module("check_syntax_test_module", "__check_syntax__.py")
check_portable_paths = _load_module(
    "check_portable_paths_test_module", ".github/scripts/check_portable_paths.py"
)
large_file_watchdog = _load_module(
    "large_file_watchdog_test_module", ".github/scripts/large_file_watchdog.py"
)
jupytext_sync_paired = _load_module(
    "jupytext_sync_paired_test_module", ".github/scripts/jupytext_sync_paired.py"
)


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
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
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
            [check_syntax.sys.executable, "-m", "unittest", check_syntax.UNITTEST_TARGET, "-v"],
            cwd=check_syntax.REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
            check=False,
        )

    def test_portable_paths_detects_case_only_collisions(self) -> None:
        collisions = check_portable_paths.case_collisions(
            ["SOURCES/Foo.md", "SOURCES/foo.md", "SOURCES/bar.md"]
        )

        self.assertIn("sources/foo.md", collisions)
        self.assertEqual(collisions["sources/foo.md"], ["SOURCES/Foo.md", "SOURCES/foo.md"])

    def test_portable_paths_reports_reserved_names(self) -> None:
        findings = check_portable_paths.path_violations("NOTES/CON.md")

        self.assertEqual(findings, ["RESERVED NAME: NOTES/CON.md (component: CON.md)"])

    def test_portable_paths_flags_backslash_paths(self) -> None:
        # The exact shape that broke Windows checkout: a Windows-absolute path
        # committed as a single tracked name with literal backslashes.
        findings = check_portable_paths.path_violations(
            r"C:\Users\loganf\.vibe\logs\session/s/messages.jsonl"
        )

        self.assertTrue(
            any(f.startswith("BACKSLASH IN PATH:") for f in findings),
            findings,
        )

    def test_portable_paths_clean_path_has_no_findings(self) -> None:
        self.assertEqual(check_portable_paths.path_violations("notes/clean-name.md"), [])

    def test_portable_paths_git_tracked_files_fails_closed_when_git_missing(self) -> None:
        with patch.object(
            check_portable_paths.subprocess,
            "run",
            side_effect=FileNotFoundError("git"),
        ):
            with self.assertRaises(RuntimeError) as exc:
                check_portable_paths.git_tracked_files()

        self.assertIn("could not run", str(exc.exception))

    def test_large_file_watchdog_fails_closed_when_git_missing(self) -> None:
        with (
            patch.object(
                large_file_watchdog.subprocess,
                "run",
                side_effect=FileNotFoundError("git"),
            ),
            patch.object(
                # Never actually written: git failure returns before the report step.
                # A non-hardcoded-tmp placeholder avoids tripping Bandit's B108 on a
                # path this test never opens.
                sys, "argv", ["large_file_watchdog.py", "--report-path", "report.md"]
            ),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()) as captured_stderr,
        ):
            status = large_file_watchdog.main()

        self.assertEqual(status, 1)
        self.assertIn("could not run", captured_stderr.getvalue())

    def test_large_file_watchdog_tolerates_non_utf8_tracked_filenames(self) -> None:
        # A lone continuation byte (0x80) is never valid UTF-8 on its own --
        # git can still track a file whose name isn't valid UTF-8.
        stdout = b"weird-\x80-name.md\0"
        with tempfile.TemporaryDirectory() as tmp_dir:
            report_path = Path(tmp_dir) / "report.md"
            with (
                patch.object(
                    large_file_watchdog.subprocess,
                    "run",
                    return_value=types.SimpleNamespace(returncode=0, stdout=stdout, stderr=b""),
                ),
                patch.object(
                    sys, "argv", ["large_file_watchdog.py", "--report-path", str(report_path)]
                ),
                redirect_stdout(io.StringIO()),
            ):
                status = large_file_watchdog.main()

        self.assertEqual(status, 0)


class JupytextSyncPairedTest(unittest.TestCase):
    """The paired-sync helper's contract: skip unpaired, surface (don't fail on) corrupt
    notebooks, fail on a real sync error, and keep stdout to twin-paths only."""

    def _run_main(self, argv: list[str]):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = jupytext_sync_paired.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_unpaired_notebook_is_skipped(self) -> None:
        with patch.object(
            jupytext_sync_paired, "read_notebook", return_value=({"metadata": {}}, None)
        ), patch.object(jupytext_sync_paired.subprocess, "run") as mock_run:
            code, out, _ = self._run_main(["prog", "nb.ipynb"])

        self.assertEqual(code, 0)
        mock_run.assert_not_called()  # unpaired notebooks are never synced
        self.assertEqual(out, "")

    def test_corrupt_notebook_reported_to_stderr_without_failing(self) -> None:
        with patch.object(
            jupytext_sync_paired, "read_notebook", return_value=(None, ValueError("bad json"))
        ), patch.object(jupytext_sync_paired.subprocess, "run") as mock_run:
            code, out, err = self._run_main(["prog", "broken.ipynb"])

        self.assertEqual(code, 0)  # a corrupt stray is observability, not a failure
        mock_run.assert_not_called()  # ...and is never synced
        self.assertEqual(out, "")  # stdout stays clean (the hook contract)
        self.assertIn("broken.ipynb", err)  # ...but is surfaced on stderr
        self.assertIn("unparseable", err)

    def test_nonzero_jupytext_exit_fails_the_run(self) -> None:
        paired = ({"metadata": {"jupytext": {"formats": "ipynb,md"}}}, None)
        with patch.object(
            jupytext_sync_paired, "read_notebook", return_value=paired
        ), patch.object(
            jupytext_sync_paired.subprocess,
            "run",
            return_value=types.SimpleNamespace(returncode=1, stdout="", stderr="boom"),
        ):
            code, _, err = self._run_main(["prog", "paired.ipynb"])

        self.assertEqual(code, 1)  # a paired notebook that fails to sync fails the run
        self.assertIn("paired.ipynb", err)

    def test_paired_success_prints_only_twin_path_on_stdout(self) -> None:
        # The stdout contract the pre-commit hook word-splits: ONLY twin paths reach stdout --
        # jupytext's own chatter (here on the captured subprocess stdout) must not leak through.
        paired = ({"metadata": {"jupytext": {"formats": "ipynb,md"}}}, None)
        with patch.object(
            jupytext_sync_paired, "read_notebook", return_value=paired
        ), patch.object(
            jupytext_sync_paired.os.path, "exists", return_value=True
        ), patch.object(
            jupytext_sync_paired.subprocess,
            "run",
            return_value=types.SimpleNamespace(
                returncode=0, stdout="[jupytext] noisy chatter", stderr=""
            ),
        ):
            code, out, _ = self._run_main(["prog", "LLM-Router.ipynb"])

        self.assertEqual(code, 0)
        self.assertEqual(out, "LLM-Router.md\n")  # twin only; no jupytext chatter

    def test_twin_paths_parses_common_formats(self) -> None:
        self.assertEqual(
            jupytext_sync_paired.twin_paths("LLM-Router.ipynb", "ipynb,md"), ["LLM-Router.md"]
        )
        self.assertEqual(
            jupytext_sync_paired.twin_paths("nb/Deep.ipynb", "ipynb,py:percent"), ["nb/Deep.py"]
        )
        self.assertEqual(
            jupytext_sync_paired.twin_paths("x.ipynb", "ipynb,md,py:light"), ["x.md", "x.py"]
        )
        self.assertEqual(jupytext_sync_paired.twin_paths("x.ipynb", "ipynb"), [])


if __name__ == "__main__":
    unittest.main()
