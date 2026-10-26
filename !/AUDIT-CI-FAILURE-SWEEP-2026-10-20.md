---
title: CI Failure Sweep — 2026-10-20
type: audit
status: final
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-10-18T17:10Z to 2026-10-20T17:10Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-10-20

Read `CONSTITUTION.md` and `AGENTS.md` in full first. Every row below was read from its own job log (`get_job_logs failed_only`).

## 5W Summary

| | |
|---|---|
| **Who** | `pullfrog` (workflow_dispatch, branch `main`), provider OpenCode |
| **What** | 5 failed runs: `Review #1088 [8ph6k]` (39224762313), `Fix CI on #1088 [ewdor]` (39224774243), `Review new commits on #1088 [rhv5o]` (39224957514), `Review new commits on #1088 [736bz]` (39227430147), `Review #1089 [cb6he]` (39292218355). Category: provider credential. |
| **When** | 2026-10-19 08:43Z – 09:05Z (four runs); 2026-10-19 17:13Z (one run). |
| **Where** | `.github/workflows/pullfrog.yml`, job `pullfrog`, step "Run agent". |
| **Why** | Identical in all five logs: `provider error: This API key has expired. Create a new API key in OpenCode Console and replace it in your client or secret store.` |
| **How** | `actions_list` with `status=failure` (50 newest, 5 inside the window), then `get_job_logs failed_only` for each. Next step: escalate. Logan must rotate `OPENCODE_API_KEY` (console and repo secret) or choose a funded provider. No repo change fixes it; `pullfrog.yml` is do-not-edit. |

Also in the window, not failures: 2 `opencode` runs (39228459864, 39228460215, 2026-10-19 09:13Z, branch `muse/add-workspace-projects-20261019`) ended `action_required` with 0 jobs. Cause not investigated.

## Repeated failure

`pullfrog.yml` has failed for three different provider reasons since 2026-08-26: OpenAI quota/credits (08-26, 09-30, 10-07), OpenRouter credits (10-12, 10-15), OpenCode key expiry (10-19). Tracking: GitHub #1022, Linear LAF-83.

## Big IF

- The newest run of any kind in the repo is 2026-10-19T17:46Z (skipped). Nothing has run since, so whether the key has been rotated is unverified.
- Only the 50 newest failure runs were listed; older failures were not re-read here.

---
Cross-posted: GitHub #1022 (comment 6296648261), Linear LAF-83, Slack DM, Discord #ledger (via Zapier).

Claude-Session: https://claude.ai/code/session_019PFDpG6shj8cuxe3oc2zVb
