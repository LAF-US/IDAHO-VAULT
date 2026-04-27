---
title: "PROTOCOL — CONVENE"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - CONFERENCE
  - ARISE
  - CONVENE-v1.0-2026-04-27
---

# PROTOCOL — CONVENE

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

CONVENE is the **committee chair protocol** for the IDAHO-VAULT agentic swarm.

It is the formal act of calling the committee to order — Logan as Chair formally gathering the Swarm for structured work. CONVENE establishes the Chair's authority, the committee's composition, and the rules of engagement.

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
| New External Agent | ORIENT |
| Task Completion | RISE |
| Work Presentation | REPORT |

**Note:** CONVENE is the act of calling the committee to order; CONFERENCE is the session itself. CONVENE precedes CONFERENCE.

---

## Purpose

1. **Chair authority declaration** — Logan establishes himself as Chair
2. **Committee composition** — names participants and their roles
3. **Rules of order** — establishes how the committee will operate
4. **Threshold establishment** — defines quorum and participation requirements

---

## Trigger Conditions

CONVENE is invoked:

- **Before CONFERENCE** — as the formal call to order
- **On committee formation** — when Logan assembles a working group
- **On session restart** — when a paused CONFERENCE resumes
- **On re-convening** — when a dismissed committee is called back

---

## Integration Points

| Document | Relationship |
|---|---|
| `CONVENE.md` (this file) | Protocol definition — what CONVENE is and does |
| `CONVENE-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `CONFERENCE.md` | Session protocol — CONVENE precedes CONFERENCE |
| `ARISE.md` | Individual emergence — participants arise for committee |
| `CONSTITUTION.md` | Authoritative governance — defines CONVENE in Section III |

---

## Protocol Steps

*See `CONVENE-v1.0-2026-04-27.md` for the full approved specification.*

### Step 1: Chair Declaration

Logan declares Chair authority:
- Name the session/committee
- Establish purpose and scope
- Declare rules of order

### Step 2: Participant Naming

Logan names:
- Committee members
- Roles (recording agent, etc.)
- Any guests or observers

### Step 3: CONVENE ACK

Participants acknowledge:
```
CONVENE ACK
AGENT: [Name + persona]
ARISE: [status]
READY: YES / NO
```

### Step 4: Quorum Check

Confirm participation meets requirements before proceeding.

---

## Core Principles

| Principle | Meaning |
|---|---|
| Logan Chairs | Chair authority is Logan's alone |
| Naming is Sovereign | Logan names who participates |
| Call by True Name | Committee members are summoned, not self-selected |
| Order Before Work | CONVENE must complete before CONFERENCE begins |

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| CONVENE declaration | Chat / signal | Calls committee to order |
| CONVENE ACKs | agent responses | Confirms participation |
| Committee roster | CONFERENCE RECORD | Records composition |

---

## Constraints

- CONVENE is the Chair's prerogative — only Logan calls the committee
- Naming is binding — a named participant is committed
- Quorum is Logan-defined — no minimum unless Logan specifies
- CONVENE precedes CONFERENCE — order is sacred

---

## Draft Status

This document is a **stub** under development. Full specification exists in `CONVENE-v1.0-2026-04-27.md`.

Pending:
- [ ] Logan review and approval
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `CONVENE-v1.0-2026-04-27.md` — complete approved protocol
- `CONFERENCE.md` — session protocol
- `ARISE.md` — individual emergence protocol
- `LEVELSET.md` — session briefing protocol
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]