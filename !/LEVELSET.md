---
tags:
  - administration/levelset
updated: 2026-03-29
status: active
source: ground-truth
---

# LEVELSET

Current status of the IDAHO-VAULT ecosystem as of **2026-03-29 (UTC)**.
This file is intentionally rewritten as a fresh snapshot to remove stale assumptions.

## Ground Truth Snapshot

- **Repository:** `IDAHO-VAULT`
- **Current branch:** `work`
- **HEAD commit:** `16e8536` (`chore(gitignore): ignore local mcp-server.exe binary`)
- **Working tree:** clean (no staged or unstaged changes)
- **Recent baseline:** merges for PR #102 and PR #103 are present in history
- **Markdown file count:** 3,595 (`*.md`)

## What Changed Since Prior LEVELSET

The previous LEVELSET carried historical operational assumptions from 2026-03-15/16 that were no longer reliable for day-to-day execution. This refresh:

1. Drops old blocker/task lists that were tied to earlier coordination windows.
2. Anchors status to current git facts (branch, commit, cleanliness).
3. Preserves governance source-of-truth references without stale execution guidance.

## Current Governance Anchors

Use these files as the active orientation stack:

1. `!/CONSTITUTION.md`
2. `!/PROTOCOL.md`
3. `!/AGENTS.md`
4. `!/LEVELSET.md` (this file)
5. `!/VAULT-CONVENTIONS.md`
6. `!/VAULT-ZONES.md`
7. `!/DECISIONS.md`

## Active Notes

- Root `AGENTS.md` remains the cross-tool pointer; canonical registry is `!/AGENTS.md`.
- No conflict markers or in-progress merge state detected.
- The latest local change is gitignore hygiene for a machine-local MCP binary path.

## Operator Guidance (Now)

When resuming work in a new session:

1. Re-check branch + clean state (`git branch --show-current`, `git status --short`).
2. Validate latest commits (`git log --oneline -n 8`).
3. Confirm any requested task against current vault files before carrying forward historical assumptions.

