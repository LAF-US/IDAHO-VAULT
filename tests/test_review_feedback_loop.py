"""Tests for review_feedback_loop.py — loaded dynamically via importlib."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


def _load_review_feedback_loop_module():
    project_root = Path(__file__).resolve().parents[1]
    scripts_dir = project_root / ".github" / "scripts"
    script_path = scripts_dir / "review_feedback_loop.py"
    spec = importlib.util.spec_from_file_location("review_feedback_loop_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # The engine imports its shared thread-analysis lib (pr_threads) as a sibling
    # module; loading it by file path needs the scripts dir importable. Scope the
    # mutation to the exec so the test run's global sys.path isn't left altered —
    # the import is bound during exec, and pr_threads stays cached in sys.modules.
    # (Production runs the script directly, which already has this on sys.path[0].)
    original_sys_path = list(sys.path)
    sys.path.insert(0, str(scripts_dir))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = original_sys_path
    return module


review_feedback_loop = _load_review_feedback_loop_module()
# The shared thread-analysis vocabulary now lives in pr_threads (#600 §5). The
# engine's load above imported it, so it's cached in sys.modules; predicates the
# engine no longer re-exports (e.g. _author_is_bot) are tested against it directly.
pr_threads = sys.modules["pr_threads"]
# Every ``gh`` command line is now built inside gh_cli by a typed operation, and the
# run primitive there is private. Tests that assert on the emitted argv patch that one
# primitive, so they check the command line that is actually executed.
gh_cli = sys.modules["gh_cli"]


def _labels(*names: str) -> dict[str, list[dict[str, str]]]:
    return {"nodes": [{"name": name} for name in names]}


def _thread(
    *,
    resolved: bool = False,
    outdated: bool = False,
    authors: tuple[str, ...] = ("reviewer",),
    author_type: str = "User",
    body: str = "review note",
    resolved_by: str | None = None,
) -> dict[str, object]:
    return {
        "id": "THREAD_1",
        "isResolved": resolved,
        "isOutdated": outdated,
        "resolvedBy": {"login": resolved_by} if resolved_by else None,
        "comments": {
            "pageInfo": {"hasNextPage": False},
            "nodes": [
                {
                    "author": {"login": author, "__typename": author_type},
                    "body": body,
                    "url": "https://example.test/thread",
                }
                for author in authors
            ],
        },
    }


def _pr(
    *,
    number: int = 17,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
    labels: tuple[str, ...] = (),
    review_decision: str | None = None,
    draft: bool = False,
    threads: tuple[dict[str, object], ...] = (),
    threads_truncated: bool = False,
    body: str = "## Auto-generated PR\n\n**Risk tier:**\n`low`\n",
    auto_merge_enabled: bool = False,
    state: str = "OPEN",
) -> dict[str, object]:
    created_at = created_at or datetime(2026, 4, 16, 2, 0, tzinfo=timezone.utc)
    updated_at = updated_at or created_at
    return {
        "number": number,
        "url": f"https://example.test/pr/{number}",
        "body": body,
        "state": state,
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
        "updatedAt": updated_at.isoformat().replace("+00:00", "Z"),
        "isDraft": draft,
        "reviewDecision": review_decision,
        "autoMergeRequest": {"enabledAt": created_at.isoformat().replace("+00:00", "Z")} if auto_merge_enabled else None,
        "labels": _labels(*labels),
        "reviewThreads": {"pageInfo": {"hasNextPage": threads_truncated}, "nodes": list(threads)},
    }


class ReviewFeedbackLoopTest(unittest.TestCase):
    def test_prior_verify_comment_is_found_past_the_first_page(self) -> None:
        # Regression: `gh api --paginate` emits one array PER PAGE, so reading stdout as a
        # single JSON document sees `[...][...]`, raises, and yields no bodies at all. The
        # recursion guard then failed open on exactly the busy PRs most likely to already
        # carry a verification comment. Reading via --jq has no document boundary.
        marker = review_feedback_loop.VERIFY_CLAIM_MARKER
        two_pages = "\n".join(["first page body", "another", f"page two body {marker}"])
        captured = {}

        def fake(owner, repo, issue_number, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(stdout=two_pages, stderr="", returncode=0)

        with mock.patch.object(review_feedback_loop.gh_cli, "api_issue_comments", fake):
            found = review_feedback_loop._has_prior_verify_comment("LAF-US", "IDAHO-VAULT", 877)

        self.assertTrue(found)
        self.assertEqual(captured.get("jq"), ".[].body")

    def test_clear_pair_pr_becomes_auto_merge_eligible_after_grace(self) -> None:
        # K3/#629: the `—/—` pair — and ONLY it — arms auto-merge. A PR that classify
        # scored clear (risk/—) with no blocking feedback is eligible once the grace window
        # elapses; within grace it is not yet eligible.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        early_state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=10),
                labels=(review_feedback_loop.RISK_CLEAR_LABEL,),
            ),
            now=now,
        )
        ready_state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=(review_feedback_loop.RISK_CLEAR_LABEL,),
            ),
            now=now,
        )

        self.assertTrue(early_state["is_clear"])
        self.assertFalse(early_state["grace_elapsed"])
        self.assertFalse(early_state["eligible_for_auto_merge"])

        self.assertTrue(ready_state["is_clear"])
        self.assertTrue(ready_state["grace_elapsed"])
        self.assertTrue(ready_state["eligible_for_auto_merge"])

    def test_low_risk_pr_holds_and_never_auto_merges(self) -> None:
        # K3/#629 norm flip: risk/low is a sorter that FIRED (machine-doc paths) — it HOLDS
        # for review, it does not arm. Only the positive clear marker auto-merges. A low-risk
        # PR past grace with no blocking feedback stays ineligible and carries review/pending.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=(review_feedback_loop.RISK_LOW_LABEL,),
            ),
            now=now,
        )

        self.assertTrue(state["low_risk"])
        self.assertFalse(state["is_clear"])
        self.assertTrue(state["grace_elapsed"])
        self.assertFalse(state["eligible_for_auto_merge"])
        self.assertTrue(state["should_have_agent_review_pending"])

    def test_risk_label_is_canonical_over_body_marker(self) -> None:
        """Label-based risk tier wins when body marker was overwritten by an editor."""
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)

        # Body has no marker (agent rewrote it), but risk/low label is present.
        state = review_feedback_loop.evaluate_review_state(
            _pr(
                created_at=now - timedelta(minutes=45),
                labels=("risk/low", review_feedback_loop.DEFAULT_REVIEW_PENDING_LABEL),
                body="## Real description\n\nSummary of changes.",
            ),
            now=now,
        )

        self.assertEqual(state["risk_tier"], "low")
        self.assertTrue(state["low_risk"])
        self.assertTrue(state["grace_elapsed"])
        # K3/#629: risk/low HOLDS — the label is canonical for the tier, but low is not the
        # clear pair, so it never arms.
        self.assertFalse(state["eligible_for_auto_merge"])

    def test_high_risk_label_wins_when_low_and_high_are_both_present(self) -> None:
        state = review_feedback_loop.evaluate_review_state(
            _pr(labels=("risk/low", "risk/high")),
            now=datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(state["risk_tier"], "high")
        self.assertFalse(state["low_risk"])
        self.assertFalse(state["eligible_for_auto_merge"])

    def test_pair_lane_parses_both_axes(self) -> None:
        # K6/#632: the lane IS the label pair — one label per independent analysis.
        rfl = review_feedback_loop
        ft, dp, marked = rfl._risk_pair_for_pr({"filetype:risk/—", "depth:risk/—"})
        self.assertEqual((ft, dp, marked), (None, None, True))
        ft, dp, marked = rfl._risk_pair_for_pr({"filetype:risk/med", "depth:risk/high"})
        self.assertEqual((ft, dp, marked), ("med", "high", True))
        ft, dp, marked = rfl._risk_pair_for_pr({"filetype:risk/low", "depth:risk/nope"})
        self.assertEqual((ft, dp, marked), ("low", "nope", True))
        # One axis unmarked (and no legacy fallback) -> NOT fully marked: the PR holds.
        ft, dp, marked = rfl._risk_pair_for_pr({"filetype:risk/med"})
        self.assertFalse(marked)

    def test_pair_axis_exclusion_fails_loud(self) -> None:
        # K6 per-axis mutual exclusion: an axis carries exactly ONE label — its `—` XOR
        # its fired flag. Two labels on one axis is a producer/restamp bug: raise.
        rfl = review_feedback_loop
        for labels in (
            {"filetype:risk/—", "filetype:risk/med", "depth:risk/—"},
            {"filetype:risk/low", "filetype:risk/med"},
            {"depth:risk/high", "depth:risk/nope", "filetype:risk/—"},
        ):
            with self.subTest(labels=labels):
                with self.assertRaises(rfl.RiskMarkerInvariantError):
                    rfl._risk_pair_for_pr(labels)

    def test_pair_clear_arms_and_pair_flag_holds(self) -> None:
        # The {—,—} pair arms after grace; a fired lane holds until its review completes.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        clear_state = review_feedback_loop.evaluate_review_state(
            _pr(created_at=now - timedelta(minutes=45),
                labels=("filetype:risk/—", "depth:risk/—")),
            now=now,
        )
        self.assertTrue(clear_state["is_clear"])
        self.assertTrue(clear_state["eligible_for_auto_merge"])

        held_state = review_feedback_loop.evaluate_review_state(
            _pr(created_at=now - timedelta(minutes=45),
                labels=("filetype:risk/med", "depth:risk/—")),
            now=now,
        )
        self.assertEqual(held_state["risk_tier"], "med")
        self.assertFalse(held_state["eligible_for_auto_merge"])

    def test_lane_completion_clears_flag_and_flows(self) -> None:
        # K6 "Restamp + clear": an approving review with no current threads completes the
        # lane — the PR becomes eligible, and the projection consumes the fired flag
        # (restamps the axis to its `—`).
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        state = review_feedback_loop.evaluate_review_state(
            _pr(created_at=now - timedelta(minutes=45),
                labels=("filetype:risk/med", "depth:risk/—"),
                review_decision="APPROVED"),
            now=now,
        )
        self.assertTrue(state["lane_complete"])
        self.assertTrue(state["flag_clearable"])
        self.assertTrue(state["eligible_for_auto_merge"])

        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, \
             mock.patch.object(review_feedback_loop, "_disable_auto_merge"):
            actions = review_feedback_loop.apply_review_state_projection(17, state)
        self.assertIn("add:filetype:risk/—", actions)
        self.assertIn("remove:filetype:risk/med", actions)
        edit_label.assert_any_call(17, add="filetype:risk/—")

    def test_nope_lane_never_auto_clears_even_approved(self) -> None:
        # The still point asks for the sovereign's own hand: depth:risk/nope is never
        # consumed by review completion and never arms.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        state = review_feedback_loop.evaluate_review_state(
            _pr(created_at=now - timedelta(minutes=45),
                labels=("filetype:risk/—", "depth:risk/nope"),
                review_decision="APPROVED"),
            now=now,
        )
        self.assertEqual(state["risk_tier"], "nope")
        self.assertTrue(state["lane_complete"])
        self.assertFalse(state["flag_clearable"])
        self.assertFalse(state["eligible_for_auto_merge"])
        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, \
             mock.patch.object(review_feedback_loop, "_disable_auto_merge"):
            actions = review_feedback_loop.apply_review_state_projection(18, state)
        self.assertNotIn("remove:depth:risk/nope", actions)

    def test_restamp_mirrors_classifier_and_syncs_legacy(self) -> None:
        # K6 restamp: labels mirror the verdict — pair stamped, stale pair labels and
        # contradicted legacy sparse labels retired, legacy mirror kept in sync.
        with mock.patch.object(review_feedback_loop, "_edit_label"):
            labels = {"filetype:risk/med", "depth:risk/—", "risk/low", "review/pending"}
            actions = review_feedback_loop.restamp_risk_pair(21, labels, None, None)
        self.assertIn("add:filetype:risk/—", actions)
        self.assertIn("remove:filetype:risk/med", actions)
        self.assertIn("add:risk/—", actions)
        self.assertIn("remove:risk/low", actions)
        self.assertIn("review/pending", labels)  # non-risk labels untouched
        self.assertEqual(
            labels & {"filetype:risk/—", "depth:risk/—", "risk/—"},
            {"filetype:risk/—", "depth:risk/—", "risk/—"},
        )

        with mock.patch.object(review_feedback_loop, "_edit_label"):
            labels = {"risk/—"}
            actions = review_feedback_loop.restamp_risk_pair(22, labels, "low", "high")
        self.assertIn("add:filetype:risk/low", actions)
        self.assertIn("add:depth:risk/high", actions)
        self.assertIn("add:risk/high", actions)
        self.assertIn("remove:risk/—", actions)

    def test_sync_pr_restamps_unmarked_pr_from_classifier(self) -> None:
        # K6 backfill-by-automation: an unmarked in-flight PR gets its pair stamped from
        # the classifier on the next sync — no hand-sweep.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        args = SimpleNamespace(
            owner="LAF-US", repo="IDAHO-VAULT", pr_number=300,
            sync_actor="someone", grace_minutes=30,
        )
        unmarked = _pr(number=300, created_at=now - timedelta(minutes=45), labels=())
        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop, "_fetch_pr", return_value=unmarked
        ), mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop, "_resolve_outdated_resolvable_threads", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "_classify_pr_pair", return_value=(None, None)
        ), mock.patch.object(
            review_feedback_loop, "_edit_label"
        ), mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ), mock.patch.object(
            gh_cli, "_run"
        ), mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ) as arm, contextlib.redirect_stdout(io.StringIO()):
            result = review_feedback_loop.sync_pr(args)
        self.assertEqual(result, 0)
        # Restamped to the {—,—} pair -> clear lane -> armed on this same pass.
        arm.assert_called_once_with("LAF-US", "IDAHO-VAULT", 300)

    def test_clear_marker_classifies_as_clear(self) -> None:
        # K4/#630: the positive `risk/—` marker is its own tier ("clear"), distinct from low.
        self.assertEqual(
            review_feedback_loop._risk_tier_for_pr("", {review_feedback_loop.RISK_CLEAR_LABEL}),
            "clear",
        )

    def test_unmarked_pr_holds_and_is_not_clear(self) -> None:
        # K4/#630 core: absence of a marker is NOT classified-clear. An unmarked PR resolves
        # to "unknown" and never arms — only the positive risk/— marker does.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        state = review_feedback_loop.evaluate_review_state(
            _pr(created_at=now - timedelta(minutes=45), labels=(), body="## No marker\n"),
            now=now,
        )

        self.assertEqual(state["risk_tier"], "unknown")
        self.assertFalse(state["is_clear"])
        self.assertFalse(state["low_risk"])
        self.assertTrue(state["grace_elapsed"])
        self.assertFalse(state["eligible_for_auto_merge"])

    def test_clear_marker_is_mutually_exclusive_with_flags(self) -> None:
        # K4/#630 invariant: risk/— XOR a flag, never both. A PR carrying the clear marker
        # alongside any risk/* flag is a producer/backfill bug — fail LOUD, never silently
        # auto-merge a PR a sorter actually flagged.
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        for flag in (review_feedback_loop.RISK_LOW_LABEL, review_feedback_loop.RISK_HIGH_LABEL):
            with self.subTest(flag=flag):
                with self.assertRaises(review_feedback_loop.RiskMarkerInvariantError):
                    review_feedback_loop.evaluate_review_state(
                        _pr(
                            created_at=now - timedelta(minutes=45),
                            labels=(review_feedback_loop.RISK_CLEAR_LABEL, flag),
                        ),
                        now=now,
                    )

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
        edit_label.assert_called_once_with(31, remove=review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL)
        disable_auto_merge.assert_called_once_with(31)

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
        edit_label.assert_called_once_with(41, add=review_feedback_loop.DEFAULT_PENDING_LABEL)
        comment.assert_called_once()

    def test_sync_pr_clears_pending_only_for_allowed_completion_actors(self) -> None:
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=57,
            sync_actor="Copilot",
            grace_minutes=30,
        )

        # The helper returns a mix of applied/not-applied results so we can assert sync_pr
        # counts only the applied ones (resolved_count) — and, because that count is > 0,
        # re-fetches the PR to recompute state against the now-cleared threads.
        outdated_results = [
            {"thread_id": "A", "eligible": True, "applied": True, "reason": ""},
            {"thread_id": "B", "eligible": False, "applied": False, "reason": "blocked"},
            {"thread_id": "C", "eligible": True, "applied": True, "reason": ""},
        ]

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop,
            "_fetch_pr",
            return_value=_pr(labels=(review_feedback_loop.DEFAULT_PENDING_LABEL,)),
        ) as fetch_pr, mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_resolvable_threads",
            return_value=outdated_results,
        ) as resolve_outdated, mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ) as projection:
            result = review_feedback_loop.sync_pr(args)

        self.assertEqual(result, 0)
        self.assertTrue(projection.call_args.kwargs["clear_apply_pending"])
        # Applies on the event path; the looker is left None so the helper resolves it
        # lazily (only if there's a stale thread) — no eager _viewer_login() round-trip.
        resolve_outdated.assert_called_once()
        self.assertIsNone(resolve_outdated.call_args.args[1])
        self.assertEqual(resolve_outdated.call_args.kwargs["apply"], True)
        # Two of three results applied -> resolved_count == 2 (> 0) -> PR re-fetched once
        # more (initial fetch + the post-resolve re-fetch).
        self.assertEqual(fetch_pr.call_count, 2)

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
        ) as disable_auto_merge, mock.patch.object(gh_cli, "_run") as run:
            result = review_feedback_loop.enable_auto_merge(args)

        self.assertEqual(result, 0)
        disable_auto_merge.assert_called_once_with(73)
        run.assert_not_called()

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
        ) as disable_auto_merge, mock.patch.object(gh_cli, "_run") as run:
            result = review_feedback_loop.enable_auto_merge(args)

        self.assertEqual(result, 0)
        disable_auto_merge.assert_called_once_with(74)
        run.assert_not_called()

    def test_arm_auto_merge_degrades_when_protected_branch_blocks_enablement(self) -> None:
        error = RuntimeError(
            "Command failed (1): gh pr merge 289 --merge --auto\n"
            "stdout:\n\n"
            "stderr:\n"
            "GraphQL: Pull request User is not authorized for this protected branch "
            "(enablePullRequestAutoMerge)\n"
        )

        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(gh_cli, "_run", side_effect=error):
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 289)

        self.assertFalse(enabled)
        self.assertIn("not authorized to enable auto-merge", arm_error)

    def test_arm_auto_merge_plain_enable_then_enqueue_when_off(self) -> None:
        # Auto-merge off → enable (`--auto`) AND THEN add it to the merge queue (enqueue).
        # Both halves: arming alone never queued it (the bug); enqueue is the missing half.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node1"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(True, None)
        ) as enqueue, mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 10)
        self.assertTrue(enabled)
        self.assertIsNone(arm_error)
        run.assert_called_once_with(
            ["gh", "pr", "merge", "10", "--merge", "--auto"], check=True
        )
        enqueue.assert_called_once_with("PR_node1")

    def test_arm_auto_merge_enqueues_when_armed_but_not_queued(self) -> None:
        # The #508 case: auto-merge already on but the PR was never put in the queue.
        # Re-arming is an idempotent no-op — the actual fix is to call enqueue, not re-toggle.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(True, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node2"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(True, None)
        ) as enqueue, mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 11)
        self.assertTrue(enabled)
        self.assertIsNone(arm_error)
        run.assert_not_called()  # already armed — no redundant enable
        enqueue.assert_called_once_with("PR_node2")

    def test_arm_auto_merge_leaves_queued_pr_untouched(self) -> None:
        # Already in the merge queue → do nothing; re-enqueuing/re-arming would disturb it.
        # Also never reads mergeStateStatus — a queued PR is never a BEHIND candidate here.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(True, True)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status"
        ) as merge_state, mock.patch.object(
            review_feedback_loop, "_enqueue_pr"
        ) as enqueue, mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 12)
        self.assertTrue(enabled)
        self.assertIsNone(arm_error)
        run.assert_not_called()
        enqueue.assert_not_called()
        merge_state.assert_not_called()

    def test_arm_auto_merge_enqueue_not_ready_is_non_fatal(self) -> None:
        # Enqueue is best-effort: a not-yet-ready PR can't be queued now, but it stays armed
        # (auto-merge enqueues it when green). Benign not-ready is _enqueue_pr → (False, None),
        # so this is success — armed True, and crucially NO error is surfaced.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node3"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(False, None)
        ), mock.patch.object(gh_cli, "_run"):
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 13)
        self.assertTrue(enabled)
        self.assertIsNone(arm_error)  # benign not-ready must not leak as an error

    def test_arm_auto_merge_surfaces_real_enqueue_failure(self) -> None:
        # A REAL enqueue failure (auth/API), distinct from benign not-ready, is surfaced as the
        # error while still reporting armed=True — so "armed but never queued" can't recur silently.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(True, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node4"
        ), mock.patch.object(
            review_feedback_loop,
            "_enqueue_pr",
            return_value=(False, "Resource not accessible by integration"),
        ), mock.patch.object(gh_cli, "_run"):
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 14)
        self.assertTrue(enabled)
        self.assertIsNotNone(arm_error)
        self.assertIn("enqueue was rejected", arm_error)
        self.assertIn("Resource not accessible", arm_error)

    def test_arm_auto_merge_skips_enqueue_when_node_id_missing(self) -> None:
        # Fail-open: if the node id can't be read, arming still succeeds and enqueue is skipped
        # (no _enqueue_pr call) — the armed auto-merge enqueues the PR when it goes green.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="CLEAN"
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value=None
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr"
        ) as enqueue, mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 15)
        self.assertTrue(enabled)
        self.assertIsNone(arm_error)
        run.assert_called_once_with(
            ["gh", "pr", "merge", "15", "--merge", "--auto"], check=True
        )
        enqueue.assert_not_called()

    def test_arm_auto_merge_updates_branch_when_behind_then_still_arms(self) -> None:
        # BEHIND means neither arming nor enqueuing can make the PR CLEAN — merge base in
        # first (the same recovery batch-arm-merge-queue.yml already does for this state),
        # then still arm as a backstop so it's ready to enqueue once CI recomputes it CLEAN.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="BEHIND"
        ), mock.patch.object(
            review_feedback_loop, "_update_branch", return_value=(True, None)
        ) as update_branch, mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node20"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(False, None)
        ), mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 20)
        self.assertTrue(enabled)
        self.assertIn("branch updated (was BEHIND)", arm_error)
        update_branch.assert_called_once_with("o", "r", 20)
        run.assert_called_once_with(["gh", "pr", "merge", "20", "--merge", "--auto"], check=True)

    def test_arm_auto_merge_still_arms_when_branch_update_fails(self) -> None:
        # A real update-branch failure (e.g. an actual conflict surfaced as DIRTY by the time
        # this ran) is surfaced as an informational note, not treated as arming having failed.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="BEHIND"
        ), mock.patch.object(
            review_feedback_loop, "_update_branch", return_value=(False, "merge conflict")
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node21"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(False, None)
        ), mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 21)
        self.assertTrue(enabled)
        self.assertIn("branch update (BEHIND) failed", arm_error)
        self.assertIn("merge conflict", arm_error)
        run.assert_called_once_with(["gh", "pr", "merge", "21", "--merge", "--auto"], check=True)

    def test_arm_auto_merge_aggregates_notes_when_branch_update_and_enqueue_both_fail(
        self,
    ) -> None:
        # Both failure notes must survive the join — neither overwrites the other.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(False, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="BEHIND"
        ), mock.patch.object(
            review_feedback_loop, "_update_branch", return_value=(False, "merge conflict")
        ), mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node23"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(False, "enqueue error")
        ), mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 23)
        self.assertTrue(enabled)
        self.assertIn("branch update (BEHIND) failed", arm_error)
        self.assertIn("merge conflict", arm_error)
        self.assertIn("enqueue was rejected", arm_error)
        self.assertIn("enqueue error", arm_error)
        run.assert_called_once_with(["gh", "pr", "merge", "23", "--merge", "--auto"], check=True)

    def test_arm_auto_merge_checks_behind_even_when_already_enabled(self) -> None:
        # A PR can already be armed and still fall BEHIND later — the BEHIND check does not
        # depend on `enabled`, so this must still trigger an update-branch attempt.
        with mock.patch.object(
            review_feedback_loop, "_auto_merge_state", return_value=(True, False)
        ), mock.patch.object(
            review_feedback_loop, "_merge_state_status", return_value="BEHIND"
        ), mock.patch.object(
            review_feedback_loop, "_update_branch", return_value=(True, None)
        ) as update_branch, mock.patch.object(
            review_feedback_loop, "_pr_node_id", return_value="PR_node22"
        ), mock.patch.object(
            review_feedback_loop, "_enqueue_pr", return_value=(False, None)
        ), mock.patch.object(gh_cli, "_run") as run:
            enabled, arm_error = review_feedback_loop._arm_auto_merge("o", "r", 22)
        self.assertTrue(enabled)
        self.assertIn("branch updated (was BEHIND)", arm_error)
        update_branch.assert_called_once_with("o", "r", 22)
        run.assert_not_called()  # already enabled — no redundant enable call

    def test_merge_state_status_returns_value_and_fails_open(self) -> None:
        with mock.patch.object(
            review_feedback_loop,
            "_graphql",
            return_value={"repository": {"pullRequest": {"mergeStateStatus": "BEHIND"}}},
        ):
            self.assertEqual(
                review_feedback_loop._merge_state_status("o", "r", 9), "BEHIND"
            )
        with mock.patch.object(review_feedback_loop, "_graphql", return_value={}):
            self.assertEqual(
                review_feedback_loop._merge_state_status("o", "r", 9), "UNKNOWN"
            )
        with mock.patch.object(
            review_feedback_loop, "_graphql", side_effect=RuntimeError("boom")
        ):
            self.assertEqual(
                review_feedback_loop._merge_state_status("o", "r", 9), "UNKNOWN"
            )
        with mock.patch.object(
            review_feedback_loop,
            "_graphql",
            return_value={"repository": {"pullRequest": {"mergeStateStatus": None}}},
        ):
            self.assertEqual(
                review_feedback_loop._merge_state_status("o", "r", 9), "UNKNOWN"
            )

    def test_update_branch_tri_state_success_and_failure(self) -> None:
        # Real owner/repo: gh_cli pins these engines to the repository they govern,
        # so a placeholder slug is now rejected before argv is built.
        with mock.patch.object(gh_cli, "_run") as run:
            ok, err = review_feedback_loop._update_branch("LAF-US", "IDAHO-VAULT", 9)
        self.assertTrue(ok)
        self.assertIsNone(err)
        run.assert_called_once_with(
            ["gh", "api", "--method", "PUT",
             "repos/LAF-US/IDAHO-VAULT/pulls/9/update-branch"],
            check=True,
        )
        with mock.patch.object(
            gh_cli, "_run", side_effect=RuntimeError("conflict")
        ):
            ok, err = review_feedback_loop._update_branch("LAF-US", "IDAHO-VAULT", 9)
        self.assertFalse(ok)
        self.assertEqual(err, "conflict")

    def test_enqueue_pr_tri_state_entry_notready_failure(self) -> None:
        # The enqueue primitive is tri-state:
        #   entry id present        → (True, None)   enqueued
        #   no entry (graphql ok)   → (False, None)  benign not-ready
        #   graphql raises          → (False, str)   real failure, surfaced
        with mock.patch.object(
            review_feedback_loop,
            "_graphql",
            return_value={"enqueuePullRequest": {"mergeQueueEntry": {"id": "MQE_1"}}},
        ):
            ok, err = review_feedback_loop._enqueue_pr("PR_node")
        self.assertTrue(ok)
        self.assertIsNone(err)
        with mock.patch.object(
            review_feedback_loop,
            "_graphql",
            return_value={"enqueuePullRequest": {"mergeQueueEntry": None}},
        ):
            ok, err = review_feedback_loop._enqueue_pr("PR_node")
        self.assertFalse(ok)
        self.assertIsNone(err)  # not-ready is benign — no error
        with mock.patch.object(
            review_feedback_loop, "_graphql", side_effect=RuntimeError("boom")
        ):
            ok, err = review_feedback_loop._enqueue_pr("PR_node")
        self.assertFalse(ok)
        self.assertEqual(err, "boom")

    def test_pr_node_id_returns_id_missing_keys_and_fail_open(self) -> None:
        # Normal response yields the id; missing repository/pullRequest keys and a raising
        # _graphql both fail open to None (so the caller skips enqueue rather than crashing).
        with mock.patch.object(
            review_feedback_loop,
            "_graphql",
            return_value={"repository": {"pullRequest": {"id": "PR_node9"}}},
        ):
            self.assertEqual(review_feedback_loop._pr_node_id("o", "r", 9), "PR_node9")
        with mock.patch.object(review_feedback_loop, "_graphql", return_value={}):
            self.assertIsNone(review_feedback_loop._pr_node_id("o", "r", 9))
        with mock.patch.object(
            review_feedback_loop, "_graphql", return_value={"repository": {"pullRequest": None}}
        ):
            self.assertIsNone(review_feedback_loop._pr_node_id("o", "r", 9))
        with mock.patch.object(
            review_feedback_loop, "_graphql", side_effect=RuntimeError("api down")
        ):
            self.assertIsNone(review_feedback_loop._pr_node_id("o", "r", 9))
        with mock.patch.object(
            review_feedback_loop, "_graphql", side_effect=ValueError("bad json")
        ):
            self.assertIsNone(review_feedback_loop._pr_node_id("o", "r", 9))

    # ----- guarded arm (#521/#527 reversal, 2026-06-17). The protected-path veto was
    # retired 2026-06-29 (K1/#627, K2/#628): the CODEOWNERS hard gate
    # (require_code_owner_review) now enforces "this path needs a human", so the engine no
    # longer vetoes protected paths — these tests assert the un-vetoed arm path. -----

    def test_maybe_arm_arms_eligible_pr(self) -> None:
        # On a successful arm, the merge/auto label is applied via a CHECKED gh call so the
        # write can fail-close (see test below). Mock the gh_cli run primitive for that edit.
        with mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ) as arm, mock.patch.object(
            gh_cli, "_run"
        ) as run:
            result = review_feedback_loop._maybe_arm_auto_merge(
                "o", "r", 5, {"eligible_for_auto_merge": True}
            )
        self.assertTrue(result["armed"])
        arm.assert_called_once_with("o", "r", 5)
        # The arm tags merge/auto so the disable path can later un-arm if it becomes blocked.
        run.assert_called_once_with(
            ["gh", "pr", "edit", "5", "--add-label", review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL],
            check=True,
        )

    def test_maybe_arm_fails_closed_when_label_write_fails(self) -> None:
        # If arming succeeds but the merge/auto label write fails, disable the auto-merge we
        # just enabled and report failure — never leave an armed PR the disable path can't track.
        with mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ), mock.patch.object(
            gh_cli, "_run", side_effect=RuntimeError("label write failed")
        ), mock.patch.object(
            review_feedback_loop, "_disable_auto_merge"
        ) as disable:
            result = review_feedback_loop._maybe_arm_auto_merge(
                "o", "r", 6, {"eligible_for_auto_merge": True}
            )
        self.assertFalse(result["armed"])
        self.assertIn("label write failed", result["reason"])
        disable.assert_called_once_with(6)

    def test_maybe_arm_noops_when_not_eligible(self) -> None:
        # Not eligible → never arms.
        with mock.patch.object(
            review_feedback_loop, "_arm_auto_merge"
        ) as arm:
            result = review_feedback_loop._maybe_arm_auto_merge(
                "o", "r", 7, {"eligible_for_auto_merge": False}
            )
        self.assertFalse(result["armed"])
        arm.assert_not_called()

    def test_sync_pr_arms_eligible_clear_pr_when_threads_clear(self) -> None:
        # End-to-end through sync_pr: a clear-pair (risk/—), grace-elapsed PR with no current
        # threads is armed (guarded). Mirrors "arm when the last blocking thread clears".
        now = datetime(2026, 4, 16, 3, 0, tzinfo=timezone.utc)
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            pr_number=200,
            sync_actor="someone",
            grace_minutes=30,
        )
        ready = _pr(
            number=200,
            created_at=now - timedelta(minutes=45),
            labels=(review_feedback_loop.RISK_CLEAR_LABEL,),
        )
        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop, "_fetch_pr", return_value=ready
        ), mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop, "_resolve_outdated_resolvable_threads", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ), mock.patch.object(
            gh_cli, "_run"
        ), mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ) as arm, contextlib.redirect_stdout(io.StringIO()):
            result = review_feedback_loop.sync_pr(args)
        self.assertEqual(result, 0)
        arm.assert_called_once_with("LAF-US", "IDAHO-VAULT", 200)

    def test_resolve_outdated_resolvable_attests_only_outdated_bot_threads(self) -> None:
        # The event-driven outdated-resolve: attest-resolves the OUTDATED bot thread and
        # leaves the current (substantive needs-fix) one alone — a caught error to fix,
        # not to dispose of.
        outdated = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True)
        outdated["id"] = "OUT"
        current = _thread(authors=("chatgpt-codex-connector",), author_type="Bot", outdated=False)
        current["id"] = "CUR"
        pr = _pr(threads=(outdated, current))
        seen: list[str] = []

        def fake_attest(pr_arg, thread_arg, looker, *a, **k):
            seen.append(thread_arg["id"])
            return {"thread_id": thread_arg["id"], "eligible": True, "applied": True, "reason": ""}

        with mock.patch.object(review_feedback_loop, "attest_and_resolve", side_effect=fake_attest):
            results = review_feedback_loop._resolve_outdated_resolvable_threads(
                pr, "github-actions[bot]", apply=True
            )
        self.assertEqual(seen, ["OUT"])  # only the outdated bot thread is touched
        self.assertEqual(sum(1 for r in results if r["applied"]), 1)

    def test_resolve_outdated_resolvable_records_failure_when_attest_raises(self) -> None:
        # A transient gh/GraphQL failure on one thread must not abort the pass: the thread
        # gets a non-applied result whose reason carries the error, so the JSON report (and
        # the stderr log) stay diagnosable.
        outdated = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True)
        outdated["id"] = "OUT"
        pr = _pr(threads=(outdated,))

        with mock.patch.object(
            review_feedback_loop,
            "attest_and_resolve",
            side_effect=RuntimeError("boom: attest failed"),
        ), contextlib.redirect_stderr(io.StringIO()):
            results = review_feedback_loop._resolve_outdated_resolvable_threads(
                pr, "github-actions[bot]", apply=True
            )

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["thread_id"], "OUT")
        self.assertFalse(result["eligible"])
        self.assertFalse(result["applied"])
        self.assertIn("boom: attest failed", result["reason"])

    def test_resolve_outdated_resolvable_resolves_looker_lazily(self) -> None:
        # When looker is omitted, _viewer_login() is paid for ONLY if there's a stale
        # thread to clear — a push with nothing outdated costs no extra round-trip.
        current = _thread(authors=("coderabbitai",), author_type="Bot", outdated=False)
        pr_no_work = _pr(threads=(current,))
        with mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ) as viewer_login, mock.patch.object(
            review_feedback_loop, "attest_and_resolve"
        ):
            review_feedback_loop._resolve_outdated_resolvable_threads(pr_no_work)
        viewer_login.assert_not_called()

        outdated = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True)
        pr_with_work = _pr(threads=(outdated,))
        with mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ) as viewer_login, mock.patch.object(
            review_feedback_loop, "attest_and_resolve"
        ) as attest:
            review_feedback_loop._resolve_outdated_resolvable_threads(pr_with_work)
        viewer_login.assert_called_once()
        # The lazily-resolved actor is the witness passed to attest_and_resolve.
        self.assertEqual(attest.call_args.args[2], "github-actions[bot]")

    def test_reconcile_open_prs_promotes_and_arms_eligible_clear_pair_pr(self) -> None:
        # K3/#629: a clear-pair (risk/—), grace-elapsed, unblocked PR is promoted to
        # merge/auto and armed for the merge queue. (A risk/low PR would HOLD instead.)
        args = SimpleNamespace(
            owner="LAF-US",
            repo="IDAHO-VAULT",
            grace_minutes=30,
        )
        ready_pr = _pr(
            number=88,
            created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
            labels=(review_feedback_loop.RISK_CLEAR_LABEL,),
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
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_resolvable_threads",
            return_value=[],
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
        edit_label.assert_any_call(88, add=review_feedback_loop.DEFAULT_AUTO_MERGE_LABEL)
        comment.assert_called_once()
        arm_auto_merge.assert_called_once_with("LAF-US", "IDAHO-VAULT", 88)

    def test_promote_ready_fails_loud_on_invariant_violation(self) -> None:
        # K4/#630: promote_ready shares reconcile's exit-code contract — non-zero when the
        # invariant tripped (CI red), zero otherwise. `promote_ready` reads the report via
        # dict.get, so the stub returns a dict (not a namespace).
        args = SimpleNamespace(owner="LAF-US", repo="IDAHO-VAULT", grace_minutes=30)

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop, "_build_reconciliation_report"
        ) as build_report, contextlib.redirect_stdout(io.StringIO()):
            build_report.return_value = {"invariant_violations": [{"number": 90, "error": "x"}]}
            self.assertEqual(review_feedback_loop.promote_ready(args), 1)

            build_report.return_value = {"invariant_violations": []}
            self.assertEqual(review_feedback_loop.promote_ready(args), 0)

    def test_reconcile_fails_loud_on_invariant_but_still_sweeps_rest(self) -> None:
        # K4/#630 fail-loud, right blast radius: a PR carrying risk/— alongside a flag trips
        # the invariant. The sweep records it, exits non-zero (CI red), yet still processes
        # every OTHER open PR — one mis-labeled PR must not starve the rest.
        args = SimpleNamespace(owner="LAF-US", repo="IDAHO-VAULT", grace_minutes=30)
        bad_pr = _pr(
            number=90,
            created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
            labels=(review_feedback_loop.RISK_CLEAR_LABEL, review_feedback_loop.RISK_LOW_LABEL),
        )
        good_pr = _pr(
            number=91,
            created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc),
            labels=(review_feedback_loop.RISK_CLEAR_LABEL,),
        )

        out = io.StringIO()
        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop, "_list_open_pr_numbers", return_value=[90, 91]
        ), mock.patch.object(
            review_feedback_loop, "_fetch_pr", side_effect=[bad_pr, good_pr]
        ), mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop, "_resolve_outdated_resolvable_threads", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ), mock.patch.object(
            review_feedback_loop, "_edit_label"
        ), mock.patch.object(
            review_feedback_loop, "_comment"
        ), mock.patch.object(
            review_feedback_loop, "_arm_auto_merge", return_value=(True, None)
        ) as arm_auto_merge, contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            result = review_feedback_loop.reconcile_open_prs(args)

        self.assertEqual(result, 1)  # fail loud → non-zero exit
        report = json.loads(out.getvalue())
        self.assertEqual([v["number"] for v in report["invariant_violations"]], [90])
        # The good PR was still armed — the sweep did not abort on the bad one.
        arm_auto_merge.assert_called_once_with("LAF-US", "IDAHO-VAULT", 91)

    def test_reconcile_open_prs_reports_auth_blocked_auto_merge(self) -> None:
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
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_resolvable_threads",
            return_value=[],
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

        # Reversal (2026-06-17): the PR is eligible and armed; the arm is rejected by the
        # protected base branch, so it is reported as authorization-blocked (not silently green).
        self.assertEqual(report["rearmed_prs"], [])
        self.assertEqual(report["auto_merge_authorization_blocked"], [89])
        self.assertEqual(
            report["evaluated"][0]["auto_merge_arm_error"],
            "GitHub Actions is not authorized to enable auto-merge on the protected base branch.",
        )

    def test_reconcile_resolves_outdated_via_witnessed_helper(self) -> None:
        # The scheduled reconcile lane no longer resolves blindly: it routes through the
        # WITNESSED, disposition-driven helper (the same one the event path uses), passing
        # the looker it resolved once for the batch, and counts only the applied results
        # into resolved_outdated_threads.
        pr88 = _pr(number=88, created_at=datetime(2026, 4, 16, 1, 0, tzinfo=timezone.utc))
        outdated_results = [
            {"thread_id": "A", "eligible": True, "applied": True, "reason": ""},
            {"thread_id": "B", "eligible": False, "applied": False, "reason": "blocked"},
        ]

        with mock.patch.object(review_feedback_loop, "ensure_labels"), mock.patch.object(
            review_feedback_loop, "_list_open_pr_numbers", return_value=[88]
        ), mock.patch.object(
            review_feedback_loop, "_fetch_pr", return_value=pr88
        ), mock.patch.object(
            review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"
        ), mock.patch.object(
            review_feedback_loop,
            "_resolve_outdated_resolvable_threads",
            return_value=outdated_results,
        ) as resolve_outdated, mock.patch.object(
            review_feedback_loop, "apply_review_state_projection", return_value=[]
        ):
            report = review_feedback_loop._build_reconciliation_report(
                "LAF-US", "IDAHO-VAULT", grace_minutes=30
            )

        # Witnessed by the actor resolved once for the batch walk, applying.
        resolve_outdated.assert_called_once()
        self.assertEqual(resolve_outdated.call_args.args[1], "github-actions[bot]")
        self.assertEqual(resolve_outdated.call_args.kwargs["apply"], True)
        # Only the one applied result is counted (not the blocked one).
        self.assertEqual(report["resolved_outdated_threads"], 1)

    def test_thread_has_attested_look_requires_self_attested_marker(self) -> None:
        # Valid: structured marker whose by= matches the comment's own author.
        looked = _thread(authors=("coderabbitai",))
        looked["comments"]["nodes"].append(
            {
                "author": {"login": "claude-code-bot"},
                "body": "advisory, no action <!-- looked: by=claude-code-bot; decision=advisory; v=1 -->",
                "url": "https://example.test/attestation",
            }
        )
        self.assertTrue(review_feedback_loop._thread_has_attested_look(looked))

        # No marker at all.
        self.assertFalse(
            review_feedback_loop._thread_has_attested_look(_thread(authors=("coderabbitai",)))
        )

        # Forged: marker present but by= does not match the author -> not a look.
        forged = _thread(authors=("coderabbitai",))
        forged["comments"]["nodes"].append(
            {
                "author": {"login": "random-user"},
                "body": "<!-- looked: by=someone-else; decision=advisory; v=1 -->",
                "url": "https://example.test/forged",
            }
        )
        self.assertFalse(review_feedback_loop._thread_has_attested_look(forged))

        # Nil-safe shapes: comments None, nodes None, comment missing body.
        nil_comments = _thread(authors=("coderabbitai",))
        nil_comments["comments"] = None
        nil_nodes = _thread(authors=("coderabbitai",))
        nil_nodes["comments"] = {"nodes": None}
        missing_body = _thread(authors=("coderabbitai",))
        missing_body["comments"]["nodes"].append({"author": {"login": "x"}, "url": "u"})
        self.assertFalse(review_feedback_loop._thread_has_attested_look(nil_comments))
        self.assertFalse(review_feedback_loop._thread_has_attested_look(nil_nodes))
        self.assertFalse(review_feedback_loop._thread_has_attested_look(missing_body))

    def test_build_looker_queue_unresolved_only_with_authors_and_looked_flag(self) -> None:
        looked_thread = _thread(authors=("coderabbitai",))
        looked_thread["comments"]["nodes"].append(
            {
                "author": {"login": "claude-code-bot"},
                "body": "<!-- looked: by=claude-code-bot; decision=advisory; v=1 -->",
                "url": "https://example.test/attestation",
            }
        )
        pr = _pr(
            number=42,
            threads=(
                _thread(authors=("coderabbitai", "human-reviewer", "coderabbitai")),
                looked_thread,
                _thread(resolved=True, authors=("copilot-pull-request-reviewer",)),
                _thread(outdated=True, authors=("human-reviewer",)),
            ),
        )

        with mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve_thread:
            items = review_feedback_loop._build_looker_queue(pr)

        resolve_thread.assert_not_called()
        self.assertEqual(len(items), 3)  # resolved thread excluded
        self.assertTrue(all(item["pr"] == 42 for item in items))
        # authors sorted + deduplicated; url from the first comment
        self.assertEqual(items[0]["authors"], ["coderabbitai", "human-reviewer"])
        self.assertEqual(items[0]["url"], "https://example.test/thread")
        self.assertFalse(items[0]["looked"])
        self.assertTrue(items[1]["looked"])
        self.assertTrue(any(item["is_outdated"] for item in items))

    # ----- Layer B1: pure core of attest_and_resolve -----

    def test_author_is_bot(self) -> None:
        self.assertTrue(
            pr_threads._author_is_bot({"login": "coderabbitai", "__typename": "Bot"})
        )
        self.assertTrue(pr_threads._author_is_bot({"login": "dependabot[bot]"}))
        self.assertFalse(
            pr_threads._author_is_bot({"login": "loganfinney27", "__typename": "User"})
        )
        self.assertFalse(pr_threads._author_is_bot({}))

    def test_thread_is_bot_only(self) -> None:
        bot_only = _thread(authors=("coderabbitai", "chatgpt-codex-connector"), author_type="Bot")
        self.assertTrue(review_feedback_loop._thread_is_bot_only(bot_only))

        human_only = _thread(authors=("human-reviewer",), author_type="User")
        self.assertFalse(review_feedback_loop._thread_is_bot_only(human_only))

        mixed = _thread(authors=("coderabbitai",), author_type="Bot")
        mixed["comments"]["nodes"].append(
            {"author": {"login": "human-reviewer", "__typename": "User"}, "body": "x", "url": "u"}
        )
        self.assertFalse(review_feedback_loop._thread_is_bot_only(mixed))

        empty = _thread(authors=(), author_type="Bot")
        self.assertFalse(review_feedback_loop._thread_is_bot_only(empty))

    def test_build_attestation_roundtrips_through_detector(self) -> None:
        body = review_feedback_loop._build_attestation(
            "claude-code-bot",
            "advisory",
            "advisory nit, no code change needed",
            now=datetime(2026, 6, 16, 1, 0, tzinfo=timezone.utc),
        )
        self.assertIn(review_feedback_loop.LOOK_ATTESTATION_MARKER, body)
        self.assertIn("by=claude-code-bot", body)
        self.assertIn("decision=advisory", body)

        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        thread["comments"]["nodes"].append(
            {"author": {"login": "claude-code-bot", "__typename": "Bot"}, "body": body, "url": "u"}
        )
        self.assertTrue(review_feedback_loop._thread_has_attested_look(thread))

    def test_build_attestation_rejects_unknown_decision(self) -> None:
        with self.assertRaises(ValueError):
            review_feedback_loop._build_attestation("claude-code-bot", "bogus", "x")

    def test_build_attestation_accepts_bot_identity_looker(self) -> None:
        # B2 decision: a looker may sign under its native App/CI identity, e.g.
        # github-actions[bot]. The attestation still round-trips through the detector.
        body = review_feedback_loop._build_attestation(
            "github-actions[bot]", "advisory", "advisory; no change needed"
        )
        self.assertIn("by=github-actions[bot]", body)
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        thread["comments"]["nodes"].append(
            {
                "author": {"login": "github-actions[bot]", "__typename": "Bot"},
                "body": body,
                "url": "u",
            }
        )
        self.assertTrue(review_feedback_loop._thread_has_attested_look(thread))

    def test_build_attestation_rejects_malformed_looker(self) -> None:
        for bad in ("has space", "a/b", "[bot]", "", "-leading"):
            with self.assertRaises(ValueError):
                review_feedback_loop._build_attestation(bad, "advisory", "x")

    def test_build_attestation_normalizes_timestamp_to_utc_zulu(self) -> None:
        # naive datetime is treated as UTC (never local)
        naive = datetime(2026, 6, 16, 1, 0)
        self.assertIn(
            "at=2026-06-16T01:00:00Z",
            review_feedback_loop._build_attestation("claude-code-bot", "advisory", "x", now=naive),
        )
        # tz-aware non-UTC datetime is converted to UTC
        plus5 = datetime(2026, 6, 16, 6, 0, tzinfo=timezone(timedelta(hours=5)))
        self.assertIn(
            "at=2026-06-16T01:00:00Z",
            review_feedback_loop._build_attestation("claude-code-bot", "advisory", "x", now=plus5),
        )


    # ----- Layer B2: attest_and_resolve (the guarded disposition core) -----

    def test_attest_and_resolve_dry_run_writes_nothing(self) -> None:
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok"
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertTrue(result["eligible"])
        self.assertFalse(result["applied"])
        self.assertIn(review_feedback_loop.LOOK_ATTESTATION_MARKER, result["attestation"])

    def test_attest_and_resolve_apply_resolves_then_attests(self) -> None:
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        pr = _pr(threads=(thread,))
        manager = mock.Mock()
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="claude-code-bot"), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            manager.attach_mock(reply, "reply")
            manager.attach_mock(resolve, "resolve")
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        # resolve, THEN attest — the "cleared" attestation is posted only after the
        # resolve succeeds, so it can never claim a clearing that did not happen.
        manager.assert_has_calls(
            [mock.call.resolve("THREAD_1"), mock.call.reply("THREAD_1", mock.ANY)]
        )
        self.assertTrue(result["applied"])

    def test_attest_and_resolve_no_false_witness_when_resolve_forbidden(self) -> None:
        # The live #398 boundary: resolveReviewThread is FORBIDDEN for the integration
        # token. The resolve must run FIRST and raise BEFORE any attestation is posted —
        # so a thread that could not be cleared never gains a "thread cleared" comment.
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread",
                               side_effect=RuntimeError("FORBIDDEN: Resource not accessible by integration")) as resolve:
            with self.assertRaises(RuntimeError):
                review_feedback_loop.attest_and_resolve(
                    pr, thread, "github-actions[bot]", "advisory", "ok", apply=True
                )
        resolve.assert_called_once_with("THREAD_1")
        reply.assert_not_called()  # NO false "cleared" attestation left behind

    def test_attest_and_resolve_skips_human_thread(self) -> None:
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        thread["comments"]["nodes"].append(
            {"author": {"login": "loganfinney27", "__typename": "User"}, "body": "x", "url": "u"}
        )
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertFalse(result["eligible"])
        self.assertIn("not bot-authored", result["reason"])

    def test_attest_and_resolve_skips_changes_requested(self) -> None:
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        pr = _pr(review_decision="CHANGES_REQUESTED", threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertFalse(result["eligible"])
        self.assertIn("CHANGES_REQUESTED", result["reason"])

    def test_attest_and_resolve_recovers_partial_success_without_duplicate(self) -> None:
        # A prior run posted the attestation but the resolve failed: the thread is
        # attested yet still OPEN. A retry must resolve it WITHOUT re-posting the look.
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        body = review_feedback_loop._build_attestation("claude-code-bot", "advisory", "ok")
        thread["comments"]["nodes"].append(
            {"author": {"login": "claude-code-bot", "__typename": "Bot"}, "body": body, "url": "u"}
        )
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()  # no duplicate attestation
        resolve.assert_called_once_with("THREAD_1")  # but it DOES resolve
        self.assertTrue(result["applied"])
        self.assertIn("existing attested look", result["reason"])

    def test_attest_and_resolve_skips_resolved_thread(self) -> None:
        thread = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertIn("already resolved", result["reason"])

    def test_attest_and_resolve_refuses_paginated_comments(self) -> None:
        # Bot-only cannot be proven from a truncated comment page — refuse.
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        thread["comments"]["pageInfo"] = {"hasNextPage": True}
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertFalse(result["eligible"])
        self.assertIn("paginated", result["reason"])

    def test_attest_and_resolve_refuses_actor_mismatch(self) -> None:
        # Self-attested: a looker that differs from the authenticated actor would post
        # an undetectable attestation — refuse before any write.
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="github-actions[bot]"), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.attest_and_resolve(
                pr, thread, "claude-code-bot", "advisory", "ok", apply=True
            )
        reply.assert_not_called()
        resolve.assert_not_called()
        self.assertFalse(result["eligible"])
        self.assertIn("does not match", result["reason"])

    def test_attest_and_resolve_reports_missing_thread_id(self) -> None:
        thread = _thread(authors=("coderabbitai",), author_type="Bot")
        thread["id"] = None
        pr = _pr(threads=(thread,))
        result = review_feedback_loop.attest_and_resolve(
            pr, thread, "claude-code-bot", "advisory", "ok", apply=True
        )
        self.assertFalse(result["eligible"])
        self.assertIn("no id", result["reason"])

    def test_attest_resolve_cli_dispatches_dry_run(self) -> None:
        # parser + handler wiring smoke test (dry-run; no writes)
        args = review_feedback_loop.build_parser().parse_args(
            [
                "attest-resolve", "--owner", "o", "--repo", "r", "--pr-number", "7",
                "--thread-id", "THREAD_1", "--looker", "claude-code-bot",
                "--decision", "advisory", "--rationale", "ok",
            ]
        )
        self.assertEqual(args.command, "attest-resolve")
        self.assertFalse(args.apply)
        pr = _pr(number=7, threads=(_thread(authors=("coderabbitai",), author_type="Bot"),))
        with mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            rc = review_feedback_loop.attest_resolve(args)
        self.assertEqual(rc, 0)
        reply.assert_not_called()
        resolve.assert_not_called()

    def test_attest_resolve_looker_defaults_to_authenticated_actor(self) -> None:
        # Parity with engage_outdated: when --looker is omitted (None), attest_resolve
        # defaults the witness to the authenticated actor (_viewer_login) and forwards it.
        args = review_feedback_loop.build_parser().parse_args(
            [
                "attest-resolve", "--owner", "o", "--repo", "r", "--pr-number", "7",
                "--thread-id", "THREAD_1", "--decision", "advisory", "--rationale", "ok",
            ]
        )
        self.assertIsNone(args.looker)  # --looker omitted
        pr = _pr(number=7, threads=(_thread(authors=("coderabbitai",), author_type="Bot"),))
        seen_looker = []

        def fake_attest(pr_arg, thread_arg, looker, *a, **k):
            seen_looker.append(looker)
            return {"thread_id": thread_arg.get("id"), "eligible": True, "applied": False, "reason": ""}

        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="loganfinney27") as viewer, \
             mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
             mock.patch.object(review_feedback_loop, "attest_and_resolve", side_effect=fake_attest), \
             contextlib.redirect_stdout(io.StringIO()):
            rc = review_feedback_loop.attest_resolve(args)
        self.assertEqual(rc, 0)
        viewer.assert_called_once()
        self.assertEqual(seen_looker, ["loganfinney27"])

    def test_attest_resolve_cli_rejects_cross_pr_thread(self) -> None:
        # The target thread isn't in the PR's first-100 window; the global node fetch
        # returns one whose links point at a DIFFERENT PR — reject, never act on it.
        args = review_feedback_loop.build_parser().parse_args(
            [
                "attest-resolve", "--owner", "laf-us", "--repo", "idaho-vault",
                "--pr-number", "7", "--thread-id", "GLOBAL_ID", "--looker",
                "claude-code-bot", "--decision", "advisory", "--apply",
            ]
        )
        pr = _pr(number=7, threads=())  # target thread not in the window
        foreign = _thread(authors=("coderabbitai",), author_type="Bot")
        foreign["comments"]["nodes"][0]["url"] = (
            "https://github.com/laf-us/idaho-vault/pull/999#discussion_r1"
        )
        with mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
             mock.patch.object(review_feedback_loop, "_fetch_thread", return_value=foreign), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            rc = review_feedback_loop.attest_resolve(args)
        self.assertEqual(rc, 1)
        reply.assert_not_called()
        resolve.assert_not_called()


    # ----- Layer C: looker-walk classification (read-only) -----

    def _bot_thread(self) -> dict[str, object]:
        return _thread(authors=("coderabbitai",), author_type="Bot")

    def test_classify_needs_fix_is_machine_lane_but_not_drainable(self) -> None:
        # A plain bot prose finding is the coarse machine-disposable LANE, but it is a
        # needs-fix (substantive) thread — NOT safe_to_drain. A bare attest-resolve would
        # rubber-stamp a caught error. (codex review on #529.)
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=1, created_at=now - timedelta(days=1), threads=(self._bot_thread(),))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "machine-disposable")
        self.assertEqual(report["threads"][0]["resolution"], "needs-fix")
        self.assertFalse(report["safe_to_drain"])
        self.assertFalse(report["stale"])

    def test_classify_outdated_bot_thread_is_safe_to_drain(self) -> None:
        # Bare-resolvable: an outdated bot-only thread (referenced lines moved) is the one
        # non-stale case a bare attest-resolve may clear without a fix.
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True)
        pr = _pr(number=14, created_at=now - timedelta(days=1), threads=(thread,))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["resolution"], "outdated-resolvable")
        self.assertEqual(report["lane"], "machine-disposable")
        self.assertTrue(report["safe_to_drain"])

    def test_classify_would_cascade_when_auto_merge_armed(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=2, created_at=now - timedelta(days=1),
            auto_merge_enabled=True, threads=(self._bot_thread(),),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "would-cascade")
        self.assertFalse(report["safe_to_drain"])

    def test_classify_needs_human_on_human_thread(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=3, created_at=now - timedelta(days=1),
            threads=(_thread(authors=("loganfinney27",), author_type="User"),),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")
        self.assertFalse(report["safe_to_drain"])

    def test_classify_needs_human_on_changes_requested(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=4, created_at=now - timedelta(days=1),
            review_decision="CHANGES_REQUESTED", threads=(self._bot_thread(),),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")

    def test_classify_needs_human_on_truncated_comments(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = self._bot_thread()
        thread["comments"]["pageInfo"] = {"hasNextPage": True}
        pr = _pr(number=5, created_at=now - timedelta(days=1), threads=(thread,))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")
        self.assertEqual(report["unprovable_threads"], 1)

    def test_classify_clear_when_no_unresolved(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=6, created_at=now - timedelta(days=1),
            threads=(_thread(resolved=True, authors=("coderabbitai",), author_type="Bot"),),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "clear")

    def test_classify_stale_is_never_safe_to_drain(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=7, created_at=now - timedelta(days=30), threads=(self._bot_thread(),))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now, stale_days=14)
        self.assertEqual(report["lane"], "machine-disposable")  # threads are clearable...
        self.assertTrue(report["stale"])  # ...but it's abandoned
        self.assertFalse(report["safe_to_drain"])  # so never auto-drained

    def _looked_open_thread(self) -> dict[str, object]:
        thread = self._bot_thread()
        body = review_feedback_loop._build_attestation("claude-code-bot", "advisory", "ok")
        thread["comments"]["nodes"].append(
            {"author": {"login": "claude-code-bot", "__typename": "Bot"}, "body": body, "url": "u"}
        )
        return thread

    def test_classify_looked_open_is_machine_clearable(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=9, created_at=now - timedelta(days=1), threads=(self._looked_open_thread(),))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["disposition"], "looked-open")
        self.assertEqual(report["machine_clearable"], 1)
        self.assertEqual(report["lane"], "machine-disposable")  # recoverable, clearable

    def test_classify_human_on_truncated_page_is_human_not_unprovable(self) -> None:
        # A human on the page we DO have is definitive — truncation must not mask it.
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = _thread(authors=("loganfinney27",), author_type="User")
        thread["comments"]["pageInfo"] = {"hasNextPage": True}
        pr = _pr(number=10, created_at=now - timedelta(days=1), threads=(thread,))
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["disposition"], "human")
        self.assertEqual(report["human_threads"], 1)
        self.assertEqual(report["unprovable_threads"], 0)
        self.assertEqual(report["lane"], "needs-human")

    def test_classify_needs_human_on_mixed_human_and_bot(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        human = _thread(authors=("loganfinney27",), author_type="User")
        pr = _pr(
            number=11, created_at=now - timedelta(days=1),
            threads=(human, self._bot_thread()),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")  # any human forces it
        self.assertEqual(report["machine_clearable"], 1)  # the bot thread, still counted
        self.assertEqual(report["human_threads"], 1)

    def test_classify_needs_human_on_truncated_thread_list(self) -> None:
        # reviewThreads itself is paginated: a blocking thread may lie beyond page 1.
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=12, created_at=now - timedelta(days=1),
            threads=(self._bot_thread(),), threads_truncated=True,
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertTrue(report["threads_truncated"])
        self.assertEqual(report["lane"], "needs-human")
        self.assertFalse(report["safe_to_drain"])

    def test_classify_stale_uses_updated_at_over_created_at(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=13, created_at=now - timedelta(days=30),
            updated_at=now - timedelta(days=1),
            threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now, stale_days=14)
        self.assertFalse(report["stale"])  # recent activity wins over old creation
        self.assertTrue(report["safe_to_drain"])  # bare-resolvable (outdated) + not stale

    def test_stale_days_rejects_non_positive(self) -> None:
        for bad in ("0", "-1"):
            with self.assertRaises(SystemExit):
                review_feedback_loop.build_parser().parse_args(
                    ["looker-walk", "--owner", "o", "--repo", "r", "--stale-days", bad]
                )

    def test_looker_walk_is_read_only_and_emits_json(self) -> None:
        pr = _pr(number=8, created_at=datetime(2026, 6, 15, tzinfo=timezone.utc),
                 threads=(self._bot_thread(),))
        args = review_feedback_loop.build_parser().parse_args(
            ["looker-walk", "--owner", "o", "--repo", "r"]
        )
        buf = io.StringIO()
        with mock.patch.object(review_feedback_loop, "_list_open_pr_numbers", return_value=[8]), \
             mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve, \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             contextlib.redirect_stdout(buf):
            rc = review_feedback_loop.looker_walk(args)
        self.assertEqual(rc, 0)
        resolve.assert_not_called()
        reply.assert_not_called()
        data = json.loads(buf.getvalue())
        self.assertEqual(data["open_prs"], 1)
        self.assertEqual(data["by_lane"], {"machine-disposable": 1})
        self.assertIsInstance(data["safe_to_drain"], list)
        self.assertEqual(data["reports"][0]["pr"], 8)
        self.assertEqual(data["reports"][0]["lane"], "machine-disposable")

    # ----- Resolution disposition (#399 engine): HOW each thread gets resolved -----

    SUGGESTION_BODY = "Wrong value.\n\n```suggestion\ncorrected = True\n```\n"

    def test_has_committable_suggestion_detects_block(self) -> None:
        t = _thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY)
        self.assertTrue(pr_threads._thread_has_committable_suggestion(t))

    def test_has_committable_suggestion_false_on_prose(self) -> None:
        t = _thread(authors=("coderabbitai",), author_type="Bot", body="Consider fixing X.")
        self.assertFalse(pr_threads._thread_has_committable_suggestion(t))

    def test_resolution_apply_suggestion(self) -> None:
        t = _thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY)
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "apply-suggestion")

    def test_resolution_needs_fix_on_substantive_prose(self) -> None:
        # The dam's reality (#474): bot-authored, substantive, no mechanical fix.
        t = _thread(authors=("chatgpt-codex-connector",), author_type="Bot", body="Sabrina's name is wrong.")
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "needs-fix")

    def test_resolution_outdated_beats_suggestion(self) -> None:
        # An outdated comment's suggestion can't apply (lines moved) -> resolvable as stale.
        t = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True, body=self.SUGGESTION_BODY)
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "outdated-resolvable")

    def test_resolution_needs_human_on_human_author(self) -> None:
        t = _thread(authors=("loganfinney27",), author_type="User", body="please fix")
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "needs-human")

    def test_resolution_needs_human_on_truncated_page(self) -> None:
        t = _thread(authors=("coderabbitai",), author_type="Bot", body="prose")
        t["comments"]["pageInfo"] = {"hasNextPage": True}
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "needs-human")

    def test_resolution_looked_when_attested(self) -> None:
        looker = "claude-code-bot"
        body = review_feedback_loop._build_attestation(looker, "advisory", "ok")
        t = _thread(authors=(looker,), author_type="Bot", body=body)
        self.assertEqual(review_feedback_loop._thread_resolution_disposition(t), "looked")

    def test_classify_surfaces_resolution_and_counts(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=1,
            created_at=now - timedelta(days=1),
            threads=(
                _thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY),
                _thread(authors=("chatgpt-codex-connector",), author_type="Bot", body="prose finding"),
            ),
        )
        report = review_feedback_loop._classify_pr_for_looker(pr, now=now)
        self.assertEqual(sorted(t["resolution"] for t in report["threads"]), ["apply-suggestion", "needs-fix"])
        self.assertEqual(report["resolution_counts"], {"apply-suggestion": 1, "needs-fix": 1})

    # ----- Propose-only surfacing of committable suggestions (#3, 2026-06-19) -----

    def test_committable_suggestion_count_counts_only_ready_apply_suggestion_threads(self) -> None:
        # One ready suggestion (counted), one resolved suggestion (skipped), one prose
        # needs-fix (not a suggestion), one outdated suggestion (outdated-resolvable, not
        # apply-suggestion). Only the first counts.
        pr = _pr(
            threads=(
                _thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY),
                _thread(
                    authors=("coderabbitai",), author_type="Bot",
                    body=self.SUGGESTION_BODY, resolved=True,
                ),
                _thread(authors=("chatgpt-codex-connector",), author_type="Bot", body="prose"),
                _thread(
                    authors=("coderabbitai",), author_type="Bot",
                    outdated=True, body=self.SUGGESTION_BODY,
                ),
            )
        )
        self.assertEqual(review_feedback_loop._count_committable_suggestion_threads(pr), 1)

    def test_state_surfaces_committable_suggestion_count(self) -> None:
        state = review_feedback_loop.evaluate_review_state(
            _pr(threads=(_thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY),))
        )
        self.assertEqual(state["committable_suggestion_threads"], 1)

    def test_projection_adds_suggestions_ready_label_when_present(self) -> None:
        # Propose-only: a PR with a committable suggestion is flagged review/suggestions-ready
        # (the engine surfaces it; it does NOT commit the diff).
        state = review_feedback_loop.evaluate_review_state(
            _pr(threads=(_thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY),))
        )
        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, \
                mock.patch.object(review_feedback_loop, "_disable_auto_merge"):
            actions = review_feedback_loop.apply_review_state_projection(17, state)
        self.assertIn(f"add:{review_feedback_loop.DEFAULT_SUGGESTIONS_LABEL}", actions)
        edit_label.assert_any_call(17, add=review_feedback_loop.DEFAULT_SUGGESTIONS_LABEL)

    def test_projection_removes_suggestions_ready_label_when_absent(self) -> None:
        # The label clears (idempotently) once no committable suggestions remain — e.g.
        # after they were applied and the threads resolved.
        state = review_feedback_loop.evaluate_review_state(
            _pr(labels=(review_feedback_loop.DEFAULT_SUGGESTIONS_LABEL,))
        )
        with mock.patch.object(review_feedback_loop, "_edit_label") as edit_label, \
                mock.patch.object(review_feedback_loop, "_disable_auto_merge"):
            actions = review_feedback_loop.apply_review_state_projection(17, state)
        self.assertIn(f"remove:{review_feedback_loop.DEFAULT_SUGGESTIONS_LABEL}", actions)
        edit_label.assert_any_call(17, remove=review_feedback_loop.DEFAULT_SUGGESTIONS_LABEL)

    # ----- render_looker_worklist: read-only durable-issue triage surface -----

    def test_render_looker_worklist_is_read_only_triage_markdown(self) -> None:
        report = {
            "open_prs": 3,
            "by_lane": {"machine-disposable": 1, "needs-human": 1, "clear": 1},
            "by_resolution": {"needs-fix": 2, "outdated-resolvable": 1},
            "stale": 1,
            "safe_to_drain": [42],
            "reports": [
                {"pr": 42, "lane": "machine-disposable", "stale": False, "auto_merge_armed": False,
                 "unresolved_threads": 1, "resolution_counts": {"outdated-resolvable": 1}},
                {"pr": 7, "lane": "needs-human", "stale": True, "auto_merge_armed": True,
                 "unresolved_threads": 2, "resolution_counts": {"needs-fix": 2}},
                {"pr": 9, "lane": "clear", "stale": False, "auto_merge_armed": False,
                 "unresolved_threads": 0, "resolution_counts": {}},
            ],
        }
        md = review_feedback_loop.render_looker_worklist(report)
        self.assertIn("No threads resolved, no PRs merged", md)  # read-only framing
        self.assertIn("**Open PRs:** 3", md)
        self.assertIn("machine-disposable: 1", md)
        self.assertIn("needs-fix: 2", md)
        self.assertIn("- #42", md)  # safe_to_drain
        self.assertIn("**#7**", md)  # actionable PR surfaced
        self.assertIn("auto-merge-armed", md)  # flagged
        self.assertNotIn("**#9**", md)  # clear PR (0 unresolved) omitted from worklist

    def test_render_looker_worklist_handles_empty_report(self) -> None:
        md = review_feedback_loop.render_looker_worklist({})
        self.assertIn("**Open PRs:** 0", md)
        self.assertIn("none", md)

    def test_render_looker_worklist_surfaces_truncated_needs_human(self) -> None:
        # Truncated past page 1: lane needs-human, 0 VISIBLE unresolved. Must still surface
        # (the census can't prove it clear) and be flagged truncated. (codex review on #531.)
        report = {
            "open_prs": 1, "by_lane": {"needs-human": 1}, "by_resolution": {},
            "stale": 0, "safe_to_drain": [],
            "reports": [{"pr": 88, "lane": "needs-human", "stale": False,
                         "auto_merge_armed": False, "threads_truncated": True,
                         "unresolved_threads": 0, "resolution_counts": {}}],
        }
        md = review_feedback_loop.render_looker_worklist(report)
        self.assertIn("**#88**", md)  # surfaced despite 0 visible unresolved
        self.assertIn("threads-truncated", md)

    # ----- engage-outdated: the first 'engage' step (outdated-only) -----

    def test_engage_outdated_acts_only_on_outdated_resolvable(self) -> None:
        # Touches ONLY outdated-resolvable threads — never needs-fix or apply-suggestion —
        # with decision 'advisory', honoring --apply. (Logan: outdated-only to start.)
        pr = _pr(
            number=7,
            threads=(
                _thread(authors=("coderabbitai",), author_type="Bot", outdated=True),            # outdated-resolvable
                _thread(authors=("coderabbitai",), author_type="Bot", body="prose finding"),     # needs-fix
                _thread(authors=("coderabbitai",), author_type="Bot", body=self.SUGGESTION_BODY), # apply-suggestion
            ),
        )
        calls = []

        def fake_attest(pr_arg, thread_arg, looker, decision, rationale, *, apply, now=None):
            calls.append({"decision": decision, "looker": looker, "apply": apply})
            return {"thread_id": thread_arg.get("id"), "eligible": True, "applied": apply, "reason": ""}

        args = SimpleNamespace(owner="o", repo="r", looker="github-actions[bot]", apply=True)
        with mock.patch.object(review_feedback_loop, "_list_open_pr_numbers", return_value=[7]), \
                mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
                mock.patch.object(review_feedback_loop, "attest_and_resolve", side_effect=fake_attest), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = review_feedback_loop.engage_outdated(args)
        self.assertEqual(rc, 0)
        self.assertEqual(len(calls), 1)  # only the outdated-resolvable thread
        self.assertEqual(calls[0]["decision"], "advisory")
        self.assertEqual(calls[0]["looker"], "github-actions[bot]")
        self.assertTrue(calls[0]["apply"])

    def test_engage_outdated_continues_past_a_thread_failure(self) -> None:
        # One thread's transient gh/GraphQL failure must not abort the backlog pass —
        # the rest are still processed and the run completes. (CodeRabbit review on #534.)
        pr1 = _pr(number=1, threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),))
        pr2 = _pr(number=2, threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),))
        seen = []

        def flaky(pr_arg, thread_arg, *a, **k):
            seen.append(pr_arg.get("number"))
            if pr_arg.get("number") == 1:
                raise RuntimeError("transient gh failure")
            return {"thread_id": thread_arg.get("id"), "eligible": True, "applied": True, "reason": ""}

        args = SimpleNamespace(owner="o", repo="r", looker="github-actions[bot]", apply=True)
        with mock.patch.object(review_feedback_loop, "_list_open_pr_numbers", return_value=[1, 2]), \
                mock.patch.object(review_feedback_loop, "_fetch_pr", side_effect=lambda o, r, n: {1: pr1, 2: pr2}[n]), \
                mock.patch.object(review_feedback_loop, "attest_and_resolve", side_effect=flaky), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = review_feedback_loop.engage_outdated(args)
        self.assertEqual(rc, 0)
        self.assertEqual(seen, [1, 2])  # did NOT abort after PR #1 raised

    # ----- reconcile-witness: backfill the unwitnessed ending (#399) -----

    def test_backfill_witness_posts_missing_attestation_for_our_resolve(self) -> None:
        # Resolved + bot-only + unattested + resolvedBy == looker → backfill the look.
        # It posts the attestation and NEVER resolves/unresolves (already resolved).
        thread = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot",
                         resolved_by="loganfinney27")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="loganfinney27"), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply, \
             mock.patch.object(review_feedback_loop, "_resolve_thread") as resolve:
            result = review_feedback_loop.backfill_witness(
                pr, thread, "loganfinney27", "ok", apply=True
            )
        reply.assert_called_once()      # the missing witness is posted
        resolve.assert_not_called()     # never resolves/unresolves
        self.assertTrue(result["applied"])
        self.assertIn(review_feedback_loop.LOOK_ATTESTATION_MARKER, result["attestation"])

    def test_backfill_witness_refuses_when_resolved_by_another_identity(self) -> None:
        # The truthfulness line: a thread a HUMAN (or any non-looker) resolved must NOT
        # gain a witness from us — we never forge a look for someone else's resolve.
        thread = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot",
                         resolved_by="some-human")
        pr = _pr(threads=(thread,))
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply:
            result = review_feedback_loop.backfill_witness(
                pr, thread, "loganfinney27", "ok", apply=True
            )
        reply.assert_not_called()
        self.assertFalse(result["eligible"])
        self.assertIn("refusing to witness", result["reason"])

    def test_backfill_witness_skips_already_attested_and_unresolved(self) -> None:
        looker = "loganfinney27"
        # Already-attested resolved thread → no-op.
        body = review_feedback_loop._build_attestation(looker, "advisory", "ok")
        attested = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot",
                           resolved_by=looker)
        attested["comments"]["nodes"].append(
            {"author": {"login": looker, "__typename": "User"}, "body": body, "url": "u"}
        )
        # Unresolved thread → not a backfill target.
        unresolved = _thread(resolved=False, authors=("coderabbitai",), author_type="Bot",
                             resolved_by=None)
        pr = _pr()
        with mock.patch.object(review_feedback_loop, "_add_thread_reply") as reply:
            r1 = review_feedback_loop.backfill_witness(pr, attested, looker, "ok", apply=True)
            r2 = review_feedback_loop.backfill_witness(pr, unresolved, looker, "ok", apply=True)
        reply.assert_not_called()
        self.assertIn("already carries an attested look", r1["reason"])
        self.assertIn("not resolved", r2["reason"])

    def test_reconcile_witness_defaults_looker_and_backfills(self) -> None:
        # The walker: --looker omitted → defaults to the authenticated actor; backfills
        # only the resolved-bot-only-unattested thread we resolved.
        ours = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot",
                       resolved_by="loganfinney27")
        ours["id"] = "OURS"
        theirs = _thread(resolved=True, authors=("coderabbitai",), author_type="Bot",
                         resolved_by="some-human")
        theirs["id"] = "THEIRS"
        pr = _pr(number=7, threads=(ours, theirs))
        posted = []
        args = SimpleNamespace(owner="o", repo="r", looker=None, pr=None, rationale="", apply=True)
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="loganfinney27") as viewer, \
             mock.patch.object(review_feedback_loop, "_list_open_pr_numbers", return_value=[7]), \
             mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
             mock.patch.object(review_feedback_loop, "_add_thread_reply",
                               side_effect=lambda tid, body: posted.append(tid)), \
             contextlib.redirect_stdout(io.StringIO()) as out:
            rc = review_feedback_loop.reconcile_witness(args)
        self.assertEqual(rc, 0)
        viewer.assert_called()                  # looker defaulted to the actor
        self.assertEqual(posted, ["OURS"])      # only the thread WE resolved got the witness
        report = json.loads(out.getvalue())
        self.assertEqual(report["looker"], "loganfinney27")
        self.assertEqual(report["backfilled"], 1)

    def test_engage_outdated_looker_defaults_to_authenticated_actor(self) -> None:
        # Agent-driven operation: when --looker is not given (args.looker is None), the
        # witness defaults to the authenticated actor (_viewer_login), so the attestation
        # truthfully names whoever actually ran the resolve — not a hardcoded bot.
        pr = _pr(number=7, threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),))
        seen_looker = []

        def fake_attest(pr_arg, thread_arg, looker, *a, **k):
            seen_looker.append(looker)
            return {"thread_id": thread_arg.get("id"), "eligible": True, "applied": False, "reason": ""}

        args = SimpleNamespace(owner="o", repo="r", looker=None, apply=False)
        with mock.patch.object(review_feedback_loop, "_viewer_login", return_value="loganfinney27") as viewer, \
                mock.patch.object(review_feedback_loop, "_list_open_pr_numbers", return_value=[7]), \
                mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=pr), \
                mock.patch.object(review_feedback_loop, "attest_and_resolve", side_effect=fake_attest), \
                contextlib.redirect_stdout(io.StringIO()):
            rc = review_feedback_loop.engage_outdated(args)
        self.assertEqual(rc, 0)
        viewer.assert_called_once()             # resolved the actor once for the run
        self.assertEqual(seen_looker, ["loganfinney27"])  # witness names the real actor

    def test_engage_outdated_pr_scope_targets_one_pr(self) -> None:
        # --pr scopes the pass to a single PR (the guinea-pig case): the backlog walk is
        # bypassed entirely and only the named PR is fetched/processed. (Logan: #481 is the
        # ideal guinea pig for this step.)
        pr = _pr(number=481, threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),))
        fetched = []

        def fake_fetch(owner, repo, number):
            fetched.append(number)
            return pr

        args = SimpleNamespace(owner="o", repo="r", looker="github-actions[bot]", apply=False, pr=481)
        with mock.patch.object(review_feedback_loop, "_list_open_pr_numbers") as list_all, \
                mock.patch.object(review_feedback_loop, "_fetch_pr", side_effect=fake_fetch), \
                mock.patch.object(review_feedback_loop, "attest_and_resolve",
                                  side_effect=lambda p, t, *a, **k: {"thread_id": t.get("id"), "eligible": True, "applied": False, "reason": ""}), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            rc = review_feedback_loop.engage_outdated(args)
        self.assertEqual(rc, 0)
        list_all.assert_not_called()      # the backlog walk is bypassed under --pr
        self.assertEqual(fetched, [481])  # only the named PR is fetched
        self.assertEqual(json.loads(out.getvalue())["scope_pr"], 481)

    def test_engage_outdated_pr_scope_refuses_non_open_pr(self) -> None:
        # engage-outdated acts only on the open queue. The backlog walk only yields open
        # PRs; a --pr scope must hold the same invariant — a closed/merged PR is refused,
        # not engaged. (Sourcery review on #536.)
        closed = _pr(number=481, state="CLOSED",
                     threads=(_thread(authors=("coderabbitai",), author_type="Bot", outdated=True),))
        attested = []
        args = SimpleNamespace(owner="o", repo="r", looker="github-actions[bot]", apply=True, pr=481)
        with mock.patch.object(review_feedback_loop, "_fetch_pr", return_value=closed), \
                mock.patch.object(review_feedback_loop, "attest_and_resolve",
                                  side_effect=lambda *a, **k: attested.append(1)):
            with self.assertRaises(SystemExit):
                review_feedback_loop.engage_outdated(args)
        self.assertEqual(attested, [])  # refused before touching any thread

    def test_engage_outdated_pr_arg_rejects_non_positive(self) -> None:
        # --pr is parsed by _positive_int: 0/negative are rejected at parse time, so a
        # falsy int can never silently fall back to the full backlog walk. (Copilot +
        # Codex P1 on #536.)
        parser = review_feedback_loop.build_parser()
        for bad in ("0", "-5"):
            with self.assertRaises(SystemExit):
                parser.parse_args(["engage-outdated", "--owner", "o", "--repo", "r", "--pr", bad])


if __name__ == "__main__":
    unittest.main()
