# FORCE-PUSH ENABLEMENT FOR MAIN BRANCH

**Date:** 2026-04-01
**Context:** LFS history rewrite requires temporary force-push to main
**Issue:** GitHub branch protection rule GH013 is blocking force-push to main
**Status:** AWAITING LOGAN ACTION

---

## What Logan Needs to Do

### Option 1: Allow Force Pushes (Recommended for this use case)

1. Navigate to: https://github.com/loganfinney27/IDAHO-VAULT/settings/branches
2. Find the branch protection rule for `main`
3. Click "Edit" on the main branch protection rule
4. Scroll down to find "Allow force pushes"
5. Check the box next to "Allow force pushes"
6. Click "Save changes" at the bottom of the page

### Option 2: Grant Bypass to GitHub Actions Actor

1. Navigate to: https://github.com/loganfinney27/IDAHO-VAULT/settings/branches
2. Find the branch protection rule for `main`
3. Click "Edit" on the main branch protection rule
4. Scroll to "Bypass list" section
5. Add the GitHub Actions app or service account to the bypass list
6. Click "Save changes"

---

## After Force-Push Completes

**CRITICAL:** Re-disable force pushes immediately after the LFS rewrite push completes.

1. Navigate back to: https://github.com/loganfinney27/IDAHO-VAULT/settings/branches
2. Edit the main branch protection rule
3. Uncheck "Allow force pushes" (or remove the bypass)
4. Save changes

---

## Verification

After enabling force pushes, verify the setting took effect:

```bash
gh api repos/loganfinney27/IDAHO-VAULT/branches/main/protection | jq '.allow_force_pushes'
```

Should return: `{"enabled": true}`

When force pushes are disabled, it should return: `{"enabled": false}`

---

## Current State

- ✅ Local main has rewritten LFS history
- ✅ Working edits preserved in stash
- ❌ Remote main blocks force-push (GH013)
- ⏳ Awaiting Logan to enable force-push permission

---

## What Happens Next

Once Logan enables force-pushes:

1. Tell Claude: "retry the push"
2. Claude will immediately run: `git push --force-with-lease origin main`
3. The rewritten history will sync to GitHub
4. Claude will verify the push succeeded
5. Logan will re-disable force-pushes
6. Claude will pop the stash to restore working edits
7. Work continues normally
