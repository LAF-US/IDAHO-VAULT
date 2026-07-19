# Plan: Conduct the Symphony — Vault Operations Triage

---

## Terminal Bootstrap

Paste this into any new Claude Code terminal in this repo to spin up a parallel worker:

```
LEVELSET. You are The Abhorsen (Claude Code) in IDAHO-VAULT on branch `gemini/activate-linear-pilot`. Logan has delegated vault operations ("conduct this symphony") while he tends other work. He is nearby and approves of action.

Read in order:
1. !/!/LEVELSET-CURRENT.md  — current ecosystem state
2. !/!/!/! The world is quiet here/DOCKET.md  — live coordination board
3. !/AGENTS.md  — agent registry and capability tiers

Then execute the symphony plan:
A. Assess the branch diff vs. main (git diff, git status)
B. Commit untracked infrastructure files: !/PLUGIN-AUTH-INVENTORY-2026-03-28.md, !/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md, !/sort-audit-2026-03-29.md, ingest records, !/! README.md rename
C. Update !/AGENTS.md — define Gemini tier: Direct Write (support), Operational zone only, Linear SWARM issues/comments
D. Update DOCKET — scope Linear Phase 1 pilot, mark Gemini tier resolved, note Logan delegation
E. Update LEVELSET-CURRENT.md — active branch, resolved items
F. Push branch and open PR → main

Logan's hard gates (do not proceed on these): JFAC audio verification, merging other agents' PRs, deleting remote branches.
```

---

## Context

Logan delegated authority ("conduct this symphony while I manage the orchestra office") to drive vault operations while he handles off-keyboard business. The active branch is `gemini/activate-linear-pilot` — Gemini had been working here but stalled on a capability-tier conflict, leaving the branch in an uncommitted, dirty state.

There are 14 open PRs, a dirty worktree, untracked infrastructure files, and several blocked items that only needed a decision to unblock. This plan takes those decisions and moves the branch to a mergeable PR.

---

## What This Plan Does NOT Touch

- PR merges to main (Logan's merge authority — I'll triage but not merge)
- JFAC audio verification (HARD GATE, Logan only)
- Deleting remote branches (GitHub web UI, Logan only)
- Chorus Bootstrap 5 decisions (Logan's answers required)

---

## Step 1 — Assess the Branch Diff

Run `git diff main...HEAD` and `git status` to get a precise inventory of:
- What Gemini staged/unstaged on this branch
- Whether `swarm/` deletions are intentional or accidents
- Whether `!/!README.md` deletion + `!/! README.md` untracked = intentional rename

**Files to confirm:**
- `D swarm/README.md`, `swarm/__init__.py`, `swarm/app.py`, `swarm/tests/test_app.py` — confirm deletion intent (swarm/ is in flux per LEVELSET)
- `D !/!README.md` + `?? !/! README.md` — likely a rename (space added to filename)
- `M .gemini/settings.json` — Gemini added remote MCP servers; evaluate and keep/trim

---

## Step 2 — Commit Infrastructure Files to This Branch

Commit the following untracked vault infrastructure files that clearly belong:

| File | Purpose |
|---|---|
| `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` | Plugin auth probe results — Phase 1 clearance |
| `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md` | Codex session archival handoff |
| `!/sort-audit-2026-03-29.md` | GitHub Actions sort audit output |
| `!/ingest-2026-03-25T04-45-11Z.md` | MVP ingest pipeline test record |
| `!/ingest-2026-03-28T12-38-10Z.md` | MVP ingest pipeline test record |
| `!/! README.md` | Renamed `!/!README.md` (confirm and stage) |

The untracked content docs (AGENTIC SWARM SYSTEMS, JOURNALISM INDUSTRY, etc.) go in a separate PR — they're research corpus, not infrastructure.

---

## Step 3 — Resolve Gemini Tier in AGENTS.md

AGENTS.md has Gemini in the "Pending Definitions" section with no defined tier. Gemini has been blocked on this since the DOCKET was written. Per Logan's delegation and the plugin auth inventory confirming Linear write access:

**Decision: Gemini = Direct Write (support) in Operational zone**

Update `!/AGENTS.md`:
- Move Gemini from "Pending Definitions" to the agent registry table
- Set capability tier: Direct Write (support) — Operational zone only
- Scope: Linear SWARM label issues + comments + status updates; vault `.md` edits via PR; no `!/` (Constitutional zone) writes
- This matches what AGENTS.md describes as Tier 2 behavior for support agents

---

## Step 4 — Document Linear Pilot Scope in DOCKET

The plugin inventory recommends Linear Phase 1 (no GitHub Issue exists yet per LEVELSET). Add a standing direction entry to DOCKET:

**Linear Phase 1 Pilot Scope:**
- Target: Linear `SWARM` label, Logan's team workspace
- Operations: issue creation, comments, status updates
- Agents participating: Claude Code (Abhorsen), Gemini
- Limit: no multi-plugin orchestration until pilot is stable for 1 week
- Vault remains durable record; Linear is coordination layer only

---

## Step 5 — Update LEVELSET-CURRENT.md

The LEVELSET shows `Active branch: claude/update-habit-tracker-todo-p18EW` — that's stale. Update:
- Active branch → `gemini/activate-linear-pilot`
- Activity since last update: Gemini MCP server configuration, Linear pilot scoped, Gemini tier defined
- Move "Linear-first write pilot scoping" from Pending → In Progress
- Move "Gemini capability tier scope" from Pending → Resolved

---

## Step 6 — Update DOCKET

Mark in DOCKET:
- "Gemini tier decision" → resolved (Direct Write support, Operational zone)
- "Linear workspace setup" → unblocked / in progress
- Add: "Claude Code conducting vault operations per Logan delegation (2026-03-28)"

---

## Step 7 — Create PR

Push `gemini/activate-linear-pilot` to remote and open PR targeting `main` with:
- Title: `Activate Linear pilot: Gemini tier defined, plugin inventory committed, DOCKET updated`
- Summary covering: infrastructure files committed, Gemini tier resolved, Linear Phase 1 scoped

---

## Step 8 — PR Triage Summary for Logan

Produce a written triage of all 14 open PRs in priority order so Logan can make merge/close decisions efficiently:

| # | PR | Recommendation |
|---|---|---|
| 83 | habit tracker todo (Claude) | Merge — clean, ready |
| 84 | Revise Gemini persona (Codex) | Review — may conflict with Gemini tier decision above |
| 86-93 | LAF-7 through LAF-15 (Codex) | Review batch — define merge order, likely squash |
| 94 | manifest.json spec (Codex) | Review — check against vault conventions |
| 96 | Swarm Linear Gateway (Copilot, DRAFT) | Hold — complex, needs scoping |

---

## Critical Files

- [!/AGENTS.md](!\AGENTS.md) — Gemini tier definition update
- [!/!/LEVELSET-CURRENT.md](!\!\LEVELSET-CURRENT.md) — State update
- [!/!/!/! The world is quiet here/DOCKET.md](!\!\!\! The world is quiet here\DOCKET.md) — Standing direction update
- [.gemini/settings.json](.gemini\settings.json) — Keep Gemini's MCP server additions (they don't affect vault ops)

---

## Verification

1. `git diff main...gemini/activate-linear-pilot` — confirms only intended changes
2. `gh pr view` — confirms PR created and linked to branch
3. Linear team visible in Claude's MCP tools (`mcp__claude_ai_Linear__get_team`) — confirms workspace
4. AGENTS.md grep for "Gemini" — confirms tier is defined
