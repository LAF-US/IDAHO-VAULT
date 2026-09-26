---
name: PATH fixes — do not re-diagnose, just fix
description: Logan has had to tell multiple agents to fix standing PATH issues; do not re-investigate or ask, just apply the known fix
type: feedback
---

Logan has explicitly said PATH issues are a recurring annoyance across agents — do not re-diagnose or ask him about them.

**PERMANENT FIX APPLIED (2026-03-29):**

Three-layer fix — all three must be in place:

1. **Windows user PATH** (via `[Environment]::SetEnvironmentVariable(..., 'User')`):
   ```text
   C:\Users\loganf\.vscode\extensions\anthropic.claude-code-2.1.87-win32-x64\resources\native-binary
   ```
   Note: this breaks on extension updates because the path is version-specific.

2. **`~/.bashrc`** — for bash sessions in VS Code terminal.

3. **PowerShell profile** — the durable fix for PS sessions:
   `C:\Users\loganf\OneDrive - Idaho Public Television\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
   Uses a glob to find the highest-versioned claude-code extension dir — survives auto-updates.

**Why PATH fixes keep recurring:** Windows user PATH is version-specific and breaks when Claude Code updates. VS Code also doesn't inherit PATH changes made after VS Code is already running — so even a correct PATH change doesn't help until VS Code is restarted. The PS profile glob is the permanent fix for PowerShell.

**How to apply:** If `claude` is missing in PowerShell, check that the PS profile exists and contains the glob snippet. If it's a PATH issue in bash, check `~/.bashrc`. Do NOT re-diagnose from scratch — Logan is tired of this.
