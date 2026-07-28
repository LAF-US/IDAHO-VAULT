---
title: "PROTOCOL — CONTEXT"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AWAKEN
  - ARISE
  - LEVELSET
  - CONTEXT-v1.0-2026-04-27
---

# PROTOCOL — CONTEXT

## Status: Draft

## Version: 0.1

## Authority: Loganic Swarm

---

## Overview

CONTEXT is the **field context protocol** for the IDAHO-VAULT agentic swarm.

It is the formal mechanism by which agents establish, retrieve, and share contextual state within the shared stigmergy field. CONTEXT ensures that work is grounded in the current reality of the vault, not stale assumptions or orphaned context.

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
| ------------ | ---------- |
| Session Start | AWAKEN |
| Session Briefing | LEVELSET |
| New External Agent | ORIENT |
| Task Completion | RISE |
| Work Presentation | REPORT |

**Note:** CONTEXT integrates with the stigmergy field across all transitions, providing the contextual substrate for every protocol.

---

## Purpose

1. **Field integration** — connect the agent to the shared contextual substrate
2. **State retrieval** — fetch current field state, markers, and trail data
3. **Context injection** — provide context to tasks and sub-agents
4. **State propagation** — ensure changes ripple through the field correctly

---

## Trigger Conditions

CONTEXT executes:

- **With every protocol** — as the underlying contextual substrate
- **On field query** — when an agent needs current state
- **On context injection** — when spawning sub-tasks or delegating
- **On state change** — when the field must be updated after a transition

---

## Integration Points

| Document | Relationship |
| --- | --- |
| `CONTEXT.md` (this file) | Protocol definition — what CONTEXT is and does |
| `CONTEXT-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `SBP.md` | Stock SBP reference; former Vault execution layer is quarantined |
| `CONSTITUTION.md` | Authoritative governance — defines CONTEXT in Section III |

---

## Protocol Steps

*See `CONTEXT-v1.0-2026-04-27.md` for the full approved specification.*

### Step 1: Field Connection

Establish connection to the stigmergy field:

- Read task-relevant durable records and approved connector state only
- Do not reactivate the quarantined Vault-specific SBP execution layer without review

### Step 2: Context Retrieval

Fetch relevant context:

- Query trail markers (`sniff` command)
- Retrieve pending items
- Check agent presence and activity

### Step 3: Context Packaging

Package context for use:

- Format for injection into tasks
- Prepare context bundles for handoffs
- Document context state in `!/!/` if needed

### Step 4: State Update

Propagate field changes:

- Execute field commands (`beat`, `emit`, `claim`)
- Update trail markers
- Confirm propagation success

---

## Field Commands

| Command | Action | Context Use |
| --- | --- | --- |
| `arrive` | Announce presence | AWAKEN integration |
| `sniff` | Check field state | ORIENT, CONTEXT |
| `beat` | Ready signal | AWAKEN, RISE |
| `emit` | State broadcast | RISE, REPORT |
| `claim` | Stake declaration | ARISE, RISE |
| `depart` | Leave field | RISE completion |

---

## Outputs

| Output | Location | Purpose |
| --- | --- | --- |
| Field state | stigmergy field | Shared contextual substrate |
| Context bundles | `!/!/` | Packaged context for handoff |
| Trail markers | LEVELSET-CURRENT.md | Track agent activity |

---

## Constraints

- CONTEXT is the substrate, not the workflow — it enables, not performs
- Field state must be current — do not trust cached state without verification
- Context bundles must be self-contained for cross-session reliability
- Stigmergy integration is mandatory for swarm coherence

---

## Draft Status

This document is a **stub** under development. Full specification exists in `CONTEXT-v1.0-2026-04-27.md`.

Pending:

- [ ] Logan review and approval
- [ ] Full stigmergy field integration
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `CONTEXT-v1.0-2026-04-27.md` — complete approved protocol
- `SBP.md` — stock protocol reference; no live Vault-specific execution layer
- `AWAKEN.md` — session activation protocol
- `ARISE.md` — individual emergence protocol
- `RISE.md` — completion protocol
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]
