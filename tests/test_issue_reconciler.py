"""Tests for issue_reconciler.py — the find-or-create-by-title recurring-issue driver."""
# Two halves: ``IssueReconcilerTest`` covers the create/comment/close decision, and
# ``LookupTest`` covers the search and fingerprint reads underneath it — the half the
# gh_cli migration rewrote.

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from unittest import TestCase, main, mock


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


class IssueReconcilerTest(TestCase):
    """Which of create / comment / close the current findings select."""

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


class LookupTest(TestCase):
    """The search/view logic the gh_cli migration rewrote."""

    def _result(self, stdout: str = "", returncode: int = 0):
        # Built from the module's own subprocess, so this test file needs no
        # subprocess import of its own and stays pinned to what gh_cli returns.
        return issue_reconciler.gh_cli.subprocess.CompletedProcess(
            args=["gh"], returncode=returncode, stdout=stdout, stderr=""
        )

    def _env(self):
        return mock.patch.dict(
            "os.environ", {"GITHUB_REPOSITORY": "LAF-US/IDAHO-VAULT"}, clear=False
        )

    def test_find_open_issue_requires_an_exact_title_match(self) -> None:
        # gh's --search is fuzzy, so the exact-title check is what actually decides.
        payload = json.dumps(
            [{"number": 5, "title": "[Looker Worklist] Review-thread triage census (old)"},
             {"number": 7, "title": "[Looker Worklist] Review-thread triage census"}]
        )
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli, "issue_search_open", return_value=self._result(payload)
        ) as search:
            found = issue_reconciler.find_open_issue_number(
                "[Looker Worklist] Review-thread triage census"
            )
        self.assertEqual(found, 7)
        search.assert_called_once_with(
            "LAF-US",
            "IDAHO-VAULT",
            search='"[Looker Worklist] Review-thread triage census" in:title',
            json_fields="number,title",
        )

    def test_find_open_issue_raises_when_the_search_fails(self) -> None:
        # A failed lookup must not be mistaken for "no issue exists": the caller would
        # then open a duplicate on every transient gh/API blip. It propagates instead,
        # matching what this did before the gh_cli migration.
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli, "issue_search_open", side_effect=RuntimeError("gh down")
        ), self.assertRaises(RuntimeError):
            issue_reconciler.find_open_issue_number("anything")

    def test_find_open_issue_survives_unparseable_output(self) -> None:
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli, "issue_search_open", return_value=self._result("not json")
        ):
            self.assertIsNone(issue_reconciler.find_open_issue_number("anything"))

    def test_fingerprint_found_in_the_issue_body_skips_the_comment_read(self) -> None:
        marker = "<!-- issue-reconciler-fingerprint:abc -->"
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli,
            "issue_view",
            return_value=self._result(json.dumps({"body": f"report\n\n{marker}\n"})),
        ), mock.patch.object(
            issue_reconciler.gh_cli, "api_issue_comments"
        ) as comments:
            self.assertTrue(issue_reconciler.issue_has_fingerprint(7, marker))
        comments.assert_not_called()

    def test_fingerprint_falls_through_to_comments(self) -> None:
        marker = "<!-- issue-reconciler-fingerprint:abc -->"
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli,
            "issue_view",
            return_value=self._result(json.dumps({"body": "no marker here"})),
        ), mock.patch.object(
            issue_reconciler.gh_cli,
            "api_issue_comments",
            return_value=self._result(f"something\n{marker}\n"),
        ) as comments:
            self.assertTrue(issue_reconciler.issue_has_fingerprint(7, marker))
        comments.assert_called_once_with(
            "LAF-US", "IDAHO-VAULT", 7, jq=".[].body", check=False
        )

    def test_fingerprint_absent_when_the_comment_read_fails(self) -> None:
        # api_issue_comments runs with check=False, so a non-zero exit arrives as a
        # returncode rather than an exception — and must read as "not found", not as
        # a crash and not as a false duplicate.
        marker = "<!-- issue-reconciler-fingerprint:abc -->"
        with self._env(), mock.patch.object(
            issue_reconciler.gh_cli,
            "issue_view",
            side_effect=RuntimeError("no such issue"),
        ), mock.patch.object(
            issue_reconciler.gh_cli,
            "api_issue_comments",
            return_value=self._result("", returncode=1),
        ):
            self.assertFalse(issue_reconciler.issue_has_fingerprint(7, marker))

    def test_repo_rejects_a_missing_or_malformed_repository(self) -> None:
        for value in ("", "no-slash"):
            with self.subTest(value=value):
                with mock.patch.dict(
                    "os.environ", {"GITHUB_REPOSITORY": value}, clear=False
                ), self.assertRaises(RuntimeError):
                    issue_reconciler._repo()

    def test_body_fingerprint_refuses_a_traversing_path(self) -> None:
        with self.assertRaises(ValueError):
            issue_reconciler.ensure_body_fingerprint(Path("../etc/passwd"))

    def test_body_fingerprint_is_stable_across_restamping(self) -> None:
        # The digest is taken with any previous marker stripped, so an unchanged report
        # yields an unchanged marker — that is the whole basis of the duplicate check.
        with tempfile.TemporaryDirectory() as tempdir:
            body_file = Path(tempdir) / "report.md"
            body_file.write_text("# Report\n\nfindings\n", encoding="utf-8")
            first = issue_reconciler.ensure_body_fingerprint(body_file)
            second = issue_reconciler.ensure_body_fingerprint(body_file)
        self.assertEqual(first, second)


if __name__ == "__main__":
    main()
