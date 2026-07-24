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

    def test_review_state_sync_jobs_can_maintain_labels(self) -> None:
        # review_feedback_loop.py sync-pr/review-submitted calls ensure_labels()
        # before reconciling review state. Label creation/update uses the Issues
        # API, so these write-capable review-state jobs must carry issues: write
        # alongside pull-requests/contents permissions. Without it, the PR can
        # be otherwise queue-ready while the review-state workflow fails before
        # it can restamp labels or re-arm enqueue.
        review_feedback = yaml.safe_load(
            (WORKFLOWS / "review-feedback-loop.yml").read_text(encoding="utf-8")
        )
        sweep_permissions = review_feedback["jobs"]["sweep-review-threads"]["permissions"]
        self.assertEqual(sweep_permissions["contents"], "write")
        self.assertEqual(sweep_permissions["issues"], "write")
        self.assertEqual(sweep_permissions["pull-requests"], "write")

        review_response = yaml.safe_load(
            (WORKFLOWS / "review-response.yml").read_text(encoding="utf-8")
        )
        self.assertEqual(review_response["permissions"]["contents"], "write")
        self.assertEqual(review_response["permissions"]["issues"], "write")
        self.assertEqual(review_response["permissions"]["pull-requests"], "write")

    def test_no_schedule_triggers_until_the_chron_clock_is_established(self) -> None:
        # Logan's standing order (restated 2026-07-06): NO cron jobs until the chron_clock
        # is established. The rule is the EMPTY SET — no allowlist to maintain, no
        # grandfathered exceptions: any `schedule:` trigger in any workflow turns this red.
        # Every periodic surface runs by workflow_dispatch until Logan establishes the
        # chron_clock; when he does, its ruling REPLACES this test wholesale (it is the
        # prescription of the interim norm, not of the eventual clock).
        offenders: list[str] = []
        for path in sorted(WORKFLOWS.glob("*.yml")):
            workflow = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            events = workflow.get("on", workflow.get(True)) or {}
            # Normalize every `on:` shape GitHub accepts — mapping, list, bare string —
            # so no shorthand slips the guard. (A bare `schedule` can't actually FIRE
            # without a cron mapping, but the guard is airtight, not merely practical.)
            if isinstance(events, dict):
                names = set(events)
            elif isinstance(events, list):
                names = set(events)
            else:
                names = {events}
            if "schedule" in names:
                offenders.append(path.name)
        self.assertEqual(
            offenders, [],
            "schedule trigger(s) found, but the chron_clock is not established "
            "(Logan's standing order — no cron jobs): " + ", ".join(offenders),
        )

    def test_merge_method_is_the_queues_alone(self) -> None:
        # K5/#631 (norm set by Logan, 2026-07-06): the merge QUEUE's configured method is
        # the single merge-method norm. gh syntax forces a method flag on every
        # `gh pr merge`, but on a merge-queue repo the queue overrides it — so the one
        # canonical, inert spelling is `--merge`. This goes red the moment any workflow
        # or script grows its own divergent method opinion (--squash/--rebase), which is
        # exactly the two-prescriptions-no-norm drift K5 names.
        scripts = ROOT / ".github" / "scripts"
        offenders: list[str] = []
        for path in sorted(list(WORKFLOWS.glob("*.yml")) + list(scripts.glob("*.py"))):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "pr" in line and "merge" in line and ("--squash" in line or "--rebase" in line):
                    offenders.append(f"{path.name}:{lineno}: {line.strip()}")
        self.assertEqual(
            offenders, [],
            "divergent merge-method opinion(s) found — the queue's configured method is "
            "the norm; use the canonical inert `--merge` flag:\n" + "\n".join(offenders),
        )

    def test_dependabot_auto_merge_requires_verified_low_risk_updates_and_gates(self) -> None:
        workflow = yaml.safe_load(
            (WORKFLOWS / "dependabot-rhythm.yml").read_text(encoding="utf-8")
        )
        events = workflow.get("on", workflow.get(True))
        self.assertEqual(
            events["pull_request_target"]["types"],
            ["opened", "reopened", "ready_for_review", "synchronize", "labeled", "unlabeled"],
        )
        # Least privilege: the workflow-level default is read-only; only the jobs
        # that actually merge/disable-merge escalate to write, at the job level.
        self.assertEqual(workflow["permissions"], {"contents": "read", "pull-requests": "read"})

        jobs = workflow["jobs"]
        eligible_job = jobs["auto-merge-low-risk"]
        self.assertEqual(
            eligible_job["permissions"], {"contents": "write", "pull-requests": "write"}
        )
        eligibility = eligible_job["if"]
        self.assertIn("github.event.pull_request.user.type == 'Bot'", eligibility)
        self.assertIn("!contains(github.event.pull_request.labels.*.name, 'risk/high')", eligibility)
        steps = {step["name"]: step for step in eligible_job["steps"]}
        # Pinned SHA tracks the merged Dependabot bump #361 (fetch-metadata 3.0.0 → 3.1.0).
        self.assertEqual(
            steps["Fetch Dependabot metadata"]["uses"],
            "dependabot/fetch-metadata@25dd0e34f4fe68f24cc83900b1fe3fe149efef98",
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
        # The gate requires the four policy checks that actually run on every PR
        # to have a `success` conclusion on the PR head. `submit-pypi` is NOT
        # gated here: it has no producing workflow in this repo (it lives only in
        # review_feedback_loop.KNOWN_NOISE_CHECKS as a check to ignore), so polling
        # for its success would fail-closed as "missing" and permanently disable
        # auto-merge. De-requiring it is the whole point of the ruleset change in
        # this PR; the gate is decoupled from required-for-merge to pass-on-PR.
        for context in (
            "check-secret-patterns",
            "check-large-files",
            "check-paths",
            "check-dotfolder-anchors",
        ):
            self.assertIn(context, gate_step["run"])
        self.assertNotIn("submit-pypi", gate_step["run"])
        enable_step = steps["Enable verified auto-merge"]
        self.assertIn("steps.scope.outputs.eligible == 'true'", enable_step["if"])
        self.assertIn("gh pr merge --auto --merge", enable_step["run"])
        self.assertNotIn("gh pr review --approve", enable_step["run"])
        self.assertNotIn("gh label create", enable_step["run"])
        self.assertNotIn("--delete-branch", enable_step["run"])

        high_risk_job = jobs["disable-high-risk-auto-merge"]
        self.assertEqual(
            high_risk_job["permissions"], {"contents": "write", "pull-requests": "write"}
        )
        self.assertIn("contains(github.event.pull_request.labels.*.name, 'risk/high')", high_risk_job["if"])
        self.assertIn("gh pr merge --disable-auto", high_risk_job["steps"][0]["run"])

    def test_security_required_check_contexts_are_distinct(self) -> None:
        secret = yaml.safe_load((WORKFLOWS / "secret-pattern-policy.yml").read_text(encoding="utf-8"))
        large = yaml.safe_load((WORKFLOWS / "large-file-policy.yml").read_text(encoding="utf-8"))
        self.assertIn("check-secret-patterns", secret["jobs"])
        self.assertIn("check-large-files", large["jobs"])
        self.assertNotIn("check", secret["jobs"])
        self.assertNotIn("check", large["jobs"])

    def test_portability_gate_runs_python_integrity_checker_with_timeout(self) -> None:
        workflow = yaml.safe_load((WORKFLOWS / "check-portable-paths.yml").read_text(encoding="utf-8"))
        job = workflow["jobs"]["check-paths"]
        self.assertEqual(job["timeout-minutes"], 10)

        steps = {step["name"]: step for step in job["steps"] if "name" in step}
        run = steps["Check Python automation integrity"]["run"]
        self.assertIn("trusted-main/.github/scripts/check_python_integrity.py", run)
        self.assertIn(".github/scripts/check_python_integrity.py", run)
        self.assertIn('python "$INTEGRITY_CHECKER"', run)

    def test_levelset_content_cannot_trigger_external_closure_message(self) -> None:
        self.assertFalse((WORKFLOWS / "levelset-closure-notify.yml").exists())
        self.assertFalse((ROOT / ".github" / "scripts" / "post_levelset_closure.py").exists())


if __name__ == "__main__":
    unittest.main()
