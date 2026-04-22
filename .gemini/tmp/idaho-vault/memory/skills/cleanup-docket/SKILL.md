---
name: cleanup-docket
description: Clean and update the DOCKET.md file to align with its function as a live coordination board.
---

## When to Use
- When the user asks to "clean up the DOCKET", "update the courtroom", or provides a "precice accounting update".
- When the DOCKET contains stale directives, outdated tasks, or duplicate entries.

## Procedure
1. **Update Metadata**: Update the `date modified` in the YAML frontmatter to today's date and the current time.
2. **Prune Stale Directives**: Remove any delegation notes, dispatch instructions, or operator notes that are tied to past dates and are no longer relevant for live coordination.
3. **Refine ACTIVE WORK Table**:
    - **Merge Duplicates**: Consolidate identical or nearly-identical task entries into a single row.
    - **Remove Completed Tasks**: Excise rows for tasks that are marked as "Completed", "Done", or have achieved their final outcome (e.g., "Partial Success").
    - **Fix Broken Links**: Update or remove local file links that no longer resolve.
4. **Enforce Courtroom Boundary**: 
    - Remove legacy sections like detailed backlogs, project-scoped work items, or archival summaries.
    - Reminder: Detailed execution state belongs in Linear/GitHub; the DOCKET is only for immediate orientation (dispatch, signals, blockers, floor-holders).
5. **Promote Durable Context**: If removing a section that contains important history (like a bootstrap synthesis), ensure the DOCKET mentions the durable file where that context now lives.

## Pitfalls and Fixes
- **Fire Sale vs. Accounting**: Do not delete items wholesale. Analyze each entry's relevance against other files like `LEVELSET-CURRENT.md` before removing.
- **Path Sensitivity**: The `DOCKET.md` file may live in a nested directory with special characters (e.g., `!/!/__!__/!/! The world is quiet here/DOCKET.md`). Use `glob("**/DOCKET.md")` to find the exact path before writing.

## Verification
- Frontmatter `updated` and `date modified` fields match the current session.
- The `ACTIVE WORK` table only contains tasks that are "In progress", "Active", or "Blocked".
- The file content respects the "COURTROOM BOUNDARY" rule stated at the top of the file.
