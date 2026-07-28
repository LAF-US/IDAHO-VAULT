# Service Compatibility Validator Reference

This note maps compatibility guidance to the live validation scripts.

## Checks Performed
- API version compatibility (e.g., OpenRouter API v1)
- Python package compatibility (e.g., `requests-oauthlib` vs `authlib`)
- Operating system compatibility (macOS 12.7.6 constraints)
- Network access (firewall, proxy settings)

## Usage
```bash
python3 scripts/validate_openrouter.py
python3 scripts/validate_services.py
python3 scripts/validate_services.py --write-matrix
```

## Notes
- Run before adding new external integrations.
- `scripts/validate_openrouter.py` checks the provider runtime contract.
- `scripts/validate_services.py` checks the broader documented surface and can
  write the compatibility matrix to `!/INTEGRATIONS/COMPATIBILITY.md`.
- Treat this file as a reference note. The live compatibility logic is in the
  Python scripts above.
