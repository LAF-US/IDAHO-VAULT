---
name: MCP connector suite removal
description: Unused MCP connectors removed 2026-04-19 to eliminate startup overhead and 1Password wake-time prompts
type: project
---

All project-level MCP server registrations were removed on 2026-04-19 (commit 7d7caf6b). This eliminated:
- `.mcp.json` — Linear MCP via 1Password (was triggering wake-time unlock prompts)
- `.vscode/mcp.json` — VS Code OpenAI developer docs endpoint
- 7 unused HTTP endpoints from `.gemini/settings.json`
- `enabledMcpjsonServers` from `.claude/settings.json`

**Why:** None of the registered MCP servers had been successfully called in vault sessions. The 1Password `op run` wrapper on the Linear server was causing friction on every session start.

**How to apply:** If an MCP server is needed, re-add it per-project when it actually gets used. Serena remains available as an MCP server at user scope (registered locally via `claude mcp add -s user`).

**Status:** Infrastructure simplified. No regression expected — unused code removed.
