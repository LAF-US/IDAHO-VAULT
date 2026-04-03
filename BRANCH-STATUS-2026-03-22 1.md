---
type: branch-status-report
date: 2026-03-22
compiled-by: claude/github-agent-setup-1N07i
main-head: 932bab7
---

# Branch Status Report — 2026-03-22

## Executive Summary

**Status:** 15 active feature branches; 4 are merge-ready (ahead of main); 9 are stale (behind main).

| Category | Count | Action |
|----------|-------|--------|
| **Merge-Ready** | 4 | Prioritize for PR review |
| **Blocked/Stale** | 9 | Rebase or close per Logan direction |
| **Collision Risk** | 1 | `levelset-current-synthesis-zWxJc` conflicts with merged `levelset-multi-conversation-zWxJc` |

---

## MERGE-READY BRANCHES (Ahead of Main)

### 1. `claude/levelset-current-synthesis-zWxJc`
- **Status:** ⚠️ COLLISION — branch ancestor merged as PR #15; this branch has 3 new commits
- **Ahead:** 3 commits
- **Latest commit:** `1d63124` — "Append 7 approved decisions to DECISIONS.md, hold #8 pending taxonomy"
- **Content:**
  - `!ADMINISTRATION/LEVELSET-CURRENT.md` (old dir structure)
  - `!ADMINISTRATION/LEVELSET-v2.md`
  - `LEVELSET 1.md`, `LEVELSET 2.md` (root)
  - `DECISIONS.md` (root, 7 approved decisions)
- **Issue:** Uses obsolete `!ADMINISTRATION/` folder; main uses `!ADMIN/`. Needs rebase + refactoring.
- **Recommendation:** ⏸️ HOLD — Rebase onto main, migrate to `!ADMIN/` structure, or cherry-pick DECISIONS.md commits.

### 2. `claude/context-persistence-system-gVP3x`
- **Status:** ✅ Clean merge candidate
- **Ahead:** 2 commits
- **Latest commit:** `bda1a16` — "Merge origin/main — resolve swarm/ conflicts with populated main versions"
- **Content:** Swarm coherence work; already merged main into branch (clean state)
- **Recommendation:** ✅ MERGE — Ready for PR review.

### 3. `claude/levelset-multi-conversation-zWxJc`
- **Status:** ⚠️ MOSTLY MERGED — PR #15 merged ancestor; branch is 1 commit ahead
- **Ahead:** 1 commit
- **Latest commit:** `3fb4daf` — "Align all agent instruction files to post-flatten vault structure"
- **Content:** Post-merge alignment work; uses correct `!ADMIN/` structure
- **Recommendation:** ✅ MERGE — Fast-forward should apply cleanly.

### 4. `claude/public-conversation-setup-zl2oe`
- **Status:** ✅ Independent work
- **Ahead:** 4 commits
- **Latest commit:** `fc4fd9d` — "Loosen auto-merge threshold so Logan reviews fewer PRs"
- **Content:** Conversation infrastructure setup
- **Recommendation:** ✅ MERGE — No structural conflicts visible; review for content.

### Copilot Branches
- `copilot/check-public-repo` — 2 commits ahead
- `copilot/collaboration-context-unification` — 4 commits ahead
- `copilot/deploy-dependabot-configurations` — 3 commits ahead

All appear independent; recommend review before merge.

---

## STALE BRANCHES (Behind Main)

These branches are 15+ commits behind main and likely need rebasing or closure:

| Branch | Behind | Latest Commit | Action |
|--------|--------|---------------|--------|
| `claude/fix-swarm-alert-DIIQq` | 131 | 447c38c (swarm consolidation flag) | Rebase or close |
| `claude/github-agent-setup-1N07i` | 133 (self) | 2f51dc3 (idaho-scraper LEVELSET v3.2.6) | N/A — current branch |
| `claude/idaho-legislature-scraper-RI6Ku` | 133 | 2f51dc3 (same as above) | Archive — scraper terminated |
| `claude/review-code-task-plan-FB4jo` | 15 | 948aab6 (agent roles CSV) | Rebase or scope out |
| `copilot/consolidate-copilot-efforts` | 31 | af82c33 (merged main) | Rebase or close |
| `copilot/emergency-handoff-swarm-coherence` | 78 | dbb208a (swarm dir) | Rebase or close |
| `copilot/fix-idaho-legislature-scraper` | 26 | d3368d8 (initial plan) | Rebase + review |
| `copilot/fix-token-permissions-and-error-handling` | 115 | 0e4d3d8 (scraper error logging) | Rebase + review |
| `copilot/setup-copilot-instructions` | 115 | 868dd58 (copilot instructions) | Rebase + review |

---

## COLLISION RISKS

### Primary: `levelset-current-synthesis-zWxJc`
- **Problem:** Branch was created to synthesize LEVELSET-CURRENT.md but uses obsolete `!ADMINISTRATION/` folder name.
- **Solution:** Either:
  - Option A: Rebase onto main, migrate files to `!ADMIN/`, merge
  - Option B: Cherry-pick DECISIONS.md commits only (decision log is valuable)
  - Option C: Close branch as superseded by PR #15 merge

---

## KNOWN ARTIFACTS & ISSUES

1. **`pull_requests/1.md`** — Copilot artifact on one of the branches (misexecuted PR creation). Mark for deletion before merge.
2. **Unbuilt workflows** (deferred from scraper conversation):
   - `idaho-leg-setup.yml` — Label/issue bootstrap
   - `idaho-leg-bill-lookup.yml` — Mobile single-bill lookup
3. **Scraper branch dangling** — `claude/idaho-legislature-scraper-RI6Ku` terminated cleanly but left on origin.

---

## RECOMMENDED MERGE SEQUENCE

### Immediate (This Week)
1. ✅ `claude/levelset-multi-conversation-zWxJc` — Fast-forward merge (1 commit)
2. ✅ `claude/context-persistence-system-gVP3x` — Clean merge candidate (2 commits)
3. ✅ `claude/public-conversation-setup-zl2oe` — Review + merge (4 commits)

### Pending Logan Decision
- ⏸️ `claude/levelset-current-synthesis-zWxJc` — Rebase + refactor OR cherry-pick OR close
- 📋 Copilot branches (4) — Prioritize which are needed; rebase/review/merge accordingly

### Archive/Close
- 🗑️ `claude/github-agent-setup-1N07i` (current, stale — rebased onto main)
- 🗑️ `claude/idaho-legislature-scraper-RI6Ku` (scraper terminated)
- 🗑️ Stale copilot branches (9) — Consolidate or close per Logan

---

## Next Steps for Logan

1. **Approve merge sequence** — Which branches should merge this week?
2. **Resolve `levelset-current-synthesis-zWxJc` collision** — Rebase + migrate, cherry-pick, or close?
3. **Review Copilot branches** — Consolidate or close outdated ones?
4. **Delete artifacts** — `pull_requests/1.md` before final merge
5. **Rebase stale branches** — Any still needed should be updated

---

*Report compiled by PERMANENT: AUTHORITY: CODE after rebase to origin/main 932bab7*
