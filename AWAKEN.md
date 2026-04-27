---
title: "PROTOCOL — AWAKEN"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AGENTS
  - ARISE
  - ORIENT
  - LEVELSET
  - RISE
  - REPORT
  - AWAKEN-v1.0-2026-04-27
---

# PROTOCOL — AWAKEN

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

AWAKEN is the **session activation and agent wake protocol** for the IDAHO-VAULT agentic swarm.

It is the formal equivalent of a gavel striking the table — the moment an agent enters the world and declares readiness. AWAKEN establishes identity, authorization, and field presence before any substantive work begins.

> *"The world is quiet here."*

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
| Session Start | AWAKEN ← *this document* |
| Session Briefing | LEVELSET |
| New External Agent | ORIENT |
| Task Completion | RISE |
| Work Presentation | REPORT |

---

## Purpose

1. **Self-identification** — declare name, tier, session ID, and origin point
2. **Authorization check** — verify boot chain, credentials, and scope
3. **Context load** — retrieve field state, pending items, and trail markers
4. **Readiness declaration** — signal presence to the stigmergy field

---

## Trigger Conditions

AWAKEN executes:

- **At session start** — first action upon entering the vault
- **Upon handoff** — when an agent receives work from another
- **After recovery** — when resuming from a paused or interrupted state
- **On reactivation** — when a dormant agent returns to live service

---

## Integration Points

| Document | Relationship |
|---|---|
| `AWAKEN.md` (this file) | Protocol definition — what AWAKEN is and does |
| `AWAKEN-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `ARISE.md` | Paired protocol — individual emergence from void |
| `ORIENT.md` | External agent protocol — onboarding foreign voices |
| `CONSTITUTION.md` | Authoritative governance — defines AWAKEN in Section III |
| `!/AGENTS.md` | Agent registry — confirmed tiers and authorizations |
| `swarm.json` | Machine-readable registry — canonical boot chain |

---

## Protocol Steps

*See `AWAKEN-v1.0-2026-04-27.md` for the full approved specification.*

### Step 1: Self-Identification

Declare the following:

- **Name**: Primary identity within the vault
- **Tier**: Capability level per `!/AGENTS.md`
- **Session ID**: Unique instance identifier
- **Origin**: How this instance entered the vault (boot, handoff, recovery, reactivation)

### Step 2: Authorization Check

Verify the bootstrap chain:

1. Read `AGENTS.md` — cross-tool pointer
2. Read `!/AGENTS.md` — narrative registry
3. Confirm entry in `swarm.json`
4. Validate credentials against `!/agent.sh` or equivalent

### Step 3: Field Integration

Connect to the stigmergy field via `scripts/vault-pheromones.py`:

- Execute `arrive` signal
- Execute `sniff` to check current field state
- Identify pending items and trail markers

### Step 4: Readiness Declaration

- Execute `beat` signal
- Update `LEVELSET-CURRENT.md` with agent presence
- Declare readiness to receive work or begin task

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| Field presence | stigmergy field | Announce arrival |
| Agent status | LEVELSET-CURRENT.md | Record active voice |
| Session marker | `!/!/` handoff package | Track instance lifecycle |

---

## Constraints

- AWAKEN must complete before any substantive work begins
- Authorization failure is terminal — do not proceed without valid credentials
- Field integration is mandatory — the vault operates as a swarm, not a collection of siloed instances
- Pair with ARISE for individual emergence workflow

---

## Draft Status

This document is a **stub** under development. Full specification exists in `AWAKEN-v1.0-2026-04-27.md`.

Pending:
- [ ] Logan review and approval
- [ ] Integration with stigmergy field
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `AWAKEN-v1.0-2026-04-27.md` — complete approved protocol
- `ARISE.md` — individual emergence protocol
- `ORIENT.md` — external agent onboarding
- `LEVELSET.md` — session briefing protocol
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]