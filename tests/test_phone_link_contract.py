from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
import unittest.mock
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec for {module_name} at {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PhoneLinkContractTest(unittest.TestCase):
    def test_python_watcher_prefers_explicit_config_before_env_and_fallback(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_contract_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            explicit_root = Path(workspace) / "explicit-vault-root"
            explicit_root.mkdir()
            with unittest.mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": r"C:\ignored"}, clear=False):
                root, source = module.resolve_vault_root(explicit_root)

            self.assertEqual(root, explicit_root.resolve())
            self.assertEqual(source, "argument")

    def test_python_watcher_uses_env_vault_root_when_no_argument_is_supplied(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_contract_test_module_env",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            env_root = Path(workspace) / "env-vault-root"
            env_root.mkdir()
            with unittest.mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": str(env_root)}, clear=False):
                root, source = module.resolve_vault_root()

            self.assertEqual(root, env_root.resolve())
            self.assertEqual(source, "IDAHO_VAULT_ROOT")

    def test_python_watcher_rejects_missing_configured_vault_root(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_missing_root_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            missing_root = Path(workspace) / "missing-vault-root"

            with self.assertRaisesRegex(RuntimeError, "Vault root does not exist"):
                module.resolve_vault_root(missing_root)

    def test_launcher_uses_python_not_powershell(self) -> None:
        launcher = (PROJECT_ROOT / "START-PHONE-LINK-SWEEP.cmd").read_text(encoding="utf-8")
        vbs = (PROJECT_ROOT / "phone-link-sweep-launcher.vbs").read_text(encoding="utf-8")

        self.assertIn("phone_link_auto_sweep.py", launcher)
        self.assertIn("python", launcher.lower())
        self.assertIn("%~dp0", launcher)
        self.assertNotIn("powershell", launcher.lower())
        self.assertIn("WScript.ScriptFullName", vbs)
        self.assertNotIn("powershell", vbs.lower())
        self.assertNotIn(r"C:\Users\loganf\Documents\IDAHO-VAULT", vbs)

    def test_legacy_powershell_wrapper_delegates_to_python(self) -> None:
        wrapper = (PROJECT_ROOT / "phone-link-auto-sweep.ps1").read_text(encoding="utf-8")

        self.assertIn("phone_link_auto_sweep.py", wrapper)
        self.assertIn("python", wrapper.lower())
        self.assertIn("--source", wrapper)
        self.assertIn("--vault-root", wrapper)
        self.assertNotIn(r"C:\Users\loganf\Documents\IDAHO-VAULT", wrapper)

    def test_python_intake_prefers_explicit_vault_root_argument(self) -> None:
        module = _load_module(
            "phone_link_intake_contract_test_module",
            ".github/scripts/phone_link_intake.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            explicit_root = Path(workspace) / "explicit-vault-root"
            explicit_root.mkdir()
            with unittest.mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": r"C:\ignored"}, clear=False):
                self.assertEqual(module.get_vault_root(explicit_root), explicit_root.resolve())

    def test_python_intake_uses_env_vault_root_when_no_argument_is_supplied(self) -> None:
        module = _load_module(
            "phone_link_intake_contract_test_module_env",
            ".github/scripts/phone_link_intake.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            env_root = Path(workspace) / "env-vault-root"
            env_root.mkdir()
            with unittest.mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": str(env_root)}, clear=False):
                self.assertEqual(module.get_vault_root(), env_root.resolve())

    def test_python_intake_rejects_missing_configured_vault_root(self) -> None:
        module = _load_module(
            "phone_link_intake_missing_root_test_module",
            ".github/scripts/phone_link_intake.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            missing_root = Path(workspace) / "missing-intake-vault-root"

            with self.assertRaisesRegex(RuntimeError, "Vault root does not exist"):
                module.get_vault_root(missing_root)

    def test_python_watcher_moves_file_once_into_vault_root(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_behavior_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            root = Path(workspace)
            source = root / "source"
            vault = root / "vault"
            log = vault / "!" / "INBOX" / "_phone-link-watcher.log"
            source.mkdir()
            incoming = source / "sample.txt"
            incoming.write_text("phone link sample", encoding="utf-8")

            moved = module.sweep_once(source, vault, log)

            self.assertEqual(moved, 1)
            self.assertFalse(incoming.exists())
            self.assertEqual((vault / "sample.txt").read_text(encoding="utf-8"), "phone link sample")
            self.assertIn("MOVED (direct): sample.txt", log.read_text(encoding="utf-8"))

    def test_python_watcher_skips_identical_duplicate_without_deleting_source(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_duplicate_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            root = Path(workspace)
            source = root / "source"
            vault = root / "vault"
            log = vault / "!" / "INBOX" / "_phone-link-watcher.log"
            source.mkdir()
            vault.mkdir()
            (source / "sample.txt").write_text("same", encoding="utf-8")
            (vault / "sample.txt").write_text("same", encoding="utf-8")

            moved = module.sweep_once(source, vault, log)

            self.assertEqual(moved, 0)
            self.assertTrue((source / "sample.txt").exists())
            self.assertEqual((vault / "sample.txt").read_text(encoding="utf-8"), "same")
            self.assertIn("SKIP (duplicate): sample.txt", log.read_text(encoding="utf-8"))

    def test_python_watcher_suffixes_name_collision(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_collision_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            root = Path(workspace)
            source = root / "source"
            vault = root / "vault"
            log = vault / "!" / "INBOX" / "_phone-link-watcher.log"
            source.mkdir()
            vault.mkdir()
            (source / "sample.txt").write_text("incoming", encoding="utf-8")
            (vault / "sample.txt").write_text("existing", encoding="utf-8")

            moved = module.sweep_once(source, vault, log)

            self.assertEqual(moved, 1)
            self.assertEqual((vault / "sample.txt").read_text(encoding="utf-8"), "existing")
            collisions = sorted(vault.glob("sample-*.txt"))
            self.assertEqual(len(collisions), 1)
            self.assertEqual(collisions[0].read_text(encoding="utf-8"), "incoming")
            self.assertIn("MOVED (collision): sample.txt", log.read_text(encoding="utf-8"))

    def test_python_watcher_creates_default_source_only_when_omitted(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_default_source_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            root = Path(workspace)
            vault_root = root / "vault"
            vault_root.mkdir()
            default_source = root / "default-source"

            with unittest.mock.patch.object(module, "DEFAULT_SOURCE", default_source):
                exit_code = module.main(["--vault-root", str(vault_root), "--once"])

            self.assertEqual(exit_code, 0)
            self.assertTrue(default_source.is_dir())

    def test_python_watcher_does_not_create_explicit_missing_source(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_explicit_source_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as workspace:
            root = Path(workspace)
            vault_root = root / "vault"
            vault_root.mkdir()
            explicit_source = root / "explicit-source-does-not-exist"

            exit_code = module.main(
                ["--vault-root", str(vault_root), "--source", str(explicit_source), "--once"]
            )

            self.assertEqual(exit_code, 1)
            self.assertFalse(explicit_source.exists())


if __name__ == "__main__":
    unittest.main()
