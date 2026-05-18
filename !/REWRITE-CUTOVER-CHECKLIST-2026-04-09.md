---
authority: Codex
date created: 2026-04-09
status: active
source: ground-truth
---

# Rewrite Cutover Checklist - 2026-04-09

This note records the exact current state and the concrete cutover sequence for replacing protected `main` with the refreshed rewritten history.

It does not execute the cutover.

## Current State

Live remote heads:

- `main` -> `b56b3094679ed5a04652b71264d27ea8e5413237`
- `codex/rewrite-main-2026-04-09` -> `ad16792806ff7934c445a5db53c74d273490897a`

Local live repo:

- branch: `main`
- HEAD: `b56b3094`
- working tree: clean

Disposable rewrite mirror:

- path: `_private/rewrite-prep`
- bare: `true`
- rewritten HEAD: `ad167928`
- pack size: `32.78 MiB`
- garbage: `0`

## What Is Already Proven

- the rewritten mirror is based on the current post-`#200` / post-`#201` / post-`#203` repo state
- the six large first-pass offenders are gone from rewritten history
- the second-pass binary/media cleanup has been applied
- the parked review branch has already been refreshed from the rewritten mirror

## Protection State on `main`

Current `main` protection includes:

- `allow_force_pushes: true`
- `required_signatures: true`
- `required_linear_history: true`
- `required_conversation_resolution: true`
- PR review count required: `0`

## Likely Cutover Blockers

The most likely blockers are:

1. **Required signed commits**
   - the rewritten history in the disposable mirror is not guaranteed to satisfy GitHub's signed-commit protection on `main`
   - this is the most likely reason a force-push to protected `main` would still be rejected even though force-push is allowed

2. **Rule-based PR expectations around `main`**
   - normal direct updates to `main` are still governed by repo rules favoring PR flow
   - a true history replacement is not a normal PR merge, so this must be treated as an intentional protected-branch replacement

3. **Local clone fallout**
   - every existing local checkout and old branch base becomes suspect after cutover
   - stale local histories can reintroduce purged content later if reused casually

## Accuracy and Precision Standard

This cutover must satisfy both:

- **accuracy**
  - replace `main` with the intended refreshed rewritten history
  - preserve the current logical repo state, not an older rehearsal
  - keep the benchmarked workflow fixes and flatten-prep records in the rewritten result

- **precision**
  - replace only `main`
  - keep the parked review branch as reference until Logan chooses to prune it
  - avoid any extra branch or file churn during cutover
  - follow with explicit reclone/reset guidance

## Pre-Cutover Checklist

Before cutover, confirm all of the following:

- live repo on `main` is clean
- open PR count is `0`
- no new must-keep changes landed after `b56b3094`
- rewrite mirror still reports `ad167928` / `32.78 MiB`
- Logan has explicitly approved protected-branch replacement
- Logan has decided what to do with `required_signatures` during the cutover window

## Exact Cutover Shape

Run from the disposable rewrite mirror only.

### Step 1 - verify rewrite mirror state

```powershell
git -C "C:\Users\loganf\Documents\IDAHO-VAULT\_private\rewrite-prep" rev-parse --short HEAD
git -C "C:\Users\loganf\Documents\IDAHO-VAULT\_private\rewrite-prep" count-objects -vH
```

Expected:

- `ad167928`
- `size-pack: 32.78 MiB`

### Step 2 - ensure `origin` is attached

```powershell
git -C "C:\Users\loganf\Documents\IDAHO-VAULT\_private\rewrite-prep" remote -v
```

Expected:

- `origin https://github.com/loganfinney27/IDAHO-VAULT.git`

### Step 3 - replace `main`

```powershell
git -C "C:\Users\loganf\Documents\IDAHO-VAULT\_private\rewrite-prep" push --force origin main:refs/heads/main
```

If blocked:

- inspect the exact rejection
- most likely Logan action is temporarily adjusting signed-commit or branch-rule constraints on `main`

### Step 4 - verify remote heads after cutover

```powershell
git ls-remote --heads origin
```

Expected:

- `main` now points at the rewritten history
- `codex/rewrite-main-2026-04-09` may still exist until explicitly pruned

## Post-Cutover Cleanup

After successful cutover:

1. freeze old local clones as historical until reset or recloned
2. reset or reclone the live local repo
3. prune stale local branches/worktrees based on old SHAs
4. decide whether to keep or delete `codex/rewrite-main-2026-04-09`
5. only then begin the doctrinal flatten on the clean rewritten base

## Recommended Local Reset Paths

### Safeest: reclone

- archive current local checkout if desired
- make a fresh clone from rewritten `main`

### Faster: hard reset an existing checkout

Only if Logan explicitly wants reuse:

```powershell
git fetch origin
git checkout main
git reset --hard origin/main
git clean -fd
```

Then verify:

```powershell
git status --short --branch
git rev-parse --short HEAD
```

## Secret-Scanning Note

Current tracked content is clean of `AIza` matches, but GitHub still has an open secret-scanning alert because the leaked Google API key remains in historical commits and is marked publicly leaked.

That alert will remain logically open until:

- the broader key-rotation / 1Password sweep is handled, and/or
- the rewritten history fully replaces the old history on `main`

## Next Logan Gate

Logan still needs to decide:

1. whether to perform the protected-branch rewrite cutover now
2. whether `required_signatures` on `main` should be temporarily relaxed for that cutover
3. whether to keep or delete the parked review branch after successful cutover

Until those are decided, the correct lane remains preparation only.
