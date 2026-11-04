---
title: CI Failure Sweep — 2026-10-21
type: audit
status: final
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-10-19T17:09Z to 2026-10-21T17:09Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-10-21

Read `CONSTITUTION.md` and `AGENTS.md` in full first. Both rows below were read from their own job log (`get_job_logs failed_only`).

## 5W Summary

| | |
|---|---|
| **Who** | `pullfrog[bot]` (workflow_dispatch, branch `main`), provider OpenCode |
| **What** | 2 failed runs: `Review #1089 [cb6he]` (39292218355), `Review #1090 [ku2vh]` (39464086257). Category: provider credential. |
| **When** | 2026-10-19 17:14Z and 2026-10-20 17:14Z |
| **Where** | `.github/workflows/pullfrog.yml`, job `pullfrog`, step "Run agent" |
| **Why** | Identical in both logs: `provider error: This API key has expired. Create a new API key in OpenCode Console and replace it in your client or secret store.` |
| **How** | `actions_list` pages 1–2 (100 runs each; page 1 spans 10-19T17:13Z–10-21T08:23Z, page 2 reaches 10-19T09:05Z). Page 1: 79 skipped, 17 success, 3 cancelled, 1 failure; page 2 holds the other in-window failure. Next step: escalate. Logan must rotate `OPENCODE_API_KEY` (console and repo secret). `pullfrog.yml` is do-not-edit. |

## Repeated failure

Same fault as the 2026-10-19 and 2026-10-20 sweeps. The `Review #1090` run is new since the 10-20 report and ran after it, so the key was still expired on 2026-10-20T17:14Z. Tracking: GitHub #1022, Linear LAF-83.

## Big IFs

- No non-skipped run exists after 2026-10-20T17:14Z, so whether the key was rotated is unverified.
- Three distinct provider-credential failures in 14 days (OpenAI credits 10-07, OpenRouter credits 10-15, OpenCode key 10-19/20); nothing in the repo detects an exhausted credential before a review is needed.
- Oldest open items #252 (policy calls reserved to Logan) and #1029 (Logan's DO NOT MERGE) were left untouched. #1072 (one-line SHA-pin bump in `opencode.yml`, green, `clean`) had auto-merge armed.

---
Cross-posted: GitHub #1022 (comment 6321944962), Linear LAF-83, Slack DM, Discord #ledger (via Zapier).

Claude-Session: https://claude.ai/code/session_01UUY437a2cVajiM5pU58dVq
