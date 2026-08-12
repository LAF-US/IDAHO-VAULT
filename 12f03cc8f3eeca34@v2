# Plan: Fix PowerShell `claude` PATH + Qodo Extension Crash

## Context

**This is a recurring issue.** Multiple agents have been told to fix PATH problems. The Windows user PATH has been patched before but the fix keeps breaking because: (a) VS Code needs to be fully restarted after any Windows PATH change, and (b) the claude binary path is version-specific and breaks on updates. The PowerShell profile is the durable fix — it runs on every PS session regardless of when VS Code started, and the glob approach survives extension updates.

Two issues to fix:

1. **PowerShell can't find `claude`** — The Windows user PATH already has the correct claude binary directory (`...anthropic.claude-code-2.1.87-win32-x64\resources\native-binary`). The problem is VS Code was already running when that PATH was written via PowerShell. Windows PATH changes to the user environment don't propagate to already-running processes — VS Code and all terminals it spawns are still using the old PATH snapshot. Bash works because `~/.bashrc` is re-sourced on each new shell, but PowerShell does not re-read Windows user PATH mid-session.

2. **Qodo tab crashed/blanked** — The `.pr_agent.toml` is already on v2 (`/agentic_describe`, `/agentic_review`), so that migration is done. The `.qodo/agents/` and `.qodo/workflows/` directories exist but are empty. The VS Code extension tab itself has blanked — likely a runtime crash of the extension process. These two issues may be related: Qodo's VS Code extension may invoke `claude` via PowerShell (not bash), fail to find it, and crash.

---

## Fix 1: PowerShell `claude` PATH

**Root cause:** VS Code process inherited PATH before the user PATH was updated. All child terminals share VS Code's initial PATH snapshot.

**Fix:** Add the claude binary path to the PowerShell profile so it applies to every new PS session regardless of VS Code restart timing. Also covers the version-change fragility risk.

**File to edit:** `C:\Users\loganf\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
(Create if it doesn't exist — `$PROFILE` resolves there on Windows 11 PowerShell 7+)

**Content to add:**
```powershell
# Claude Code CLI — ensure it's on PATH for all PowerShell sessions
$claudeBin = "$env:USERPROFILE\.vscode\extensions" |
    Get-ChildItem -Filter "anthropic.claude-code-*" |
    Sort-Object Name -Descending |
    Select-Object -First 1 -ExpandProperty FullName
if ($claudeBin) {
    $env:PATH += ";$claudeBin\resources\native-binary"
}
```

This glob-selects the highest-versioned claude-code extension directory, so it survives auto-updates.

**Verification:** Open a new PowerShell terminal in VS Code → run `claude --version` → should return version string without error.

---

## Fix 2: Qodo Extension Crash

**Immediate fix (no config change needed):**
- Run `Developer: Reload Window` from the VS Code command palette. This restarts all extension host processes, including Qodo, and spawns fresh terminals that inherit the updated Windows PATH.
- If Qodo was crashing because it couldn't invoke `claude` in PowerShell, the PATH fix above + a window reload should resolve it.

**If it crashes again after reload:**
- Open the Output panel → select "Qodo" from the dropdown to read the extension's error log
- The `.qodo/agents/` and `.qodo/workflows/` directories are empty — Qodo may need config files there. Check Qodo docs for what belongs in those directories and populate accordingly.

**What is NOT the issue:**
- `.pr_agent.toml` is already migrated to v2. No changes needed there.
- The Qodo docs file in the vault root is just reference material — it can be committed or deleted, no action required for the fix.

---

## Execution Order

1. Edit PowerShell profile (create if needed) with the glob-based PATH snippet above
2. Run `Developer: Reload Window` in VS Code
3. Open new PowerShell terminal → verify `claude --version`
4. Check Qodo tab — if still blank, open Output → Qodo and report what the log shows

---

## Critical Files

- `C:\Users\loganf\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` — create/edit
- `c:\Users\loganf\Documents\IDAHO-VAULT\.pr_agent.toml` — no changes needed (already v2)
- `c:\Users\loganf\Documents\IDAHO-VAULT\.qodo\agents\` — may need population if Qodo still crashes post-reload
