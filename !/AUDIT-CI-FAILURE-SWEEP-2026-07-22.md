---
title: CI Failure Sweep — 2026-07-22
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-21T08:24Z to 2026-07-22T08:24Z (actual data 2026-07-21T12:22Z–08:24Z; a genuine quiet gap 04:43–12:21Z on the 21st predates the window)
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-22

## Context

Scheduled 24-hour review of failing GitHub Actions runs across `laf-us/idaho-vault`. Read `CONSTITUTION.md` and GH #822 / Linear LAF-72 (the standing tracking thread, 14+ prior entries) before writing anything, per this routine's standing instruction not to pad the open-and-unaddressed pile. A sibling session (`claude/practical-cerf-xdwsi9`, PR #859) had already filed yesterday's (2026-07-21) sweep a few hours before this one started — checked its content directly rather than re-deriving, and this report covers only the delta plus independent verification, not a re-file of the same day.

**Shipped this run, not just findings:**

1. `.github/scripts/review_feedback_loop.py` — `ensure_labels()` now catches a per-label `gh label create` failure and warns (`::warning::`) instead of raising. Verified via job logs that a `MERGE_QUEUE_TOKEN`/`GITHUB_TOKEN` permission gap (`HTTP 403: Resource not accessible by personal access token`) was aborting `review_submitted()` (and 6 other call sites) *before* any of their real work — thread resolution, auto-merge arming — ran. This is a bigger deal than the Codacy noise: Codacy's failure never blocked anything (`mergefreeze` is the real gate), but this one was silently dropping real review-processing side effects on every PR review event the token touched. Added a regression test (`test_ensure_labels_survives_a_token_permission_failure`); full local suite (116 review-feedback tests + 9 workflow-security-invariant tests) passes.
2. Continued PR #450 (oldest open PR not already blocked on one of Logan's judgment calls — #470, #859-confirmed-#596-already-worked-today, and several others were checked and are either judgment-blocked or already touched today): fixed the two remaining live CodeRabbit findings (script-injection quoting in `claude-sign.yml`, a doc typo) and replied with reasoning on the third (job-level token scope) rather than applying a diff that would have silently broken two other steps' `if:` conditions. See PR #450 for detail.

## 5W Summary

| | |
|---|---|
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; a `MERGE_QUEUE_TOKEN`/`GITHUB_TOKEN` with insufficient label-create scope; `secret-pattern-policy` flagging content on `logan/obsidian`. |
| **What** | 13 failing runs across 6 workflows (up from yesterday's 12-across-2, because this window extends ~20h past yesterday's cutoff): Codacy Security Scan (4), Codacy Coverage Reporter (3), Python Test Suite (1), Agent Review Response (1), Secret Pattern Policy (1), Sync Plugin Registry (1). 0 `cancelled`/`timed_out`/`stale`, 0 stuck `in_progress`/`queued`. |
| **When** | 2026-07-21T12:22Z – 2026-07-22T08:24Z. |
| **Where** | PR #596 (Codacy x2, Python Test Suite), PR #859 (Codacy, on the sibling's own audit PR), PR #860 (Codacy x2, Agent Review Response), `logan/obsidian`/PR #563 (Secret Pattern Policy, Sync Plugin Registry). Nothing failed on a direct push to `main`. |
| **Why** | Codacy: unchanged, day 14, still the same account-side gap corrected 2026-07-21T14:15Z to "not yet diagnosed which of (a) repo never added to Codacy's account or (b) wrong token type" — not re-guessing further, no network path to app.codacy.com from here either. Agent Review Response: **newly root-caused** this run (see below) — a token permission gap, not previously diagnosed in #822's history. Python Test Suite: a real test/fixture mismatch on an experimental migration branch. Sync Plugin Registry / Secret Pattern Policy: both are the **same already-tracked chronic patterns** (#822 items 2/3; the google_api_key/Zoom-pwd/Preservica-token false-positive class first diagnosed 2026-07-11), re-confirmed, not new categories. |
| **How** (next steps) | Agent Review Response: shipped the resilience fix above; the underlying token-scope gap itself still needs Logan to check/regrant `MERGE_QUEUE_TOKEN`'s scopes (needs `issues:write`, i.e. classic `repo` scope or a fine-grained "Issues: write" repo permission). Codacy: still Logan's call (account-side, per 2026-07-21's correction). Python Test Suite: flagged on PR #596, not fixed (see below). Secret Pattern Policy: flagged for one-time confirmation, not touched (secrets/PII judgment stays outside the author). Sync Plugin Registry: no new action — self-heal fix remains parked in #831/#834 pending Logan's direction per his 2026-07-10 comment. |

---

## New this window

### Agent Review Response — `HTTP 403: Resource not accessible by personal access token` (root-caused + fixed the blast radius)

`review-response.yml` → `review_feedback_loop.py review-submitted` on PR #860, 2026-07-21T14:28:28Z:

```
stderr:
HTTP 403: Resource not accessible by personal access token (https://api.github.com/repos/LAF-US/IDAHO-VAULT/labels/review/required)
RuntimeError: Command failed (1): gh label create review/required --color D93F0B --description ... --force
```

`review-response.yml`'s own `permissions:` block already grants `issues: write`, `pull-requests: write`, `contents: write` — but that block only scopes the auto-generated `GITHUB_TOKEN`. The step actually runs with `GH_TOKEN: ${{ secrets.MERGE_QUEUE_TOKEN || secrets.GITHUB_TOKEN }}` (intentional, per the file's own comment: `GITHUB_TOKEN`-actored events never dispatch further workflow runs, so `MERGE_QUEUE_TOKEN` is preferred so armed PRs actually enqueue). Whichever of those two resolved here is a real credential whose scope lives outside this YAML, and it doesn't have label-create rights.

**Higher-impact than it looks:** `ensure_labels()` is called first thing inside `review_submitted()` (and 6 other functions), before any of the actual review-processing logic (outdated-thread resolution, auto-merge arming, label projection). An unhandled `RuntimeError` there means **every one of those 7 code paths aborted entirely** on every invocation where the token lacked this scope — not just cosmetic red CI, but silently-dropped review-event processing. Category: **Configuration** (credential scope), but the blast radius was a **Code** resilience gap, which is the part this run could actually fix.

**Fixed:** `ensure_labels()` now wraps each `_ensure_label()` call in `try/except RuntimeError`, logging `::warning::` and continuing — matching the existing K6-restamp "fail safe, never abort" precedent already in the same file. Verified locally (see script output in commit) that all 15 labels now warn-and-continue instead of raising. Regression test added. **Not fixed:** the actual token scope — that's Logan's to grant/rotate.

### Python Test Suite — real fixture/branch mismatch, flagged not fixed

PR #596 (`test/dotfolder-live-snapshot-with-drive-migration-attempt`), run 29829790389:

```
FileNotFoundError: [Errno 2] No such file or directory: '.../.openclaw/openclaw-live-ref.json'
```
(+2 more, for `SECRETS-1PASSWORD.md` and `DISCORD-SETUP.md`) — 3 of 326 tests error.

The branch's own dotfolder-migration removed/renamed the `.openclaw/*` fixture paths some test still expects. This is an experimental branch (`test/` prefix) already touched today by the sibling session for 5 unrelated review threads — not re-touching it further this run without understanding whether the fixtures or the migration script is the thing that's supposed to change; flagging for whoever owns that migration's intended end-state.

### Secret Pattern Policy — confirmed same false-positive class, one new instance type

`logan/obsidian` push, run 29875268313, 8 files flagged. Checked file content directly (not the raw secret values) rather than assuming:

- 5 `google_api_key` hits — same pattern as 2026-07-11's diagnosis (Google Static Maps/embed keys in saved-webpage-capture notes).
- 3 `generic_secret_assignment` hits — **new instance of the same false-positive class, not previously catalogued**: Zoom `?pwd=...` query parameters in public meeting-agenda citation links (2 files), and one Preservica digital-archive iframe `token=` render parameter (1 file) — both are third-party embed tokens that the source site itself serves publicly to any viewer, not vault-owned credentials.

Consistent with the class already flagged 2026-07-11 as "worth your one-time confirmation, then likely a narrow Secret Pattern Policy exemption" — not adding that exemption unilaterally (Logan's call per that thread), just widening the confirmed instance list.

### Sync Plugin Registry — recurrence of the known chronic gap, no new action

`logan/obsidian`, job "Verify plugin registry blocks are current" — same pattern as #822 items 2/3 (no `--write` step runs before commits touching plugin config land). The self-heal fix (#831/#834) remains open and parked; not touching either PR this pass per Logan's 2026-07-10 direction.

## Unchanged from yesterday

**Codacy Security Scan (4) + Codacy Coverage Reporter (3), day 14.** Same account-side gap as every prior entry back to 2026-07-08; the 2026-07-21T14:15Z correction (root cause is "repo never added to Codacy's account" *or* "wrong token type," not "link the project in a dashboard setting" — that setting doesn't exist) still stands, still unresolved, still not reachable from this sandbox (no network path to `app.codacy.com`). PR #859's `continue-on-error` mitigation (yesterday) is still open/unmerged, so these still post hard `failure` conclusions for now.

## Insights and Findings (Big IF)

1. **The Agent Review Response finding is the most consequential thing this sweep found** — a silent side-effect-dropping bug (not mere CI noise) that likely affected every PR reviewed while the token was out of scope, for an unknown but possibly multi-day duration. Worth Logan's specific attention beyond "another chronic item."
2. **This is now the 15th consecutive sweep entry** referencing the Codacy account-side gap (#822, since 2026-07-08) — still a pure external-account fix, not a code fix.
3. Cross-checked two independently-generated same-day claims (this report vs. PR #859's) and found a real, named gap between them (12-vs-13 failures, 2-vs-6 workflows) rather than silently reconciling — the difference is fully explained by the ~20h the sibling's window didn't cover, not a disagreement about the same data.

---

*Full cross-references: [GH #822](https://github.com/LAF-US/IDAHO-VAULT/issues/822) · Linear LAF-72 · [PR #859](https://github.com/LAF-US/IDAHO-VAULT/pull/859) (yesterday's sweep) · [PR #450](https://github.com/LAF-US/IDAHO-VAULT/pull/450) (oldest-open-PR pickup, this run).*
