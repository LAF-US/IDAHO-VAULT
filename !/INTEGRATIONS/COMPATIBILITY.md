# Runtime Compatibility Matrix

This is the canonical Round 1 runtime/provider compatibility snapshot.

## Local Runtime Surfaces

| Surface | Status | Detail |
| --- | --- | --- |
| OpenClaw config `.openclaw-local-only.yml` | `OK` | .openclaw-local-only.yml present |
| OpenClaw config `.openclaw-local-mesh.yml` | `OK` | .openclaw-local-mesh.yml present |
| Documented script `health_monitor.py` | `OK` | scripts\health_monitor.py present |
| Documented script `validate_openrouter.py` | `OK` | scripts\validate_openrouter.py present |
| Documented script `validate_services.py` | `OK` | scripts\validate_services.py present |

## OpenRouter Contract

| Check | Status | Severity | Detail |
| --- | --- | --- | --- |
| Resolver (Python) | `OK` | `error` | !\resolve_openrouter_secret.py present |
| Resolver (PowerShell) | `OK` | `error` | !\resolve-openrouter-secret.ps1 present |
| Runtime launcher | `OK` | `error` | scripts\openrouter_runtime.py present |
| Launcher `Start-CodexOpenRouter.ps1` | `OK` | `error` | scripts\Start-CodexOpenRouter.ps1 present |
| Launcher `Start-ClaudeOpenRouter.ps1` | `OK` | `error` | scripts\Start-ClaudeOpenRouter.ps1 present |
| Launcher `launch-codex-openrouter.cmd` | `OK` | `error` | !\launch-codex-openrouter.cmd present |
| Launcher `launch-claude-openrouter.cmd` | `OK` | `error` | !\launch-claude-openrouter.cmd present |
| OpenRouter env file | `OK` | `error` | .op\openrouter.env present |
| 1Password CLI | `FAIL` | `warn` | `op` is installed but not signed in; env-file fallback is required. |
| Env key `OPENROUTER_API_KEY` | `OK` | `error` | OpenRouter API key ref/value present |
| Env key `OPENAI_API_KEY` | `OK` | `error` | OpenAI compatibility key ref/value present |
| Env key `OPENAI_BASE_URL` | `OK` | `error` | OpenAI compatibility base URL present |
| Env key `ANTHROPIC_AUTH_TOKEN` | `OK` | `error` | Anthropic compatibility auth token ref/value present |
| Env key `ANTHROPIC_BASE_URL` | `OK` | `error` | Anthropic compatibility base URL present |
| Env key `ANTHROPIC_API_KEY` | `OK` | `error` | Anthropic compatibility API key ref/value present |
| OpenAI base URL | `OK` | `error` | expected `https://openrouter.ai/api/v1`, got `https://openrouter.ai/api/v1` |
| Anthropic base URL | `OK` | `error` | expected `https://openrouter.ai/api`, got `https://openrouter.ai/api` |
| Secret style `OPENROUTER_API_KEY` | `OK` | `info` | uses a 1Password item reference. |
| Secret style `OPENAI_API_KEY` | `OK` | `info` | uses a 1Password item reference. |
| Secret style `ANTHROPIC_AUTH_TOKEN` | `OK` | `info` | uses a 1Password item reference. |
| Secret style `ANTHROPIC_API_KEY` | `OK` | `info` | uses a 1Password item reference. |

## Scope Notes

- `op://...` references are the preferred local secret format for `.op/openrouter.env`.
- 1Password SSH agent guidance is separate and limited to local developer-machine SSH and git workflows.
- Network/provider reachability is checked separately by `scripts/health_monitor.py`.
