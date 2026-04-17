from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


def _load_topology_census_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "topology_census.py"
    spec = importlib.util.spec_from_file_location("topology_census_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


topology_census = _load_topology_census_module()


class TopologyCensusTest(unittest.TestCase):
    def setUp(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        self.tempdir = project_root / "tests" / "_tmp_topology_census_case"
        shutil.rmtree(self.tempdir, ignore_errors=True)
        self.root = self.tempdir / "vault"
        self.root.mkdir(parents=True, exist_ok=True)
        self.output_dir = self.root / "!"
        subprocess.run(["git", "init"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Topology Census Test"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )
        self._write_fixture()

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def _write(self, relpath: str, content: str) -> None:
        path = self.root / Path(relpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _write_fixture(self) -> None:
        self._write(
            ".gitignore",
            "\n".join(
                [
                    "_private/",
                    "_private/**",
                    "@/",
                    "@/**",
                    "",
                ]
            ),
        )
        self._write("CONSTITUTION.md", "# Constitution\n\n`INBOX/` is a named surface.\n")
        self._write(
            "VAULT-CONVENTIONS.md",
            "\n".join(
                [
                    "# Vault Conventions",
                    "",
                    "Treat `!/` as the Swarmic Nest.",
                    "Treat `.*` dotfolders as individual agent space.",
                    "Each agent keeps `.dotfolder/MEMORY/` as a tracked memory surface.",
                    "",
                ]
            ),
        )
        self._write("!/WAKEUP.md", "# Wakeup\n\nRead `!/README.md`.\n")
        self._write(
            "!/README.md",
            "\n".join(
                [
                    "# Nest README",
                    "",
                    "Read `INBOX/README.md` and `!/INBOX/README.md` for intake work.",
                    "Read `!/AGENTS.md` for the live roster.",
                    "",
                ]
            ),
        )
        self._write(
            "!/AGENTS.md",
            "\n".join(
                [
                    "# Agents",
                    "",
                    "## Direct-Write Agents (Autoloaded)",
                    "",
                    "| Agent | Persona | Vendor | Tier | Dotfolder | Git Suffix |",
                    "| --- | --- | --- | --- | --- | --- |",
                    "| OpenAI Codex | **The Lexicographer** | OpenAI | Scripting | .codex/ | -X |",
                    "",
                    "## Advisory & Specialized Agents",
                    "",
                    "| Agent | Persona | Vendor | Role | Dotfolder |",
                    "| --- | --- | --- | --- | --- |",
                    "| Bartimaeus | **The Cartographer** | - | Crawler | .bartimaeus/ |",
                    "",
                    "## Narrative Recovery Layer",
                    "",
                    "Historical aliases still include `.shade/` as a preserved chamber.",
                    "",
                ]
            ),
        )
        self._write(
            "INBOX/README.md",
            "# INBOX\n\nAutomation and protocol live in `!/INBOX/`.\n",
        )
        self._write(
            "!/INBOX/README.md",
            "# !/INBOX\n\nThis folder holds the protocol face; the file-drop face lives at root `INBOX/`.\n",
        )
        self._write(
            "!/CREWAI/README.md",
            "# !/CREWAI\n\nThis directory is the live staging surface. It also preserves historical harbor records.\n",
        )
        self._write("!/swarm/README.md", "# !/swarm\n\nActive state room.\n")
        self._write("!/swarm 1/state/stabilization_plan.md", "# swarm 1\n\n- swarm/state/run_state.md\n")
        self._write("!/swarm 1/tools/state_manager.py", "print('state manager')\n")
        self._write(".codex/CODEX.md", "# CODEX\n")
        self._write(".codex/MEMORY/anchor.md", "# memory\n")
        self._write(".bartimaeus/README.md", "# Bartimaeus\n")
        self._write(".shade/archive.md", "# shade archive\n")
        self._write("2026/04/2026-04-17.md", "# daily note\n")
        self._write("INBOX/AI-CAPTURES/sample.md", "# capture\n")
        self._write("INBOX/PHONE-LINK/phone.txt", "hello\n")
        self._write("_private/notes.md", "# private\n")
        self._write("@/tweets/thread.md", "# tweet\n")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True, capture_output=True)
        # Keep ignored creatures local-only.
        subprocess.run(["git", "reset", "--", "_private", "@"], cwd=self.root, check=True, capture_output=True)

    def test_root_scope_counts_ignored_and_tracked_folders_without_move_commands(self) -> None:
        report = topology_census.build_scope_report(self.root, "root")
        entries = {entry["path"]: entry for entry in report["entries"]}

        self.assertIn("INBOX", entries)
        self.assertIn("_private", entries)
        self.assertIn("@", entries)
        self.assertTrue(entries["INBOX"]["appears_in_live_doctrine"])
        self.assertEqual(entries["INBOX"]["authority_state"], "explicit_live_authority")
        self.assertTrue(entries["_private"]["git_state"]["ignored"])
        self.assertEqual(entries["_private"]["obvious_authority"], "ignore rules only")

        rendered = topology_census.render_scope_markdown(report)
        self.assertNotIn("git mv", rendered)
        self.assertNotIn("move_to_", rendered)

    def test_dotfolder_scope_reports_roster_recovery_and_memory(self) -> None:
        report = topology_census.build_scope_report(self.root, "dotfolders")
        entries = {entry["path"]: entry for entry in report["entries"]}

        self.assertIn(".codex", entries)
        self.assertIn(".shade", entries)
        self.assertTrue(entries[".codex"]["live_roster"])
        self.assertTrue(entries[".codex"]["memory_state"]["memory_dir_tracked"])
        self.assertFalse(entries[".shade"]["live_roster"])
        self.assertTrue(entries[".shade"]["historical_recovery"])

    def test_nest_scope_recurses_and_surfaces_duplicate_internal_systems(self) -> None:
        report = topology_census.build_scope_report(self.root, "nest")
        entries = {entry["path"]: entry for entry in report["entries"]}

        self.assertIn("!/INBOX", entries)
        self.assertIn("!/swarm", entries)
        self.assertIn("!/swarm 1", entries)
        self.assertEqual(entries["!/swarm"]["room_status"], "ambiguous")
        self.assertEqual(entries["!/swarm 1"]["room_status"], "ambiguous")
        self.assertIn("!/swarm 1", entries["!/swarm"]["duplicate_conflicts"])
        self.assertEqual(
            entries["!/INBOX"]["local_governing_surface"]["path"],
            "!/INBOX/README.md",
        )

    def test_write_scope_reports_creates_scope_artifacts_and_index(self) -> None:
        result = topology_census.write_scope_reports(
            root=self.root,
            output_dir=self.output_dir,
            scopes=["root", "dotfolders", "nest"],
        )

        self.assertEqual(len(result["generated"]), 3)
        index_path = self.root / result["index"]
        self.assertTrue(index_path.exists())
        index_text = index_path.read_text(encoding="utf-8")
        self.assertIn("`root`", index_text)
        self.assertIn("`dotfolders`", index_text)
        self.assertIn("`nest`", index_text)

        for row in result["generated"]:
            markdown_path = self.root / row["markdown"]
            json_path = self.root / row["json"]
            self.assertTrue(markdown_path.exists())
            self.assertTrue(json_path.exists())
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["scope"], row["scope"])


if __name__ == "__main__":
    unittest.main()
