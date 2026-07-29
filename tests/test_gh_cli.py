"""Tests for gh_cli._validate_cmd — the argv guard on the shared gh wrapper.

Covers the command-shape allowlist added in response to CodeQL's "uncontrolled
command line" finding: the verb prefix is pinned to a literal set, while argument
values (PR numbers, label text, multi-line bodies, jq expressions) stay free.
"""

# pylint: disable=missing-function-docstring,missing-class-docstring,protected-access

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / ".github" / "scripts"
_original_sys_path = list(sys.path)
sys.path.insert(0, str(SCRIPTS_DIR))
try:
    import gh_cli
finally:
    sys.path[:] = _original_sys_path


class ValidateCmdTest(TestCase):
    def test_rejects_empty_and_non_gh_executables(self):
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd([])
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd(["curl", "https://example.com"])

    def test_rejects_nul_bytes(self):
        with self.assertRaises(ValueError):
            gh_cli._validate_cmd(["gh", "pr", "comment", "1", "--body", "a\x00b"])

    def test_allows_every_family_the_scripts_actually_use(self):
        # Each entry is a real invocation shape from .github/**/*.py. If one of these
        # starts raising, an engine has lost its ability to run in production.
        for cmd in (
            ["gh", "api", "--paginate", "repos/o/r/issues/1/comments", "--jq", ".[].body"],
            ["gh", "api", "graphql", "-f", "query=query{}"],
            ["gh", "label", "create", "risk/med", "--color", "F9D0C4", "--force"],
            ["gh", "pr", "close", "21"],
            ["gh", "pr", "comment", "5", "--body", "multi\nline\nattestation"],
            ["gh", "pr", "edit", "5", "--add-label", "merge/auto"],
            ["gh", "pr", "list", "--state", "open", "--json", "number"],
            ["gh", "pr", "merge", "10", "--auto", "--merge"],
            ["gh", "pr", "view", "5", "--json", "mergeStateStatus"],
            ["gh", "issue", "list", "--repo", "o/r", "--state", "open"],
            ["gh", "issue", "view", "7", "--repo", "o/r", "--json", "body"],
            ["gh", "issue", "create", "--repo", "o/r", "--title", "t", "--body", "b"],
            ["gh", "issue", "comment", "7", "--repo", "o/r", "--body-file", "f.md"],
            ["gh", "issue", "close", "7", "--repo", "o/r", "--reason", "completed"],
        ):
            with self.subTest(cmd=cmd):
                gh_cli._validate_cmd(cmd)  # must not raise

    def test_rejects_a_family_outside_the_allowlist(self):
        # The point of the guard: an unlisted verb cannot be reached even though the
        # executable is allowed and the argv is well-formed.
        for cmd in (
            ["gh", "repo", "delete", "o/r", "--yes"],
            ["gh", "auth", "token"],
            ["gh", "release", "create", "v1"],
            ["gh", "label", "delete", "risk/—"],  # create is allowed; delete is not
        ):
            with self.subTest(cmd=cmd):
                with self.assertRaises(ValueError):
                    gh_cli._validate_cmd(cmd)

    def test_multiline_body_values_remain_legal(self):
        # Regression guard: an earlier newline check broke every attestation comment.
        gh_cli._validate_cmd(
            ["gh", "pr", "comment", "1", "--body", "Looked by `x`\n\n<!-- looked: v=1 -->"]
        )


if __name__ == "__main__":
    main()
