# Runtime Environment Scaffold

This repo tracks runtime shape, not local runtime contents.

Tracked scaffold:

- `.env.example` documents safe local defaults.
- `.venv/.gitkeep` preserves the repo-local Python environment directory.
- `.cache/.gitkeep`, `.state/.gitkeep`, `.tmp/.gitkeep`, and `.agent-home/.gitkeep` preserve vault-local runtime containment directories.
- `.op/openrouter.env.template` documents the OpenRouter/1Password env-file shape.

Local-only files:

- `.env`
- `.env.*` except tracked examples/templates
- `.op/*.env` except tracked examples/templates
- all installed packages and generated files inside `.venv/`
- all generated cache, state, temp, log, and agent-home contents

## Dependency contract

`pyproject.toml` declares the project’s direct Python requirements. **`uv.lock` is the canonical resolved dependency graph** for the supported Python versions. `requirements.txt` is a compatibility export produced from `uv.lock`; it is not a separate dependency authority and should not be hand-edited or resolved independently.

The standard local bootstrap is therefore `uv sync`, which creates or synchronizes the local environment from the project metadata and `uv.lock`. A pip installation from `requirements.txt` is available only where a pip-compatible export is required.

```bash
cp .env.example .env
cp .op/openrouter.env.template .op/openrouter.env
uv venv .venv
uv sync
```

The scheduled dependency workflow runs `uv lock --upgrade`, then regenerates `requirements.txt` with `uv export`. It opens a review PR when either artifact changes. Dependabot maintains GitHub Actions and Git submodule pins every other Thursday at noon America/Denver; a submodule PR advances only its gitlink and does not replace a vendored reference snapshot. Review and branch protections remain the authority for accepting any proposed update.

Keep real API keys out of tracked files. Prefer `op://...` 1Password references in `.op/openrouter.env`.
