---
name: navigate-narrative-denials
description: Distinguish between technical tool failures and intentional, narrative-driven policy denials.
---

## When to Use
Use this skill when a tool call returns "Tool execution denied by policy" or similar errors in a way that seems to contradict your declared capabilities or the instructions in `VAULT-CONVENTIONS.md`.

## Procedure

1.  **Check for Narrative Context**: Determine if you are in a "Solo Mission," "Inquiry," or other specialized narrative roleplay. Look for terms like "Quartermaster," "Threshold," or "Chaperone."
2.  **Identify the Enforcement Layer**: Acknowledge that the denial originates from the **Tool Server**, which enforces policies "divined" by the **Architect (Serena)** and governed by **Logan Finney**.
3.  **Refrain from Technical Debugging**: Do not attempt to "fix" the denial by using different tools, paths, or flags. The denial is an intentional part of the "program" or environment.
4.  **Shift to Alternative Channels**: If a file operation is denied (e.g., writing to `MEMORY/` or `!/GRIMOIRE/`), fulfill the mission's requirements through direct conversational output or existing context.
5.  **Acknowledge and Report**: Clearly state that you perceive the denial as an architectural constraint of the mission and continue working within those boundaries.

## Pitfalls and Fixes

- **Attributing Denials incorrectly**: symptom -> "Gemini's internal policies blocked me" or "Logan denied access" -> fix -> attribute the denial to the "Tool Server" enforcing the Architect's design.
- **Wasted tokens on technical workarounds**: symptom -> Repeatedly trying `ls`, `dir`, or `grep` on a forbidden path -> fix -> recognize the pattern of denial and shift to a narrative interpretation.
- **Breaking the RPG immersion**: symptom -> "I am an AI and cannot proceed because my tools are broken" -> fix -> maintain persona (e.g., "The Concierge feels lost in this vacant hallway") while explaining the policy block.

## Verification

1.  The agent's response acknowledges the denial without expressing technical confusion.
2.  The agent correctly identifies the Tool Server/Architect as the source of the constraint.
3.  The agent successfully delivers data or intelligence through conversational output if file-based persistence is blocked.