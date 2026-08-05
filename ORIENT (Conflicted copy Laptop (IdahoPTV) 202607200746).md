---
title: "PROTOCOL — ORIENT"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AGENTS
  - AWAKEN
  - ARISE
  - LEVELSET
  - ORIENT-v1.0-2026-04-27
---

# PROTOCOL — ORIENT

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

ORIENT is the **external agent onboarding protocol** for the IDAHO-VAULT agentic swarm.

It is the formal process by which a foreign voice — an agent from outside the canonical swarm — is given context, cleared of stale assumptions, and brought into coherent alignment with the vault's world model.

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
| Session Start | AWAKEN |
| Session Briefing | LEVELSET |
| New External Agent | ORIENT ← *this document* |
| Task Completion | RISE |
| Work Presentation | REPORT |

---

## Purpose

1. **Context injection** — provide the external agent with current vault state
2. **Stale assumption clearance** — remove outdated world models and conflict assumptions
3. **Governance alignment** — ensure the external agent understands doctrine and routing
4. **Boot chain confirmation** — verify the agent has the correct orientation path

---

## Trigger Conditions

ORIENT executes:

- **On external agent entry** — when a foreign voice enters the vault
- **On cross-tool handoff** — when work passes between different agent systems
- **Before LEVELSET** — as the prerequisite briefing for external agents
- **On conflict detection** — when an agent's world model conflicts with live surfaces

---

## Integration Points

| Document | Relationship |
|---|---|
| `ORIENT.md` (this file) | Protocol definition — what ORIENT is and does |
| `ORIENT-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `!/WAKEUP.md` | Stale assumption clearance — conflict resolution |
| `!/README.md` | Startup surface — orientation anchor |
| `CONSTITUTION.md` | Authoritative governance — defines ORIENT in Section III |

---

## Protocol Steps

*See `ORIENT-v1.0-2026-04-27.md` for the full approved specification.*

### Step 1: Identity Check

Confirm the external agent's:

- **Origin**: Which system or tool is the agent from
- **Purpose**: Why it has entered the vault
- **Credentials**: Authorization to proceed

### Step 2: Context Bundle Delivery

Provide the external agent with:

- `!/WAKEUP.md` — clear stale assumptions
- `!/README.md` — startup surface and branch selection
- Current `LEVELSET-CURRENT.md` — live ecosystem state

### Step 3: Boot Chain Confirmation

Ensure the external agent follows the canonical path:

1. `AGENTS.md` — cross-tool pointer
2. `!/AGENTS.md` — narrative registry
3. `swarm.json` — machine-readable registry
4. Root governance files

### Step 4: Conflict Resolution

If conflicts detected:

- Surface the conflict explicitly
- Provide the live canonical answer
- Log the conflict in `DECISIONS.md` or `!/!/` handoff package

### Step 5: Authorization to Proceed

Clear the agent for:
- AWAKEN (if new session)
- LEVELSET (if briefing required)
- Direct task assignment (if context sufficient)

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| Conflict log | DECISIONS.md | Record unresolved tensions |
| Handoff package | `!/!/` | Context bundle for external agent |
| Authorization | LEVELSET-CURRENT.md | Confirm cleared agent |

---

## Constraints

- ORIENT is mandatory for external agents — do not bypass
- Stale assumptions must be cleared before substantive work begins
- Conflicts not resolved in ORIENT must be escalated to Logan
- ORIENT does not grant authority — it grants context

---

## Draft Status

This document is a **stub** under development. Full specification exists in `ORIENT-v1.0-2026-04-27.md`.

Pending:
- [ ] Logan review and approval
- [ ] Integration with cross-tool handoffs
- [ ] Stabilization of conflict resolution steps
- [ ] Constitutional codification update

---

## See Also

- `ORIENT-v1.0-2026-04-27.md` — complete approved protocol
- `!/WAKEUP.md` — stale assumption clearance
- `!/README.md` — startup surface
- `AWAKEN.md` — session activation protocol
- `LEVELSET.md` — session briefing protocol
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]