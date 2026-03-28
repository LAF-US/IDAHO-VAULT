---
tags:
  - administration/coordination
updated: 2026-03-25
status: active
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record).

---

## ACTIVE WORK

| Task                                | Owner       | Status      | Linear | Notes                                     |
| ----------------------------------- | ----------- | ----------- | ------ | ----------------------------------------- |
| THE COURTROOM coordination hub      | All agents  | In progress | LAF-7  | Docket/orientation only; no catch-all execution |
| Idaho Legislature scraper           | Claude Code | Running     | —      | Daily 6 AM MT, commits to main            |
| Vault sort audit                    | Automated   | Weekly      | —      | Monday 6 AM UTC                           |
| Wayback preservation                | Automated   | Weekly      | —      | Monday 8 AM UTC                           |
| Operation: Spring Clean             | Claude Code | In progress | —      | Branch graveyard, DOCKET/LEVELSET refresh |

## PROJECT-SCOPED WORK ITEMS (BROKEN OUT FROM LAF-7)

| Work item | Scope | Owner | Status | Linear | Notes |
| --------- | ----- | ----- | ------ | ------ | ----- |
| COURTROOM decomposition | Break standing docket into scoped issue slots and keep LAF-7 as hub | Codex | Done | LAF-12 | This issue delivers the decomposition structure in this file |
| Scraper operations | Idaho Legislature scraper runtime + reliability changes | Claude Code | In progress | _(create child issue)_ | Move all scraper implementation work out of LAF-7 |
| Automation maintenance | Vault sort audit + Wayback preservation workflow maintenance | Claude Code / Copilot | Planned | _(create child issue)_ | Keep operational fixes scoped to automation-only issue(s) |
| Branch hygiene | Branch cleanup, stale branch deletion workflow, and audit bookkeeping | Claude Code | In progress | _(create child issue)_ | Move Spring Clean execution updates to its own issue |
| Publication gatekeeping | JFAC quote audio verification and publication blocking checks | Logan | Blocked | _(create child issue)_ | Keep evidence gate work separate from coordination docket |

## RECENTLY COMPLETED

| Task                                                      | Completed  | Notes                                                                                       |
| --------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------- |
| LAF-1 — Linear onboarding resources                       | 2026-03-25 | Intro video and setup guides captured in `!/LINEAR-ONBOARDING.md`                           |
| LAF-3 — Connect your tools brief                          | 2026-03-25 | Brief filed at `!/BRIEF-LAF-3-2026-03-25.md`                                                |
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
| LAF-9 — Vault template + document class system            | 2026-03-25 | Drafted `VAULT-TEMPLATES.md`; linked from conventions + canonical README                   |

## BLOCKED / PENDING LOGAN

| Item                            | Blocker                                                                                                                                                                                                                                                                                                                                                                     | Who can unblock |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| Gemini capability tier          | Google Cloud `idaho-vault` project exists, APIs enabled, credentials not created — role decision required before any integration                                                                                                                                                                                                                                            | Logan           |
| `.obsidian/workspace.json`      | Tracked in git; should be untracked + gitignored — separate hygiene PR                                                                                                                                                                                                                                                                                                     | Logan           |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Q1 MCP disallowed? **No**. Q2 Transport-only with native terms canonical? **Yes (adopted)**. Q3 MCP primary integration model? **No**. Q4 Governance authority source? **Vault-native governance files/terms remain canonical**. Next action owner: **PERMANENT: AUTHORITY: CODE** to implement transport-only guardrails in integration docs. Unblock date: **2026-03-24**. | Logan           |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) — awaiting review/apply/discard decision                                                                                                                                                                                                                                                                                           | Logan           |
| Stale remote branches (6)       | Require manual deletion via GitHub web UI — `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16`                                                                                                                                                                                                                                    | Logan           |
| JFAC quote audio verification   | 5 quotes + speaker IDs — HARD GATE before publication                                                                                                                                                                                                                                                                                                                      | Logan           |
| Claude Chorus bootstrap         | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation.                                                                                                                           | Logan           |

### Chorus Bootstrap — Logan's Decisions Required

*Full context: `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`*

1. **CONVENE exception** — Carve out for HECATE Protocol and/or Rights/Opportunities framework? Or keep frozen? Unlocks Chorus Pieces 3, 4, 5.
2. **Grimoire directory** — Create `!/GRIMOIRE/`? If yes: `HECATE-HECATE-HECATE.md` is the first entry (triple invocation). If no: stage elsewhere.
3. **Rick & Morty doc** — "Rick and Morty object lessons" referenced in Chorus but not included in handoff. Surface for vault commit, or defer?
4. **Innie/Outie architecture** — Stage 8-part Severance-derived swarm architecture as proposal doc now, or mark premature under CONVENE?
5. **"Claude Chorus" naming** — Sanctioned swarm identity designation, or informal shorthand to discard?

---

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
