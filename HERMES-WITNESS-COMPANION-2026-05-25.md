---
title: "HERMES WITNESS COMPANION — 2026-05-25"
subtitle: "Local Machine Survey: Bellhop (MacBook) Nous/Hermes Presence"
type: witness-report
companion-to: HERMES-WITNESS-REPORT-2026-05-25
source: local-machine-survey-claude-code-session-2026-05-25
tags:
- hermes-agent
- nous-research
- witness
- local-survey
- bellhop
- gateway
- ollama
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - HERMES-WITNESS-REPORT-2026-05-25
  - NOUS-RESEARCH-HERMES-AGENT-2026-04-28
  - HERMES-OLLAMA-OPENROUTER-SETUP-2026-04-28
  - RECOVERY-HERMES-CONFIG-2026-05-23
  - PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23
---

# HERMES WITNESS COMPANION — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Local machine witness — observed state of Bellhop (MacBook) only
**Companion to:** `HERMES-WITNESS-REPORT-2026-05-25.md` (research/theory)
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

This document records what I observed on Bellhop (Logan's MacBook) regarding Nous Research and Hermes Agent presence during a survey on 2026-05-25. I was instructed to look, not touch.

The companion report (`HERMES-WITNESS-REPORT-2026-05-25.md`) covers what Hermes Agent *is* — research grounded in external sources. This document covers what is *here* — grounded in direct local observation.

**Correction on record:** Logan directed the Hermes agent to wipe its MEMORY.md and USER.md files this morning (2026-05-25). The empty/absent state of those files is intentional, not a gap or error. Memory starts fresh from this point forward.

---

## RUNNING PROCESSES (observed at survey time)

Two Hermes processes were active at time of survey:

| PID | Process | Details |
|---|---|---|
| 62971 | `hermes_cli.main gateway run --replace` | Gateway daemon |
| 63078 | `node whatsapp-bridge/bridge.js` | Port 3000, self-chat mode |

Hermes is **not idle**. It is operating as a live multi-platform gateway daemon.

---

## LAUNCH AGENT — AUTO-START

```
~/Library/LaunchAgents/ai.hermes.gateway.plist
```

The gateway is registered as a macOS LaunchAgent. It starts automatically at login. This is a persistent infrastructure presence, not a manually-launched session.

---

## GATEWAY: LIVE PLATFORM STATE

| Platform | State | Notes |
|---|---|---|
| Telegram | 🟢 connected | |
| Discord | 🟢 connected | LAF-US guild |
| WhatsApp | 🟢 connected | self-chat bridge, port 3000 |
| Signal | 🔴 retrying | "failed to reconnect" — last attempt 2026-05-10 |

**Discord channels known to Hermes:**

| Channel | ID | Guild |
|---|---|---|
| `ledger` | 1495651518760882198 | LAF-US |
| `purgatory` | 1495660774708871289 | LAF-US |

The `ledger` channel is designated as the Discord home channel in `config.yaml`.

---

## INSTALLATION STATE

### Binaries

| Path | Version | Python | Status |
|---|---|---|---|
| `~/.hermes/hermes-agent/venv/bin/hermes` | v0.14.0 | 3.11 | **Active** |
| `~/Library/Python/3.13/bin/hermes` | v0.12.0 | 3.13 | Stale |
| `~/.local/bin/hermes` | unknown | — | Present |

Two `hermes` binaries exist on PATH from different Python environments. The active venv (3.11) runs v0.14.0. The Python 3.13 system path points to a stale v0.12.0 install.

`hermes-acp` (ACP server binary) present at both venv and Python 3.13 paths.

### uv Cache — Version History

Cached build artifacts for: **v0.11.0**, **v0.12.0**, **v0.14.0** — installation history preserved.

---

## CONFIGURATION SNAPSHOT

File: `~/.hermes/config.yaml` (version 23, last modified 2026-05-24)
Config backups present from: 2026-05-05 through 2026-05-19

| Parameter | Value |
|---|---|
| Default model | `mistralai/mistral-small-2603` via OpenRouter |
| Fallback 1 | `anthropic/claude-sonnet-4` via OpenRouter |
| Fallback 2 | `openai/gpt-4o-mini` via OpenRouter |
| Fallback 3 | `mistralai/mistral-small-2603` via OpenRouter |
| Fallback 4 | `open-mistral-7b` via mistral-direct |
| Fallback 5 | `devstral:latest` via local Ollama |
| Terminal CWD | `~/IDAHO-VAULT` |
| Active toolsets (config) | `hermes-cli` only |
| Platform toolsets | Full lists for telegram / cli / discord / whatsapp |
| Display personality | `kawaii` |
| TUI status indicator | `kaomoji` |
| TTS provider | Gemini (+ custom SAM TTS via Node.js) |
| STT | Enabled, local Whisper (base), voice key `ctrl+b` |
| Context engine | compressor |
| Compression threshold | 67%, target 20%, protect last 20 turns |
| Session retention | 90 days, reset at idle 960 min or 4am daily |
| Curator | Enabled, interval 168 hours (weekly) |
| Kanban dispatch | Every 60 seconds in gateway |
| Approvals mode | Manual, 60-second timeout |
| Signal | `enabled: false` in platforms config |
| OpenRouter response cache | 5 minute TTL |
| Prompt caching TTL | 5 minutes |

**OpenRouter API key:** In `~/.hermes/.env` (not in config.yaml — correct pattern)

`.env` backup history:
- `.env.bak-20260518-BEEFSTACK`
- `.env.bak-20260519-hermes-direct-mistral`

---

## SOUL.md STATE

**File:** `~/.hermes/SOUL.md`
**Content:** Empty — contains only the template placeholder comment block
**Effect:** Hermes is running on its built-in default identity for every session and every platform

The SOUL.md was seeded automatically at install (2026-05-05, per timestamp) but never written with content.

---

## MEMORY STATE

| File | State | Notes |
|---|---|---|
| `MEMORY.md` | Empty | Wiped this morning by Logan's direction |
| `USER.md` | Absent | Wiped this morning by Logan's direction |
| `MEMORY.md.lock` | Present | Lock file only |
| `USER.md.lock` | Present | Lock file only |

**44 sessions** exist in `~/.hermes/sessions/` predating the wipe. Most recent sessions: 2026-05-23 through 2026-05-25 (today).

Memory starts fresh as of this morning.

---

## SKILLS INSTALLED

26 categories present in `~/.hermes/skills/`:

| Category | Notable sub-skills |
|---|---|
| `autonomous-ai-agents` | hermes-agent (self-reference) |
| `note-taking` | **obsidian** |
| `github` | codebase-inspection, github-auth, code-review, issues, pr-workflow, repo-management |
| `productivity` | google-workspace, notion, linear, airtable, ocr-and-documents, powerpoint, teams-meeting-pipeline |
| `messaging` | signal-cli (includes hermes-gateway-local-linking-flow reference) |
| `software-development` | hermes-agent-skill-authoring, debugging-hermes-tui-commands, hermes-s6-container-supervision |
| `mcp` | MCP server integration |
| `devops` | — |
| `data-science` | — |
| `research` | — |
| `smart-home` | — |
| + 15 others | creative, gaming, gifs, inference-sh, media, mlops, red-teaming, social-media, yuanbao, domain, email, apple, diagramming, dogfood |

Note: Skills are installed but not all toolsets are active. The `toolsets:` field in config.yaml lists only `hermes-cli`. Platform-specific toolset lists are configured separately.

---

## LOCAL OLLAMA MODELS

| Model | Size | Last modified |
|---|---|---|
| devstral:latest | 14 GB | ~2 weeks ago |
| codestral:latest | 12 GB | ~3 weeks ago |
| mistral-large:latest | 73 GB | ~3 weeks ago |
| qwen3.5:latest | 6.6 GB | ~3 weeks ago |
| phi3:mini | 2.2 GB | ~2 weeks ago |
| qwen2.5:3b | 1.9 GB | ~3 weeks ago |

Total local model footprint: ~110 GB. `devstral:latest` is the designated Ollama fallback in config.

---

## KANBAN

`~/.hermes/kanban.db` — 106KB SQLite database, actively written. Kanban dispatch runs every 60 seconds in gateway mode. A kanban spec PDF exists: `~/.hermes/hermes-agent/docs/hermes-kanban-v1-spec.pdf`.

---

## OPENCLAW RESIDUE

OpenClaw was previously installed on Bellhop. Remaining presence:

- `~/.openclaw/workspace/SOUL.md` — OpenClaw workspace with its own SOUL.md
- Hermes ships a migration script: `optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py`
- `onboarding.seen.openclaw_residue_cleanup: true` — cleanup was acknowledged in Hermes config

---

## CUSTOM COMPONENTS

- **SAM TTS**: Custom Node.js text-to-speech at `~/.hermes/bin/hermes-sam-tts.js`
- **Signal QR codes**: Four QR image files in `~/.hermes/` (signal-link-qr*.png), dated 2026-05-09 — Signal linking was attempted
- **`interrupt_debug.log`**: Present, indicating prior interrupt events
- **Docker SOUL.md**: `~/.hermes/hermes-agent/docker/SOUL.md` — a separate SOUL for containerized deployments

---

## SUMMARY OBSERVATIONS

1. **Hermes is a live daemon on this machine**, not a tool that runs on demand. Three platforms connected simultaneously as of survey time.
2. **Signal is the broken platform** — was attempted May 9 (QR codes), failed to reconnect by May 10, still retrying.
3. **SOUL.md has never been written.** Every session across every platform — Telegram, Discord, WhatsApp, CLI — runs on Hermes's built-in default identity.
4. **Memory starts clean** as of this morning, by Logan's direction.
5. **Two hermes binaries on PATH** from different Python environments. The stale Python 3.13 install predates the venv-based v0.14.0.
6. **110 GB of local Ollama models** provide a substantial offline fallback.
7. **The obsidian skill is installed** under note-taking — but ACP and note-taking toolsets are not active in the current config.
8. **OpenClaw migration is complete** — residue acknowledged, Hermes is the active agent framework.

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a local survey artifact.*
*Companion to: `HERMES-WITNESS-REPORT-2026-05-25.md`*
