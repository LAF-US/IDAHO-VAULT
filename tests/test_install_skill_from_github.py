from __future__ import annotations

import importlib.util
import sys
import unittest
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
