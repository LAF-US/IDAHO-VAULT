# OpenRouter Cross-Platform Setup

## Model IDs (OpenRouter format)
Use `mistralai/` prefix, not `mistral/`:
- `mistralai/mistral-small-2603` (free, current)
- `mistralai/mistral-large-2411` (paid)
- `openai/gpt-4o-mini` (free)
- `anthropic/claude-3.5-haiku` (free)

## Environment Setup

### Mac (launchd)
Add to `~/Library/LaunchAgents/ai.openclaw.gateway.plist`:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>OPENROUTER_API_KEY</key>
    <string>op://Vault/OpenRouter API Key/credential</string>
</dict>
```

### Windows (Task Scheduler)
Prefer generating `.op/openrouter.env` with the vault resolver and loading it at
launch time rather than duplicating raw secrets into scheduler settings.

## Canonical Local Runtime Path

```bash
python3 !/resolve_openrouter_secret.py
python3 scripts/validate_openrouter.py
python3 scripts/validate_services.py --write-matrix
```

- `op://...` references are the preferred local secret format.
- `!/resolve_openrouter_secret.py` and `!/resolve-openrouter-secret.ps1` render
  the env contract for Codex and Claude launchers.
- `scripts/validate_openrouter.py` verifies the provider contract.
- `scripts/validate_services.py` writes the canonical compatibility snapshot to
  `!/INTEGRATIONS/COMPATIBILITY.md`.
- The runtime and launch wrappers normalize `OPENROUTER_API_KEY` /
  `OPENAI_API_KEY` and `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY` so one
  env file can survive different OS-machine conventions.

## Config (works both platforms)
```json
{
  "models": {
    "providers": {
      "openrouter": {
        "apiKey": "env:OPENROUTER_API_KEY",
        "baseUrl": "https://openrouter.ai/api/v1",
        "models": [
          {"id": "openai/gpt-4o-mini"},
          {"id": "anthropic/claude-3.5-haiku"},
          {"id": "mistralai/mistral-large-2411"},
          {"id": "mistralai/mistral-small-2603"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {"primary": "openrouter/openai/gpt-4o-mini"}
    }
  }
}
```

## Get API Key
1. OpenRouter.ai → Account → API Keys
2. Store it in 1Password and resolve it through the vault runtime scripts
