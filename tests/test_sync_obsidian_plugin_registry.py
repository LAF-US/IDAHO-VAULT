"""Regression coverage for #514: an untracked/gitignored local plugin
manifest present only in this checkout must never leak into the generated
registry, and a linked worktree of the same commit must produce identical
output to the main checkout.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Resolved once to an absolute path, matching this repo's tests/test_git_guardrails.py
# convention, rather than the bare string "git".
GIT_BIN = shutil.which("git") or "git"


def _load_module(module_name: str, relative_path: str):
    """Load a `.github/scripts/*.py` module by file path, per this repo's tests/ convention."""
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load spec for {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sync_registry = _load_module(
    "sync_obsidian_plugin_registry_test_module",
    ".github/scripts/sync_obsidian_plugin_registry.py",
)


def _run_git(cwd: Path, *args: str) -> None:
    """Run a git subcommand in `cwd`, raising on failure."""
    subprocess.run([GIT_BIN, *args], cwd=cwd, check=True, capture_output=True, text=True)


class TrackedPluginManifestsTest(unittest.TestCase):
    """Real temp-git-repo coverage for #514: tracked vs. untracked plugin manifests."""

    def setUp(self):
        """Build a real git repo with one tracked and one untracked plugin manifest."""
        self._tmpdir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self._tmpdir.name)

        _run_git(self.repo_root, "init", "-q")
        _run_git(self.repo_root, "config", "user.email", "test@example.invalid")
        _run_git(self.repo_root, "config", "user.name", "Test")

        obsidian_dir = self.repo_root / ".obsidian"
        plugin_dir = obsidian_dir / "plugins"

        tracked_dir = plugin_dir / "tracked-plugin"
        tracked_dir.mkdir(parents=True)
        (tracked_dir / "manifest.json").write_text(
            '{"id": "tracked-plugin", "name": "Tracked Plugin", "version": "1.0.0"}\n',
            encoding="utf-8",
        )
        _run_git(self.repo_root, "add", ".obsidian/plugins/tracked-plugin/manifest.json")
        _run_git(self.repo_root, "commit", "-q", "-m", "add tracked plugin manifest")

        # Simulates a gitignored plugin directory (e.g. obsidianclaw) that only
        # exists on this particular workstation/worktree and was never staged.
        untracked_dir = plugin_dir / "untracked-local-plugin"
        untracked_dir.mkdir(parents=True)
        (untracked_dir / "manifest.json").write_text(
            '{"id": "untracked-local-plugin", "name": "Untracked", "version": "9.9.9"}\n',
            encoding="utf-8",
        )

        self._orig = {
            name: getattr(sync_registry, name)
            for name in (
                "REPO_ROOT",
                "OBSIDIAN_DIR",
                "COMMUNITY_CONFIG",
                "CORE_CONFIG",
                "PLUGIN_DIR",
                "MANIFEST_PATH",
                "SWARM_PATH",
            )
        }
        sync_registry.REPO_ROOT = self.repo_root
        sync_registry.OBSIDIAN_DIR = obsidian_dir
        sync_registry.COMMUNITY_CONFIG = obsidian_dir / "community-plugins.json"
        sync_registry.CORE_CONFIG = obsidian_dir / "core-plugins.json"
        sync_registry.PLUGIN_DIR = plugin_dir
        sync_registry.MANIFEST_PATH = self.repo_root / "manifest.json"
        sync_registry.SWARM_PATH = self.repo_root / "swarm.json"

    def tearDown(self):
        """Restore the module's real repo-path constants and remove the temp repo."""
        for name, value in self._orig.items():
            setattr(sync_registry, name, value)
        self._tmpdir.cleanup()

    def test_untracked_local_plugin_is_excluded(self):
        """A manifest present on disk but not `git add`-ed must not be enumerated."""
        installed = sync_registry.read_plugin_manifests()
        self.assertIn("tracked-plugin", installed)
        self.assertNotIn("untracked-local-plugin", installed)

    def test_build_state_counts_only_tracked_plugins(self):
        """Generated counts/lists must reflect only the tracked manifest."""
        state = sync_registry.build_state()
        self.assertEqual(state["current_state"]["installed_community_count"], 1)
        self.assertEqual(
            [p["id"] for p in state["installed_community_plugins"]],
            ["tracked-plugin"],
        )

    def test_linked_worktree_produces_identical_output(self):
        """A linked worktree of the same commit must generate byte-identical output."""
        # A linked worktree of the same commit has no working-tree-only
        # untracked files unless something is copied in manually -- simulate
        # that by pointing a second "checkout" at a fresh directory containing
        # only the tracked manifest (no untracked-local-plugin dir at all).
        main_state = sync_registry.build_state()

        with tempfile.TemporaryDirectory() as worktree_dir:
            worktree_root = Path(worktree_dir)
            _run_git(
                self.repo_root,
                "worktree",
                "add",
                "--detach",
                str(worktree_root),
                "HEAD",
            )
            try:
                sync_registry.REPO_ROOT = worktree_root
                sync_registry.OBSIDIAN_DIR = worktree_root / ".obsidian"
                sync_registry.COMMUNITY_CONFIG = sync_registry.OBSIDIAN_DIR / "community-plugins.json"
                sync_registry.CORE_CONFIG = sync_registry.OBSIDIAN_DIR / "core-plugins.json"
                sync_registry.PLUGIN_DIR = sync_registry.OBSIDIAN_DIR / "plugins"
                sync_registry.MANIFEST_PATH = worktree_root / "manifest.json"
                sync_registry.SWARM_PATH = worktree_root / "swarm.json"

                worktree_state = sync_registry.build_state()
            finally:
                _run_git(self.repo_root, "worktree", "remove", "--force", str(worktree_root))

        self.assertEqual(
            main_state["current_state"],
            worktree_state["current_state"],
        )
        self.assertEqual(
            main_state["installed_community_plugins"],
            worktree_state["installed_community_plugins"],
        )


if __name__ == "__main__":
    unittest.main()
