---
authority: LOGAN
agent: Codex
created: 2026-06-18
observed_at: 2026-06-18T12:43:29-06:00
doc_class: status-snapshot
status: filed
tags:
  - snapshot
  - codex
  - config
  - sandbox
  - git-safety
related:
  - "CONSTITUTION.md"
  - "AGENTS.md"
  - "!/SNAPSHOT-GITHUB-CONFIG-ARBORSCAPE-SIGNING-CODEX-318-2026-06-03.md"
---

# Snapshot - Codex Config Rebalance - 2026-06-18

## Scope

This is a status snapshot and operational audit note. It records a local Codex
configuration change made after repeated Codex failures involving unauthorized
or confusing work surfaces, dangerous Git approvals, and ambiguous language
around checkout state.

No credentials are recorded here.

## Local Repository State

- Repository: `C:\Users\loganf\Documents\IDAHO-VAULT`
- Observed branch before and after the change: `codex/codex-work-surface-guard`
- Repo files were not cleaned, staged, restored, or otherwise edited as part of
  the Codex config rebalance.
- The checkout directory had unrelated dirty state from other agents at the
  time of observation. That state was deliberately left untouched.

Terminology correction for future Codex runs:

- Use `checkout directory` for the repo folder.
- Use `linked git worktree` only for checkouts created by `git worktree`.
- Use `working copy changes` for modified, added, deleted, or untracked files.
- Avoid the ambiguous phrase `working tree` in this repository context.

## Config Files Changed

Two global Codex files outside the vault were changed:

- `C:\Users\loganf\.codex\config.toml`
- `C:\Users\loganf\.codex\rules\default.rules`

Backups were created before editing:

- `C:\Users\loganf\.codex\config.toml.bak-20260618-124329-codex-config-rebalance`
- `C:\Users\loganf\.codex\rules\default.rules.bak-20260618-124329-codex-config-rebalance`

## Sandbox Policy

`config.toml` was changed from read-only sandboxing to workspace-write
sandboxing:

```toml
sandbox_mode = "workspace-write"
```

Verified state after the edit:

- `sandbox_mode` parsed as `workspace-write`.
- The only trusted Codex project was
  `c:\users\loganf\documents\idaho-vault`.
- Windows sandbox remained `unelevated`.

The intent is not maximum restriction. The intent is to let Codex collaborate
inside the authorized vault checkout while removing broad Git powers that were
more dangerous than ordinary file edits.

## Git Approval Hardening

`default.rules` was rewritten so 73 previously allowed dangerous command
prefixes now have `decision="deny"`.

Denied categories include:

- broad staging and committing: `git add`, `git commit`
- branch/ref/history mutation: `git switch`, `git checkout`, `git reset`,
  `git restore`, `git cherry-pick`, `git merge`, `git rebase`, `git stash`,
  `git update-ref`, `git symbolic-ref`, `git read-tree`, `git commit-tree`
- publishing: `git push`, `git push origin`, `git push origin main`,
  `git push origin HEAD`
- linked git worktree mutation: `git worktree add`, `git worktree remove`,
  `git worktree prune`
- PowerShell or shell wrapper approvals that embedded dangerous Git operations

Allowed read-only Git inspection remains intentionally narrow:

- `git status`
- `git diff`
- `git log`
- `git show`
- `git rev-parse`
- `git ls-files`
- `git worktree list`
- exact branch inspection commands:
  - `git branch --show-current`
  - `git branch -vv`
  - `git branch -a`
  - `git branch -r`

Broad `git branch` is denied because the prefix can also cover branch deletion
or branch creation commands.

## Verification Performed

After the edit:

- `config.toml` was parsed with Python `tomllib`.
- The parsed sandbox mode was `workspace-write`.
- The parsed trusted project list contained only the IDAHO-VAULT path.
- A search for remaining allowed shell-wrapper rules containing `git` returned
  no matches.
- A direct-rule scan showed the dangerous Git prefixes as denied and the exact
  read-only branch inspection exceptions as allowed.
- The current branch still reported `codex/codex-work-surface-guard`.

A Git status check against the external config paths failed because those files
are outside the vault repository. That is expected and was not treated as a
config failure.

## Caveats

This change affects future Codex behavior more reliably than an already-running
session. The active session may still have prompt-level approved command
prefixes loaded from before the rewrite.

The change does not make Git impossible to use. It removes standing approval for
the classes of Git command that caused or could cause checkout confusion,
branch/ref damage, linked-worktree side effects, unsafe staging, unsafe
commits, and unsafe pushes. Those operations should require explicit,
context-specific approval.

Repo-level guardrails remain useful, but the durable enforcement layer for
Codex command approval is the global Codex rules file, not an `AGENTS.md`
reminder.

## Filed Statement

Codex configuration was rebalanced toward collaborative vault editing with
dangerous Git operations no longer pre-approved. The vault should be used as
the shared tracked work surface, not bypassed through unauthorized linked git
worktrees or hidden temporary checkouts. Future agents should verify the
checkout directory, branch, and working copy changes before writing, and should
use precise terminology when reporting state.
