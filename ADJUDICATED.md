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

| Task | Completed | Notes |
| --- | --- | --- |
| **Agent registry and bootstrap repair breadcrumbed** | 2026-04-02 | Missing `!/` registry surface materialized; root governance kept authoritative; canonical bootstrap is now `!/AGENTS.md` -> `swarm.json` -> `!/agents.json` -> `!/agent.sh`; see `[[BRIEF-LAF-28-2026-04-02]]` and `[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]` |
| **TRIUNE COVENANT + 1Password + Agent Protocol** | 2026-03-30 | 1Password CLI + SSH agent infrastructure deployed (.op/SETUP.md, .op/secrets.template.md, 1password-secret-template.yml); AGENT PROTOCOL defined with 6-phase bootstrap (!\agent.sh, !/AGENT-PROTOCOL.md); agents can now invoke via `source !\agent.sh [NAME]` - `4463d4d` |
| **Unified Swarm research filed** | 2026-03-29 | Two-part Perplexity report filed as `BIG IFS - UNIFIED SWARM.md`; org stubs created for [[Factory]], [[CrewAI]], [[OpenAI Swarm]] (R&D flagged by Logan) - branch `claude/research-unified-swarm-rDmOg` |
| **Gemini Code Assist cowork enabled** | 2026-03-28 | `.gemini/GEMINI.md` tier fixed, cowork pattern documented; `.gemini/settings.json` context expanded to 6 files; AGENTS.md + entity note updated - `3563a66` |
| **Stale `!ADMIN/` refs cleaned + root frontmatter spring-cleaned** | 2026-03-28 | DECISIONS.md, LEVELSET-STEP-0, THREAT-MODEL updated; 10 content docs tagged; `!/SWARM-LOOP.md` committed - `ba01c2e` |
| **Triage + commit 10 untracked content docs** | 2026-03-28 | AGENTIC SWARM SYSTEMS, AI-AUTOMATION, IDAHO-VAULT SYSTEM CONTEXT/WORKFLOW, JOURNALISM INDUSTRY, Kano Play, Notebook LM, Podcast, David Leroy - `07d2cb7` |
| **PR 98 opened + updated** | 2026-03-28 | Covers all 3 session commits; flags PR 84 conflict and pending DECISIONS 18-21 |
| **`claude/agent-dotfolder-architecture` local branch deleted** | 2026-03-28 | Already merged to main; remote gone |
| **LEVELSET-CURRENT refreshed** | 2026-03-28 | Activity log, UNRESOLVED, NEXT ACTIONS, DECISIONS count updated |
| **Gemini capability tier defined** | 2026-03-28 | Tier 1 (Support): Direct Write, Operational zone only, Linear SWARM issues/comments - `!/AGENTS.md` updated |
| **Linear Phase 1 pilot scoped** | 2026-03-28 | Plugin auth inventory -> recommendation captured; ACTIVE WORK entry created; vault/Slack doctrine confirmed |
| Plugin auth inventory committed | 2026-03-28 | `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` - all 7 connectors probed; Linear-first recommended |
| Codex archival levelset committed | 2026-03-28 | `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md` - Codex session handoff and boundary truths |
| LAF-1 - Linear onboarding resources | 2026-03-25 | Intro video and setup guides captured in `!/LINEAR-ONBOARDING.md` |
| LAF-3 - Connect your tools brief | 2026-03-25 | Brief filed at `!/BRIEF-LAF-3-2026-03-25.md` |
| PR 34 - Obsidian vault update (42 files) | 2026-03-23 | Merged via `copilot/deploy-dependabot-configurations` |
| PR 39 - Get scrapers running | 2026-03-24 | Merged; scraper now on main, running daily |
| PR 40 - CodeRabbit GitHub integration | 2026-03-23 | Merged |
| PR 44 - REST API credential sanitization | 2026-03-24 | Merged; machine credentials purged from repo |
| PR 46 - Workflow centralization + settings.json fix | 2026-03-24 | Merged; composite action, zombie `!ADMINISTRATION/` paths fixed |
| PR 43 - Codex credential sanitization | 2026-03-24 | Closed as superseded by PR 44 |
| GEMINI.md update | 2026-03-24 | Direct commit by Logan |
| PR 48 - CONSTITUTION.md LEVELSET path fix | 2026-03-23 | Merged; zombie `!ADMIN/LEVELSET-v3.2.6.1-PROMPT.md` -> `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` |
| PR 50 - CONSTITUTION.md AGENTS.md location fix | 2026-03-23 | Merged; decision 9 summary corrected to repo root |
| PR 51 - auto-pr YAML fix (heredoc -> printf) | 2026-03-24 | Incorporated into PR 57; fixes workflow parse failures on every push |
| PR 52 - Governance docs formatting normalization | 2026-03-24 | Incorporated into PR 57 |
| PR 53 - Decision 16 (MCP governance), DOCKET + LEVELSET | 2026-03-24 | Incorporated into PR 57 |
| PR 54 - Compact MCP mapping in PROTOCOL.md | 2026-03-24 | Incorporated into PR 57 |
| PR 55 - MCP implementation plan (new file) | 2026-03-24 | Incorporated into PR 57 |
| PR 56 - MCP action logging template in VAULT-CONVENTIONS | 2026-03-24 | Incorporated into PR 57 |
| LAF-9 - Vault template + document class system | 2026-03-25 | Drafted `VAULT-TEMPLATES.md`; linked from conventions + canonical README |

### Resolved Blockers
| Item | Notes |
| --- | --- |
| **`LINEAR_API_KEY` secret** | **Resolved 2026-03-29:** provisioned by Logan. `Sync PR state to Linear` workflow is now live. |
| **PR 96 conflict resolution** | **Resolved** by Unified `linear-pr-sync.yml` workflow. Collision risk cleared; ready for Logan review/merge. |
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

###### "The world is quiet here."
