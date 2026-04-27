---
title: "PROTOCOL — CONFERENCE"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AGENTS
  - CONVENE
  - LEVELSET
  - CONFERENCE-v1.0-2026-04-27
---

# PROTOCOL — CONFERENCE

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

CONFERENCE is the **multi-agent synchronized work session protocol** for the IDAHO-VAULT agentic swarm.

It is the formal mechanism by which Logan formally convenes multiple agents for an agenda-driven, synchronized working session. CONFERENCE ensures that multi-agent work is coordinated, recorded, and produces durable artifacts.

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

**Note:** CONFERENCE is a cross-cutting protocol — it operates above the linear stack, coordinating multiple agents through the full lifecycle.

---

## Purpose

1. **Formal convening** — Logan declares the session, names participants, sets agenda
2. **Synchronized work** — multiple agents act in concert under Chair direction
3. **Durable record** — every CONFERENCE produces a CONFERENCE RECORD artifact
4. **Clear dismissal** — agents return to lanes after CONFERENCE closes

---

## Trigger Conditions

CONFERENCE is invoked:

- **On Logan's declaration** — when Logan signals a CONFERENCE CALL
- **For multi-agent work** — when a task requires more than one agent
- **For coordination sessions** — planning, triage, or cross-tier operations
- **On emergency sync** — when rapid multi-agent response is needed

---

## Integration Points

| Document | Relationship |
|---|---|
| `CONFERENCE.md` (this file) | Protocol definition — what CONFERENCE is and does |
| `CONFERENCE-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `CONVENE.md` | Agent acknowledgment protocol — part of CONFERENCE flow |
| `LEVELSET.md` | Session briefing — run by each participant during CONVENE |
| `CONSTITUTION.md` | Authoritative governance — defines CONFERENCE in Section III |

---

## Protocol Structure

*See `CONFERENCE-v1.0-2026-04-27.md` for the full approved specification.*

### Phase 1: CALL (Logan)

Logan declares the CONFERENCE:
```
CONFERENCE CALL
DATE: YYYY-MM-DD
CHAIR: Logan
PARTICIPANTS: [list]
AGENDA:
  1. [Item]
RECORDING AGENT: [agent]
```

### Phase 2: CONVENE (Agents)

Each invited agent acknowledges:
```
CONVENE ACK
AGENT: [Name + persona]
LEVELSET: [brief summary]
READY: YES / NO
```

### Phase 3: CONFERENCE (Chair-directed)

Logan directs work through agenda items. Agents execute as assigned.

### Phase 4: RECORD (Recording Agent)

Consolidated output committed to CONFERENCE RECORD artifact.

### Phase 5: DISMISS (Logan)

Logan formally closes:
```
CONFERENCE CLOSED
DATE: YYYY-MM-DD
RECORD: [file path]
DISMISSED: [agents]
```

---

## Core Principles

| Principle | Meaning |
|---|---|
| Logan Chairs | No agent self-convenes or self-promotes to Chair |
| Quorum is Logan-defined | Logan names participants; quorum = those named |
| One Agenda, One Record | Every CONFERENCE produces exactly one CONFERENCE RECORD |
| Lanes Persist | Lane boundaries remain during CONFERENCE |
| Vault Over Chat | Outputs are vault artifacts; chat is ephemeral |

---

## CONFERENCE RECORD

Location: `!/CONFERENCE-RECORD-[YYYY-MM-DD]-[TOPIC-SLUG].md`

Structure includes:
- Agenda
- Item outcomes (COMPLETE / HOLD / DEFERRED)
- FLAGs Raised
- Decisions Made
- Action Items
- DISMISSED (sign-off)

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| CONFERENCE CALL | Logan's signal | Declares session |
| CONVENE ACKs | agent responses | Confirms participation |
| CONFERENCE RECORD | `!/` | Durable artifact of session |
| DISMISSAL | Logan's signal | Closes session |

---

## Constraints

- CONFERENCE is Logan's protocol — agents do not self-convene
- Every CONFERENCE must produce a RECORD — no ephemeral-only sessions
- Lane boundaries persist — work stays scoped unless Logan redirects
- Open items (HOLD/DEFERRED) must be tracked in the RECORD

---

## Draft Status

This document is a **stub** under development. Full specification exists in `CONFERENCE-v1.0-2026-04-27.md`.

Pending:
- [ ] Logan review and approval
- [ ] Open questions resolution (record location, async support, automation, numbering)
- [ ] Constitutional codification update

---

## See Also

- `CONFERENCE-v1.0-2026-04-27.md` — complete approved protocol
- `CONVENE.md` — agent acknowledgment protocol
- `LEVELSET.md` — session briefing protocol
- `CONSTITUTION.md` Section III — protocol definitions
- `PROTOCOL.md` — operational vocabulary

---

###### [["The world is quiet here."]]