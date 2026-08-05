---
authority: Codex
date created: 2026-04-09
status: active
---

# Rewrite Prep Purge List — 2026-04-09

This is the approved starting scope for repo history rewrite preparation. The goal is to slim the repository before any destructive rewrite is executed.

## Primary tracked payload candidates

- `idex greater idaho/3D/NAmerica.dn`
- `idex greater idaho/3D/us-capitol-building/source/model/model.obj`
- `QodoGenVS_Release.vsix`
- `SCRATCH FOLDER/SCRATCH_2026.prin`
- `idex greater idaho/3D/north-america-3d-map/source/model/model.obj`
- `gh_2.89.0_windows_amd64.msi`

## Secondary candidates for review

- oversized tracked `.obsidian/plugins/` runtime artifacts
- historical-only large geographic/media objects identified in prior payload audits

## Deferred items

- LF/CRLF normalization across vault notes
- any broad formatting pass unrelated to repository payload size

## Rule for rewrite execution

Do not begin destructive `git filter-repo` work until:

1. rewrite prep is running from a disposable clean clone or worktree
2. `git-filter-repo` is installed and verified there
3. the final purge set is confirmed against current `main`
