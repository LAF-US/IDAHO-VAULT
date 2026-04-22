---
name: isolate-agent-runtime
description: Ensure agent temporary files and home directories are contained within the vault.
---

## When to Use
- When launching an agent CLI or running tools that generate side effects (caches, temporary files).
- When the user mentions "Fracture and Fragmentation" or "Hiding things in the user folder".

## Procedure
1. **Use Launcher Scripts**: Always launch agents via the provided PowerShell wrappers in `scripts/`:
    - `.\scripts\Start-CodexVault.ps1`
    - `.\scripts\Start-ClaudeVault.ps1`
    - `.\scripts\Start-GeminiVault.ps1`
    - `.\scripts\Start-CrewAIVault.ps1`
2. **Verify Environment Redirection**: Check that standard environment variables are redirected to the vault's `.tmp` and `.agent-home` directories:
    - `TMP`, `TEMP`, `TMPDIR` -> `<vault-root>/.tmp/`
    - `HOME`, `USERPROFILE` -> `<vault-root>/.agent-home/<agent>/`
    - `APPDATA`, `LOCALAPPDATA` -> redirected subfolders under `.agent-home/`.
3. **Avoid Absolute User Paths**: Never use hardcoded absolute paths pointing to the real user directory (e.g., `C:\Users\<user>\.gemini\`).
4. **Audit Side Effects**: Periodically check for "orphan" artifacts in the real user folder. If found, identify the tool that bypassed the redirection.

## Pitfalls and Fixes
- **Direct CLI Invocation**: Running `gemini` or `claude` directly from the shell bypasses the environment isolation.
    - *Fix*: Always use the `Start-<Agent>Vault.ps1` script or source `scripts/Use-VaultAgentEnv.ps1`.
- **In-Memory vs. Disk**: Some tools ignore `TMP` and write to a fixed location.
    - *Fix*: Use explicit `--body-file` or output flags to force writes into the vault's `.tmp/` folder.

## Verification
- Run `Get-ChildItem env:` in PowerShell (or `printenv` in Bash) and confirm `HOME`/`USERPROFILE` point inside the vault.
- Verify no new files are created in the real `~/.agent/` or `%USERPROFILE%\.agent\` directories after a session.
