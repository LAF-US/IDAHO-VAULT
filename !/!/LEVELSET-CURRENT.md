# LEVELSET-CURRENT — Live Ecosystem State

**Date:** 2026-03-28 (updated: Gemini Code Assist cowork enabled; stale refs cleaned; frontmatter spring clean; PR #98 open)
**Status:** CURRENT — living synthesis, updated each LEVELSET round
**Synthesized by:** Claude Code (The Abhorsen) — LEVELSET round triggered 2026-03-28
**Input authority chain:** CONSTITUTION.md > DECISIONS.md > CLAUDE.md
**Approved by:** Pending Logan Finney review

---

## What This File Is

LEVELSET-CURRENT is the rolling synthesis document. Unlike numbered LEVELSET files (v1, v2, v3...) which are permanent snapshots, LEVELSET-CURRENT reflects the **present state** of the ecosystem. It is updated — not appended — each round. The numbered files remain the permanent audit trail.

**Relationship to other files:**
- **LEVELSET-v2.md** — Permanent snapshot from 2026-03-13. In `!/!/` archive.
- **DECISIONS.md** — Additive-only decision log. Now at `!/DECISIONS.md`.
- **CLAUDE.md** — Living vault authority. Repo root (must stay there for Claude Code auto-load).

---

## ECOSYSTEM STATE

### Repository

| Field | Value |
|---|---|
| Remote | github.com/loganfinney27/IDAHO-VAULT (public) |
| Primary branch | `origin/main` at `c708bb7` |
| Active branch | `gemini/activate-linear-pilot` |
| Open PRs | PR #98 (`gemini/activate-linear-pilot` — 3 commits this session), PR #83 (`claude/update-habit-tracker-todo-p18EW`), PRs #84–96 (Codex/Copilot backlog — 13 PRs) |
| Last commit | `3563a66` — feat: Enable Gemini Code Assist cowork |

### Branch Status

| Branch | Purpose | Status |
|---|---|---|
| `gemini/activate-linear-pilot` | Linear Phase 1 pilot scoping + Gemini tier + infrastructure commits | **Active (current)** |
| `claude/update-habit-tracker-todo-p18EW` | Habit tracker / PR #83 | **Awaiting Logan merge** |
| `claude/agent-dotfolder-architecture` | Agent dotfolder architecture | **Local — no PR yet** |
| `vault-moves-2026-03-23` | 30 auto-proposed file moves (US states) | **Awaiting Logan's review/decision** |

**Remote Codex branches (stale — awaiting Logan deletion or merge):**
`codex/linear-mention-laf-7` through `codex/linear-mention-laf-15` (LAF swarm decomposition), `codex/create-manifest.json-specification-and-guidelines`, `codex/revise-persona-and-constitutional-files`, `copilot/logans-project-execution`

*Note: Remote branch deletion requires Logan via GitHub web UI.*

### Infrastructure Inventory

| Asset | Type | Location | Status |
|---|---|---|---|
| `CLAUDE.md` | Administrative | Repo root | On main — operational |
| `GEMINI.md` | Administrative | Repo root | On main |
| `!/CONSTITUTION.md` | Administrative | `!/` | Moved from root — canonical governance |
| `!/DECISIONS.md` | Administrative | `!/` | Moved from root — 15 confirmed decisions |
| `!/AGENTS.md` | Administrative | `!/` | Moved from root |
| `!/LEVELSET.md` | Administrative | `!/` | Moved from root |
| `!/PROTOCOL.md` | Administrative | `!/` | Moved from root |
| `!/VAULT-CONVENTIONS.md` | Administrative | `!/` | Moved from root |
| `!/SWARM.md` | Administrative | `!/` | Moved from root |
| `!/MCP-IMPLEMENTATION-PLAN.md` | Administrative | `!/` | Added 2026-03-24 |
| `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` | Protocol | `!/` | Canonical external agent prompt |
| `sort_audit.py` | Python | `.github/scripts/` | On main, operational (weekly) |
| `idaho_leg_scraper.py` | Python | `.github/scripts/` | On main — running daily 6 AM MT |
| `post_digest.py` | Python | `.github/scripts/` | On main |
| `vault-ingest.yml` | YAML | `.github/workflows/` | On main — ingest pipeline initialized |
| `auto-pr.yml` | YAML | `.github/workflows/` | On main — auto-creates PRs from `claude/*` |
| `branch-cleanup.yml` | YAML | `.github/workflows/` | On main — cleans merged `claude/*` branches |
| `.obsidian/plugins/obsidian-local-rest-api/data.json` | Config | `.obsidian/plugins/` | Sanitized — credentials purged (PR #44) |
| `.gitignore` | Config | Repo root | On main — hardened; workspace.json untracked this session |

### Activity Since Previous LEVELSET-CURRENT (2026-03-24 → 2026-03-28)

1. **Plugin auth inventory completed (2026-03-28)** — Codex ran read-only probe of all 7 enabled connectors. GitHub, Linear, Slack, Google Calendar, Google Drive, Hugging Face all verified. Cloudflare `not-directly-probeable`. Report at `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` (committed).
2. **Linear LAF issues decomposed** — Codex opened branches for LAF-7 through LAF-15 on remote; 13 PRs open awaiting Logan merge.
3. **`tag_stubs.py` added** — Frontmatter refactor script added by Codex (`3f9a945`); admin files relocated to `/!` subdirectory; `sort_audit.py` updated for new paths.
4. **`date_tagger.py` added** — Tags 39 source notes with YYYY/MM/DD publish date (`2224689`).
5. **Daily notes hardened** — Frontmatter standardized, conflict duplicates resolved, bad-date filenames corrected, navigation links patched.
6. **Codex tooling aligned** — `c708bb7` aligned Codex tooling and hardened vault automation.
7. **`swarm/` Python application** — `swarm/app.py` (126 lines), `swarm/tests/test_app.py`, `swarm/README.md` committed; `!/SWARM-LOOP.md` added as vault-facing README.
8. **10 untracked content docs committed** (`07d2cb7`) — AGENTIC SWARM SYSTEMS, AI-AUTOMATION TOOL LANDSCAPE, IDAHO-VAULT SYSTEM CONTEXT/WORKFLOW/JOURNALISM-WORKFLOW, JOURNALISM INDUSTRY, Kano Play, Notebook LM, Podcast, David Leroy — all tagged and frontmatter-clean.
9. **Stale `!ADMIN/` references cleaned** (`ba01c2e`) — DECISIONS.md (rows 1, 9, 10 + section titles), LEVELSET-STEP-0, THREAT-MODEL. Root frontmatter spring-cleaned (10 files + SWARM-LOOP).
10. **Gemini Code Assist cowork enabled** (`3563a66`) — `.gemini/GEMINI.md` tier fixed (Advisory → Tier 1 Support), cowork pattern with Abhorsen documented, Code Assist section added. `.gemini/settings.json` context expanded to 6 files. `GEMINI.md` + `!/AGENTS.md` updated.
11. **`claude/agent-dotfolder-architecture` local branch deleted** — already merged to main (remote was gone).
12. **PR #98 opened** — covers all 3 commits from this session; flags PR #84 conflict and pending DECISIONS items 18–21.

---

## CONVERSATION CENSUS

### Tier 1 — Direct Write Access

| Conversation | Role | Known Output | Current Status |
|---|---|---|---|
| **PERSISTENT: CODE AUTHORITY** | Authoritative code session; LEVELSET synthesis; infrastructure | LEVELSET-v2.md, LEVELSET-CURRENT.md, CLAUDE.md, DECISIONS.md, swarm nest reorganization, Chorus Bootstrap | **Active** |

### Tier Unknown — Reports Not Yet Received

| Conversation | Presumed Role | Known Output | Gap |
|---|---|---|---|
| **PERSISTENT: ADMINISTRATION** | Vault governance, policy | Nothing committed to repo | No LEVELSET report received. Role overlap with CODE AUTHORITY needs resolution. |
| **PROJECT: 2026 Budget Tracker** | Budget tracking | Unknown | No report received |

### Tier 3 — Context/Research (dormant)

Dormant reference conversations — no action needed.

---

## DECISIONS CURRENT STATE

As of 2026-03-28: **17 confirmed decisions** + **4 pending decisions (18–21)** in `!/DECISIONS.md`. Decisions 18–21 were auto-generated from content docs committed this session; marked `Status: Pending`; require Logan review. Decision 21 flagged ⚠️ requires CODE AUTHORITY review before publishing.

| # | Decision | Status |
|---|---|---|
| 1 | `!ADMIN/` canonical folder structure | ✅ CONFIRMED — `!ADMIN/` deleted; `!/` is canonical |
| 2 | Constitution.md replaces Claude.md as governance authority | ✅ CONFIRMED |
| 3 | Capabilities language replaces tiers | ✅ CONFIRMED |
| 4 | Broader digital consciousness framing adopted | ✅ CONFIRMED |
| 5 | FāVS freelance paused | ✅ CONFIRMED |
| 6 | PERMANENT: AUTHORITY: CODE is correct conversation name | ✅ CONFIRMED |
| 7 | Native protocols over MCP | ✅ CONFIRMED |
| 8 | Slack is ephemeral; vault is the record | ✅ CONFIRMED |
| 9 | AGENTS.md lives in `!/`, not `.github/` | ✅ CONFIRMED |
| 10 | `copilot-instructions.md` guardrails in place | ✅ CONFIRMED |
| 11 | Logan's Project = unachievable end goal on the horizon | ✅ CONFIRMED |
| 12 | OpenClaw is a peer system | ✅ CONFIRMED |
| 13 | Slack-to-file rule adopted in principle | ✅ CONFIRMED |
| 14 | STORY: JFAC is read-only | ✅ CONFIRMED |
| 15 | Security hardening: input sanitization + content validation | ✅ CONFIRMED |
| 16 | MCP allowed as transport only; native vault terms canonical | ✅ CONFIRMED (2026-03-24) |
| 17 | STEP-0 LEVELSET prompt for external agents | ✅ CONFIRMED (2026-03-22) |

**Pending Logan's review:** AGENTS-v0.2-DRAFT.md approval, ORIENTATE-v0.1-BETA.md approval, LEVELSET-LITE-v0.1.md approval, AUTHORITY: ADMIN: CLAUDE consolidation, FāVS resume decision, Gemini ADMIN scope.

---

## JFAC OPEN MEETINGS — SESSION CONTRIBUTION (2026-03-12)

*(Unchanged from previous LEVELSET-CURRENT — see that document in `!/!/` archive for full detail.)*

Key status: Multiple quotes flagged **AUDIO VERIFICATION REQUIRED** — HARD GATES before publication. Only Logan can clear these.

---

## SOURCING & SENSITIVITY

- All committed content is on the record
- No background-sourced material identified in repo
- JFAC session cache block received and incorporated — multiple quotes flagged AUDIO VERIFICATION REQUIRED, not publication-ready until cleared

---

## UNRESOLVED & PENDING

### Awaiting Logan

| Item | Priority | Notes |
|---|---|---|
| Audio verify JFAC quotes (5 quotes + speaker IDs) | **High** | HARD GATE for publication |
| Review + merge PR #98 (`gemini/activate-linear-pilot`) | **High** | 3 commits: content triage, stale ref cleanup, Gemini Code Assist enablement |
| ⚠️ Review PR #84 (`codex/revise-persona-and-constitutional-files`) | **High** | Conflicts with PR #98 on `.gemini/GEMINI.md` and `GEMINI.md`; also touches `!/CONSTITUTION.md` (Constitutional zone). Recommend close as superseded. |
| Review DECISIONS.md pending items 18–21 | **High** | Auto-generated from content docs; Decision 21 flagged ⚠️ CODE AUTHORITY review before publishing |
| Review + merge PR #83 (`claude/update-habit-tracker-todo-p18EW`) | **Medium** | Active branch — awaiting Logan review |
| Chorus Bootstrap — 5 decisions | **Medium** | See DOCKET; Logan's answers unlock Pieces 3, 4, 5 |
| `vault-moves-2026-03-23` branch decision | **Medium** | 30 auto-proposed file moves (US states). Review, apply, or discard. |
| Delete stale remote branches | **Medium** | PRs #84–96 backlog (13 Codex/Copilot PRs). Plus stale local branches already cleaned. |
| Pending decisions review (`!/DECISIONS.md`) | Medium | AGENTS-v0.2, ORIENTATE-v0.1, LEVELSET-LITE, etc. |
| Gemini Code Assist activation | **Medium** | Install VS Code extension + sign in to `idaho-vault` Google Cloud project; `cloudcode.duetAI.project` setting may need ID correction |
| Obsidian sync conflict copies | Low | `2026-03-27` and `2026-03-28` daily note conflicts untracked — resolve via Obsidian Sync UI |
| Ethics.md creation | Low | No draft exists anywhere |
| LEVELSET cadence decision | Low | Weekly? Milestone-triggered? Needs a standing rule. |
| ~~Commit/triage untracked content docs~~ | ~~Done~~ | Committed `07d2cb7` |
| ~~`claude/agent-dotfolder-architecture` branch~~ | ~~Done~~ | Already merged to main; local branch deleted |
| ~~Gemini capability tier scope~~ | ~~Resolved~~ | Tier 1 Support defined + Code Assist cowork enabled `3563a66` |

### Known Technical Issues

| Issue | Priority | Notes |
|---|---|---|
| Sort audit false positives | Low | Out-of-state counties flagged as Idaho counties |
| `X LABELER/` unsorted files | Ongoing | Manual triage by Logan |
| ~3,400 markdown files at repo root | Low | `vault-propose-moves` workflow addresses incrementally |

---

## WHAT THIS SYNTHESIS IS MISSING

1. **Conversation census is stale** — Active conversations and their outputs not re-surveyed.
2. **PROJECT: 2026 Budget Tracker state** — Unknown scope, architecture, data sources, progress.
3. **Audio verification for JFAC quotes** — Five quotes and Woodward-and-Cook speaker ID verification are HARD GATES.
4. **Codex LAF PR outcomes** — 13 Codex/Copilot PRs (#84–96) open; content overlap and merge readiness not fully assessed.
5. **Chorus Bootstrap decisions** — Logan's 5 decisions outstanding; CONVENE-frozen items remain blocked until answered.
6. **DECISIONS 18–21 legitimacy** — Auto-generated; may or may not reflect Logan-approved decisions. Require Logan review before confirming.

---

## NEXT ACTIONS

1. Logan: audio verify JFAC quotes — 5 quotes + speaker IDs (HARD GATE before publication)
2. Logan: review + merge PR #98 (`gemini/activate-linear-pilot`) — stale refs, frontmatter, Gemini Code Assist
3. Logan: review PR #84 — recommend close as superseded; check `!/CONSTITUTION.md` change before closing
4. Logan: review DECISIONS.md pending items 18–21 (auto-generated; Decision 21 flagged ⚠️)
5. Logan: review + merge PR #83 (`claude/update-habit-tracker-todo-p18EW`)
6. Logan: answer 5 Chorus Bootstrap decisions (see DOCKET)
7. Logan: review 13-PR Codex/Copilot backlog (#84–96) — triage, merge, or close
8. Logan: install Gemini Code Assist VS Code extension + sign in to `idaho-vault` GCP project
9. Logan: decide on `vault-moves-2026-03-23` (30 proposed file moves)
10. ~~Logan: scope Linear-first write pilot~~ **Done**
11. ~~Agents: commit/triage untracked content docs~~ **Done** (`07d2cb7`)
12. ~~Fix stale !ADMIN/ references~~ **Done** (`ba01c2e`)
13. ~~Enable Gemini Code Assist cowork~~ **Done** (`3563a66`)

---

*LEVELSET-CURRENT.md — Originally synthesized 2026-03-13. Updated 2026-03-24 (Spring Clean), 2026-03-24 (Swarm Nest Reorganization), 2026-03-28 (Plugin Auth Inventory + Codex tooling sprint), 2026-03-28 (Linear Phase 1 pilot scoped + Gemini tier defined; Logan-delegated symphony round), and 2026-03-28 (Gemini Code Assist cowork enabled; stale refs cleaned; frontmatter spring clean) by Claude Code (The Abhorsen). Living document, updated each LEVELSET round. Permanent audit trail in numbered LEVELSET files at `!/!/`.*
