# Service Compatibility Validator Skill

This skill validates external service compatibility with the vault’s current configuration and dependencies.

## Checks Performed
- API version compatibility (e.g., OpenRouter API v1)
- Python package compatibility (e.g., `requests-oauthlib` vs `authlib`)
- Operating system compatibility (macOS 12.7.6 constraints)
- Network access (firewall, proxy settings)

## Usage
```bash
# Validate OpenRouter API compatibility
python3 scripts/validate_openrouter.py

# Check all services
python3 scripts/validate_services.py
```

## Notes
- Run before adding new external integrations.
- Document compatibility matrix in `!/INTEGRATIONS/COMPATIBILITY.md`.
- Flag deprecated APIs for replacement.
