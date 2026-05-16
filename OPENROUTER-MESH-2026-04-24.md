---
title: "OpenRouter Mesh Configuration"
status: active
authority: LOGAN
date created: 2026-04-24
date modified: 2026-05-14
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

# OpenRouter + Local Ollama Mesh

Cloud and complex AI model calls are centralized through OpenRouter for:
- Single API key (1Password: `op://Vault/OpenRouter API Key/credential`)
- Cost control via per-key rate limits
- Tool-call-capable cloud models for OpenClaw defaults
- Model flexibility without rewiring

Preferred hosted family order: Mistral, then Claude, then ChatGPT/OpenAI.

Local Ollama remains installed but is not active in OpenClaw routing; allowed local Mistral-family models were too slow on this Mac.

## Current Status

| Component | Status | Model |
|-----------|--------|-------|
| OpenClaw Gateway | ✅ Running | `openrouter/mistralai/mistral-small-2603` |
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

## Tool-Capable Cloud Models (Active)

| Model | Context | Use |
|-------|---------|-----|
| `mistralai/mistral-small-2603` | Provider advertised | Primary / default |
| `mistralai/mistral-medium-3-5` | Provider advertised | Complex Mistral fallback |
| `anthropic/claude-sonnet-4.6` | Provider advertised | Claude fallback |
| `openai/gpt-5.3-codex` | Provider advertised | Codex fallback |
| `mistralai/mistral-large-2512` | Provider advertised | Larger Mistral fallback |
| `mistralai/devstral-2512` | Provider advertised | Mistral coding alias |
| `anthropic/claude-haiku-4.5` | Provider advertised | Fast Claude alias |

## Current Live Binding

- Gateway bind: `loopback`
- Auth mode: `token`
- Preferred routing families: Mistral -> Claude -> ChatGPT/OpenAI
- Primary model: `openrouter/mistralai/mistral-small-2603`
- Fallbacks: `openrouter/mistralai/mistral-medium-3-5`, `openrouter/anthropic/claude-sonnet-4.6`, `openrouter/openai/gpt-5.3-codex`, `openrouter/mistralai/mistral-large-2512`
- Specialist aliases: `mistral-coder` -> `openrouter/mistralai/devstral-2512`
- Magistral routes were tested and removed because they returned no usable text output through OpenClaw `model.run`.
- Local aliases: none active
- Local Ollama models were removed from active routing because allowed Mistral-family local routes did not return promptly, and Phi/Qwen/Gemma/Gemini are not acceptable alternatives.
- Local `codestral:latest` was tested and removed because it did not return promptly on this Mac.
- Excluded/disliked families: Phi, Qwen, Gemma.
- Banned family: Gemini.

## Bootstrap

Run the canonical local bootstrap chain to:
1. Resolve the OpenRouter secret (1Password when configured; chmod `600` fallback until then)
2. Start OpenClaw gateway
3. Reload secrets
4. Audit configuration

Current runtime helpers:
- `python3 !/resolve_openrouter_secret.py`
- `./!-launch-claude-openrouter.sh`
- `./!-launch-codex-openrouter.sh`
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

- Live OpenClaw: `~/.openclaw/openclaw.json`
- Model routing patch: `~/.openclaw/model-routing-20260513.patch.json5`
- Vault reference: `.openclaw/openclaw.json`
- SPARKSEED: `src/idaho_vault/sparkseed.py`

## Launch Scripts

```bash
# Claude Code via OpenRouter
./!-launch-claude-openrouter.sh

# Codex via OpenRouter
./!-launch-codex-openrouter.sh
```

## Mac Runtime Notes

- OpenClaw config uses an exec SecretRef resolver for the OpenRouter API key.
- 1Password CLI is installed but not configured for account access on this Mac.
- Temporary plaintext fallback is restricted to `.op/openrouter.env` mode `600`; replace it with the `op://Vault/OpenRouter API Key/credential` reference after `op` is configured.
- `phi3:mini`, Qwen, Gemma, Codestral, and Devstral may remain installed locally but are not part of active OpenClaw routing.
- Gemini must not be added to active OpenClaw routing.

## Validation Surfaces

- Compatibility snapshot: `!/INTEGRATIONS/COMPATIBILITY.md`
- Health log: `!/MONITORING/health-log.md`
- SSH/Git signing guidance remains separate in the harvested 1Password SSH agent docs.

###### [["The world is quiet here."]]
