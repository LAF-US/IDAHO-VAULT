---
name: Where things live in the vault
description: Key file locations, coordination systems, and external references
type: reference
---

## Vault Key Files

| What | Path |
|---|---|
| Live coordination board | `!/!/!/! The world is quiet here/DOCKET.md` |
| Rolling ecosystem state | `!/!/LEVELSET-CURRENT.md` |
| Confirmed decisions log | `DECISIONS.md` |
| Vault governance (canonical) | `CONSTITUTION.md` |
| Claude Code instructions | `CLAUDE.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Agent registry (canonical) | `!/AGENTS.md` |
| Cross-tool pointer (auto-load) | `AGENTS.md` (root) — thin pointer for Codex/Copilot/Qodo |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| NETWEB path guard (CI) | `.github/workflows/check-portable-paths.yml` |

## External Coordination

| System | Purpose |
|---|---|
| github.com/loganfinney27/IDAHO-VAULT | Public repo — all agents work here |
| GitHub Issues with `agent:*` labels | Task assignment to specific agents |
| Linear (SWARM label) | Task tracking |
| Slack | Ephemeral breadcrumbs only — not durable |

## Orientation Protocol

When starting a new session: read `!/!/LEVELSET-CURRENT.md` and `!/!/!/! The world is quiet here/DOCKET.md` to orient. Check git status for branch state.
