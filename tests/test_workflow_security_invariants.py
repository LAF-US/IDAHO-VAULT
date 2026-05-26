from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


class WorkflowSecurityInvariantsTest(unittest.TestCase):
    def test_agent_ref_is_passed_as_environment_data(self) -> None:
        workflow = (WORKFLOWS / "agent-auto-pr.yml").read_text(encoding="utf-8")
        gate_script = workflow.split("- name: Gate on supported branch events", 1)[1].split(
            "- name: Checkout repo", 1
        )[0]
        self.assertIn("EVENT_REF: ${{ github.event.ref }}", gate_script)
        self.assertIn('BRANCH_NAME="$EVENT_REF"', gate_script)
        self.assertNotIn('BRANCH_NAME="${{ github.event.ref }}"', gate_script)
        self.assertIn('[[ "$BRANCH_NAME" =~ ^[A-Za-z0-9._/-]+$ ]]', gate_script)

    def test_scheduled_mutations_open_prs_instead_of_pushing_main(self) -> None:
        for name in ("sync-dependencies.yml", "daily-rollover.yml"):
            workflow = (WORKFLOWS / name).read_text(encoding="utf-8")
            self.assertNotIn("git push origin main", workflow)
            self.assertIn("gh pr create --base main", workflow)

    def test_agent_auto_merge_and_label_reaper_are_retired(self) -> None:
        self.assertFalse((WORKFLOWS / "auto-merge.yml").exists())
        self.assertFalse((WORKFLOWS / "dependabot-reaper.yml").exists())
        self.assertTrue((WORKFLOWS / "dependabot-rhythm.yml").exists())

    def test_dependabot_auto_merge_requires_verified_low_risk_updates_and_gates(self) -> None:
        workflow = (WORKFLOWS / "dependabot-rhythm.yml").read_text(encoding="utf-8")
        self.assertIn(
            "types: [opened, reopened, ready_for_review, synchronize, labeled, unlabeled]",
            workflow,
        )
        self.assertIn(
            "dependabot/fetch-metadata@ffa630c65fa7e0ecfa0625b5ceda64399aea1b36",
            workflow,
        )
        self.assertIn("github.event.pull_request.user.type == 'Bot'", workflow)
        self.assertIn("!contains(github.event.pull_request.labels.*.name, 'risk/high')", workflow)
        self.assertIn("contains(github.event.pull_request.labels.*.name, 'risk/high')", workflow)
        self.assertIn("Exclude protected live surfaces from automatic merge", workflow)
        for protected_path in (
            ".github/workflows/*",
            ".github/scripts/*",
            ".codex/*",
            ".openclaw/*",
            "AGENTS.md",
            "CONSTITUTION.md",
            "DECISIONS.md",
            "VAULT-CONVENTIONS.md",
            "swarm.json",
            "!/*",
        ):
            self.assertIn(protected_path, workflow)
        self.assertIn("steps.scope.outputs.eligible == 'true'", workflow)
        self.assertIn("Verify protected required checks exist", workflow)
        for context in (
            "check-secret-patterns",
            "check-large-files",
            "check-paths",
            "check-dotfolder-anchors",
        ):
            self.assertIn(context, workflow)
        self.assertIn("gh pr merge --disable-auto", workflow)
        self.assertNotIn("issues: write", workflow)
        self.assertNotIn("gh label create", workflow)
        self.assertNotIn("--delete-branch", workflow)

    def test_security_required_check_contexts_are_distinct(self) -> None:
        secret = (WORKFLOWS / "secret-pattern-policy.yml").read_text(encoding="utf-8")
        large = (WORKFLOWS / "large-file-policy.yml").read_text(encoding="utf-8")
        self.assertIn("check-secret-patterns:", secret)
        self.assertIn("check-large-files:", large)
        self.assertNotIn("\n  check:\n", secret)
        self.assertNotIn("\n  check:\n", large)

    def test_levelset_content_cannot_trigger_external_closure_message(self) -> None:
        self.assertFalse((WORKFLOWS / "levelset-closure-notify.yml").exists())
        self.assertFalse((ROOT / ".github" / "scripts" / "post_levelset_closure.py").exists())


if __name__ == "__main__":
    unittest.main()
