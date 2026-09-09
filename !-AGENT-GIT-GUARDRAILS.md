---
title: "Agent Git Guardrails - Issues & Solutions"
updated: 2026-07-02
status: active
authority: "LOGAN"
---

# Agent Git Guardrails - Issues & Solutions

## Problem Statement

Agents (Vibe CLI, Claude, and others) repeatedly run destructive git commands that break local repository remote tracking. This manifests as GitHub Desktop asking to "publish repository" instead of fetch/push/pull, lost remote origin configuration, and broken branch upstream tracking.

### Root Cause

Agents misanalyze git history, conclude files need to be "scrubbed" from history, then run history-rewriting commands (git filter-branch, git filter-repo). These rewrite commit SHAs and break remote tracking. The agents' analysis is often wrong - false positives on file existence in history.

## Proposed Solutions

### Solution 1: One-Liner Fix (Manual)

For immediate recovery:

```bash
git remote add origin https://github.com/LAF-US/IDAHO-VAULT.git 2>/dev/null; git fetch origin; git branch -u origin/main main 2>/dev/null
```

### Solution 2: Automatic Guardrail Wrapper

Two installable wrappers live in `scripts/`, one per platform. Both detect the
repo by its worktree folder name (`IDAHO-VAULT`), not by grepping the origin
remote's URL out of `.git/config` - that string is exactly what disappears
the moment `git remote remove origin` runs, which is the case the guard
exists to catch.

**macOS / Linux** - `scripts/git-guard.sh`

Install it as `~/bin/git` (the file must be named `git`, not `git-guard` -
naming it anything else means plain `git ...` calls never reach the wrapper):

```bash
mkdir -p ~/bin
cp scripts/git-guard.sh ~/bin/git
chmod +x ~/bin/git
```

Then make sure `~/bin` comes *before* the real git's directory on `PATH`:

```bash
export PATH="$HOME/bin:$PATH"
```

**Windows (PowerShell)** - `scripts/Invoke-GitGuard.ps1`

Dot-source it from your PowerShell profile so it loads in every session:

```powershell
. "<repo root>\scripts\Invoke-GitGuard.ps1"
```

This defines a `git` function that PowerShell resolves before `git.exe`, so
no PATH reordering, admin rights, or Git Bash/WSL install is required -
matching this vault's Windows-first operating constraints.

## Why Not Block Commands?

User explicitly rejected blocking solutions. The problem is agent behavior, not available commands. Agents need full git functionality.

## Implementation

- Immediate: Use Solution 1
- Long-term: Install Solution 2 (`scripts/git-guard.sh` or `scripts/Invoke-GitGuard.ps1`)
- Repo Machinery: This doc + the two wrapper scripts

## Verification

1. Install the wrapper for your platform (see Solution 2)
2. Run `git remote remove origin` (simulate breakage)
3. Run any git command, e.g. `git status`
4. Verify origin was automatically reconnected: `git remote -v`
