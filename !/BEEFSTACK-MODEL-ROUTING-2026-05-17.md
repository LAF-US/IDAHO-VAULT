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
| ------ | ------------- | ------- |
| 1 | **Mistral** / **Claude** (Anthropic) | Top preferred voices/providers. |
| 2 | **ChatGPT·Codex** (OpenAI) | Preferred coding/frontier fallback after Mistral/Claude. |
| 3 | **Grok** (xAI) / **Perplexity** | Frontier alternate plus search-augmented research lane. |
| 4 | **Meta·Llama** | Strong local/open model family. |
| 5 | **Proton / Lumo** | Privacy-first providers. |
| 6 | **Moonshot·Kimi** / **DeepSeek** | Capable alternatives. |
| 7 | **Microsoft Copilot** / **GitHub Copilot** | Last-resort Microsoft/GitHub lane. |
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
  Must distinguish shared OpenRouter capacity from BYOK provider lanes

LEG 3 — OPENCODE ────────────────────────────────────────────────
  Coding and agent execution interface
  Complex implementation workflows
  Uses configured local/cloud providers without making one provider the whole stack
```

The stool should be portable across macOS, Windows, and Linux. Individual model availability may differ by machine, but the routing principle stays stable.

## OpenRouter Is Not One Lane

OpenRouter is the cloud routing leg, but it is not a single uniform failure domain. It can carry several distinct lanes:

| Lane | Meaning | Failure mode |
| ------ | --------- | -------------- |
| OpenRouter shared capacity | OpenRouter-hosted provider access billed through OpenRouter. | OpenRouter credit, workspace, or shared-provider routing limits. |
| OpenRouter BYOK | OpenRouter request brokered through Logan's own provider key. | The upstream provider key's rate limits, spend limits, or provider policy. |
| Direct provider API | Hermes/OpenCode/etc. call Mistral, Anthropic, OpenAI, or another provider without OpenRouter. | That provider key's direct limit, independent of OpenRouter transport. |

This distinction matters. A route like `openrouter/mistralai/mistral-medium-3-5` can fail because the selected OpenRouter route is using Mistral BYOK, not because the OpenRouter runtime key itself is capped. A direct Mistral fallback may then fail with the same upstream Mistral `429` because it shares the same provider-side limit.

Recent evidence:

- OpenRouter returned `429 Provider returned error` for `mistralai/mistral-medium-3-5`.
- The error metadata identified `provider_name: Mistral` and `is_byok: True`.
- Direct Mistral fallback returned the same `429 Rate limit exceeded` / provider code `1300`.
- A later OpenRouter Mistral Small route succeeded, showing that the whole OpenRouter account was not necessarily blocked.

Therefore BEEFSTACK fallback design must diversify by **provider bucket**, not just by model name or preferred family. If the first failure is Mistral BYOK, the next automatic fallback should usually jump to another bucket, such as non-BYOK OpenRouter capacity, Claude, OpenAI/Codex, or local Ollama, before retrying another route that uses the same exhausted Mistral provider key.

## Dual-Modal Capabilities Across the Stack

Each BEEFSTACK leg possesses dual operational modes that create an even richer redundancy mesh:

- **Ollama**: Can operate both **Local** (on-device) and **Cloud** (remote instances via `OLLAMA_HOST`)
- **OpenRouter**: Can operate both **Routed** (shared capacity) and **Direct/BYOK** (using personal provider keys)  
- **OpenCode**: Can operate both **Routed** (via intermediaries like OpenRouter) and **Direct** (provider API calls)
- **Provider Access**: Can be both **Shared** (platform-managed) and **Dedicated** (personal keys/endpoints)

This means true redundancy exists not just between the three legs, but within each leg's operational modes. A failure in one mode (e.g., OpenRouter Routed due to shared capacity limits) can often be bypassed by switching to another mode of the same leg (e.g., OpenRouter Direct/BYOK or Direct Provider API) without changing the fundamental leg.

The most resilient configurations leverage orthogonal combinations - for example, using OpenCode Direct Provider API calls when both OpenRouter modes are experiencing issues, or using Ollama Cloud instances when local Ollama is unavailable but remote devices are accessible.

Understanding these dual capabilities allows for more sophisticated fallback strategies that don't just swap between legs, but can switch operational modes within the same leg to maintain continuity when specific pathways encounter issues.

## Preference Stack on Top

The current model-family preference stack is:

```
1. Mistral / Claude
2. ChatGPT-Codex
3. Grok / Perplexity
4. Meta-Llama
5. Proton-Lumo
6. Moonshot-Kimi / DeepSeek
7. Microsoft-Copilot / GitHub-Copilot
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
  Prefer Mistral/Claude, then ChatGPT-Codex, subject to tool-call support,
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

**BYOK-aware fallback rule:** after a provider-specific BYOK `429`, do not immediately retry the same upstream provider through a different wrapper unless the caller knows the next route uses a different capacity pool. Treat `OpenRouter -> Mistral BYOK` and `Direct Mistral` as potentially the same rate-limit bucket.

**Router-aware fallback rule:** after an OpenRouter account/workspace/key failure, direct provider calls can be a useful escape route. After an upstream provider failure, another OpenRouter route with a different provider can be the escape route.

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

## OpenRouter Management Key

Hermes additionally has access to the **OpenRouter Management Key** for admin operations: creating/revoking sub-keys, setting credit limits, viewing usage across all keys. This key **cannot** be used for inference.

| Purpose | Env var | 1Password ref | Item title |
|---------|---------|---------------|------------|
| Inference (Swarm Router Key) | `OPENROUTER_API_KEY` | `op://Vault/OpenRouter API Key/credential` | OpenRouter API Key |
| Admin (Management Key) | `OPENROUTER_MANAGEMENT_KEY` | `op://Vault/OpenRouter Key/credential` | OpenRouter Key |

The Management Key reference lives in `.op/openrouter.env` alongside the inference key. On the Mac, Hermes reads it from `~/.hermes/.env` after sync. Use `OPENROUTER_MANAGEMENT_KEY` for OpenRouter admin API calls (e.g., `GET https://openrouter.ai/api/v1/admin/...`), not for `/v1/chat/completions`.

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

- Universal doctrine: local-first remains the desired system posture.
- MacBook operational override: primary is `openrouter` / `mistralai/mistral-medium-3-5` because this hardware has repeatedly hung on local `devstral:latest` calls.
- Fallback chain as of 2026-05-21:
  - `openrouter` / `mistralai/mistral-small-2603`
  - `openrouter` / `anthropic/claude-haiku-4.5`
  - `openrouter` / `anthropic/claude-sonnet-4.6`
  - `openrouter` / `openai/gpt-5.3-codex`
  - `custom` / `mistral-small-2603` via direct Mistral API
  - `openrouter` / `mistralai/mistral-large-2512`
- `OPENROUTER_API_KEY` is present in `~/.hermes/.env`; keep the source of truth in the vault's `.op/openrouter.env` / 1Password path.
- Local Ollama remains a preferred doctrine and an explicit/manual contingency, but this MacBook should not pretend local inference is the reliable live default.
- Gemini is allowed for TTS / Google infrastructure only. It is not part of the agentic LLM fallback chain.
- BYOK caveat: when OpenRouter reports `is_byok: true` and a provider-specific `429`, Hermes should prefer a fallback in a different provider bucket instead of immediately retrying the same provider through a direct API route.
- Direct Mistral remains configured, but it is now late in the chain as an OpenRouter transport/account contingency rather than the immediate fallback after a Mistral BYOK rate limit.

**OpenCode**

- OpenCode is the third leg as a coding/agent execution interface.
- Do not configure Hermes to call `http://127.0.0.1:3000/v1` as an OpenCode model endpoint unless an actual `opencode serve` OpenAI-compatible endpoint is running there.
- On the MacBook, port `3000` is currently used by the Hermes WhatsApp bridge, so it must not be treated as an OpenCode LLM provider.
- OpenCode has its own provider credential store and can use both OpenRouter and direct provider keys. Treat those as separate routing surfaces but not automatically separate rate-limit buckets if they point at the same BYOK upstream provider.

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
| ---- | ------------------- |
| macOS | launchd (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`) |
| Windows | Startup folder login item (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\OpenClaw Gateway.cmd`) |
| Linux | systemd (`openclaw-gateway.service`) |

`openclaw gateway install` / `restart` / `stop` abstracts over all three — prefer the CLI over touching service files directly.

---

## Local Model Catalog

Ollama models are portable — `ollama pull <model>` works identically on macOS, Windows, and Linux. The model store lives in `~/.ollama/models/` on all platforms.

The table below is the desired portable BEEFSTACK catalog, not a guarantee that every machine currently has every model installed.

| Model | Size | Status |
| ------- | ------ | -------- |
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
| ------- | -------- |
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
