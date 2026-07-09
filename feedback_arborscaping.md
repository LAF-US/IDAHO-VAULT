---
name: Arborscaping — deletion is last resort
description: Arborscaping doctrine for IDAHO-VAULT branch/worktree/PR management; deletion and disabling are never invoked lightly
type: feedback
originSessionId: arborscaping-2026-05-25
---

**Arborscaping** is the IDAHO-VAULT protocol for GitHub branch, worktree, and PR management. It is trunk-directed: all work moves toward the accepted `main` trunk.

## The Three Actions (in order)

1. **SALVAGE** — preserve and identify unique payload before any structural change. Default action.
2. **CHERRY-PICK** — lift specific useful commits, files, or notes into the accepted trunk when full salvage isn't appropriate.
3. **PRUNE** — remove or archive stale shells *only* after salvage and cherry-pick checks show no unique payload, and *only* with Logan's explicit approval.

## Critical Rule

> **Deletion and disabling are the final last resort and must never be invoked lightly.**

Do not classify a branch as PRUNE candidate based on surface-level checks (filename match, file existence in trunk). You must verify actual content — including diffs and byte-level comparison — before recommending deletion.

## Orphan History Warning

Local IDAHO-VAULT branches may be **orphan histories** (no shared commits with origin/main) from before a vault history rewrite. Standard `git branch --merged` and `git rev-list --count` comparisons give misleading results for orphan branches. Always check:
```bash
git merge-base <branch> origin/main
```
before drawing any conclusions about a branch's relationship to trunk.

## Arborscaping Source Files

- `!-ARBORSCAPING-REPORT-2026-04-16.md` — first baseline report
- `LOCAL-ARBORSCAPE-IDAHO-VAULT-SPLINTERS-2026-05-09.md` — Windows splinter census
- `!-ARBORSCAPING-REPORT-2026-05-24.md` — Mac census (this session; git pull completed, branch inspection in progress)
- `.github/scripts/branch_garden_report.py` — automation machinery
