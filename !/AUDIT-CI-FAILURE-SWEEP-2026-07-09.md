---
title: CI Failure Sweep — 2026-07-09
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-08T04:00Z to 2026-07-09T04:15Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-09

## 5W Summary

| | |
|---|---|
| **Who** | No new human-caused breakage. One item needs a look for possible leaked secret material (below). |
| **What** | 47 failing runs across 7 workflows: Codacy (29, known token gap), Sync Plugin Registry (8, known chronic), Sync Agent Discovery Index (4, known chronic), Secret Pattern Policy (1, NEW), Validate Agent Content (1, known pattern/new branch), Redaction Damage Policy (1, NEW), Python Test Suite (2, NEW regression), Claude Sign (1, NEW/unclear). |
| **When** | 2026-07-08T04:00Z – 2026-07-09T04:15Z |
| **Where** | Codacy/Sync failures: `main` and `logan/obsidian` pushes. New items: `agent/adr-canon-core-portability`, `agent-git-guardrails`, `codex/phone-link-explicit-vault-root`, `claude/draft-signing-via-action-2026-06-01`. |
| **Why** | See per-item below. |
| **How** | See per-item next step. `cloud-run-deploy.yml` (the deploy workflow) had zero runs in the window — nothing to report there. |

## Blocking / repeated

- **Codacy Security Scan (29 runs)** — still failing, but now purely on the already-tracked `CODACY_PROJECT_TOKEN` missing-credentials error (`Could not get remote project configuration: No credentials found.`), confirmed on run 28993399166. The SARIF-crash bugs from yesterday are gone; this is the same open item in #822 waiting on you to provision the token or drop the workflow.
- **Sync Plugin Registry (8) / Sync Agent Discovery Index (4)** — same chronic drift-check pattern on `logan/obsidian` push, already tracked in #822. No new information.

## New findings

1. **Secret Pattern Policy — possible secret material, `logan/obsidian` push (run 28981227139, 2026-07-08T22:51:25Z).** Flagged a `[google_api_key]`-shaped pattern in 4 journal markdown files. **Category: Configuration/Security.** Worth a direct look — could be a real leaked key or a false positive from quoted example text. Not something to wave off; suggest you check those 4 files directly.
2. **Redaction Damage Policy — `agent-git-guardrails` PR (run 28962574565, 2026-07-08T17:29:16Z).** A redaction/sanitization script is clobbering substrings *inside* words across many files (`sho***REMOVED***description`, `impo***REMOVED***edges`, etc.) instead of whole secret values. **Category: Code bug.** Next step: find and fix the redaction script's matching logic on that branch — it's over-matching word-internal substrings.
3. **Python Test Suite — `codex/phone-link-explicit-vault-root` PR, real regression (runs 28980007941, 28979980554).** 4 errors in `tests/test_phone_link_contract.py`: fixtures reference vault-root paths (`IDAHO_VAULT_ROOT`, explicit vault root) that are never created in CI. **Category: Code bug** in that branch's test setup, not flaky — next step: fix the test fixtures on that branch to create the expected directories, or mock `require_existing_dir`.
4. **Validate Agent Content — `agent/adr-canon-core-portability` (run 28921488227).** Same size-limit pattern as yesterday: a generated `!/TOPOLOGY-CENSUS-dotfolders-*.md` census artifact (177.5 KB) exceeds the 50 KB content policy on that branch. **Category: Configuration.** Next step: exclude generated census output from that branch, or don't commit it there.
5. **Claude Sign — anomalous, zero jobs (run 28919974166).** Same unresolved oddity as yesterday: conclusion `failure`, but no jobs recorded at all. **Category: Infrastructure, unclear.** Needs a look in the Actions UI directly; not diagnosable via the API.

## Big IF

Two of today's five new findings (Redaction Damage, Python Test Suite) are **real code bugs on active agent branches**, not CI flakiness or config gaps — worth flagging to whoever's driving those branches (`agent-git-guardrails`, `codex/phone-link-explicit-vault-root`) directly rather than leaving them for the next sweep to re-report.
