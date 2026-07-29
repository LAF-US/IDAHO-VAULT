from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def _load_issue_reconciler_module():
    project_root = Path(__file__).resolve().parents[1]
    scripts_dir = project_root / ".github" / "scripts"
    script_path = scripts_dir / "issue_reconciler.py"
    spec = importlib.util.spec_from_file_location("issue_reconciler_test_module", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("issue_reconciler.py could not be loaded by file path")
    module = importlib.util.module_from_spec(spec)
    # The reconciler imports gh_cli as a sibling module; loading it by file path needs
    # the scripts dir importable. Scope the mutation to the exec, as the engine tests do.
    original_sys_path = list(sys.path)
    sys.path.insert(0, str(scripts_dir))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original_sys_path
    return module


issue_reconciler = _load_issue_reconciler_module()


class IssueReconcilerTest(unittest.TestCase):
    def test_creates_issue_when_findings_exist_and_no_open_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.dict(
            "os.environ", {"GITHUB_REPOSITORY": "LAF-US/IDAHO-VAULT"}, clear=False
        ), mock.patch.object(
            issue_reconciler, "find_open_issue_number", return_value=None
        ), mock.patch.object(
            issue_reconciler, "create_issue", return_value=321
        ) as create_issue, mock.patch.object(
            issue_reconciler, "comment_issue"
        ) as comment_issue, mock.patch.object(
            issue_reconciler, "close_issue"
        ) as close_issue:
            body_file = Path(tempdir) / "report.md"
            body_file.write_text("# Report\n", encoding="utf-8")

            report = issue_reconciler.reconcile_issue(
                title="[Branch Garden] Weekly report",
                body_file=body_file,
                has_findings=True,
                resolved_comment="done",
            )

        create_issue.assert_called_once_with("[Branch Garden] Weekly report", body_file)
        comment_issue.assert_not_called()
        close_issue.assert_not_called()
        self.assertEqual(report["issue_action"], "created")
        self.assertEqual(report["issue_number"], 321)

    def test_comments_when_findings_exist_and_issue_is_open(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.dict(
            "os.environ", {"GITHUB_REPOSITORY": "LAF-US/IDAHO-VAULT"}, clear=False
        ), mock.patch.object(
            issue_reconciler, "find_open_issue_number", return_value=99
        ), mock.patch.object(
            issue_reconciler, "issue_has_fingerprint", return_value=False
        ), mock.patch.object(
            issue_reconciler, "comment_issue"
        ) as comment_issue, mock.patch.object(
            issue_reconciler, "create_issue"
        ) as create_issue, mock.patch.object(
            issue_reconciler, "close_issue"
        ) as close_issue:
            body_file = Path(tempdir) / "report.md"
            body_file.write_text("# Report\n", encoding="utf-8")

            report = issue_reconciler.reconcile_issue(
                title="[Large File Watchdog] Weekly report",
                body_file=body_file,
                has_findings=True,
                resolved_comment="done",
            )

        comment_issue.assert_called_once_with(99, body_file)
        create_issue.assert_not_called()
        close_issue.assert_not_called()
        self.assertEqual(report["issue_action"], "commented")
        self.assertEqual(report["issue_number"], 99)

    def test_closes_open_issue_when_findings_clear(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir, mock.patch.dict(
            "os.environ", {"GITHUB_REPOSITORY": "LAF-US/IDAHO-VAULT"}, clear=False
        ), mock.patch.object(
            issue_reconciler, "find_open_issue_number", return_value=41
        ), mock.patch.object(
            issue_reconciler.gh_cli, "issue_comment"
        ) as issue_comment, mock.patch.object(
            issue_reconciler, "close_issue"
        ) as close_issue:
            body_file = Path(tempdir) / "report.md"
            body_file.write_text("# Report\n", encoding="utf-8")

            report = issue_reconciler.reconcile_issue(
                title="[PR Loop Watchdog] Reconciliation report",
                body_file=body_file,
                has_findings=False,
                resolved_comment="Resolved automatically.",
            )

        issue_comment.assert_called_once_with(
            41,
            owner="LAF-US",
            repo="IDAHO-VAULT",
            body="Resolved automatically.",
        )
        close_issue.assert_called_once_with(41)
        self.assertEqual(report["issue_action"], "closed")


if __name__ == "__main__":
    unittest.main()
