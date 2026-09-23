from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LiveStartupContractTest(unittest.TestCase):
    def test_live_orientation_has_no_launcher_requirement(self) -> None:
        paths = [
            ROOT / "AGENTS.md",
            ROOT / "!" / "WAKEUP.md",
            ROOT / "!" / "AGENTS.md",
            ROOT / ".claude" / "CLAUDE.md",
        ]
        text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        self.assertNotIn("start_SPARKSEED", text)
        self.assertNotIn("`!/agent.sh`", text)
        self.assertNotIn("requires Git Bash", text)

    def test_retired_local_launcher_paths_are_absent(self) -> None:
        for path in (
            "agent.sh",
            "!/agent.sh",
            "start_SPARKSEED.sh",
            "start_SPARKSEED.cmd",
            "start_SPARKSEED.py",
            "src/idaho_vault/sparkseed.py",
        ):
            self.assertFalse((ROOT / path).exists(), path)

    def test_generated_index_is_discovery_only(self) -> None:
        payload = json.loads((ROOT / "!" / "agents.json").read_text(encoding="utf-8"))
        serialized = json.dumps(payload)
        self.assertEqual(payload["purpose"], "discovery_index")
        self.assertNotIn("bootstrap_entrypoint", serialized)
        self.assertNotIn("agent.sh", serialized)

    def test_agent_registry_contains_no_present_liveness_or_occupancy_fields(self) -> None:
        payload = json.loads((ROOT / "swarm.json").read_text(encoding="utf-8"))
        prohibited = {"office", "title", "status", "launched", "installed"}

        for agent in payload["agents"]:
            self.assertFalse(prohibited.intersection(agent), agent["id"])
            for observation in agent.get("observations", []):
                self.assertIn("kind", observation)
                self.assertIn("date", observation)
                self.assertIn("source_commit", observation)

    def test_codex_voice_registry_disclaims_present_population(self) -> None:
        text = (ROOT / "!" / "CODEX-VOICE-REGISTRY-2026-05-18.md").read_text(encoding="utf-8")
        self.assertIn("not a population register", text)
        self.assertNotIn("| Status |", text)
        self.assertNotIn("| Active |", text)


if __name__ == "__main__":
    unittest.main()
