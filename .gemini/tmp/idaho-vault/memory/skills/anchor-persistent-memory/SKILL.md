---
name: anchor-persistent-memory
description: Anchor ephemeral session state and brain artifacts into the vault's versioned repository.
---

## When to Use
- When a task involves complex reasoning, multi-step planning, or forensic analysis.
- Before closing a session that produced durable context or decisions.
- Triggers: User mentions "Vault is the RECORD" or "Persistent Memory Anchoring".

## Procedure
1. **Identify Ephemeral Artifacts**: Collate chat-based plans, task lists, debug logs, or forensic reports generated during the session.
2. **Format for Persistence**: Convert the artifacts into a structured Markdown file (`.md`).
3. **Target the Memory Folder**:
    - Locate the agent's specific memory directory: `<agent-dotfolder>/MEMORY/` (e.g., `.gemini/MEMORY/`).
    - Create the directory if it does not exist.
4. **Descriptive Naming**: Use a descriptive filename including the date or task ID (e.g., `pr-280-body-2026-04-19.md`).
5. **Anchor to the Vault**:
    - Ensure the file is written to a path WITHIN the vault's root (e.g., `C:\Users\<user>\Documents\IDAHO-VAULT\.gemini\MEMORY\`).
    - **Crucial**: Do NOT use user-level temporary folders (e.g., `C:\Users\<user>\.gemini\tmp\`).
6. **Commit or Stage**: Add the file to the vault's versioned repository so it is visible to future agents.

## Pitfalls and Fixes
- **Hiding in User Folders**: Creating artifacts in `~/.agent/tmp` or `/tmp/` violates the "Vault is the RECORD" principle.
    - *Fix*: Always use absolute paths within the vault or relative paths starting from the vault root.
- **Overwriting without Archiving**: Replacing a plan without saving the old one loses the audit trail.
    - *Fix*: Use versioned filenames (date/timestamp suffixes).

## Verification
- File exists at `<vault-root>/<agent-dotfolder>/MEMORY/<filename>.md`.
- File content matches the session's key findings or plan.
- File is tracked by Git.
