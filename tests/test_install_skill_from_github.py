from __future__ import annotations

import importlib.util
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    script_dir = (
        PROJECT_ROOT
        / ".codex"
        / "skills"
        / ".system"
        / "skill-installer"
        / "scripts"
    )
    script_path = script_dir / "install-skill-from-github.py"
    # The script does `from github_utils import ...`, a sibling module it
    # expects on sys.path when run from its own directory in production.
    sys.path.insert(0, str(script_dir))
    try:
        spec = importlib.util.spec_from_file_location("install_skill_from_github_test_module", script_path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(script_dir))


installer = _load_module()


class GitSparseCheckoutArgvSafetyTest(unittest.TestCase):
    """--ref and --path are user-controlled (CLI flags); a bare trailing
    positional argument to `checkout`/`sparse-checkout set` lets a
    dash-prefixed value be parsed as a git option instead of a literal
    revision/pathspec. Every call must guard its untrusted trailing argument
    with a `--` separator (or, where `checkout`'s own revision/pathspec
    ambiguity makes `--` unsafe, use `switch --detach --` instead)."""

    def _run(self, ok_returncode: int = 0):
        return types.SimpleNamespace(returncode=ok_returncode, stdout="", stderr="")

    def test_sparse_checkout_set_guards_paths_with_double_dash(self) -> None:
        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            return self._run()

        with patch.object(installer.subprocess, "run", side_effect=fake_run):
            installer._git_sparse_checkout("https://example.invalid/o/r.git", "main", ["--evil"], "dest-dir")

        sparse_call = next(c for c in calls if "sparse-checkout" in c)
        set_index = sparse_call.index("set")
        self.assertEqual(sparse_call[set_index + 1], "--")
        self.assertIn("--evil", sparse_call[set_index + 2:])

    def test_ref_checkout_uses_switch_detach_double_dash_not_bare_checkout(self) -> None:
        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            return self._run()

        with patch.object(installer.subprocess, "run", side_effect=fake_run):
            installer._git_sparse_checkout("https://example.invalid/o/r.git", "--force", ["skills/foo"], "dest-dir")

        # No call may hand `ref` to `checkout` as a bare trailing positional --
        # that is the exact pattern that let a value like "--force" be
        # interpreted as a git option instead of a revision.
        for call in calls:
            if "checkout" in call and "sparse-checkout" not in call:
                self.fail(f"unsafe bare 'checkout <ref>' call still present: {call}")

        switch_call = next(c for c in calls if "switch" in c)
        self.assertIn("--detach", switch_call)
        dash_index = switch_call.index("--", switch_call.index("switch"))
        self.assertEqual(switch_call[dash_index + 1], "--force")

    def test_real_git_rejects_dash_prefixed_ref_instead_of_treating_it_as_an_option(self) -> None:
        """End-to-end proof against the real git binary (not just argv shape):
        a malicious --ref value must fail loudly as an invalid reference,
        never silently succeed as a reinterpreted flag."""
        if not installer.shutil.which("git"):
            self.skipTest("git not available")
        result = subprocess.run(
            ["git", "switch", "--detach", "--", "--force"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid reference", (result.stdout + result.stderr).lower())


if __name__ == "__main__":
    unittest.main()
