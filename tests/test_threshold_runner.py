from __future__ import annotations

from datetime import date
import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.five_wizards.enums import GateState, LaneDomain
from idaho_vault.operator_context import load_operator_context
from idaho_vault.five_wizards.threshold_runner import (
    OPERATOR_FRONT_DOOR_SURFACES,
    ThresholdContractError,
    build_threshold_workflow_input,
    render_threshold_stage_summary,
    run_threshold_stage,
    threshold_stage_root,
)


class ThresholdRunnerTest(unittest.TestCase):
    def test_build_threshold_workflow_input_covers_all_lanes(self) -> None:
        context = load_operator_context(root=PROJECT_ROOT)
        workflow = build_threshold_workflow_input(
            run_id="threshold-run-001",
            session_id="threshold-session-001",
            context=context,
        )

        self.assertEqual(workflow.run_id, "threshold-run-001")
        self.assertEqual(workflow.session_id, "threshold-session-001")
        self.assertEqual([lane_run.lane_domain for lane_run in workflow.lane_runs], list(LaneDomain))
        self.assertIn("AGENTS.md", workflow.gaggle_evidence_refs)
        self.assertIn(".crewai/MANIFEST.md", workflow.gaggle_evidence_refs)
        self.assertIn("TO DO LIST.md", workflow.gaggle_evidence_refs)
        self.assertTrue(any(context.daily_note_path in lane_run.wizard_note.text for lane_run in workflow.lane_runs))

    def test_run_threshold_stage_dry_run_uses_declared_stage_root(self) -> None:
        context = load_operator_context(root=PROJECT_ROOT)
        result = run_threshold_stage(run_id="threshold-run-dry", materialize=False, context=context)
        summary = render_threshold_stage_summary(result, context=context)

        self.assertFalse(result.materialized)
        self.assertEqual(Path(result.stage_root), threshold_stage_root())
        self.assertEqual(result.workflow.gate_report.overall_state, GateState.GREEN)
        self.assertIn(
            "AGENTS.md -> !/WAKEUP.md -> !/README.md -> !/AGENTS.md -> CONSTITUTION.md -> swarm.json",
            summary,
        )
        self.assertIn(" -> ".join(OPERATOR_FRONT_DOOR_SURFACES), summary)
        self.assertIn(context.daily_note_path, summary)
        self.assertIn("Promotion: Logan approval", summary)
        self.assertIn(str(threshold_stage_root()), summary)

    def test_run_threshold_stage_materializes_only_to_crewai_staging(self) -> None:
        context = load_operator_context(root=PROJECT_ROOT)
        run_id = "threshold-run-materialized"
        pack_root = threshold_stage_root() / run_id

        try:
            shutil.rmtree(pack_root, ignore_errors=True)
            result = run_threshold_stage(run_id=run_id, materialize=True, context=context)

            self.assertTrue(result.materialized)
            self.assertEqual(Path(result.stage_root), threshold_stage_root())
            self.assertEqual(Path(result.pack_root), pack_root)
            self.assertTrue(pack_root.exists())
            self.assertTrue(
                (pack_root / "meta" / f"{run_id}__workflow-artifact-manifest.json").exists()
            )
            self.assertGreater(len(result.materialized_paths), 0)
        finally:
            shutil.rmtree(pack_root, ignore_errors=True)

    def test_run_threshold_stage_refuses_missing_front_door(self) -> None:
        root = PROJECT_ROOT / "tests" / "_tmp_threshold_runner_case"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True, exist_ok=True)
        try:
            for relpath in (
                "AGENTS.md",
                "!/WAKEUP.md",
                "!/README.md",
                "!/AGENTS.md",
                "CONSTITUTION.md",
                "swarm.json",
                "DAILY NOTE TEMPLATE.md",
                ".obsidian/daily-notes.json",
                ".obsidian/plugins/periodic-notes/data.json",
                ".github/scripts/daily_rollover.py",
            ):
                path = root / relpath
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")

            context = load_operator_context(root=root, target_date=date(2026, 4, 17))

            with self.assertRaises(ThresholdContractError) as exc:
                run_threshold_stage(
                    run_id="threshold-run-missing-front-door",
                    materialize=False,
                    context=context,
                )
            self.assertIn("operator front door", str(exc.exception))
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
