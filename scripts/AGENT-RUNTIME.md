# Agent Runtime Containment

These launchers keep agent temp/cache state inside the vault instead of spraying
artifacts into user-level folders.

## Shared local runtime paths

- `.tmp/`
- `.uv-cache/`
- `.pip-cache/`
- `.npm-cache/`
- `.cache/`
- `.state/`
- `.pycache/`
- `.agent-home/`

## Launchers

Use these from the vault root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Start-CodexVault.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\Start-ClaudeVault.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\Start-GeminiVault.ps1
```

Arguments after the script name are passed through to the agent CLI.

Examples:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\Start-CodexVault.ps1 --help
powershell -ExecutionPolicy Bypass -File .\scripts\Start-GeminiVault.ps1 -m gemini-2.5-pro
```

## Notes

- `codex` uses `CODEX_HOME=.agent-home/codex/`.
- `gemini` is launched with an isolated vault-local home under `.agent-home/gemini/`
  because its upstream CLI keeps global state in `~/.gemini/`.
- `claude` gets vault-local temp/cache directories by default. If you later want
  full home isolation for Claude too, use `Use-VaultAgentEnv.ps1 -Agent claude -IsolateHome`.
- The former CrewAI launcher and CrewAI-specific bootstrap preflight were retired with the experimental runtime; this guide documents only active containment launchers.
