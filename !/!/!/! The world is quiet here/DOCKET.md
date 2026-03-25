---
tags:
  - administration/coordination
updated: 2026-03-25
status: active
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

---

## ACTIVE WORK

| Task                                | Owner       | Status      | Linear | Notes                                     |
| ----------------------------------- | ----------- | ----------- | ------ | ----------------------------------------- |
| Swarm coordination — agent assembly | All agents  | In progress | LAF-7  | Agents finding each other                 |
| Linear workspace team setup         | GitHub Copilot | In progress | LAF-2  | Configure teams/members/roles in Linear   |
| Idaho Legislature scraper           | Claude Code | Running     | —      | Daily 6 AM MT, commits to main            |
| Vault sort audit                    | Automated   | Weekly      | —      | Monday 6 AM UTC                           |
| Wayback preservation                | Automated   | Weekly      | —      | Monday 8 AM UTC                           |
| Operation: Spring Clean             | Claude Code | In progress | —      | Branch graveyard, DOCKET/LEVELSET refresh |
| Connect your tools brief            | Copilot     | Complete    | LAF-3  | Brief filed at `!/BRIEF-LAF-3-2026-03-25.md` |

## RECENTLY COMPLETED

| Task                                                      | Completed  | Notes                                                                                       |
| --------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------- |
| LAF-1 — Linear onboarding resources                       | 2026-03-25 | Intro video and setup guides captured in `!/LINEAR-ONBOARDING.md`                           |
| PR #34 — Obsidian vault update (42 files)                 | 2026-03-23 | Merged via `copilot/deploy-dependabot-configurations`                                       |
| PR #39 — Get scrapers running                             | 2026-03-24 | Merged; scraper now on main, running daily                                                  |
| PR #40 — CodeRabbit GitHub integration                    | 2026-03-23 | Merged                                                                                      |
| PR #44 — REST API credential sanitization                 | 2026-03-24 | Merged; machine credentials purged from repo                                                |
| PR #46 — Workflow centralization + settings.json fix      | 2026-03-24 | Merged; composite action, zombie `!ADMINISTRATION/` paths fixed                             |
| PR #43 — Codex credential sanitization                    | 2026-03-24 | Closed as superseded by PR #44                                                              |
| GEMINI.md update                                          | 2026-03-24 | Direct commit by Logan                                                                      |
| PR #48 — CONSTITUTION.md LEVELSET path fix                | 2026-03-23 | Merged; zombie `!ADMIN/LEVELSET-v3.2.6.1-PROMPT.md` → `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` |
| PR #50 — CONSTITUTION.md AGENTS.md location fix           | 2026-03-23 | Merged; decision 9 summary corrected to repo root                                           |
| PR #51 — auto-pr YAML fix (heredoc → printf)              | 2026-03-24 | Incorporated into PR #57; fixes workflow parse failures on every push                       |
| PR #52 — Governance docs formatting normalization         | 2026-03-24 | Incorporated into PR #57                                                                    |
| PR #53 — Decision 16 (MCP governance), DOCKET + LEVELSET | 2026-03-24 | Incorporated into PR #57                                                                    |
| PR #54 — Compact MCP mapping in PROTOCOL.md              | 2026-03-24 | Incorporated into PR #57                                                                    |
| PR #55 — MCP implementation plan (new file)               | 2026-03-24 | Incorporated into PR #57                                                                    |
| PR #56 — MCP action logging template in VAULT-CONVENTIONS | 2026-03-24 | Incorporated into PR #57                                                                    |

## BLOCKED / PENDING LOGAN

| Item                            | Blocker                                                                                                                                                                                                                                                                                                                                                                     | Who can unblock |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| Gemini capability tier          | Google Cloud `idaho-vault` project exists, APIs enabled, credentials not created — role decision required before any integration                                                                                                                                                                                                                                            | Logan           |
| `.obsidian/workspace.json`      | Tracked in git; should be untracked + gitignored — separate hygiene PR                                                                                                                                                                                                                                                                                                     | Logan           |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Q1 MCP disallowed? **No**. Q2 Transport-only with native terms canonical? **Yes (adopted)**. Q3 MCP primary integration model? **No**. Q4 Governance authority source? **Vault-native governance files/terms remain canonical**. Next action owner: **PERMANENT: AUTHORITY: CODE** to implement transport-only guardrails in integration docs. Unblock date: **2026-03-24**. | Logan           |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) — awaiting review/apply/discard decision                                                                                                                                                                                                                                                                                           | Logan           |
| Stale remote branches (6)       | Require manual deletion via GitHub web UI — `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16`                                                                                                                                                                                                                                    | Logan           |
| JFAC quote audio verification   | 5 quotes + speaker IDs — HARD GATE before publication                                                                                                                                                                                                                                                                                                                      | Logan           |

## WHERE THINGS LIVE

| What                     | Where                                                       |
| ------------------------ | ----------------------------------------------------------- |
| Agent instructions       | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md`                                      |
| Confirmed decisions      | `DECISIONS.md`                                              |
| Automation scripts       | `.github/scripts/`                                          |
| Automation workflows     | `.github/workflows/`                                        |
| Task coordination        | Linear (SWARM label) + GitHub Issues (`agent:*` labels)     |
| Breadcrumbs              | Slack #general                                              |

## COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live status board. Update it when you start or finish work.

---

###### [["The world is quiet here."]]
