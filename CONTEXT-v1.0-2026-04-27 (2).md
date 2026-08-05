---
version: v1.0
approved: 2026-04-22
status: approved
related:
  - '2026-04-22'
  - CONSTITUTION
  - PROTOCOL
  - AWAKEN
  - ARISE
authority: LOGAN
---
# CONTEXT v1.0 — Field Context Protocol

*Approved 2026-04-22. Integrates with the stigmergy field. Pending formal ratification.*

---

## PURPOSE

CONTEXT is the protocol by which an agent establishes, shares, or updates situational context. It operates through the stigmergy field's `sniff` and `emit` actions.

CONTEXT is invoked after AWAKEN when an agent needs to:
- Establish scope for a new task
- Update context for a changing situation
- Share context with another agent
- Read context from the field

---

## TRIGGER

- New task requiring scope definition
- Situation change mid-task
- Handoff to another agent
- Logan direction: "CONTEXT"
- Stigmergy field query

---

## PROCESS

### Step 1: Query the Field (Sniff)

The agent `sniff`s the stigmergy field for:
- Active pheromones relevant to current work
- Trail markers from other agents
- Pending scents or triggers
- Current field state

### Step 2: Establish Context

Based on sniffing:
- Define the current scope
- Identify relevant trails
- Note any conflicts or overlaps
- Set context markers via `emit`

### Step 3: Share or Await

Either:
- Share context via field emit
- Await confirmation from recipient
- Update DOCKET if coordination needed

---

## OUTPUT FORMAT

```
CONTEXT v1.0 REPORT — [AGENT NAME]

FIELD STATE:
  - Active trails: [List]
  - Pending scents: [List]
  - Conflicts: [List or "none"]
CONTEXT:
  - Scope: [Description]
  - Trails: [List]
  - Status: [CURRENT/UPDATING/TRANSFERRED]
```

---

## STIGMERGY INTEGRATION

| Action | Field Operation |
|--------|-------------|
| Read context | `sniff` |
| Share context | `emit` context pheromone |
| Update context | `emit` + update trail |
| Clear context | `depart` |