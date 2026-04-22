---
name: scrub-protocol-references
description: Systematically remove references to suspended or retired protocols from operational governance files.
---

## When to Use
- When the user announces a protocol has been "suspended", "retired", or "abandoned" before implementation.
- When instructed to "scrub references" or "sanitize governance".

## Procedure
1. **Repository Search**: Perform a case-insensitive `grep_search` across the entire vault for the protocol name (e.g., "Whistle Protocol").
2. **Identify Target Files**: Focus on "operational governance" files:
    - `DOCKET.md`
    - `LEVELSET-CURRENT.md`
    - `CONSTITUTION.md`
    - `!/AGENTS.md`
    - `!/PROTOCOL.md`
    - Recent agent-filed `LEVELSET-REPORT-*.md` files.
3. **Execute Deletion/Rephrasing**:
    - **Tables**: Delete the entire row containing the reference.
    - **Lists**: Remove the bullet point.
    - **Reports**: If the entire report is about the retired protocol, check if it can be deleted or if it needs rephrasing to describe the event as a generic "synchronization" or "checkpoint" without using the banned name.
4. **Consistency Check**: Ensure that removing the item doesn't leave trailing commas, broken table formatting, or dangling references.
5. **Update Metadata**: Update the `date modified` in the frontmatter of any edited file.

## Pitfalls and Fixes
- **Record vs. Doctrine**: If the user says "REPORTS are for the RECORD -- DOCTRINE is for GOVERNANCE", prefer rephrasing historical reports rather than deleting them, but strictly remove the protocol from doctrinal files (DOCKET, AGENTS).
- **Broken Links**: If the protocol was a link target (e.g., `[[Whistle Protocol]]`), searching for the name might miss the brackets. Search for the core string.

## Verification
- A final `grep_search` for the protocol name returns zero results in the targeted governance files.
- `DOCKET.md` and `LEVELSET-CURRENT.md` no longer list the protocol as an active or blocked task.
