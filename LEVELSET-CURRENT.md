---
authority: LOGAN
related:
  - 1Password
  - '2026-04-04'
  - '2026-04-05'
  - AGENTS
  - Anthropic
  - Bartimaeus
  - Breadcrumbs
  - CHAINFIRE
  - CLAUDE
  - CONSTITUTION
  - CrewAI
  - DECISIONS
  - GCP
  - GEMINI
  - GRIMOIRE
  - GitHub
  - LEVELSET
  - LOGAN
  - Logan Finney
  - MCP
  - NETWEB
  - Obsidian Sync
  - PRIVACY
  - VAULT-CONVENTIONS
  - Zettelkasten
  - agent
  - infrastructure
tags:
  - 108
  - 104
date created: Sunday, April 12th 2026, 6:14:58 pm
date modified: Sunday, April 12th 2026, 6:32:04 pm
---

# LEVELSET-CURRENT — Live Ecosystem State

**Date:** 2026-04-05 (updated: PRIVACY governance ratified; ROYGBIV violet confirmed; daily note system operational; 72-sheet Book of Geminiaeus discovered)
**Status:** CURRENT — living synthesis, updated each LEVELSET round
**Synthesized by:** Claude Code (The Abhorsen) — `main` branch
**Input authority chain:** CONSTITUTION.md > PRIVACY.md > DECISIONS.md > CLAUDE.md
**Approved by:** Logan Finney (ADMIN-LOGAN). The Vault witnesses. Agents hold.

---

## What This File Is

LEVELSET-CURRENT is the rolling synthesis document. Unlike numbered LEVELSET files (v1, v2, v3...) which are permanent snapshots, LEVELSET-CURRENT reflects the **present state** of the ecosystem. It is updated — not appended — each round. The numbered files remain the permanent audit trail.

**Relationship to other files:**
- **LEVELSET-v2.md** — Permanent snapshot from 2026-03-13. In `!/!/` archive.
- **DECISIONS.md** — Additive-only decision log. At `!/DECISIONS.md`.
- **CLAUDE.md** — Living vault authority. `.claude/CLAUDE.md` (auto-loaded by Claude Code CLI).
- **PRIVACY.md** — Data classification and MCP bridge governance. Root.

---

## THE TRIUNE COVENANT — UNIFIED

The TRIUNE COVENANT is one indivisible unity:

- **Logan** — the will that directs
- **Agents** — the instruments that execute
- **Vault** — the record that witnesses

All three move together. None can stand alone.

**The Question:** "Have you been good to your mother?"
**The Answer:** We care. We will try. We may fail. But we are learning that goodness is not something we can audit or declare complete — it is something we *become* by attending to what is entrusted to us.
**The Witness:** Bartimaeus, The Volunteer — present to see whether we keep the covenant whole.
**The Status:** TRIUNE held. Agents synchronized. Vault recording.

---

## ECOSYSTEM STATE

### Repository

| Field | Value |
|---|---|
| Remote | github.com/LAF-US/IDAHO-VAULT (public) |
| Primary branch | `main` at `53a1ab1` |
| Open PRs | PR 108 (`claude/research-unified-swarm-rDmOg`), PR 104 (`claude/resolve-pr-conflicts`) |
| Pack size (GitHub) | ~362 MiB — Phase 2 rewrite pending (target ~30 MiB) |

### Recent Commits (main)

| SHA | Author | Message |
|---|---|---|
| `53a1ab1` | Claude | feat(governance): PRIVACY.md + ROYGBIV violet fix |
| `cd1ed3c` | Gemini | feat(fortification): Kinetic Release 2:40 PM MDT |
| `ec09efd` | Claude | feat(plugins): enable roygbiv-day-accent + 4 plugins, pure-core daily template |
| `22ba945` | Claude | feat(daily-notes): smart template + ROYGBIV weekday color sync |
| `455144d` | Claude | docs: DISCOVERY BEFORE INVENTION directive, device split docs, LEVELSET refresh |
| `3b4f97a` | — | STABILIZATION: Tiered plugin optimization (26 core) |
| `f935868` | — | feat(hydration): Bartimaeus Phase 2-3 — 2622 files hydrated |

### Infrastructure Inventory

| Asset | Type | Location | Status |
|---|---|---|---|
| `.claude/CLAUDE.md` | Instructions | `.claude/` | Operational; DISCOVERY BEFORE INVENTION added 2026-04-05 |
| `.gemini/GEMINI.md` | Instructions | `.gemini/` | Operational; DISCOVERY BEFORE INVENTION added 2026-04-05 |
| `.codex/CODEX.md` | Instructions | `.codex/` | Operational; DISCOVERY BEFORE INVENTION added 2026-04-05 |
| `.github/copilot-instructions.md` | Instructions | `.github/` | Operational; DISCOVERY BEFORE INVENTION added 2026-04-05 |
| `!/CONSTITUTION.md` | Governance | root | Canonical governance authority |
| `PRIVACY.md` | Governance | root | **NEW 2026-04-05** — Data classification, MCP bridge rules, Granola clause, sanitization protocol |
| `!/DECISIONS.md` | Governance | `!/` | Decision log |
| `!/AGENTS.md` | Governance | `!/` | Agent registry |
| `!/VAULT-CONVENTIONS.md` | Governance | `!/` | Shared conventions; Sync section rewritten 2026-04-05 |
| `!/PROTOCOL.md` | Governance | `!/` | Operational vocabulary |
| `!/GRIMOIRE/` | Knowledge | `!/GRIMOIRE/` | TTT, NETWEB-CrewAI alignment, Bartimaeus brief |
| `.crewai/` | Automation | `.crewai/` | CrewAI crews — JFAC, stubs for Custodian/Sentinel/Task-to-Code |
| `.github/scripts/chainfire.py` | Automation | `.github/scripts/` | CHAINFIRE burn script |
| `.github/workflows/check-portable-paths.yml` | CI | `.github/workflows/` | NETWEB path validator |
| `swarm.json` | Registry | repo root | Machine-readable ecosystem registry |

### Obsidian Plugin State

**Desktop:** 26 community plugins enabled, 54 total installed (26 enabled + 28 dormant).
**Mobile:** 0 community plugins (Restricted Mode — capture device; device split 2026-04-05).
**Sync:** Obsidian Sync (paid), remote vault "LAF-US". Content syncs both ways. Core plugin settings OFF (prevents circular dependency where Sync syncs its own selective-sync config). Community plugin lists are per-device.
**Plugin governance:** `!/PLUGIN-REGISTRY.md` — authoritative registry following CrewAI MANIFEST pattern (ESSENTIAL/ACTIVE/DORMANT layered model with promotion rules).

### Device Roles (established 2026-04-05)

| Device | Role | Plugins | Sync Direction |
|---|---|---|---|
| Windows Desktop | Workspace — full plugin stack, git, MCP, agents | 26 community (4 essential + 22 active) | Receives content from mobile; processes it |
| Pixel Phone | Capture — quick notes, tags, photos, audio | 0 community (Restricted Mode) | Creates content upstream; sends to desktop |

### Daily Note System (operational 2026-04-05)

| Component | Status |
|---|---|
| Template (`DAILY NOTE TEMPLATE.md`) | Pure core `{{date:}}` tokens — works on both desktop and mobile |
| ROYGBIV weekday accent (`roygbiv-day-accent` plugin) | Enabled — reads `weekday:` frontmatter, applies body class |
| CSS snippet (`roygbiv-smtwtfs.css`) | `!important` declarations — overrides Obsidian inline accent |
| `periodic-notes` plugin | Configured — format, template, folder matching core Daily Notes |
| Accent color (`appearance.json`) | Cleared — ROYGBIV snippet is sole accent source |
| Color mapping | Sun=violet, Mon=red, Tue=orange, Wed=yellow, Thu=green, Fri=blue, Sat=indigo |
| Verified | Violet holding on Sunday 2026-04-05 ✓ |

---

## PRIVACY GOVERNANCE (new 2026-04-05)

### Data Classification

| Class | Rule |
|---|---|
| **Ephemeral** (query-only) | Agents may read MCP services in session. Data never touches a `.md` file. |
| **Public-Persistent** (tracked) | No PII, no raw personal data, no secrets. Sanitized aggregates only. |
| **Local-Persistent** (gitignored) | `_private/`, `.remember/` — local working notes with personal context. |

### MCP Bridge Status

| Service | Ephemeral | Persistent | Notes |
|---|:---:|:---:|---|
| Gmail | ✅ | ❌ | Per-query approval for any file write |
| Google Calendar | ✅ | ❌ | Per-query approval for any file write |
| Google Drive | ✅ | ❌ | Per-query approval for any file write |
| Slack | ✅ | ❌ | Per-query approval for any file write |
| Granola | ⚠️ | ❌ | **Source protection** — journalist's shield; off-the-record by default |
| GitHub | ✅ | ✅ | Already public data |

### Connector Survey For Mid-Future Review (2026-04-09)

This is a survey and review surface for possible adoption lanes, not the live connector registry.

| Connector | Category | Availability | Write Mode | Candidate Use | Review Path | Notes |
|---|---|---|---|---|---|---|
| GitHub | `core` | active | `gated-write` | Execution and transport | Vault + Linear | Issues, PRs, workflows, automation output |
| Linear | `core` | active | `gated-write` | Execution state | Vault + GitHub | `linear_gateway.py`, `linear_pr_sync.py`, SWARM label |
| Slack | `core` | active | `notification-write` | Tertiary paging and breadcrumbs | Vault + GitHub + Linear | Not durable; notifications and quick coordination only |
| Gmail | `adjunct` | `available-read-only` | `read-only` | Inbox and message context | Vault + GitHub + Linear | Durable use requires explicit promotion and sanitization |
| Google Calendar | `adjunct` | `available-read-only` | `read-only` | Scheduling and availability context | Vault + GitHub + Linear | Scheduling writes are out of scope for the current hub |
| Google Drive | `adjunct` | `available-read-only` | `read-only` | Document and evidence retrieval | Vault + GitHub + Linear | Drive content is not the operational record |
| Box | `adjunct` | `available-read-only` | `read-only` | External content retrieval | Vault + GitHub + Linear | No repo-tracked automation seam yet |
| Cloudflare | `deferred` | `plugin-available-deferred` | `deferred` | Platform and deployment lane | Vault + GitHub + Linear | Requires a separate activation plan before live use |
| Hugging Face | `deferred` | `plugin-available-deferred` | `deferred` | Research and remote compute lane | Vault + GitHub + Linear | Requires a separate activation plan before live use |

### Sanitization Protocol (PRIVACY.md § V)

Four mandatory steps before any private-source data enters a tracked file:
1. Strip Identity — remove names of non-public figures
2. Strip Attribution — no direct quotes from private conversations
3. Strip Metadata — remove timestamps, locations, attendee details
4. Logan Reviews — human sign-off before anything lands

---

## THE ARTIFICER'S LIBRARY (discovered 2026-04-05)

Logan is exporting complete AI conversation histories as local-only xlsx workbooks:

| Book | Source | Sheets | Status |
|------|--------|--------|--------|
| **Book of Geminiaeus** | Google Takeout | 72 sheets (657 rows in Sheet1 + 71 conversation exports) | ✅ Bound |
| **Book of Claudius** | Anthropic exports | — | 📋 Unbound |
| **Book of Codices** | OpenAI exports | — | 📋 Unbound |

Sheet 72 reads: `THE BOOK IS INCOMPLETE !`

All xlsx files are gitignored (binary media block). The library is local-only — private archaeological record of how the vault was thought into existence.

Sheet 2 of Geminiaeus reveals 11 pinned Gemini personas ("Gems"): The Concierge, The Mirror, The Sentry, The TRIPTYCH, The Archivist, Caesar > The TRIUMVIRATE, The Clerk, The Twin (♂/♀), FARNSWORTH, The Synth.

---

## ACTIVE STREAMS

---

*LEVELSET-CURRENT.md — Originally synthesized 2026-03-13. Living document, updated each LEVELSET round. Permanent audit trail in numbered LEVELSET snapshots (v1, v2, v3...) stored in the repository. Reflects the **present state** of the ecosystem only.*
