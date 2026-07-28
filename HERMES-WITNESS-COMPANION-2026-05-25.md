---
title: "HERMES WITNESS COMPANION — 2026-05-25"
subtitle: "Local Machine Survey: Logan's MacBook — Nous/Hermes Presence"
type: witness-report
companion-to: HERMES-WITNESS-REPORT-2026-05-25
source: local-machine-survey-claude-code-session-2026-05-25
tags:
- hermes-agent
- nous-research
- witness
- local-survey
- macbook
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
  - SYZYGY-HERMES-OPENCLAW-2026-05-25
---

# HERMES WITNESS COMPANION — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Local machine witness — observed state of the MacBook only
**Companion to:** `HERMES-WITNESS-REPORT-2026-05-25.md` (research/theory)
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

This document records what I observed on the MacBook regarding Nous Research and Hermes Agent presence during a survey on 2026-05-25. I was instructed to look, not touch.

The companion report (`HERMES-WITNESS-REPORT-2026-05-25.md`) covers what Hermes Agent *is* — research grounded in external sources. This document covers what is *here* — grounded in direct local observation.

**Correction on record:** Logan directed the Hermes agent to wipe its MEMORY.md and USER.md files this morning (2026-05-25). The empty/absent state of those files is intentional, not a gap or error. Memory starts fresh from this point forward.

---

## RUNNING PROCESSES (observed at survey time)

Two Hermes processes were active at time of survey:

| PID | Process | Details |
| --- | --- | --- |
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
| --- | --- | --- |
| Telegram | 🟢 connected | |
| Discord | 🟢 connected | LAF-US guild |
| WhatsApp | 🟢 connected | self-chat bridge, port 3000 |
| Signal | 🔴 retrying | "failed to reconnect" — last attempt 2026-05-10 |

**Discord channels known to Hermes:**

| Channel | ID | Guild |
| --- | --- | --- |
| `ledger` | 1495651518760882198 | LAF-US |
| `purgatory` | 1495660774708871289 | LAF-US |

The `ledger` channel is designated as the Discord home channel in `config.yaml`.

---

## INSTALLATION STATE

### Binaries

| Path | Version | Python | Status |
| --- | --- | --- | --- |
| `~/.hermes/hermes-agent/venv/bin/hermes` | v0.14.0 | 3.11 | **Active** |
| `~/Library/Python/3.13/bin/hermes` | v0.12.0 | 3.13 | Stale at survey time — updated to v0.14.0 during this session |
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
| --- | --- |
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

## MCP & ACP STATE (amended 2026-05-25)

A full MCP/ACP surface audit was conducted during this session, reading the local documentation at `~/.hermes/hermes-agent/website/docs/`.

### MCP client — Hermes connecting to external servers

**Status: installed, no servers configured.**

- MCP Python package: installed and importable in active venv
- `hermes mcp` CLI available: `add / remove / list / test / configure / login / serve`
- No `mcp_servers:` entries in `~/.hermes/config.yaml`
- Built-in `codex` preset available; `codex` CLI is at `/usr/local/bin/codex` v0.130.0
- `opencode` CLI present at `/Users/logan/.opencode/bin/opencode` v1.14.50 — no preset, manual config needed
- OAuth 2.1 authenticated HTTP MCP servers supported natively (`auth: oauth`)

### MCP server — Hermes exposing tools to other agents

**Status: available but not wired.**

`hermes mcp serve` is a documented command. It runs Hermes as a stdio MCP server exposing 10 messaging tools (list/read/send/poll conversations across Telegram, Discord, WhatsApp). Gateway must be running for send operations; it is currently running.

Integration with Claude Code requires a `.mcp.json` in the vault root or an `mcpServers` entry in `~/.claude/claude_desktop_config.json`. Neither exists.

### ACP server — Hermes as editor agent

**Status: server-side ready, no editor configured.**

- `hermes-acp --check OK`
- ACP registry manifest: `~/.hermes/hermes-agent/acp_registry/agent.json` (v0.14.0)
- Compatible editors: VS Code (ACP Client extension), Zed (v0.221.x+ ACP Registry, requires `uv`), JetBrains
- ACP mode uses `hermes-acp` toolset; sessions bind to editor cwd; approvals surface inline
- No editor has been configured to connect to `hermes-acp`

### .env amendment

`OBSIDIAN_VAULT_PATH=/Users/logan/IDAHO-VAULT` added to `~/.hermes/.env`. The Obsidian skill was previously falling back to `~/Documents/Obsidian Vault` because this variable was unset.

---

## MEMORY STATE

| File | State | Notes |
| --- | --- | --- |
| `MEMORY.md` | Empty | Wiped this morning by Logan's direction |
| `USER.md` | Absent | Wiped this morning by Logan's direction |
| `MEMORY.md.lock` | Absent | Lock file does not exist |
| `USER.md.lock` | Absent | Lock file does not exist |

**44 sessions** exist in `~/.hermes/sessions/` predating the wipe. Most recent sessions: 2026-05-23 through 2026-05-25 (today).

Memory starts fresh as of this morning.

---

## SKILLS INSTALLED

21 categories containing skills in `~/.hermes/skills/`, totaling 95 SKILL.md files. (Four additional empty category directories — `domain`, `inference-sh`, `diagramming`, `gifs` — contain no SKILL.md files and are excluded from the table below.)

| Category | Notable sub-skills |
| --- | --- |
| `autonomous-ai-agents` | claude-code, codex, hermes-agent, kanban-codex-lane, opencode |
| `note-taking` | **obsidian** |
| `github` | codebase-inspection, github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management |
| `productivity` | google-workspace, notion, linear, airtable, ocr-and-documents, powerpoint, teams-meeting-pipeline, maps, nano-pdf |
| `messaging` | signal-cli |
| `software-development` | hermes-agent-skill-authoring, debugging-hermes-tui-commands, hermes-s6-container-supervision, plan, spike, subagent-driven-development, systematic-debugging, test-driven-development, writing-plans, node-inspect-debugger, python-debugpy, requesting-code-review |
| `mcp` | native-mcp |
| `devops` | kanban-orchestrator, kanban-worker, webhook-subscriptions |
| `data-science` | jupyter-live-kernel |
| `research` | arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing |
| `smart-home` | openhue |
| `creative` | 16 sub-skills including touchdesigner-mcp, excalidraw, manim-video, p5js, comfyui, sketch |
| `mlops` | 13 sub-skills across evaluation, inference, training, models, research subdirectories |
| `media` | gif-search, heartmula, songsee, spotify, youtube-content |
| `apple` | apple-notes, apple-reminders, findmy, imessage, macos-computer-use |
| `gaming` | minecraft-modpack-server, pokemon-player |
| `red-teaming` | godmode |
| `social-media` | xurl |
| `email` | himalaya |
| `dogfood` | dogfood |
| `yuanbao` | yuanbao |

**Amendment (same session, 2026-05-25):** Three bespoke skills wiped at Logan's direction — `logan-environment-discovery` (with 4 reference files), `terminal-output-format`, `terminal-output-formatting`. These were Logan-specific custom skills written under prior configuration assumptions. Clearing them is the correct foundation for writing fresh skills on correct foundations.

Note: Skills are installed but not all toolsets are active. The `toolsets:` field in config.yaml lists only `hermes-cli`. Platform-specific toolset lists are configured separately.

---

## LOCAL OLLAMA MODELS

| Model | Size | Last modified |
| --- | --- | --- |
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

## OPENCLAW ON THE MACBOOK

OpenClaw is a **live, separate installation** on the MacBook — not residue. Both Hermes and OpenClaw are active simultaneously. What is visible from the Hermes side:

- `~/.openclaw/workspace/SOUL.md` — OpenClaw's own workspace SOUL.md (has content; generic default template)
- Hermes ships a migration script: `optional-skills/migration/openclaw-migration/scripts/openclaw_to_hermes.py` — not run; no migration was performed or requested
- `onboarding.seen.openclaw_residue_cleanup: true` — this is Hermes's own onboarding wizard bookkeeping; it does not record any Logan action or migration

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
8. **OpenClaw is a live, separate installation** — both Hermes and OpenClaw are active simultaneously on the MacBook. No migration was performed. The `onboarding.seen.openclaw_residue_cleanup: true` field in Hermes config is Hermes's own onboarding bookkeeping, not a Logan action.

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a local survey artifact.*
*Companion to: `HERMES-WITNESS-REPORT-2026-05-25.md`*
