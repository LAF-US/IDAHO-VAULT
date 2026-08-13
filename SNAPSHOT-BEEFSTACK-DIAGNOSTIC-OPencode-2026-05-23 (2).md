---
authority: LOGAN
agent: opencode
created: 2026-05-23
tags: [snapshot, beefstack, hermes, openrouter, mistral, routing, diagnostics]
related:
  - BEEFSTACK-MODEL-ROUTING-2026-05-17.md
  - SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md
  - OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE-2026-05-23.md
  - ../skills/openrouter-config.md
---

# Snapshot — BEEFSTACK Diagnostic State (OpenCode) — 2026-05-23

## Context

OpenCode (third BEEFSTACK leg) was called in to troubleshoot why Hermes Agent
could not start up. Hermes was resuming a session with `mistralai/mistral-7b-free`
as primary — a model that no longer exists on OpenRouter.

The BEEFSTACK backup on disk (`config.yaml.bak-20260518-BEEFSTACK`) had Ollama
as primary with zero fallback providers. This is the correct universal doctrine
for the BEEFSTACK but not the correct MacBook operational posture: this machine
cannot run local Ollama models without hanging.

## Problems Discovered

### 1. OpenRouter — Invalid Model ID
- `mistralai/mistral-7b-free` → HTTP 400: not a valid model ID (removed from OpenRouter)
- `mistralai/mistral-small-latest` → HTTP 400: not a valid model ID (OpenRouter does not support `-latest` suffix)

### 2. OpenRouter — Privacy Guardrails Blocking Mistral
- `mistralai/mistral-medium-3-5` → HTTP 404: "No endpoints available matching your guardrail restrictions"
- `mistralai/mistral-small-2603` → HTTP 404: same guardrail error
- Cause: OpenRouter account-level privacy settings restrict endpoints available to this key
- Non-Mistral models (e.g., `meta-llama/llama-3.1-8b-instruct` via DeepInfra) pass through fine
- Fix requires dashboard change at openrouter.ai/settings/privacy

### 3. OpenRouter — Insufficient Credits
- `anthropic/claude-sonnet-4.6` → HTTP 402: requested 64000 tokens, can only afford 36025
- Management API shows `total_credits: $10.00`, `total_usage: $9.66`, remaining `$0.34`
- Account is functionally exhausted for paid models

### 4. Mistral Direct API — Rate Limited on Paid Tier
- `mistral-small-latest` → HTTP 429: "Service tier capacity exceeded"
- Transient — cleared later in the session and now working

### 5. Ollama Local — Too Slow
- `devstral:latest` via Ollama hangs on this MacBook
- Cannot be used as default live inference path

## Current BEEFSTACK Config (Live)

### Primary
- Provider: `mistral-direct` (direct Mistral API via `MISTRAL_API_KEY`)
- Model: `mistral-small-latest`
- Status: ✅ Working (recites Jabberwocky correctly)

### Fallback Chain (6 entries)
| # | Provider | Model | Status | Notes |
|---|----------|-------|--------|-------|
| 1 | mistral-direct | `open-mixtral-8x7b` | ✅ Working | Free tier, served as `mistral-small-2603` |
| 2 | openrouter | `meta-llama/llama-3.1-8b-instruct` | ✅ Working | Free via DeepInfra, different provider bucket |
| 3 | mistral-direct | `open-mistral-7b` | ✅ Working | Free tier, served as `ministral-8b-2512` |
| 4 | openrouter | `mistralai/mistral-small-2603` | ⛔ Guardrails | Works if privacy settings fixed |
| 5 | openrouter | `anthropic/claude-sonnet-4.6` | ⛔ Credits | Works if credits added |
| 6 | ollama | `devstral:latest` | 🐌 Slow | Last resort only |

### Provider Configuration
```yaml
providers:
  openrouter:
    api_key: ''  # loaded from OPENROUTER_API_KEY env
  mistral-direct:
    base_url: https://api.mistral.ai/v1
    key_env: MISTRAL_API_KEY
    api_mode: chat_completions
```

## OpenRouter Management Findings

### SWARM ROUTER KEY (Inference)
- Hash prefix: `160f2dcf`
- Label: `sk-or-v1-737...cf2`
- Disabled: false
- Limit: null (no key-level cap)
- Limit remaining: null
- `include_byok_in_limit`: true
- Total usage: $9.66 (of $10.00 added)
- Created: 2026-04-20
- Workspace: Default Workspace

### Default Workspace
- ID: `79a8f7cd-9292-5dcf-8450-1419dbee5920`
- `default_provider_sort`: exacto (no automatic fallback between providers)
- `default_text_model`: `mistralai/mistral-large`
- I/O logging enabled

### Credit Balance
- Total credits added: $10.00
- Total usage: $9.66
- Remaining: $0.34

## Key Decisions Made

1. **MacBook operational override remains**: cloud-first via Mistral Direct API,
   not local-first via Ollama (Ollama hangs on this hardware)
2. **OpenRouter retained in fallback chain** but demoted behind working free routes
   until privacy settings and credits are resolved
3. **Mistral Direct** is the primary inference path — uses the user's own
   `MISTRAL_API_KEY`, bypasses OpenRouter entirely
4. **Gemini not introduced** into any agentic LLM route (per BEEFSTACK ban)
5. **Phi/Qwen/Gemma not introduced** into any fallback (per BEEFSTACK dislike)
6. **OpenRouter Management Key** is available for admin operations but cannot be
   used for inference. Autonomy rules per OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE:
   list/inspect autonomous, create/disable semi-autonomous, delete/raise limits
   requires Logan approval.

## Files Touched This Session

### Deleted
- `~/.hermes/sessions/session_20260523_053921_24370e.json` — stale session with broken model
- `~/.hermes/sessions/request_dump_20260523_053921_24370e_074739.json`
- `~/.hermes/sessions/request_dump_20260523_053921_24370e_337287.json`

### Modified
- `~/.hermes/config.yaml` — lines 1-27 (model/providers/fallbacks); lines 28-515 untouched

### Created (test sessions, all successful)
- 7 Hermes session files under `~/.hermes/sessions/session_20260523_14*`
- This diagnostic snapshot

### Untouched
- `~/.hermes/.env` — all 22 lines, all keys present
- `~/.hermes/auth.json` — unmodified
- All 13 `~/.hermes/config.yaml.bak*` files
- All vault documents and skill files

## Standing BEEFSTACK Principles (Reaffirmed)

- Mistral #1 preferred provider family (Claude #2, ChatGPT/Codex #3)
- Gemini banned for agentic LLM routing
- Phi/Qwen/Gemma excluded from defaults and fallbacks
- Local-first in doctrine, cloud-first on this MacBook operationally
- Diversify by provider bucket, not just model name
- BYOK-aware fallback: don't retry same upstream provider after BYOK 429
- Router-aware fallback: after OpenRouter failure, direct API calls can escape
