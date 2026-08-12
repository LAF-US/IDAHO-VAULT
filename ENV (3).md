# Runtime Environment Scaffold

This repo tracks runtime shape, not local runtime contents.

Tracked scaffold:

- `.env.example` documents safe local defaults.
- `.venv/.gitkeep` preserves the repo-local Python environment directory.
- `.cache/.gitkeep`, `.state/.gitkeep`, `.tmp/.gitkeep`, and `.agent-home/.gitkeep` preserve vault-local runtime containment directories.
- `.crewai/logs/.gitkeep` preserves the CrewAI log directory.
- `.op/openrouter.env.template` documents the OpenRouter/1Password env-file shape.

Local-only files:

- `.env`
- `.env.*` except tracked examples/templates
- `.op/*.env` except tracked examples/templates
- all installed packages and generated files inside `.venv/`
- all generated cache, state, temp, log, and agent-home contents

Setup pattern:

```bash
cp .env.example .env
cp .op/openrouter.env.template .op/openrouter.env
uv venv .venv
uv sync
```

Keep real API keys out of tracked files. Prefer `op://...` 1Password references in `.op/openrouter.env`.
