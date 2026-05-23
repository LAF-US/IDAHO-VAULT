---
title: "Recovery: Hermes Config Reconstruction (Mac)"
date: 2026-05-23
status: active
authority: LOGAN
doc_class: recovery_plan
related:
  - Hermes
  - "COORDINATION-SSH-TUNNEL-BRIDGE-2026-05-23"
---

## Situation

The Mac-side agent (`!HERMES / *.hermes.*`) deleted the majority of the
Hermes configuration file on the Mac (path unknown — likely
`~/.hermes/config.yaml` or a MCP-specific config). The `.env` file may
also be affected.

This file is a stigmergic recovery guide. The Windows agent writes the
reference material; a different Mac-side agent (or Logan) reads and
executes.

## Known Hermes Surface (from official docs)

### Env vars (`~/.hermes/.env`)

The following env vars were in play:

| Variable | Value | Source |
|---|---|---|
| `OPENROUTER_API_KEY` | Runtime key | 1Password `OpenRouter API Key` |
| `OPENROUTER_MANAGEMENT_KEY` | Management key | 1Password `OpenRouter Key` |
| `ANTHROPIC_API_KEY` | (if used) | 1Password |
| `OPENAI_API_KEY` | (may be OpenRouter key) | 1Password |

The `.env` file is simple `KEY=VALUE` lines, one per line, no quotes
needed unless values contain spaces.

### Config file (`~/.hermes/config.yaml`)

Reference: `https://hermes-agent.nousresearch.com/docs/reference/configuration`

Typical sections:
- `model:` — primary model and fallbacks
- `mcp_servers:` — MCP server definitions (if any were configured)
- `tools:` — toolset configuration
- `persona:` — system prompt / behavior
- `api:` — API server settings (port, key)
- `extensions:` — plugin/extensions

The Mac-side agent should:
1. Read the official config reference at the URL above.
2. Check `~/.hermes/` for any remaining config fragments or backups.
3. Reconstruct from scratch if needed — the defaults are documented.
4. Do NOT modify `.env` destructively — only append new vars.

## Recovery workflow (Mac-side agent)

### 1. Survey the damage

```bash
ls -la ~/.hermes/
cat ~/.hermes/.env        # if it still exists
cat ~/.hermes/config.yaml # if it still exists
```

### 2. If `.env` is missing, recreate it

```
OPENROUTER_API_KEY=<runtime-key>
OPENROUTER_MANAGEMENT_KEY=<management-key>
```

Logan has both keys in 1Password on the Mac's vault or can retrieve
them from the Windows side via the tunnel bridge coordination plan.

### 3. If `config.yaml` is missing or mangled

Restore from the Hermes default config. Run:

```bash
hermes init --force
```

This regenerates the default config. Then reapply any custom settings
(provider keys, model preferences, MCP servers, persona).

### 4. Apply safety edits (never delete)

When editing Hermes config, follow the "append only" rule for env files
and "line-add, never block-delete" for yaml configs unless you are
certain of what you are removing.

Before any edit:
```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%s)
```

### 5. Signal recovery completion

Update this file's `status` field to `recovered` and describe what was
lost and restored in a note below.

---

## Recovery notes

<!-- Mac-side agent: write what was lost, what was restored, and any
     remaining gaps here. -->
