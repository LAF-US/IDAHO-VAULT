# Agent Git Guardrails - Issue & Solutions

## Problem Statement

Agents (Vibe CLI, Claude, and others) repeatedly run destructive git commands that break local repository remote tracking. This manifests as GitHub Desktop asking to "publish repository" instead of fetch/push/pull, lost remote origin configuration, and broken branch upstream tracking.

### Root Cause

Agents misanalyze git history, conclude files need to be "scrubbed" from history, then run history-rewriting commands (git filter-branch, git filter-repo). These rewrite commit SHAs and break remote tracking. The agents analysis is often wrong - false positives on file existence in history.

## Proposed Solutions

### Solution 1: One-Liner Fix (Manual)

For immediate recovery:

```bash
git remote add origin https://github.com/LAF-US/IDAHO-VAULT.git 2>/dev/null; git fetch origin; git branch -u origin/main main 2>/dev/null
```

### Solution 2: Automatic Guardrail Wrapper

Create ~/bin/git-guard:

```bash
#!/bin/sh
REPO_URL="https://github.com/LAF-US/IDAHO-VAULT.git"
if [ -d .git ] && grep -q "IDAHO-VAULT" .git/config 2>/dev/null; then
  if ! git remote | grep -q origin; then
    git remote add origin "$REPO_URL"
    git fetch origin 2>/dev/null
    git branch --set-upstream-to=origin/main main 2>/dev/null
  fi
fi
exec /usr/bin/git "$@"
```

Prepend to PATH: export PATH="$HOME/bin:$PATH"

## Why Not Block Commands?

User explicitly rejected blocking solutions. The problem is agent behavior, not available commands. Agents need full git functionality.

## Implementation

- Immediate: Use Solution 1
- Long-term: Implement Solution 2
- Repo Machinery: This doc + optional wrapper script

## Verification

1. Run git remote remove origin (simulate breakage)
2. Run any git command with wrapper installed
3. Verify automatic reconnection