# OpenRouter Cross-Platform Setup

## Model IDs (OpenRouter format)
Use `mistralai/` prefix, not `mistral/`:
- `mistralai/mistral-small-2603` (free, current)
- `mistralai/mistral-large-2411` (paid)
- `anthropic/claude-3.5-haiku` (free)

## Environment Setup

### Mac (launchd)
Add to `~/Library/LaunchAgents/ai.openclaw.gateway.plist`:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>OPENROUTER_API_KEY</key>
    <string>sk-or-v1-...</string>
</dict>
```

### Windows (Task Scheduler)
Set as system environment variable or in task definition.

## Config (works both platforms)
```json
{
  "models": {
    "providers": {
      "openrouter": {
        "apiKey": "env:OPENROUTER_API_KEY",
        "models": [
          {"id": "mistralai/mistral-small-latest"},
          {"id": "anthropic/claude-3.5-haiku"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {"primary": "mistralai/mistral-small-latest"}
    }
  }
}
```

## Get API Key
1. OpenRouter.ai → Account → API Keys
2. Or fetch from 1Password vault