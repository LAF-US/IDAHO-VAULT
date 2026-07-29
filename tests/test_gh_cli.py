"""
Tests for gh_cli.py — the one module that builds a ``gh`` command line.

These assert the exact argv each typed operation emits, and that values which
could turn a value position into a flag (or a path traversal, or a second
command) are rejected before argv is built. The run primitive is private, so a
caller cannot bypass any of this; these tests are what stands behind that claim.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock


def _load_gh_cli_module():
    scripts_dir = Path(__file__).resolve().parents[1] / ".github" / "scripts"
    spec = importlib.util.spec_from_file_location("gh_cli_test_module", scripts_dir / "gh_cli.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    original_sys_path = list(sys.path)
    sys.path.insert(0, str(scripts_dir))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original_sys_path
    return module


gh_cli = _load_gh_cli_module()


def _completed(stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=["gh"], returncode=returncode, stdout=stdout, stderr="")


class ArgvTest(unittest.TestCase):
    """Each typed operation emits exactly the command line it documents."""

    def _argv(self, call, *args, **kwargs) -> tuple[list[str], dict]:
        with mock.patch.object(gh_cli, "_run", return_value=_completed()) as run:
            call(*args, **kwargs)
        run.assert_called_once()
        return (run.call_args.args[0], run.call_args.kwargs)

    def test_label_create(self) -> None:
        argv, kwargs = self._argv(
            gh_cli.label_create, "risk/low", color="0E8A16", description="Low risk"
        )
        self.assertEqual(
            argv,
            ["gh", "label", "create", "risk/low",
             "--color", "0E8A16", "--description", "Low risk", "--force"],
        )
        self.assertEqual(kwargs, {"check": True})

    def test_label_create_without_force(self) -> None:
        argv, _ = self._argv(
            gh_cli.label_create, "risk/low", color="0E8A16", description="d", force=False
        )
        self.assertNotIn("--force", argv)

    def test_pr_edit_add_and_remove(self) -> None:
        argv, kwargs = self._argv(
            gh_cli.pr_edit, 854, add_label="risk/low", remove_label="risk/high", check=False
        )
        self.assertEqual(
            argv,
            ["gh", "pr", "edit", "854",
             "--add-label", "risk/low", "--remove-label", "risk/high"],
        )
        self.assertEqual(kwargs, {"check": False})

    def test_pr_edit_requires_a_label(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli.pr_edit(854)

    def test_pr_view_with_and_without_repo(self) -> None:
        argv, _ = self._argv(gh_cli.pr_view, 12, json_fields="labels")
        self.assertEqual(argv, ["gh", "pr", "view", "12", "--json", "labels"])
        argv, _ = self._argv(
            gh_cli.pr_view, 12, owner="LAF-US", repo="IDAHO-VAULT", json_fields="labels"
        )
        self.assertEqual(
            argv,
            ["gh", "pr", "view", "12", "--repo", "LAF-US/IDAHO-VAULT", "--json", "labels"],
        )

    def test_pr_view_rejects_half_a_repository(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli.pr_view(12, owner="LAF-US", json_fields="labels")

    def test_pr_comment_keeps_multiline_markdown_in_one_element(self) -> None:
        body = "line one\n\n- bullet\n"
        argv, _ = self._argv(gh_cli.pr_comment, 3, body)
        self.assertEqual(argv, ["gh", "pr", "comment", "3", "--body", body])

    def test_pr_merge_arms_and_disarms(self) -> None:
        argv, _ = self._argv(gh_cli.pr_merge, 5, auto=True)
        self.assertEqual(argv, ["gh", "pr", "merge", "5", "--merge", "--auto"])
        argv, _ = self._argv(gh_cli.pr_merge, 5, disable_auto=True)
        self.assertEqual(argv, ["gh", "pr", "merge", "5", "--disable-auto"])
        argv, _ = self._argv(gh_cli.pr_merge, 5)
        self.assertEqual(argv, ["gh", "pr", "merge", "5", "--merge"])

    def test_pr_merge_rejects_any_method_but_the_queues(self) -> None:
        # K5/#631: a divergent merge method is unexpressible, not test-caught.
        for method in ("squash", "rebase", "MERGE"):
            with self.assertRaises(ValueError):
                gh_cli.pr_merge(5, method=method)

    def test_pr_list_open(self) -> None:
        argv, _ = self._argv(gh_cli.pr_list_open, "LAF-US", "IDAHO-VAULT")
        self.assertEqual(
            argv,
            ["gh", "pr", "list", "--repo", "LAF-US/IDAHO-VAULT",
             "--state", "open", "--limit", "1000", "--json", "number"],
        )

    def test_pr_list_open_rejects_a_bad_repository(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli.pr_list_open("LAF-US", "../etc")

    def test_issue_search_open_and_view(self) -> None:
        argv, _ = self._argv(
            gh_cli.issue_search_open, "LAF-US", "IDAHO-VAULT",
            search='"[Looker Worklist] x" in:title', json_fields="number,title",
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "list", "--repo", "LAF-US/IDAHO-VAULT", "--state", "open",
             "--search", '"[Looker Worklist] x" in:title',
             "--json", "number,title", "--limit", "20"],
        )
        argv, _ = self._argv(
            gh_cli.issue_view, 7, owner="LAF-US", repo="IDAHO-VAULT", json_fields="body"
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "view", "7", "--repo", "LAF-US/IDAHO-VAULT", "--json", "body"],
        )

    def test_issue_create_comment_and_close(self) -> None:
        argv, _ = self._argv(
            gh_cli.issue_create,
            owner="LAF-US", repo="IDAHO-VAULT", title="T", body_file="/tmp/body.md",
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "create", "--repo", "LAF-US/IDAHO-VAULT",
             "--title", "T", "--body-file", "/tmp/body.md"],
        )
        argv, _ = self._argv(
            gh_cli.issue_comment, 7, owner="LAF-US", repo="IDAHO-VAULT", body="done"
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "comment", "7", "--repo", "LAF-US/IDAHO-VAULT", "--body", "done"],
        )
        argv, _ = self._argv(
            gh_cli.issue_comment_file,
            7, owner="LAF-US", repo="IDAHO-VAULT", body_file="/tmp/body.md",
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "comment", "7", "--repo", "LAF-US/IDAHO-VAULT",
             "--body-file", "/tmp/body.md"],
        )
        argv, _ = self._argv(
            gh_cli.issue_close, 7, owner="LAF-US", repo="IDAHO-VAULT"
        )
        self.assertEqual(
            argv,
            ["gh", "issue", "close", "7", "--repo", "LAF-US/IDAHO-VAULT",
             "--reason", "completed"],
        )

    def test_issue_close_rejects_an_unknown_reason(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli.issue_close(7, owner="LAF-US", repo="IDAHO-VAULT", reason="because")

    def test_graphql_types_its_variables(self) -> None:
        argv, _ = self._argv(
            gh_cli.graphql, "query($n:Int!){x}", owner="LAF-US", number=854, flag=True
        )
        self.assertEqual(
            argv,
            ["gh", "api", "graphql", "-f", "query=query($n:Int!){x}",
             "-f", "owner=LAF-US", "-F", "number=854", "-f", "flag=True"],
        )

    def test_graphql_rejects_a_non_identifier_variable_name(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli.graphql("query{x}", **{"--switch": "1"})

    def test_api_endpoints(self) -> None:
        argv, _ = self._argv(gh_cli.api_pr_update_branch, "LAF-US", "IDAHO-VAULT", 9)
        self.assertEqual(
            argv,
            ["gh", "api", "--method", "PUT",
             "repos/LAF-US/IDAHO-VAULT/pulls/9/update-branch"],
        )
        argv, _ = self._argv(gh_cli.api_pr_files, "LAF-US", "IDAHO-VAULT", 9)
        self.assertEqual(
            argv,
            ["gh", "api", "--paginate", "repos/LAF-US/IDAHO-VAULT/pulls/9/files",
             "--jq", ".[].filename"],
        )
        argv, _ = self._argv(gh_cli.api_issue_comments, "LAF-US", "IDAHO-VAULT", 9)
        self.assertEqual(
            argv, ["gh", "api", "--paginate", "repos/LAF-US/IDAHO-VAULT/issues/9/comments"]
        )
        argv, _ = self._argv(
            gh_cli.api_issue_comments, "LAF-US", "IDAHO-VAULT", 9, jq=".[].body"
        )
        self.assertEqual(argv[-2:], ["--jq", ".[].body"])


class ValueGuardTest(unittest.TestCase):
    """A value can never become a flag, a path segment, or a second command."""

    def test_slug_rejects_traversal_flags_and_separators(self) -> None:
        for owner, repo in (
            ("..", "IDAHO-VAULT"),
            ("LAF-US", "../../etc"),
            ("--repo=evil", "IDAHO-VAULT"),
            ("LAF-US", "IDAHO VAULT"),
            ("LAF-US/extra", "IDAHO-VAULT"),
            ("", "IDAHO-VAULT"),
        ):
            with self.subTest(owner=owner, repo=repo):
                with self.assertRaises(ValueError):
                    gh_cli._slug(owner, repo)

    def test_slug_accepts_real_names(self) -> None:
        self.assertEqual(gh_cli._slug("LAF-US", "IDAHO-VAULT"), "LAF-US/IDAHO-VAULT")
        self.assertEqual(gh_cli._slug("a_b.c", "d-e_f.g"), "a_b.c/d-e_f.g")

    def test_num_rejects_non_numbers_and_non_positives(self) -> None:
        for value in ("12; rm -rf /", "--flag", "", None, 0, -1):
            with self.subTest(value=value):
                with self.assertRaises((ValueError, TypeError)):
                    gh_cli._num(value)

    def test_num_accepts_a_numeric_string(self) -> None:
        self.assertEqual(gh_cli._num("854"), "854")
        self.assertEqual(gh_cli._num(854), "854")

    def test_validate_cmd_guards_the_argv_this_module_built(self) -> None:
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd([])
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd(["curl", "https://example.test"])
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd(["gh", "pr", 854])
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd(["gh", "pr", "comment", "1", "--body", "a\x00b"])
        # Multi-line bodies stay legal: shell=False means a newline is inert.
        gh_cli._validate_cmd(["gh", "pr", "comment", "1", "--body", "a\nb"])

    def test_run_is_private(self) -> None:
        # The generic sink is not part of the module's surface: adding a gh call means
        # adding a typed operation here, not reaching past it.
        self.assertFalse(hasattr(gh_cli, "run"))


class RunPrimitiveTest(unittest.TestCase):
    """The run-capture-raise contract every operation inherits."""

    def test_returns_the_completed_process_on_success(self) -> None:
        with mock.patch.object(
            gh_cli.subprocess, "run", return_value=_completed(stdout="[]")
        ) as run:
            result = gh_cli._run(["gh", "pr", "list"])
        self.assertEqual(result.stdout, "[]")
        self.assertEqual(
            run.call_args.kwargs,
            {"capture_output": True, "text": True, "timeout": 300, "check": False},
        )

    def test_raises_with_both_streams_on_non_zero_exit(self) -> None:
        failed = subprocess.CompletedProcess(
            args=["gh"], returncode=1, stdout="out", stderr="err"
        )
        with mock.patch.object(gh_cli.subprocess, "run", return_value=failed):
            with self.assertRaises(RuntimeError) as caught:
                gh_cli._run(["gh", "pr", "list"])
        message = str(caught.exception)
        self.assertIn("Command failed (1)", message)
        self.assertIn("out", message)
        self.assertIn("err", message)

    def test_returns_the_failure_when_check_is_false(self) -> None:
        failed = subprocess.CompletedProcess(
            args=["gh"], returncode=1, stdout="", stderr="nope"
        )
        with mock.patch.object(gh_cli.subprocess, "run", return_value=failed):
            result = gh_cli._run(["gh", "pr", "list"], check=False)
        self.assertEqual(result.returncode, 1)

    def test_timeout_raises_the_same_surface_and_decodes_byte_streams(self) -> None:
        expired = subprocess.TimeoutExpired(
            cmd=["gh"], timeout=300, output=b"partial", stderr=b"\xff"
        )
        with mock.patch.object(gh_cli.subprocess, "run", side_effect=expired):
            with self.assertRaises(RuntimeError) as caught:
                gh_cli._run(["gh", "pr", "list"])
        message = str(caught.exception)
        self.assertIn("timed out after 300s", message)
        self.assertIn("partial", message)


if __name__ == "__main__":
    unittest.main()
