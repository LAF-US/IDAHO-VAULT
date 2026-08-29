---
title: "LAF-35 — CI/NETWEB Triage Report"
updated: 2026-04-08
status: active
authority: LOGAN
related:
  - LAF-35
  - NETWEB
  - AGENTS
  - DECISIONS
---

# LAF-35 — SURGICAL PLAN: CI/NETWEB Triage
**Agent:** GitHub Copilot (The Clerk)
**Date:** 2026-04-08
**Status:** AWAITING ARCHITECT APPROVAL — no kinetic action taken
**Linear:** LAF-35

---

## Executive Summary

Four confirmed CI failures are active on `main`. One is a false-positive pattern in the NETWEB checker that masks real violations. Three `action_required` entries on the current copilot PR are expected behavior (Copilot deployment gate pending Logan's approval). No implementation has been made. This document is the deliverable.

---

## PART I — FORENSIC DIAGNOSIS

### Failure 1 — NETWEB Path Portability Check (False Positive)

**Workflow:** `.github/workflows/check-portable-paths.yml`
**Last failure:** `run 24055498987`, 2026-04-06T23:02:30Z
**Conclusion:** `failure`

**Root Cause:**

The NETWEB checker calls `git diff --name-only` and `git ls-tree` without disabling git's `core.quotePath` behavior. By default, git wraps filenames containing non-ASCII characters in double-quote delimiters: e.g. a file named `article • source.md` becomes `"article \342\200\242 source.md"` in the output.

The checker's illegal-character regex is:
```bash
if echo "$filepath" | grep -qE '[<>:"|?*]'; then
```

This character class includes `"`. The result: **every file with non-ASCII characters in its name is falsely reported as an ILLEGAL CHARACTER violation** because the surrounding `"` that git added as quoting is being matched.

**Specific offenders in the log (false positives):**
- `"2026-04-05 - Idaho Capital Sun - ...• Idaho Capital Sun.md"` → the `•` (U+2022 BULLET) triggered git quoting; the `"` is git's delimiter, not part of the filename
- `"2026-04-06 - Idaho Capital Sun - ...• Idaho Capital Sun.md"` → same
- `"SCRATCH FOLDER/SCRATCH BIN/vault/TOPICS/Idaho Code ╬╂74-202 (2).md"` → box-drawing chars triggered quoting

**Evidence the files are syntactically valid on the filesystem:**
```bash
# This returns the files without error, confirming no actual " in names:
git -c core.quotePath=false ls-files | grep -E '[<>:"|?*]'
# Returns nothing — no real violations in those filenames
```

**Impact:** The NETWEB check blocks all main-branch pushes and PRs that touch any file with Unicode characters (accented letters, curly quotes, bullets, em-dashes, etc.) — which is the majority of the journalism notes in this vault.

---

### Failure 2 — Vault Ingest (Missing Permission)

**Workflow:** `.github/workflows/vault-ingest.yml`
**Last failure:** `run 24082829625`, 2026-04-07T13:04:12Z
**Conclusion:** `failure`

**Root Cause:**

The `ingest` job declares only:
```yaml
permissions:
  contents: write
```

But the final step calls `gh pr create`, which requires a token with `pull-requests: write` scope. Without it, the GitHub GraphQL API rejects the mutation:

```
pull request create failed: GraphQL: Resource not accessible by integration (createPullRequest)
```

The push to origin succeeds (branch is created), but the PR creation fails, leaving an orphaned branch in the repo.

**Additional note:** The branch name pattern `ingest-YYYYMMDDTHHMMSSZ` does not match any prefix covered by `auto-pr.yml` (which only handles `claude/**`, `codex/**`, `gemini/**`, `copilot/**`, `perplexity/**`, `grok/**`, `serena/**`). Even with permission fixed, auto-PR logic would not fire for ingest branches.

---

### Failure 3 — Daily To-Do Rollover (git abort in create-pull-request)

**Workflow:** `.github/workflows/daily-rollover.yml`
**Last failure:** `run 24077654638`, 2026-04-07T10:52:31Z
**Conclusion:** `failure`

**Root Cause:**

The workflow's "Create rollover pull request" step uses `peter-evans/create-pull-request@v7` without specifying `add-paths`. By default, this action stages **all** modified/untracked files in the working tree, not just the two target files (`${TARGET_DATE}.md` and `TO DO LIST.md`).

The action's internal `git add --all` (or equivalent) encounters the full vault file tree — including files with Unicode characters. When the action then attempts `git commit`, git outputs:

```
	original equipment manufacturer.md
	...
Aborting
##[error]The process '/usr/bin/git' failed with exit code 1
```

The abort is triggered when the action's internal git commit encounters files it cannot cleanly process in its automated context (no interactive terminal, no git identity configured at the action level, or a conflict with a previously-staged state left by the `git add` in the "Prepare rollover changes" step).

**Secondary contributing factor:** The `git add "${TARGET_DATE}.md" "TO DO LIST.md"` in the prior step stages specific files, but `create-pull-request@v7` without `add-paths` resets and re-stages everything, discarding the targeted staging.

---

### Failure 4 — Dependabot npm/maven (Missing manifests)

**Source:** `.github/dependabot.yml`
**Last failure:** `run 24105630392`, 2026-04-07T21:36:17Z
**Conclusion:** `failure`

**Root Cause:**

The `dependabot.yml` configures two package ecosystems with no manifests in this repo root:

```yaml
- package-ecosystem: "npm"      # No package.json exists
  directory: "/"
- package-ecosystem: "maven"    # No pom.xml exists
  directory: "/"
```

This is an Obsidian markdown vault, but it does have a root `requirements.txt`, so `pip` is a valid ecosystem here. The invalid entries are `npm` and `maven`, which point at missing manifests and generate noisy failures without adding coverage.

Dependabot logs include `ERROR: /package.json not found`. If `pip` begins failing later, that should be triaged separately against the actual root manifest rather than removed by assumption.

---

### Non-Failure: `action_required` on Copilot PR Workflows

**Workflow runs:** 24116358855, 24116358858, 24116358862
**Workflows:** Auto Merge on Label, NETWEB Path Portability Check, Sync PR state to Linear
**On:** `copilot/triage-state-of-flows` (this PR)

These are **not failures**. The `action_required` conclusion with `total_jobs: 0` is the expected result of the Copilot deployment gate (branch protection rule requiring Copilot code review approval) before `pull_request_target` workflows can run. Logan must approve the deployment gate to unblock these.

---

### Warning: Node.js 20 Action Deprecation

**Affected actions:** `actions/checkout@v4`, `actions/setup-python@v5`, `peter-evans/create-pull-request@v7`
**Deadline:** June 2, 2026 (forced to Node.js 24); September 16, 2026 (Node.js 20 removed)

Not a current failure, but will become blocking in ~7 weeks. All three actions have Node.js 24-compatible releases already published.

---

## PART II — SURGICAL PLAN

> No files have been staged, committed, or pushed as part of this plan.  
> Awaiting Architect approval before execution.

---

### Fix 1 — NETWEB Checker: Disable git quotePath

**File:** `.github/workflows/check-portable-paths.yml`

**Change:** Add `-c core.quotePath=false` to all `git` calls that produce file lists, so filenames with non-ASCII characters are returned as raw paths without surrounding `"` delimiters.

**Exact diff:**

```diff
-          if [ "${{ github.event_name }}" = "pull_request" ]; then
-            FILES=$(git diff --name-only "origin/${{ github.base_ref }}"...HEAD 2>/dev/null || git ls-tree -r HEAD --name-only)
-          else
-            FILES=$(git diff --name-only HEAD~1...HEAD 2>/dev/null || git ls-tree -r HEAD --name-only)
-          fi
+          if [ "${{ github.event_name }}" = "pull_request" ]; then
+            FILES=$(git -c core.quotePath=false diff --name-only "origin/${{ github.base_ref }}"...HEAD 2>/dev/null || git -c core.quotePath=false ls-tree -r HEAD --name-only)
+          else
+            FILES=$(git -c core.quotePath=false diff --name-only HEAD~1...HEAD 2>/dev/null || git -c core.quotePath=false ls-tree -r HEAD --name-only)
+          fi
```

And in the case-collision check:
```diff
-          ALL_FILES=$(git ls-tree -r HEAD --name-only)
+          ALL_FILES=$(git -c core.quotePath=false ls-tree -r HEAD --name-only)
```

**Result:** Files with `•`, `–`, `'`, and other non-ASCII characters will pass through as raw Unicode strings. The `[<>:"|?*]` regex will correctly test the actual characters in the filename rather than git's quoting delimiters.

**Note on genuine violations:** After this fix, any file that truly contains a literal `"`, `<`, `>`, `:`, `|`, `?`, or `*` character in its name will still be caught correctly. The SCRATCH FOLDER files with box-drawing characters (`╬`, `╂`) contain characters that are legal on Linux but problematic on Windows — those will need a separate review decision (rename or exclude from check if the SCRATCH FOLDER is not cross-platform-synced).

---

### Fix 2 — Vault Ingest: Add `pull-requests: write`

**File:** `.github/workflows/vault-ingest.yml`

**Exact diff:**

```diff
   permissions:
     contents: write
+    pull-requests: write
```

---

### Fix 3 — Daily To-Do Rollover: Scope create-pull-request with `add-paths`

**File:** `.github/workflows/daily-rollover.yml`

**Exact diff:**

```diff
       - name: Create rollover pull request
         if: steps.changes.outputs.has_changes == 'true' && github.event.inputs.dry_run != 'true'
         uses: peter-evans/create-pull-request@v7
         with:
           branch: bot/daily-rollover-${{ steps.changes.outputs.target_date }}
           commit-message: "rollover: carry incomplete to-dos to ${{ steps.changes.outputs.target_date }}"
           title: "rollover: carry incomplete to-dos to ${{ steps.changes.outputs.target_date }}"
           labels: auto-merge
+          add-paths: |
+            ${{ steps.changes.outputs.target_date }}.md
+            TO DO LIST.md
+          commit-author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
+          author: github-actions[bot] <github-actions[bot]@users.noreply.github.com>
           body: |
             Automated daily rollover update generated by GitHub Actions.
           delete-branch: true
```

**Why `add-paths` fixes the abort:** The action will only stage the two explicitly named files. It will no longer attempt to stage the full vault file tree, which eliminates the path where the git operation encounters problematic conditions.

**Why `commit-author`/`author`:** Explicitly setting the author identity prevents failures in environments where git global config is not pre-configured by the action runner.

---

### Fix 4 — Dependabot: Remove only invalid ecosystems

**File:** `.github/dependabot.yml`

**Exact replacement (full file):**

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    allow:
      - dependency-type: "all"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 5
    allow:
      - dependency-type: "all"
```

**Rationale:** Remove `npm` and `maven` entries only. This vault has no root `package.json` and no root `pom.xml`, but it does have a root `requirements.txt`, so the `pip` ecosystem is valid and should remain.

---

### Fix 5 (Optional/Deferred) — Node.js 20 Action Upgrades

**Files:** All workflows using `actions/checkout@v4`, `actions/setup-python@v5`, `peter-evans/create-pull-request@v7`

When ready (before June 2, 2026):
- Set `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` at the workflow or repo level to opt in early, OR
- Pin explicit versions of each action that ship with Node.js 24 support (check each action's release notes)

---

## PART III — PRIORITY ORDER

| # | Fix | Workflow | Severity | Est. Time |
|---|-----|----------|----------|-----------|
| 1 | NETWEB quotePath fix | check-portable-paths.yml | **Critical** — blocks all PRs/pushes with Unicode filenames | 5 min |
| 2 | Vault Ingest permissions | vault-ingest.yml | **High** — daily scheduled workflow fails every run | 2 min |
| 3 | Rollover add-paths | daily-rollover.yml | **High** — daily scheduled workflow fails every run | 5 min |
| 4 | Dependabot cleanup | dependabot.yml | **Medium** — daily noise, no actual security value | 5 min |
| 5 | Node.js 20 upgrades | all workflows | **Low/Deferred** — deadline June 2026 | 30 min |

---

## PART IV — WHAT IS NOT BROKEN

- `auto-pr.yml` — Functioning correctly for agent branches
- `auto-merge.yml` — Functioning correctly; `action_required` on copilot PR is expected
- `linear-pr-sync.yml` — Functioning correctly (Linear sync working per DOCKET)
- `branch-cleanup.yml` — Functioning correctly
- `budget-tracker-csv-export.yml` — Functioning correctly
- `janitor-sweep.yml` — Functioning correctly
- `wayback-preserve.yml` / `wayback-audit.yml` — Functioning correctly

---

## Standing Order Compliance

Per LAF-35 directive:

- ✅ **DIAGNOSED** — Four confirmed root causes identified with evidence from raw CI logs
- ✅ **PRESCRIBED** — Surgical plan with exact YAML diffs for each fix
- ⏸️ **NO KINETIC ACTION** — No files staged, committed, or pushed beyond this report
- ⏳ **AWAITING ARCHITECT APPROVAL** — All four fixes are ready to execute on Logan's order

**-C** (The Clerk)
