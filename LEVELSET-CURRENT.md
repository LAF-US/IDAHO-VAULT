---
authority: LOGAN
related:
  - AGENTS
  - CONSTITUTION
  - DECISIONS
  - DOCKET
  - LEVELSET
  - PRIVACY
  - VAULT-CONVENTIONS
updated: 2026-04-17
---

# LEVELSET-CURRENT — Live Ecosystem State

**Mother anchor:** [[LEVELSET]] — permanent snapshot; this file is its rolling child. Do not accumulate doctrine here.

**Scope:** Repository + infrastructure snapshot only. Updated in place each LEVELSET round — not appended.

**Doctrine homes:** CONSTITUTION.md · PRIVACY.md · `!/AGENTS.md` · DOCKET.md

---

## REPOSITORY

| Field | Value |
|---|---|
| Remote | github.com/LAF-US/IDAHO-VAULT (public) |
| Primary branch | `main` at `9bb6b028` |
| Pack size | ~332 MiB trash identified — Phase 2 rewrite pending (Logan unblock required) |

## INFRASTRUCTURE

| Asset | Location | Status |
|---|---|---|
| `.claude/CLAUDE.md` | `.claude/` | Operational |
| `.gemini/GEMINI.md` | `.gemini/` | Operational |
| `.codex/CODEX.md` | `.codex/` | Operational |
| `.github/copilot-instructions.md` | `.github/` | Operational |
| `CONSTITUTION.md` | root | Canonical governance — revised 2026-04-17 |
| `PRIVACY.md` | root | Data classification + MCP bridge rules |
| `!/DECISIONS.md` | `!/` | Decision log |
| `!/AGENTS.md` | `!/` | Agent registry |
| `!/VAULT-CONVENTIONS.md` | `!/` | Shared conventions |
| `!/GRIMOIRE/` | `!/GRIMOIRE/` | TTT + knowledge artifacts |
| `.crewai/` | `.crewai/` | CrewAI crews — env stable, E2E blocked on API credits |
| `.github/scripts/chainfire.py` | `.github/scripts/` | CHAINFIRE burn script |
| `.github/workflows/check-portable-paths.yml` | `.github/workflows/` | NETWEB path validator |
| `swarm.json` | root | Machine-readable ecosystem registry |

## AUTOMATION

| Job | Schedule | Status |
|---|---|---|
| Idaho Legislature scraper | Daily 6 AM MT | Running |
| Budget tracker CSV export | Daily 6:30 AM MT | Running |
| Vault sort audit | Monday 6 AM UTC | Weekly |
| Wayback preservation | Monday 8 AM UTC | Weekly |

---

*LEVELSET-CURRENT.md — rolling snapshot, updated in place. Permanent audit trail in numbered snapshots stored in `!/!/`. Last updated: 2026-04-17 by The Abhorsen.*
