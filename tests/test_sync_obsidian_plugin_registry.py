"""Regression coverage for #514: untracked local plugins must not leak in.

An untracked/gitignored local plugin manifest present only in this checkout
must never appear in the generated registry, and a linked worktree of the
same commit must produce identical output to the main checkout.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

import pygit2


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


def _init_repo_with_commit(repo_root: Path, relative_file: str, content: str) -> pygit2.Repository:
    """Init a repo at `repo_root`, commit one tracked file, return the pygit2.Repository."""
    repo = pygit2.init_repository(str(repo_root))
    repo.config["user.email"] = "test@example.invalid"
    repo.config["user.name"] = "Test"

    file_path = repo_root / relative_file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    index = repo.index
    index.add(relative_file)
    index.write()
    tree = index.write_tree()
    author = pygit2.Signature("Test", "test@example.invalid")
    repo.create_commit("HEAD", author, author, "add tracked plugin manifest", tree, [])
    return repo


class TrackedPluginManifestsTest(unittest.TestCase):
    """Real temp-git-repo coverage for #514: tracked vs. untracked plugin manifests."""

    def setUp(self):
        """Build a real git repo with one tracked and one untracked plugin manifest."""
        self._tmpdir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self._tmpdir.name)

        self.repo = _init_repo_with_commit(
            self.repo_root,
            ".obsidian/plugins/tracked-plugin/manifest.json",
            '{"id": "tracked-plugin", "name": "Tracked Plugin", "version": "1.0.0"}\n',
        )

        obsidian_dir = self.repo_root / ".obsidian"
        plugin_dir = obsidian_dir / "plugins"

        # Simulates a gitignored plugin directory (e.g. obsidianclaw) that only
        # exists on this particular workstation/worktree and was never staged.
        untracked_dir = plugin_dir / "untracked-local-plugin"
        untracked_dir.mkdir(parents=True)
        (untracked_dir / "manifest.json").write_text(
            '{"id": "untracked-local-plugin", "name": "Untracked", "version": "9.9.9"}\n',
            encoding="utf-8",
        )

        patcher = unittest.mock.patch.multiple(
            sync_registry,
            REPO_ROOT=self.repo_root,
            OBSIDIAN_DIR=obsidian_dir,
            COMMUNITY_CONFIG=obsidian_dir / "community-plugins.json",
            CORE_CONFIG=obsidian_dir / "core-plugins.json",
            PLUGIN_DIR=plugin_dir,
            MANIFEST_PATH=self.repo_root / "manifest.json",
            SWARM_PATH=self.repo_root / "swarm.json",
        )
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._tmpdir.cleanup)

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
            worktree_root = Path(worktree_dir) / "wt"
            worktree = self.repo.add_worktree("linked-worktree-test", str(worktree_root))
            worktree_obsidian_dir = worktree_root / ".obsidian"
            try:
                with unittest.mock.patch.multiple(
                    sync_registry,
                    REPO_ROOT=worktree_root,
                    OBSIDIAN_DIR=worktree_obsidian_dir,
                    COMMUNITY_CONFIG=worktree_obsidian_dir / "community-plugins.json",
                    CORE_CONFIG=worktree_obsidian_dir / "core-plugins.json",
                    PLUGIN_DIR=worktree_obsidian_dir / "plugins",
                    MANIFEST_PATH=worktree_root / "manifest.json",
                    SWARM_PATH=worktree_root / "swarm.json",
                ):
                    worktree_state = sync_registry.build_state()
            finally:
                worktree.prune(True)

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
