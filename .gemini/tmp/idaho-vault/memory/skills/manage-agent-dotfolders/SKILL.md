---
name: manage-agent-dotfolders
description: List, audit, and perform mass operations on agent persona dotfolders (e.g., .claude, .gemini, .codex).
---

## When to Use
Use this skill when you need to identify all active agent personas, create new dotfolders, or perform operations across all agent-specific hidden directories.

## Procedure

1.  **List Dotfolders**: Standard `list_directory` or `glob` often hide or ignore dotfolders by default. Use PowerShell to list all directories starting with a dot.
    
    ```powershell
    Get-ChildItem -Path . -Force | Where-Object { $_.PSIsContainer -and $_.Name -like '.*' } | Select-Object -ExpandProperty Name
    ```

2.  **Audit Dotfolders**: Check each dotfolder for the presence of mandatory files (e.g., `MEMORY/`, `*.*.md` shims) as defined in `VAULT-CONVENTIONS.md`.

3.  **Perform Mass Operations**: Use PowerShell loops to copy files or update shims across all dotfolders.
    
    ```powershell
    # Example: Copy a file to every dotfolder
    $sourceFile = 'C:\path\to\source.txt';
    $folders = Get-ChildItem -Path . -Force | Where-Object { $_.PSIsContainer -and $_.Name -like '.*' } | Select-Object -ExpandProperty Name;
    foreach ($f in $folders) { Copy-Item -Path $sourceFile -Destination "$f/" -Force }
    ```

## Pitfalls and Fixes

- **`list_directory` returns 0 items**: symptom -> Using `list_directory(ignore=["*"])` or similar to find hidden files -> fix -> use the PowerShell command in step 1.
- **`glob` skips dotfolders**: symptom -> `**/.*` pattern doesn't return hidden folders -> fix -> use PowerShell `Get-ChildItem -Force`.
- **System folders included**: symptom -> `.git`, `.github`, `.obsidian` appear in the list -> fix -> filter out non-persona folders if necessary (see `AGENTS.md` for the list of authorized personas).

## Verification

1.  Confirm the number of dotfolders matches the expected count in the agent registry.
2.  Check for the presence of the copied file or modification in a sample of the targeted folders.
