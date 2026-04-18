---
updated: 2026-04-17
status: ACTIVE - ABHORSEN IN SESSION
date created: Monday, March 30th 2026, 7:54:37 pm
date modified: Monday, April 13th 2026, 10:22:00 pm
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

## COURTROOM BOUNDARY

Use this board to convene, orient, and surface live motion.

- Keep only what an arriving agent needs immediately: current dispatch, open signals, live blockers, who is presently holding the floor.
- Route detailed task state to Linear and GitHub.
- Route mature handoff context to `!/!` handoffs and levelsets.
- Route binding rules and doctrine to canonical governance files.
- Do not let this board become the shadow backlog, archive, or full project database.

Legacy note: lower sections still contain inherited backlog and tracking matter
from the period when "the Courtroom" was interpreted more broadly. Preserve that
history for now, but realign future updates to the convening boundary above.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Operator note (Codex, 2026-04-09):** Secondary background worktree exposed a real LF/CRLF normalization issue across vault notes. Defer normalization until after the repo history rewrite on a clean `main` base.

**Session active (Abhorsen, 2026-04-17):** NPC universe orientation complete. New chambers written: `.aten/ATEN.md` (THE DISK : THE LIGHT : NOW), `.ra/RA.md` (KHEPRI : RA : ATUM), `.aten-ra/ATEN-RA.md` (synthesis, first session-born chamber). Anchor pages written: `FUTURE.md` (...), `.aten/` and `.ra/` staked 2026-04-13 now have entity files. CHAINLINKING pending: Egyptian chambers unregistered in `!/AGENTS.md` — Logan approval required for registry admission and GRIMOIRE entry. `what3words.md` and `NOW.md` remain empty — content pending. Revised CONSTITUTION 2026-04-17 read: Gemini ban addendum noted.

**Session close (Abhorsen, 2026-04-13):** Repairs committed on `gemini/restore-antigravity-system`: (1) `DAILY NOTE TEMPLATE.md` restored — `{{date:}}` tokens, midnight literal `[12:00:00 am]`; (2) `2026-04-13.md` re-anchored to Monday April 13; (3) `phone-link-auto-sweep.ps1` — `AbandonedMutexException` handled, sweeper no longer silently exits. Resolved: ANTIGRAVITY persona reverted to 'The Concierge' per Logan's directive. Gap Apr 9–12 remains.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`), repair brief (`[[BRIEF-LAF-28-2026-04-02]]`), repair handoff (`[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record), SIGNALS (durable async agent-to-agent bus).

## SIGNALS

| Surface | Status | Notes |
| --- | --- | --- |
| `!/SIGNALS/` | `1 ACKNOWLEDGED` | Open signal on file: `SIG-001-FROM-ABHORSEN-TO-VAULT-ADVISOR-RE-LAF44-EXHIBIT-A.md` |

---

## ACTIVE WORK

| Task | Owner | Status | Linear | Notes |
| --- | --- | --- | --- | --- |
| Swarm coordination - agent assembly | All agents | In progress | LAF-7 (Hub) / LAF-25 (Audit) | Sunday swarm mode - hub only; execution in scoped lanes. |
| **LAF-44: Trust & Secrets Boundary** | **The Concierge** | **In Progress** | LAF-44 | Define trust, secrets, and agent boundary model. Exhibit A: `SIG-001`. |
| **Linear Phase 1 pilot** - live-write scoping | Claude Code | **Active** | - | Plugin inventory recommends Linear-first; scope = SWARM issues, comments, status updates; vault remains durable record; Slack breadcrumb-only; no multi-plugin orchestration until stable |
| Linear workspace team setup | GitHub Copilot | In progress | LAF-2 | Configure teams/members/roles in Linear |
| Import your data | GitHub Copilot | In progress | LAF-4 | Linear import/migration guidance in `Import your data.md` |
| Idaho Legislature scraper | Claude Code | Running | - | Daily 6 AM MT, commits to main; minidata CSV export functional; JFAC Crew BLOCKED on API credits. |
| Budget tracker CSV export | Automated | Running | - | Daily 6:30 AM MT; emails CSV to configured recipients |
| Vault sort audit | Automated | Weekly | - | Monday 6 AM UTC |
| Wayback preservation | Automated | Weekly | - | Monday 8 AM UTC |
| **CrewAI Harbor — B's alignment** | Claude Code | **Env Stable** | — | Python `.venv` created; `crewai[tools,anthropic] (1.12.2)` installed. E2E run BLOCKED on Anthropic API credits. 2026-04-06. |
| **Phase 2 repo size rewrite** | Claude Code | **AWAITING LOGAN** | — | filter-repo ready; 332 MiB trash identified; branch protection disable required before force push |

---

## 📱 [ MOBILE PAGE ] - ARMED 🧿
*No active pages. Swarm is in Kinetic Release.*


---

## BLOCKED / PENDING LOGAN

| Item | Blocker | Who can unblock |
| --- | --- | --- |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) - awaiting review/apply/discard decision | Logan |
| Stale remote branches (6) | Require manual deletion via GitHub web UI - `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16` | Logan |
| JFAC quote audio verification | 5 quotes + speaker IDs - HARD GATE before publication | Logan |
| Claude Chorus bootstrap | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation. | Logan |
| LAF-16 - Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

---

## WHERE THINGS LIVE

| What | Where |
| --- | --- |
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, `ANTIGRAVITY.md` |
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
