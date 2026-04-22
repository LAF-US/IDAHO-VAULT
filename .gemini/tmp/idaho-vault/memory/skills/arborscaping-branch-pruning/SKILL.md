---
name: arborscaping-branch-pruning
description: Identify and prune stale or orphan Git branches while preserving "cannon fodder" troubleshooting branches.
---

## When to Use
- When the user directs "ARBORSCAPING" or requests a cleanup of the repository's branch structure.
- When the `DOCKET.md` lists stale remote branches needing attention.
- Periodic repository maintenance to reduce clutter and confusion in the Git graph.

## Procedure
1. **List All Branches**: Run `git branch -a` to see all local and remote branches.
2. **Identify Merged Candidates**: Run `git branch -a --merged main` (or the current primary branch) to find branches that have been fully incorporated.
3. **Check for "Cannon Fodder" Exceptions**:
    - DO NOT delete branches identified as "cannon fodder" for GitHub Workflow Troubleshooting, even if they appear merged.
    - Protected patterns include: `bot/`, `dependabot/`, `ingest-`, or branches explicitly named for workflow repair.
    - If unsure, check `DOCKET.md` or ask the user if a specific branch is "cannon fodder."
4. **Audit Unmerged Branches**:
    - For branches not merged into `main`, check their recent history: `git log main..[branch]`.
    - Cross-reference with the "BLOCKED / PENDING LOGAN" section in the `DOCKET.md` (usually at `!/__!__/!/! The world is quiet here/DOCKET.md`).
    - Identify "orphan" branches (no active work, no associated PR, no mention in DOCKET).
5. **Verify and Propose**:
    - Compile a list of branches recommended for deletion.
    - Present the list to the user and request explicit confirmation (e.g., using `ask_user` with a `yesno` question).
6. **Execution**:
    - Delete local branches: `git branch -d [branch]`.
    - Delete remote branches: `git push origin --delete [branch]`.

## Pitfalls and Fixes
- **Merged vs. Deleted**: A branch can be merged but still exist locally or on origin. Pruning handles both.
- **Accidental Deletion**: If you delete a "cannon fodder" branch by mistake, notify the user immediately so it can be restored from the Git reflog or remote backup.
- **Diverged Branches**: Branches that have diverged significantly from `main` without being merged should be flagged for "human review" rather than deletion.

## Verification
- Run `git branch -a` after pruning to confirm the branch list is clean.
- Ensure no "cannon fodder" branches were removed.
- Verify that `DOCKET.md` status matches the actual state of the repository.
