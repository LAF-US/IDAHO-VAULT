---
name: winget installs (no admin)
description: Claude Code, Antigravity, and Cursor installed via winget without admin credentials — user-scope installs, IT-managed machine
type: reference
---

Claude Code, Antigravity, and Cursor were installed via `winget` without admin credentials on a work IT-managed machine.

**Constraints:**
- Unapproved `.exe` publishers are blocked by IT policy
- No admin credentials available
- User-scope installs only (`%LOCALAPPDATA%\Microsoft\WinGet\Packages\`)

**Active issue:** Claude Desktop app is out of date — "Cowork needs newer installation" error. Cannot upgrade via `winget upgrade` because new `.exe` installer will be blocked by publisher policy.

**Workarounds:**
1. Microsoft Store version (MSIX) — bypasses publisher block in most enterprise configs
2. `claude.ai/code` web app — no install required
3. IT request to whitelist `Anthropic, Inc.` as approved publisher

**How to apply:** When diagnosing PATH issues, missing executables, upgrade failures, or permission errors for these tools, check user-scope install locations and IT policy first.
