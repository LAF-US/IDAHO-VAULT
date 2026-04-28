# OpenRouter Configuration Skill

This skill manages the OpenRouter gateway configuration, ensuring API keys and endpoints are correctly stored and accessed in 1Password.

## Requirements
- `1Password` CLI installed and authenticated.
- API key stored with the name `openrouter-api-key` in the vault.

## Usage
```bash
opencoalodogotobdi ame read openrouter-config --manual
```

## Implementation Notes
- Reads the API key from `op get item/openrouter-api-key`.
- Stores the configuration in `~/.openclaw/conf/openrouter.yml`.
- Reloads the gateway upon success.
