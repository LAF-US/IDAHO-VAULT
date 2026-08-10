---
title: CI Failure Sweep — 2026-08-10
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-08-09T12:08Z to 2026-08-10T12:08Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-08-10

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (65 workflows per `list_workflows`). No new human-caused breakage this window. |
| **What** | 1 confirmed-chronic, currently 100%-reproducing failure (Codacy Security Scan — already tracked as #822/LAF-72 since 2026-07-08, now worse than last measured); 1 confirmed-recurring `action_required` pattern on Copilot-bot-triggered review events (root cause not fully confirmed); everything else on `main` is green. Zero new hard `failure` conclusions found on `main` in-window. |
| **When** | 2026-08-09T12:08Z – 2026-08-10T12:08Z. Codacy's failure streak is older than this window — traced back at least to 2026-08-07T18:21Z (60/60 sampled runs cancelled) and originally flagged 2026-07-08 at 29/30. |
| **Where** | Codacy: every push to `main` and every open PR (repo-wide, `codacy.yml`). `action_required`: scattered across agent branches with Copilot reviews (today: `claude/skill-doc-qzt7le` 03:42Z, `claude/practical-cerf-p3gz8m`/PR #927 05:40Z). |
| **Why** | Codacy: third-party CLI bug (see Incident A). `action_required`: signature matches a GitHub workflow-run-approval gate; exact trigger unconfirmed (`*`). |
| **How** | Verified via direct job-log reads (not just conclusion fields) for both incidents — see below. |

## Findings

### Incident A — Codacy Security Scan: 100% failure, unaddressed 33 days, worse than last measured — Code (upstream), P1

**This is not a new finding — it is #822 / LAF-72 ("CI failure sweep 2026-07-08: Codacy SARIF crash"), still open, still in Backlog, now confirmed worse.**

- **Then (2026-07-08):** 29/30 runs failed.
- **Now (2026-08-10):** Sampled the last 60 runs of `codacy.yml` (2026-08-07T18:21Z–2026-08-10T05:41Z, 30 pages × 2). 59 `cancelled`, 1 `action_required`, **zero `success`**.
- **Verified via full job-log read** (run [31359405240](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31359405240), PR #927, today 05:41–06:07Z): the "Run Codacy Analysis CLI" step runs the full 25-minute `timeout-minutes` budget, throws `java.nio.charset.MalformedInputException: Input length = 1` at `Sarif.scala:149` (`Files.readAllLines` on a matched issue's source file, decoding as UTF-8) at ~10 minutes in, then hangs — orphaned — until the timeout kills it at 06:06:59. This is the **exact signature already root-caused in #822**, not a new bug. `timeout-minutes: 25` (added between 07-08 and now, per the workflow file's own comments) is a damage-bound, not a fix — it stops the runner from occupying 6 hours, but the scan itself never completes.
- **Correction to a prior sweep:** the 2026-08-03 sweep (Incident G) waved off 6 `cancelled` Codacy runs as "concurrency-group cancellations... not counted as failures." I checked: `codacy.yml` has **no `concurrency:` block at all**, and the job-log timeline above (full 25:07 runtime, crash mid-run, `##[error]The operation was canceled` only at the timeout boundary) is inconsistent with a concurrency-supersede cancel (which fires near-instantly on a new push, not after the full timeout window). That dismissal looks like it was wrong, or measured a different, non-representative sample — flagging so it isn't re-asserted (`*`, unable to check what that sweep actually looked at).
- **New in this sweep:** a `git ls-files` + UTF-8 decode sweep of all 38,421 tracked files found **21 tracked files that are not valid UTF-8** (mostly binaries: `IMG_20260203_102718.dng`, `.serena/news_read.pkl`, `context.mdb`, `minidata*.csv` with Windows-1252 smart quotes, `backup-diff.log`, `backup-compare-temp/MEDIA/*.webm`, a WhatsApp `.crypt14` DB, several stray/garbled filenames like `io5ujgpo.a4y`). These are **plausible, not confirmed** (`*`) triggers for the crash — the Codacy CLI never logs which file it was reading when it throws. None are `.gitignore`d.
- **Next step (unchanged from #822, still not done):** needs either (a) someone with local Docker/Codacy-CLI access to reproduce and bisect the exact offending file, (b) a different `codacy-analysis-cli` pin, or (c) excluding non-source paths from Codacy's scan scope — exact `.codacy.yml`/CLI exclude-flag syntax was **not verified live** in this session (WebFetch to Codacy's own docs 404'd) and is not being guessed at here rather than risk shipping a fix that silently does nothing.
- **Not attempted in this session:** deleting/gitignoring the 21 non-UTF-8 tracked files. Several look like accidental commits (backup dumps, stray temp files) rather than intentional vault content, but that determination and any bulk removal is Logan's call, not this routine's, per the vault's no-unauthorized-restructuring rule.

### Incident B — `Agent Review Response` `action_required` on Copilot-bot review events — Configuration, recurring, unconfirmed root cause

- `.github/workflows/review-response.yml` (`pull_request_review`, `types: [submitted]`) shows `action_required` with **0 jobs ever scheduled** specifically when the triggering actor is the `Copilot` code-review bot. Confirmed via `get_workflow_run`/`list_workflow_jobs` on run [31359358406](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31359358406) (PR #927, today 05:40:50Z, `jobs.total_count: 0`).
- **Not new**: sampled the last 30 Copilot-actor runs of this workflow — same pattern going back to at least 2026-07-24 (`claude/poka-yoke-qzt7le`), recurring roughly weekly-to-daily since (07-24, 07-26, 07-27 ×2, 07-31, 08-03 ×2, 08-04, 08-08 ×2, and today 08-10). Two occurrences in this 24h window: `claude/skill-doc-qzt7le` 03:42:11Z (×2 runs) and PR #927 05:40:50Z.
- **Root cause not confirmed** (`*`): the signature (0 jobs, `action_required`) matches GitHub's own "this workflow run needs approval" gate, which most commonly applies to first-time/low-trust or bot actors under repo/org Actions settings. This session does not have access to check **Settings → Actions → General → Fork pull request workflow approvals**, which would confirm or rule this out. Flagging for Logan to check directly rather than asserting the mechanism as fact.
- **Impact:** the PR's review-state sync (labels, auto-merge arming) doesn't run for that review event; a later event on the same PR (another review, a push) recomputes state from scratch, so it isn't silently lost — just delayed until someone manually approves the run or a different event fires.

### Ruled out — scheduled/cron workflows are NOT broken

Every `schedule:`-triggered workflow (`daily-rollover.yml`, `sort-audit.yml`, `wayback-audit.yml`, `stale-bot-prs.yml`, `branch-garden-report.yml`, `metadata-survey.yml`, etc.) shows no runs since 2026-07-06 — which on first look reads like a mass breakage. It is not: commit `eb4b5a5` (PR #778, 2026-07-06, "remove EVERY schedule trigger — no cron jobs until the chron_clock is established") intentionally stripped every `schedule:` trigger repo-wide per Logan's own standing order, with a test (`test_no_schedule_triggers_until_the_chron_clock_is_established`) enforcing it stays that way. Verified by reading the workflow files and the commit itself, not inferred from the gap. Ruling this out here so it doesn't get re-discovered as a false alarm in a future sweep.

### Ruled out — two previously-chronic issues now appear resolved

- **opencode.yml `startup_failure`** (tracked across #595/#688/#700/#719/#743, weeks of daily recurrence): sampled the last 30 runs — now correctly `skipped` (the `if` condition evaluates as intended), not `startup_failure`. Not re-flagging.
- **CodeQL "no source found" on `javascript-typescript`** (#599/#617, chronic since 06-20): the old `.github/workflows/codeql.yml` advanced-setup workflow was deleted (PR #726, ~07-02); GitHub's default code-scanning setup (`dynamic/github-code-scanning/codeql`) has run 100% green across the last 30 samples, all within this 24h window.

### Main-branch health

All 9 required policy/gate checks on every `main` push sampled in-window (Action Pin Policy, Check Dotfolder Anchors, Daily Notes Placeholder Check, NETWEB Path Portability Check, Large File Policy, Secret Pattern Policy, Redaction Damage Policy, NORMALIZATION Character Conformity Check, Cross-Platform Smoke) — **100% success.** Only Codacy (Incident A) is non-green on `main`.

## Big IF

- **IF #822/LAF-72 keeps being read as "already tracked" without anyone re-measuring it, its failure rate can silently climb from 97% to 100% (as it did) without anyone noticing the difference between "hard to reproduce" and "never succeeds."** A tracked issue that nobody re-verifies is functionally the same as an unfiled one.
- **IF the 2026-08-03 sweep's "just concurrency-cancellation, not counted" dismissal of Codacy `cancelled` runs was wrong** (this sweep's job-log read says it was, for at least this run), **then Codacy's true failure rate has likely been ~100% for longer than the 3 days directly confirmed here** — worth someone spot-checking further back if the exact onset date matters.
- **IF the `action_required` gate on Copilot-actor review events is in fact an org/repo Actions-approval setting**, it's a one-time repo Settings change, not a code fix — flagging clearly so it doesn't get mistaken for something a future CI-sweep session should keep trying to "fix" from inside the workflow YAML.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
