# OpenRouter Configuration Reference

This note maps the documented OpenRouter workflow to the live runtime surfaces
in the vault. The executable path lives in the resolver and validation scripts,
not in this markdown file.

## Requirements
- `op` CLI installed and authenticated.
- `openclaw` CLI installed.
- OpenRouter API key stored in 1Password as `op://Vault/OpenRouter API Key/credential`.

## Canonical files
- `.op/openrouter.env`
- `.op/openrouter.env.template`
- `scripts/openrouter_runtime.py`
- `scripts/Use-OpenRouterEnv.ps1`
- `!/resolve_openrouter_secret.py`
- `!/resolve-openrouter-secret.ps1`
- `!/launch-codex-openrouter.cmd`
- `!/launch-claude-openrouter.cmd`
- `~/.openclaw/openclaw.json`
- `~/.hermes/config.yaml`
- `~/.hermes/.env`

## Live commands
```bash
python3 !/resolve_openrouter_secret.py
python3 scripts/validate_openrouter.py
```

## What the runtime path does
- Resolves the OpenRouter secret reference from 1Password.
- Materializes `.op/openrouter.env` for Codex and Claude launchers.
- Prefers `op://...` references instead of plaintext credentials.
- Validates the runtime contract with `scripts/validate_openrouter.py`.
- Keeps OpenClaw aligned to the vault's BEEFSTACK shape: Ollama +
  OpenRouter + OpenCode, with Logan's model-family preferences layered on top.
- Keeps model IDs in OpenRouter format, including the `mistralai/` prefix.

## Current OpenClaw contract
Use these values unless the vault explicitly updates them:

```json
{
  "models": {
    "providers": {
      "ollama": {
        "apiKey": "ollama",
        "baseUrl": "http://127.0.0.1:11434/v1",
        "models": [
          {"id": "devstral"},
          {"id": "mistral-large"}
        ]
      },
      "openrouter": {
        "apiKey": "env:OPENROUTER_API_KEY",
        "baseUrl": "https://openrouter.ai/api/v1",
        "models": [
          {"id": "mistralai/mistral-small-2603"},
          {"id": "anthropic/claude-haiku-4.5"},
          {"id": "mistralai/mistral-medium-3-5"},
          {"id": "mistralai/devstral-2512"},
          {"id": "anthropic/claude-sonnet-4.6"},
          {"id": "openai/gpt-5.3-codex"},
          {"id": "mistralai/mistral-large-2512"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/devstral:latest",
        "fallbacks": [
          "openrouter/mistralai/mistral-medium-3-5",
          "openrouter/anthropic/claude-sonnet-4.6",
          "openrouter/openai/gpt-5.3-codex",
          "openrouter/mistralai/mistral-large-2512"
        ]
      }
    }
  }
}
```

## Current Hermes contract

Hermes should match the same BEEFSTACK posture:

```yaml
model:
  provider: ollama
  default: ollama/devstral:latest
  base_url: http://127.0.0.1:11434/v1
fallback_providers:
  - provider: openrouter
    model: mistralai/mistral-medium-3-5
  - provider: openrouter
    model: anthropic/claude-sonnet-4.6
  - provider: openrouter
    model: openai/gpt-5.3-codex
  - provider: openrouter
    model: mistralai/mistral-large-2512
```

Hermes reads `OPENROUTER_API_KEY` from `~/.hermes/.env`. Keep that value synchronized from the vault's `.op/openrouter.env` source and never paste the secret into notes.

## Operational notes
- Use `gateway.bind = loopback` for local machines unless the vault has a
  documented reason to expose the service beyond localhost.
- Do not hard-code the secret value into the vault. Keep the env file reference
  pointed at 1Password.
- Logan's strongest satisfaction signals to date are Devstral and Mistral;
  treat them as preferred local-first options, not just inherited defaults.
- Keep the standing bias toward free, private, local, and open models when the
  task does not require a remote paid route.
- Google's Gemini is banned for agentic LLM routing. It may remain configured
  only for explicitly approved TTS / Google infrastructure paths.
- Treat `openrouter/` model prefixes as the gateway-level selection path and
  `openai/`, `anthropic/`, and `mistralai/` as provider model IDs.
- The runtime normalizes `OPENROUTER_API_KEY` / `OPENAI_API_KEY` and
  `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` aliases so the same env file
  works across macOS and Windows.
- Do not point Hermes at `http://127.0.0.1:3000/v1` as an OpenCode provider
  unless `opencode serve` is actually running an OpenAI-compatible endpoint
  there. On the MacBook, port `3000` is currently the Hermes WhatsApp bridge.
- Treat this file as reference guidance only. The live automation surface is
  the resolver plus the validation scripts above.
