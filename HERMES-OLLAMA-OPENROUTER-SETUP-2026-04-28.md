---
title: "Hermes + Ollama + OpenRouter Configuration"
subtitle: "Local-First AI Stack Setup"
type: documentation
created: 2026-04-28
author: Logan Finney
status: configured
---

# Hermes Agent: Ollama + OpenRouter Configuration

**Date:** April 28, 2026  
**Status:** ✅ Configured, pending model downloads

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Hermes Agent                            │
│                                                             │
│  Primary: Ollama Local (qwen3.5, phi3, qwen2.5, +more)     │
│         ↓ (if unavailable)                                  │
│  Fallback 1: Ollama Light (phi3, qwen2.5)                   │
│         ↓ (if unavailable)                                  │
│  Fallback 2: OpenRouter Auto (paid tier)                    │
│         ↓ (if unavailable/rate-limited)                    │
│  Fallback 3: OpenRouter Free (Nemotron, Llama, Gemma)       │
│         ↓ (if unavailable/rate-limited)                    │
│  Fallback 4: OpenRouter Reasoning (DeepSeek R1)            │
└─────────────────────────────────────────────────────────────┘
```

---

## Provider Configuration

### Primary: Ollama Local

| Setting | Value |
|---------|-------|
| Endpoint | `http://127.0.0.1:11434/v1` |
| Default Model | `qwen3.5:latest` |
| API Key | `ollama` (placeholder) |

**Models (installed):**
- `qwen3.5:latest` — 9.7B, best quality, 6.6 GB
- `phi3:mini` — 3.8B, lightweight, 2.2 GB
- `qwen2.5:3b` — 3.1B, minimal, 1.9 GB

**Models (pending):**
- `codestral:latest` — Code generation
- `devstral:latest` — Code understanding
- `mistral-large:latest` — Complex reasoning

### Fallback 1: Ollama Lightweight

| Setting | Value |
|---------|-------|
| Endpoint | `http://127.0.0.1:11434/v1` |
| Default Model | `phi3:mini` |

Quick local fallback for lightweight tasks.

### Fallback 2: OpenRouter Auto (Best Quality)

| Setting | Value |
|---------|-------|
| Endpoint | `https://openrouter.ai/api/v1` |
| API Key | `env:OPENROUTER_API_KEY` |
| Default Model | `openrouter/auto` |

Routes to best available model for your request. Uses paid tier credits.

### Fallback 3: OpenRouter Free

| Setting | Value |
|---------|-------|
| Endpoint | `https://openrouter.ai/api/v1` |
| API Key | `env:OPENROUTER_API_KEY` |
| Default Model | `nvidia/nemotron-3-super-120b-a12b:free` |

**Available Free Models:**
- NVIDIA Nemotron 3 Super (120B, 1M context)
- Meta Llama 3.2 3B Instruct
- Google Gemma 4 31B
- inclusionAI L3.1 Euryale 70B
- `openrouter/free` — Auto-selects free model

### Fallback 4: OpenRouter Reasoning

| Setting | Value |
|---------|-------|
| Endpoint | `https://openrouter.ai/api/v1` |
| API Key | `env:OPENROUTER_API_KEY` |
| Default Model | `deepseek/deepseek-r1:free` |

For complex reasoning tasks.

---

## Config File Location

```
~/.hermes/config.yaml
```

### Key Settings

```yaml
model:
  provider: ollama-local      # Primary provider
  default: qwen3.5:latest    # Default model
  api_mode: chat_completions

providers:
  ollama-local:
    api: http://127.0.0.1:11434/v1
    api_key: ollama
    default_model: qwen3.5:latest

  openrouter-auto:
    api: https://openrouter.ai/api/v1
    api_key: env:OPENROUTER_API_KEY
    default_model: openrouter/auto

  openrouter-free:
    api: https://openrouter.ai/api/v1
    api_key: env:OPENROUTER_API_KEY
    default_model: nvidia/nemotron-3-super-120b-a12b:free

fallback_providers:
- ollama-light
- openrouter-auto
- openrouter-free
- openrouter-reasoning
```

---

## Environment Variables

File: `~/.hermes/.env`

```bash
# OpenRouter API Key (required for cloud fallbacks)
OPENROUTER_API_KEY=sk-or-v1-xxx

# Optional: Override default base URLs
# OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
# OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

---

## Model Selection Strategy

| Task Type | Recommended Provider | Model |
|-----------|---------------------|-------|
| General chat | Ollama Local | `qwen3.5:latest` |
| Quick/simple tasks | Ollama Light | `phi3:mini` |
| Code generation | Ollama Coding | `codestral:latest` |
| Code review | Ollama Coding | `devstral:latest` |
| Complex reasoning | Ollama Reasoning | `mistral-large:latest` |
| Unknown/any | OpenRouter Auto | `openrouter/auto` |
| Budget-constrained | OpenRouter Free | `nvidia/nemotron-3-super-120b-a12b:free` |
| Deep reasoning | OpenRouter Reasoning | `deepseek/deepseek-r1:free` |

---

## Usage

### Start Hermes
```bash
hermes
```

### Switch Model Mid-Session
```
/model openrouter-auto
```

### Check Status
```bash
hermes doctor
```

### View Config
```bash
hermes config
```

---

## Notes

- OpenRouter free tier: 50 req/day (rate-limited)
- Paid tier: ~$10 credit gets 1M free requests
- Ollama must be running (`ollama serve`)
- Models load into RAM when first used

---

## TODO

- [ ] Verify codestral, devstral, mistral-large downloads complete
- [ ] Update config with downloaded model names
- [ ] Test full fallback chain
- [ ] Run `hermes doctor` to verify setup

---

*Configuration created via Hermes Agent session — April 28, 2026*
