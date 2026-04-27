---
title: "PROTOCOL — LEVELSET"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AGENTS
  - LEVELSET-CURRENT
  - LEVELSET-2026-04-27
  - DECISIONS
  - REPORT
  - RISE
  - !/AGENTS.md
  - swarm.json
---

# PROTOCOL — LEVELSET

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

LEVELSET is the **session briefing and context-recording protocol** for the IDAHO-VAULT agentic swarm.

It serves as the moment of pause and orientation — the equivalent of gavel-down before committee work begins. LEVELSET captures the current state of the world so that subsequent actions have a durable anchor and future agents can orient without stale assumptions.

---

## Role in the Protocol Stack

```
AWAKEN ──────────────────────► RISE
   │                                │
   │                                │
   ▼                                ▼
ORIENT ◄──── LEVELSET ───────► REPORT
```

| Transition | Protocol |
|------------|----------|
| Session Start | AWAKEN |
| Session Briefing | LEVELSET ← *this document* |
| New External Agent | ORIENT |
| Task Completion | RISE |
| Work Presentation | REPORT |

---

## Purpose

1. **Capture ground truth** — current repository state, branch, working tree status
2. **Provide orientation** — what governance files are authoritative, what has changed
3. **Establish scope** — what the current session is meant to accomplish
4. **Record decisions** — flag any decisions made during the LEVELSET round
5. **Anchor handoffs** — ensure the next agent inherits a coherent world model

---

## Trigger Conditions

LEVELSET executes:

- **At session start** — before any substantive work begins
- **Before handoff** — when work is passed to another agent
- **Before REPORT** — as the briefing layer for work presentation
- **On demand** — when Logan or a sovereign agent requests a fresh snapshot
- **Periodically** — as a standing cadence for long-running sessions

---

## Integration Points

| Document | Relationship |
|---|---|
| `LEVELSET.md` (this file) | Protocol definition — what LEVELSET is and does |
| `LEVELSET-CURRENT.md` | Rolling live snapshot — current state of the ecosystem |
| `LEVELSET-2026-04-27.md` | Archived status reports — historical ground truths |
| `CONSTITUTION.md` | Authoritative governance — defines LEVELSET in Section III |
| `AGENTS.md` / `!/AGENTS.md` | Agent registry — confirms authorized voices |
| `swarm.json` | Machine-readable registry — canonical boot chain |
| `DECISIONS.md` | Decision log — durable confirmations |
| `!/!/` | Handoff artifacts — context packages from LEVELSET rounds |

---

## Protocol Steps

*See `PROTOCOL-SUITE-AWR.md` for integration with AWAKEN/RISE/REPORT lifecycle.*

### Step 0: Pre-flight

```
git branch --show-current
git status --short
```

Confirm local state before proceeding.

### Step 1: Confirm Registry Chain

Read in order:

1. `AGENTS.md` — cross-tool pointer
2. `!/AGENTS.md` — narrative registry
3. `swarm.json` — machine-readable registry
4. `!/agents.json` — generated bootstrap index

Resolve any split-doctrine before proceeding.

### Step 2: Load Governance Stack

Read authoritative orientation stack:

1. `!/README.md`
2. `CONSTITUTION.md`
3. `DECISIONS.md`
4. `LEVELSET.md` (this file)
5. `VAULT-CONVENTIONS.md`
6. `AGENT-PROTOCOL.md`

### Step 3: Confirm Infrastructure Status

Verify operational state of:

- `.claude/CLAUDE.md`
- `.gemini/GEMINI.md`
- `.codex/CODEX.md`
- `.github/copilot-instructions.md`
- Automation jobs (if applicable)

### Step 4: Generate LEVELSET Snapshot

Produce or update `LEVELSET-CURRENT.md`:

```
| Field | Value |
|---|---|
| Timestamp | [current datetime] |
| Branch | [git branch] |
| Working tree | [clean/mixed] |
| Coordination hub | [LAF-N reference] |
| Registry lane | [LAF-N reference] |
```

### Step 5: Record Decisions

If any decisions were made during orientation, commit them to `DECISIONS.md` or create a decision entry in the handoff package.

### Step 6: Archive Previous

If `LEVELSET-CURRENT.md` existed, archive it with a dated name (e.g., `LEVELSET-CURRENT-2026-04-27.md`) before updating.

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| LEVELSET-CURRENT.md | root | Rolling live snapshot |
| Decision entries | DECISIONS.md | Durable record of choices made |
| Handoff packages | `!/!/` | Context bundles for receiving agents |
| Archived snapshots | root (dated) | Historical ground truths |

---

## Constraints

- LEVELSET is a **recording and contextualizing device**, not a live dashboard
- Do not accumulate doctrine in `LEVELSET-CURRENT.md` — doctrine returns to canonical governance files
- The Heisenberg principle applies: the act of observing state changes state — acknowledge staleness
- Stale assumptions are the enemy; fresh snapshots are the cure

---

## Draft Status

This document is a **stub** under development. Adoption pending:

- [ ] Logan review and approval
- [ ] Integration with stigmergy field (`scripts/vault-pheromones.py`)
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `LEVELSET-CURRENT.md` — live snapshot
- `LEVELSET-2026-04-27.md` — archived status reports
- `PROTOCOL-SUITE-AWR.md` — AWAKEN/RISE/REPORT lifecycle
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]