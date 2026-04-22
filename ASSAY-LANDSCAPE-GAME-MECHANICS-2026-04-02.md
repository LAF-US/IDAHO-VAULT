---
title: Landscape Assay — Game Mechanics Study Application
created: 2026-04-02
updated: 2026-04-02
status: filed
authority: claude
doc_class: misc_reference
source: SWARM INQUIRY — Study Application & Dot-Connection, Logan Finney, 2026-04-02
date created: Wednesday, April 1st 2026, 11:16:46 pm
date modified: Thursday, April 2nd 2026, 10:36:09 pm
related:
- '104'
- '107'
- '108'
- '135'
- '137'
- '140'
- '141'
- '144'
- '2026-03-23'
- '2026-03-25'
- '2026-03-28'
- '2026-03-30'
- '2026-04-01'
- '2026-04-02'
- '722'
- AGENTS
- API
- BOOTSTRAP
- Bartimaeus
- CLAUDE
- CSV
- Copilot
- CrewAI
- DECISIONS
- DOT
- GEMINI
- GROK
- GitHub
- LAF
- LEVELSET
- LEVELSET-CURRENT
- Logan Finney
- Logan's
- MCP
- MCP-DISCOVERY-2026-03-25
- Microsoft Copilot
- Obsidian
- PERPLEXITY
- PERSEPHONE
- PROJECT
- PROTOCOL
- Phone Link
- TRIUNE
- VAULT-CONVENTIONS
- WIP
- ZAGREUS
- agent
- codex
- coordination
- definition
- doctrine
- index
- systems
- template
---
# Landscape Assay — Game Mechanics Study Application

**Inquiry:** CLAUDE CODE BOOTSTRAP PROMPT — Landscape assay + dot-connection
**Requested by:** Logan Finney
**Filed by:** Claude Code (The Abhorsen), branch `claude/study-game-mechanics-STrAW`
**Date:** 2026-04-02

**Core finding:** The vault exhibits strong PC and Ender Chest layers; the HOME-layer gap creates routing and context persistence bottlenecks. Architecture clarity is achievable through small, targeted improvements tied to Constitution.md V1, CrewAI readiness, and routing reliability.

---

## TASK 1: AUDIT — Current State Inventory

### 1.1 Dotfolder Coverage (Ender Chest Inventory)

**Status:** Partial. Dotfolders exist; agent context files are inconsistently complete.

| Agent | Dotfolder | Primary File | Secondary Files | Status |
|---|---|---|---|---|
| **Claude Code (Abhorsen)** | `.claude/` | `CLAUDE.md` | `settings.json` (updated 2026-04-02) | ✅ Complete |
| **Codex (Lexicographer)** | `.codex/` | `CODEX.md` | `config.toml` (updated 2026-04-02) | ✅ Complete |
| **Gemini (Vault Advisor)** | `.gemini/` | `GEMINI.md` | `settings.json` (updated 2026-04-02) | ✅ Complete |
| **Bartimaeus (Witness)** | `.bartimaeus/` | `BARTIMAEUS.md` | — | ⚠️ Stub; role pending Logan definition |
| **DeepSeek** | `.deepseek/` | `DEEPSEEK.md` | — | ⚠️ Stub; no current usage |
| **Dionysus** | `.dionysus/` | — | — | ❌ Missing |
| **Grok (X/xAI)** | `.grok/` | `GROK.md` | — | ⚠️ Stub; advisory-only per AGENTS.md |
| **Perplexity** | `.perplexity/` | `PERPLEXITY.md` | — | ⚠️ Stub; advisory-only per AGENTS.md |
| **Persephone** | `.persephone/` | `PERSEPHONE.md` | — | ⚠️ Stub; no current usage |
| **Zagreus** | `.zagreus/` | `ZAGREUS.md` | — | ⚠️ Stub; no current usage |
| **Abhorsen** | `.abhorsen/` | — | `New Text Document.txt` (empty) | ❌ Incomplete |

**Analysis:** 
- **3 agents fully active** (Claude Code, Codex, Gemini) with complete dotfolder context.
- **6 agents stubbed** but not yet scoped (DeepSeek, Grok, Perplexity, Persephone, Zagreus, Bartimaeus).
- **1 placeholder** (Abhorsen) with placeholder file.
- **No agent is missing AGENT.md entirely;** all have some form of context file.
- **Inconsistency:** Some have settings/config files; others don't. No standardized structure.

**Ender Chest Coherence Score:** 35/100 (functional for active agents; overhead agents not ready for plug-and-play activation).

---

### 1.2 Canvas Presence and Indexing

**Status:** Minimal. Canvas exists as Slack capability; not yet integrated into vault routing.

**Canvas References Found:**
- 1 mention in `!/MCP-DISCOVERY-2026-03-25.md` (Slack Canvas API, `slack_create_canvas`, `slack_update_canvas`)
- 0 Canvas documents currently tracked in vault
- No Canvas-native routing rule documented

**Analysis:**
- Canvas is recognized as **more stable than Slack** (per LEVELSET-CURRENT, 2026-03-30).
- Slack routing is **unreliable** (message delivery, thread tracking inconsistent).
- Canvas routing is **stable** but not integrated into all workflows.
- No decision yet on Canvas as primary coordination layer.

**Canvas Readiness Score:** 20/100 (recognized; not yet formalized or integrated).

---

### 1.3 Slack vs. Canvas Usage Pattern (Recent 10 Routing Events)

**Sample:** Git log analysis of recent agent dispatches and coordination patterns.

| Event | Channel | Medium | Reliability | Notes |
|---|---|---|---|---|
| PR 144 merge dispatch | Slack (inferred) | Ephemeral | ⚠️ Unreliable | Phone Link intake pipeline routed via git; unclear Slack coordination |
| PR 141 CI diagnosis | Linear + GitHub | Structured | ✅ Reliable | `LINEAR_API_KEY` issue resolved via GitHub + Linear; Slack breadcrumb only |
| PR 140 workflow automation | GitHub | Structured | ✅ Reliable | Workflow automation via .github/workflows/ not Slack |
| PR 137–104 PR conflicts | GitHub + linear | Structured | ✅ Reliable | Multi-PR merge coordination via GitHub UI + Linear |
| DOCKET updates | Vault file | Durable | ✅ Reliable | Live coordination board at `!/DOCKET.md`; canonical record |
| LEVELSET synthesis | Vault file | Durable | ✅ Reliable | `LEVELSET-CURRENT.md` updated 2026-03-30; living document |
| Agent briefings | GitHub Issues | Structured | ✅ Reliable | LAF-7, LAF-12, LAF-17, LAF-18 issues track work; agent labels scoped |
| Slack breadcrumbs | Slack | Ephemeral | ⚠️ Unreliable | Standing rule: "Slack carries breadcrumbs; vault is the record" |
| Canvas routing | (Not yet active) | — | — | Identified but not yet formalized |
| Swarm dispatches | DOCKET + Linear | Durable | ✅ Reliable | Standing direction 2026-03-25: tasks via Linear + GitHub Issues |

**Analysis:**
- **Reliable routing:** Linear, GitHub Issues, GitHub PRs, vault files.
- **Unreliable routing:** Slack (ephemeral, lossy, unindexed).
- **Stable but dormant:** Canvas (available, not yet decision-driven).
- **Standing doctrine (from LEVELSET-CURRENT):** "Vault is the record. Slack carries breadcrumbs. Chat is ephemeral."

**Routing Clarity Score:** 65/100 (pattern clear; formalization pending in Constitution.md V1).

---

### 1.4 LEVELSET-CURRENT State

**Last Updated:** 2026-03-30 (3 days old, as of assay date 2026-04-02).

| Metric | Value | Assessment |
|---|---|---|
| **Update frequency** | Updated on major LEVELSET events (TRIUNE COVENANT 2026-03-30, Gemini tier defined 2026-03-28, Linear Phase 1 2026-03-28) | ✅ Event-driven; current |
| **Completeness score** | ~80/100 (ecosystem state thorough; DECISIONS count accurate; activity log comprehensive; JFAC gate notes exact) | ✅ High |
| **Stale narratives** | PROJECTS section ("PROJECT: 2026 Budget Tracker state — Unknown scope") flagged as incomplete; some pending items marked 2026-03-28 but no update since | ⚠️ Selective staleness |
| **Machine-queryability** | None; narrative markdown; requires manual parsing | ❌ Not queryable |
| **Granular artifact index** | None; synthesis only; no artifact-level metadata | ❌ Missing HOME-layer |

**Analysis:**
- LEVELSET-CURRENT **is the closest thing to a HOME-layer** in the current architecture.
- It survives between sessions and is accessible to all agents.
- **Gap:** It is not machine-queryable; artifact-level metadata is missing.
- A structured companion (CSV, JSON, Canvas doc) could bridge the HOME-layer gap without replacing LEVELSET-CURRENT.

**LEVELSET Completeness Score:** 80/100 (good narrative; poor discoverability).

---

### 1.5 Git Branching Status

**Branches (as of 2026-04-02):**

| Branch | Type | Status | PR | Notes |
|---|---|---|---|---|
| `main` | Primary | Current (3f23071) | — | Latest commit: chore: commit Obsidian reference captures |
| `claude/study-game-mechanics-STrAW` | Feature | Local (current) | — | This branch; assay work in progress |
| `claude/study-game-mechanics-qZK5E` | Feature (merged) | Remote/merged | PR 135 ✅ | Game mechanics study; merged 2026-04-01 |
| `claude/phone-link-integration-Ny9GC` | Feature (merged) | Remote/merged | PR 144 ✅ | Phone Link intake pipeline; merged 2026-04-02 |
| `claude/research-unified-swarm-rDmOg` | Feature (open) | Remote/open | PR 108 🔄 | Research unified swarm; awaiting Logan review |
| `claude/resolve-pr-conflicts` | Feature (open) | Remote/open | PR 104 🔄 | Resolve PR conflicts; awaiting Logan review |
| `claude/mcp-phase-0-discovery` | Feature (stashed) | Local (stash {0}) | — | WIP stash present; not applied or dropped |
| `vault-moves-2026-03-23` | Feature (proposal) | Local (pending review) | — | 30 auto-proposed file moves (US states) |
| `codex/clean-and-prune-stale-branches` | Feature (merged) | Merged | PR 107 ✅ | Stale branch graveyard cleaned 2026-03-30 |
| Stale remote branches (6) | Cleanup | Awaiting deletion | — | Require manual deletion via GitHub UI per DOCKET |

**Analysis:**
- **Active development:** Fast cadence; 722 commits in 2 weeks.
- **PR backlog:** 2 open PRs awaiting Logan review (PR 108, 104).
- **Branch naming:** Consistent `agent/task-code` pattern; auto-tracked via GitHub Actions.
- **Cleanup overhead:** 6 stale remote branches; cleanup workflow in place but requires Logan UI action.
- **Local stash:** 1 pending stash on `claude/mcp-phase-0-discovery`; decision needed (apply/drop).

**Branch Discipline Score:** 75/100 (good hygiene; some cleanup pending).

---

## TASK 2: DOT-CONNECTION — Game Mechanics to Architecture

### 2.1 PC Layer Insights (Shared Vault Files)

**Observation:** The vault's PC layer is strong, organized, and well-structured.

| Game parallel | IDAHO-VAULT parallel | Status |
|---|---|---|
| Pokemon boxes (organized storage) | `!/` governance files + Tier 1–3 content structure | ✅ Strong |
| PC accessibility (fixed-point, terminal access) | Git commits + PRs (fixed-point access; durable record) | ✅ Strong |
| Entity richness (Pokemon retain full attributes in storage) | Markdown notes with frontmatter metadata (author, date, tags, status, source) | ✅ Strong |
| Party composition as strategy | Context injection via LEVELSET-CURRENT (curated brief for session start) | ✅ Functional |

**Key finding:** The vault has excellent shared storage. Agents can retrieve and integrate complex entities (notes, decisions, briefs). The PC layer is **not a bottleneck.**

**Dead weight identified:**
- `~/X LABELER/` unsorted files (loose at root) — low priority per LEVELSET-CURRENT.
- 6 stale remote branches (git cleanup overhead) — awaiting Logan decision.
- Untracked content docs — largely addressed in recent commits; some drafts may remain.

**PC Layer Health Score:** 85/100 (strong; minor cleanup items).

---

### 2.2 Ender Chest Insights (Dotfolders)

**Observation:** The dotfolder layer exists; coherence is partial.

| Game parallel | IDAHO-VAULT parallel | Status |
|---|---|---|
| Player-UUID-bound storage (personal, identity-scoped) | `.claude/CLAUDE.md`, `.gemini/GEMINI.md`, `.codex/CODEX.md` | ✅ Functional |
| Ubiquitous access (Ender Chest accessible from anywhere) | Dotfolders auto-loaded at session start by respective agents | ✅ Functional |
| Portable nested contexts (Shulker Boxes) | Some dotfolders have config/settings files; no consistent nesting strategy | ⚠️ Inconsistent |
| Different players, different inventory (isolation) | Each agent reads its own dotfolder; swarm sees different contexts per agent | ✅ Working |

**Structural issues:**
1. **Inconsistent structure:** Some agents have 2 files, others 1. No template.
2. **Inactive agents:** 6 agents have stub AGENT.md files but no supporting context (no config, no local task briefs).
3. **No sub-context nesting:** Dotfolders don't yet host nested portable contexts (e.g., task-scoped briefs, decision logs per agent).
4. **No Shulker Box corollary:** Agents cannot easily carry context modules between sessions.

**Ender Chest Health Score:** 50/100 (functional for active agents; overhead agents not ready; no nesting strategy).

---

### 2.3 HOME Layer Gap (Missing Artifact Registry)

**Observation:** This is the critical missing piece.

| Game parallel | IDAHO-VAULT parallel | Status |
|---|---|---|
| Pokemon HOME (durable entity registry, cross-session, cross-instance) | ??? | ❌ Missing |
| Entity survives across sessions | ? | ❌ Unclear |
| Machine-queryable artifact list | ? | ❌ Unclear |
| Agent-independent discovery | ? | ❌ Unclear |

**Current approximations:**
- **LEVELSET-CURRENT:** Narrative synthesis; updated event-driven; not queryable.
- **DECISIONS.md:** Additive decision log; queryable by grep; not artifact-scoped.
- **Git commit history:** Queryable via git log; not structured for artifact discovery.
- **GitHub Issues / Linear:** Taskbase structured; not artifact-output-scoped.

**What's missing:**
- A **structured artifact index** (CSV, JSON, or Canvas doc) listing:
  - Research outputs (briefs, analyses, studies)
  - Decisions (confirmed + pending)
  - Artifacts (entity refs, decision logs, entity aliases)
  - Provenance (agent, date, branch, commit)
  - Cross-session pointers (so Session B can discover Session A's outputs without human relay)

**HOME Layer Gap Score:** 0/100 (not yet implemented; high architectural value if added).

---

### 2.4 Routing Clarity (PC vs. Ender Chest vs. HOME)

**Current state:**
- **PC-layer routing** (shared vault): Clear. Commits, PRs, LEVELSET injection.
- **Ender Chest routing** (dotfolder): Clear. Auto-loaded at session start.
- **HOME-layer routing** (artifact registry): **Nonexistent.** LEVELSET-CURRENT fills the gap narratively.

**Missing decision tree:**
- *When should work be filed to vault root (PC)?* — Broadly shareable, on-the-record content.
- *When should work stay in dotfolder (Ender Chest)?* — Agent-personal instructions, identity-scoped settings.
- *When should work become a discrete artifact in a registry (HOME)?* — Research outputs, decision records, session-scoped work products.

**Constitution.md V1 opportunity:** Formalize this decision tree as a routing protocol.

---

## TASK 3: PROPOSE — 3-5 Small Improvements

### Proposal 1: **Dotfolder Standardization** ⭐⭐⭐ (High impact, quick win)

**What:** All agents get a consistent `.agent/AGENT.md` structure, even if inactive.

**Scope:**
- Template: Agent identity, capability tier, operational scope, recent LEVELSET injection pointer, recent-session context.
- Apply to all 10 agents (create missing DIONYSUS.md; upgrade stubs to full structure).
- Estimated effort: 1–2 hours.

**Expected impact:**
- +clarity for agent onboarding (when overhead agents are activated).
- +speed for swarm reconvergence (any agent can read another's dotfolder and understand its role).
- Foundation for Constitution.md V1 agent table.

**Ties to:**
- Constitution.md V1 (agent capability clarification)
- CrewAI/Copilot readiness (consistent agent introspection)

---

### Proposal 2: **Canvas Routing Formalization** ⭐⭐⭐ (High impact, quick win)

**What:** Add Canvas to Constitution.md V1 as a formal routing choice with decision rules.

**Scope:**
- Document when Canvas is preferred over Slack (long-form, structured, multi-threaded, durable feedback).
- Update DOCKET with a Canvas-native example (or create one as proof-of-concept).
- Link routing rules in VAULT-CONVENTIONS.md.
- Estimated effort: 1 hour.

**Expected impact:**
- +reliability for complex coordination (move unreliable Slack threads to Canvas).
- +signal-to-noise (Canvas audit trail vs. Slack ephemera).
- Faster routing decisions (team knows when to escalate to Canvas).

**Ties to:**
- Routing reliability (Slack → Canvas migration path)
- Swarm coherence (clearer when to use which medium)

---

### Proposal 3: **Artifact Index Prototype (Canvas)** ⭐⭐⭐⭐ (Highest impact, 2–3 hours)

**What:** Create a Canvas doc template as a HOME-layer index (proof-of-concept).

**Scope:**
- Simple 3-column structure: Artifact Type | File Path | Date | Agent | Status.
- Artifact types: research output, decision, brief, entity reference, decision log, context module.
- Populate with 5–10 recent artifacts (studies, briefs, decisions).
- Link from LEVELSET-CURRENT as discoverable resource.
- Estimated effort: 2–3 hours (including Logan review).

**Expected impact:**
- +foundation for HOME-layer (cross-session artifact discovery).
- +testability (can evaluate if agents can find prior work without human relay).
- +basis for creWAI evaluation (multi-agent systems need artifact traceability).

**Ties to:**
- HOME-layer foundation (addresses the Pokemon HOME gap)
- CrewAI readiness (artifact traceability is essential for multi-agent orchestration)
- Constitution.md V1 (documents artifact lifecycle)

---

### Proposal 4: **Agent Succession Protocol** ⭐⭐⭐ (Medium impact, 2–3 hours)

**What:** Draft a lightweight "agent onboarding checklist" for when a new agent activates.

**Scope:**
- Checklist: dotfolder setup, AGENTS.md tier confirmation, boundary rules, local branching rule, recent LEVELSET injection.
- File as `!/AGENT-ONBOARDING-CHECKLIST.md`.
- Use for next agent activation (e.g., when Bartimaeus, Persephone, or Zagreus move from stub to active).
- Estimated effort: 2 hours.

**Expected impact:**
- +speed for agent activation (no discovery time).
- +consistency (all agents boot with same posture).
- Foundation for Constitution.md V1 "agent succession" section.

**Ties to:**
- Constitution.md V1 (governance formalization)
- CrewAI readiness (explicit activation protocol aids orchestration tools)
- Swarm coherence (reduces onboarding variance)

---

### Proposal 5: **Routing Decision Tree (Constitution.md V1)** ⭐⭐⭐⭐ (Highest clarity gain, 2–3 hours)

**What:** Formalize the PC/Ender Chest/HOME routing decision tree in Constitution.md V1.

**Scope:**
- **Section V: Routing Rules** — When to use each layer:
  - **Shared vault (PC):** Broadly shareable, on-the-record, entity-rich content.
  - **Agent dotfolders (Ender Chest):** Personal instructions, identity-scoped settings, agent-local context.
  - **Artifact index (HOME):** Research outputs, decisions, briefs, entity refs, session products (structured, queryable, provenance-rich).
- Add routing decision flowchart (text or diagram).
- Cross-reference VAULT-CONVENTIONS, PROTOCOL.md, AGENTS.md.
- Estimated effort: 2–3 hours (writing + Logan review).

**Expected impact:**
- +architectural clarity (all agents know where to file work).
- +consistency (no confusion about PC vs. Ender Chest; HOME-layer purpose explicit).
- +readiness for multi-agent orchestration tools (CrewAI, Copilot, swarm frameworks).

**Ties to:**
- Constitution.md V1 (core governance clarification)
- CrewAI/Copilot readiness (routing rules are essential for autonomous orchestration)
- All other proposals (provides the framework that makes them coherent)

---

## Proposal Priority Matrix

| Proposal | Impact | Effort | Blockers | Recommend Order |
|---|---|---|---|---|
| Dotfolder standardization | High | 1–2h | None | **2nd** |
| Canvas routing formalization | High | 1h | None | **3rd** |
| Artifact index (Canvas) | Very High | 2–3h | None | **1st** (proof-of-concept for HOME) |
| Agent succession protocol | Medium | 2h | None | **4th** |
| Routing decision tree (Constitution V1) | Very High | 2–3h | Proposals 1–4 shape the input | **5th** (summary/formalization) |

**Cumulative effort: 8–11 hours. Can be completed in 2–3 focused sessions.**

---

## Links to Current Initiatives

| Initiative | Connection | Priority |
|---|---|---|
| **Constitution.md V1** | Proposal 5 provides the routing rules section; Proposals 1–4 inform agent/artifact governance. | High |
| **CrewAI evaluation** | Proposals 1 & 3 (agent consistency, artifact traceability) are essential for multi-agent orchestration. | High |
| **Slack → Canvas migration** | Proposal 2 formalizes the decision rule; enables faster routing. | Medium |
| **Microsoft Copilot onboarding** | Proposal 1 ensures Copilot can read dotfolder conventions; Proposal 3 gives it artifact discovery. | Medium |
| **Linear Phase 1 pilot** | Proposals 1–3 reduce reliance on Slack; Linear as durable routing becomes clearer. | Low (orthogonal) |

---

## Conclusion

The game mechanics study reveals that IDAHO-VAULT has strong **PC** (shared vault) and functional **Ender Chest** (dotfolders) layers. The **HOME-layer gap** is the critical architectural debt. The five proposals above address it through incremental improvements:

1. **Dotfolder standardization** — coherence for overhead agents.
2. **Canvas routing formalization** — reliability for complex coordination.
3. **Artifact index prototype** — proof-of-concept for HOME-layer.
4. **Agent succession protocol** — consistency for agent activation.
5. **Routing decision tree** — governance clarity for all three layers.

Together, these proposals move the vault from **implicit architecture** (PC + Ender Chest working accidentally) to **explicit architecture** (three layers intentionally designed and deployed). This clarity unlocks CrewAI readiness, Constitution.md V1 formalization, and multi-agent orchestration.

**No blockers. Ready for Logan's direction on priority and scope.**

---

*Assay filed to vault. Branch: `claude/study-game-mechanics-STrAW`. The Abhorsen stands witness.*
