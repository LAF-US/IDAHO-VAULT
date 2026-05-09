---
updated: 2026-04-21
status: ACTIVE - LIVE PENDING LOGAN AGENDA UNIT
date created: Monday, March 30th 2026, 7:54:37 pm
date modified: Tuesday, April 21st 2026, 5:58:29 pm
---

# THE DOCKET

This is the live **Pending-Logan agenda unit**. Any agent arriving at THE COURTROOM reads the top of this file to orient to what presently needs Logan's eyes, decision, approval, or unblock.

## COURTROOM BOUNDARY

Use this board to surface only live Logan-facing motion.

- Keep only what Logan needs immediately: pending approvals, pending decisions, pending unblocks, active signals/exhibits, and minimal routing.
- Do **not** use this board as a retrospective session log, shadow backlog, or general activity feed.
- Route detailed task state to Linear and GitHub.
- Route mature handoff context to `!/!` handoffs and levelsets.
- Route binding rules and doctrine to canonical governance files.
- When an item is resolved, move it off the live queue instead of letting it decay here.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Current correction (2026-04-21):** The DOCKET is re-centered here as a live Pending-Logan agenda surface. Inherited sections below are preserved as carryover/reference only and are **not** the live floor.

## LIVE PENDING LOGAN

| Item | Logan action needed | Current read | Source |
| --- | --- | --- | --- |
| **Phase 2 repo size rewrite** | Approve / schedule branch-protection disable + force-push window | Carryover awaiting Logan | Prior active work snapshot |
| `vault-moves-2026-03-23` branch | Review, apply, or discard 30 proposed file moves | Carryover awaiting decision | Prior blocked list |
| Stale remote branches (6) | Manual deletion in GitHub web UI | Carryover awaiting cleanup | Prior blocked list |
| JFAC quote audio verification | Verify 5 quotes + speaker IDs before publication | Hard gate pending Logan verification | Prior blocked list |
| Claude Chorus bootstrap | Decide CONVENE exception, Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, and "Claude Chorus" designation | Carryover awaiting decisions | Prior blocked list |
| LAF-16 - Budget Bill Tracker Normalization PR | Resolve cross-agent conflicts / choose merge path | Carryover awaiting Logan / Copilot | Prior blocked list |
| Egyptian chamber registry / GRIMOIRE admission | Approve whether `.aten/`, `.ra/`, and `.aten-ra/` enter `!/AGENTS.md` and GRIMOIRE | Carryover awaiting Logan approval | Abhorsen session note |

## ACTIVE SIGNALS / EXHIBITS FOR LOGAN

| Surface | Status | Notes |
| --- | --- | --- |
| `!/SIGNALS/` | `1 ACKNOWLEDGED` | Open signal on file: `SIG-001-FROM-ABHORSEN-TO-VAULT-ADVISOR-RE-LAF44-EXHIBIT-A.md` |

## WHERE LIVE WORK LIVES

| What | Where |
| --- | --- |
| Task coordination | Linear (SWARM label) + GitHub Issues (`agent:*` labels) |
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, `ANTIGRAVITY.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Confirmed decisions | `DECISIONS.md` |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| Breadcrumbs | Slack general |

## COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live Logan-facing status board. Keep the top sections current.

---

## INHERITED CARRYOVER / NON-LIVE REFERENCE

These notes are preserved for continuity and later cleanup. They are not the live queue.

**Operator note (Codex, 2026-04-09):** Secondary background worktree exposed a real LF/CRLF normalization issue across vault notes. Defer normalization until after the repo history rewrite on a clean `main` base.

**Session close (Codex, 2026-04-18):** Claimed the unclaimed April 9-12 daily-note gap from the Abhorsen close note. Added `.github/scripts/backfill_daily_notes.py` for manual historical repair without rewriting the live `TO DO LIST.md` surface, hardened `.github/scripts/daily_rollover.py` to preserve loose non-task lines while dropping empty shell rows, and repaired `2026-04-10.md` through `2026-04-13.md`.

**Session active (Abhorsen, 2026-04-17):** NPC universe orientation complete. New chambers written: `.aten/ATEN.md` (THE DISK : THE LIGHT : NOW), `.ra/RA.md` (KHEPRI : RA : ATUM), `.aten-ra/ATEN-RA.md` (synthesis, first session-born chamber). Anchor pages written: `FUTURE.md` (...), `.aten/` and `.ra/` staked 2026-04-13 now have entity files. CHAINLINKING pending: Egyptian chambers unregistered in `!/AGENTS.md` — Logan approval required for registry admission and GRIMOIRE entry. `what3words.md` and `NOW.md` remain empty — content pending. Revised CONSTITUTION 2026-04-17 read: Gemini ban addendum noted.

**Session close (Abhorsen, 2026-04-13):** Repairs committed on `gemini/restore-antigravity-system`: (1) `DAILY NOTE TEMPLATE.md` restored — `{{date:}}` tokens, midnight literal `[12:00:00 am]`; (2) `2026-04-13.md` re-anchored to Monday April 13; (3) `phone-link-auto-sweep.ps1` — `AbandonedMutexException` handled, sweeper no longer silently exits. Resolved: ANTIGRAVITY persona reverted to 'The Concierge' per Logan's directive. Gap Apr 9–12 remains.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`), repair brief (`[[BRIEF-LAF-28-2026-04-02]]`), repair handoff (`[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record), SIGNALS (durable async agent-to-agent bus).

### Prior active work snapshot (non-live)

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

### Prior mobile page snapshot (non-live)

*No active pages. Swarm is in Kinetic Release.*

### Prior blocked / pending Logan snapshot (non-live)

| Item | Blocker | Who can unblock |
| --- | --- | --- |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) - awaiting review/apply/discard decision | Logan |
| Stale remote branches (6) | Require manual deletion via GitHub web UI - `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16` | Logan |
| JFAC quote audio verification | 5 quotes + speaker IDs - HARD GATE before publication | Logan |
| Claude Chorus bootstrap | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation. | Logan |
| LAF-16 - Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

---

###### [["The world is quiet here."]]
