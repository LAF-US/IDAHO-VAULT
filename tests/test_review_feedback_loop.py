from __future__ import annotations

import importlib.util
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


def _load_review_feedback_loop_module():
    project_root = Path(__file__).resolve().parents[1]
    script_path = project_root / ".github" / "scripts" / "review_feedback_loop.py"
    spec = importlib.util.spec_from_file_location("review_feedback_loop_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


review_feedback_loop = _load_review_feedback_loop_module()


def _labels(*names: str) -> dict[str, list[dict[str, str]]]:
    return {"nodes": [{"name": name} for name in names]}


def _thread(
    *,
    resolved: bool = False,
    outdated: bool = False,
    authors: tuple[str, ...] = ("reviewer",),
) -> dict[str, object]:
    return {
        "id": "THREAD_1",
        "isResolved": resolved,
        "isOutdated": outdated,
        "comments": {
            "nodes": [
                {
                    "author": {"login": author},
                    "body": "review note",
                    "url": "https://example.test/thread",
                }
                for author in authors
            ]
        },
    }


def _pr(
    *,
    number: int = 17,
    created_at: datetime | None = None,
    labels: tuple[str, ...] = (),
    review_decision: str | None = None,
    draft: bool = False,
    threads: tuple[dict[str, object], ...] = (),
    body: str = "## Auto-generated PR\n\n**Risk tier:**\n`low`\n",
    auto_merge_enabled: bool = False,
) -> dict[str, object]:
    created_at = created_at or datetime(2026, 4, 16, 2, 0, tzinfo=timezone.utc)
    return {
        "number": number,
        "url": f"https://example.test/pr/{number}",
        "body": body,
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
        "isDraft": draft,
        "reviewDecision": review_decision,
        "autoMergeRequest": {"enabledAt": created_at.isoformat().replace("+00:00", "Z")} if auto_merge_enabled else None,
        "labels": _labels(*labels),
        "reviewThreads": {"nodes": list(threads)},
    }


class ReviewFeedbackLoopTest(unittest.TestCase):
    def test_low_risk_pr_stays_pending_until_grace_elapses(self) -> None:
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        early_state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=10),
                labels=(review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL,),
            ),
            now=now,
        )
        ready_state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=(review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL,),
            ),
            now=now,
        )

        self.assertTrue(early_state["low_risk"])
        self.assertFalse(early_state["grace_elapsed"])
        self.assertTrue(early_state["should_have_agent_review_pending"])
        self.assertFalse(early_state["eligible_for_auto_merge"])

        self.assertTrue(ready_state["grace_elapsed"])
        self.assertFalse(ready_state["should_have_agent_review_pending"])
        self.assertTrue(ready_state["eligible_for_auto_merge"])

    def test_risk_label_is_canonical_over_body_marker(self) -> None:
        """Label-based risk tier wins when body marker was overwritten by an editor."""
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        # Body has no marker (agent rewrote it), but risk/low label is present.
        state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=("risk/low", "agent-review-pending"),
                body="## Real description\n\nSummary of changes.",
            ),
            now=now,
        )

        self.assertTrue(state["low_risk"])
        self.assertTrue(state["grace_elapsed"])
        self.assertTrue(state["eligible_for_auto_merge"])

    def test_risk_high_label_keeps_pr_out_of_auto_merge(self) -> None:
        """risk/high label alone must classify the PR as high-risk even if body is missing/empty."""
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=("risk/high",),
                body="",
            ),
            now=now,
        )

        self.assertFalse(state["low_risk"])
        self.assertFalse(state["eligible_for_auto_merge"])
        self.assertFalse(state["should_have_agent_review_pending"])

    def test_changes_requested_review_blocks_merge(self) -> None:
        state = review_feedback_loop.evaluate_review_state(
            _pr(
                labels=(review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL,),
                review_decision="CHANGES_REQUESTED",
            ),
            now=datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc),
        )

        self.assertTrue(state["blocking_review"])
        self.assertTrue(state["merge_blocked"])
        self.assertIn("changes-requested", state["blocking_reasons"])

    def test_outdated_allowlisted_threads_do_not_hold_review_threads_open(self) -> None:
        state = review_feedback_loop.evaluate_review_state(
            _pr(
                threads=(
                    _thread(
                        outdated=True,
                        authors=("copilot-pull-request-reviewer",),
                    ),
                ),
            ),
            auto_resolve_reviewers={"copilot-pull-request-reviewer"},
        )

        self.assertEqual(state["current_unresolved_threads"], 0)
        self.assertEqual(state["outdated_unresolved_threads"], 1)
        self.assertEqual(state["auto_resolvable_outdated_threads"], 1)
        self.assertFalse(state["merge_blocked"])

    def test_current_unresolved_threads_block_promotion(self) -> None:
        state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
                labels=("agent-review-pending",),
                threads=(_thread(authors=("human-reviewer",)),),
            ),
            now=datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(state["current_unresolved_threads"], 1)
        self.assertTrue(state["merge_blocked"])
        self.assertIn("current-review-threads", state["blocking_reasons"])
        self.assertFalse(state["eligible_for_auto_merge"])

    def test_apply_review_state_projection_clears_stale_labels(self) -> None:
        state = {
            "labels": [
                review_feedback_loop.DEFAULT_REVIEW_REQUIRED_LABEL,
                review_feedback_loop.DEFAULT_THREAD_LABEL,
                review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL,
                review_feedback_loop.DEFAULT_PENDING_LABEL,
            ],
            "blocking_review": False,
            "current_unresolved_threads": 0,
            "should_have_agent_review_pending": False,
            "merge_blocked": False,
        }

        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable_auto_merge:
            actions = review_feedback_loop.apply_review_state_projection(
                17,
                state,
                clear_apply_pending=True,
            )

        self.assertEqual(
            actions,
            [
                f"remove:{review_feedback_loop.DEFAULT_REVIEW_REQUIRED_LABEL}",
                f"remove:{review_feedback_loop.DEFAULT_THREAD_LABEL}",
                f"remove:{review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL}",
                f"remove:{review_feedback_loop.DEFAULT_PENDING_LABEL}",
            ],
        )
        self.assertEqual(
            edit_label.call_args_list,
            [
                mock.call(17, remove=review_feedback_loop.DEFAULT_REVIEW_REQUIRED_LABEL),
                mock.call(17, remove=review_feedback_loop.DEFAULT_THREAD_LABEL),
                mock.call(17, remove=review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL),
                mock.call(17, remove=review_feedback_loop.DEFAULT_PENDING_LABEL),
            ],
        )
        disable_auto_merge.asse***REMOVED***not_called()

    def test_apply_review_state_projection_disables_auto_merge_when_blocked(self) -> None:
        state = {
            "labels": [review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL],
            "blocking_review": True,
            "current_unresolved_threads": 0,
            "should_have_agent_review_pending": False,
            "merge_blocked": True,
            "eligible_for_auto_merge": False,
        }

        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable_auto_merge:
            actions = review_feedback_loop.apply_review_state_projection(29, state)

        self.assertEqual(
            actions,
            [
                f"add:{review_feedback_loop.DEFAULT_REVIEW_REQUIRED_LABEL}",
                f"remove:{review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL}",
            ],
        )
        self.assertEqual(
            edit_label.call_args_list,
            [
                mock.call(29, add=review_feedback_loop.DEFAULT_REVIEW_REQUIRED_LABEL),
                mock.call(29, remove=review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL),
            ],
        )
        disable_auto_merge.asse***REMOVED***called_once_with(29)

    def test_apply_review_state_projection_clears_stale_auto_merge_when_not_eligible(self) -> None:
        state = {
            "labels": [review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL],
            "blocking_review": False,
            "current_unresolved_threads": 0,
            "should_have_agent_review_pending": False,
            "merge_blocked": False,
            "eligible_for_auto_merge": False,
        }

        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable_auto_merge:
            actions = review_feedback_loop.apply_review_state_projection(31, state)

        self.assertEqual(actions, [f"remove:{review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL}"])
        edit_label.asse***REMOVED***called_once_with(31, remove=review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL)
        disable_auto_merge.asse***REMOVED***called_once_with(31)

    def test_acknowledge_apply_marks_pending_after_trusted_request(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=41,
            comment_author="loganf",
            author_association="OWNER",
            comment_body="@copilot apply changes",
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            return_value=_pr(labels=()),
        ), mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, mock.patch.object(
            review_feedback_loop, "_comment"
        ) as comment:
            result = review_feedback_loop.acknowledge_apply(args)

        self.assertEqual(result, 0)
        edit_label.asse***REMOVED***called_once_with(41, add=review_feedback_loop.DEFAULT_PENDING_LABEL)
        comment.asse***REMOVED***called_once()

    def test_sync_pr_clears_pending_only_for_allowed_completion_actors(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=57,
            sync_actor="Copilot",
            grace_minutes=30,
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            return_value=_pr(labels=(review_feedback_loop.DEFAULT_PENDING_LABEL,)),
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_advisory_threads",
            return_value=0,
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ) as projection:
            result = review_feedback_loop.sync_pr(args)

        self.assertEqual(result, 0)
        self.assertTrue(projection.call_args.kwargs["clear_apply_pending"])

    def test_enable_auto_merge_refuses_to_arm_when_derived_state_is_blocking(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=73,
            grace_minutes=30,
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            return_value=_pr(
                labels=(review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL,),
                review_decision="CHANGES_REQUESTED",
            ),
        ), mock.patch.object(review_feedback_loop, "_edit_label"), mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable_auto_merge, mock.patch.object(review_feedback_loop, "_run") as run:
            result = review_feedback_loop.enable_auto_merge(args)

        self.assertEqual(result, 0)
        disable_auto_merge.asse***REMOVED***called_once_with(73)
        run.asse***REMOVED***not_called()

    def test_enable_auto_merge_refuses_to_arm_when_not_eligible(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=74,
            grace_minutes=30,
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            return_value=_pr(
                labels=(review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL,),
                body="## Auto-generated PR\n\n**Risk tier:**\n`high`\n",
            ),
        ), mock.patch.object(review_feedback_loop, "_edit_label"), mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable_auto_merge, mock.patch.object(review_feedback_loop, "_run") as run:
            result = review_feedback_loop.enable_auto_merge(args)

        self.assertEqual(result, 0)
        disable_auto_merge.asse***REMOVED***called_once_with(74)
        run.asse***REMOVED***not_called()

    def test_arm_auto_merge_degrades_when_protected_branch_blocks_enablement(self) -> None:
        error = RuntimeError(
            "Command failed (1): gh pr merge 289 --squash --delete-branch --auto\n"
            "stdout:\n\n"
            "stderr:\n"
            "GraphQL: Pull request User is not authorized for this protected branch "
            "(enablePullRequestAutoMerge)\n"
        )

        with mock.patch.object(review_feedback_loop, "_run", side_effect=error):
            enabled, arm_error = review_feedback_loop._arm_auto_merge(289)

        self.assertFalse(enabled)
        self.assertIn("not authorized to enable auto-merge", arm_error)

    def test_reconcile_open_prs_repairs_drift_and_rearms_auto_merge(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            grace_minutes=30,
        )
        ready_pr = _pr(
            number=88,
            created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
            labels=(review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL,),
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_list_open_pr_numbers",
            return_value=[88],
        ), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            side_effect=[ready_pr],
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_advisory_threads",
            return_value=0,
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "_edit_label"
        ) as edit_label, mock.patch.object(
            review_feedback_loop, "_comment"
        ) as comment, mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ) as arm_auto_merge:
            result = review_feedback_loop.reconcile_open_prs(args)

        self.assertEqual(result, 0)
        edit_label.asse***REMOVED***called_once_with(88, add=review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL)
        comment.asse***REMOVED***called_once()
        arm_auto_merge.asse***REMOVED***called_once_with(88)

    def test_reconcile_open_prs_reports_auth_blocked_auto_merge(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            grace_minutes=30,
        )
        ready_pr = _pr(
            number=89,
            created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
            labels=(review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL,),
        )

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_list_open_pr_numbers",
            return_value=[89],
        ), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            side_effect=[ready_pr],
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_advisory_threads",
            return_value=0,
        ), mock.patch.object(
            review_feedback_loop,
            "evaluate_review_state",
            return_value={
                "labels": {review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL},
                "low_risk": True,
                "eligible_for_auto_merge": True,
                "merge_blocked": False,
                "blocking_reasons": [],
            },
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(
                False,
                "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
            )
        ):
            report = review_feedback_loop._build_reconciliation_report(
                "LAF-US",
                "IDAHO-VAULT",
                grace_minutes=30,
            )

        self.assertEqual(report["rearmed_prs"], [])
        self.assertEqual(report["auto_merge_authorization_blocked"], [89])
        self.assertEqual(
            report["evaluated"][0]["auto_merge_arm_error"],
            "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
        )


if __name__ == "__main__":
    unittest.main()
