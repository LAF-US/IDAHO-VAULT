# LEVELSET-CURRENT — Live Ecosystem State

**Date:** 2026-03-24
**Status:** CURRENT — living synthesis, updated each LEVELSET round
**Synthesized by:** Claude Code (The Abhorsen) — Operation: Spring Clean update
**Input authority chain:** CONSTITUTION.md > DECISIONS.md > CLAUDE.md
**Approved by:** Pending Logan Finney review

---

## What This File Is

LEVELSET-CURRENT is the rolling synthesis document. Unlike numbered LEVELSET files (v1, v2, v3...) which are permanent snapshots, LEVELSET-CURRENT reflects the **present state** of the ecosystem. It is updated — not appended — each round. The numbered files remain the permanent audit trail.

**Relationship to other files:**
- **LEVELSET-v2.md** — Permanent snapshot from 2026-03-13. LEVELSET-CURRENT supersedes it as the live state but does not replace it.
- **DECISIONS.md** — Additive-only decision log. LEVELSET-CURRENT reads from it; new decisions flow to it.
- **CLAUDE.md** — Living vault authority. LEVELSET-CURRENT may surface corrections that flow back to CLAUDE.md as updates.

---

## ECOSYSTEM STATE

### Repository

| Field | Value |
|---|---|
| Remote | github.com/loganfinney27/IDAHO-VAULT (public) |
| Primary branch | `origin/main` at `83cb4ee` |
| Open PRs | 0 |
| Open Issues | 0 |
| Last commit | `83cb4ee` — GEMINI.md update (Logan, 2026-03-24) |

### Branch Status

| Branch | Purpose | Commits Ahead | Status |
|---|---|---|---|
| `claude/fix-pr-43-Ogp5S` | Spring Clean — DOCKET/LEVELSET refresh | active | **Current working branch** |
| `vault-moves-2026-03-23` | 30 auto-generated proposed file moves | 1 | **Awaiting Logan's review/decision** |
| `codex/fix-high-priority-bug-in-pr-#34` | REST API credential sanitization (PR #43, superseded) | 3 | **Safe to delete** — superseded by PR #44 |
| `copilot/consolidate-copilot-efforts` | — | 0 | **Safe to delete** — fully merged |
| `copilot/emergency-handoff-swarm-coherence` | — | 0 | **Safe to delete** — fully merged |
| `copilot/fix-token-permissions-and-error-handling` | — | 0 | **Safe to delete** — fully merged |
| `copilot/setup-copilot-instructions` | — | 0 | **Safe to delete** — fully merged |
| `vault-moves-2026-03-16` | Prior proposed file moves | 0 | **Safe to delete** — fully merged |

*Note: Branch deletion requires Logan via GitHub web UI — Claude Code does not have remote delete permissions for non-`claude/*` branches.*

### Infrastructure Inventory

| Asset | Type | Location | Status |
|---|---|---|---|
| `CLAUDE.md` | Administrative | Repo root | On main — operational |
| `CONSTITUTION.md` | Administrative | Repo root | On main — canonical governance |
| `DECISIONS.md` | Administrative | Repo root | On main — 15 confirmed decisions |
| `AGENTS.md` | Administrative | Repo root (or `!ADMIN/`) | On main |
| `VAULT-CONVENTIONS.md` | Administrative | Repo root | On main |
| `GEMINI.md` | Administrative | Repo root | On main — updated 2026-03-24 |
| `sort_audit.py` | Python | `.github/scripts/` | On main, operational (weekly) |
| `idaho_leg_scraper.py` | Python | `.github/scripts/` | On main — running daily 6 AM MT |
| `post_digest.py` | Python | `.github/scripts/` | On main |
| `propose_moves.py` | Python | `.github/scripts/` | On main |
| `wayback_audit.py` | Python | `.github/scripts/` | On main |
| `linear_brief_generator.py` | Python | `.github/scripts/` | On main — Stage 1 mesh pipeline |
| `auto-pr.yml` | YAML | `.github/workflows/` | On main — auto-creates PRs from `claude/*` |
| `branch-cleanup.yml` | YAML | `.github/workflows/` | On main — cleans merged `claude/*` branches |
| `idaho-leg-scraper.yml` | YAML | `.github/workflows/` | On main — daily cron + manual |
| `linear-brief.yml` | YAML | `.github/workflows/` | On main — Linear webhook relay pipeline |
| `.github/actions/setup-vault/` | Composite action | `.github/actions/` | On main — centralized workflow setup |
| `.obsidian/plugins/obsidian-local-rest-api/data.json` | Config | `.obsidian/plugins/` | Sanitized — credentials purged (PR #44) |
| `.gitignore` | Config | Repo root | On main — hardened post-PR #44 |

### Corrections Since LEVELSET-v2 (2026-03-13 → 2026-03-24)

1. **CLAUDE.md on main** — Now on main (was feature branch as of v2).
2. **Legislature scraper on main and running** — Daily cron firing; was on feature branch as of v2.
3. **`!ADMINISTRATION/` → `!ADMIN/`** — Folder structure renamed; zombie references purged in PR #46.
4. **Ethics.md** — Still does not exist.
5. **DECISIONS.md at repo root** — Moved from `!ADMINISTRATION/`; now 15 confirmed decisions (was 5 as of v2).
6. **REST API credentials** — Machine-specific `apiKey` and crypto material purged via PR #44. `.gitignore` updated.
7. **Total commits** — Well past 19; recent merge sequence: PR #34, #39, #40, #44, #46 + direct commits.

---

## CONVERSATION CENSUS

### Tier 1 — Direct Write Access

| Conversation | Role | Known Output | Current Status |
|---|---|---|---|
| **PERSISTENT: CODE AUTHORITY** | Authoritative code session; LEVELSET synthesis; infrastructure | LEVELSET-v2.md, LEVELSET-CURRENT.md, CLAUDE.md, DECISIONS.md | **Active** — executing Option A synthesis |

### Tier Unknown — Reports Not Yet Received

| Conversation | Presumed Role | Known Output | Gap |
|---|---|---|---|
| **PERSISTENT: ADMINISTRATION** | Vault governance, policy | Nothing committed to repo | No LEVELSET report received. Role overlap with CODE AUTHORITY needs resolution. |
| **TASK: LEVELSET reports** | Synthesis routing hub | Distributed LEVELSET v2 prompt; produced Option A/B/C sequencing recommendation | Active but role may be fulfilled after this round |
| **STORY: JFAC Open Meetings** | Journalism story development | Cache block delivered 2026-03-13. People updates, verified facts, open tasks, lessons learned, architectural decisions, transcript protocols. | **Incorporated** into this synthesis. |
| **PROJECT: 2026 Budget Tracker** | Budget tracking | Unknown | No report received |
| **ISSUE: Repository browsing** | Repo navigation | Unknown | No report received |

### Tier 3 — Context/Research (dormant)

| Conversation | Role | Action Needed |
|---|---|---|
| Idaho Public Television overview | IPTV background | None |
| Idaho Reports episode production | Production workflow | None |
| Understanding Black's Law diction... | Legal terminology | None |
| Interpreting an unclear concept | Research | None |
| In the Blink of an Eye book recom... | Craft reference | None |
| INQUIRY: Adobe Premiere Pro | Production software | None |

**Consolidation assessment (unchanged from LEVELSET-v2):** Tier 3 conversations are dormant reference. No consolidation needed. If Logan wants durable notes extracted from any of them into vault Markdown files, that can be done on request.

---

## DECISIONS CURRENT STATE

As of 2026-03-24: **15 confirmed decisions** in DECISIONS.md at repo root. See that file for full text; summary below.

| # | Decision | Status |
|---|---|---|
| 1 | `!ADMIN/` canonical folder structure | ✅ CONFIRMED |
| 2 | Constitution.md replaces Claude.md as governance authority | ✅ CONFIRMED |
| 3 | Capabilities language replaces tiers | ✅ CONFIRMED |
| 4 | Broader digital consciousness framing adopted | ✅ CONFIRMED |
| 5 | FāVS freelance paused | ✅ CONFIRMED |
| 6 | PERMANENT: AUTHORITY: CODE is correct conversation name | ✅ CONFIRMED |
| 7 | Native protocols over MCP | ✅ CONFIRMED |
| 8 | Slack is ephemeral; vault is the record | ✅ CONFIRMED |
| 9 | AGENTS.md lives in `!ADMIN/`, not `.github/` | ✅ CONFIRMED |
| 10 | `copilot-instructions.md` guardrails in place | ✅ CONFIRMED |
| 11 | Logan's Project = unachievable end goal on the horizon | ✅ CONFIRMED |
| 12 | OpenClaw is a peer system | ✅ CONFIRMED |
| 13 | Slack-to-file rule adopted in principle | ✅ CONFIRMED |
| 14 | STORY: JFAC is read-only | ✅ CONFIRMED |
| 15 | Security hardening: input sanitization + content validation | ✅ CONFIRMED |

**Pending Logan's review (DECISIONS.md):** AGENTS-v0.2-DRAFT.md approval, ORIENTATE-v0.1-BETA.md approval, LEVELSET-LITE-v0.1.md approval, AUTHORITY: ADMIN: CLAUDE consolidation, FāVS resume decision, Gemini ADMIN scope.

---

## JFAC OPEN MEETINGS — SESSION CONTRIBUTION (2026-03-12)

Source: STORY: JFAC Open Meetings session cache block, routed by Logan 2026-03-13.

### Project Status

| Field | Value |
|---|---|
| Story | JFAC working groups / open meetings |
| CCA letter deadline | ~2026-03-18 |
| Sunshine Week | 2026-03-15 through 2026-03-21 |
| Draft exists | 3-10_JFAC_working_groups_-1.docx |
| Editorial constraint | IPTV state agency status; [[Clark Corbin]] (Idaho Capital Sun) carries primary byline burden |

### People Updates

**[[Kyle Harris]]** — CORRECTED
- Was: conflated with [[Mark Harris]]
- Now: Junior House member, Lewiston (House)
- Action needed: Vault note needs first name correction, separate entry from [[Mark Harris]]

**[[Mark Harris]]** — Senior Senate member, Soda Springs area (Senate)
- Interview still needed
- Expressed frustration at Monday JFAC hearing re working groups — pull Idaho In Session archive

**[[Cornel Rasor]]** — NAY on S1331 confirmed from vote board image
- Pattern: NAY on Rule 27 suspension + NAY on S1331
- Interview priority: Friday, Mason's Manual angle

**[[Britt Raybould]]** — NAY on S1331 confirmed from vote board image
- Interview priority: Friday hallway catch only

**Rep. Bruce** — NEW
- First year on JFAC
- Working group assignments top-down from leadership, no member input confirmed
- On record favoring transparency: "I've always been for more transparency" [AUDIO VERIFICATION REQUIRED]

**[[Dustin Manwaring]]** — AYE on S1331 (read from vote board, one Manwaring in House, high confidence)
- On record: "I'm a sunshine person" [AUDIO VERIFICATION REQUIRED]
- On record: "Should it be an open and public process — I would air that, I would be fine with that personally" [AUDIO VERIFICATION REQUIRED]

**[[Wintrow]]** — CORRECTION
- Previous entry assigned role "Senate President Pro Tem / Anthon's number two" — **THIS WAS FABRICATED, no source basis**
- Actual role: unconfirmed, needs verification
- [[Kelly Anthon]] is Senate President Pro Tem

### Verified Facts (sourced, not yet audio-verified for quotes)

1. Working group assignment sheet exists, distributed to all JFAC members (Cook, Woodward-and-Cook transcript)
2. Active quorum management confirmed on record (Woodward-and-Cook transcript)
3. Working group assignments come from leadership, not member preference (Bruce transcript)
4. No parliamentary appeal of working group decisions on record (Cook: "not that I know of")
5. JFAC rules never voted on by full committee per Cook (Woodward-and-Cook transcript)

### Pending Verification Queue

All items below are **HARD GATES** before publication:

| Quote / Claim | Speaker | Source | Status |
|---|---|---|---|
| "Without a TV or a microphone" | Speaker 3 (identity unknown) | Transcript | SPEAKER UNVERIFIED |
| "The rules were never voted on by the committee" | Cook | Woodward-and-Cook transcript | AUDIO VERIFICATION REQUIRED |
| "I'm a sunshine person" | Manwaring | Interview | AUDIO VERIFICATION REQUIRED |
| "Should it be an open and public process — I would air that" | Manwaring | Interview | AUDIO VERIFICATION REQUIRED |
| "I've always been for more transparency" | Bruce | Interview | AUDIO VERIFICATION REQUIRED |
| All Woodward-and-Cook speaker IDs | Speaker 2 vs Speaker 3 | Transcript | IDENTITY UNVERIFIED |

### Open Tasks (from JFAC session)

| Task | Owner | Status | Gate |
|---|---|---|---|
| Correct [[Kyle Harris]] vault note (first name, chamber) | Any session | PENDING | — |
| New vault note: [[Cornel Rasor]] | Any session | PENDING | — |
| New topic note: House Rule 27 | Any session | PENDING | — |
| Working group assignment sheet records request | Logan | PENDING | — |
| Pull Idaho In Session: Kyle Harris Monday JFAC hearing | Logan | PENDING | — |
| Audio verify all 2026-03-10 transcript quotes | Logan | HARD GATE | Pre-pub |
| Grow/Tanner interview — public access question | Logan | PENDING | Mar 18 |
| [[Mark Harris]] interview | Logan | PENDING | — |
| Patch increment 2 (Monks, Rasor, Rule 27, 2024-01-09 IR) | Any session | PENDING | — |
| Vault patch collision check (vault-deploy.zip) | Repo session | BLOCKED | Pre-commit |
| BIN processing pipeline architecture | Audio session | ASSIGNED | — |

### Transcript Processing Protocols

**Google Recorder .txt files:**
- Speaker tags non-persistent, identity-unverified by definition
- All quotes: SPEAKER UNVERIFIED until human audio check
- Re-processing must start from vault note, not raw file
- Verification gate covers both speaker ID and quote accuracy

**Adobe Premiere Pro transcripts:**
- Read-only. Syntax must be preserved for editorial re-import
- No vault notes derived until format protocol defined by Logan
- Separate processing protocol required before Claude handling

**Blocking dependency:** [[Audrey Dutton]] — Idaho reporter. Source relationship to cultivate. Peer with likely applicable experience in AI-assisted transcript processing and bulk research workflows. Reporter-to-reporter conversation needed before pipeline architecture is finalized. Not a tool dependency — a human expertise node.

### Lessons Learned (2026-03-12 session)

Four failure modes identified — permanent record, never delete:

1. **Context-triggered confabulation** — Claude fabricated Wintrow's role based on contextual inference, not source material
2. **Verification flag stripping** — Unverified speaker IDs lost their flags during processing
3. **Misattribution within auto-generated transcript** — Google Recorder speaker tags are not reliable identity markers
4. **Inference presented as sourced record** — Claude treated its own inferences as if they were sourced facts

### Idaho Reports Byline Archive

- 268 posts, 23 pages at blog.idahoreports.idahoptv.org
- Earliest: November 2020
- Vault captures approximately 1% of published output
- Two high-priority missing pieces:
  - 2024-03-29: "Open meetings law questioned with tense budget season" (direct prior reporting on JFAC/open meetings)
  - 2024-03-11: "Senate pushes to re-adopt JFAC rules"
- Both need vault notes in SOURCES/NEWS MEDIA

---

## SOURCING & SENSITIVITY

Updated with JFAC session incorporation:

- All committed content is on the record
- No background-sourced material identified in repo
- No off-the-record material held by this session
- JFAC session cache block received and incorporated — all material in the block was provided by Logan for on-the-record inclusion
- Multiple quotes flagged AUDIO VERIFICATION REQUIRED — these are on the record but **not publication-ready** until verification clears

---

## UNRESOLVED & PENDING

### Awaiting Logan

| Item | Priority | Notes |
|---|---|---|
| Audio verify JFAC quotes (5 quotes + speaker IDs) | **High** | HARD GATE for publication. See Pending Verification Queue above. |
| `vault-moves-2026-03-23` branch decision | **Medium** | 30 auto-proposed file moves (US states to `PLACES/OTHER/STATES/`). Review, apply, or discard. |
| Delete stale remote branches (6) | Medium | `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4), `vault-moves-2026-03-16` — safe to delete via GitHub web UI |
| Pending decisions review (DECISIONS.md) | Medium | AGENTS-v0.2, ORIENTATE-v0.1, LEVELSET-LITE, etc. |
| Ethics.md creation | Low | No draft exists anywhere in the ecosystem |
| LEVELSET cadence decision | Low | Weekly? Milestone-triggered? Needs a standing rule. |
| Gemini capability tier scope | Low | Undefined — Gemini blocked from vault commits until scoped |

### Known Technical Issues

| Issue | Priority | Notes |
|---|---|---|
| Sort audit false positives | Low | Out-of-state counties flagged as Idaho counties in `sort_audit.py` |
| `X LABELER/` unsorted files | Ongoing | Manual triage by Logan |
| ~3,400 markdown files at repo root | Low | Massive root-level clutter; `vault-propose-moves` workflow addresses incrementally |

---

## WHAT THIS SYNTHESIS IS MISSING

Transparency about gaps — this section exists so Logan and other conversations know exactly what's thin:

1. ~~**JFAC Open Meetings session context**~~ — **RESOLVED.** Cache block received and incorporated 2026-03-13.

2. **Conversation census is stale** — The CONVERSATION CENSUS below reflects March 2026 conversation state. Active conversations and their outputs have not been re-surveyed for this update.

3. **PROJECT: 2026 Budget Tracker state** — Unknown scope, architecture, data sources, progress.

4. **Audio verification for all JFAC quotes** — Five quotes and full Woodward-and-Cook speaker ID verification are HARD GATES before publication. Only Logan can clear these.

5. **Gemini vault activity** — Gemini's capability tier is undefined; no vault commits exist. GEMINI.md was updated 2026-03-24 by Logan directly but scope remains unscoped.

---

## NEXT ACTIONS

1. ~~Commit LEVELSET-CURRENT.md to separate branch~~ — Done (historically)
2. ~~Wait for JFAC session cache block from Logan~~ — Received and incorporated
3. ~~Merge feature branches (scraper, CLAUDE.md, DECISIONS.md) to main~~ — Done
4. ~~Sanitize REST API credentials~~ — Done (PR #44)
5. ~~Centralize workflow setup~~ — Done (PR #46)
6. Logan: delete 6 stale branches via GitHub web UI
7. Logan: decide on `vault-moves-2026-03-23` (30 proposed file moves)
8. Logan: audio verify JFAC quotes (HARD GATE before publication)
9. Logan: review pending decisions in DECISIONS.md

---

*LEVELSET-CURRENT.md — Originally synthesized 2026-03-13 by PERSISTENT: CODE AUTHORITY. Updated 2026-03-24 by Claude Code (The Abhorsen), Operation: Spring Clean. This is a living document, updated each LEVELSET round. For the permanent audit trail, see numbered LEVELSET files in this directory.*
