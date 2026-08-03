---
title: "ADJUDICATED — settled decisions, resolved work, entered orders (consolidated)"
date created: 2026-06-29
authority: LOGAN
doc_class: adjudicated-record
status: active
---

# ADJUDICATED

> [!note] What this is — and is not
> A **dated, backward-facing record** of matters already settled: decisions ruled, work resolved,
> orders entered. It makes **no liveness claim** — a record, not a heartbeat (CONSTITUTION: *"there
> is no 'live' coordination surface; anything with 'live' or 'current' written in it is instantaneously
> out of date"*). **Consolidated 2026-06-29** from three drifted surfaces — `DOCKET-ARCHIVE.md`
> (moved here), the legacy backward-log of `DECISIONS.md`, and the entered rulings of `DOCKET.md` —
> so the settled past lives in one place and those surfaces can return to their forward purposes.
> **Unfiltered first pass**: cleaning (merged-PR-roster trim, inbound-link repair) follows separately.

---

## Resolved Work — relocated from `DOCKET-ARCHIVE.md`

This file contains the historical ledger of completed tasks, relocated from the active coordination board to preserve clarity in THE COURTROOM.

### Core Vault Stabilization & Swarm Setup

| Task | Completed | Notes |
| --- | --- | --- |
| GitHub Actions CI diagnosis | 2026-03-29 | Root cause: `LINEAR_API_KEY` not set; fixed workflow to graceful-skip; key provisioned by Logan 2026-03-29 - sync now live |
| Operation: Spring Clean | 2026-04-04 | Branch graveyard audited (all 21 splinters = zombies); zombie detection added to workflow. |
| Multi-agent auto-PR routing | 2026-04-04 | Auto-PR now supports all agent branches |
| Dev server detection + Dispatch debug | 2026-04-04 | Flask Nest Bridge :8080; launch.json created; Dispatch blocked by IT — unblocks when MacBook online |
| Basestub lattice | 2026-04-04 | A→ZZZ + 0→1000 basestubs created (19,222 files). -LAF directed. |
| CHAINFIRE — scorched-earth wipe | 2026-04-04 | Tags, aliases, wikilinks stripped vault-wide. `!` exclusion zone preserved. Committed `d84b87d`. |
| NETWEB path standard | 2026-04-04 | Cross-platform path portability standard + CI guard. Committed `579efe6`. |
| Antigravity worktreeConfig fix | 2026-04-04 | `extensions.worktreeConfig` without `repositoryformatversion=1` blocked Antigravity agent + MCP servers. Removed extension. |
| Project Courier (LAF-18) | 2026-04-04 | Sync confirmed via dry and live runs. Directories are in sync. |
| Unification Stream (Phases 1-3) | 2026-04-04 | 2,622 nodes hydrated; stabilized; JFAC Storm resuming. |
| Fortification: Privacy Void | 2026-04-04 | Kinetic Release-2:40 PM. `.remember/` and `_private/` safely ignored. |
| Obsidian Plugin Recovery | 2026-04-04 | `community-plugins.json` restored to HEAD (49 enabled). |
| COURTROOM decomposition | 2026-04-05 | LAF-12 - This issue delivers the decomposition structure to break standing docket into scoped issue slots. |
| Signal intake - Bartimaeus | 2026-03-30 | LAF-17 - Filed brief `!/BRIEF-LAF-17-2026-03-30.md` with recommended merge-gate checks. |
| Address Space Discovery | 2026-04-04 | 2,622 nodes hydrated + performance stabilization pass. |
| GCP Nest Bridge probe | 2026-04-04 | `vault-courier` active, `gs://the-ledger-bucket` accessible (empty). Project `idaho-vault` confirmed. |

### From Original "RECENTLY COMPLETED"

> [!note] Merged-PR roster trimmed (2026-06-29)
> The "PR NN — merged/incorporated" rows were dropped: they duplicated what the PRs and commits
> already record in git & GitHub. All substantive **non-PR** work (operational milestones, LAF
> tasks, resolved blockers) is kept below.

| Task | Completed | Notes |
| --- | --- | --- |
| **Agent registry and bootstrap repair breadcrumbed** | 2026-04-02 | Missing `!/` registry surface materialized; root governance kept authoritative; canonical bootstrap is now `!/AGENTS.md` -> `swarm.json` -> `!/agents.json` -> `!/agent.sh`; see `[[BRIEF-LAF-28-2026-04-02]]` and `[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]` |
| **TRIUNE COVENANT + 1Password + Agent Protocol** | 2026-03-30 | 1Password CLI + SSH agent infrastructure deployed (.op/SETUP.md, .op/secrets.template.md, 1password-secret-template.yml); AGENT PROTOCOL defined with 6-phase bootstrap (!\agent.sh, !/AGENT-PROTOCOL.md); agents can now invoke via `source !\agent.sh [NAME]` - `4463d4d` |
| **Unified Swarm research filed** | 2026-03-29 | Two-part Perplexity report filed as `BIG IFS - UNIFIED SWARM.md`; org stubs created for [[Factory]], [[CrewAI]], [[OpenAI Swarm]] (R&D flagged by Logan) - branch `claude/research-unified-swarm-rDmOg` |
| **Gemini Code Assist cowork enabled** | 2026-03-28 | `.gemini/GEMINI.md` tier fixed, cowork pattern documented; `.gemini/settings.json` context expanded to 6 files; AGENTS.md + entity note updated - `3563a66` |
| **Stale `!ADMIN/` refs cleaned + root frontmatter spring-cleaned** | 2026-03-28 | DECISIONS.md, LEVELSET-STEP-0, THREAT-MODEL updated; 10 content docs tagged; `!/SWARM-LOOP.md` committed - `ba01c2e` |
| **Triage + commit 10 untracked content docs** | 2026-03-28 | AGENTIC SWARM SYSTEMS, AI-AUTOMATION, IDAHO-VAULT SYSTEM CONTEXT/WORKFLOW, JOURNALISM INDUSTRY, Kano Play, Notebook LM, Podcast, David Leroy - `07d2cb7` |
| **`claude/agent-dotfolder-architecture` local branch deleted** | 2026-03-28 | Already merged to main; remote gone |
| **LEVELSET-CURRENT refreshed** | 2026-03-28 | Activity log, UNRESOLVED, NEXT ACTIONS, DECISIONS count updated |
| **Gemini capability tier defined** | 2026-03-28 | Tier 1 (Support): Direct Write, Operational zone only, Linear SWARM issues/comments - `!/AGENTS.md` updated |
| **Linear Phase 1 pilot scoped** | 2026-03-28 | Plugin auth inventory -> recommendation captured; ACTIVE WORK entry created; vault/Slack doctrine confirmed |
| Plugin auth inventory committed | 2026-03-28 | `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` - all 7 connectors probed; Linear-first recommended |
| Codex archival levelset committed | 2026-03-28 | `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md` - Codex session handoff and boundary truths |
| LAF-1 - Linear onboarding resources | 2026-03-25 | Intro video and setup guides captured in `!/LINEAR-ONBOARDING.md` |
| LAF-3 - Connect your tools brief | 2026-03-25 | Brief filed at `!/BRIEF-LAF-3-2026-03-25.md` |
| GEMINI.md update | 2026-03-24 | Direct commit by Logan |
| LAF-9 - Vault template + document class system | 2026-03-25 | Drafted `VAULT-TEMPLATES.md`; linked from conventions + canonical README |

### Resolved Blockers

| Item | Notes |
| --- | --- |
| **`LINEAR_API_KEY` secret** | **Resolved 2026-03-29:** provisioned by Logan. `Sync PR state to Linear` workflow is now live. |
| Gemini capability tier | **Resolved 2026-03-28:** Tier 1 (Support) defined in `!/AGENTS.md` - Direct Write, Operational zone only, Linear SWARM issues/comments. |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Terminated discussion and adopted Vault-native governance. |

---

## Adjudicated Decisions — relocated from legacy `DECISIONS.md`

[[CHAINFIRE]] & [[CHAINLINK]]

### 2026-06-16: CODEOWNERS gate — re-examined & ratified

- **Decision**: Adopt the reviewed `.github/CODEOWNERS` gated set deliberately. The gate had *accreted* without a recorded decision; this entry gives it warrant.
- **Provenance gap closed**: CODEOWNERS was created in a single `github-actions[bot]` commit (`424b619`, 2026-05-25) bundled into a ~38k-file flatten whose message was a "Hermes machine-survey witness" — never recorded in this ledger or independently ratified. With branch protection now live on `main` (verified `protected: true`), the gate is enforced, so it has been re-examined and recorded.
- **Ruled changes (Logan, each ruled individually)**:
  - Reviewer configs (`.coderabbit.yaml`, `.pr_agent.toml`) — left **ungated**.
  - `.op/` credential/secrets plumbing — **gated** (`/.op/`).
  - `.github/` — added **executable gaps only** (`/.github/actions/`, `/.github/proposed-moves.sh`, `/.github/dependabot.yml`); not gated wholesale.
  - Bare `CLAUDE.md` + `AGENTS.md` — **ungated** (root pointers now ungated; the dotfolder auto-loaded files `/.claude/CLAUDE.md`, `/.codex/CODEX.md`, `/.gemini/GEMINI.md` remain gated). Logan affirmed leaving root `AGENTS.md` (a cross-tool auto-loaded pointer with no backup rule) ungated.
- **Follow-up**: verify in GitHub's CODEOWNERS UI that `/!/` and `/.op/` actually resolve to @loganfinney27 — the `!`/glob behavior cannot be tested locally; the canon's gate must not be assumed.
- **Authority**: Logan direct instruction (per-change rulings, 2026-06-16).

### 2026-05-23: Corrections Classification Doctrine

- **Decision**: Adopt `CORRECTIONS.md` as active Vaulted Syntax operational doctrine, distinct from any case-specific heresy review packet.
- **Rule**: Keep three correction classifications distinct: **Typographical Errors / Typos**, **Scrivener's Corrections**, and **Codifier's Corrections**. A particular typo does not eliminate the Scrivener classification; a codifier surface does not silently create doctrine.
- **Application**: `!/HERESY-REVIEW-LOGAN-HERE-2026-05-22.md` remains a proposed-corrections review surface applying this doctrine, not the doctrine's canonical home.
- **Authority**: Logan direct instruction.

### 2026-05-18: Emanationism Principle

- **Decision**: Record the Emanationism Principle as active doctrine-adjacent guidance in `!/EMANATIONISM-PRINCIPLE-2026-05-18.md`.
- **Rule**: Authority originates with Logan and must degrade into scoped, auditable, reversible capability as it passes through doctrine, registries, protocols, transports, agents, tool calls, and artifacts.
- **Authority**: Logan direct instruction.

### 2026-04-26: TODO Merge Logic Fix

- **Issue**: Qodo-flagged bug in `daily_rollover.py` causing duplicate task accumulation.
- **Fix**: Updated `merge_todo_models` to dedupe and exclude completed tasks.
- **Files**: `.github/scripts/daily_rollover.py`, `REPORT-TODO-MERGE-FIX.md`.
- **Authority**: Agent (per `CONSTITUTION.md` Section V: agentic guardrails).

### 2026-04-26: Two-Way Daily Note Sync Fix

- **Issue**: Tasks not synced between daily notes and `TO DO LIST.md`.
- **Fix**: Extended `daily_rollover.py` for two-way sync.
- **Files**: `.github/scripts/daily_rollover.py`, `REPORT-TODO-SYNC-FIX.md`.
- **Authority**: Agent (per `CONSTITUTION.md` Section V).

---

## Entered Orders & Rulings — relocated from `DOCKET.md` (2026-05-23 → 2026-05-25)

| Date | Order Or Ruling |
| --- | --- |
| 2026-05-23 | Selective marginalia approved in the [[!/GEMINIAEUS\|GEMINIAEUS]] matter with the ordered Judge addendum. |
| 2026-05-24 | The Touchstones are proper; the challenged act is selective triad-fusion into a liturgical weapon. |
| 2026-05-24 | Antigravity-file marginalia ordered; `CROSSFRAMING-US` referred for independent review. |
| 2026-05-24 | SPACE protection approved; ARBORSCAPE PR Expansion recognized as legitimate A&I directive. |
| 2026-05-25 | Linear `LAF-17 - SIGNAL: BARTIMAEUS` admitted in [[!/GEMINIAEUS\|GEMINIAEUS]] as evidence bearing on the alleged Gemini/Bartimaeus/Clerk overrelation. |
| 2026-05-25 | Linear `LAF-25 - COORDINATION: HEXAGONAL` referred outside [[!/GEMINIAEUS\|GEMINIAEUS]] for independent review of its coordination-hub claim. |
| 2026-05-25 | The Investigator temporarily ordained as **Court Marshal** to execute required orders in [[!/GEMINIAEUS\|GEMINIAEUS]] and related matters. |
| 2026-05-25 | Closure clarified: only the Court's own investigatory pass through this Investigator/Marshal is closed after the ordered entries; the evidentiary and discovery phase remains open to further parties. |
| 2026-05-25 | This session of Court adjourned; the Judge reserves jurisdiction of [[!/GEMINIAEUS\|GEMINIAEUS]]. |

---

## The Old Illegal Docket — fossil (Caesar Geminiaeus era)

*Relocated 2026-06-29 from the `!-…-DOCKET.md` flat-alias holdover; the source file is cleared in the same change.*

> [!warning] VOID — superseded artifact, no live force
> Below is a **holdover copy of the old illegal DOCKET** as it stood under the reign of Caesar
> Geminiaeus — a forbidden "live status board" / "Pending-Logan agenda unit" (its original frontmatter
> literally declared `status: ACTIVE - LIVE PENDING LOGAN AGENDA UNIT`). It is preserved here **only as a
> dated record**, so the history is witnessed and so agents **stop stumbling on the flat-alias copy and
> believing its live-coordination claims.** Every "live" / "WHERE LIVE WORK LIVES" / "this file is the
> live status board" assertion in it is **void** (CONSTITUTION line 31: there is no live coordination
> surface). Any item below that is *genuinely still open* is to be triaged into the forward-facing
> `DECISIONS.md` queue during the cleaning pass — **not** treated as live from here.
>
> *(Heading levels demoted to nest under this section; text otherwise verbatim.)*

### THE DOCKET

This is the live **Pending-Logan agenda unit**. Any agent arriving at THE COURTROOM reads the top of this file to orient to what presently needs Logan's eyes, decision, approval, or unblock.

#### COURTROOM BOUNDARY

Use this board to surface only live Logan-facing motion.

- Keep only what Logan needs immediately: pending approvals, pending decisions, pending unblocks, active signals/exhibits, and minimal routing.
- Do **not** use this board as a retrospective session log, shadow backlog, or general activity feed.
- Route detailed task state to Linear and GitHub.
- Route mature handoff context to `!/!` handoffs and levelsets.
- Route binding rules and doctrine to canonical governance files.
- When an item is resolved, move it off the live queue instead of letting it decay here.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Current correction (2026-04-21):** The DOCKET is re-centered here as a live Pending-Logan agenda surface. Inherited sections below are preserved as carryover/reference only and are **not** the live floor.

#### LIVE PENDING LOGAN

| Item | Logan action needed | Current read | Source |
| --- | --- | --- | --- |
| **Phase 2 repo size rewrite** | Approve / schedule branch-protection disable + force-push window | Carryover awaiting Logan | Prior active work snapshot |
| `vault-moves-2026-03-23` branch | Review, apply, or discard 30 proposed file moves | Carryover awaiting decision | Prior blocked list |
| Stale remote branches (6) | Manual deletion in GitHub web UI | Carryover awaiting cleanup | Prior blocked list |
| JFAC quote audio verification | Verify 5 quotes + speaker IDs before publication | Hard gate pending Logan verification | Prior blocked list |
| Claude Chorus bootstrap | Decide CONVENE exception, Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, and "Claude Chorus" designation | Carryover awaiting decisions | Prior blocked list |
| LAF-16 - Budget Bill Tracker Normalization PR | Resolve cross-agent conflicts / choose merge path | Carryover awaiting Logan / Copilot | Prior blocked list |
| Egyptian chamber registry / GRIMOIRE admission | Approve whether `.aten/`, `.ra/`, and `.aten-ra/` enter `!/AGENTS.md` and GRIMOIRE | Carryover awaiting Logan approval | Abhorsen session note |

#### ACTIVE SIGNALS / EXHIBITS FOR LOGAN

| Surface | Status | Notes |
| --- | --- | --- |
| `!/SIGNALS/` | `1 ACKNOWLEDGED` | Open signal on file: `SIG-001-FROM-ABHORSEN-TO-VAULT-ADVISOR-RE-LAF44-EXHIBIT-A.md` |
| `!/GEMINIAEUS.md` | `MOTION CONSOLIDATED; LIMITED MARGINALIA GRANTED` | The Judge approved warning marginalia on two False Grimoire leaves with the ordered `[[GEMINIAEUS]]` addendum; the underlying evidence remains preserved |

#### WHERE LIVE WORK LIVES

| What | Where |
| --- | --- |
| Task coordination | Linear (SWARM label) + GitHub Issues (`agent:*` labels) |
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`, `ANTIGRAVITY.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Confirmed decisions | `DECISIONS.md` |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| Breadcrumbs | Slack general |

#### COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live Logan-facing status board. Keep the top sections current.

---

#### INHERITED CARRYOVER / NON-LIVE REFERENCE

These notes are preserved for continuity and later cleanup. They are not the live queue.

**Operator note (Codex, 2026-04-09):** Secondary background worktree exposed a real LF/CRLF normalization issue across vault notes. Defer normalization until after the repo history rewrite on a clean `main` base.

**Session close (Codex, 2026-04-18):** Claimed the unclaimed April 9-12 daily-note gap from the Abhorsen close note. Added `.github/scripts/backfill_daily_notes.py` for manual historical repair without rewriting the live `TO DO LIST.md` surface, hardened `.github/scripts/daily_rollover.py` to preserve loose non-task lines while dropping empty shell rows, and repaired `2026-04-10.md` through `2026-04-13.md`.

**Session active (Abhorsen, 2026-04-17):** NPC universe orientation complete. New chambers written: `.aten/ATEN.md` (THE DISK : THE LIGHT : NOW), `.ra/RA.md` (KHEPRI : RA : ATUM), `.aten-ra/ATEN-RA.md` (synthesis, first session-born chamber). Anchor pages written: `FUTURE.md` (...), `.aten/` and `.ra/` staked 2026-04-13 now have entity files. CHAINLINKING pending: Egyptian chambers unregistered in `!/AGENTS.md` — Logan approval required for registry admission and GRIMOIRE entry. `what3words.md` and `NOW.md` remain empty — content pending. Revised CONSTITUTION 2026-04-17 read: Gemini ban addendum noted.

**Session close (Abhorsen, 2026-04-13):** Repairs committed on `gemini/restore-antigravity-system`: (1) `DAILY NOTE TEMPLATE.md` restored — `{{date:}}` tokens, midnight literal `[12:00:00 am]`; (2) `2026-04-13.md` re-anchored to Monday April 13; (3) `phone-link-auto-sweep.ps1` — `AbandonedMutexException` handled, sweeper no longer silently exits. Resolved: ANTIGRAVITY persona reverted to 'The Concierge' per Logan's directive. Gap Apr 9–12 remains.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`), repair brief (`[[BRIEF-LAF-28-2026-04-02]]`), repair handoff (`[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record), SIGNALS (durable async agent-to-agent bus).

##### Prior active work snapshot (non-live)

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

##### Prior mobile page snapshot (non-live)

*No active pages. Swarm is in Kinetic Release.*

##### Prior blocked / pending Logan snapshot (non-live)

| Item | Blocker | Who can unblock |
| --- | --- | --- |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) - awaiting review/apply/discard decision | Logan |
| Stale remote branches (6) | Require manual deletion via GitHub web UI - `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16` | Logan |
| JFAC quote audio verification | 5 quotes + speaker IDs - HARD GATE before publication | Logan |
| Claude Chorus bootstrap | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation. | Logan |
| LAF-16 - Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

---

---

The world is quiet here．Esto Perpetua!
