---
title: CI Failure Sweep — 2026-07-23
type: audit
status: draft
authority: CLAUDE (routine CI sweep)
scope: GitHub Actions workflow runs, laf-us/idaho-vault, 2026-07-22T08:24Z to 2026-07-23T07:19Z
owner: Logan Finney
---

# CI Failure Sweep — 2026-07-23

## 5W Summary

| | |
| --- | --- |
| **Who** | GitHub Actions runners on `laf-us/idaho-vault`; Claude Code (this session, scheduled). No new human-caused breakage. |
| **What** | 20 failing runs across 5 workflows: Codacy Security Scan (7) + Codacy Coverage Reporter (7, day 15 of the same known account-side gap), `check-notebooks-paired` (3, NEW — root-caused and fixed this pass, not just re-flagged), Sync Plugin Registry (2, known chronic), Secret Pattern Policy (1, known false-positive class). |
| **When** | 2026-07-22T08:24Z – 2026-07-23T07:19Z |
| **Where** | Codacy: `claude/practical-cerf-dpdkku` (PR), `main` (push). `check-notebooks-paired`: `claude/practical-cerf-dpdkku`, `claude/draft-signing-via-action-2026-06-01`, `claude/shall-rome-lyrics-ok9049` (all PRs against `main`). Sync Plugin Registry / Secret Pattern Policy: `logan/obsidian` (push). |
| **Why** | See per-item below. |
| **How** | See per-item next step. No stuck `in_progress`/`queued` runs found; no other workflow with a `failure` conclusion in-window. |

## Blocking / repeated

- **Codacy Security Scan / Codacy Coverage Reporter (14 runs)** — unchanged, day 15. Confirmed non-blocking (`mergefreeze` is the actual merge gate, per Logan's 2026-07-11 correction in #822). Root cause open question stands as last corrected on 2026-07-21: either `CODACY_PROJECT_TOKEN` doesn't belong to this specific repo's Repository API token, or the repo was never opened in the Codacy account's repo list — not re-diagnosed further this pass, still Logan's call.
- **Sync Plugin Registry (2 runs, `logan/obsidian`)** — same chronic `manifest.json`/`swarm.json` drift-check pattern (confirmed via job log: `Run: python .github/scripts/sync_obsidian_plugin_registry.py --write`). Fix (#831/#834) remains parked per Logan's 2026-07-10 direction not to touch either PR further until he decides; not touched this pass.
- **Secret Pattern Policy (1 run, `logan/obsidian`)** — flagged a `[google_api_key]`-shaped pattern in `2026-07-17 - It's official_ McCall OKs new farm supply retailer.md:74`. Consistent with the false-positive class diagnosed 2026-07-11/2026-07-22 (third-party embed tokens baked into saved webpage captures, e.g. Google Static Maps tile URLs) — not independently re-verified against this specific file's content this pass, so flagging with the same "needs your one-time confirmation" caveat rather than asserting it's resolved.

## New findings — root-caused and fixed, not just re-flagged

**`check-notebooks-paired` (3 runs: `claude/practical-cerf-dpdkku`, `claude/draft-signing-via-action-2026-06-01`, `claude/shall-rome-lyrics-ok9049`).** All three failures, on three unrelated branches, showed the byte-identical diff: `LLM-Router.md | 2 +-`. That ruled out per-branch content drift immediately — three independent branches don't converge on the same one-line change unless the drift is actually on `main` itself.

Reproduced locally: checked out `main` (`ed549676`), ran `.github/scripts/jupytext_sync_paired.py`. With `jupytext` installed per the workflow's floating `"jupytext>=1.16,<2"` spec, pip resolves to the newest release (**1.19.5**, shipped after `LLM-Router.md`'s twin was last committed and stamped `jupytext_version: 1.19.4`). Every sync run rewrites that frontmatter stamp to whatever version is installed, so the "twin out of sync" check fails on **any** PR that touches an `.md`/`.ipynb` file — which is most of them — regardless of what the PR itself changed.

Confirmed the fix by re-running with `jupytext==1.19.4` installed (matching the version already pinned in `requirements.txt`): zero diff, clean run.

**Category: Code (CI script/workflow bug — floating dependency version, not a real content drift).**

**Fixed this pass:** `.github/workflows/check-notebooks-paired.yml` no longer installs a floating `jupytext>=1.16,<2` range. Existing `tests/test_helper_scripts.py::JupytextSyncPairedTest` (5 tests, all mock the `jupytext` subprocess call directly) pass unchanged throughout; no new test was needed since this is a version-pin/install-source fix, not a code-path change.

*Update, same review cycle:* the first version of this fix hardcoded `jupytext==1.19.4` as a workflow literal. Before this PR merged, an unrelated commit landed on `main` (the POKA-YOKE.md / codacy.yml rework) that carried its own stray re-sync of `LLM-Router.md`, stamping it `jupytext_version: 1.19.5` — which immediately drifted from this PR's hardcoded `1.19.4` pin the moment `main` was merged into this branch. Same failure class, inverted. The durable fix parses the version out of `requirements.txt` at run time instead (`sed -n 's/^jupytext==\([^[:space:]#]*\).*/\1/p' requirements.txt`, with a validation step that fails closed with a clear error if no pin is found there), so there is exactly one place this version can live and the workflow's install can never disagree with what's actually committed. `LLM-Router.md` was re-synced against `jupytext==1.19.4` (still current in `requirements.txt` as of this writing) to clear that second drift.

## Big IF

This was a **repo-wide, always-on false-positive waiting to happen on the next jupytext point release** — indistinguishable from real branch drift in the GitHub Actions UI (same error text: "A notebook twin is out of sync") until someone diffed multiple branches' failures against each other and noticed they were identical. The same failure mode (CI installs an unpinned/floating tool version that drifts ahead of what's actually committed to the repo) is worth a quick grep across other `check-*.yml` workflows for other floating `pip install` specs — not done in this sweep, flagging as a follow-up rather than asserting the rest are clean.

## Not touched, not this sweep's to fix

- Codacy account/token gap — Logan's call (provision vs. retire vs. dashboard fix), unchanged.
- Sync Plugin Registry / Sync Agent Discovery Index self-heal (#831/#834) — parked per Logan's explicit 2026-07-10 instruction.
- Secret Pattern Policy `logan/obsidian` false-positive class — needs Logan's one-time confirmation before any exemption is added, per the same standing caution as prior sweeps.
