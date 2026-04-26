---
updated: 2026-04-26
status: ACTIVE - BIG PICKLE WORK IN PROGRESS
date created: Monday, March 30th 2026, 7:54:37 pm
date modified: Sunday, April 26th 2026
---

# THE DOCKET

This is the live **Pending-Logan agenda unit**. Any agent arriving at THE COURTROOM reads the top of this file to orient to what presently needs Logan's eyes, decision, approval, or unblock.

## LIVE PENDING LOGAN

| Item | Logan action needed | Current read | Source |
| --- | --- | --- | --- |
| **Automation Unification (Phase 1)** | Approve consolidation | COMPLETED 2026-04-26 | Big Pickle session |

## ACTIVE WORK IN PROGRESS

| Item | Agent | Status | Notes |
|---|---|---|
| PR Loop Fix | Big Pickle | ✅ COMPLETED | Fixed pr_loop_watchdog.py syntax error, merged PR #307 |
| agent-auto-pr unification | Big Pickle | ✅ COMPLETED | Now handles all agent/bot/dependabot origins |
| dependabot-rhythm merge | Big Pickle | ✅ COMPLETED | Deleted dependabot-rhythm.yml |
| Branch prefix docs | Big Pickle | ✅ COMPLETED | Added to AGENTS.md |
| branch-cleanup + stale-bot consolidation | Big Pickle | ⏳ PENDING | Next candidate for unity |

## PENDING CONSOLIDATION

Remaining workflow redundancies:

| Candidate | Current | Action |
|---|---|---|
| stale-bot-prs.yml + branch-cleanup.yml | 2 | Merge into branch-cleanup |
| linear-pr-sync + linear-webhook + linear-brief | 3 | Distinct purposes - KEEP |

## SIGNALS FOR LOGAN

- automation unification: Phase 1 complete ~ 30 → 29 workflows
- Branch prefix standard now in AGENTS.md (canonical)
- pr_loop_watchdog.py fixed on main (was syntax error)
- All agent/bot/dependabot now covered by agent-auto-pr

## DONE

- ✅ dependabot-rhythm.yml deleted
- ✅ Branch prefix standard documented in !/AGENTS.md
- ✅ pr_loop_watchdog.py syntax error healed
- ✅ agent-auto-pr.yml unified trigger for all origins
- ✅ PR #307 merged to main

---

## COURTROOM BOUNDARY

Use this board to surface only live Logan-facing motion.

- Keep only what Logan needs immediately
- Route detailed task state to Linear and GitHub
- When resolved, move off live queue

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues.