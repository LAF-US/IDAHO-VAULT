---
authority: LOGAN
created: 2026-05-17
tags: [openclaw, models, routing, infrastructure, beefstack]
related:
  - OPENROUTER-CROSS-PLATFORM.md
  - .openclaw/openclaw.json
---

# BEEFSTACK — Model Routing Architecture

**Principle:** Redundancy on redundancy on redundancy. Belts and suspenders and a third thing.

The BEEFSTACK is the live model routing configuration for the OpenClaw gateway on `logan-zbfury` (Windows / ZBFURY). It governs which language model handles any given agentic request — local-first, Mistral-first, with independent cloud fallback legs so no single provider outage kills the Device.

---

## Provider Preference Rankings

Logan's canonical agentic LLM provider rankings, in order of preference:

| Rank | Provider(s) | Notes |
|------|-------------|-------|
| 1 | **Mistral** | Primary preference. Best local model coverage via Ollama. |
| 2 | **Claude** (Anthropic) / **ChatGPT·Codex** (OpenAI) | Tied. Both tier-1 cloud providers. |
| 3 | **Perplexity** / **Grok** (xAI) | Tied. Search-augmented and frontier tiers. |
| 4 | **Meta / Llama** | Strong local fallback via Ollama (llama3.2-vision). |
| 5 | **Proton / Lumo** | Privacy-first providers. |
| 6 | **Kimi** (Moonshot) / **DeepSeek** | Tied. Capable alternatives. |
| 7 | **Copilot** (Microsoft) | Last resort cloud option. |
| — | ~~Gemini / Gemma~~ | **BANNED** |
| — | ~~Phi / Pi~~ | **BANNED** |
| — | ~~Qwen / Qwen~~ | **BANNED** |

**Governing principles:**
- Prefer local models when possible — data stays on-device, no retention, no tracking
- Robust cloud fallbacks required for resilience
- Control over data retention and tracking takes priority over convenience
- Banned providers are excluded from all config, catalogs, and fallback chains
- All config and tooling must be portable across macOS, Windows, and Linux

---

## The Three-Legged Stool

The BEEFSTACK routes through three independent legs. If Leg 1 fails completely, Leg 2 catches it. If Leg 2 fails, Leg 3 catches it. Deep local anchors sit beneath all three as the floor.

```
PRIMARY ──────────────────────────────────────────────────────────
  ollama/magistral:latest              Local Mistral reasoning model

LEG 1 — LOCAL OLLAMA (Mistral-first) ────────────────────────────
  ollama/devstral:latest               Local Mistral coding model
  ollama/mistral-small:latest          Local Mistral fast/light
  ollama/mistral-nemo:latest           Local Mistral efficient
  ollama/mistral:latest                Local Mistral base

LEG 2 — MISTRAL API DIRECT ──────────────────────────────────────
  mistral/magistral-small              Mistral cloud reasoning
  mistral/devstral-medium-latest       Mistral cloud coding
  mistral/codestral-latest             Mistral cloud code-specialist
  mistral/mistral-large-latest         Mistral cloud heavyweight

LEG 3a — CLAUDE (dual-route) ────────────────────────────────────
  anthropic/claude-sonnet-4-6          Direct Anthropic API
  openrouter/anthropic/claude-sonnet-4-6  Claude via OpenRouter

LEG 3b — GPT-5 / CODEX (three tiers) ───────────────────────────
  codex/gpt-5.5                        Codex GPT-5 flagship
  codex/gpt-5.2                        Codex GPT-5 stable
  codex/gpt-5.4-mini                   Codex GPT-5 light

LEG 3c — MISTRAL VIA OPENROUTER (third route to Mistral) ────────
  openrouter/mistralai/mistral-large-2411
  openrouter/mistralai/mistral-small-2603

DEEP LOCAL ANCHORS (offline floor) ──────────────────────────────
  ollama/mixtral:latest                26GB local MoE
  ollama/mistral-large:latest          73GB local anchor
```

**Fallback count:** 17 models across 3 independent cloud legs + local floor.

**Mistral redundancy:** Reachable 4 independent ways (Ollama local → Mistral API direct → OpenRouter → deep Ollama).

**Claude redundancy:** Reachable 2 independent ways (direct Anthropic API + OpenRouter).

---

## Why This Shape

- **Local-first** keeps sensitive vault work off cloud logs by default
- **Mistral at primary + legs 1 & 2** honors provider ranking without sacrificing resilience
- **Dual-route Claude** means Anthropic API outage ≠ Claude outage
- **Three Codex tiers** give cost/capability flex within the GPT-5 family
- **Third Mistral route via OpenRouter** means Leg 3c independently reaches Mistral even if Leg 2 (direct API) is down
- **73GB local anchor** is the last line — no internet required, no provider dependency

---

## Banned Model Hygiene

The following are excluded from all openclaw config, model catalogs, and fallback chains:

- **Gemini / Gemma** (Google) — banned
- **Phi / Pi** (Microsoft / Inflection) — banned
- **Qwen / Qwen** (Alibaba) — banned

If an openclaw update re-introduces any of these as defaults, remove them manually and restart the gateway.

---

## Live Config Location

Config path is OS-agnostic — `openclaw` resolves `~/.openclaw/` correctly on macOS, Windows, and Linux:

```
~/.openclaw/openclaw.json  →  agents.defaults.model
```

All model IDs in the BEEFSTACK use provider-prefixed strings (`ollama/`, `mistral/`, `openrouter/`, `codex/`, `anthropic/`) that are resolved by the OpenClaw gateway — no OS-specific paths in the model chain itself.

To inspect the live stack (any OS):
```bash
openclaw models list
```

To validate after any edit (any OS):
```bash
openclaw config validate
openclaw gateway restart
openclaw gateway health
```

**Gateway service name varies by OS:**

| OS | Service mechanism |
|----|-------------------|
| macOS | launchd (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`) |
| Windows | Startup folder login item (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw Gateway.cmd`) |
| Linux | systemd (`openclaw-gateway.service`) |

`openclaw gateway install` / `restart` / `stop` abstracts over all three — prefer the CLI over touching service files directly.

---

## Installed Local Models (as of 2026-05-17)

Ollama models are portable — `ollama pull <model>` works identically on macOS, Windows, and Linux. The model store lives in `~/.ollama/models/` on all platforms.

| Model | Size | Status |
|-------|------|--------|
| ollama/magistral:latest | 14 GB | PRIMARY |
| ollama/devstral:latest | 14 GB | Leg 1 |
| ollama/mistral-small:latest | 14 GB | Leg 1 |
| ollama/mistral-nemo:latest | 7.1 GB | Leg 1 |
| ollama/mistral:latest | 4.4 GB | Leg 1 |
| ollama/mixtral:latest | 26 GB | Deep anchor |
| ollama/mistral-large:latest | 73 GB | Deep anchor |
| ollama/gpt-oss:latest | 13 GB | Unverified — not in stack |
| ollama/nemotron:latest | 42 GB | Unverified — not in stack |
| ollama/llama3.2-vision:90b | 54 GB | Meta tier 4 — not in stack |
| ~~ollama/qwen:latest~~ | 2.3 GB | **BANNED** — do not use |

`gpt-oss`, `nemotron`, and `llama3.2-vision` are installed but not yet validated for agentic use. Logan to decide whether to slot them in after testing.

To replicate the local model stack on a new machine:
```bash
ollama pull magistral
ollama pull devstral
ollama pull mistral-small
ollama pull mistral-nemo
ollama pull mistral
ollama pull mixtral
ollama pull mistral-large
```
