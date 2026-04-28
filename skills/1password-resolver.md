# 1Password API Key Resolver Skill

This skill resolves API keys from 1Password CLI for external services used in the vault.

## Requirements
- 1Password CLI installed and authenticated.
- API keys stored in 1Password vault with consistent naming.

## Supported Services
- `openrouter-api-key`
- `linear-api-key`
- `slack-webhook-url`
- `github-token`

## Usage
```bash
# Resolve key for a service
op get item openrouter-api-key --fields password

# Example in Python
import subprocess
key = subprocess.getoutput("op get item openrouter-api-key --fields password")
```

## Notes
- Keys are never hardcoded in scripts.
- All external API calls should use this resolver.
- Validate key exists before attempting API calls.
