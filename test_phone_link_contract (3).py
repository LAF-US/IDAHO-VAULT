from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_module(module_name: str, relative_path: str):
    script_path = PROJECT_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PhoneLinkContractTest(unittest.TestCase):
    def test_python_watcher_prefers_explicit_config_before_env_and_fallback(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_contract_test_module",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(prefix="phone_link_vault_") as vault_dir:
            with mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": r"C:\ignored"}, clear=False):
                root, source = module.resolve_vault_root(Path(vault_dir))

        self.assertEqual(root, Path(vault_dir).resolve())
        self.assertEqual(source, "argument")

    def test_python_watcher_uses_env_vault_root_when_no_argument_is_supplied(self) -> None:
        module = _load_module(
            "phone_link_auto_sweep_contract_test_module_env",
            ".github/scripts/phone_link_auto_sweep.py",
        )

        with tempfile.TemporaryDirectory(prefix="phone_link_vault_") as vault_dir:
            with mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": vault_dir}, clear=False):
                root, source = module.resolve_vault_root()

        self.assertEqual(root, Path(vault_dir).resolve())
        self.assertEqual(source, "IDAHO_VAULT_ROOT")

    def test_launcher_uses_python_not_powershell(self) -> None:
        launcher = (PROJECT_ROOT / "START-PHONE-LINK-SWEEP.cmd").read_text(encoding="utf-8")
        vbs = (PROJECT_ROOT / "phone-link-sweep-launcher.vbs").read_text(encoding="utf-8")

        self.assertIn("phone_link_auto_sweep.py", launcher)
        self.assertIn("python", launcher.lower())
        self.assertNotIn("powershell", launcher.lower())
        self.assertIn("WScript.ScriptFullName", vbs)
        self.assertNotIn("powershell", vbs.lower())
        self.assertNotIn("C:\\Users\\loganf\\Documents\\IDAHO-VAULT", vbs)

    def test_python_intake_prefers_explicit_vault_root_argument(self) -> None:
        module = _load_module(
            "phone_link_intake_contract_test_module",
            ".github/scripts/phone_link_intake.py",
        )

        with tempfile.TemporaryDirectory(prefix="phone_link_vault_") as vault_dir:
            with mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": r"C:\ignored"}, clear=False):
                self.assertEqual(module.get_vault_root(Path(vault_dir)), Path(vault_dir).resolve())

    def test_python_intake_uses_env_vault_root_when_no_argument_is_supplied(self) -> None:
        module = _load_module(
            "phone_link_intake_contract_test_module_env",
            ".github/scripts/phone_link_intake.py",
        )

        with tempfile.TemporaryDirectory(prefix="phone_link_vault_") as vault_dir:
            with mock.patch.dict(os.environ, {"IDAHO_VAULT_ROOT": vault_dir}, clear=False):
                self.assertEqual(module.get_vault_root(), Path(vault_dir).resolve())


if __name__ == "__main__":
    unittest.main()
