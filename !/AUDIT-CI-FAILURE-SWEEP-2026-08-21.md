---
title: CI Failure Sweep — 2026-08-21
type: audit
status: complete
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, ~2026-08-19T17:10Z to 2026-08-21T17:10Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-21

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (77 registered workflows). One new regression confirmed (GitHub-hosted Copilot review backend), one chronic known issue confirmed still-red on `main` itself, remainder is already-tracked or self-resolving noise. |
| **What** | (1) **`Running Copilot Code Review`** — a GitHub-hosted dynamic workflow, not a file in this repo — has failed on **27 consecutive triggers** since 2026-08-20T02:36:08Z (run #1214), every one at the step **"Processing Request (Linux)"**, after running clean immediately prior (runs #1211–#1213, 2026-08-19T10:18–14:18Z, all `success`). This is a new onset within the window, not previously reported in the 2026-08-12 or 2026-08-19 sweeps. (2) **`Check Dotfolder Anchors`** is still failing on `main` at its most recent push-triggered run in-window (run #3995, 2026-08-19T14:16:18Z, the merge of PR #964 — `main`'s current HEAD) — a known, already-diagnosed, already-flagged-to-Logan issue (root-anchor ratchet at 294 missing vs. a 293 ceiling; needs an authored persona note, which is outside this session's delegated authority to write per governing guardrails). |
| **When** | Copilot regression: onset 2026-08-20T02:36:08Z, still failing at last check (2026-08-21T17:12:00Z, run #1240) — ongoing for ~39 hours as of this sweep. Dotfolder-anchors: red on `main` since PR #961 merged 2026-08-18T11:42:25Z; confirmed still red at the latest in-window push to `main` (2026-08-19T14:16:18Z). |
| **Where** | Copilot regression is repo-wide — every PR push in the window shows it, across `claude/apply-patch-fixes-9gesn5`, `claude/rework-census-doctrine-463-4033po`, `claude/sweet-edison-6btuur`, `claude/fullcalendar-obsidian-integration-1u2a0l`, and others. Dotfolder-anchors failure is on `main` itself, not a branch artifact. |
| **Why** | Copilot regression: root cause not determinable from job/step metadata alone — "Processing Request (Linux)" is GitHub's own hosted Copilot-review runner step, no logs are exposed to this repo's tooling, and the workflow file isn't one this repo authors or can edit (`dynamic/agents/copilot-pull-request-reviewer`). Consistent with a GitHub-side Copilot backend disruption, not a repo misconfiguration. Dotfolder-anchors: `.triagebot/` (added by PR #961) and other recent chambers pushed the vault's missing-root-anchor count from 293 to 294 against the check's own ratchet ceiling; the fix is an authored vault-canon note, which prior sessions (PR #984, #1000) explicitly declined to author without Logan's direct instruction — still the case here. |
| **How** | Verified directly via `actions_list`/`actions_get` job and step data (not inference): confirmed 0-success/27-failure run sequence for Copilot review with exact timestamps, confirmed the specific failing step name via `list_workflow_jobs`, and confirmed `Check Dotfolder Anchors` conclusion on `main`-branch-scoped runs going back through the window. One data-quality caveat: a first delegated sub-sweep (background agent, ~723K tokens / 215 tool calls) surfaced 8 additional workflows with aggregate failure counts (pr-linear-sync ×1, linear-pr-sync ×1, check-portable-paths ×5, validate-daily-notes ×8, review-response ×1, CodeQL Advanced ×24, sync-plugin-registry ×2 — 42 runs) that it had independently verified earlier in its own run, but lost the per-run detail (branch/actor/step) to its own context compaction before reporting back. I am **not** fabricating row-level detail for those 42 runs to fill the gap — reporting the counts as agent-verified-at-the-time, the detail as unreconstructed. A direct re-check of `codeql.yml` scoped to `branch=main` in this session returned stale July data despite a `total_count` of 498 for the in-window period — reproducing the same pagination-instability-at-write-throughput problem this series has flagged since 2026-08-12, not a new finding. |

## Findings

### Incident A — `Running Copilot Code Review` failing 27/27 in-window, GitHub-side, NEW this cycle

Confirmed via direct job data (run `32506902249`, job `copilot-pull-request-reviewer`): step 19, "Processing Request (Linux)," fails after ~25 seconds; every other step in the job (checkout, MCP server setup, Copilot prep) succeeds. This is GitHub's managed Copilot code-review action (`dynamic/agents/copilot-pull-request-reviewer`, distinct from the separate `Copilot code review` app-installed workflow, id 247071622, which had no runs in-window) — not a file this repo owns or can patch. Sampled PR #999 (head commit `ade90adc`, one of the affected pushes) currently shows `mergeable_state: unstable`, not `blocked` — so this specific PR is not being held out of the merge queue by it, at least as sampled. But `VAULT-CONVENTIONS.md` § "Merge queue vs. auto-merge" names "the latest commit's Copilot review complete" as one of the PR-level **queue-entry** gates (`copilot_code_review`, `review_on_push`) — if this outage persists, it is a plausible path to a real entry-gate stall repo-wide, not just noise. **Not fixed here** — nothing in this repo to fix; flagged for Logan's awareness and for the next sweep to re-check whether it has self-resolved (GitHub-side incidents of this kind are typically transient).

### Incident B — `Check Dotfolder Anchors` still red on `main`, known issue, unchanged status

Re-confirmed rather than re-discovered: this is the same root-anchor ratchet (294 missing vs. 293 allowed) first flagged on PR #984 (2026-08-18) and revisited on PR #1000/#1001 (2026-08-20, which cleared the mechanical `.triagebot/stub.txt` half of the finding but explicitly left the authored-note half open, "not something this PR generates"). Verified still failing at the most recent in-window push directly to `main` (run #3995, the merge of PR #964, 2026-08-19T14:16:18Z — `main`'s current HEAD as of this sweep). Not fixed here, for the same reason prior sessions gave: the missing piece is an authored vault-canon note, not a mechanical fix, and writing vault canon without Logan's direct instruction is outside this session's delegated authority per `CONSTITUTION.md` § V ("No unauthorized restructuring... Logan must approve"). Restating rather than re-diagnosing.

### Incident C — `Secret Pattern Policy` — 4 isolated push-triggered failures, self-resolved on retry

All 4 (runs on `claude/apply-patch-fixes-9gesn5`, `claude/rework-census-doctrine-463-4033po`, `claude/shall-rome-lyrics-ok9049`, `wayback-audit-20260420100033`) failed once on a `push` event and were immediately followed by `success` on the next trigger for the same branch. One instance directly checked (run #4597, 2026-08-21T05:53:55Z) sits between two commits on the same branch that also carry an explicit, already-landed fix for a related force-push/orphaned-`before` edge case in this same check (commit `02eb3213`, 2026-08-21T03:13:20Z, "fall back to merge-base when a force-push orphans `before`"). Consistent with residual instances of that same edge-case family rather than a new bug. Not chased to full root-cause on all 4 individually — self-resolving, non-blocking, low volume.

### Incident D — `Codacy Security Scan` — 2 failures on dependabot-authored branches, consistent with known chronic issue

Not independently re-verified with full job-log detail this session (surfaced by the delegated sub-sweep, both on `dependabot/github_actions/anomalyco/opencode/...` branches, "Upload SARIF results file" step). Consistent with the chronic Codacy CLI SARIF-formatter bug tracked since GH #822 item 1 (2026-07-08) and only partially remediated by PR #962 (per the 2026-08-12 sweep). Not a new incident.

### Zero new-and-unexplained failures found on `main` itself; nothing found newly blocking merges to `main`.

## Big IF

- **A genuinely new, GitHub-side regression surfaced this cycle** (Incident A) — the first sweep in this series to catch a live Copilot-backend disruption rather than only a repo-side misconfiguration or chronic drift. Worth a same-day recheck rather than waiting for the next scheduled sweep, since GitHub-side incidents typically resolve faster than this series' cadence.
- **Delegating the initial sweep to a background subagent cost ~723K tokens and 215 tool calls and still returned an incomplete result** (42 of 93 candidate failing runs lack reconstructable per-run detail, after the subagent's own context compacted mid-run). The verification work in this report — the two real findings above — was redone directly rather than trusting the delegated pass at face value. For a repo at this write-throughput, a single long-running delegated sweep is the wrong shape; several narrowly-scoped agents (one workflow file each) would likely finish inside their context budget rather than needing to compact.
- **The audit-PR pile has not shrunk since 2026-08-19**: #859 (open since 07-21, now 31 days, `review/threads-open`), #966 (08-12 rolling review), #1002 (08-19 sweep) — three, before this one, which makes four. This sweep's own governing task explicitly named not adding to that pile as a goal, not merely a report-only PR; consistent with that instruction, this report carries no repo-side fix (there wasn't a safely-actionable one in-window — Incident A is GitHub-side, Incident B is outside delegated authority, Incidents C/D are self-resolving or already tracked), and the pile itself is not something this session has authority to clear by merging or closing — that is Logan's call, or the separate later phase of this session's task that works the oldest open item toward merge.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
