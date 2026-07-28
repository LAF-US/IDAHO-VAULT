# 1Password Runtime Resolver Reference

This note maps 1Password-backed runtime secret resolution to the live vault
scripts. It is reference guidance, not the executable implementation.

## Requirements
- 1Password CLI installed and authenticated.
- API keys stored in 1Password vault with consistent naming.

## Canonical runtime path
- `!/resolve_openrouter_secret.py`
- `!/resolve-openrouter-secret.ps1`
- `.op/openrouter.env`
- `scripts/validate_openrouter.py`

## Usage
```bash
python3 !/resolve_openrouter_secret.py
pwsh -File !/resolve-openrouter-secret.ps1
python3 scripts/validate_openrouter.py
```

## Notes
- Runtime provider secrets should resolve through the vault scripts above.
- Prefer `op://...` references in `.op/openrouter.env` over plaintext values.
- The harvested 1Password SSH agent docs are a separate local machine workflow
  for SSH and Git signing, not the provider runtime secret path.
