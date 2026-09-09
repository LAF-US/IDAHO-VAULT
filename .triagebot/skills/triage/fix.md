# Fix

Develop and verify a fix for a diagnosed bug in IDAHO-VAULT.

**CRITICAL: You MUST always read `report.md` and append to `report.md` before finishing, regardless of outcome. Even if the fix fails — always update `report.md`.**

**SCOPE: Do not spawn tasks/sub-agents.**

## Prerequisites

- **`triageDir`** — Directory containing the reproduction project.
- **`issueDetails`** — The GitHub API issue details payload.
- **`report.md`** — File in `triageDir` from previous steps.

## Overview

1. Review the diagnosis from `report.md`
2. Implement a minimal fix
3. Verify the fix
4. Check for regressions
5. Generate git diff
6. Append fix details to `report.md`
7. Clean up

## Step 1: Review the Diagnosis

Read `report.md` to understand the root cause, affected files, and suggested approach.

**Skip if prerequisites unmet:** If the bug was not reproduced or was skipped, append "FIX SKIPPED: Not reproduced" and return `fixed: false`.

**Low-confidence path:** If diagnosis confidence is `low` or no clear root cause was found, do NOT attempt a fix. Instead:

1. Identify the most likely area(s) of the repository related to the issue
2. If possible, document what would need to be changed
3. Add brief inline comments (prefixed `// TRIAGE:` or `# TRIAGE:`) near relevant lines to help the implementor orient
4. Append findings to `report.md` and return `fixed: false`

**High-confidence path:** If confidence is `medium` or `high`, proceed with implementing a fix.

## Step 2: Implement the Fix

For IDAHO-VAULT, make changes based on the issue type:

### Content/Link Fixes

- Update broken links to point to correct files
- Verify the target file exists
- Update all references if files were moved

### Metadata Fixes

- Correct metadata in file headers or frontmatter
- Ensure consistency with other files
- Verify the metadata format is valid

### Workflow Fixes

- Fix syntax errors in workflow files
- Update references to renamed/moved files
- Ensure dependencies are correct
- Update environment variables or secrets

### Organization Fixes

- Move files to correct locations
- Rename files for consistency
- Update all references to the moved/renamed files

**Protected surfaces — mandatory stop condition:** Before proposing or making any move, rename, or restructuring change, read the applicable frontmatter and `VAULT-CONVENTIONS.md`. Do not modify `!/`, root-flat notes, or another agent's persona folder without Logan's explicit authorization. Record the blocked recommendation in `report.md` and return `fixed: false` when the requested change touches a protected surface.

**Keep it minimal:**

- Only change what's necessary to fix the bug
- Don't refactor unrelated content
- Don't add new features
- Preserve historical accuracy

**Consider edge cases:**

- Will this break other references?
- Are there multiple files with the same issue?
- Should all similar cases be fixed?

## Step 3: Verify the Fix

After making changes:

1. **For content fixes:** Verify links work, metadata is valid, no new issues are introduced
2. **For workflow fixes:** Run the workflow to verify it passes (if possible in CI)
3. **For organization fixes:** Verify all references are updated, nothing is broken

## Step 4: Check for Regressions

Check that your fix doesn't introduce new problems:

- Search for other references to the changed files
- Verify similar files don't have the same issue
- Check that navigation and links still work

## Step 5: Generate Git Diff

```bash
git diff
```

This captures all your changes for the report.

## Step 6: Write Output

Append fix details to `report.md`:

- What was changed and why
- The full git diff
- Whether the fix was successful
- Verification results
- Any limitations or edge cases not addressed
- Alternative approaches considered

## Step 7: Clean Up

1. Run `git status` and review all changed files
2. Revert changes that are NOT part of the fix:
   - Debug code and temporary test files
   - Temporary files from diagnosis/reproduction
3. Use `git checkout -- <file>` to discard unwanted changes
4. DO NOT commit or push — the orchestrator handles that
