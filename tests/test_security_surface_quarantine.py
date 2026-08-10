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

    def test_unreviewed_bridge_session_and_launcher_surfaces_are_quarantined(self) -> None:
        for relative_path in (
            ".mcp.json",
            ".openclaw/gateway.cmd",
            "2026-05-13-135349-this-session-is-being-cont-abhorsen-and-judge-on-the-road.txt",
            "gpg-agent.conf",
            "package copy.json",
            "package-lock copy.json",
            "session-export-1779427275139",
        ):
            self.assertFalse((ROOT / relative_path).exists(), relative_path)
        # This test used to also assert three literal patterns were present in
        # .gitignore. That was a substring grep on a config file — the same
        # species as the retired bootstrap-contract token checks — and it
        # enforced the pre-2026-08-03 .gitignore against Logan's deliberate cut.
        # The quarantine question this test answers is the existence check
        # above: the removed surfaces must not return to the tree.

    def test_platform_metadata_remains_os_neutral(self) -> None:
        metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertNotIn("HOST: macOS", metadata)
        self.assertNotIn('requires-python = ">=3.11,<3.12"', metadata)

    def test_openclaw_operation_guidance_is_containment_gated(self) -> None:
        guidance = (ROOT / ".openclaw" / "SECRETS-1PASSWORD.md").read_text(encoding="utf-8")
        self.assertIn("OpenClaw is not project startup", guidance)
        self.assertNotIn("source .openclaw/.env.local", guidance)
        self.assertNotIn("DISCORD_BOT_TOKEN", guidance)


if __name__ == "__main__":
    unittest.main()
