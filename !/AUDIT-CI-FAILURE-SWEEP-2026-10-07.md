---
title: CI Failure Sweep — 2026-10-07
type: audit
status: complete
authority: CLAUDE (routine CI sweep, session 01VMymjfRxJvKJhKYwVHG1Bp)
scope: GitHub Actions runs, LAF-US/IDAHO-VAULT, 2026-10-05T17:00Z to 2026-10-07T17:10Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-10-07

## 5W Summary

| | |
|---|---|
| **Who** | `pullfrog[bot]` (workflow dispatch on `main`); Zaxion (external GitHub App) |
| **What** | (1) Three Pullfrog dispatch runs failed at "Run agent": `Fix CI on #1077 [rd00z]` (run 37656412860), `Enrich issue #1078 [cycfz]` (37656768453) and `Label #1078 [6fbqg]` (37656774189). (2) Check `Zaxion Governance` on PR #1077 reported BLOCK. |
| **When** | (1) 2026-10-07T17:05:57Z to 17:10:40Z. (2) 2026-10-07T17:05:33Z to 17:05:50Z. |
| **Where** | (1) `.github/workflows/pullfrog.yml`. (2) PR #1077, 13 files. |
| **Why** | (1) Job log: `Pullfrog session error: You have no credits remaining. Add credits to continue using the API at https://platform.openai.com/settings/organization/billing/`. (2) Check output: `coverage` policy wants 1+ test file (PR has 0); `complexity_metrics` flags `INBOX/RECORD-OF-THE-VAULTED-ABHORSENS-FIRST-DRAFT-2026-05-31.md` at 754 lines (limit 300). |
| **How** | `gh api -X GET repos/LAF-US/IDAHO-VAULT/actions/runs -f status=completed -f 'created=2026-10-05T17:00:00Z..2026-10-07T17:10:00Z' -F per_page=100 --paginate`: 66 completed runs (56 skipped, 7 success, 3 failure), re-run on 2026-11-21 with the upper bound. The first count (64 completed, 1 failed) was taken near 17:10Z on 2026-10-07, before the two #1078 Pullfrog runs had finished, and had no upper bound; it is superseded. Job logs read via `get_job_logs` and the REST job-log endpoint; check text read via `get_check_run`. |

## Failures

| # | Failure | Category | Root cause | Next step |
|---|---|---|---|---|
| 1 | Pullfrog `Fix CI on #1077`, `Enrich issue #1078`, `Label #1078` (3 runs) | Provider billing | OpenAI account out of credits; all three logs read, same error (above) | Escalate: Logan tops up credits. Retry only after. |
| 2 | Zaxion Governance on #1077 | External policy check | Rules for tests and file length fire on a syntax-only frontmatter repair (#1077) | Investigate; not a repo workflow. Do not disable (`AGENTS.md` "Fix Errors - Do NOT Disable"). |

## Big IFs

- No failed repo workflow in the window ran tests. FixSense's issue #1078 ("no test report") reports a failure with no test step to attach a report to; the only failed workflows are the three billing failures above.
- Earlier Pullfrog dispatch failures since 2026-09-09 show `failure` in the run listing. Their logs were not read here, so no shared cause is claimed.
- The August failures (Python Test Suite, Codacy Coverage Reporter) have no runs in this window. Absence of runs is not evidence they were fixed.

## Surfaces written

GitHub: issue #1078 comment 6042877315. Linear: LAF-83. Slack: DM to Logan. Discord: not posted (Zapier `find_channel` for "general" returned no channel; none guessed).
