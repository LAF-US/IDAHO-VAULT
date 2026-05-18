---
authority: LOGAN
created: 2026-05-18
tags: [snapshot, beefstack, hermes, openrouter, opencode, macbook, routing]
related:
  - BEEFSTACK-MODEL-ROUTING-2026-05-17.md
  - OPENROUTER-CROSS-PLATFORM.md
  - ../skills/openrouter-config.md
---

# Snapshot - OpenRouter / Hermes / BEEFSTACK State - 2026-05-18

## Executive State

Hermes on the MacBook is not failing because the OpenRouter API key itself is exhausted. The direct OpenRouter key metadata endpoint reports no key-level limit and no remaining-credit cap:

- `limit: null`
- `limit_remaining: null`
- `include_byok_in_limit: false`
- daily/monthly usage present but modest
- key in `~/.hermes/.env` matches the vault `.op/openrouter.env` value

Raw OpenRouter calls outside Hermes still return:

```text
403 Budget limit exceeded (daily limit). Contact your org admin.
```

This points away from Hermes and away from the OpenRouter API key's own budget. Current best read: a provider-side / BYOK / workspace routing budget is being hit underneath OpenRouter, or BYOK routing is preventing fallback to shared OpenRouter capacity.

## Doctrine vs Machine Policy

Universal BEEFSTACK doctrine remains:

1. Local-first where hardware can carry it.
2. OpenRouter for cloud breadth and fallback.
3. OpenCode as the separate coding/agent execution surface.

The MacBook is a machine-specific exception, not a doctrine change. Local `ollama/devstral:latest` repeatedly hangs or times out on this laptop, so Hermes has been configured cloud-first for live messages while preserving local-first as the desired universal posture.

## Current MacBook Hermes Policy

Live Hermes config path:

```text
~/.hermes/config.yaml
```

Current effective Hermes route:

```yaml
model:
  provider: openrouter
  default: mistralai/mistral-medium-3-5
fallback_providers:
  - provider: openrouter
    model: mistralai/mistral-small-2603
  - provider: openrouter
    model: anthropic/claude-sonnet-4.6
  - provider: openrouter
    model: openai/gpt-5.3-codex
  - provider: openrouter
    model: mistralai/mistral-large-2512
```

`hermes status` now reports:

- Model: `mistralai/mistral-medium-3-5`
- Provider: `OpenRouter`
- OpenRouter key present
- Gemini key present for approved TTS / Google infrastructure use only

## Tests Run

### Local Hermes / Ollama

Command shape:

```bash
hermes --provider ollama -m devstral:latest -z "Reply with exactly: HERMES_OLLAMA_TEST_OK" --ignore-rules
```

Result:

- Hung until manually stopped.
- `ollama ps` showed no active model after stop.
- Historical Hermes logs show local custom/Ollama route timeouts:

```text
API call failed after 3 retries. Request timed out. | provider=custom model=devstral:latest
```

Conclusion: local inference on this MacBook is not reliable enough for default live Hermes.

### Hermes via OpenRouter

Command shape:

```bash
hermes chat -q "Reply with exactly: HERMES_MACBOOK_CLOUD_OK" -Q --ignore-rules
```

Result:

- Session created.
- Hermes selected OpenRouter primary.
- Hermes attempted fallbacks in sequence.
- Final failure:

```text
403 Budget limit exceeded (daily limit). Contact your org admin.
```

Conclusion: Hermes is now routing to OpenRouter correctly, but the OpenRouter route is rejected by backend budget/routing state.

### Raw OpenRouter

Raw calls were sent directly to:

```text
https://openrouter.ai/api/v1/chat/completions
```

Mistral test:

```json
{"model":"mistralai/mistral-small-2603","messages":[{"role":"user","content":"Reply with exactly: RAW_OPENROUTER_OK"}],"max_tokens":16}
```

Claude test:

```json
{"model":"anthropic/claude-haiku-4.5","messages":[{"role":"user","content":"Reply with exactly: RAW_CLAUDE_HAIKU_OK"}],"max_tokens":16}
```

Both returned:

```json
{"error":{"message":"Budget limit exceeded (daily limit). Contact your org admin.","code":403}}
```

Conclusion: the 403 is not Hermes-specific.

### OpenRouter Key Metadata

OpenRouter key endpoint:

```text
GET https://openrouter.ai/api/v1/key
```

Reported:

```json
{
  "limit": null,
  "limit_remaining": null,
  "include_byok_in_limit": false,
  "is_free_tier": false,
  "usage_daily": 1.062516,
  "byok_usage_daily": 0.028164
}
```

Conclusion: this API key is not itself capped at the key level.

### OpenCode

`opencode providers list` reports credentials for:

- OpenRouter
- Mistral
- Hugging Face
- GitHub Copilot

Initial `opencode` calls inside sandbox hit a local SQLite checkpoint error. Retesting with normal filesystem permissions reached:

```text
build - mistral-medium-latest
```

but did not return promptly and was stopped.

Conclusion: OpenCode has promising separate credential surfaces, but it was not yet validated as a clean Hermes fallback path in this pass.

## OpenRouter Backend Investigation Targets

Logan is investigating OpenRouter backend state. Highest-value checks:

1. OpenRouter Activity page for the failed requests.
   - Open the failed generation.
   - Inspect raw metadata.
   - Look for `provider_responses`.
   - Confirm which provider endpoint returned the budget limit.

2. OpenRouter BYOK settings.
   - Check Mistral provider key.
   - Check Anthropic provider key.
   - Look for daily/provider/org budget caps.
   - Check whether "Always use for this provider" is enabled.

3. Workspace / org settings.
   - Check any daily budget cap at workspace/org level.
   - Check whether the user/API key is assigned to a project with a daily limit.

4. Routing fallback behavior.
   - OpenRouter BYOK docs say prioritized BYOK keys are tried before shared OpenRouter endpoints.
   - "Always use for this provider" can prevent fallback to shared OpenRouter capacity.
   - BYOK provider ordering can override expected provider/model order.

Relevant OpenRouter docs:

- <https://openrouter.ai/docs/guides/overview/auth/byok>
- <https://openrouter.ai/docs/guides/routing/provider-selection>
- <https://openrouter.ai/docs/api/reference/limits>

## Current Working Hypothesis

The OpenRouter API key is valid and uncapped, but requests are being routed into a provider/BYOK/workspace budget wall. The phrase "Contact your org admin" strongly suggests an org/workspace/provider-account budget constraint rather than a normal OpenRouter credit exhaustion condition.

Likely fixes are in the OpenRouter dashboard, not in Hermes:

- Adjust or remove a BYOK/provider daily budget.
- Disable "Always use for this provider" if shared OpenRouter capacity should be allowed.
- Move the affected BYOK keys from prioritized to fallback if shared capacity should be tried first.
- Add or select a non-capped direct provider route for Hermes if OpenRouter is intentionally budget-restricted.

## Standing Decisions

- Do not change universal BEEFSTACK doctrine from local-first.
- Do treat this MacBook as a hardware exception for live Hermes messaging.
- Do not route agentic LLM calls through Gemini.
- Gemini remains acceptable for TTS / Google infrastructure only.
- Keep OpenClaw Mac/Windows version coherence intact unless Logan directs an update.
- Do not expose OpenClaw publicly; keep loopback plus SSH tunnel posture.

## Follow-Up Once OpenRouter Backend Is Fixed

Run:

```bash
hermes config check
hermes fallback list
hermes chat -q "Reply with exactly: HERMES_MACBOOK_CLOUD_OK" -Q --ignore-rules
```

Then confirm:

- Hermes returns the exact test string.
- No local Ollama hang occurs.
- No `403 Budget limit exceeded` appears in `~/.hermes/logs/errors.log`.
- OpenClaw Windows-ZBFURY pairing remains connected.
