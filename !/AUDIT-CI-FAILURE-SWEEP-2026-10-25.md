---
title: CI Failure Sweep — 2026-10-25
type: audit
status: final
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, LAF-US/IDAHO-VAULT, 2026-10-23T17:09Z to 2026-10-25T17:09Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-10-25

Read `CONSTITUTION.md` and `AGENTS.md` in full first.

## 5W Summary

| | |
|---|---|
| **Who** | `Pullfrog` workflow, `workflow_dispatch` on `main` (head `14dbf54f`) |
| **What** | `Key check (no-op)`, run 40149111159, job `pullfrog`, step "Run agent": 1 failure in window. `cancelled`, `timed_out`, `startup_failure`, `action_required`: none in window. |
| **When** | 2026-10-25 01:03:22Z; failed 01:05:00Z (agent turn 2.9 s) |
| **Where** | `.github/workflows/pullfrog.yml` |
| **Why** | Job log: `Pullfrog session error: This API key has expired. Create a new API key in OpenCode Console and replace it in your client or secret store.` Provider-side credential expiry, not code. |
| **How** | `gh run list --status failure` and per-status queries; `gh run view 40149111159 --log-failed`. The five 10-19 to 10-21 failures (#1089–#1094) were re-checked and carry the identical error line. |

## Repeated / blocking

Same expired `OPENCODE_API_KEY` as 10-19, 10-20, 10-21. The 10-25 run is the first evidence that it was still expired after 10-21. Who dispatched the no-op check, and whether a rotation was attempted, is not known. Open dependabot bumps #1093 and #1094 do not address it (the error comes from the OpenCode API, not the action version).

**Needs Logan:** new key in OpenCode Console, replace the `OPENCODE_API_KEY` repo secret, re-run the no-op check. No repo-side fix; `pullfrog.yml` is DO NOT EDIT.

## Big IFs

- Three different provider credentials have failed in three weeks (OpenAI credits 10-07, OpenRouter credits 10-12/10-15, OpenCode key expiry 10-19 onward).
- Tracking: issue #1022, Linear LAF-83.

Claude-Session: https://claude.ai/code/session_01RsHM3yoNTsFThCdEhsR9ML
