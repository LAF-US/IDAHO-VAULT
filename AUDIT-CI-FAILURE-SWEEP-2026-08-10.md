---
title: CI Failure Sweep — 2026-08-10
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-08-09T12:08Z to 2026-08-10T12:08Z
owner: Logan Finney
---

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault` (65 workflows per `list_workflows`). No new human-caused breakage this window. |
| **What** | 1 currently 100%-reproducing failure (Codacy Security Scan — tracked as #822/LAF-72 since 2026-07-08; real history of a genuine fix, a later regression, and a rejected-and-repeated mitigation attempt — see Incident A); 1 confirmed-recurring `action_required` pattern on Copilot-bot-triggered review events (root cause not fully confirmed); everything else on `main` is green. Zero new hard `failure` conclusions found on `main` in-window. |
| **When** | 2026-08-09T12:08Z – 2026-08-10T12:08Z. Codacy's *current* failure streak traces back at least to 2026-08-07T18:21Z (60/60 sampled runs cancelled); the underlying defect's history goes back further — see Incident A's timeline. |
| **Where** | Codacy: every push to `main` and every open PR (repo-wide, `codacy.yml`). `action_required`: scattered across agent branches with Copilot reviews (today: `claude/skill-doc-qzt7le` 03:42Z, `claude/practical-cerf-p3gz8m`/PR #927 05:40Z). |
| **Why** | Codacy: third-party CLI bug (see Incident A). `action_required`: signature matches a GitHub workflow-run-approval gate; exact trigger unconfirmed (`*`). |
| **How** | Verified via direct job-log reads (not just conclusion fields) for both incidents — see below. |

## Findings

### Incident A — Codacy Security Scan: 100% failure, currently unaddressed — Code (upstream), P1

**Corrected framing, thanks to a Copilot review comment on this PR that caught an error in an earlier version of this section: this was NOT "unaddressed 33 days." It has a real history of being fixed, breaking again for a different reason, and one fix attempt (mine, today) being an exact repeat of something already tried and explicitly rejected. The full, verified timeline:**

1. **2026-07-08 (#822/LAF-72 origin):** real fix landed via PR #821 — two distinct SARIF-formatter crashes (a `MalformedInputException` on non-UTF-8 bytes, and a separate `IndexOutOfBoundsException` in the same formatter) fixed by re-pinning `codacy-analysis-cli-action` to `v4.0.2`, the oldest tagged release with both fixes. A `.codacy.yml` `exclude_paths` list was also added at the same time. **Confirmed working**: "Both SARIF crashes are now gone" per that sweep, checked against actual job logs.
2. **2026-07-23 (#864):** Codacy added a "High" severity level that `v4.0.2` couldn't deserialize, breaking the scan a different way. Bumping to a newer action version (`v4.4.7`) that understood "High" severity tripped this repo's action-pin policy (that release transitively references an unpinned `actions/setup-go@v3`), and no released version of the wrapper action satisfied both constraints. The fix: **stop using the wrapper action entirely** and invoke the raw `codacy-analysis-cli` script directly, pinned to version `7.9.25`. This is almost certainly what reintroduced the SARIF crash — `7.9.25` is a different lineage from the patched `v4.0.2`, and nothing confirms it carries the same formatter fix.
3. **2026-08-03:** a session rediscovered the SARIF crash, tested the `.codacy.yml` exclude list directly (confirmed complete via `fnmatch` against all 21 non-UTF-8 tracked files, not by eye), and **proved it doesn't stop the crash** — job 91547088834 crashed anyway with the full list in place. That session's own hypothesis, from the CLI's verbose log ("Preparing to run opengrep with remote configuration"): config likely resolves from Codacy's cloud, so the local file may never be read. Deleted `.codacy.yml` at Logan's direction, with an explicit commit message: **"Do not re-add it."**
4. **2026-08-10, earlier in this same PR:** without checking `.codacy.yml`'s git history first, re-added the exact same exclude-list mitigation this session had already independently ruled out. Confirmed it doesn't work (run [31411077637](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31411077637): identical crash, identical timeout), and — independently, before seeing the 08-03 commit — landed on the same explanation (`"Success getting config file from endpoint /project/analysis/configuration"` in the verbose log: remote config, not the local file). **Reverted the `.codacy.yml` re-add in this same PR once the duplication was caught.** Recorded here as a real process failure: git blame on the exact file being touched would have caught this before pushing anything, not after.

**What that leaves as the actual open problem, per the 08-03 commit's own framing (still accurate):** the defect is upstream, in `codacy-analysis-cli`'s SARIF formatter, which fails an entire analysis batch on one byte it can't decode as UTF-8. `timeout-minutes: 25` (added between 07-08 and now) bounds the damage but isn't a fix. The three real repair options, none attempted in this session: **(a)** drop `--format sarif` from the CLI invocation, **(b)** find a CLI version/pin that has both the "High" severity support (needed since 07-23) and the SARIF formatter fix (present in `v4.0.2`, status in `7.9.25` unconfirmed), or **(c)** retire this workflow, since Codacy's own cloud-side analysis posts to PRs independently of it (per the 08-03 commit).

- **Current failure rate, this sweep:** sampled the last 60 runs of `codacy.yml` (2026-08-07T18:21Z–2026-08-10T05:41Z, 30 pages × 2). 59 `cancelled`, 1 `action_required`, **zero `success`**. Verified via full job-log read (run [31359405240](https://github.com/LAF-US/IDAHO-VAULT/actions/runs/31359405240), PR #927): the "Run Codacy Analysis CLI" step runs the full 25-minute `timeout-minutes` budget, throws `MalformedInputException` at `Sarif.scala:149` at ~10 minutes in, then hangs until the timeout kills it.
- **Correction to a different prior sweep:** the 2026-08-03 sweep's *other* Codacy note (Incident G in that report, not the one described above) waved off 6 `cancelled` runs elsewhere as "concurrency-group cancellations... not counted as failures." `codacy.yml` has no `concurrency:` block, and this sweep's job-log timeline (full 25-minute runtime, crash mid-run) is inconsistent with a concurrency-supersede cancel. Flagging so it isn't re-asserted (`*`, unable to check what that specific note was measuring).
- **The 21 non-UTF-8 tracked files** found via a `git ls-files` + UTF-8 decode sweep this session (matching the 08-03 session's independent count of 21) remain unconfirmed as *the* trigger — per point 3 above, a complete exclude list covering all of them didn't stop the crash, which is evidence the byte is coming from tool-generated intermediate content, not a repo source file, or that exclusion genuinely never reaches the CLI's actual config source either way.

**Confirmed vs. speculative, at a glance:**

| Confirmed (verified via logs/commits) | Speculative / unresolved |
|---|---|
| Crash signature, timeout behavior, 100% failure rate over 3+ days | Which specific file(s) trigger the crash |
| `.codacy.yml` exclude-list mitigation does not stop the crash (proven twice: 08-03 and 08-10, independently) | Whether the crash is triggered by a repo file at all, vs. tool-generated intermediate content |
| CLI fetched config from Codacy's remote API in this run, at least once | Whether that's always true, or only under some condition (e.g. token presence) |
| The 07-23 CLI-invocation change (#864, wrapper action → raw script) is the most likely regression point | Whether CLI 7.9.25 genuinely lacks the Sarif.scala fix `v4.0.2` had, vs. some other cause |
| `action_required` pattern recurs on Copilot-actor review events | Whether it's a repo/org Actions-approval setting (plausible, not checked directly) |

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

- **The real lesson from this sweep isn't about Codacy — it's that re-reading "#822 is tracked" as "the mitigation is unverified/inert" instead of checking what was actually already tried cost real time today.** A prior session (08-03) had already run the exact experiment this session ran (exclude the 21 non-UTF-8 files), proven it doesn't work, and written "Do not re-add it" directly in the commit message. That message was never read before this session repeated it. **The fix for this class of mistake is cheap and specific: `git log --all -- <path>` on any file about to be added, before adding it**, not a general call to "be more careful."
- **The action-pin policy and the "High" severity requirement are in direct tension for this specific tool, and nobody has found a CLI version that satisfies both.** `v4.0.2` has the SARIF fix but not "High" severity support; `7.9.25` (or whatever supports "High" severity now) reintroduced the crash. Until someone bisects for a version with both, or drops `--format sarif`, or retires the workflow, this will keep recurring regardless of how many more exclude-list attempts happen.
- **IF the `action_required` gate on Copilot-actor review events is in fact an org/repo Actions-approval setting**, it's a one-time repo Settings change, not a code fix — flagging clearly so it doesn't get mistaken for something a future CI-sweep session should keep trying to "fix" from inside the workflow YAML.

---
Cross-posted: GitHub issue #822 (comment), Linear LAF-72 (comment), Slack #all-logan-finney, Discord #ledger (via Zapier).
