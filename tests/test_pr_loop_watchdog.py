from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def _load_pr_loop_watchdog_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "pr_loop_watchdog.py"
    spec = importlib.util.spec_from_file_location("pr_loop_watchdog_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pr_loop_watchdog = _load_pr_loop_watchdog_module()


class PrLoopWatchdogTest(unittest.TestCase):
    def test_build_repo***REMOVED***marks_blocked_authorizations_as_findings(self) -> None:
        markdown, has_findings = pr_loop_watchdog.build_report(
            {
                "checked_prs": 1,
                "promoted_prs": [],
                "rearmed_prs": [],
                "resolved_outdated_threads": 0,
                "auto_merge_authorization_blocked": [89],
                "evaluated": [
                    {
                        "number": 89,
                        "eligible_for_auto_merge": True,
                        "merge_blocked": False,
                        "auto_merge_enabled": False,
                        "blocking_reasons": [],
                        "actions": [],
                        "auto_merge_arm_error": "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
                    }
                ],
            }
        )

        self.assertTrue(has_findings)
        self.assertIn("PR #89", markdown)
        self.assertIn("not authorized to enable auto-merge", markdown)

    def test_build_repo***REMOVED***renders_healthy_reconciliation_without_findings(self) -> None:
        markdown, has_findings = pr_loop_watchdog.build_report(
            {
                "checked_prs": 2,
                "promoted_prs": [12],
                "rearmed_prs": [12],
                "resolved_outdated_threads": 3,
                "auto_merge_authorization_blocked": [],
                "evaluated": [
                    {
                        "number": 12,
                        "eligible_for_auto_merge": True,
                        "merge_blocked": False,
                        "auto_merge_enabled": True,
                        "blocking_reasons": [],
                        "actions": ["add:auto-merge"],
                        "auto_merge_arm_error": None,
                    }
                ],
            }
        )

        self.assertFalse(has_findings)
        self.assertIn("No unresolved PR-loop blockers remain after reconciliation.", markdown)
        self.assertIn("Promoted to `auto-merge`: **1**", markdown)


if __name__ == "__main__":
    unittest.main()
