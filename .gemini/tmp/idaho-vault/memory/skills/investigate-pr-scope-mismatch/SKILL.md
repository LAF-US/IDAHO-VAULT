---
name: investigate-pr-scope-mismatch
description: Forensic procedure to reconcile git commit diffs against original Pull Request scope.
---

## When to Use
- When a commit diff includes changes that seem unrelated to the commit message or PR title.
- When investigating "suspicious" activity that might be an automation artifact.
- Trigger: User flags a "scope mismatch" in a squash-merged commit.

## Procedure
1. **Identify the Commit**: Get the commit hash and linked PR number (usually found in the squash commit message: "Merge pull request #X").
2. **Fetch PR Metadata**: Use the GitHub CLI (`gh`) to retrieve structured data for the PR:
    ```bash
    gh pr view <PR_NUMBER> --json author,body,headRefName,labels,title
    ```
3. **Analyze Branch Name (`headRefName`)**:
    - Check if the branch name (e.g., `fix-rollover-and-demote-readme`) is broader than the PR title (e.g., `fix rollover`).
    - **Known Issue**: The `auto-pr.yml` workflow has a "Title Amputation" bug that truncates the last word of branch names.
4. **Inspect Body for Overwrites**:
    - Compare the current PR body with the auto-generated markers (e.g., `**Risk tier:** low`).
    - Note if an agent has overwritten the body, potentially erasing original context or scope markers.
5. **Trace Identity**:
    - Recognize that `[ID]+[login]@users.noreply.github.com` is a standard GitHub privacy email, not a daemon.
    - Massive file counts are normal for squash-merged commits as they bundle the entire branch history.
6. **Reconcile Findings**: Determine if the mismatch is a result of the "Title Amputation" bug or intentional scope creep.

## Pitfalls and Fixes
- **Narrative Over-reaching**: Mistaking standard GitHub behavior (squash-merges, noreply emails) for malicious activity.
    - *Fix*: Check the `AUDIT-PR-LOOP-2026-04-19.md` for known automation bugs before forming a hypothesis.
- **Incomplete Local Context**: PR history and branch names are often lost after a squash-merge.
    - *Fix*: Use `gh pr view` to reach into the GitHub API for the original metadata.

## Verification
- Investigation is complete when the mismatch is definitively linked to either an automation bug (e.g., title truncation) or a deliberate action documented in the PR metadata.
