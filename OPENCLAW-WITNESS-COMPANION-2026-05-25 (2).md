---
title: "OPENCLAW WITNESS COMPANION — 2026-05-25"
subtitle: "Local Machine Survey: Logan's MacBook — OpenClaw Presence"
type: witness-report
companion-to: OPENCLAW-WITNESS-REPORT-2026-05-25
source: local-machine-survey-claude-code-session-2026-05-25
tags:
- openclaw
- witness
- local-survey
- macbook
- gateway
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - OPENCLAW-WITNESS-REPORT-2026-05-25
  - OPENCLAW-WITNESS-DELTA-2026-05-25
  - HERMES-WITNESS-COMPANION-2026-05-25
  - SYZYGY-HERMES-OPENCLAW-2026-05-25
---

# OPENCLAW WITNESS COMPANION — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Local machine witness — observed state of the MacBook only
**Companion to:** `OPENCLAW-WITNESS-REPORT-2026-05-25.md` (research/theory)
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

This document records what I observed on the MacBook regarding OpenClaw during a survey on 2026-05-25.

The companion report (`OPENCLAW-WITNESS-REPORT-2026-05-25.md`) covers what OpenClaw *is* — research grounded in external sources. This document covers what is *here* — grounded in direct local observation.

---

## RUNNING PROCESS

One OpenClaw process is active at time of survey:

| PID | Process | Details |
|---|---|---|
| 868 | `node .../openclaw/dist/index.js gateway --port 18789` | Gateway daemon, loopback only |

OpenClaw is **not idle**. Its gateway has been running since machine restart at 00:04 today (2026-05-25). The gateway is the WebSocket hub for all local and node connections.

---

## LAUNCH AGENT — AUTO-START

```
~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

The gateway is registered as a macOS LaunchAgent (`ai.openclaw.gateway`). It starts automatically at login. Version string in plist: `v2026.5.16-beta.3`.

---

## VERSION STATE

| | Value |
|---|---|
| **Installed** | v2026.5.16-beta.3 (**beta** — not stable release) |
| **Available (latest stable)** | v2026.5.22 |
| **Runtime** | Node.js v24.15.0 via nvm |
| **Binary path** | `/Users/logan/.nvm/versions/node/v24.15.0/bin/openclaw` |
| **Module path** | `/Users/logan/.nvm/versions/node/v24.15.0/lib/node_modules/openclaw/` |
| **Last update check** | 2026-05-25 05:03 UTC |

OpenClaw is running a **beta** build, one stable release behind. v2026.5.22 is available.

---

## GATEWAY: PLATFORM AND NODE STATE

### Gateway mode: **`local`**

This is the defining configuration fact. OpenClaw's gateway is set to `local` mode:

```json
"gateway": {
  "mode": "local",
  "port": 18789,
  "bind": "loopback"
}
```

**`local` mode means:** The gateway only accepts WebSocket connections from local processes and paired nodes. It is **not** connected to any external messaging platform channels. There is no Telegram bot, no Discord connection, no WhatsApp bridge, no Signal — none of the external channel infrastructure that Hermes uses.

The gateway is a **local hub**, not a platform gateway in the Hermes sense.

### Paired Nodes

| Node | Device | Role | First paired | Last connected |
|---|---|---|---|---|
| the MacBook (operator node) | macOS (darwin), operator | probe / admin | 2026-05-13 | (local) |
| **Windows-ZBFURY** | Windows | node-host | 2026-05-17 | **2026-05-18 20:40** |

**ZBFURY** is the Windows laptop. It is a paired node with capabilities: `system`, `browser`, `file`, and commands `system.run.prepare`, `system.run`, `system.which`, `browser.proxy`. It was last connected May 18 — currently offline.

**No pending nodes.** `pending.json` is empty `{}`.

### Bonjour Advertisement

Gateway advertises via mDNS:
```
Logan's MacBook Pro (OpenClaw)._openclaw-gw._tcp.local.
host: Logans-MBP.local., port: 18789
```

---

## CONFIGURATION SNAPSHOT

File: `~/.openclaw/openclaw.json` (observed 2026-05-25)

| Parameter | Value |
|---|---|
| Primary model | `mistralai/mistral-medium-3-5` via OpenRouter |
| Fallback 1 | `mistralai/mistral-small-2603` via OpenRouter |
| Fallback 2 | `anthropic/claude-sonnet-4.6` via OpenRouter |
| Fallback 3 | `openai/gpt-5.3-codex` via OpenRouter |
| Fallback 4 | `mistralai/mistral-large-2512` via OpenRouter |
| Local Ollama | `devstral:latest` — **disabled** in plugins |
| Tools profile | `coding` |
| Gateway mode | `local` — loopback only |
| Gateway port | 18789 |
| Session DM scope | `per-channel-peer` |

**Secret provider chain:** Three providers are configured in `openclaw.json`:
1. **1Password CLI**: `op read op://Vault/OpenRouter API Key/credential` — requires `op` CLI authenticated
2. **Vault script**: `/Users/logan/IDAHO-VAULT/!/resolve_openrouter_secret.py` — custom resolver
3. **Gateway token file**: file-based provider reading from `~/.openclaw/secrets/gateway-token` (internal gateway auth token)

This is more sophisticated than Hermes's `.env` file pattern. But it means the agent requires `op` or the vault script to be functional at runtime.

**Budget event on record:** Gateway log (2026-05-19) shows `403 Budget limit exceeded (daily limit)` for all OpenRouter models on that date. All four fallbacks failed. Daily budget resets; this is a dated event.

---

## WORKSPACE STATE

All files live at `~/.openclaw/workspace/`.

### Identity and Memory Files

| File | State | Contents |
|---|---|---|
| **SOUL.md** | ✅ Present — has content | **Generic OpenClaw default template** — not Logan-specific (see below) |
| **IDENTITY.md** | ⬜ Empty template | Name, creature, vibe, emoji: all blank |
| **USER.md** | ⬜ Empty template | Name, timezone, notes: all blank |
| **MEMORY.md** | ❌ Absent | No long-term memory file |
| **BOOTSTRAP.md** | ⚠️ Still present | Onboarding script — presence means bootstrap was never completed |
| **HEARTBEAT.md** | ⬜ Empty | No active heartbeat tasks |
| **TOOLS.md** | ⬜ Empty template | No custom tool notes |
| **AGENTS.md** | ✅ Present | Standard OpenClaw workspace instructions |

### SOUL.md — Content

OpenClaw's SOUL.md has content — but it is the **generic OpenClaw-shipped default template**, not a Logan-specific identity. Key sections of what is there:

- "Be genuinely helpful, not performatively helpful"
- "Have opinions"
- "Be resourceful before asking"
- "Earn trust through competence"
- "Remember you're a guest"
- Boundaries: private things stay private; ask before acting externally
- Vibe guidance for group chats

This SOUL.md was written by OpenClaw contributors as the starter template. It is not Logan's appointment of this agent. It is a placeholder that was never overwritten with Logan's voice.

### BOOTSTRAP.md — Still Present

The BOOTSTRAP.md file serves as OpenClaw's onboarding script. Per OpenClaw's own AGENTS.md:

> "If BOOTSTRAP.md exists, that's your birth certificate. Follow it, figure out who you are, then delete it. You won't need it again."

The file exists on the MacBook. This means the agent was never guided through its identity initialization. It has no name. It has no declared nature. It does not know Logan's name, pronouns, or timezone. Every session begins as if it is meeting Logan for the first time.

### Memory DB

`~/.openclaw/memory/main.sqlite` — present but empty:
- Files indexed: **0**
- Chunks: **0**

The semantic memory engine has never processed any content.

---

## SKILLS INSTALLED

### Built-in skills (npm module) — 53 total

**Active (default on):** 27 skills available at session start

| Skill | Description |
|---|---|
| `1password` | 1Password CLI |
| `apple-notes` | Apple Notes via memo CLI |
| `blogwatcher` | RSS/Atom feed monitoring |
| `canvas` | OpenClaw Canvas |
| `clawhub` | ClawHub CLI — install/update skills |
| `gemini` | Gemini CLI |
| `gh-issues` | GitHub Issues + subagent workflows |
| `gifgrep` | GIF search and download |
| `github` | `gh` CLI for GitHub |
| `gog` | Google Workspace CLI |
| `healthcheck` | Host security audit |
| `mcporter` | MCP server management |
| `nano-pdf` | PDF editing |
| `node-connect` | Node pairing diagnosis |
| `obsidian` | Obsidian vaults via obsidian-cli |
| `openhue` | Philips Hue control |
| `oracle` | Second-model review |
| `session-logs` | Search own session logs |
| `skill-creator` | Create/edit SKILL.md files |
| `songsee` | Audio spectrogram |
| `taskflow` | Multi-step durable tasks |
| `taskflow-inbox-triage` | Inbox triage pattern |
| `things-mac` | Things 3 on macOS |
| `video-frames` | Extract frames via ffmpeg |
| `wacli` | WhatsApp history sync |
| `weather` | Weather lookup |
| `xurl` | X (Twitter) API |

**Explicitly disabled in config:** 26 skills
`apple-reminders`, `bear-notes`, `blucli`, `bluebubbles`, `camsnap`, `coding-agent`, `discord`, `eightctl`, `goplaces`, `himalaya`, `imsg`, `model-usage`, `notion`, `openai-whisper`, `openai-whisper-api`, `ordercli`, `peekaboo`, `sag`, `sherpa-onnx-tts`, `slack`, `sonoscli`, `spotify-player`, `summarize`, `tmux`, `trello`, `voice-call`

### Plugin skills (ClawHub-installed) — 1

| Skill | Source |
|---|---|
| `browser-automation` | ClawHub — browser control via OpenClaw browser tool |

### Workspace skills (user-created) — 1

| Skill | Notes |
|---|---|
| `sam-tts` | Custom Node.js TTS skill — same SAM TTS present in Hermes workspace |

---

## SESSIONS

**18 sessions** with `.jsonl` trajectory files in `~/.openclaw/agents/main/sessions/`.

Most recent sessions by file modification date:
- 2026-05-19 22:23 — last active session
- 2026-05-19 01:25
- 2026-05-18 22:56
- 2026-05-17 01:26
- 2026-05-14 21:26

The agent has not had an active session since May 19 (six days ago as of this survey).

---

## PLUGINS STATE

`~/.openclaw/plugins/installs.json` — 90 plugin records.

Notable enabled/disabled state:
- `openrouter` — **enabled** (primary model provider)
- `ollama` — **disabled**
- `admin-http-rpc` — **disabled**
- `bonjour` — active (local network advertisement)
- `browser` — active (browser control on port 18791)
- `canvas` — active
- `device-pair` — active
- `file-transfer` — active
- `memory-core` — active (SQLite, but 0 files indexed)
- `phone-control` — active
- `talk-voice` — active

---

## MCP STATE

No MCP servers configured. One temp file present:
```
~/.openclaw/tmp/jiti/dist-bundle-mcp-DPPOalPH.fcd0b7c9.cjs
```
This is a cached MCP bundle — the runtime has MCP capability but no servers have been added.

`openclaw mcp serve` is available (documented capability) but not currently wired to any MCP client (Claude Code, Cursor, etc.).

---

## SUMMARY OBSERVATIONS

1. **OpenClaw is a live daemon on the MacBook.** Gateway has been running since 00:04 today. LaunchAgent ensures it restarts at login.

2. **Gateway is local-only.** `mode: local` means no external platform channels. OpenClaw has no Telegram, Discord, or WhatsApp connections on the MacBook. It operates as a local hub.

3. **One node paired: the Windows laptop (ZBFURY).** The Windows machine is paired and configured as a compute node with system/browser/file capabilities. Currently offline (last connected May 18).

4. **Bootstrap was never completed.** BOOTSTRAP.md is still present. IDENTITY.md and USER.md are both empty templates. The agent does not know its own name or Logan's name.

5. **SOUL.md has generic content — not Logan's.** The default OpenClaw-shipped template is there. It reads well but is not a Logan-specific appointment.

6. **Memory is empty.** MEMORY.md absent. Memory DB has 0 indexed items. 18 prior sessions have produced no accumulated memory.

7. **Secrets via 1Password.** More sophisticated than Hermes's .env pattern — but requires `op` CLI to be authenticated at runtime.

8. **Running a beta build.** v2026.5.16-beta.3 vs. stable v2026.5.22.

9. **No MCP servers configured.** The mcporter skill is available and the MCP runtime is present, but no servers added.

10. **sam-tts custom skill present** — the same Node.js TTS skill found in both agent workspaces.

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a local survey artifact.*
*Companion to: `OPENCLAW-WITNESS-REPORT-2026-05-25.md`*
