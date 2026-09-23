---
title: "Continue local sessions from any device with Remote Control"
source: "https://code.claude.com/docs/en/remote-control"
authority: LOGAN
doc_class: sources
agent: Claude Code
tags:
  - remote-control
  - mobile
  - cross-device
  - session-continuity
status: captured
date created: 2026-06-03
---

# Source: Claude Code Remote Control Documentation

> **Summary**: Claude Code's Remote Control feature allows continuing local sessions from any device (phone, tablet, browser) while the session runs on your local machine.

## Key Points

- **Local execution**: Session runs on your machine, not in the cloud
- **Cross-device sync**: Conversation stays in sync across all connected devices
- **Auto-reconnect**: Survives interruptions (sleep, network drops)
- **Full environment access**: Filesystem, MCP servers, tools, project config all available remotely

## Requirements

- Claude Code v2.1.51+
- Pro, Max, Team, or Enterprise plan (API keys not supported)
- On Team/Enterprise: Admin must enable Remote Control in [admin settings](https://claude.ai/admin-settings/claude-code)
- Authentication: `claude /login`
- Workspace trust: Run `claude` in project directory once

## Quick Start

```bash
claude remote-control
```

Displays session URL and QR code for mobile access.

## Comparison to Web Version

| Feature | Remote Control | Web (code.claude.com) |
|---------|---------------|----------------------|
| Execution | Local machine | Cloud |
| Filesystem access | Full local access | Limited |
| MCP servers | Available | Not available |
| Tools | Local tools | Cloud tools |

## See Also

- [Full Remote Control Documentation](https://code.claude.com/docs/en/remote-control)
- [Claude Code CLI](https://code.claude.com/docs/en/cli)
- [MCP Servers](https://code.claude.com/docs/en/mcp)
