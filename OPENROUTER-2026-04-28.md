---
title: "OPENROUTER"
subtitle: "Deep Research Report"
type: research
source: web-search-2026-04-28
tags:
- openrouter
- unified-api
- llm-aggregation
- ai-infrastructure
- free-models
created: 2026-04-28
author: Logan Finney
---

# OPENROUTER
## Deep Research Report

**Date:** April 28, 2026  
**Source:** Web research via Hermes Agent (this session)  
**Status:** Active research — Living document

---

## EXECUTIVE SUMMARY

**OpenRouter** is a unified API that provides access to 300+ AI models from 60+ providers through a single endpoint. It normalizes provider schemas to OpenAI-compatible format, handles fallbacks automatically, and offers both free and paid tiers.

> *"A single API for hundreds of AI models."*

---

## WHAT IS OPENROUTER?

### Core Value Proposition

- **Unified API** — One endpoint, 300+ models
- **Automatic Fallbacks** — Routes to least expensive/best available GPU
- **OpenAI Compatible** — Drop-in replacement for existing code
- **Free Tier** — 25+ free models, no credit card required
- **No Markup** — Pricing shown is exactly what providers charge

### Key Stats

| Metric | Value |
|--------|-------|
| Models | 300+ |
| Providers | 60+ |
| Free Models | 25+ |
| Free Tier Limit | 50 req/day |
| Context Lengths | Up to 2M tokens (varies by model) |

---

## PRICING TIERS

### Free

| Feature | Limit |
|---------|-------|
| Platform Fee | None |
| Free Models | 25+ |
| Free Providers | 4 |
| Rate Limit | 50 req/day |
| Payment | None required |

### Pay-as-you-go

| Feature | Details |
|---------|---------|
| Platform Fee | 5.5% |
| Models | 300+ |
| Providers | 60+ |
| Rate Limit | High global limits |
| Payment | Credit card, crypto, bank transfer |
| BYOK | 1M free req/month, 5% fee after |

### Enterprise

| Feature | Details |
|---------|---------|
| Platform Fee | Bulk discounts |
| Rate Limits | Optional dedicated limits |
| SLAs | Contractual SLAs |
| SSO/SAML | Available |
| Payment | Invoicing, POs |

---

## FREE MODELS (Current)

### Top Free Models by Usage

| Model | Provider | Context | Strengths |
|-------|----------|---------|-----------|
| **Tencent Hy3 preview** | Tencent | 262K | Agentic workflows, code generation, reasoning |
| **NVIDIA Nemotron 3 Super** | NVIDIA | 262K | 120B MoE, multi-agent, 1M context |
| **inclusionAI Ling-2.6-1T** | inclusionai | 262K | Fast reasoning, SWE-bench, AIME26 |
| **OpenAI gpt-oss-120b** | OpenAI | 131K | Apache 2.0, MoE, tool calling |
| **MiniMax M2.5** | MiniMax | 197K | Office automation, SWE-bench 80.2% |
| **Google Gemma 4 31B** | Google | 262K | Multimodal, 140+ languages |
| **NVIDIA Nemotron Nano 9B** | NVIDIA | 128K | Reasoning + non-reasoning unified |

### Free Router

Model: `openrouter/free`

Automatically selects a free model based on request requirements (vision, tools, etc.)

---

## API REFERENCE

### Endpoint

```
POST https://openrouter.ai/api/v1/chat/completions
```

### Headers

| Header | Purpose |
|--------|---------|
| `Authorization: Bearer <KEY>` | API key (required) |
| `HTTP-Referer` | App attribution for leaderboards |
| `X-OpenRouter-Title` | App name for leaderboards |

### Basic Request

```json
{
  "model": "openai/gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

### Supported Parameters

| Parameter | Range | Notes |
|-----------|-------|-------|
| `max_tokens` | [1, context_length) | Max completion tokens |
| `temperature` | [0, 2] | Sampling temperature |
| `top_p` | (0, 1] | Nucleus sampling |
| `top_k` | [1, ∞) | Not for OpenAI models |
| `frequency_penalty` | [-2, 2] | Repetition penalty |
| `presence_penalty` | [-2, 2] | Topic novelty |
| `repetition_penalty` | (0, 2] | Token repetition |
| `seed` | integer | Deterministic output |
| `stop` | string/array | Stop sequences |
| `stream` | boolean | SSE streaming |
| `response_format` | object | Structured outputs |
| `tools` | array | Function calling |
| `plugins` | array | Web, PDF, etc. |

### Features

#### Structured Outputs

```json
{
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "weather",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "temperature": {"type": "number"},
          "conditions": {"type": "string"}
        },
        "required": ["temperature", "conditions"]
      }
    }
  }
}
```

#### Plugins

```json
{
  "plugins": [
    {"id": "web"},
    {"id": "response-healing"},
    {"id": "file-parser"},
    {"id": "context-compression"}
  ]
}
```

#### Tool Calling

Passes `tools` array to providers. OpenRouter transforms tools for non-OpenAI interfaces.

---

## MODEL ROUTING

### Route Parameter

```json
{"route": "fallback"}
```

Automatically tries alternative models on failure.

### Provider Preferences

```json
{
  "provider": {
    "require_parameters": true,
    "order": ["Anthropic", "OpenAI"]
  }
}
```

### Body Builder

Model: `openrouter/bodybuilder`

Transforms natural language into multi-model request bodies:

```json
// Generate parallel requests
{
  "model": "openrouter/bodybuilder",
  "messages": [{"role": "user", "content": "Count to 10 using Claude and GPT-5"}]
}

// Returns:
{
  "requests": [
    {"model": "anthropic/claude-sonnet-4.5", "messages": [...]},
    {"model": "openai/gpt-5.1", "messages": [...]}
  ]
}
```

---

## RESPONSE FORMAT

### Normalized Schema

```json
{
  "id": "gen-xxxxx",
  "choices": [{
    "finish_reason": "stop",
    "native_finish_reason": "stop",
    "message": {
      "role": "assistant",
      "content": "Hello!"
    }
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 4,
    "total_tokens": 14,
    "prompt_tokens_details": {
      "cached_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0
    },
    "cost": 0.00014
  },
  "model": "openai/gpt-4o"
}
```

### Finish Reasons (Normalized)

- `tool_calls` — Model requested tool execution
- `stop` — Normal stop
- `length` — Hit token limit
- `content_filter` — Content filtered
- `error` — Error occurred

---

## SDKS

### Official SDKs

| Language | Package |
|----------|---------|
| TypeScript/JS | `@openrouter/sdk` |
| Python | `openrouter` |

### OpenAI SDK Compatibility

OpenRouter works as drop-in replacement:

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: '<OPENROUTER_API_KEY>',
});
```

---

## HERMES INTEGRATION

### Current Config (Updated)

```yaml
model:
  provider: ollama-local
  default: qwen3.5:latest

providers:
  ollama-local:
    api: http://127.0.0.1:11434/v1
    default_model: qwen3.5:latest
    models: [qwen3.5:latest, phi3:mini, qwen2.5:3b, devstral, codestral, mistral-large]
  
  openrouter-free:
    api: https://openrouter.ai/api/v1
    default_model: meta-llama/llama-3.2-3b-instruct:free
    models: [meta-llama/llama-3.2-3b-instruct:free, nvidia/nemotron-3-super-120b-a12b:free]

fallback_providers: [ollama-light, openrouter-free]
```

### OpenRouter ENV Variable

```
OPENROUTER_API_KEY=sk-or-v1-xxx  # Set in ~/.hermes/.env
```

---

## USE CASES

| Use Case | Recommended Model |
|----------|-------------------|
| Code generation | `openrouter/free` or NVIDIA Nemotron |
| Reasoning | DeepSeek R1, Gemini |
| General chat | Llama 3.2, GPT-4o-mini (paid) |
| Vision/multimodal | Gemma, Claude (paid) |
| Free experimentation | `openrouter/free` router |

---

## RESOURCES & LINKS

| Resource | URL |
|----------|-----|
| Docs | openrouter.ai/docs |
| API Reference | openrouter.ai/docs/api/reference |
| Models | openrouter.ai/models |
| Free Models | openrouter.ai/collections/free-models |
| Pricing | openrouter.ai/pricing |
| Status | openrouter.ai/status |

---

## NOTES

- OpenRouter does NOT mark up provider pricing
- Failed/fallback attempts are NOT billed
- Zero Completion Insurance — only successful runs charged
- Prompt caching supported for cost reduction
- BYOK (Bring Your Own Key) available with 1M free req/month

---

*Research conducted via Hermes Agent session — April 28, 2026*
