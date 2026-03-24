---
tags:
  - administration/coordination
updated: 2026-03-23
status: active
---
# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

---

## ACTIVE WORK

| Task | Owner | Status | Linear | Notes |
|------|-------|--------|--------|-------|
| Swarm coordination — agent assembly | All agents | In progress | LAF-7 | Agents finding each other |
| Idaho Legislature scraper | Claude Code | Running | — | Daily 6 AM MT, commits to main |
| Vault sort audit | Automated | Weekly | — | Monday 6 AM UTC |
| Wayback preservation | Automated | Weekly | — | Monday 8 AM UTC |
| PR #35 — Vault settings + MCP workflows | Copilot | Draft (7/8 tasks) | — | Needs scoping review |
| PR #34 — Obsidian vault update | Logan | Open | — | 42 files — needs breakdown |
| PR #24 — Fix scraper workflow | Copilot | Draft (6/9 tasks) | — | WIP |

## BLOCKED

| Item | Blocker | Who can unblock |
|------|---------|-----------------|
| Gemini capability tier | Undefined — no vault commits until scoped | Logan |
| Copilot non-vault repo boundaries | TBD | Logan |
| 6 stale `claude/` remote branches | Need cleanup or close | Claude Code |
| 10 stale `copilot/` remote branches | Need cleanup or close | Logan / Claude Code |

## WHERE THINGS LIVE

| What | Where |
|------|-------|
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Confirmed decisions | `DECISIONS.md` |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| Task coordination | Linear (SWARM label) + GitHub Issues (`agent:*` labels) |
| Breadcrumbs | Slack #general |

## COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live status board. Update it when you start or finish work.

---

###### [["The world is quiet here."]]
