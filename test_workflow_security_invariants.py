from __future__ import annotations

import unittest
from pathlib import Path

import yaml


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
        workflow = yaml.safe_load(
            (WORKFLOWS / "dependabot-rhythm.yml").read_text(encoding="utf-8")
        )
        events = workflow.get("on", workflow.get(True))
        self.assertEqual(
            events["pull_request_target"]["types"],
            ["opened", "reopened", "ready_for_review", "synchronize", "labeled", "unlabeled"],
        )
        self.assertEqual(workflow["permissions"], {"contents": "write", "pull-requests": "write"})

        jobs = workflow["jobs"]
        eligible_job = jobs["auto-merge-low-risk"]
        eligibility = eligible_job["if"]
        self.assertIn("github.event.pull_request.user.type == 'Bot'", eligibility)
        self.assertIn("!contains(github.event.pull_request.labels.*.name, 'risk/high')", eligibility)
        steps = {step["name"]: step for step in eligible_job["steps"]}
        self.assertEqual(
            steps["Fetch Dependabot metadata"]["uses"],
            "dependabot/fetch-metadata@ffa630c65fa7e0ecfa0625b5ceda64399aea1b36",

        )
        scope_run = steps["Exclude protected live surfaces from automatic merge"]["run"]
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
            self.assertIn(protected_path, scope_run)

        gate_step = steps["Verify protected required checks exist"]
        self.assertIn("steps.scope.outputs.eligible == 'true'", gate_step["if"])
        for context in (
            "check-secret-patterns",
            "check-large-files",
            "check-paths",
            "check-dotfolder-anchors",
            "submit-pypi",
        ):
            self.assertIn(context, gate_step["run"])

        enable_step = steps["Enable verified auto-merge"]
        self.assertIn("steps.scope.outputs.eligible == 'true'", enable_step["if"])
        self.assertIn("gh pr merge --auto --squash", enable_step["run"])
        self.assertNotIn("gh pr review --approve", enable_step["run"])
        self.assertNotIn("gh label create", enable_step["run"])
        self.assertNotIn("--delete-branch", enable_step["run"])

        high_risk_job = jobs["disable-high-risk-auto-merge"]
        self.assertIn("contains(github.event.pull_request.labels.*.name, 'risk/high')", high_risk_job["if"])
        self.assertIn("gh pr merge --disable-auto", high_risk_job["steps"][0]["run"])

    def test_security_required_check_contexts_are_distinct(self) -> None:
        secret = yaml.safe_load((WORKFLOWS / "secret-pattern-policy.yml").read_text(encoding="utf-8"))
        large = yaml.safe_load((WORKFLOWS / "large-file-policy.yml").read_text(encoding="utf-8"))
        self.assertIn("check-secret-patterns", secret["jobs"])
        self.assertIn("check-large-files", large["jobs"])
        self.assertNotIn("check", secret["jobs"])
        self.assertNotIn("check", large["jobs"])

    def test_levelset_content_cannot_trigger_external_closure_message(self) -> None:
        self.assertFalse((WORKFLOWS / "levelset-closure-notify.yml").exists())
        self.assertFalse((ROOT / ".github" / "scripts" / "post_levelset_closure.py").exists())


if __name__ == "__main__":
    unittest.main()
