# Diagnose

Find the root cause of a reproduced bug in IDAHO-VAULT.

**CRITICAL: You MUST always read `report.md` and append to `report.md` before finishing, regardless of outcome. Even if you cannot identify the root cause — always update `report.md` with your findings.**

**SCOPE: Your job is diagnosis only. Do NOT go further (no fixing). Do not spawn tasks/sub-agents.**

## Prerequisites

- **`triageDir`** — Directory containing the reproduction project.
- **`issueDetails`** — The GitHub API issue details payload.
- **`report.md`** — File in `triageDir` from the reproduce step.

## Overview

1. Review the reproduction and error details from `report.md`
2. Locate relevant source files
3. Investigate the code/content to understand the issue
4. Identify the root cause
5. Append diagnosis findings to `report.md`

## Step 1: Review the Reproduction

Read `report.md` from the `triageDir` directory.

**Skip if not reproduced:** If `report.md` shows the bug was NOT reproduced or was skipped, append "DIAGNOSIS SKIPPED: No reproduction" and return `confidence: null`.

Re-run the reproduction if needed to see the error firsthand.

## Step 2: Locate Relevant Files

Using error messages, reproduction details, and issue description, identify the files likely involved. For IDAHO-VAULT, look in:

- **Content files** — Markdown files (`.md`), images, PDFs in the root and year-specific directories
- **Workflow files** — `.github/workflows/` for automation-related issues
- **Metadata files** — Any files with frontmatter, headers, or structured metadata
- **Configuration files** — `.github/` directory for repository configuration

## Step 3: Investigate

For different types of issues in IDAHO-VAULT:

### Content/Link Issues

- Check if files were moved or renamed (use `git log --follow -- path/to/file`)
- Look for typos in paths or URLs
- Verify relative vs absolute path usage
- Check for case sensitivity issues

### Metadata Issues

- Examine file headers and frontmatter
- Check for inconsistent metadata formats
- Look for missing required fields
- Verify date formats and naming conventions

### Workflow Issues

- Review the failing workflow file for syntax errors
- Check for references to non-existent files or dependencies
- Look at recent changes to the workflow
- Verify environment variables and secrets

### Organization Issues

- Check directory structure consistency
- Look for duplicate files with different naming conventions
- Verify file extensions are correct

Use commands to investigate:

```bash
# Search for files
find . -name "*.md" -type f

# Check file contents
grep -r "search term" .

# Check git history
git log --oneline -20 -- path/to/file

# Check recent changes
git diff HEAD~5 HEAD -- path/to/file

# List directory contents
ls -la path/to/directory/
```

## Step 4: Identify Root Cause

Document:

1. **Which file(s)** contain the bug or issue
2. **What the problem is** — the specific error or inconsistency
3. **Why this causes the observed behavior**
4. **What the fix should be** — high-level approach

Consider:

- Is this a regression from a recent change?
- Does this affect other similar use cases?
- Are there edge cases to consider?

**Tone calibration:** Describe the root cause factually, not dramatically. Avoid overstating impact unless evidence supports it.

## Step 5: Write Output

Append diagnosis findings to `report.md`. Include:

- Root cause explanation (which files, what is wrong, why)
- Affected file paths with line numbers (if applicable)
- Suggested fix approach
- Confidence level (`high`, `medium`, or `low`) and any caveats
