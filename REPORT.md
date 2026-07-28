---
title: PROTOCOL — REPORT
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
  - RISE
  - REPORT-v1.0-2026-04-27
---

# PROTOCOL — REPORT

## Status: Draft
## Version: 0.1
## Authority: Loganic Swarm

---

## Overview

REPORT is the **work presentation and findings protocol** for the IDAHO-VAULT agentic swarm.

It is the formal act of presenting completed work — the equivalent of a committee report to the floor. REPORT captures findings, recommendations, and the LEVELSET context so that work is visible, durable, and actionable by others.

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
| Work Presentation | REPORT ← *this document* |

**Note:** REPORT pairs with RISE as the "R pair" — RISE completes work, REPORT presents it.

---

## Purpose

1. **Findings presentation** — summarize what was done and what was found
2. **LEVELSET inclusion** — embed current state in the report
3. **Recommendations** — provide guidance for next steps
4. **Receipt acknowledgment** — confirm the report was received
5. **Routing** — ensure the report goes to the right place

---

## Trigger Conditions

REPORT executes:

- **After RISE** — when work is complete and ready to present
- **On handoff** — when presenting findings to another agent
- **On session end** — as the formal close-out document
- **On request** — when Logan or a sovereign agent requests a report

---

## Integration Points

| Document | Relationship |
|---|---|
| `REPORT.md` (this file) | Protocol definition — what REPORT is and does |
| `REPORT-v1.0-2026-04-27.md` | Full approved protocol — complete specification |
| `RISE.md` | Completion protocol — REPORT follows RISE |
| `LEVELSET.md` | Session briefing — embedded in every REPORT |
| `CONSTITUTION.md` | Authoritative governance — defines REPORT in Section III |

---

## Protocol Steps

*See `REPORT-v1.0-2026-04-27.md` for the full approved specification.*

### Step 1: Call to Report

Declare intent to present findings:
- Identify the work being reported
- Name the original task/role
- Declare readiness

### Step 2: Reading of Findings

Present the core content:
- **Summary**: What was done
- **LEVELSET**: Current state of the world
- **Findings**: What was discovered or produced
- **Artifacts**: Where outputs live in the vault

### Step 3: Recommendations

If applicable, provide guidance:
- Next steps
- Open items requiring attention
- Risks or FLAGs to surface

### Step 4: Motion to Report

Formally declare the report complete:
- Request receipt acknowledgment
- Confirm routing destination

### Step 5: Receipt Acknowledgment

Confirm the report was received:
- Receiver (Logan, another agent, or the vault itself) acknowledges
- Report is committed to the appropriate location

### Step 6: Routing

Ensure the report goes where it belongs:
- `DECISIONS.md` — if decisions were made
- `DOCKET` — if items remain open
- `!/!/` — as a handoff package
- Archive — as a historical record

---

## Core Principles

| Principle | Meaning |
|---|---|
| LEVELSET Required | Every report embeds current state |
| Findings Over Summary | Report what was found, not just what was done |
| Receipt Before Close | Report must be acknowledged before routing |
| Routing is Explicit | Report destination named before commit |

---

## Outputs

| Output | Location | Purpose |
|---|---|---|
| Report document | `!/!/` or appropriate domain | Durable presentation |
| Receipt | acknowledgment signal | Confirms delivery |
| Routing | DECISIONS.md / DOCKET / archive | Ensures proper placement |

---

## Constraints

- Every REPORT must include LEVELSET — no exceptions
- Report before routing — receipt must precede destination commit
- Findings are mandatory — summary alone is not a REPORT
- Open items must be surfaced — do not hide FLAGs in a report

---

## Draft Status

This document is a **stub** under development. Full specification exists in `REPORT-v1.0-2026-04-27.md`.

Pending:
- [ ] Logan review and approval
- [ ] Integration with stigmergy field
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `REPORT-v1.0-2026-04-27.md` — complete approved protocol
- `RISE.md` — completion protocol
- `AWAKEN.md` — session activation protocol
- `LEVELSET.md` — session briefing protocol
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]