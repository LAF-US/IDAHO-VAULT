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
    def test_watcher_prefers_explicit_contract_before_legacy_fallback(self) -> None:
        script = (PROJECT_ROOT / "phone-link-auto-sweep.ps1").read_text(encoding="utf-8")

        self.assertIn("IDAHO_VAULT_ROOT", script)
        self.assertIn("legacy fallback", script)
        self.assertIn("VaultRootSource", script)
        self.assertLess(script.index("ExplicitVaultDir"), script.index("IDAHO_VAULT_ROOT"))
        self.assertLess(script.index("IDAHO_VAULT_ROOT"), script.index("legacyVaultDir"))

    def test_vbs_launcher_resolves_sweeper_relative_to_itself(self) -> None:
        launcher = (PROJECT_ROOT / "phone-link-sweep-launcher.vbs").read_text(encoding="utf-8")

        self.assertIn("WScript.ScriptFullName", launcher)
        self.assertIn("BuildPath", launcher)
        self.assertNotIn("C:\\Users\\loganf\\Documents\\IDAHO-VAULT", launcher)

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
