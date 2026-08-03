from __future__ import annotations

import importlib.util
import sys
import unittest
from unittest.mock import patch
from pathlib import Path


def _load_installer():
    """Load the installer by file path: its name is hyphenated, and it imports a
    sibling module, so the scripts dir has to be on sys.path first."""
    scripts = Path(__file__).resolve().parents[1] / ".codex/skills/.system/skill-installer/scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location(
        "install_skill_from_github", scripts / "install-skill-from-github.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # @dataclass resolves cls.__module__ through sys.modules, so the entry has
    # to exist before the module body runs.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


installer = _load_installer()


class GitArgumentGuardTest(unittest.TestCase):
    """git reads its own options out of argv, so shell=False is not sufficient:
    a ref or path beginning with `-` becomes an option to git rather than data."""

    def test_option_like_ref_is_refused(self) -> None:
        # --upload-pack makes git execute an arbitrary command on clone.
        with self.assertRaises(installer.InstallError):
            installer._validate_git_argument("--upload-pack=touch /tmp/pwned", "ref")

    def test_short_option_ref_is_refused(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._validate_git_argument("-c", "ref")

    def test_empty_value_is_refused(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._validate_git_argument("", "ref")

    def test_shell_metacharacters_are_refused(self) -> None:
        for value in ("main; rm -rf /", "main$(id)", "main|tee", "main`id`"):
            with self.subTest(value=value):
                with self.assertRaises(installer.InstallError):
                    installer._validate_git_argument(value, "ref")

    def test_ordinary_refs_and_paths_pass(self) -> None:
        for value in ("main", "v1.2.3", "release/2026-08", "skills/my-skill", "a_b.c"):
            with self.subTest(value=value):
                self.assertEqual(installer._validate_git_argument(value, "ref"), value)

    def test_sparse_checkout_refuses_option_like_ref(self) -> None:
        # The guard sits at the point argv is assembled, so the whole call is
        # refused before any subprocess starts.
        with self.assertRaises(installer.InstallError):
            installer._git_sparse_checkout(
                "https://github.com/o/r.git", "--upload-pack=id", ["skills/x"], "/tmp/x"
            )

    def test_sparse_checkout_refuses_option_like_path(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._git_sparse_checkout(
                "https://github.com/o/r.git", "main", ["--output=/etc/passwd"], "/tmp/x"
            )

    def test_sparse_checkout_refuses_option_like_repo_url(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._git_sparse_checkout("--upload-pack=id", "main", ["skills/x"], "/tmp/x")


class RepoSegmentGuardTest(unittest.TestCase):
    """An owner and a repo name are single path segments that get interpolated
    into both the clone URL and the codeload download URL. Checking the built
    URL's scheme constrained nothing about what those segments contained, so
    the segments themselves are what is checked."""

    def test_owner_with_separator_is_refused(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._validate_repo_segment("owner/../other", "owner")

    def test_dot_dot_is_refused(self) -> None:
        # `..` is a path traversal in the codeload URL, not a repo name.
        with self.assertRaises(installer.InstallError):
            installer._validate_repo_segment("..", "owner")

    def test_option_like_owner_is_refused(self) -> None:
        with self.assertRaises(installer.InstallError):
            installer._validate_repo_segment("-owner", "owner")

    def test_whitespace_in_repo_is_refused(self) -> None:
        for value in ("re po", "repo\nX", "repo\ty"):
            with self.subTest(value=value):
                with self.assertRaises(installer.InstallError):
                    installer._validate_repo_segment(value, "repo")

    def test_ordinary_owner_and_repo_pass(self) -> None:
        for value in ("LAF-US", "IDAHO-VAULT", "repo.js", "some_repo", "v2.0"):
            with self.subTest(value=value):
                self.assertEqual(installer._validate_repo_segment(value, "repo"), value)

    def test_built_urls_are_the_only_accepted_shapes(self) -> None:
        https = installer._build_repo_url("LAF-US", "IDAHO-VAULT")
        ssh = installer._build_repo_ssh("LAF-US", "IDAHO-VAULT")
        self.assertEqual(installer._validate_repo_url(https), https)
        self.assertEqual(installer._validate_repo_url(ssh), ssh)
        for bad in (
            "https://evil.example/LAF-US/IDAHO-VAULT.git",
            "https://github.com/LAF-US/IDAHO-VAULT",  # no .git suffix
            "ext::sh -c touch% /tmp/pwned",
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(installer.InstallError):
                    installer._validate_repo_url(bad)

    def test_source_construction_refuses_a_bad_owner(self) -> None:
        args = installer.Args(repo="--upload-pack=id/repo", path=["skills/x"])
        with self.assertRaises(installer.InstallError):
            installer._resolve_source(args)


class RunGitErrorContractTest(unittest.TestCase):
    """Every failure leaves _run_git as an InstallError. _git_sparse_checkout
    falls back from https to ssh by catching InstallError, so a failure that
    escapes as some other type skips the fallback and aborts the install."""

    def test_timeout_becomes_install_error(self) -> None:
        import subprocess
        with patch.object(
            installer.subprocess, "run",
            side_effect=subprocess.TimeoutExpired(cmd=["git"], timeout=300),
        ):
            with self.assertRaises(installer.InstallError) as exc:
                installer._run_git(["git", "clone", "--", "u", "d"])
        self.assertIn("timed out", str(exc.exception))

    def test_missing_git_becomes_install_error(self) -> None:
        with patch.object(
            installer.subprocess, "run", side_effect=FileNotFoundError("git")
        ):
            with self.assertRaises(installer.InstallError) as exc:
                installer._run_git(["git", "status"])
        self.assertIn("could not run", str(exc.exception))


class GithubRequestHostPinTest(unittest.TestCase):
    """github_request attaches GITHUB_TOKEN, so the URL decides where the
    credential goes; the destination is pinned where it is attached."""

    def setUp(self) -> None:
        import github_utils
        self.gu = github_utils

    def test_offsite_host_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            self.gu.github_request("https://evil.example/x", "test")

    def test_plaintext_scheme_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            self.gu.github_request("http://api.github.com/x", "test")


if __name__ == "__main__":
    unittest.main()
