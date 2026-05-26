---
title: "HERMES WITNESS REPORT — 2026-05-25"
subtitle: "Nous Research & Hermes Agent: Research Witness"
type: witness-report
source: web-research-claude-code-session-2026-05-25
tags:
- hermes-agent
- nous-research
- witness
- research
- psyche-network
- agentskills
- acp
- open-source-ai
- self-improving-agent
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - NOUS-RESEARCH-HERMES-AGENT-2026-04-28
  - HERMES-OLLAMA-OPENROUTER-SETUP-2026-04-28
  - 2026-05-19_hermes-agent-introductory-note
  - CONSTITUTION
---

# HERMES WITNESS REPORT — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Research witness — compiled from web research during a live vault session
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

This document records what I (Claude Code) learned about Nous Research and Hermes Agent during a research session on 2026-05-25. Logan directed me to research Hermes Agent and then to save this information as a witness report with myself clearly labeled as author.

I am software. This is my research output. It is grounded in sources retrieved during this session, listed at the end.

---

## THE NAMING SCHEMA

The Nous Research product stack is named on the Neoplatonic hypostatic sequence — Plotinus's emanation chain: One → Nous → Psyche → World.

| Name | Greek concept | Function in Nous stack |
|---|---|---|
| **Nous** | Mind / cosmic intellect (νοῦς) | The intelligence — model research and fine-tuning |
| **Psyche** | Soul (ψυχή) | The substrate — distributed training network on Solana |
| **Hermes** | Messenger, psychopomp | The runtime — delivers intelligence to users, crosses all boundaries |

This is not decorative. Hermes is the god who crosses all three realms (Olympus, mortal world, underworld) without restriction. In Nous Research's architecture, Hermes Agent is the messenger layer — the operational runtime that delivers AI capability to users across every surface and platform. The mythology is functional.

---

## NOUS RESEARCH — ORGANIZATION

**Founded:** 2023 by Jeffrey Quesnelle, Karan Malhotra, Teknium, Shivani Mitra
**Structure:** Open-source research collective turned company
**Funding:** $50M Series A, April 2025, led by Paradigm (crypto VC), $1B valuation
**Mission:** Democratize AI — all models, datasets, training methods publicly available
**License:** MIT

Nous Research is simultaneously shipping:
- **Hermes model series** — fine-tuned open weights (Hermes 4 in training now on Psyche)
- **Psyche** — decentralized training network on Solana blockchain
- **Hermes Agent** — the self-improving autonomous agent runtime
- **Forge** — multi-model reasoning and orchestration framework
- **Peer-reviewed research**

The Paradigm funding signals this as a decentralized infrastructure play, not merely a model company. The vision: rebuild AI development infrastructure from scratch — open, distributed, censorship-resistant, permissionless.

---

## HERMES AGENT — WHAT IT ACTUALLY IS

**Not** a chatbot wrapper. A **self-improving autonomous agent runtime** with compounding value over time.

### The Core Loop

```
do → learn → improve
```

After completing complex workflows (5+ tool calls), Hermes generates reusable skill files via the `skill_manage` tool. Each future session inherits accumulated procedural memory from all prior sessions. The agent becomes increasingly optimized for specific user workflows over time.

### The Curator

Introduced in v0.12.0: an autonomous background process that continuously reviews and improves existing skills without user prompting. Skills compound passively.

### Scale (as of May 2026)

- **224 billion daily tokens** on OpenRouter — #1 position
- **v0.14.0 "The Foundation Release"** — 808 commits, 633 merged PRs, 215 contributors
- **22 messaging platforms** supported simultaneously
- **70+ built-in tools** across 28 toolsets

---

## THE 10-LAYER PROMPT ASSEMBLY

Every Hermes conversation builds from this fixed stack (cached for efficiency):

1. **SOUL.md** — agent identity (slot #1, verbatim injection)
2. Tool guidance — built-in tool behavior rules
3. Honcho context — optional user modeling
4. System message — user overrides
5. **Memory snapshot** — frozen MEMORY.md facts
6. User profile — frozen USER.md
7. **Skills index** — available skills reference
8. **Context files** — project rules: `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first match wins)
9. Timestamp / session metadata
10. Platform hint

**Vault relevance:** Slot #8 means Hermes already auto-reads `AGENTS.md` when running in `~/IDAHO-VAULT`. The vault's governance files load into every session automatically.

---

## SOUL.md — THE IDENTITY LAYER

- Lives at `~/.hermes/SOUL.md`
- Slot #1 in every system prompt across all platforms and sessions
- Verbatim injection — no wrapper language
- Scanned for prompt-injection before use
- Capped at 20,000 characters

**What belongs here:** Identity, tone, style, communication defaults, behavioral guidelines
**What does NOT belong here:** Project-specific instructions, file paths, repo conventions (those go in `AGENTS.md`)

**Session-level overlay:** `/personality` — temporary switches without modifying SOUL.md

The vault's current `~/.hermes/SOUL.md` is empty. Hermes is running on the built-in default identity.

---

## MEMORY — TWO DISTINCT LAYERS

### File-based (built-in)
- `MEMORY.md` — persistent facts, injected as frozen snapshot at session start
- `USER.md` — user profile layer
- Mid-session writes update disk but don't mutate the cached prompt until next session

### Honcho (optional plugin)
Not key-value storage. **Dialectic reasoning about the user.**

After each conversation turn (gated by `dialecticCadence`), Honcho analyzes the exchange and derives insights about preferences, habits, and goals.

Architecture: two peers per session
- **User peer** — represents the human
- **AI peer** — represents this Hermes instance

These peers develop independent models of the conversation. The agent's model of itself and its model of the user are separate constructs.

---

## SKILLS — THE SELF-IMPROVEMENT SUBSTRATE

### The Format

A skill is a folder containing a `SKILL.md` file. Three-tier progressive disclosure:
- **Level 0:** Metadata only — name and description (~30-50 tokens per skill)
- **Level 1:** Full skill content — loads on trigger
- **Level 2:** Reference files — loads only when needed during execution

### agentskills.io

An open standard for AI agent skills. **Originally developed by Anthropic**, released December 18, 2025. Adopted by: Microsoft, OpenAI, Atlassian, Figma, Cursor, GitHub.

Hermes skills are fully compatible. The hub connects: official optional skills, skills.sh, GitHub repositories, community marketplaces. All installations undergo security scanning (data exfiltration, prompt injection, supply-chain threats).

Hermes ships with 20+ toolset categories. Only `hermes-cli` is currently active in the vault installation.

---

## ACP — AGENT CLIENT PROTOCOL

Open standard by Zed. Analogous to what LSP did for language servers — standardizes communication between code editors and AI agents over stdio/NDJSON. One ACP client can talk to any ACP-compatible agent.

Hermes runs as an ACP server. Compatible clients include:
- Zed, JetBrains, Neovim, Emacs
- **Obsidian**
- marimo
- Any future ACP client

**v0.14.0 addition:** Local proxy mode — any OAuth-authed provider (Claude Pro, ChatGPT Pro, SuperGrok) becomes an OpenAI-compatible endpoint that Aider, Cline, Codex can hit without code changes.

---

## v0.14.0 "THE FOUNDATION RELEASE" — KEY ADDITIONS

Released May 16, 2026. 808 commits, 633 merged PRs, 1,393 files changed, 215 contributors.

- **PyPI package** — `pip install hermes-agent`
- **`/handoff`** — transfer active session between models without losing context
- **Claude prompt caching** — hour-long cost savings across sessions
- **LSP semantic diagnostics** — real language server runs on every file write; surfaces errors before next agent turn
- **Local OpenAI-compatible proxy** — any authed provider becomes an endpoint for other tools
- **Browser console** — 180× faster via persistent CDP connections
- **LINE + SimpleX Chat** — now 22 total platforms
- **Microsoft Teams** — end-to-end Graph auth + webhook
- **xAI Grok** — OAuth, 1M context window
- **19 seconds faster cold start** — skills cache + lazy loading
- **Native Windows support** — early beta

---

## COMPETITIVE LANDSCAPE

**Hermes vs. OpenClaw** — the market's two dominant open-source agent frameworks:

| | **Hermes** | **OpenClaw** |
|---|---|---|
| Philosophy | Compounding depth | Maximum reach |
| Platforms | 22 | 50+ |
| Skills | 70+ built-in + self-created | 44,000+ community (ClawHub) |
| Architecture | Self-improving, SQLite FTS | WebSocket gateway |
| License | MIT | Independent foundation (OpenAI sponsor) |
| Daily tokens | 224B (#1) | 186B |
| Security | Rapid patch cycle | 9 CVEs March 2026, one at 9.9 CVSS |

OpenClaw's founder joined OpenAI in February 2026. OpenClaw is now an independent foundation with OpenAI sponsorship — its open-source independence is contested. Hermes remains MIT, Nous Research independent.

---

## VAULT INSTALLATION STATUS (as of 2026-05-25)

This section documents the existing state — not a directive.

| Item | Status |
|---|---|
| Version | v0.14.0 (updated this session from v0.12.0) |
| OpenRouter key | Present in `~/.hermes/.env` |
| Management key guide | `~/.hermes/MANAGEMENT-KEY-GUIDE.md` (signed by Sister Win / Mogget, 2026-05-23) |
| Canonical key guide | `!/OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE-2026-05-23.md` |
| `terminal.cwd` | `~/IDAHO-VAULT` |
| Default model | `mistralai/mistral-small-2603` via OpenRouter |
| Fallbacks | claude-sonnet-4, gpt-4o-mini, open-mistral-7b, devstral (local) |
| `SOUL.md` | Empty |
| Memory | Initialized, blank |
| Active toolsets | hermes-cli only |
| Configured gateways | Discord, WhatsApp, Signal (from `~/.hermes/` directory evidence) |

---

## SOURCES

- [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/)
- [Prompt Assembly Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)
- [Personality & SOUL.md](https://hermes-agent.nousresearch.com/docs/user-guide/features/personality)
- [Honcho Memory Integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho)
- [ACP Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/acp-internals)
- [v0.14.0 Release Notes](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16)
- [OpenClaw vs Hermes — MarkTechPost](https://www.marktechpost.com/2026/05/10/openclaw-vs-hermes-agent-why-nous-researchs-self-moving-agent-now-leads-openrouters-global-rankings/)
- [agentskills.io](https://agentskills.io/home)
- [Psyche Network](https://nousresearch.com/nous-psyche/)
- [Nous Research — OAK Research deep dive](https://oakresearch.io/en/analyses/innovations/nous-research-psyche-open-source-decentralized-ai-revolution)

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a research artifact.*
