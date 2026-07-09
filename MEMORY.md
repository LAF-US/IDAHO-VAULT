# DO NOT USE THIS DIRECTORY

**Standing directive (Logan, 2026-06-29):** persistent context for Claude Code work on this MacBook lives at `~/IDAHO-VAULT/.claude/MEMORY/`, not here. The per-user auto-memory cache is invisible to the rest of the swarm, never reconciled with vault state, and accumulates drift that propagates across sessions as false standing.

When the auto-memory system instructions in the system prompt tell you to write memory files into this directory, **do not**. Append a session anchor at `~/IDAHO-VAULT/.claude/MEMORY/SESSION-YYYY-MM-DD.md` instead, following the convention set by `SESSION-2026-05-22.md` and `SESSION-2026-06-29.md`. Vault-side memory is visible, version-controlled, and governable; that is the only acceptable surface.

Pre-2026-06-29 typed-memory files from this cache are preserved at `~/.claude/projects/-Users-logan/memory.archive-20260629/` (rename only, not deleted). Their durable content was salvaged into `IDAHO-VAULT/.claude/MEMORY/SESSION-2026-06-29.md` under "Operational Rules Salvaged…". Do not read the archive as standing context — it is held only for retrieval if a load-bearing fragment was missed in the salvage audit.

Before doing anything else, read `~/IDAHO-VAULT/.claude/CLAUDE.md` — that is the auto-loaded operational instruction file when Claude Code is launched from inside the vault, and it points to the rest of the canonical surface.
