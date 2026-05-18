---
authority: LOGAN
created: 2026-05-17
tags: [openclaw, models, routing, infrastructure, beefstack]
related:
  - OPENROUTER-CROSS-PLATFORM.md
  - .openclaw/openclaw.json
---

# BEEFSTACK — Model Routing Preferences and Redundancy Architecture

**Principle:** Redundancy on redundancy on redundancy. Belts and suspenders and a third thing.

The BEEFSTACK is Logan's stated model-calling preference architecture. It is not a Windows-only configuration, and `logan-zbfury` was only the first machine where the stack was documented and exercised.

The stool has three legs:

1. **Ollama** — local-first model calls and privacy floor.
2. **OpenRouter** — broad cloud routing, fallback breadth, and provider resilience.
3. **OpenCode** — coding/agent execution interface for complex implementation work.

The provider preferences sit on top of that stool. The goal is to keep work moving when weak local hardware chokes on a local model, when a cloud provider hits rate limits, or when an API/provider path fails. Redundancy is the design, not an incidental convenience.

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
| — | ~~Gemini~~ | **BANNED** for agentic LLM routing |
| — | Phi / Qwen / Gemma | Disliked; exclude from defaults and fallbacks unless Logan explicitly overrides |

**Governing principles:**
- Prefer local models when possible — data stays on-device, no retention, no tracking
- Robust cloud fallbacks required for resilience
- Control over data retention and tracking takes priority over convenience
- Banned providers are excluded from all config, catalogs, and fallback chains
- Disliked model families are excluded from defaults and fallback chains unless Logan explicitly overrides
- All config and tooling must be portable across macOS, Windows, and Linux

---

## The Three-Legged Stool

The BEEFSTACK rests on three independent tool/runtime legs. Preferences and model families are stacked above those legs.

```
LEG 1 — OLLAMA ──────────────────────────────────────────────────
  Local-first calls
  Simple/private/offline work
  Mistral-family local preference where hardware can carry it

LEG 2 — OPENROUTER ──────────────────────────────────────────────
  Cloud fallback breadth
  Mistral / Claude / ChatGPT / other allowed families through one router
  Rate-limit and provider-outage resilience

LEG 3 — OPENCODE ────────────────────────────────────────────────
  Coding and agent execution interface
  Complex implementation workflows
  Uses configured local/cloud providers without making one provider the whole stack
```

The stool should be portable across macOS, Windows, and Linux. Individual model availability may differ by machine, but the routing principle stays stable.

## Preference Stack on Top

The current model-family preference stack is:

```
1. Mistral
2. Claude / ChatGPT-Codex
3. Perplexity / Grok
4. Meta-Llama
5. Proton-Lumo
6. Kimi / DeepSeek
7. Copilot
```

The preference stack is not the stool. Mistral-first means "prefer Mistral when the selected leg can use it safely and reliably," not "make every leg a Mistral-specific route."

## Example Routing Shape

The exact live model list can vary by machine, but the intended shape is:

```
LOCAL FIRST / OLLAMA ────────────────────────────────────────────
  ollama/magistral:latest              Local Mistral reasoning model
  ollama/devstral:latest               Local Mistral coding model
  ollama/mistral-small:latest          Local Mistral fast/light
  ollama/mistral-nemo:latest           Local Mistral efficient
  ollama/mistral:latest                Local Mistral base

CLOUD ROUTING / OPENROUTER ──────────────────────────────────────
  openrouter/mistralai/*               Preferred cloud Mistral route
  openrouter/anthropic/*               Claude fallback route
  openrouter/openai/*                  ChatGPT fallback route
  openrouter/x-ai/*                    Grok fallback route when allowed
  openrouter/meta-llama/*              Llama fallback route when useful

CODING EXECUTION / OPENCODE ─────────────────────────────────────
  OpenCode uses configured providers/models for complex coding tasks.
  Prefer Mistral, then Claude/ChatGPT-Codex, subject to tool-call support,
  rate limits, cost, privacy, and task fit.

DEEP LOCAL ANCHORS ──────────────────────────────────────────────
  ollama/mixtral:latest                26GB local MoE
  ollama/mistral-large:latest          73GB local anchor
```

**Mistral redundancy:** reachable through local Ollama and cloud routing where available.

**Claude / ChatGPT redundancy:** reachable through OpenRouter and coding-agent interfaces where configured.

---

## Why This Shape

- **Local-first** keeps sensitive vault work off cloud logs by default.
- **OpenRouter** prevents one cloud provider, rate limit, or API outage from blocking work.
- **OpenCode** keeps complex coding workflows available as a distinct execution surface.
- **Mistral-first preferences** honor Logan's preferred model family without confusing model families for architecture legs.
- **Cloud fallback** handles weak local hardware, missing local models, slow inference, and memory pressure.
- **Local fallback** handles cloud outages, rate limits, provider errors, and connectivity loss.
- **Deep local anchors** are the last line when internet and provider paths are unavailable.

---

## Banned Model Hygiene

The following is excluded from all OpenClaw and Hermes agentic LLM config, model catalogs, and fallback chains:

- **Gemini** (Google) — banned for agentic LLM routing

The following are disliked and excluded from defaults / fallback chains unless Logan explicitly says otherwise:

- **Phi / Pi** (Microsoft / Inflection)
- **Qwen** (Alibaba)
- **Gemma** (Google)

If an OpenClaw or Hermes update re-introduces banned or disliked families as defaults, remove them manually and restart the gateway/runtime. Installed local models from disliked families are hygiene risks when auto-discovered; keep them unrouted or remove them during model-store cleanup unless Logan explicitly wants them quarantined for comparison.

---

## Live Config Location

Config paths are OS-agnostic where the tools support `~` expansion:

```
~/.openclaw/openclaw.json  →  agents.defaults.model
~/.hermes/config.yaml      →  model + fallback_providers
~/.hermes/.env             →  OPENROUTER_API_KEY for Hermes
```

All model IDs in the BEEFSTACK should use provider-prefixed strings (`ollama/`, `openrouter/`, `opencode/` where supported by the caller, and provider-native IDs beneath OpenRouter) that are resolved by the calling runtime — no OS-specific paths in the model chain itself.

## Runtime Enforcement

As of 2026-05-18, the MacBook runtime contract is:

**OpenClaw**
- Primary: `ollama/devstral:latest`
- Fallbacks:
  - `openrouter/mistralai/mistral-medium-3-5`
  - `openrouter/anthropic/claude-sonnet-4.6`
  - `openrouter/openai/gpt-5.3-codex`
  - `openrouter/mistralai/mistral-large-2512`
- Gateway stays loopback by default: `127.0.0.1:18789`
- Windows-ZBFURY reaches the Mac gateway through an SSH tunnel, not public gateway exposure.

**Hermes Agent**
- Primary: `ollama/devstral:latest`
- Fallback chain:
  - `openrouter` / `mistralai/mistral-medium-3-5`
  - `openrouter` / `anthropic/claude-sonnet-4.6`
  - `openrouter` / `openai/gpt-5.3-codex`
  - `openrouter` / `mistralai/mistral-large-2512`
- `OPENROUTER_API_KEY` is present in `~/.hermes/.env`; keep the source of truth in the vault's `.op/openrouter.env` / 1Password path.
- Gemini is allowed for TTS / Google infrastructure only. It is not part of the agentic LLM fallback chain.

**OpenCode**
- OpenCode is the third leg as a coding/agent execution interface.
- Do not configure Hermes to call `http://127.0.0.1:3000/v1` as an OpenCode model endpoint unless an actual `opencode serve` OpenAI-compatible endpoint is running there.
- On the MacBook, port `3000` is currently used by the Hermes WhatsApp bridge, so it must not be treated as an OpenCode LLM provider.

To inspect the live stack (any OS):
```bash
openclaw models list
hermes fallback list
opencode --version
```

To validate after any edit (any OS):
```bash
openclaw config validate
openclaw gateway restart
openclaw gateway health
hermes config check
hermes doctor
```

**Gateway service name varies by OS:**

| OS | Service mechanism |
|----|-------------------|
| macOS | launchd (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`) |
| Windows | Startup folder login item (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw Gateway.cmd`) |
| Linux | systemd (`openclaw-gateway.service`) |

`openclaw gateway install` / `restart` / `stop` abstracts over all three — prefer the CLI over touching service files directly.

---

## Local Model Catalog

Ollama models are portable — `ollama pull <model>` works identically on macOS, Windows, and Linux. The model store lives in `~/.ollama/models/` on all platforms.

The table below is the desired portable BEEFSTACK catalog, not a guarantee that every machine currently has every model installed.

| Model | Size | Status |
|-------|------|--------|
| ollama/magistral:latest | 14 GB | Preferred local reasoner |
| ollama/devstral:latest | 14 GB | Preferred local coder |
| ollama/mistral-small:latest | 14 GB | Local fast/light |
| ollama/mistral-nemo:latest | 7.1 GB | Local efficient |
| ollama/mistral:latest | 4.4 GB | Local base |
| ollama/mixtral:latest | 26 GB | Deep anchor |
| ollama/mistral-large:latest | 73 GB | Deep anchor |
| ollama/gpt-oss:latest | 13 GB | Unverified — not in stack |
| ollama/nemotron:latest | 42 GB | Unverified — not in stack |
| ollama/llama3.2-vision:90b | 54 GB | Meta tier 4 — not in stack |
| ollama/qwen:latest | 2.3 GB | Disliked — keep unrouted unless Logan explicitly overrides |

`gpt-oss`, `nemotron`, and `llama3.2-vision` are installed but not yet validated for agentic use. Logan to decide whether to slot them in after testing.

MacBook live inventory as of 2026-05-18:

| Model | Status |
|-------|--------|
| `devstral:latest` | Primary local Hermes/OpenClaw route |
| `mistral-large:latest` | Deep local anchor; heavy |
| `codestral:latest` | Mistral-family coding candidate; not currently in fallback chain |
| `phi3:mini` | Disliked; installed but unrouted |
| `qwen3.5:latest` | Disliked; installed but unrouted |
| `qwen2.5:3b` | Disliked; installed but unrouted |

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
