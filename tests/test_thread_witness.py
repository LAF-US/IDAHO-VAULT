"""Tests for thread_witness.py — the looker read/classify/report side.

Migrated from test_review_feedback_loop.py when the looker was extracted into its own
module (2026-07-25, Logan's decision), plus dedicated tests for the two helpers the
extraction split out of `_classify_pr_for_looker` to lower its complexity.
"""

from __future__ import annotations

import contextlib
import io
import json
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

# thread_witness imports its siblings (review_feedback_loop, pr_github, pr_threads) by
# name, so the scripts dir must be importable. Production runs the script directly, which
# already has this on sys.path[0].
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import thread_witness  # noqa: E402
import review_feedback_loop  # noqa: E402  — for _build_attestation used in a fixture


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
    auto_merge_enabled: bool = False,
    state: str = "OPEN",
) -> dict[str, object]:
    created_at = created_at or datetime(2026, 4, 16, 2, 0, tzinfo=timezone.utc)
    updated_at = updated_at or created_at
    return {
        "number": number,
        "url": f"https://example.test/pr/{number}",
        "state": state,
        "createdAt": created_at.isoformat().replace("+00:00", "Z"),
        "updatedAt": updated_at.isoformat().replace("+00:00", "Z"),
        "isDraft": draft,
        "reviewDecision": review_decision,
        "autoMergeRequest": {"enabledAt": created_at.isoformat().replace("+00:00", "Z")}
        if auto_merge_enabled
        else None,
        "labels": _labels(*labels),
        "reviewThreads": {"pageInfo": {"hasNextPage": threads_truncated}, "nodes": list(threads)},
    }


def _bot_thread() -> dict[str, object]:
    return _thread(authors=("coderabbitai",), author_type="Bot")


def _looked_open_thread() -> dict[str, object]:
    thread = _bot_thread()
    body = review_feedback_loop._build_attestation("claude-code-bot", "advisory", "ok")
    thread["comments"]["nodes"].append(
        {"author": {"login": "claude-code-bot", "__typename": "Bot"}, "body": body, "url": "u"}
    )
    return thread


class LookerQueueTest(unittest.TestCase):
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
        items = thread_witness._build_looker_queue(pr)
        self.assertEqual(len(items), 3)  # resolved thread excluded
        self.assertTrue(all(item["pr"] == 42 for item in items))
        # authors sorted + deduplicated; url from the first comment
        self.assertEqual(items[0]["authors"], ["coderabbitai", "human-reviewer"])
        self.assertEqual(items[0]["url"], "https://example.test/thread")
        self.assertFalse(items[0]["looked"])
        self.assertTrue(items[1]["looked"])
        self.assertTrue(any(item["is_outdated"] for item in items))


class ClassifyPrForLookerTest(unittest.TestCase):
    def test_classify_needs_fix_is_machine_lane_but_not_drainable(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=1, created_at=now - timedelta(days=1), threads=(_bot_thread(),))
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "machine-disposable")
        self.assertEqual(report["threads"][0]["resolution"], "needs-fix")
        self.assertFalse(report["safe_to_drain"])
        self.assertFalse(report["stale"])

    def test_classify_outdated_bot_thread_is_safe_to_drain(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = _thread(authors=("coderabbitai",), author_type="Bot", outdated=True)
        pr = _pr(number=14, created_at=now - timedelta(days=1), threads=(thread,))
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["resolution"], "outdated-resolvable")
        self.assertEqual(report["lane"], "machine-disposable")
        self.assertTrue(report["safe_to_drain"])

    def test_classify_would_cascade_when_auto_merge_armed(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=2, created_at=now - timedelta(days=1),
            auto_merge_enabled=True, threads=(_bot_thread(),),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "would-cascade")
        self.assertFalse(report["safe_to_drain"])

    def test_classify_needs_human_on_human_thread(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=3, created_at=now - timedelta(days=1),
            threads=(_thread(authors=("loganfinney27",), author_type="User"),),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")
        self.assertFalse(report["safe_to_drain"])

    def test_classify_needs_human_on_changes_requested(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=4, created_at=now - timedelta(days=1),
            review_decision="CHANGES_REQUESTED", threads=(_bot_thread(),),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")

    def test_classify_needs_human_on_truncated_comments(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = _bot_thread()
        thread["comments"]["pageInfo"] = {"hasNextPage": True}
        pr = _pr(number=5, created_at=now - timedelta(days=1), threads=(thread,))
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")
        self.assertEqual(report["unprovable_threads"], 1)

    def test_classify_clear_when_no_unresolved(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=6, created_at=now - timedelta(days=1),
            threads=(_thread(resolved=True, authors=("coderabbitai",), author_type="Bot"),),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "clear")

    def test_classify_stale_is_never_safe_to_drain(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=7, created_at=now - timedelta(days=30), threads=(_bot_thread(),))
        report = thread_witness._classify_pr_for_looker(pr, now=now, stale_days=14)
        self.assertEqual(report["lane"], "machine-disposable")  # threads are clearable...
        self.assertTrue(report["stale"])  # ...but it's abandoned
        self.assertFalse(report["safe_to_drain"])  # so never auto-drained

    def test_classify_looked_open_is_machine_clearable(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(number=9, created_at=now - timedelta(days=1), threads=(_looked_open_thread(),))
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["disposition"], "looked-open")
        self.assertEqual(report["machine_clearable"], 1)
        self.assertEqual(report["lane"], "machine-disposable")  # recoverable, clearable

    def test_classify_human_on_truncated_page_is_human_not_unprovable(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        thread = _thread(authors=("loganfinney27",), author_type="User")
        thread["comments"]["pageInfo"] = {"hasNextPage": True}
        pr = _pr(number=10, created_at=now - timedelta(days=1), threads=(thread,))
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["threads"][0]["disposition"], "human")
        self.assertEqual(report["human_threads"], 1)
        self.assertEqual(report["unprovable_threads"], 0)
        self.assertEqual(report["lane"], "needs-human")

    def test_classify_needs_human_on_mixed_human_and_bot(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        human = _thread(authors=("loganfinney27",), author_type="User")
        pr = _pr(
            number=11, created_at=now - timedelta(days=1),
            threads=(human, _bot_thread()),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(report["lane"], "needs-human")  # any human forces it
        self.assertEqual(report["machine_clearable"], 1)  # the bot thread, still counted
        self.assertEqual(report["human_threads"], 1)

    def test_classify_needs_human_on_truncated_thread_list(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        pr = _pr(
            number=12, created_at=now - timedelta(days=1),
            threads=(_bot_thread(),), threads_truncated=True,
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
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
        report = thread_witness._classify_pr_for_looker(pr, now=now, stale_days=14)
        self.assertFalse(report["stale"])  # recent activity wins over old creation
        self.assertTrue(report["safe_to_drain"])  # bare-resolvable (outdated) + not stale

    def test_classify_surfaces_resolution_and_counts(self) -> None:
        now = datetime(2026, 6, 16, tzinfo=timezone.utc)
        suggestion_body = "Wrong value.\n\n```suggestion\ncorrected = True\n```\n"
        pr = _pr(
            number=1,
            created_at=now - timedelta(days=1),
            threads=(
                _thread(authors=("coderabbitai",), author_type="Bot", body=suggestion_body),
                _thread(authors=("chatgpt-codex-connector",), author_type="Bot", body="prose finding"),
            ),
        )
        report = thread_witness._classify_pr_for_looker(pr, now=now)
        self.assertEqual(
            sorted(t["resolution"] for t in report["threads"]), ["apply-suggestion", "needs-fix"]
        )
        self.assertEqual(report["resolution_counts"], {"apply-suggestion": 1, "needs-fix": 1})


class ThreadDispositionTest(unittest.TestCase):
    """The per-thread decision split out of the classifier."""

    def test_human_author_is_human(self) -> None:
        t = _thread(authors=("loganfinney27",), author_type="User")
        self.assertEqual(thread_witness._thread_disposition(t), "human")

    def test_bot_only_with_incomplete_page_is_unprovable(self) -> None:
        t = _bot_thread()
        t["comments"]["pageInfo"] = {"hasNextPage": True}
        self.assertEqual(thread_witness._thread_disposition(t), "unprovable")

    def test_bot_only_missing_pageinfo_is_unprovable(self) -> None:
        t = _bot_thread()
        t["comments"].pop("pageInfo")
        self.assertEqual(thread_witness._thread_disposition(t), "unprovable")

    def test_bot_only_attested_is_looked_open(self) -> None:
        self.assertEqual(thread_witness._thread_disposition(_looked_open_thread()), "looked-open")

    def test_bot_only_provable_unattested_is_disposable(self) -> None:
        self.assertEqual(thread_witness._thread_disposition(_bot_thread()), "bot-disposable")


class SelectLaneTest(unittest.TestCase):
    """Lane selection split out of the classifier."""

    def _lane(self, **overrides) -> str:
        kw = dict(
            threads_truncated=False, review_decision="", human=0, unprovable=0,
            unresolved_count=1, machine_clearable=1, auto_merge_armed=False,
        )
        kw.update(overrides)
        return thread_witness._select_lane(**kw)

    def test_truncated_forces_needs_human(self) -> None:
        self.assertEqual(self._lane(threads_truncated=True), "needs-human")

    def test_changes_requested_forces_needs_human(self) -> None:
        self.assertEqual(self._lane(review_decision="CHANGES_REQUESTED"), "needs-human")

    def test_any_human_forces_needs_human(self) -> None:
        self.assertEqual(self._lane(human=1), "needs-human")

    def test_any_unprovable_forces_needs_human(self) -> None:
        self.assertEqual(self._lane(unprovable=1), "needs-human")

    def test_no_unresolved_is_clear(self) -> None:
        self.assertEqual(self._lane(unresolved_count=0, machine_clearable=0), "clear")

    def test_all_clearable_unarmed_is_machine_disposable(self) -> None:
        self.assertEqual(self._lane(unresolved_count=2, machine_clearable=2), "machine-disposable")

    def test_all_clearable_armed_is_would_cascade(self) -> None:
        self.assertEqual(
            self._lane(unresolved_count=2, machine_clearable=2, auto_merge_armed=True),
            "would-cascade",
        )

    def test_partly_clearable_falls_back_to_needs_human(self) -> None:
        self.assertEqual(self._lane(unresolved_count=2, machine_clearable=1), "needs-human")


class LookerWalkTest(unittest.TestCase):
    def test_looker_walk_is_read_only_and_emits_json(self) -> None:
        pr = _pr(number=8, created_at=datetime(2026, 6, 15, tzinfo=timezone.utc),
                 threads=(_bot_thread(),))
        args = thread_witness.build_parser().parse_args(
            ["looker-walk", "--owner", "o", "--repo", "r"]
        )
        buf = io.StringIO()
        with mock.patch.object(thread_witness, "_list_open_pr_numbers", return_value=[8]), \
             mock.patch.object(thread_witness, "_fetch_pr", return_value=pr), \
             contextlib.redirect_stdout(buf):
            rc = thread_witness.looker_walk(args)
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["open_prs"], 1)
        self.assertEqual(data["by_lane"], {"machine-disposable": 1})
        self.assertIsInstance(data["safe_to_drain"], list)
        self.assertEqual(data["reports"][0]["pr"], 8)
        self.assertEqual(data["reports"][0]["lane"], "machine-disposable")

    def test_list_unlooked_is_read_only_and_emits_json(self) -> None:
        pr = _pr(number=8, threads=(_bot_thread(),))
        args = thread_witness.build_parser().parse_args(
            ["list-unlooked", "--owner", "o", "--repo", "r"]
        )
        buf = io.StringIO()
        with mock.patch.object(thread_witness, "_list_open_pr_numbers", return_value=[8]), \
             mock.patch.object(thread_witness, "_fetch_pr", return_value=pr), \
             contextlib.redirect_stdout(buf):
            rc = thread_witness.list_unlooked(args)
        self.assertEqual(rc, 0)
        data = json.loads(buf.getvalue())
        self.assertEqual(data["open_threads"], 1)
        self.assertEqual(data["unlooked_threads"], 1)

    def test_stale_days_rejects_non_positive(self) -> None:
        for bad in ("0", "-1"):
            with self.assertRaises(SystemExit):
                thread_witness.build_parser().parse_args(
                    ["looker-walk", "--owner", "o", "--repo", "r", "--stale-days", bad]
                )


class RenderWorklistTest(unittest.TestCase):
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
        md = thread_witness.render_looker_worklist(report)
        self.assertIn("No threads resolved, no PRs merged", md)  # read-only framing
        self.assertIn("**Open PRs:** 3", md)
        self.assertIn("machine-disposable: 1", md)
        self.assertIn("needs-fix: 2", md)
        self.assertIn("- #42", md)  # safe_to_drain
        self.assertIn("**#7**", md)  # actionable PR surfaced
        self.assertIn("auto-merge-armed", md)  # flagged
        self.assertNotIn("**#9**", md)  # clear PR (0 unresolved) omitted from worklist

    def test_render_looker_worklist_handles_empty_report(self) -> None:
        md = thread_witness.render_looker_worklist({})
        self.assertIn("**Open PRs:** 0", md)
        self.assertIn("none", md)

    def test_render_looker_worklist_surfaces_truncated_needs_human(self) -> None:
        report = {
            "open_prs": 1, "by_lane": {"needs-human": 1}, "by_resolution": {},
            "stale": 0, "safe_to_drain": [],
            "reports": [{"pr": 88, "lane": "needs-human", "stale": False,
                         "auto_merge_armed": False, "threads_truncated": True,
                         "unresolved_threads": 0, "resolution_counts": {}}],
        }
        md = thread_witness.render_looker_worklist(report)
        self.assertIn("**#88**", md)  # surfaced despite 0 visible unresolved
        self.assertIn("threads-truncated", md)


if __name__ == "__main__":
    unittest.main()
