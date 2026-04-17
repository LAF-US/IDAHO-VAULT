from __future__ import annotations

import shutil
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.five_wizards.enums import GateState, LaneDomain
from idaho_vault.five_wizards.threshold_runner import (
    build_threshold_workflow_input,
    render_threshold_stage_summary,
    run_threshold_stage,
    threshold_stage_root,
)


class ThresholdRunnerTest(unittest.TestCase):
    def test_build_threshold_workflow_input_covers_all_lanes(self) -> None:
        workflow = build_threshold_workflow_input(run_id="threshold-run-001", session_id="threshold-session-001")

        self.assertEqual(workflow.run_id, "threshold-run-001")
        self.assertEqual(workflow.session_id, "threshold-session-001")
        self.assertEqual([lane_run.lane_domain for lane_run in workflow.lane_runs], list(LaneDomain))
        self.assertIn("AGENTS.md", workflow.gaggle_evidence_refs)
        self.assertIn(".crewai/MANIFEST.md", workflow.gaggle_evidence_refs)

    def test_run_threshold_stage_dry_run_uses_declared_stage_root(self) -> None:
        result = run_threshold_stage(run_id="threshold-run-dry", materialize=False)
        summary = render_threshold_stage_summary(result)

        self.assertFalse(result.materialized)
        self.assertEqual(Path(result.stage_root), threshold_stage_root())
        self.assertEqual(result.workflow.gate_report.overall_state, GateState.GREEN)
        self.assertIn(
            "AGENTS.md -> !/WAKEUP.md -> !/README.md -> !/AGENTS.md -> CONSTITUTION.md -> swarm.json",
            summary,
        )
        self.assertIn("Promotion: Logan approval", summary)
        self.assertIn(str(threshold_stage_root()), summary)

    def test_run_threshold_stage_materializes_only_to_crewai_staging(self) -> None:
        run_id = "threshold-run-materialized"
        pack_root = threshold_stage_root() / run_id

        try:
            shutil.rmtree(pack_root, ignore_errors=True)
            result = run_threshold_stage(run_id=run_id, materialize=True)

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


if __name__ == "__main__":
    unittest.main()
