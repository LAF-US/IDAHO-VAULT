from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module():
    script_path = PROJECT_ROOT / "!-resolve_openrouter_secret.py"
    spec = importlib.util.spec_from_file_location("resolve_openrouter_secret_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


resolver = _load_module()


class ResolveOutFileTest(unittest.TestCase):
    def test_default_stays_under_op_directory(self) -> None:
        repo_root = Path("/vault")
        out_file = resolver.resolve_out_file(repo_root, "")
        self.assertEqual(out_file, repo_root / ".op" / "openrouter.env")

    def test_relative_override_within_vault_is_allowed(self) -> None:
        repo_root = Path("/vault")
        out_file = resolver.resolve_out_file(repo_root, "custom/openrouter.env")
        self.assertEqual(out_file, repo_root / "custom" / "openrouter.env")

    def test_relative_traversal_outside_vault_is_rejected(self) -> None:
        repo_root = Path("/vault")
        with self.assertRaises(SystemExit) as exc:
            resolver.resolve_out_file(repo_root, "../../etc/passwd")
        self.assertIn("must stay inside the vault", str(exc.exception))

    def test_absolute_path_outside_vault_is_rejected(self) -> None:
        repo_root = Path("/vault")
        with self.assertRaises(SystemExit) as exc:
            resolver.resolve_out_file(repo_root, "/etc/passwd")
        self.assertIn("must stay inside the vault", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
