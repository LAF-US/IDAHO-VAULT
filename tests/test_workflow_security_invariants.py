from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

# The one-shot risk-vocabulary migration edits PR labels and DELETES label definitions — a
# security-sensitive surface, split three ways so that BOTH the destructive mode and the
# capability to perform it are reached only on purpose. The logic file is reusable-only;
# each entry point is dispatch-only, takes no inputs, and pins its own mode. Write scope
# and the MERGE_QUEUE_TOKEN PAT ride the APPLY path alone, so a dry run cannot create,
# edit, or delete a label even if a step tried. The three tests below hold that shape.
MIGRATION_LOGIC = "flatten-label-migration.yml"
MIGRATION_READ_ONLY = {"contents": "read", "pull-requests": "read"}
MIGRATION_WRITE = {"contents": "read", "pull-requests": "write", "issues": "write"}
# name -> (dry_run it pins, permissions it declares, whether it carries the PAT)
MIGRATION_ENTRY_POINTS = {
    "flatten-label-migration-preview.yml": (True, MIGRATION_READ_ONLY, False),
    "flatten-label-migration-apply.yml": (False, MIGRATION_WRITE, True),
}


def _workflow(name: str) -> tuple[dict, set]:
    """Parse a workflow, returning it alongside the set of event names it triggers on."""
    # PyYAML resolves the bare `on:` key to the boolean True, hence the fallback.
    wf = yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))
    events = wf.get("on", wf.get(True)) or {}
    return wf, (set(events) if isinstance(events, (dict, list)) else {events})


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

    def test_flatten_label_migration_logic_file_is_callable_only(self) -> None:
        # The file holding the destructive steps must be unreachable except through an
        # entry point, and must not drag the read-only one up to its own needs.
        wf, events = _workflow(MIGRATION_LOGIC)
        self.assertEqual(
            events, {"workflow_call"},
            f"{MIGRATION_LOGIC} holds the destructive steps: it must be callable only, "
            "never dispatchable and never auto-triggered (no schedule/PR/push)",
        )
        self.assertEqual(
            wf.get("permissions"), MIGRATION_READ_ONLY,
            f"{MIGRATION_LOGIC} must declare the read-only FLOOR, not the union of what "
            "its steps want. A called workflow can only downgrade its caller's "
            "permissions — asking for more fails validation — so a write set here would "
            "break the read-only preview entry point outright. Writes ride the PAT, not "
            "GITHUB_TOKEN.",
        )

    def test_flatten_label_migration_apply_path_refuses_to_start_without_the_pat(self) -> None:
        # Because GITHUB_TOKEN is capped read-only, every label write depends on the PAT.
        # That dependency has to fail fast rather than half-way through the re-stamp.
        wf, _ = _workflow(MIGRATION_LOGIC)
        guards = [
            step for job in wf["jobs"].values() for step in job["steps"]
            if "MIGRATION_PAT" in str(step.get("run", ""))
        ]
        self.assertEqual(
            len(guards), 1,
            f"{MIGRATION_LOGIC} must keep exactly one guard asserting the PAT is present",
        )
        self.assertIn(
            "dry_run == false", str(guards[0].get("if", "")),
            "the PAT guard must fire on the destructive path only, and must fire there: "
            "without it APPLY would fall back to a read-only github.token and die "
            "part-way through re-stamping",
        )

    def test_flatten_label_migration_entry_points_are_parameterless_and_mode_pinned(self) -> None:
        # Each entry point is a thin wrapper whose only job is to name a mode. Nothing
        # about the run may be chosen at dispatch time.
        for name, (dry_run, _permissions, _pat) in MIGRATION_ENTRY_POINTS.items():
            wf, events = _workflow(name)
            self.assertEqual(
                events, {"workflow_dispatch"},
                f"{name} must be dispatch-only (no schedule/PR/push triggers)",
            )
            dispatch = (wf.get("on", wf.get(True)) or {}).get("workflow_dispatch")
            self.assertFalse(
                isinstance(dispatch, dict) and dispatch.get("inputs"),
                f"{name} must take NO dispatch inputs — the mode is the workflow you pick, "
                "not a parameter on a run that can also delete label definitions "
                "(also Checkov CKV_GHA_7)",
            )
            jobs = wf["jobs"]
            self.assertEqual(len(jobs), 1, f"{name} must be a single thin wrapper job")
            job = next(iter(jobs.values()))
            self.assertEqual(job.get("uses"), f"./.github/workflows/{MIGRATION_LOGIC}")
            self.assertEqual(
                job.get("with"), {"dry_run": dry_run},
                f"{name} must pin dry_run={dry_run} — an entry point that can flip modes "
                "would reintroduce exactly what the split removes",
            )

    def test_flatten_label_migration_write_capability_lives_on_the_apply_path(self) -> None:
        # The separation that makes PREVIEW safe: it holds neither write scope nor the PAT,
        # so a dry run has no capability to touch a label even if a step tried to.
        for name, (_dry_run, permissions, carries_pat) in MIGRATION_ENTRY_POINTS.items():
            wf, _ = _workflow(name)
            job = next(iter(wf["jobs"].values()))
            self.assertEqual(
                wf.get("permissions"), permissions,
                f"{name} must declare exactly its own least-privilege permission set",
            )
            self.assertEqual(
                job.get("permissions"), permissions,
                f"{name}'s wrapper job must cap the called workflow at the same set",
            )
            self.assertNotEqual(
                job.get("secrets"), "inherit",
                f"{name} must pass secrets explicitly, never `inherit` — inheritance is "
                "what would hand the preview path a PAT it has no use for",
            )
            self.assertEqual(
                bool(job.get("secrets")), carries_pat,
                f"{name} carries the MERGE_QUEUE_TOKEN PAT: expected {carries_pat}. The "
                "write capability belongs on the destructive path alone.",
            )

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
