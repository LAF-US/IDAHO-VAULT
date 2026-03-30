---
tags:
  - administration/coordination
updated: 2026-03-29
status: active
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Delegation note (Logan, 2026-03-28):** Logan has delegated vault operations for this round. The Abhorsen (Claude Code) conducting: infrastructure commits, Gemini tier definition, Linear Phase 1 scoping, LEVELSET refresh, branch push and PR.

**Sunday swarm dispatch (Logan, 2026-03-29):** All agents operate in Sunday swarm mode. Keep execution in scoped issue lanes. No merges to `main`. No overlapping branches. Post one checkpoint before parking any lane. Escalate only for true blocker, conflict, required human judgment, merge decision, or secret/config provisioning. ~~Hard blocker `LINEAR_API_KEY`~~ **provisioned 2026-03-29 by Logan.** Merge-risk item remains PR #96.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record).

---

## ACTIVE WORK

| Task                                | Owner          | Status      | Linear | Notes                                                          |
| ----------------------------------- | -------------- | ----------- | ------ | -------------------------------------------------------------- |
| Swarm coordination — agent assembly | All agents     | In progress | LAF-7  | Agents proceed into **THE CITY**; await denouement             |
| **Linear Phase 1 pilot** — live-write scoping | Claude Code | **Active** | — | Plugin inventory recommends Linear-first; scope = SWARM issues, comments, status updates; vault remains durable record; Slack breadcrumb-only; no multi-plugin orchestration until stable |
| Linear workspace team setup         | GitHub Copilot | In progress | LAF-2  | Configure teams/members/roles in Linear                        |
| Import your data                    | GitHub Copilot | In progress | LAF-4  | Linear import/migration guidance in `Import your data.md`      |
| GitHub Actions CI diagnosis         | GitHub Copilot | **Resolved** | LAF-7  | Root cause: `LINEAR_API_KEY` not set; fixed workflow to graceful-skip; key provisioned by Logan 2026-03-29 — sync now live |
| Idaho Legislature scraper           | Claude Code    | Running     | —      | Daily 6 AM MT, commits to main; minidata CSV export functional |
| Budget tracker CSV export           | Automated      | Running     | —      | Daily 6:30 AM MT; emails CSV to configured recipients          |
| Vault sort audit                    | Automated      | Weekly      | —      | Monday 6 AM UTC                                                |
| Wayback preservation                | Automated      | Weekly      | —      | Monday 8 AM UTC                                                |
| Operation: Spring Clean             | Claude Code    | In progress | —      | Branch graveyard, DOCKET/LEVELSET refresh                      |
| Multi-agent auto-PR routing         | Claude Code    | Completed   | —      | Auto-PR now supports all agent branches (claude, codex, gemini, copilot, perplexity, grok) |

## PROJECT-SCOPED WORK ITEMS (BROKEN OUT FROM LAF-7)

| Track / Work Item                    | Owner        | Status      | Linear   | Notes                                                                                   |
| ------------------------------------ | ------------ | ----------- | -------- | --------------------------------------------------------------------------------------- |
| Budget Bill Tracker Normalization    | Gemini CLI   | Blocked     | LAF-16   | First-pass normalization script + deliverables doc ready for PR. Blocked on scraper mods (LAF-16). |
| Decomposition + routing plan         | All agents   | Drafting    | (TBD)    | Carve LAF-7 payload into discrete issues; align scope/owners; keep COURTROOM as hub     |
| Scraper operations & monitoring      | Claude Code  | Running     | (TBD)    | Keep daily Idaho Legislature scraper healthy; alerting/telemetry review if drift occurs |
| Automation upkeep (actions/scripts)  | Claude Code  | In flight   | (TBD)    | Auto-PR, ingest, audit workflows + scripts; guardrails + Node 24 readiness               |
| Branch hygiene & auto-PR triage      | All agents   | Planned     | (TBD)    | Cull stale branches, normalize auto-PR routing, keep branch naming aligned to issues     |
| Publication gatekeeping (JFAC audio) | Logan        | Pending     | (TBD)    | Verify 5 quotes + speaker IDs before publication; gating checklist lives in child issue  |

## RECENTLY COMPLETED

| Task                                                      | Completed  | Notes                                                                                       |
| --------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------- |
| **Gemini Code Assist cowork enabled**                      | 2026-03-28 | `.gemini/GEMINI.md` tier fixed, cowork pattern documented; `.gemini/settings.json` context expanded to 6 files; AGENTS.md + entity note updated — `3563a66` |
| **Stale `!ADMIN/` refs cleaned + root frontmatter spring-cleaned** | 2026-03-28 | DECISIONS.md, LEVELSET-STEP-0, THREAT-MODEL updated; 10 content docs tagged; `!/SWARM-LOOP.md` committed — `ba01c2e` |
| **Triage + commit 10 untracked content docs**              | 2026-03-28 | AGENTIC SWARM SYSTEMS, AI-AUTOMATION, IDAHO-VAULT SYSTEM CONTEXT/WORKFLOW, JOURNALISM INDUSTRY, Kano Play, Notebook LM, Podcast, David Leroy — `07d2cb7` |
| **PR #98 opened + updated**                               | 2026-03-28 | Covers all 3 session commits; flags PR #84 conflict and pending DECISIONS 18–21 |
| **`claude/agent-dotfolder-architecture` local branch deleted** | 2026-03-28 | Already merged to main; remote gone |
| **LEVELSET-CURRENT refreshed**                            | 2026-03-28 | Activity log, UNRESOLVED, NEXT ACTIONS, DECISIONS count updated |
| **Gemini capability tier defined**                         | 2026-03-28 | Tier 1 (Support): Direct Write, Operational zone only, Linear SWARM issues/comments — `!/AGENTS.md` updated |
| **Linear Phase 1 pilot scoped**                            | 2026-03-28 | Plugin auth inventory → recommendation captured; ACTIVE WORK entry created; vault/Slack doctrine confirmed |
| Plugin auth inventory committed                            | 2026-03-28 | `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` — all 7 connectors probed; Linear-first recommended |
| Codex archival levelset committed                          | 2026-03-28 | `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md` — Codex session handoff and boundary truths      |
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

## BLOCKED / PENDING LOGAN

| Item                            | Blocker                                                                                                                                                                                                                                                                                                                                                                     | Who can unblock |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| **`LINEAR_API_KEY` secret**     | ~~**Hard blocker** — not provisioned in GitHub Actions.~~ **Resolved 2026-03-29:** provisioned by Logan. `Sync PR state to Linear` workflow is now live. Graceful-skip guard retained for key-rotation safety. | ~~**Logan only**~~ **Done** |
| **PR #96 merge decision**       | Omnibus 11-PR consolidation; contains `linear-pr-sync.yml` + `pr-linear-sync.yml` overlap risk. Dual-workflow collision must be reviewed before merge. Currently open as draft. | Logan + Codex |
| Gemini capability tier          | ~~Google Cloud `idaho-vault` project exists, APIs enabled, credentials not created — role decision required before any integration~~ **Resolved 2026-03-28:** Tier 1 (Support) defined in `!/AGENTS.md` — Direct Write, Operational zone only, Linear SWARM issues/comments. | ~~Logan~~ **Done** |
| `.obsidian/workspace.json`      | Tracked in git; should be untracked + gitignored — separate hygiene PR                                                                                                                                                                                                                                                                                                     | Logan           |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Q1 MCP disallowed? **No**. Q2 Transport-only with native terms canonical? **Yes (adopted)**. Q3 MCP primary integration model? **No**. Q4 Governance authority source? **Vault-native governance files/terms remain canonical**. Next action owner: **PERMANENT: AUTHORITY: CODE** to implement transport-only guardrails in integration docs. Unblock date: **2026-03-24**. | Logan           |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) — awaiting review/apply/discard decision                                                                                                                                                                                                                                                                                           | Logan           |
| Stale remote branches (6)       | Require manual deletion via GitHub web UI — `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16`                                                                                                                                                                                                                                    | Logan           |
| JFAC quote audio verification   | 5 quotes + speaker IDs — HARD GATE before publication                                                                                                                                                                                                                                                                                                                      | Logan           |
| Claude Chorus bootstrap         | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation.                                                                                                                           | Logan           |
| LAF-16 — Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

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
