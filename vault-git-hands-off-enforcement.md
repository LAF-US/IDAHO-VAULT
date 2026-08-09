---
name: vault-git-hands-off-enforcement
description: "Vault git state is deliberately staged by Logan's enforcement; secrets embedded in staged content; explicit affirmative from Logan required before ANY action, including content reads"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e2caf928-c9ac-4e5a-90ee-4a36a4f000b2
  modified: 2026-08-05T00:27:44.725Z
---

Logan's standing rule (stated 2026-08-04): do not touch anything in IDAHO-VAULT — no git commands, no file writes, no content reads — without asking and receiving an explicit affirmative answer from Logan first.

Context: prior agents repeatedly edited `.gitignore` as it suited them. Logan ran a strict enforcement effort; the resulting git state (hundreds of staged runtime/session artifacts on `logan/obsidian` — `.jsonl` session transcripts, hash-named files, `.makemd` caches) is the deliberate outcome of that effort, not an accident. A session's first-look inference that this was "accidentally staged temp files" was wrong and Logan corrected it.

**Why:** Much of the staged content has secrets embedded, and the repo remote is public (github.com/LAF-US/IDAHO-VAULT). A push or commit could leak secrets; even reading file contents copies secret material into session context — and session transcripts themselves land inside the vault by design (Runtime Containment), so ingested secrets can re-enter the repo.

**How to apply:** Assume nothing about the git state being a mistake. Ask before any action. If diagnostics are authorized, prefer path/metadata-level inspection (`--stat`, `--name-only`) over content reads unless Logan explicitly wants deeper. Never push, commit, stage, unstage, or edit `.gitignore` without his explicit yes.
