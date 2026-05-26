from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SecuritySurfaceQuarantineTest(unittest.TestCase):
    def test_discord_and_gateway_configuration_contains_references_only(self) -> None:
        config = json.loads((ROOT / ".openclaw" / "openclaw-live-ref.json").read_text(encoding="utf-8"))
        self.assertTrue(config["channels"]["discord"]["enabled"])
        self.assertTrue(config["channels"]["discord"]["token"].startswith("env:"))
        self.assertTrue(config["gateway"]["auth"]["token"].startswith("env:"))

    def test_persistent_discord_token_helpers_are_removed(self) -> None:
        self.assertFalse((ROOT / ".op" / "DISCORD-TOKEN-SETUP.md").exists())
        self.assertFalse((ROOT / ".op" / "fetch-discord-token.ps1").exists())
        setup = (ROOT / ".openclaw" / "DISCORD-SETUP.md").read_text(encoding="utf-8")
        self.assertNotIn('SetEnvironmentVariable("DISCORD_OPENCLAW_TOKEN"', setup)
        self.assertIn("Remove-Item Env:DISCORD_OPENCLAW_TOKEN", setup)

    def test_vault_specific_sbp_execution_surfaces_are_quarantined(self) -> None:
        for relative_path in (
            "scripts/vault-pheromones.py",
            "scripts-vault-pheromones.py",
            "scripts-vault-dispatch.sh",
            "scripts-vault-openclaw-bridge.sh",
            "scripts-vault-pre-exec-hook.sh",
            "!/sbp-blackboard.json",
            "!-sbp-blackboard.json",
        ):
            self.assertFalse((ROOT / relative_path).exists(), relative_path)
        reference = (ROOT / "SBP.md").read_text(encoding="utf-8")
        self.assertIn("AdviceNXT/sbp", reference)
        self.assertIn("quarantined", reference)


if __name__ == "__main__":
    unittest.main()
