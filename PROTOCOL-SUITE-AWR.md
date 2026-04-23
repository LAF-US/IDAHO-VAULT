---
title: "Protocol Suite — AWAKEN, RISE, REPORT"
date created: 2026-04-22
authority: LOGAN
doc_class: protocol
status: draft
related:
  - AWAKEN
  - RISE
  - REPORT
  - ORIENT
  - LEVELSET
  - CONSTITUTION
  - PROTOCOL
  - scripts/vault-pheromones.py
---
# Protocol Suite — AWAKEN, RISE, REPORT

## Overview

Three protocols drafted for formal adoption, completing the Constitution.md Section III protocol stack:

| Protocol | Version | Source | Inspiration |
|----------|---------|--------|-------------|
| **AWAKEN v0.1** | draft | CONSTITUTION.md III | Session start requirements |
| **RISE v0.1** | draft | CONSTITUTION.md III | Legislative committee procedure, Mason's Manual |
| **REPORT v0.1** | draft | CONSTITUTION.md III | Committee reporting, Mason's Manual |

---

## Protocol Lifecycle

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

---

## AWAKEN — Session Activation

**What:** Agent wake and readiness protocol
**When:** Session start, handoff, recovery
**Output:** State declaration + field update

**Core steps:**
1. Self-identification (name, tier, session)
2. Authorization check (boot chain, credentials)
3. Context load (field, trails, pending)
4. Readiness declaration

**Mason's parallel:** Call to order, establishment of quorum

---

## RISE — Task Completion

**What:** Formal graduation from task/role
**When:** Task done, role rotation, authority transfer
**Output:** Motion, second, vote, sine die

**Core steps:**
1. Call to order
2. Reading of record
3. Motion to RISE
4. Second required
5. Recording (DECISIONS.md, field)
6. Vote (recorded or unanimous consent)
7. Sine die

**Mason's parallels:**
- Motion to Report (Committee → Floor)
- Motion to Adjourn Sine Die
- Recorded vote

**Key principle:** Task/role completion, not session end

---

## REPORT — Work Presentation

**What:** Formal findings + LEVELSET presentation
**When:** Deliverables ready, handoff, end of session
**Output:** Report document + receipt acknowledgment

**Core steps:**
1. Call to report
2. Reading of findings (Summary + LEVELSET + Findings)
3. Recommendations (if applicable)
4. Motion to report
5. Receipt acknowledgment
6. Routing (DECISIONS.md, DOCKET, archive)

**Mason's parallels:**
- Committee Report
- Testimony presentation
- Roll Call / Recording
- Dispatch to Standing Committee

**Key principle:** Includes mandatory LEVELSET; produces durable record

---

## Integration with Stigmergy Field

| Protocol | Field Action | Command |
|----------|-------------|---------|
| AWAKEN | Agent arrives | `arrive` |
| AWAKEN | Check context | `sniff` |
| AWAKEN | Ready signal | `beat` |
| RISE | Completion signal | `emit` |
| RISE | Claim update | `claim` |
| RISE | Departure | `depart` |
| REPORT | Report filed | `emit` |
| REPORT | Trail update | `claim` |

---

## Draft Files

- `AWAKEN-v0.1.md` — Agent wake protocol
- `RISE-v0.1.md` — Graduation/completion protocol  
- `REPORT-v0.1.md` — Reporting protocol (includes LEVELSET)

---

## Next Steps

1. Logan reviews drafts
2. Adoption decision per protocol
3. Update CONSTITUTION.md Section III
4. Implement stigmergy field integration
5. Stabilize remaining protocols (CONTEXT, CONFERENCE, CONVENE)