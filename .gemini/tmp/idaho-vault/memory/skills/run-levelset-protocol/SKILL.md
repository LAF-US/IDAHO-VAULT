---
name: run-levelset-protocol
description: Orient a repo-connected agent using the vault's auditable checkpoint protocol (LEVELSET).
---

## When to Use
- At the start of a new session or when the user explicitly triggers "LEVELSET".
- When an agent needs to re-orient to the "present state" of the ecosystem.
- Mandatory for "first-time" agents in the IDAHO-VAULT context.

## Procedure
1. **Locate the Prompt**: Search for the latest versioned LEVELSET prompt in the `!/!/` directory (e.g., `!/!/LEVELSET-v3.2.6.1-PROMPT.md`).
2. **Consult the Constitution**: Read `CONSTITUTION.md` (root) to understand current capability tiers and role definitions.
3. **Determine Capabilities**: Identify what tools you can and cannot use (e.g., reading/writing files, searching, shell access limitations).
4. **Answer the Six-Point Format**: Your reply must answer the following (based on the latest prompt):
    - **Identity**: Confirm your name and functional office (e.g., Gemini CLI, The Vault Advisor).
    - **Constitution**: Confirm you have read and will abide by the Constitution.
    - **Tier**: State your current capability tier (e.g., Tier 1 Support: Direct Write).
    - **Context**: Briefly summarize your understanding of the current vault state (from `LEVELSET-CURRENT.md`).
    - **Status**: Report any blockers or pending tasks (from `DOCKET.md`).
    - **Handshake**: Confirm readiness for direction.

## Pitfalls and Fixes
- **External vs. Internal**: Do not use `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` if you have direct repository access; that file is for chat-only agents.
- **Outdated Paths**: If a file path in the prompt (e.g., `!ADMIN/Claude.md`) is missing, search the directory (e.g., `!/!/`) for the modernized equivalent (e.g., `CONSTITUTION.md`).

## Verification
- Successful orientation is often acknowledged by the user with a signal like "DING" or "ECHO: TRIUNE".
- The agent's next action is grounded in the latest `DOCKET.md` state.
