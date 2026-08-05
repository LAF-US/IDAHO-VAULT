---
title: PHONE-LINK / CrossDevice Adjudication
date created: 2026-07-09
updated: 2026-07-09
authority: LAF
author: Codex
agent_standing: "!.*.codex.*"
status: forward
doc_class: adjudication
related:
  - Phone Link
  - CrossDevice
  - Link to Windows
  - Android
  - Obsidian
---

# PHONE-LINK / CrossDevice Adjudication - 2026-07-09

## Purpose

This record implements the examination phase for the local PHONE-LINK work. It does not assume that any existing script is correct, canonical, or salvageable. The goal is to distinguish observed facts, prior attempts, live channels, and proposed disposition before editing or deleting implementation files.

## Current Local Facts

- Current checkout examined: `C:\Users\loganf\Documents\IDAHO-VAULT`
- Current branch: `logan/obsidian`
- Local status at examination time: branch was behind `origin/logan/obsidian` by 9 commits and had unrelated dirty/untracked vault changes.
- Local Phone Link receive folder exists: `%USERPROFILE%\Downloads\Phone Link`
- Local CrossDevice root exists: `%USERPROFILE%\CrossDevice`
- CrossDevice exposes `Pixel 10 Pro\storage\...`, including Android-style folders such as `DCIM`, `Download`, `Pictures`, and `Documents\IDAHO-VAULT`.
- `INBOX\PHONE-LINK` was referenced by older notes and scripts, but did not exist at `C:\Users\loganf\Documents\IDAHO-VAULT\INBOX\PHONE-LINK` during this examination.

## External Source Check

- Microsoft documents Android-to-PC file sharing through Phone Link / Link to Windows, with files received on the PC under `Downloads\Phone Link` and a configurable storage directory.
- Microsoft separately documents the Windows 11 File Explorer mobile-device surface, which exposes phone files under `C:\Users\<username>\CrossDevice`.
- Google Play lists `Link to Windows` as Microsoft Corporation's Android-side app for the Windows Phone Link pairing.

Sources:

- Microsoft Support: `https://support.microsoft.com/en-US/Windows/Apps/PhoneLink/seamlessly-transfer-content-between-your-devices`
- Microsoft Support: `https://support.microsoft.com/en-US/Windows/experience/fileexplorer/setting-up-and-using-your-phone-in-file-explorer`
- Google Play: `https://play.google.com/store/apps/details?id=com.microsoft.appmanager`

## Lineage Findings

- Current `logan/obsidian` contains `.github/scripts/phone_link_intake.py`, root wrappers, root notes, root tests, and tracked residue files.
- `origin/codex/phone-link-explicit-vault-root` contains later PHONE-LINK work that is not an ancestor of current `logan/obsidian`.
- That remote branch adds `.github/scripts/phone_link_auto_sweep.py`, changes the PowerShell wrapper into a Python compatibility shim, updates the CMD startup wrapper to launch Python, updates the intake script with `--vault-root`, deletes root test residue files, deletes `PHONE-LINK.md`, and moves/adds tests under `tests/`.
- The remote branch is evidence of prior work, not authority. It should not be adopted whole without review because it still contains a legacy fallback path and startup/autosweep decisions that need separate approval.

## Artifact Verdict Table

| Artifact | Observed role | Verdict | Rationale |
| --- | --- | --- | --- |
| `.github/scripts/phone_link_intake.py` | Current Python manual intake | Rewrite candidate | This is the closest current Python program surface, but current branch lacks later explicit-root handling and tests fail from root placement. |
| `Phone Link.md` | Human-facing workflow note | Keep and revise later | It records the intended channel, but currently hard-codes local paths and does not clearly separate CrossDevice. |
| `PHONE-LINK.md` | Folder-index style stub at root | Remove candidate | Content is a generated folder-index stub, not a meaningful root doctrine or implementation record. |
| `phone-link-intake.bat` | Windows launcher for Python intake | Keep candidate | Thin launcher is useful for local ergonomics if the Python target is made correct. |
| `phone-link-auto-sweep.ps1` | Current PowerShell watcher | Deprecate or replace candidate | It hard-codes the vault path and implements behavior outside the Python-first preference. Do not restore startup around it. |
| `START-PHONE-LINK-SWEEP.cmd` | Startup launcher for current watcher | Freeze/defer | Startup behavior should not be changed until the program-level decision is proven. |
| `STOP-PHONE-LINK-SWEEP.cmd` | Stops watcher processes | Freeze/defer | Operationally relevant only if autosweep remains in scope. |
| `RESTART-PHONE-LINK-SWEEP.cmd` | Restart wrapper | Freeze/defer | Operationally relevant only if autosweep remains in scope. |
| `phone-link-sweep-launcher.vbs` | Hidden-window launcher | Freeze/defer | Startup/window behavior is explicitly later than program correctness. |
| `!-PHONE-LINK-phone-link-auto-sweep.ps1` | Older tracked watcher to `INBOX\PHONE-LINK` | Archive/deprecate candidate | Represents older intake routing and should not be treated as current without a separate decision. |
| `!-PHONE-LINK-START-PHONE-LINK-SWEEP.cmd` | Older launcher | Archive/deprecate candidate | Paired with older watcher. |
| `test_phone_link_intake.py` | Root test file | Remove or relocate candidate | It fails from root because `PROJECT_ROOT = parents[1]` resolves above the repo. |
| `tests-test_phone_link_intake.py` | Duplicate/misnamed test file on remote branch only | Remove/replace candidate | Name indicates prior flatten or misplacement, not a stable test path. |
| `phone_link_source_*.md` | Tracked test residue files | Remove candidate | These are synthetic temporary-source artifacts committed into root. |
| `phone_link_vault_*.md` | Tracked test residue files | Remove candidate | These are synthetic temporary-vault artifacts committed into root. |
| `intake-log.md` | Batch intake log | Keep pending review | It may be evidence of actual intake history; do not delete as debris without reviewing entries. |
| `INBOX-README.md` | Intake policy note | Keep and revise later | It records the historical exception for Phone Link and should be synchronized with the chosen workflow. |
| `.github/scripts/phone_link_auto_sweep.py` from `origin/codex/phone-link-explicit-vault-root` | Prior Python autosweep candidate | Evaluate selectively | Useful evidence and possible source material, but autosweep and startup are out of the first program-correctness pass. |
| `tests/test_phone_link_intake.py` from `origin/codex/phone-link-explicit-vault-root` | Prior relocated tests | Evaluate selectively | Better placement than root tests, but should be reviewed against the final chosen tool behavior. |
| `tests/test_phone_link_contract.py` from `origin/codex/phone-link-explicit-vault-root` | Prior contract tests | Evaluate selectively | May encode useful invariants about no hard-coded local paths. |

## Channel Boundary

Phone Link and CrossDevice are both active on this device, but they are not the same workflow.

- Phone Link is a drop-folder intake channel. A tool may safely target `%USERPROFILE%\Downloads\Phone Link` as a source after explicit source resolution and dry-run support.
- CrossDevice is a browsable phone filesystem mirror. It must not be silently swept by the Phone Link tool.
- CrossDevice implementation is out of scope for this pass.

## Recommended Next Implementation Pass

1. Create a focused branch from the correct current base after synchronizing `logan/obsidian`.
2. Port only reviewed pieces from `origin/codex/phone-link-explicit-vault-root`.
3. Make the Phone Link Python manual intake the first verified program surface.
4. Move or recreate tests under `tests/` and remove the root test residue only in the same PR that proves the replacement tests pass.
5. Update `Phone Link.md` and `INBOX-README.md` after the executable behavior is verified.
6. Leave startup/autosweep configuration untouched until the manual Python intake is correct.

## Non-Decisions

- No CrossDevice transfer semantics are chosen here.
- No startup item is restored here.
- No current artifact is declared canonical solely because it exists.
- No prior branch is declared authoritative solely because it contains newer-looking code.
