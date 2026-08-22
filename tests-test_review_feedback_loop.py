from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


def _load_review_feedback_loop_module():
    script_name = Path(".github/scripts/review_feedback_loop.py")
    project_root = next(
        (candidate for candidate in Path(__file__).resolve().parents if (candidate / script_name).is_file()),
        None,
    )
    if project_root is None:
        raise RuntimeError(f"Unable to find repository root containing {script_name}")

    script_dir = project_root / ".github" / "scripts"
    helper_dirs = (script_dir, project_root / "scripts_scripts")
    added_to_path = [str(path) for path in helper_dirs if str(path) not in sys.path]
    for path_text in reversed(added_to_path):
        sys.path.insert(0, path_text)

    try:
        script_path = script_dir / "review_feedback_loop.py"
        spec = importlib.util.spec_from_file_location("review_feedback_loop_test_module", script_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Unable to load review feedback loop from {script_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for path_text in added_to_path:
            sys.path.remove(path_text)


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
) -> dict[str, object]:
    created_at = created_at or datetime(2026, 4, 16, 2, 0, tzinfo=timezone.utc)
    return {
        "number": number,
        "url": f"https://example.test/pr/{number}",
        "body": body,
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
        "isDraft": draft,
        "reviewDecision": review_decision,
        "labels": _labels(*labels),
        "reviewThreads": {"nodes": list(threads)},
    }


def _pr_view_result(*label_names: str) -> subprocess.CompletedProcess[str]:
    """Shape a `gh pr view --json labels` result, as `acknowledge_apply` reads it."""
    stdout = json.dumps({"labels": [{"name": name} for name in label_names]})
    return subprocess.CompletedProcess(args=["gh"], returncode=0, stdout=stdout)


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
                labels=(review_feedback_loop.RISK_LOW_LABEL, review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL),
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
                labels=(review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL,),
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
        disable_auto_merge.assert_not_called()

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
        disable_auto_merge.assert_called_once_with(29)

    def test_acknowledge_apply_marks_pending_after_trusted_request(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=41,
            comment_author="loganf",
            author_association="OWNER",
            comment_body="@copilot apply changes",
        )

        with mock.patch.object(
            review_feedback_loop, "ensure_labels"
        ) as ensure_labels, mock.patch.object(
            review_feedback_loop.gh_cli,
            "pr_view",
            return_value=_pr_view_result(),
        ), mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, mock.patch.object(
            review_feedback_loop, "_comment"
        ) as comment:
            result = review_feedback_loop.acknowledge_apply(args)

        self.assertEqual(result, 0)
        # ensure_labels() is only worth paying for on the path that actually
        # mutates a label -- see the module-level comment on acknowledge_apply.
        ensure_labels.assert_called_once_with()
        edit_label.assert_called_once_with(41, add=review_feedback_loop.DEFAULT_PENDING_LABEL)
        comment.assert_called_once()

    def test_acknowledge_apply_skips_ensure_labels_for_non_apply_comment(self) -> None:
        """Regression: a burst of unrelated PR comments (review-bot noise) must not
        each pay for a full label sweep. That amplification is what turned the
        third-party review-bot pile-on into a GitHub API rate-limit storm."""
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=41,
            comment_author="fixture-reviewer",
            author_association="NONE",
            comment_body="Insufficient balance to process this code review.",
        )

        with mock.patch.object(
            review_feedback_loop, "ensure_labels"
        ) as ensure_labels, mock.patch.object(
            review_feedback_loop.gh_cli, "pr_view"
        ) as pr_view:
            result = review_feedback_loop.acknowledge_apply(args)

        self.assertEqual(result, 0)
        ensure_labels.assert_not_called()
        pr_view.assert_not_called()

    def test_acknowledge_apply_skips_ensure_labels_for_untrusted_author(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=41,
            comment_author="fixture-untrusted",
            author_association="NONE",
            comment_body="@copilot apply changes",
        )

        with mock.patch.object(
            review_feedback_loop, "ensure_labels"
        ) as ensure_labels, mock.patch.object(
            review_feedback_loop.gh_cli, "pr_view"
        ) as pr_view:
            result = review_feedback_loop.acknowledge_apply(args)

        self.assertEqual(result, 0)
        ensure_labels.assert_not_called()
        pr_view.assert_not_called()

    def test_acknowledge_apply_skips_ensure_labels_when_already_pending(self) -> None:
        """The label already reflects the request; no mutation, so no sweep either."""
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=41,
            comment_author="loganf",
            author_association="OWNER",
            comment_body="@copilot apply changes",
        )

        with mock.patch.object(
            review_feedback_loop, "ensure_labels"
        ) as ensure_labels, mock.patch.object(
            review_feedback_loop.gh_cli,
            "pr_view",
            return_value=_pr_view_result(review_feedback_loop.DEFAULT_PENDING_LABEL),
        ) as pr_view, mock.patch.object(review_feedback_loop, "_edit_label") as edit_label:
            result = review_feedback_loop.acknowledge_apply(args)

        self.assertEqual(result, 0)
        # pr_view IS still called here -- reading current label state is how the
        # idempotent branch gets decided in the first place, so this one cheap REST
        # call is unavoidable on the genuine trusted-apply path. That's a world apart
        # from the bug this PR fixes: pr_view is never reached at all for the 15-20
        # untrusted/non-apply bot comments per push (see the two tests above), which
        # is where the actual rate-limit storm came from.
        pr_view.assert_called_once()
        ensure_labels.assert_not_called()
        edit_label.assert_not_called()

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
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ) as projection, mock.patch.object(review_feedback_loop, "_run") as run:
            result = review_feedback_loop.enable_auto_merge(args)

        self.assertEqual(result, 0)
        projection.assert_called_once()
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
