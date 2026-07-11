from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / ".codex" / "skills" / ".system" / "skill-installer" / "scripts"


def load_installer():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(
        "install_skill_from_github", SCRIPT_DIR / "install-skill-from-github.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load install-skill-from-github.py")
    module = importlib.util.module_from_spec(spec)
    # Register before exec: the script's dataclasses resolve string
    # annotations (from __future__ import annotations) via
    # sys.modules[cls.__module__], which requires the module to already
    # be registered under its own name before exec_module runs.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ValidateOwnerRepoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.installer = load_installer()

    def test_accepts_ordinary_owner_and_repo(self) -> None:
        self.installer._validate_owner_repo("LAF-US", "IDAHO-VAULT")

    def test_rejects_owner_shaped_like_a_git_option(self) -> None:
        with self.assertRaisesRegex(self.installer.InstallError, "Invalid owner"):
            self.installer._validate_owner_repo("--upload-pack=touch pwned", "repo")

    def test_rejects_repo_shaped_like_a_git_option(self) -> None:
        with self.assertRaisesRegex(self.installer.InstallError, "Invalid repo"):
            self.installer._validate_owner_repo("owner", "--upload-pack=touch pwned")

    def test_rejects_empty_values(self) -> None:
        with self.assertRaises(self.installer.InstallError):
            self.installer._validate_owner_repo("", "repo")
        with self.assertRaises(self.installer.InstallError):
            self.installer._validate_owner_repo("owner", "")

    def test_rejects_parent_traversal(self) -> None:
        with self.assertRaises(self.installer.InstallError):
            self.installer._validate_owner_repo("owner", "..")


if __name__ == "__main__":
    unittest.main()
