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

    def test_allows_op_documentation_files(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"# Documentation"
        ):
            findings = secret_checker.findings_for_paths(
                [
                    ".op/SETUP.md",
                    ".op/OP.md",
                    ".op/1password-hygiene-policy.json",
                    ".op/notes.txt",
                ],
                staged=False,
            )
        self.assertEqual(findings, [])

    def test_rejects_op_json_files(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"policy data"
        ):
            findings = secret_checker.findings_for_paths([".op/credentials.json"], staged=False)
        self.assertEqual({finding.rule for finding in findings}, {"secret_path"})

    def test_rejects_op_extensionless_credential_files(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"config data"
        ):
            findings = secret_checker.findings_for_paths([".op/config"], staged=False)
        self.assertEqual({finding.rule for finding in findings}, {"secret_path"})

    def test_rejects_op_subdirectory_files(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"# Documentation"
        ):
            findings = secret_checker.findings_for_paths([".op/docs/guide.md"], staged=False)
        self.assertEqual({finding.rule for finding in findings}, {"secret_path"})

    def test_rejects_preserved_and_windows_copy_secret_path_variants(self) -> None:
        with unittest.mock.patch.object(
            secret_checker, "worktree_file_bytes", return_value=b"reference only"
        ):
            findings = secret_checker.findings_for_paths(
                [
                    ".claude/.credentials (2).json",
                    ".codex/auth.json.home",
                    ".codex/auth.json.home.abcdef123456",
                    ".ssh/claude_code_signing (2)",
                    ".ssh/allowed_signers (2)",
                    ".ollama/id_ed25519 (2)",
                ],
                staged=False,
            )
        self.assertEqual(len(findings), 6)
        self.assertEqual({finding.rule for finding in findings}, {"secret_path"})

    def test_normalized_path_variants_strip_salvage_suffixes(self) -> None:
        variants = secret_checker.normalized_path_variants(
            ".codex/auth (2).json.home.abcdef123456"
        )
        self.assertIn(".codex/auth.json", variants)

    def test_run_git_fails_closed_when_git_missing(self) -> None:
        with unittest.mock.patch.object(
            secret_checker.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(RuntimeError) as exc:
                secret_checker.run_git(["diff"])
        self.assertIn("could not run", str(exc.exception))

    def test_staged_file_bytes_fails_closed_on_timeout(self) -> None:
        with unittest.mock.patch.object(
            secret_checker.subprocess,
            "run",
            side_effect=secret_checker.subprocess.TimeoutExpired(cmd="git show", timeout=30),
        ):
            with self.assertRaises(RuntimeError) as exc:
                secret_checker.staged_file_bytes("some/file.txt")
        self.assertIn("timed out", str(exc.exception))

    def test_main_fails_closed_when_git_missing(self) -> None:
        import io
        from contextlib import redirect_stderr

        with unittest.mock.patch.object(
            secret_checker.subprocess, "run", side_effect=FileNotFoundError("git")
        ), unittest.mock.patch.object(
            secret_checker.sys, "argv", ["check_secret_patterns.py", "--staged"]
        ), redirect_stderr(io.StringIO()) as captured_stderr:
            status = secret_checker.main()

        self.assertEqual(status, 1)
        self.assertIn("could not run", captured_stderr.getvalue())

if __name__ == "__main__":
    unittest.main()
