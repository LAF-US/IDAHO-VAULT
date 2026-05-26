from __future__ import annotations

import importlib.util
import sys
import unittest
import unittest.mock
from pathlib import Path


def _load_secret_checker():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "check_secret_patterns.py"
    spec = importlib.util.spec_from_file_location("secret_checker_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


secret_checker = _load_secret_checker()


class SecretCheckerTest(unittest.TestCase):
    def test_detects_quoted_json_token_assignment(self) -> None:
        value = b"abcdefghijklmnop" + b"qrstuvwxyz123456"
        data = b'{"gateway": {"token": "' + value + b'"}}'
        rules = {finding.rule for finding in secret_checker.content_findings("config.json", data)}
        self.assertIn("generic_secret_assignment", rules)

    def test_allow_marker_does_not_suppress_dedicated_token(self) -> None:
        value = b"ghp_" + b"abcdefghijklmnop" + b"qrstuvwxyz1234567890"
        data = b'github_token = "' + value + b'" # secret-pattern: allow'
        rules = {finding.rule for finding in secret_checker.content_findings("config.txt", data)}
        self.assertIn("github_token", rules)

    def test_detects_token_in_nul_containing_content(self) -> None:
        value = b"abcdefghijklmnop" + b"qrstuvwxyz123456"
        data = b'\x00{"token": "' + value + b'"}\x00'
        rules = {finding.rule for finding in secret_checker.content_findings("mixed.bin", data)}
        self.assertIn("generic_secret_assignment", rules)

    def test_detects_token_after_previous_size_limit(self) -> None:
        value = b"abcdefghijklmnop" + b"qrstuvwxyz123456"
        data = b"x" * (1024 * 1024 + 1) + b'\n"token": "' + value + b'"'
        rules = {finding.rule for finding in secret_checker.content_findings("large.txt", data)}
        self.assertIn("generic_secret_assignment", rules)

    def test_allows_runtime_secret_references(self) -> None:
        data = b'{"token": "env:OPENCLAW_GATEWAY_TOKEN", "secret": "$secretRef:gateway/token"}'
        self.assertEqual(secret_checker.content_findings("config.json", data), [])

    def test_allows_deletion_of_sensitive_path(self) -> None:
        with unittest.mock.patch.object(secret_checker, "worktree_file_bytes", return_value=None):
            findings = secret_checker.findings_for_paths([".op/removed-token.ps1"], staged=False)
        self.assertEqual(findings, [])

    def test_rejects_sensitive_path_when_file_still_exists(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"reference only"
        ):
            findings = secret_checker.findings_for_paths([".op/token-helper.ps1"], staged=False)
        self.assertEqual({finding.rule for finding in findings}, {"secret_path"})


if __name__ == "__main__":
    unittest.main()
