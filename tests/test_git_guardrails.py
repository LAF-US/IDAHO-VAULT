from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "!-AGENT-GIT-GUARDRAILS.md"
BASH_WRAPPER = ROOT / "scripts" / "git-guard.sh"
POWERSHELL_WRAPPER = ROOT / "scripts" / "Invoke-GitGuard.ps1"
REPO_URL = "https://github.com/LAF-US/IDAHO-VAULT.git"


class GitGuardrailsTest(unittest.TestCase):
    def test_guardrails_doc_points_to_both_platform_wrappers(self) -> None:
        doc = DOC_PATH.read_text(encoding="utf-8")

        self.assertIn("scripts/git-guard.sh", doc)
        self.assertIn("scripts/Invoke-GitGuard.ps1", doc)
        self.assertIn("cp scripts/git-guard.sh ~/bin/git", doc)
        self.assertIn(". \"<repo root>\\scripts\\Invoke-GitGuard.ps1\"", doc)
        self.assertIn("git remote remove origin", doc)
        self.assertIn("git remote -v", doc)

    def test_shell_wrapper_detects_repo_without_origin_config(self) -> None:
        wrapper = BASH_WRAPPER.read_text(encoding="utf-8")

        self.assertIn("GIT_GUARD_MARKER=idaho-vault-git-guard-v1", wrapper)
        self.assertIn('basename "$toplevel"', wrapper)
        self.assertNotIn("grep -q \"IDAHO-VAULT\" .git/config", wrapper)
        self.assertIn('grep -qx origin', wrapper)
        self.assertIn("GIT_TERMINAL_PROMPT=0", wrapper)
        self.assertIn("GIT_GUARD_FETCH_TIMEOUT", wrapper)
        self.assertIn('exec "$real_git" "$@"', wrapper)

    def test_powershell_wrapper_detects_repo_without_origin_config(self) -> None:
        wrapper = POWERSHELL_WRAPPER.read_text(encoding="utf-8")

        self.assertIn('function global:git', wrapper)
        self.assertIn("Split-Path -Leaf $topLevel", wrapper)
        self.assertIn("$leaf -ieq $repoName", wrapper)
        self.assertNotIn(".git/config", wrapper)
        self.assertIn('EnvironmentVariables["GIT_TERMINAL_PROMPT"]', wrapper)
        self.assertIn("$proc.WaitForExit(10000)", wrapper)

    @unittest.skipIf(
        os.name == "nt",
        "extensionless bash wrapper installed as 'git' cannot be resolved by Windows process creation",
    )
    def test_shell_wrapper_reconnects_missing_origin_when_installed_as_git(self) -> None:
        real_git = shutil.which("git")
        self.assertIsNotNone(real_git, "git must be available to exercise the guard wrapper")
        assert real_git is not None

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_bin = root / "bin"
            fake_bin.mkdir()
            installed_wrapper = fake_bin / "git"
            shutil.copy2(BASH_WRAPPER, installed_wrapper)
            installed_wrapper.chmod(installed_wrapper.stat().st_mode | stat.S_IXUSR)

            repo = root / "IDAHO-VAULT"
            repo.mkdir()

            env = os.environ.copy()
            env["PATH"] = f"{fake_bin}{os.pathsep}{os.path.dirname(real_git)}{os.pathsep}{env['PATH']}"
            env["GIT_GUARD_FETCH_TIMEOUT"] = "0"
            env["GIT_TERMINAL_PROMPT"] = "0"

            subprocess.run([real_git, "init", "-b", "main"], cwd=repo, env=env, check=True)
            subprocess.run([real_git, "remote", "remove", "origin"], cwd=repo, env=env, check=False)

            subprocess.run(["git", "status", "--short"], cwd=repo, env=env, check=True)

            remotes = subprocess.check_output(
                [real_git, "remote", "get-url", "origin"], cwd=repo, env=env, text=True
            ).strip()
            self.assertEqual(remotes, REPO_URL)


if __name__ == "__main__":
    unittest.main()
