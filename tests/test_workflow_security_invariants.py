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

    def test_merge_queue_branches_are_excluded_from_auto_pr(self) -> None:
        # gh-readonly-queue/<base>/pr-<n>-<sha> is GitHub's own ephemeral merge-queue
        # branch: slash-namespaced like a real work branch, so it used to slip past the
        # generic `*/*` case and reach `gh pr create`, which rejects it outright ("Head
        # must not be a merge queue branch") -- CI sweep 2026-08-03, runs 30782704220 and
        # six others on gh-readonly-queue/main/pr-562-*, gh-readonly-queue/main/pr-857-*.
        workflow = (WORKFLOWS / "agent-auto-pr.yml").read_text(encoding="utf-8")
        gate_script = workflow.split("- name: Gate on supported branch events", 1)[1].split(
            "- name: Checkout repo", 1
        )[0]
        merge_queue_case = gate_script.split("gh-readonly-queue/*)", 1)
        self.assertEqual(len(merge_queue_case), 2, "gh-readonly-queue/*) case must exist")
        case_body = merge_queue_case[1].split(";;", 1)[0]
        self.assertIn('echo "skip=true"', case_body)
        # Bash `case` takes the first match, so the exclusion must be written before
        # the generic `*/*)` pattern or it is dead code.
        self.assertLess(gate_script.index("gh-readonly-queue/*)"), gate_script.index("*/*)"))

    def test_scheduled_mutations_open_prs_instead_of_pushing_main(self) -> None:
        for name in ("sync-dependencies.yml", "daily-rollover.yml"):
            workflow = (WORKFLOWS / name).read_text(encoding="utf-8")
            self.assertNotIn("git push origin main", workflow)
            self.assertIn("gh pr create --base main", workflow)

    def test_retired_auto_merge_lanes_are_gone(self) -> None:
        # The old agent auto-merge workflow and the label reaper were retired earlier; the two
        # author-gated fast-path lanes (dependabot-rhythm, auto-merge-rhythm) are retired here
        # (Logan's decision, 2026-07-19: drop the bot fast-path — bot PRs flow through the
        # universal engine like every PR). See PREFIX-FREE-ROUTING-2026-07-19.md.
        for retired in (
            "auto-merge.yml",
            "dependabot-reaper.yml",
            "dependabot-rhythm.yml",
            "auto-merge-rhythm.yml",
        ):
            self.assertFalse((WORKFLOWS / retired).exists(), f"{retired} must stay retired")

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
        # Norm set by Logan, 2026-07-06: the merge QUEUE's configured method is
        # the single merge-method norm. gh syntax forces a method flag on every
        # `gh pr merge`, but on a merge-queue repo the queue overrides it — so the one
        # canonical, inert spelling is `--merge`. This goes red the moment any workflow
        # or script grows its own divergent method opinion (--squash/--rebase), which is
        # exactly the two-prescriptions-no-norm drift this guards against.
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
        # Regression guard: without --root "$GITHUB_WORKSPACE" pinned, running the
        # trusted-main copy makes the checker's own default --root resolve to
        # trusted-main/ (its __file__ parents), scanning the base commit's tree
        # instead of the candidate workspace — silently missing violations the
        # PR itself introduces.
        self.assertIn('--root "$GITHUB_WORKSPACE"', run)

    def test_levelset_content_cannot_trigger_external_closure_message(self) -> None:
        self.assertFalse((WORKFLOWS / "levelset-closure-notify.yml").exists())
        self.assertFalse((ROOT / ".github" / "scripts" / "post_levelset_closure.py").exists())


if __name__ == "__main__":
    unittest.main()
