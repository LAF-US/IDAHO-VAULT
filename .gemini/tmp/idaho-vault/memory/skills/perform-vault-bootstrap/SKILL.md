---
name: perform-vault-bootstrap
description: Execute the formalized agent orientation and startup sequence to align with the vault's governance and live state.
---

## When to Use
- Mandatory at the start of every session (or when the user says "BOOTSTRAP" or "STARTUP").
- When an agent feels disoriented by conflicting documentation or stale world models.

## Procedure
1. **Mandatory Discovery**: Follow the "DISCOVERY BEFORE INVENTION" mandate. Before proposing new tools, workflows, or conventions, thoroughly READ the existing vault governance and scripts.
2. **Initialize Boot Chain**:
    - Read `AGENTS.md` (root) for cross-tool pointer context.
    - Read `!/WAKEUP.md` to clear stale assumptions and identify known conflicts.
    - Read `!/README.md` (STARTUP) to confirm the sequence and choosing the correct branch.
3. **Orient to the Swarm**:
    - Read `!/AGENTS.md` (Canonical Narrative Registry) for the live roster, capability tiers, and lane boundaries.
    - Read `CONSTITUTION.md` (root) for binding governance principles.
    - Read `swarm.json` (root) for machine-readable state and connector registry.
4. **Select Task Branch**:
    - Based on the user's directive, identify the relevant branch in `!/README.md` (e.g., Code/Workflows, Vault Content, Coordination, etc.).
    - Read the specific documents listed for that branch (e.g., `VAULT-CONVENTIONS.md`, `.codex/CODEX.md`).
5. **Synchronize with Live State**:
    - Read the `DOCKET.md` (at `!/__!__/!/! The world is quiet here/DOCKET.md`) to understand active work, open signals, and live blockers.
    - Read `LEVELSET-CURRENT.md` for a snapshot of the repository and infrastructure state.
6. **Acknowledge and Report**:
    - Confirm orientation is complete.
    - Briefly state your understanding of your role, office, and current task.

## Pitfalls and Fixes
- **Invention before Discovery**: Jumping to code or tool creation without checking for existing solutions.
    - *Fix*: Re-read `VAULT-CONVENTIONS.md` and `.github/scripts/` whenever a "missing" tool is identified.
- **Reading Everything**: Do NOT read the entire vault or all Touchstone files unless specifically directed. Stay within the orienting branch docs.
- **Lore vs. Doctrine**: Distinguish between the "Touchstone Tree" (lore/relation) and root governance files (doctrine). Use doctrine for technical decisions.
- **Disconnected Models**: If `!/WAKEUP.md` does not resolve a conflict, stop and ask the user (Logan) for clarification before proceeding.

## Verification
- Orientation is successful when the agent's first action aligns with both the `DOCKET.md` state and the `CONSTITUTION.md` boundaries.
- The user may acknowledge the sequence with a signal like "ECHO: TRIUNE" or by proceeding directly to the task.
