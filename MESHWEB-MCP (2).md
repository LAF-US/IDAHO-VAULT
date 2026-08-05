---
authority: LOGAN
related:
  - MESHWEB
  - MCP
  - Linear
  - 1Password
status: active
---

# MESHWEB Annotation — `.mcp.json`

**MESHWEB scope:** `local` only  
**Portability gap:** `cloud` ❌ — no `op` CLI, no MCP server process spawning  
**Portability gap:** `ci` ❌ — no interactive MCP server process; CI uses REST API patterns

---

## What `.mcp.json` Does

Configures the Linear MCP server for Claude Code running on Logan's local desktop. Uses `op run` to inject the Linear API key from 1Password at runtime.

```json
command: op run -- npx -y linear-mcp-server@latest
env: LINEAR_API_KEY = op://IDAHO-VAULT/Linear API Key/credential
```

## Local Prerequisites (Blockers)

1. **`op` CLI installed**: `scoop install 1password` per `.op/SETUP.md`
2. **Linear API Key migrated to 1Password**: currently in GitHub Secrets — migrate to `IDAHO-VAULT` vault, item name `Linear API Key`, field `credential`

## Cloud Instance Substitute

The cloud Claude Code instance (`cloud` env) cannot spawn local MCP servers and has no `op` CLI. Cloud access to Linear uses:

- Logan pastes Linear content directly into the session, OR
- Future: Anthropic cloud infrastructure supports env var injection for `.mcp.json` (capability TBD — see MESHWEB Open Items)

## CI Substitute

GitHub Actions workflows access Linear via REST API using a key fetched from 1Password at runtime via `OP_SERVICE_ACCOUNT_TOKEN`. See `.github/workflows/1password-secret-template.yml`.
