---
name: IDAHO-VAULT — project state and architecture
description: What the vault is, how it's structured, multi-agent ecosystem, durable architecture facts
type: project
---

**IDAHO-VAULT** is Logan Finney's Obsidian.md knowledge vault, version-controlled with git at github.com/loganfinney27/IDAHO-VAULT (public repo). All committed content is on the record and publishable.

**What:** Journalism infrastructure — story development, source notes, legislative tracking, automation pipelines, and multi-agent AI coordination layer.

**Why:** Logan's Project = unachievable ambitious end goal; all vault work is incremental progress toward it.

## Multi-Agent Ecosystem — Dotfolder Architecture

Each agent has its own dotfolder. `!/` is the shared commons all agents draw from (hub-and-spoke).

Key agents (auto-loaded):
- **Claude Code** (`.claude/`) — Direct Write tier, "The Abhorsen"
- **Gemini CLI** (`.gemini/`) — Tier 1 Support, Linear SWARM operator
- **GitHub Copilot** (`.github/`) — Advisory tier, owns PR creation/management
- **OpenAI Codex CLI** (`.codex/`) — Advisory tier
- **Serena** (`.serena/`) — MCP server, semantic code intelligence (added 2026-04-04)

Additional agents: Grok, DeepSeek, Perplexity, Microsoft AI, Google, Meta, Slack AI (all manual injection, Advisory). Fictive personas: Bartimaeus, Zagreus, Persephone.

Root vault notes (`CLAUDE.md`, `GEMINI.md`, etc.) are Obsidian entity notes about the agents — wikilinks preserved. Operational instructions live in dotfolders.

**Cross-tool auto-load:** `AGENTS.md` (root pointer, auto-loaded by Codex/Copilot/Qodo).
**Machine-readable registry:** `swarm.json` at root.
**Linear Agent** (launched 2026-03-24): cloud-only AI in Linear workspace, no dotfolder.

## Naming Standards

- `ALL-CAPS.md` — infrastructure/governance
- `Title Case.md` — content vault notes (people, places, organizations)
- `YYYY-MM-DD - Outlet - Title.md` — dated sourced content
- `(YYYY) Type Number.md` — bills
- `lowercase.ext` — machine/config files
- `_PREFIX.md` — aliased stubs (NETWEB convention, see project_netweb.md)

## Active Automation

- `idaho_leg_scraper.py` — daily 6 AM MT, legislature bill data
- `sort_audit.py` — weekly Monday 6 AM UTC vault audit
- Wayback preservation — weekly Monday 8 AM UTC
- `auto-pr.yml` — auto-creates PRs from agent branches
- `check-portable-paths.yml` — NETWEB path portability guard (added 2026-04-04)

## Active Standards

- **NETWEB** — cross-platform path portability (see `project_netweb.md`)
- **DING** — informal beta relay protocol (see `project_ding.md`)
- **PRIVACY.md** — 8 sections as of 2026-04-06: Core Principle, Data Classification, Protected Zones, MCP Bridge Rules, Sanitization Protocol, **IP Boundary/Disentanglement (§ VI, added 2026-04-06)**, Agent Obligations, Amendment
- **TRIPLEX** — concurrent multi-agent lane map (adopted 2026-04-05); GRIMOIRE lane ownership under review (Logan flagged 2026-04-06)

## Infrastructure

- **GCP "Nest Bridge"** — vault sync service in progress (see `project_gcp_sync.md`)
- **1Password** — centralized credential management, CI integration via `OP_SERVICE_ACCOUNT_TOKEN`
- **Linear** — SWARM label for task coordination (Phase 1 pilot launched 2026-03-28)
