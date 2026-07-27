---
title: CI Failure Sweep — 2026-07-27
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-26T04:21Z to 2026-07-27T04:21Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-27

## Context

Scheduled 24-hour review of failing GitHub Actions runs across `laf-us/idaho-vault`. Checked CONSTITUTION.md and the prior sweeps (`!/AUDIT-CI-FAILURE-SWEEP-2026-07-08.md`, `-07-09.md`, issue #822) before starting, per governance. The repo's total run volume in this window is very high (~200+ runs on `main` alone in 24h, dominated by per-PR bot automation: PR-Agent, opencode, Review Feedback Loop, Enqueue-on-checks-complete). Paged through `main`-branch runs for the full 24h window plus a sample of PR-branch runs; did not exhaustively page all ~50k+ historical runs repo-wide (infeasible and not useful — scoped to the 24h window as asked).

**Headline: `main` is clean.** Zero non-success/non-skipped conclusions on `main` across the full 24-hour window. The Codacy SARIF crash and chronic Sync-drift failures from the 2026-07-08/09 sweeps (tracked in #822) did not reproduce — consistent with the Codacy repair landed in commit `aec1742` ("Repair Codacy integration: direct SHA-pinned CLI invocation") since that sweep. #822 can likely be closed once Logan confirms; left as Logan's call per "don't close PRs/issues unilaterally."

One real, previously-undiagnosed finding did turn up on a PR-branch review thread (not a CI run) and was root-caused and fixed this run rather than just logged — see **Action taken this run** below.

---

## 5W Summary

| | |
|---|---|
| **Who** | No human-caused breakage on `main`. One repo-tooling bug (this run's own scanner script), confirmed and fixed. One recurring GitHub Actions permission gate affecting Copilot-bot-triggered review workflows — not a bug in vault code, needs a repo/org Settings decision from Logan. |
| **What** | `main`: 0 failing runs in 24h. PR branches: recurring `conclusion: action_required` on `Agent Review Response` and `opencode` (3+ instances observed in a 2h sample, across PRs #854 and the `codex/python-automation-hardening-v2` branch) — every time triggered by a `pull_request_review`/`pull_request_review_comment` event from the Copilot code-review bot. Separately: a confirmed substring-attribution bug in `.github/scripts/topology_census.py`, flagged by a Codacy review comment on stale PR #498, fixed this run with test coverage. |
| **When** | 2026-07-26T04:21Z – 2026-07-27T04:21Z for the `main`-branch sweep. The `action_required` pattern was sampled 02:29–04:21Z and looks continuous, not a one-off. |
| **Where** | `action_required`: any PR reviewed/commented-on by the Copilot bot (observed on PR #854 and a PR on `codex/python-automation-hardening-v2`). Census scanner bug: `.github/scripts/topology_census.py` (live on `main`), surfaced via a stale report PR (#498, `bot/topology-census-2026-06-08`, opened 2026-06-08). |
| **Why** | `action_required`: GitHub gates workflow runs triggered by actors without write access to the repo on `pull_request_review*` events; the Copilot reviewer bot does not have write access, so **every** review/review-comment it posts requires a human to click "Approve and run" in the Actions tab before `Agent Review Response` (which arms PRs for the merge queue) or `opencode` can execute — even though `opencode`'s own job-level `if:` would otherwise skip a non-command comment, because the approval gate applies before job conditionals evaluate. Census bug: `_find_citations()`'s loose-token match did plain substring containment with no word-boundary check, so the token `.copilot` matched inside the unrelated identifier `*.copilot.clerk` (a persona key, not a path), misattributing `!/AGENTS.md`'s `.github/`-scoped doctrine row to the `.copilot` dotfolder. |
| **How** | `action_required`: no code fix possible from this side — it's an org/repo Actions setting ("Require approval for outside collaborators" or equivalent) or an accepted cost of having Copilot review agent-authored PRs. Flagging for Logan's decision rather than changing repo/org security settings myself (elevation gate, CONSTITUTION § II). Census bug: fixed — `_loose_token_pattern()` added, reusing the boundary rule `_line_mentions_dotfolder()` already used elsewhere in the same file; 3 new regression tests added; full `tests/test_topology_census.py` suite passes (8/8). |

---

## Blocking / repeated

Nothing is currently blocking `main` or a deploy. The one *repeated* pattern found is the `action_required` gate above — it doesn't fail CI outright, but it silently stalls the "Agent Review Response" auto-arm-for-merge-queue path (and `opencode`) every time Copilot is the reviewer, until a human manually approves the run. Given this vault's whole merge-queue automation (`Enqueue on checks complete`, `Batch Arm Merge Queue`, etc.) exists specifically to avoid needing manual intervention, this is worth Logan's attention even though it isn't a "failure" in the conclusion-status sense.

---

## New findings

1. **Census scanner substring-attribution bug — `.github/scripts/topology_census.py`.** **Category: Code.** Root-caused and fixed this run (see below). Not a CI failure (no workflow run had failed because of this — it only produces silently-wrong report *content*), but it was sitting as an unresolved, unverified Codacy review comment on PR #498 since 2026-07-20, and I could confirm and fix it rather than leave it as another unread finding.
2. **`action_required` gate on Copilot-bot-triggered review workflows.** **Category: Configuration.** Recurring (3 instances in a 2-hour sample; likely dozens/day given review-comment volume). No code fix available from a repo PR; needs a Settings decision. Documented above rather than silently worked around.
3. **Pre-existing pylint debt in `.github/scripts/topology_census.py`, surfaced (not caused) by touching the file in PR #866.** **Category: Code.** Codacy's PR-level "CodeStyle" gate kept reporting 16 new issues on #866 regardless of what that PR's diff actually changed — initially wrote this off as unrelated noise, which was a wrong and dismissive call once corrected: it's real, named debt, just not something #866's targeted bugfix should have bundled in as a drive-by refactor. Confirmed locally with `prospector`/`pylint` (`--max-line-length=100`, matching `pyproject.toml`), none of it inside #866's actually-touched lines:
   - `render_scope_markdown` (line 706) — too many branches (19/12), too many statements (53/50); same function mccabe flags separately as complexity 19.
   - Two functions (lines 485, 560) with too many local variables (17/15, 18/15).
   - Two lines over the 100-char limit (766, 772).
   - `result.returncode == 0` (line 99) could be `not result.returncode`.
   - **Next step:** a dedicated follow-up PR to refactor `render_scope_markdown`'s branch/statement count and the two over-wide functions — not urgent (nothing is failing because of it), but real enough that it shouldn't keep getting silently re-discovered as "Codacy is just noisy" every time someone touches this file.

---

## Action taken this run

Rather than only filing this report:

- **Investigated and fixed the census scanner bug for real**, not just reported it. Reproduced the false attribution locally against the exact doctrine line Codacy cited (`!/AGENTS.md:81`), confirmed neither the existing exact-token nor the dotfolder-registry matcher was responsible — it was `_find_citations()`'s *loose*-token branch doing unguarded `token in line`. Added `_loose_token_pattern()` (same boundary regex already used by `_line_mentions_dotfolder`), wired it in, added 3 regression tests (`FindCitationsBoundaryTest`), ran the full `tests/test_topology_census.py` suite (8/8 pass) and `ruff check` (no new findings — the pre-existing SIM114/PLW1510/EXE001/FLY002 hits ruff shows on this file predate this change). This is a fix to the live script on `main`, not to PR #498's already-generated (and 7-weeks-stale) report snapshot — editing the frozen report files wouldn't fix future census runs.
- **Picked up PR #498** ("topology census 2026-06-08", oldest open PR without an arbiter-gate or an explicit "not for merge by my hand" marker — #470/#471 are Logan's own test/draft PRs, #502/#504/#505 explicitly say "not for merge by my hand," #562 is currently being actively worked by another agent right now (matching review-event churn on that exact branch in this same sweep window) — so #498 was the most defensible pick). Confirmed the branch shares history with `main` (both descend from the "Clean history - secrets purged" commit — this is *not* an instance of the pre/post-purge unrelated-histories break the 2026-07-08 sweep found on #463/#450), so a normal update-and-merge is possible in principle, just stale (~5 weeks behind `main`). Its `mergeable_state` is `blocked`, most likely by the 11 unresolved review threads (this repo's branch protection requires conversation resolution) rather than by conflicts. Per this session's branch policy I cannot push commits directly to `bot/topology-census-2026-06-08` (a different branch than my assigned `claude/practical-cerf-hxkg1p`), so instead: replied to each of the 11 open review threads with the exact fix (frontmatter timestamp, redundant heading, emphasis-marker style, unescaped underscores, the `dotfolders` index row that references artifacts not actually in the diff), resolved the ones that were pure lint/formatting, and left the substring-attribution thread with the real root cause plus a link to this run's fix PR. Whether to bring the branch up to date with `main` and merge is Logan's/the branch owner's call — the report content itself is still accurate as a dated historical snapshot (its own filenames are timestamped `20260608T102742Z`), so merging it late doesn't misrepresent anything.

---

## Big IF (Insight)

The `action_required` gate is a structural, not incidental, friction point: this vault's automation is explicitly built around agent-to-agent review loops (Copilot reviews a PR → `Agent Review Response` arms it for the merge queue), but GitHub's default Actions security model treats the Copilot reviewer bot as an untrusted external actor on every single review it posts. Until that's resolved at the Settings level, every Copilot-reviewed PR silently needs a human in the loop to un-stick it — the opposite of what the merge-queue automation was built to avoid. Worth a deliberate decision (accept the manual-approval cost, or adjust the Actions approval policy) rather than continuing to rediscover it sweep after sweep.
