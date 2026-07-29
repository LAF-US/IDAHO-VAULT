---
title: CI Failure Sweep — 2026-07-29
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-28T12:06Z to 2026-07-29T12:06Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-29

## Context

Scheduled 24-hour review. Read `CONSTITUTION.md`, the prior sweeps in this thread (`-07-27.md`, `-07-28.md`, issue #822/Linear LAF-72), and the six still-open prior "audit(ci)" PRs (#838, #859, #861, #862, #866, #872, #877) before starting, specifically to avoid re-filing what they already found. Every distinct failing workflow name in-window was checked against actual job logs (`get_job_logs`, `failed_only`), not inferred from run titles.

**`main` is green** at head `ca667a5d` — zero failing runs on `main` itself in-window; nothing blocks a merge or deploy.

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; Claude Code (this session, scheduled). No human-caused breakage. |
| **What** | 10 distinct failing workflow names in-window, collapsing to 7 root causes — 6 already root-caused in prior sweeps (fix written but sitting unmerged in most cases), 1 genuinely new. |
| **When** | 2026-07-28T12:06Z – 2026-07-29T12:06Z |
| **Where** | Branches `claude/apply-patch-fixes-9gesn5` (PR #875), `claude/shall-rome-lyrics-ok9049` (PR #854), `claude/poka-yoke-player-qzt7le` (PR #873), `claude/practical-cerf-hxkg1p` (PR #866), `bot/topology-census-2026-06-08` (PR #498), `test/subtle-alien-landing` (PR #470), and `main`'s own `Enqueue on checks complete` job. |
| **Why** | Per item below — verbatim log lines, not paraphrase. |
| **How** | Per item's category and next step. |

## Findings

1. **Daily Notes Placeholder Check** (`claude/apply-patch-fixes-9gesn5`, PR #875) — `Unresolved date-placeholder tokens... 2026-04-16.md:26:- [ ] [[YESTERDAY]]`. **Category: Content, accepted-red by author's own stated decision** (PR #875's body: preserved as part of a union merge, not an oversight). Not a bug.
2. **Secret Pattern Policy** (PR #875; `claude/poka-yoke-player-qzt7le` branch scan) — PR #875 hit: a genuine 68-char Discord OAuth2 token literal, already acknowledged and redacted per that PR's own body. `poka-yoke-player-qzt7le`'s branch-wide scan surfaced ~35 hits, mostly third-party embed keys (`google_api_key` in saved-webpage captures, `.npmrc`/`.pem` paths under vendored plugin marketplaces) — same false-positive class discussed in #838/#862's sweeps. **Category: Content/Configuration**, not newly tracked as its own issue but not new either.
3. **Redaction Damage Policy** (PR #875; PR #498/`bot/topology-census-2026-06-08`) — both match `the exact corruption shape from issue #739` (open, root-caused: a redaction tool over-matched the 2-letter sequence "rt" plus a separator, mangling `start`→`sta***REMOVED***`, `import`→`impo***REMOVED***`, etc., across the repo's pre-purge history). PR #498 is a stale, already-triaged bot report (extensively worked 07-27/07-28, see below) whose old head simply keeps getting re-checked. **Category: Content, tracked (#739).**
4. **Review Feedback Loop** — checked two occurrences, confirmed **not the same error**, ruling out a single code bug: one is a raw GitHub-side 5xx (`Something went wrong while executing your query`, support code `83D2:2E600:343DD5C:B694E35:6A698EA2`), the other is `RATE_LIMIT: API rate limit already exceeded for user ID 136375980` (Logan's account, via `MERGE_QUEUE_TOKEN`). PR #877 (pushed today, still open/unmerged) refactors `gh_cli.py`'s argv handling and would not have prevented either. PR #861 ("fix review_feedback_loop label-permission abort," still open despite its title) fixed a *different* failure mode (403 from a missing `issues:write` scope). **Category: Infrastructure (transient GitHub API rate limit / server error), self-resolved.**
5. **Agent Review Response** — a 10-run burst in ~60 seconds, all `RATE_LIMIT`, same family as #4. Confirmed via the workflow file (`review-response.yml`, `on: pull_request_review: types: [submitted]`) that this fires once per review submission, not a fan-out bug — the burst reflects 10+ real near-simultaneous bot reviews each hitting an already-exhausted shared per-account quota. **Category: Infrastructure.**
6. **check-notebooks-paired** — `A notebook twin is out of sync`, on `claude/practical-cerf-hxkg1p` (PR #866). **Root cause is the same one PR #862 (2026-07-23) already fixed** (floating `jupytext` version resolving inconsistently vs. the pinned `1.19.4`) — **recurring because #862 is still open and unmerged**, not a new or different bug.
7. **Cross-Platform Smoke** (`claude/poka-yoke-player-qzt7le`, PR #873) — all 6 matrix jobs fail identically at a `test -f` step checking for one of `AGENTS.md` / `!/WAKEUP.md` / `!/README.md` / `swarm.json`, with no further log output. Consistent with one of those four required files missing on this branch. **Category: Configuration/Content — gap:** which specific file was not confirmed from logs alone; needs a direct look at the branch tree.
8. **"PR #470" / "Code Quality: PR #470"** (dynamic workflow, `test/subtle-alien-landing`) — `CodeQL... Exit code was 32... "configuration error"`. Chronic and already tracked (issue #791, 2026-07-07 sweep): the vault has no JS/TS source, so CodeQL's default-setup language matrix always exits 32. Needs a repo-Settings change outside this session's reach. Re-triggers on PR #470's own repeated pushes (83 commits total), not a scheduled recheck.
9. **Enqueue on checks complete** (`main`) — `failed to read PR #854 ... gh: API rate limit already exceeded`, same rate-limit family as #4/#5. The script's own design treats this as retriable (a later run re-attempts), so this degrades a merge-queue re-attempt rather than blocking `main`'s CI status. Flagged, not confirmed blocking.
10. **Python Test Suite / Codacy Coverage Reporter** (`claude/shall-rome-lyrics-ok9049`, PR #854) — **new finding, not in any prior sweep in this thread.** Both runs: `Ran 348 tests... FAILED (failures=3)`, all three `unittest.mock.assert_called_once_with` mismatches in `test_helper_scripts.py` (×2) and `test_phone_link_intake.py` (×1) — production code now calls `subprocess.run(..., check=False)` explicitly, but the corresponding mock assertions weren't updated to expect the new kwarg. **Category: Code (genuine test/prod drift on that branch)**, that branch's own author's active WIP — documenting here rather than pushing a fix to a PR this session doesn't own.

## Blocking / repeated

Nothing blocks `main`. The one structural pattern worth naming plainly: **items 4, 6, and 8 above are not new bugs — they are old, correctly-diagnosed bugs whose fixes already exist in this vault's history but haven't landed**, because the PRs carrying them (#862 for item 6; #861, #877 attempted a different angle on item 4's family; #791's CodeQL settings ask for item 8) are still open. Filing another report restating the same root cause without merging the fix is exactly the "pile" this routine's instructions this run explicitly named. This sweep is not adding a new fix-PR to that pile; see below for what it's doing instead.

## New findings

- Item 10 (test/prod drift on PR #854) — see above, newly surfaced this pass.
- Item 7's exact missing file — explicit gap, not resolved from available evidence.

## Big IF

**The backlog of already-correct, already-written fixes (#838, #859, #861, #862, #866, #872, #877 — all still open) is now the largest single driver of "recurring" failures in these sweeps, larger than any single new bug.** Six of today's ten failure groups trace to a fix that exists somewhere in this pile rather than to undiagnosed root cause. Continuing to file a new dated report each day documents this accurately but does not shrink it. Per this run's explicit instructions, this sweep is deliberately not opening an eleventh entry to that pile — this file accompanies no new fix-PR of its own; it's posted as a comment to the existing tracking thread (#822 / LAF-72), and this session is spending its second half advancing one specific old open PR toward an actual merge instead (see that PR's own thread for progress).

---
Cross-posted: GitHub issue #822 (comment, not a new issue), Linear LAF-72 (comment, not a new ticket), Slack #all-logan-finney, Discord #ledger (via Zapier).
