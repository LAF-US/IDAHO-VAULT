# Reproduce

Reproduce a GitHub issue to determine if a bug is valid and reproducible in IDAHO-VAULT.

**CRITICAL: You MUST always read `report.md` and write `report.md` to the triage directory before finishing, regardless of outcome. Even if you encounter errors, cannot reproduce the bug, hit unexpected problems, or need to skip — always write `report.md`. The orchestrator and downstream skills depend on this file to determine what happened. If you finish without writing it, the entire pipeline fails silently.**

**SCOPE: Your job is reproduction only. Do NOT go further than this (no diagnosis, no fixing). Do not spawn tasks/sub-agents.**

## Prerequisites

- **`triageDir`** — Directory containing the reproduction project, located outside the repository root (e.g. `../triage-issue-123`). If not passed as an arg, default to `../triage-gh-<issue_number>`.
- **`issueDetails`** — The GitHub API issue details payload.

## Overview

1. Confirm the issue details
2. Check for early exit conditions
3. Set up a reproduction project
4. Attempt to reproduce the bug
5. Write `report.md` with findings

## Step 1: Confirm Bug Details

Confirm that you have `issueDetails`. Read carefully:

- The bug description and expected vs actual behavior
- Any reproduction steps provided
- Environment details (if applicable)
- Comments that might clarify the issue

## Step 2: Check for Early Exit Conditions

Before attempting reproduction, check if this issue should be skipped.

**Comment Handling:** An early exit is only valid if no later comments in the issue invalidate it. For example, if the original reporter was on an old version but a later comment reproduces on the current version, the early exit no longer applies.

### Not Actionable (`not-actionable`)

Skip if the issue is not a bug report (feature requests, suggestions, discussions, questions about historical content).

### Missing Details (`missing-details`)

Skip if the issue is missing:

- A valid reproduction (URL, steps, or specific file references)
- A description of the expected result

### Host-Specific Issues (`host-specific`)

Skip if the bug can only be reproduced on a specific hosting platform and not locally.

### Unsupported Runtime (`unsupported-runtime`)

Skip if the bug is specific to a runtime not available in CI. IDAHO-VAULT is primarily a content repository, so most issues should be reproducible in the GitHub Actions environment.

### Maintainer Override (`maintainer-override`)

Skip if a maintainer (check `authorAssociation` for `MEMBER`, `COLLABORATOR`, or `OWNER`) has commented that this issue should not be auto-triaged.

## Step 3: Set Up Reproduction Project

For IDAHO-VAULT, the repository itself is the project. Clone it to the triage directory:

```bash
# The triage directory must be outside the repository root.
# Clone without hardlinks so the reproduction copy is isolated.
git clone --no-hardlinks . <triageDir>
cd <triageDir>
```

## Step 4: Attempt Reproduction

For IDAHO-VAULT, bugs typically fall into these categories:

### Content/Link Bugs

- Navigate to the mentioned files or paths
- Check if the described problem exists
- Verify the expected behavior should work
- Test links between documents

### Metadata Bugs

- Check file headers, frontmatter, or metadata files
- Verify consistency across the repository
- Look for missing or incorrect metadata

### Workflow Bugs

- Check the `.github/workflows/` directory
- Look at recent workflow runs
- Attempt to trigger the failing workflow

### Organization Bugs

- Check directory structure consistency
- Look for duplicate files
- Verify naming conventions

**Document what you observe:** Record exact error messages, which files are affected, and whether the issue is consistent.

## Step 5: Write Output

Write `report.md` to the triage directory. This is NOT for humans — it's context for the next pipeline stage. Include:

- The original issue title, description, and relevant details
- Full environment details
- All steps attempted and their results
- Complete error messages and observations
- Observations, theories about root cause
- Whether the issue was reproduced, not reproduced, or skipped (and why)

Be thorough. More context is better.
