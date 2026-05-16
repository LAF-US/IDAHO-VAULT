---
title: "IMPL-MESH-OPENROUTER-2026-04-24"
status: active
authority: LOGAN
date created: Friday, April 24th 2026, 2:06:15 pm
date modified: Friday, April 24th 2026, 5:33:35 pm
type: implementation-report
related:
  - OpenRouter
  - OpenClaw
  - Discord
  - SPARKSEED
  - 1Password
  - Mesh
---

# OpenRouter Mesh Implementation Report

## Executive Summary

Consolidated AI model routing through OpenRouter for flexible model selection across agentic tools. Single API key in 1Password, unified gateway, coordinated channels.

2026-05-14 note: the April model list below is historical. The current Mac runtime is documented in **Current Live Override** and uses `openrouter/mistralai/mistral-small-2603` as the OpenClaw default. Preferred hosted family order is Mistral, Claude, then ChatGPT/OpenAI. Gemini is banned from active routing; Phi, Qwen, and Gemma are disfavored and excluded from active routing. Local Ollama remains installed but has no active OpenClaw route because allowed local Mistral-family models did not return promptly on this Mac.

## Completed

### 1. OpenRouter Environment Fix

| File | Change |
|------|--------|
| `.op/openrouter.env` | Fixed 1Password path to `op://Vault/OpenRouter API Key/credential` |
| `!resolve_openrouter_secret.py` | Updated vault to `Vault`, prioritized `OpenRouter API Key` item |
| `.op/openrouter.env.template` | Template updated with correct reference |
| `.op/openrouter.env` | Anthropic compatibility keys now ride the same OpenRouter contract |

### 2. OpenClaw → OpenRouter Migration

**Config:** `C:\Users\loganf\.openclaw\openclaw.json`

| Change | Before | After |
|--------|--------|-------|
| Provider | `mistral` (paid), `ollama` (cloud, paid) | `openrouter` (free tier) |
| Primary Model | `ollama/kimi-k2.5:cloud` | Historical cloud experiment, no longer active |
| Available Models | Paid Mistral, cloud Ollama | Historical free-tier experiment, no longer active |

**Historical models added to OpenClaw in April, now superseded:**
- Google experimental route: removed from active routing; Gemini is banned.
- `openai/gpt-4o-mini` (286K context)
- `anthropic/claude-3.5-haiku` (131K context)

### 3. Discord Channel Configured

| Item | 1Password | Field |
|------|-----------|-------|
| Discord OpenClaw Bot | ✅ | credential |

Config: `token: env:DISCORD_OPENCLAW_TOKEN` (resolved by SPARKSEED)

### 4. Signal Channel Setup

| Item | 1Password | Field | Status |
|------|-----------|-------|--------|
| Signal | ✅ Created | number: +1-208-627-9028 | ⏳ Needs CLI token |

### 5. SPARKSEED Bootstrap Fix

**File:** `src/idaho_vault/sparkseed.py`

| Fix | Description |
|-----|-------------|
| Vault scoping | All 1Password queries now scoped to `--vault Vault` |
| Field alignment | Fixed field names to match actual 1Password structure |
| Graceful failure | Missing secrets no longer hard-fail; missing items skipped |
| OpenRouter first | OpenRouter API key now primary secret |
| PATH resolution | Fixed `openclaw` path resolution for subprocess calls |
| Gateway command | Changed `gateway start` → `gateway run` |

### 6. Launch Scripts

| Script | Purpose |
|--------|---------|
| `!launch-claude-openrouter.cmd` | Claude Code via OpenRouter |
| `!launch-codex-openrouter.cmd` | Codex via OpenRouter |

### 7. Startup Cleanup

- Removed `C:\Users\loganf\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw Gateway.cmd`
- Terminal flash issue resolved

### 8. Documentation

| Document | Purpose |
|----------|---------|
| `OPENROUTER-MESH-2026-04-24.md` | Live mesh topology and status |
| `!/INTEGRATIONS/COMPATIBILITY.md` | Canonical runtime/provider compatibility snapshot |
| `!/MONITORING/health-log.md` | Canonical health snapshot log |

---

## In Progress

### Channel Configuration

All channels enabled in OpenClaw config but require tokens:

| Channel | Status | Missing |
|---------|--------|---------|
| Discord | ⚠️ Enabled | Token verification |
| WhatsApp | ✅ Enabled | Working |
| Signal | ⏳ Enabled | CLI token |
| Telegram | ⏳ Enabled | Bot token |
| Nostr | ⏳ Enabled | nsec from Orpheus (ready in 1Password) |

### Gateway Persistence

- Gateway runs via `openclaw gateway run` (foreground)
- Not yet installed as Windows service
- Dies when terminal closes

---

## Pending

### Critical (Blocking Full Mesh)

1. ~~Signal CLI Token~~ ✅ Resolved - linked via QR code
2. ~~Telegram Bot Token~~ ✅ Resolved - created @LAF_US_bot

3. ~~**OpenClaw Gateway Service**~~
   - Install: `openclaw node install`
   - Allows gateway to run persistently~~ ✅

4. ~~**Claude Code OpenRouter Wiring**~~
   - VSCode settings updated for Claude Code extension
   - Need to test `.\!launch-claude-openrouter.cmd`~~ ✅ Tested

5. ~~**VSCode Continue Extension**~~
   - Install from VSCode marketplace
   - Configure OpenRouter provider~~ ⏳ Deferred

6. ~~**Cursor OpenRouter Setup**~~
   - Settings → Models → Add OpenRouter
   - Paste API key~~ ⏳ Deferred

### Channels Added

| Channel | Status | Notes |
|---------|--------|-------|
| Discord | ✅ Configured | Bot token set |
| WhatsApp | ✅ Configured | Working |
| Telegram | ✅ Configured | @LAF_US_bot |
| Signal | ✅ Configured | Linked via QR |
| Twitch | ⏳ Pending | User fetching from dev.twitch.tv |
| Google Chat | ✅ Configured | Service account JSON saved to secrets/ |
| Nostr | ⏳ Pending | Keys ready in 1Password |

---

## Architecture Summary

```
                    ┌─────────────────────────────────────┐
                    │         OpenRouter.ai                 │
                    │    openrouter.ai/api/v1 = unified    │
                    │       (cloud model routing)         │
                    └─────────────────────────────────────┘
                       ▲     ▲     ▲     ▲     ▲
                       │     │     │     │     │
              ┌────────┴┐ ┌───┴──┐ ┌────┴──┐ ┌───┴──┐ ┌────┴───┐
              │ Ollama  │ │Cursor│ │OpenClaw│ │Claude│ │ Codex  │
              │(local) │ │(UI)  │ │(models)│ │(env) │ │ (env)  │
              └─────────┘ └──────┘ └───────┘ └──────┘ └────────┘

1Password (Vault)
├── OpenRouter API Key ✅
├── OpenClaw Gateway Token ✅
├── Discord OpenClaw Bot ✅
├── Signal ✅ (number set)
├── Nostr (Orpheus) ✅
└── Other services...
```

---

## 1Password Items (Vault)

| Item | Fields | Status |
|------|--------|--------|
| OpenRouter API Key | credential | ✅ |
| OpenClaw Gateway Token | credential | ✅ Created today |
| Discord OpenClaw Bot | credential | ✅ |
| Signal | number | ✅ Created today |
| Nostr (Orpheus) | password, username | ✅ |
| Linear API Key | credential | ✅ |
| Mistral | credential | ✅ |
| GitHub | private_key | ⚠️ Multiple items |
| Claude | password | ⚠️ OAuth only, no API key |
| Qodo API Key | credential | ✅ |
| Telegram Bot | credential | ⏳ Needs token |

---

## OpenClaw Skills Status

**Total:** 52 skills | **Ready:** 14 | **Needs Setup:** 38

### Ready Skills (14)

| Skill | Description |
|-------|-------------|
| 1password | 1Password CLI integration |
| coding-agent | Codex, Claude Code, or Pi agents |
| discord | Discord operations via message tool |
| gemini | Historical only; Gemini is banned from active OpenClaw routing |
| gh-issues | GitHub issues and PRs |
| github | GitHub CLI operations |
| healthcheck | Security hardening checks |
| node-connect | Device pairing diagnostics |
| obsidian | Obsidian vault operations |
| session-logs | Session log search |
| skill-creator | Create/improve AgentSkills |
| taskflow | Durable task flows |
| taskflow-inbox-triage | Inbox triage patterns |
| weather | Weather via wttr.in |

---

## Current Live Override

The original implementation report captured the April 24 migration state. The
active workstation now uses:

- `gateway.bind = loopback`
- `agents.defaults.model.primary = openrouter/mistralai/mistral-small-2603`
- Preferred hosted family order: Mistral -> Claude -> ChatGPT/OpenAI
- Fallbacks: `openrouter/mistralai/mistral-medium-3-5`, `openrouter/anthropic/claude-sonnet-4.6`, `openrouter/openai/gpt-5.3-codex`, `openrouter/mistralai/mistral-large-2512`
- Specialist aliases: `mistral-coder` -> `openrouter/mistralai/devstral-2512`
- Magistral was tested and removed because OpenClaw `model.run` received no usable text output from the OpenRouter routes.
- Local Ollama aliases: none active
- Local `codestral:latest` and `devstral:latest` were tested and removed because they did not return promptly on this Mac
- `phi3:mini`, Qwen, and Gemma are intentionally excluded from OpenClaw routing
- Gemini is banned from active OpenClaw routing
- OpenRouter provider models aligned to the live JSON in `~/.openclaw/openclaw.json`
- OpenRouter auth uses an exec SecretRef resolver; the temporary `.op/openrouter.env` fallback is chmod `600` until 1Password CLI is configured
- Validator scripts now provide the live runtime contract check instead of
  relying on this report as the only source of truth

### Skills Needing Setup (38)

| Skill | Requirements | Priority |
|-------|-------------|----------|
| apple-notes | macOS + memo CLI | Low |
| apple-reminders | macOS + remindctl | Low |
| bear-notes | macOS + grizzly CLI | Low |
| blogwatcher | blogwatcher CLI | Low |
| blucli | BluOS CLI | Low |
| bluebubbles | iMessage via BlueBubbles | Low |
| camsnap | RTSP/ONVIF camera capture | Low |
| clawhub | ClawHub CLI | Low |
| eightctl | Eight Sleep control | Low |
| gifgrep | GIF search CLI | Low |
| gog | Google Workspace CLI | Medium |
| goplaces | Google Places API | Medium |
| himalaya | Email via IMAP/SMTP | Low |
| imsg | iMessage via CLI | Low |
| mcporter | MCP server CLI | Low |
| model-usage | CodexBar cost tracking | Low |
| nano-pdf | PDF editing CLI | Low |
| notion | Notion API key | Medium |
| openai-whisper | Local Whisper CLI | Low |
| openai-whisper-api | OpenAI Whisper API | Low |
| openhue | Philips Hue CLI | Low |
| oracle | Oracle CLI | Low |
| ordercli | Food ordering CLI | Low |
| peekaboo | macOS UI capture | Low |
| sherpa-onnx-tts | Local TTS | Low |
| slack | Slack channel control | Medium |
| songsee | Audio spectrograms | Low |
| spotify-player | Spotify control | Low |
| summarize | URL/file summarization | Medium |
| things-mac | Things 3 CLI | Low |
| tmux | tmux control | Low |
| trello | Trello API | Low |
| video-frames | ffmpeg video extraction | Low |
| voice-call | Voice call plugin | Low |
| wacli | WhatsApp CLI | Low |
| xurl | Twitter/X API | Medium |

### Skills Installation Commands

```bash
# Install specific skill
openclaw skills install <skill-name>

# Search for skills
openclaw skills search <query>

# Update all ClawHub skills
openclaw skills update
```

---

## Next Session Tasks

1. Configure Twitch OAuth: https://dev.twitch.tv
2. Configure Google Chat OAuth: Google Cloud Console
3. Enable Nostr channel: Test with Orpheus keys in 1Password
4. Consider Continue Extension and Cursor OpenRouter setup (lower priority)

---

###### [["The world is quiet here."]]
