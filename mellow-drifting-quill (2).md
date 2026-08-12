# Plan: Sunday-close PR triage + swarm handoff

## Context
End of Sunday swarm session. Repair work complete (DECISIONS.md restored, GEMINI.md guardrail landed, settings.json hook corrected, LAF-7 Linear note posted). Gemini restarted clean. Codex ready for next lane. Three PRs are open. LAF-16 is flagged due today. This plan triages what's safe to act on now vs. what holds for Logan's review later.

---

## Open PR assessment

### PR #102 — LAF-7: Fix Linear sync CI noise (Copilot, draft)
**Change:** `linear-pr-sync.yml` — `sys.exit(1)` → `sys.exit(0)` for missing `LINEAR_API_KEY`. Also touches `DOCKET.md`.
**Risk:** Low on the code change. The `sys.exit(0)` graceful degradation is correct and safe — key is now provisioned but rotation/expiry scenarios are covered.
**Concern:** `DOCKET.md` is also modified on `claude/resolve-pr-conflicts` (our current branch). If PR #102 merges to main first, the DOCKET change could conflict on our branch. Needs a quick diff check before merge.
**Verdict:** Safe to merge after confirming no DOCKET.md conflict with our working tree.

### PR #103 — ci: update Node.js 20 actions to Node.js 24 (Copilot, draft)
**Change:** Updates deprecated Node.js 20 action versions to Node.js 24-compatible versions across `.github/workflows/`.
**Risk:** Low — maintenance update, no logic changes. Node 24 readiness was already noted as an in-flight automation upkeep item in DOCKET.
**Verdict:** Safe to merge. Logan should mark ready for review (undraft) and merge.

### PR #96 — Omnibus consolidation (Copilot, draft)
**Change:** Consolidates 11 PRs including LAF-15 sync work, vault standards, Linear Gateway.
**Risk:** HIGH — both `linear-pr-sync.yml` and `pr-linear-sync.yml` converted to `workflow_call:` only with no caller. Sync silently disappears after merge.
**Verdict:** HOLD. Do not merge until Codex resolves the trigger chain (rebase LAF-15 branch, delete v1, submit clean PR with direct trigger).

---

## LAF-16 status
Gemini artifacts (`normalize_budget_data.py`, `deliverables.md`) are untracked on `claude/resolve-pr-conflicts`. Gemini's lane is blocked (upstream scraper mod out of scope for Sunday). Copilot has the pickup signal via LAF-16 Linear comment. No further action needed from Claude today — Copilot owns the PR creation.

---

## Actions for this plan

### 1. Check DOCKET.md conflict risk before recommending PR #102 merge
Run: `git diff HEAD -- "!/!/!/! The world is quiet here/DOCKET.md"` to see what our branch has vs what PR #102 changes. Report to Logan.

### 2. Confirm PR #102 merge recommendation to Logan
If no conflict: recommend Logan undraft + merge PR #102.
If conflict: flag the specific lines and let Logan resolve.

### 3. Confirm PR #103 merge recommendation to Logan
Recommend Logan undraft + merge PR #103 (Node.js 24 update, low risk).

### 4. Confirm PR #96 hold
Restate the hold with one-line rationale for Logan's review queue.

### 5. Post a brief LAF-7 Sunday-close checkpoint to Linear
One short comment: what landed today, what's holding, what's next. Clean end-of-day record.

---

## What this plan does NOT do
- Does not touch PR #96 or the Codex LAF-15 branch
- Does not commit LAF-16 artifacts (Copilot's lane)
- Does not add the Claude-side Linear guardrail to CLAUDE.md (separate follow-up)
- Does not merge anything without Logan's explicit instruction

---

## Critical files
- `.github/workflows/linear-pr-sync.yml` — changed in PR #102
- `!/!/!/! The world is quiet here/DOCKET.md` — changed in PR #102 AND in our working tree
- `.github/workflows/*.yml` — changed in PR #103 (Node.js 24 actions)

## Verification
- After PR #102 merges: next PR event should produce a green `sync` check (key is provisioned)
- After PR #103 merges: workflow runs should no longer show Node.js 20 deprecation warnings
- PR #96: remains draft/hold, no change
