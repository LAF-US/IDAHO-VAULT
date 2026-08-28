# WITNESS � `.worktrees` reconciliation � 2026-08-17

## Outcome

No recovery payload was copied. The nested clone's tracked tip is cryptographically identical to a commit already reachable from the active branch. Files changed or removed after that counterpart are active-history decisions, not missing recovery cargo.

- Active: `logan/obsidian` at `b41f512fc189d3463f6a3b5431f743e795bd3db7`
- Recovery clone: `logan/obsidian` at `691e53087dcf787be683fbb8470fdfa28fa2f076`
- Exact active tree counterpart(s): `f61fd899b01d286e5ea9e7279de5bc1184a4c93b`
- Tracked source entries covered by that tree: **119,194**
- Recovery working-tree tracked changes: **0**
- Recovery working-tree untracked items: **1**

## Current-tip comparison

- Same path and blob: **118,518**
- Same path, later active content: **651**
- Removed after the rewritten counterpart: **25**
- Added after the rewritten counterpart: **1,127**

## History audit

- Old-only commits: **5,968**
- Active-only commits: **5,433**
- Patch-equivalent non-merge commits: **4,876**
- Patch-unique non-merge commits requiring approval: **150**
- Merge or empty commits excluded from automatic replay analysis: **942**
- Candidate classes: `{'heightened_manual_review': 62, 'manual_approval_candidate': 88}`

No commit was cherry-picked. Every patch-unique candidate remains approval-only. The pre-scrub alignment commit `5f34c105974176125ee9417f4fbcb8c5326def0c` is explicitly excluded.

### Exact-tree rewrite mappings near the abandoned tip

| Abandoned commit | Active counterpart | Subject |
| --- | --- | --- |
| `691e53087dcf` | `f61fd899b01d` | .md |
| `22c3c4334d5c` | `a9c585634632` | Restore approved public embed content after history token redaction |
| `4f249d1543db` | `deeda86a19d9` | LAF-79: adopt scrubbed reconciled vault tree |
| `b9270db288f4` | `deeda86a19d9` | LAF-79 raw reconciliation candidate |

## Exclusions and preservation

- `.worktrees/repos/IDAHO-VAULT/.git/` remains excluded Git metadata.
- `process-1774818543455-47088.log` remains uncopied because it is runtime material with secret indicators.
- `.worktrees` remains intact. Cleanup requires separate explicit authorization after commit and push verification.
- The active root remains the incumbent; no active file was overwritten, deleted, reset, stashed, or restored.

## Approval gate

The JSONL manifest records each of the 150 patch-unique candidates with raw-change digest, changed-path digest, bounded path sample, and risk markers. A candidate must pass manual diff review and secret/storage checks before Logan may approve an individual cherry-pick.
