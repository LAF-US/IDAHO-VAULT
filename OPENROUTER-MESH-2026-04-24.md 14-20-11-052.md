---
title: "OpenRouter Mesh Configuration"
status: active
authority: LOGAN
date created: 2026-04-24
date modified: 2026-04-24
related:
  - OpenRouter
  - Discord
  - OpenClaw
  - Claude Code
  - Codex
  - Cursor
  - VSCode
  - Ollama
  - SPARKSEED
  - Signal
  - Telegram
  - Nostr
---

# OpenRouter Unified Mesh

All AI model calls centralized through OpenRouter for:
- Single API key (1Password: `op://Vault/OpenRouter API Key/credential`)
- Cost control via per-key rate limits
- Free tier models as default (zero-cost routing)
- Model flexibility without rewiring

## Current Status

| Component | Status | Model |
|-----------|--------|-------|
| OpenClaw Gateway | ✅ Running | `openrouter/openai/gpt-4o-mini` |
| Codex | ✅ Ready | Via launch scripts |
| Claude Code | ✅ Ready | Via launch scripts |
| Discord | ⚠️ Enabled | Needs token verification |
| WhatsApp | ✅ Enabled | |
| Signal | ⏳ Pending | Need CLI token |
| Telegram | ⏳ Pending | Need bot token |
| Nostr | ⏳ Pending | Using Orpheus keys |

## Mesh Topology

```
                    ┌─────────────────────────────────────┐
                    │         OpenRouter.ai                 │
                    │    openrouter.ai/api/v1 = unified   │
                    └─────────────────────────────────────┘
                       ▲     ▲     ▲     ▲     ▲     ▲
                       │     │     │     │     │     │
              ┌────────┴┐ ┌───┴──┐ ┌────┴──┐ ┌───┴──┐ ┌────┴───┐
              │ Ollama  │ │Cursor│ │OpenClaw│ │Claude│ │ Codex  │
              │(local) │ │(UI)  │ │(models)│ │(env) │ │ (env)  │
              └─────────┘ └──────┘ └───────┘ └──────┘ └────────┘
```

## Free Tier Models (Active)

| Model | Context | Use |
|-------|---------|-----|
| `openai/gpt-4o-mini` | 286K | Primary / default |
| `anthropic/claude-3.5-haiku` | 131K | Claude tasks |
| `mistralai/mistral-large-2411` | 131K | Paid / larger context |
| `mistralai/mistral-small-2603` | 131K | Free / lightweight |

## Current Live Binding

- Gateway bind: `loopback`
- Auth mode: `token`
- Primary model: `openrouter/openai/gpt-4o-mini`

## Bootstrap

Run the canonical local bootstrap chain to:
1. Load secrets from 1Password
2. Start OpenClaw gateway
3. Reload secrets
4. Audit configuration

Current runtime helpers:
- `python3 !/resolve_openrouter_secret.py`
- `python3 scripts/validate_openrouter.py`
- `python3 scripts/validate_services.py --write-matrix`

## 1Password Items (Vault)

| Item | Field | Status |
|------|-------|--------|
| OpenRouter API Key | credential | ✅ |
| OpenClaw Gateway Token | credential | ✅ Created |
| Discord OpenClaw Bot | credential | ✅ |
| Signal | number | ✅ |
| Nostr (Orpheus) | password, username | ✅ |
| Linear API Key | credential | ✅ |
| Mistral | credential | ✅ |
| GitHub | private_key | ⚠️ Multiple items |
| Claude | password | ⚠️ OAuth only, no API key |
| Qodo API Key | credential | ✅ |
| Telegram Bot | credential | ⏳ Needs token |

## Configuration Files

- Live OpenClaw: `C:\Users\loganf\.openclaw\openclaw.json`
- Vault reference: `.openclaw/openclaw.json`
- SPARKSEED: `src/idaho_vault/sparkseed.py`

## Launch Scripts

```bash
# Claude Code via OpenRouter
.\!launch-claude-openrouter.cmd

# Codex via OpenRouter
.\!launch-codex-openrouter.cmd
```

## Validation Surfaces

- Compatibility snapshot: `!/INTEGRATIONS/COMPATIBILITY.md`
- Health log: `!/MONITORING/health-log.md`
- SSH/Git signing guidance remains separate in the harvested 1Password SSH agent docs.

###### [["The world is quiet here."]]
