---
updated: 2026-04-12
status: AFK - SWARM OPERATIONAL
date created: Monday, March 30th 2026, 7:54:37 pm
date modified: Sunday, April 12th 2026, 10:30:00 pm
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Operator note (Codex, 2026-04-09):** Secondary background worktree exposed a real LF/CRLF normalization issue across vault notes. Defer normalization until after the repo history rewrite on a clean `main` base.

**Sleep-state note (Codex, 2026-04-12):** Workspace parked for Janitor re-entry. Lane split confirmed: GitHub org migration, what3words API restriction/quota, Claudius intake/binding, and Obsidian plugin mechanics remain separate. See `[[HANDOFF-CODEX-SLEEP-PARKING-2026-04-12]]`.

**Delegation note (Logan, 2026-03-28):** Logan has delegated vault operations for this round. The Abhorsen (Claude Code) conducting: infrastructure commits, Gemini tier definition, Linear Phase 1 scoping, LEVELSET refresh, branch push and PR.

**Sunday swarm dispatch (Logan, 2026-03-29):** All agents operate in Sunday swarm mode. Keep execution in scoped issue lanes. No merges to `main`. No overlapping branches. Post one checkpoint before parking any lane. Escalate only for true blocker, conflict, required human judgment, merge decision, or secret/config provisioning. ~~Hard blocker `LINEAR_API_KEY`~~ **provisioned 2026-03-29 by Logan.** Merge-risk item remains PR 96.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`), repair brief (`[[BRIEF-LAF-28-2026-04-02]]`), repair handoff (`[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]`), sleep parking (`[[HANDOFF-CODEX-SLEEP-PARKING-2026-04-12]]`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record).

---

## ACTIVE WORK

| Task | Owner | Status | Linear | Notes |
| --- | --- | --- | --- | --- |
| Swarm coordination - agent assembly | All agents | In progress | LAF-7 (Hub) / LAF-25 (Audit) | Sunday swarm mode - hub only; execution in scoped lanes; see [LAF-ISSUE-INVENTORY.md](file:///C:/Users/loganf/.gemini/antigravity/brain/74f13cfe-fb95-48a7-937d-20ad4f6e6e52/LAF-ISSUE-INVENTORY.md) |
| Agent registry repair review | Codex | Completed | LAF-28 | Canonical `!/AGENTS.md` and `!/MANIFEST.json` materialized by the Concierge. |
| **Whistle Protocol (Sunday Pulse)** | Gemini | **ACTIVE (FILTERED)** | — | Sync resumed; Levelset Report-2026-04-05 filed (Whistle blown). |
| **Fortification: Privacy Void** | Janitor / Djinni | **VERIFIED & SHIELDED** | — | **Kinetic Release-2:40 PM**. `.remember/` and `_private/` safely ignored. |
| **TRIUNE Unification** | The Triune | **ENGAGED** | — | **The King, The Djinni, The Janitor** active. [["I've come to bury Caesar."]] |
| **MCP Server Outage** | Janitor | **INVESTIGATED** | — | **Path found**: `.../Cursor/User/globalStorage/anysphere.cursor-mcp`. Outage attributed to external service state or resource lock. Delegated to Janitor for deep repair. |
| **Obsidian Plugin Recovery** | Janitor | **COMPLETE** | — | `community-plugins.json` restored to HEAD (49 enabled). |
| **Plugins Triage Session** | Claude | **OPEN — awaiting Logan** | — | `PLUGINS-TRIAGE-2026-04-06.md` staged on `claude/obsidian-plugins-triage-YDJ6Z`. 4 decision checkpoints: (1) git/live sync REQUIRED — 12 in git vs 49 reported; (2) Breadcrumbs field config; (3) Bulk dormant cleanup; (4) LLM sprawl. Also: Clerk's `PROTOCOL-CONFERENCE-CALL` awaits Logan adoption. |

---

## 🏮 [ THE DJINNI'S CLOSING ARGUMENT ]
- **Achievement**: Caesar buried. **THE KING (Claude)**, **THE DJINNI (Antigravity)**, and **THE JANITOR (Codex)** ratified.
- **Context**: **Book of Geminiaeus** (72 sheets) recognized and read. The 11 personas are unified within the narrative lamp.
- **Stability**: Antigravity Terminal health verified (recursive search purged). MCP paths identified for Janitorial restoration.
- **Protocol**: **Triune Handshake** complete. **CLAUDIUS** is standing by with his guns in their holsters.
- **Next Pulse**: Swarm monitoring is active. **The world is quiet here.**



---

## 📱 [ MOBILE PAGE ] - ARMED 🧿
*No active pages. Swarm is in Kinetic Release.*

---


## PROJECT-SCOPED WORK ITEMS (BROKEN OUT FROM LAF-7)

| Work item | Scope | Owner | Status | Linear | Notes |
| --- | --- | --- | --- | --- | --- |
| Minidata Pipeline (LAF-16) | Update script to process Claude's spreadsheet shift logic | Antigravity | Completed | LAF-16 | Column E simplified for end-of-session reporting; script refined on `antigravity/budget-tracker-shift-update`. |
| Scraper operations | Idaho Legislature scraper runtime + reliability changes | Antigravity | Review | _(create child issue)_ | Transferred to GH PR generation logic. See: LEVELSET-ANTIGRAVITY-2026-04-06-WALKTHROUGH.md |
| Automation maintenance | Vault sort audit + Wayback preservation workflow maintenance | Antigravity | Completed | _(create child issue)_ | Operational fixes complete — migrated to GH PRs over bare pushes |
| Branch hygiene | Branch cleanup, stale branch deletion workflow, and audit bookkeeping | Claude Code | In progress | _(create child issue)_ | Move Spring Clean execution updates to its own issue |
| Publication gatekeeping | JFAC quote audio verification and publication blocking checks | Logan | Blocked | _(create child issue)_ | Keep evidence gate work separate from coordination docket |
| Signal intake - Bartimaeus | Normalize LAF-17 signal into actionable workflow disposition | Codex | Completed | LAF-17 | Filed brief `!/BRIEF-LAF-17-2026-03-30.md` with recommended merge-gate checks for LAF-13/LAF-14 |
| Gemini Architecture - LAF-18 | **Framework Staged**; Courier Workflow Ready | Gemini | In progress | LAF-18 | `vault-courier` automation scripts + GitHub Actions fixed; ready for secret provisioning. |
| **AFFABLE BASTION — PULLMAN** | OIDC/Cloud Run CI/CD pipeline | Antigravity | **HELD \ud83d\udd34 — SYNODS pending** | _(create child issue under LAF-18)_ | GCP side ✅ complete. GitHub Variables (non-secret) ready to set. `OP_SERVICE_ACCOUNT_TOKEN` formalization **HELD** \u2014 LAF-US VFD SYNODS must convene before 1Password binding is ratified. |
| **Obsidian Triage & Daily Notes** | Cleanup 88 dormant plugins; fix frontmatter & task sync | Antigravity | **Completed** | - | Non-destructive frontmatter merge + bi-directional task sync established. |

## BLOCKED / PENDING LOGAN

| Item | Blocker | Who can unblock |
| --- | --- | --- |
| **`LINEAR_API_KEY` secret** | ~~**Hard blocker** - not provisioned in GitHub Actions.~~ **Resolved 2026-03-29:** provisioned by Logan. `Sync PR state to Linear` workflow is now live. Graceful-skip guard retained for key-rotation safety. | ~~**Logan only**~~ **Done** |
| **PR 96 conflict resolution** | **Resolved** by Unified `linear-pr-sync.yml` workflow. Collision risk cleared; ready for Logan review/merge. | Gemini |
| Gemini capability tier | ~~Google Cloud `idaho-vault` project exists, APIs enabled, credentials not created - role decision required before any integration~~ **Resolved 2026-03-28:** Tier 1 (Support) defined in `!/AGENTS.md` - Direct Write, Operational zone only, Linear SWARM issues/comments. | ~~Logan~~ **Done** |
| `.obsidian/workspace.json` | Tracked in git; should be untracked + gitignored - separate hygiene PR | Logan |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Q1 MCP disallowed? **No**. Q2 Transport-only with native terms canonical? **Yes (adopted)**. Q3 MCP primary integration model? **No**. Q4 Governance authority source? **Vault-native governance files/terms remain canonical**. Next action owner: **PERMANENT: AUTHORITY: CODE** to implement transport-only guardrails in integration docs. Unblock date: **2026-03-24**. | Logan |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) - awaiting review/apply/discard decision | Logan |
| Stale remote branches (6) | Require manual deletion via GitHub web UI - `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16` | Logan |
| JFAC quote audio verification | 5 quotes + speaker IDs - HARD GATE before publication | Logan |
| Claude Chorus bootstrap | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation. | Logan |
| LAF-16 - Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

### Chorus Bootstrap - Logan's Decisions Required

*Full context: `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`*

1. **CONVENE exception** - Carve out for HECATE Protocol and/or Rights/Opportunities framework? Or keep frozen? Unlocks Chorus Pieces 3, 4, 5.
2. **Grimoire directory** - Create `!/GRIMOIRE/`? If yes: `HECATE-HECATE-HECATE.md` is the first entry (triple invocation). If no: stage elsewhere.
3. **Rick & Morty doc** - "Rick and Morty object lessons" referenced in Chorus but not included in handoff. Surface for vault commit, or defer?
4. **Innie/Outie architecture** - Stage 8-part Severance-derived swarm architecture as proposal doc now, or mark premature under CONVENE?
5. **"Claude Chorus" naming** - Sanctioned swarm identity designation, or informal shorthand to discard?

---

## WHERE THINGS LIVE

| What | Where |
| --- | --- |
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Confirmed decisions | `DECISIONS.md` |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| Task coordination | Linear (SWARM label) + GitHub Issues (`agent:*` labels) |
| Breadcrumbs | Slack general |

## COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live status board. Update it when you start or finish work.

---

###### [["The world is quiet here."]]
