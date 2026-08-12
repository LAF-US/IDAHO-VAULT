---
name: worktreeConfig git format note
description: extensions.worktreeConfig without repositoryformatversion=1 can crash strict git implementations — historical note from Antigravity era
type: feedback
originSessionId: 52af37d3-c1c3-4af2-b0cf-cd5da2a33ed0
---
Do not set `extensions.worktreeConfig = true` without also setting `core.repositoryformatversion = 1`.

**Why:** Antigravity (Google desktop app, uninstalled 2026-04-18) used a strict Go-based git implementation that rejected `extensions.*` when `repositoryformatversion = 0`. Standard git tolerates the mismatch. Antigravity is gone, but the underlying git hygiene rule remains valid for any strict git client.

**How to apply:** When using git worktrees in IDAHO-VAULT, either (a) bump `core.repositoryformatversion` to `1` first, or (b) avoid setting `extensions.worktreeConfig` entirely. If worktree work is done, clean up by unsetting the extension.
