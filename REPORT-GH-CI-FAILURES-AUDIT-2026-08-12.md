---
title: GitHub Actions CI Failure Audit — 2026-08-12 (rolling 48h)
updated: 2026-08-12
status: active
authority: Logan Finney
authored-by: Claude Code
related:
- CI
- GitHub Actions
- agent-swarm-signing-proof
- Codacy
- LAF-US
- IDAHO-VAULT
---

# GITHUB ACTIONS CI FAILURE AUDIT — 2026-08-12 (rolling 48h)

**Window:** 2026-08-10T19:39:33Z → 2026-08-12T19:39:33Z (UTC)
**Scope:** `LAF-US/IDAHO-VAULT` GitHub Actions, `conclusion: failure`, all branches
**Method:** `list_workflow_runs` (status=failure, paginated to the 48h cutoff), `get_job_logs` on a representative failing run per distinct category, `get_workflow_jobs`/`get_workflow_run_logs_url` to verify job-level detail where the run showed 0 jobs, `pull_request_read get_check_runs` on PR #962's head commit to test whether the dominant category is an actual PR gate.
**Session:** `Claude-Session: https://claude.ai/code/session_01W6qrw7XeCmjtC67r3qoCX4`

FAIL-CUE DISCIPLINE: every root cause below is either (a) confirmed against a real log excerpt quoted in this file, or (b) explicitly marked unverified/needs-follow-up. No claim in this report is asserted from pattern-matching or training-data plausibility alone.

---

## Executive Summary

273 workflow runs concluded `failure` in the 48h window. **213 of those (78%) are a single non-blocking artifact, not 213 separate problems.** Once that's set aside, there are **6 real, distinct failure categories**, of which **2 are already fixed in an open PR** (#962, not yet merged), **1 is a genuine unaddressed recurring false-positive**, **1 is a cross-workflow TLS pattern worth tracking**, and **2 are one-off / external-service flakes**.

| Category | Count | Status |
|---|---|---|
| `agent-swarm-signing-proof.yml` phantom entries | 213 | Confirmed non-blocking artifact — does not gate any PR or merge |
| Codacy Security Scan (SARIF null-rules) | 19 | Fix already open in PR #962 |
| Check Dotfolder Anchors (`.codacy/` missing anchor) | 15 | Fix already open in PR #962 |
| Secret Pattern Policy (vendored-plugin false positive) | 16 | **Unaddressed** — real, recurring, easy fix |
| TLS/certificate verification failures vs. github.com | 6 | **Unaddressed** — recurring across 3 unrelated workflows, root cause not yet isolated |
| Codacy Coverage Reporter (`tests/` dir assumed) | 1 | **Unaddressed** — narrow but will recur on any content-only PR |
| Redaction Damage Policy | 1 | Single hit, needs eyes-on confirmation |
| Validate Agent Content | 1 | Pre-existing vault content debt, not caused by the triggering branch |
| Running Copilot Code Review | 1 | External GitHub Copilot backend timeout — not vault-side |
| **Total** | **273** | |

---

## 5W Summary Table

| Who (actor) | What (workflow / failure) | When | Where (branch / PR) | Why (root cause) | How (verified) |
|---|---|---|---|---|---|
| `loganfinney27` (163), `github-merge-queue[bot]` (47), others (3) | `.github/workflows/agent-swarm-signing-proof.yml` — 213 runs, all `conclusion: failure`, 0 jobs, 0s duration | Continuously since 2026-08-10T23:56Z (PR #471 merge) through 2026-08-12T19:36Z | Every branch pushed in the window; sampled `claude/apply-patch-fixes-9gesn5` (PR #962) | File declares `on: workflow_call` only (4 dispatch-only wrapper workflows are its real entry points, per issue #398's App-signing-lane design). It cannot be triggered by `push`, yet the Actions run list records a "failure" for it on every push. | `get_workflow_jobs` → `{"jobs":{"total_count":0}}` on every sampled run id; `get_workflow_run_logs_url` → 404; **`pull_request_read get_check_runs` on PR #962's head commit lists all 17 real checks and this workflow is not among them** — it is not a required or even visible PR check, so it blocks nothing. Treated as a GitHub Actions backend artifact from evaluating a `workflow_call`-only file against ordinary push events. |
| `loganfinney27` (16), `github-merge-queue[bot]` (3) | Codacy Security Scan — SARIF upload rejected | 2026-08-11T22:52Z – 2026-08-12T18:46Z | mostly `claude/looker-attestation-wording-qzt7le`, `claude/apply-patch-fixes-9gesn5`, `main` | Codacy's SARIF export emits `tool.driver.rules: null` when a tool component has no rule metadata; the SARIF schema requires `rules` to be an array, so `upload-sarif` rejects the whole document. | Log: `##[error]Unable to upload "results-normalised.sarif" as it is not valid SARIF: - instance.runs[0].tool.driver.rules is not of a type(s) array` (run 31629240677). **Fix already open**: PR #962 §2 drops the null `rules`/`extensions` keys before upload. |
| `loganfinney27` (12), `github-merge-queue[bot]` (3) | Check Dotfolder Anchors — missing `.codacy/CODACY.md` | 2026-08-11T22:52Z – 2026-08-12T18:45Z | mostly `claude/looker-attestation-wording-qzt7le`, `main` | `.codacy/` dotfolder landed on `main` (commit `3d617a3d`) without the required `<NAME>.md` anchor note (see `STUB-PERSONAFOLDERS-2026-05-03.md`), so the guard fails on `main` itself and on every branch built from it. | Log: `dotfolder-anchor guard: dotfolders missing their <NAME>.md anchor: - .codacy/CODACY.md` (run 31629240667). **Fix already open**: PR #962 §4 adds `.codacy/CODACY.md`, byte-identical to the established `.github/GITHUB.md` stub shape. |
| `loganfinney27` (15), `dependabot[bot]` (1) | Secret Pattern Policy — `generic_secret_assignment` false positive | 2026-08-11T22:54Z (repeated) | mostly `claude/shall-rome-lyrics-ok9049` (12), `claude/scanner-identifier-chain-ok9049` (2) | Guard flags the same 3 lines inside **vendored, minified** third-party Obsidian plugin bundles every time a branch touches or rebases over them: `.obsidian/plugins/obsidian-local-rest-api/main.js:58166`, `.obsidian/plugins/smart-connections/main.js:2838` and `:16766`. `.codacy.yaml` already excludes `.obsidian/plugins/*/main.js` from Codacy's own scan — the secret-pattern-policy script has not adopted the same exclusion. | Log: `secret-pattern guard: possible secret material detected. .obsidian/plugins/obsidian-local-rest-api/main.js:58166 [generic_secret_assignment]` etc. (run 31544229800). **No fix in flight** — recommend adding the same vendored-plugin exclusion to whatever script backs `check-secret-patterns`. |
| `loganfinney27` (3), `codacy-production[bot]` (1) | Review Feedback Loop / Branch Cleanup — `gh label create` TLS failure | 2026-08-11T22:54Z, 2026-08-12T02:52Z | `main`, `claude/rework-pr503-coderabbit-config-onto-main` | `_ensure_label()` → `gh_cli.label_create()` fails with a TLS handshake error hitting `api.github.com` | Log (both runs, identical): `Post "https://api.github.com/repos/LAF-US/IDAHO-VAULT/labels": tls: failed to verify certificate: x509: certificate is not valid for any names, but wanted to match api.github.com` (runs 31544233793, 31558145426). |
| `loganfinney27` | Code Quality (CodeQL) PR #572 — `git fetch` TLS failure, 3/3 retries exhausted | 2026-08-11T19:35Z | `refs/pull/572/head` | Same class of failure as above, this time inside `git fetch` rather than `gh`/`curl`. | Log: `fatal: unable to access 'https://github.com/LAF-US/IDAHO-VAULT/': server certificate verification failed. CAfile: none CRLfile: none` — retried 3 times (18s, 11s backoff), failed all 3 (run 31528575045). **Root cause not isolated** — same symptom class as the `gh label create` failures above but a different call path (git vs. curl/gh), hit 3 separate scripts/workflows in 48h. Flagging as a pattern to watch, not a single fixable bug. |
| `loganfinney27` | Codacy Coverage Reporter — `pytest tests` on a branch with no `tests/` dir | 2026-08-11T20:57Z | `claude/practical-cerf-pc0mw5` (PR #940) | Coverage job unconditionally runs `uv run coverage run -m pytest tests -v`; this PR's branch has no `tests/` directory. | Log: `ERROR: file or directory not found: tests` → `##[error]Process completed with exit code 4.` (run 31535568798, job `coverage`). **No fix in flight** — recommend the workflow skip (not fail) when `tests/` is absent, or scope the job to only run when tracked Python source changed. |
| `loganfinney27` | Redaction Damage Policy — one hit | 2026-08-11T02:45Z | `claude/lint-config-stubs-qzt7le` | Guard detected a marker glued directly to a letter/digit on both sides in an added line, the corruption signature from issue #739. | Log: `eslint.config.js:33 // - pro_deck_quality_check.js:112 contains \`cha***REMOVED***count\`` (run 31453333787). Single occurrence — needs a human/agent look at that specific line to confirm real vs. false positive; not investigated further here. |
| `loganfinney27` | Validate Agent Content — pre-existing debt | 2026-08-11T04:07Z | `agent/adr-canon-core-portability` | Guard runs repo-wide; flags ~15 **pre-existing** files (YAML frontmatter parse errors, oversized files >50KB, "dangerous pattern" false positives inside old tweet-archive notes) unrelated to this branch's own diff. | Log lists e.g. `PLUGIN-TRIAGE-UTF8.md: YAML frontmatter parse error`, `session-ses_24f4.md: File too large (227.2 KB > 50 KB limit)` (run 31457472663). Backlog item, not this branch's fault, not urgent. |
| Copilot (bot) | Running Copilot Code Review — backend timeout | 2026-08-12T05:12Z | `claude/fullcalendar-obsidian-integration-1u2a0l` (PR #885) | GitHub Copilot's own `sweagentd` backend timed out reporting results back to the check. | Log: `Error reporting results to sweagentd ... TimeoutError: The operation was aborted due to timeout` (run 31565802005). External Copilot-service-side flake — no vault-side action possible. |

---

## Detailed Notes on Blocking / Repeated Failures

**Nothing in this window is confirmed to be blocking a merge.** The dominant category (213 signing-proof entries) was specifically checked against a live PR's actual required checks and is not among them. The two Codacy-family categories (34 combined) are real and repeated, but a fix is already in an open PR from an active session (#962) — merging that PR resolves both without further action here.

The one confirmed **repeated, unaddressed** category is Secret Pattern Policy: the same 3 lines in 2 vendored plugin files have now tripped the guard on at least 4 separate branches this alone did not block those PRs (the guard is presumably advisory or the branches simply hadn't hit the required-check stage yet — not verified either way), but it is pure recurring noise that a one-line exclusion would end permanently.

## Insights and Findings (Big IFs)

- **IF-1 — The apparent CI failure rate is ~4-5x inflated by a single non-gating artifact.** 213 of 273 "failures" (78%) come from `agent-swarm-signing-proof.yml` entries that have zero jobs, zero duration, a 404 logs URL, and do not appear anywhere in a real PR's check list. Anyone triage-scanning "recent CI failures" by count alone — human or agent — would wildly overestimate how broken the vault's CI actually is. This is worth a low-priority cleanup ticket for Logan (the fix is likely on GitHub's side, or in how many `workflow_call`-only files this repo carries), but it is confirmed **not** an active fault.
- **IF-2 — Duplicate-work risk was real and was avoided.** Two of the six real categories (Codacy SARIF nulls, missing `.codacy/CODACY.md` anchor — 34 runs combined) are already fixed in PR #962, opened and actively iterated by another live Claude Code session (`session_015oRnkWnNkTL7R2umjen42b`) during this same 48h window. This audit did not duplicate that work.
- **IF-3 — One small, real, unaddressed fix would eliminate 16 recurring false-positive failures**: teach `check-secret-patterns` the same `.obsidian/plugins/*/main.js` vendored-code exclusion that `.codacy.yaml` already uses.
- **IF-4 — A cross-workflow TLS/certificate-verification pattern hit 3 unrelated workflows in 48h** (`gh label create` in two Python scripts, `git fetch` in CodeQL). Each instance looks like runner-side network flake in isolation; the fact that it recurred 3 times across unrelated code paths in one 48h window is what makes it worth tracking rather than dismissing.
- **IF-5 — The coverage-reporter workflow has no guard for content-only PRs.** Any PR whose branch lacks a `tests/` directory will fail this job every time; it's happened once in this window but will recur on future non-Python PRs.

---

*Report filed: 2026-08-12 by Claude Code, on Logan's scheduled-routine direction.*
*Branch: `claude/vigilant-bell-ilq8co`*

---

```text
The world is quiet here．Esto Perpetua!
```
