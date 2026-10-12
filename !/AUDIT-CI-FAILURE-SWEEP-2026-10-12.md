---
title: CI Failure Sweep — 2026-10-12
type: audit
status: complete
authority: CLAUDE (routine CI sweep, session 01NeytW4Qm4BWDLNyFkvUgt4)
scope: GitHub Actions runs, LAF-US/IDAHO-VAULT, 2026-10-10T05:00Z to 2026-10-12T05:10Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-10-12

## 5W Summary

| | |
|---|---|
| **Who** | `pullfrog[bot]` (2 workflow_dispatch runs on `main`); GitHub Copilot code-review backend (1 dynamic run). |
| **What** | 3 failed runs, all targeting PR #1029: `Review #1029 [0plph]` (38195304637), `Fix CI on #1029 [sadlq]` (38195347778), `Running Copilot Code Review` (38195296886). |
| **When** | 2026-10-12, dispatched 02:18:59Z to 02:19:48Z; failed 02:19:37Z (Copilot), 02:41:56Z (Fix CI), 02:57:56Z (Review). |
| **Where** | `.github/workflows/pullfrog.yml` (job `pullfrog`); Copilot reviewer job `copilot-pull-request-reviewer`. |
| **Why** | See Failures table; every row is a consequence of PR #1029's size (head `0c58d805`, 5,343 commits), not of a repo script or test. |
| **How** | `actions_list` (100 newest runs, 2026-10-07T21:35Z to 2026-10-12T05:07Z, so the window is fully covered): 84 skipped, 11 success, 3 failure, 2 cancelled. Job logs read with `get_job_logs`. |

## Failures

| # | Failure | Category | Root cause (from log) | Next step |
|---|---|---|---|---|
| 1 | Copilot Code Review, #1029 | External service limit | `HttpError: The diff is taking too long to generate` fetching `827811e3...0c58d805` | None possible in-repo. Goes away only when the diff is reviewable. |
| 2 | Pullfrog `Fix CI on #1029` | Timeout | `pullfrog_checkout_pr #1029 exceeded 570s`, then `activity timeout: no output for 1170s` | Do not retry; the checkout cannot finish on this history. |
| 3 | Pullfrog `Review #1029` | Timeout / dirty tree | `cannot checkout PR #1029 while the working tree has uncommitted changes` (`node_modules/`, `src/`), then `activity timeout` after 904s | Same as 2. |

Runs 2 and 3 were `workflow_dispatch` runs on `main`. `pullfrog.yml` only receives dispatches (inputs `prompt`, `name`); the dispatcher is the Pullfrog app, not a repo file, so no repo-side guard exists to edit.

## Repeated failure

Pullfrog "Fix CI on #1029" also failed 5 times between 2026-09-23 and 09-30 (per the 2026-10-10 comment on #252); the 09-30 run was OpenAI "no credits remaining". Today's cause is different (timeout), so the two are not one fault.

## Big IFs

- Logan's 2026-09-26 comment and the PR #1029 body both say DO NOT MERGE / do not rebase, retarget or push while chunks land. Today's three failures began when #1029 was marked ready for review (02:19Z per the 05:07Z comment on #1029), which fires the review bots. The PR is still `mergeable_state: dirty`.
- A comment on #1029 reports auto-merge was enabled at 04:00Z. I did not verify that. If true, it contradicts the body notice; `CONVENTIONS` says to park a waiting PR as draft. I changed nothing: this is Logan's call.
- Head has not moved: `0c58d805`, 5,343 of the notice's 9,370 commits.

## Surfaces written

GitHub: issue #252 comment. Linear, Slack, Discord, Zapier: see the PR description for what was posted or why not.
