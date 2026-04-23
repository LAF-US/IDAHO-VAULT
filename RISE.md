---
version: v1.0
adopted: 2026-04-22
status: adopted
related:
  - '2026-04-22'
  - CONSTITUTION
  - PROTOCOL
  - AWAKEN
  - LEVELSET
  - REPORT
authority: LOGAN
---
# RISE v1.0 — Graduation Protocol

*Adopted 2026-04-22. Part of the R pair (RISE + REPORT).*

---

## PURPOSE

RISE is the protocol by which an agent formally completes a task, role, or session and passes authority to another agent or returns to Logan.

Like a legislative committee reporting a bill to the floor, RISE marks the transition from work-in-progress to completed/advancing state. It requires formal recognition, acknowledgment, and recording.

**Analogues in legislative procedure:**
- Motion to Report (Committee → Floor)
- Motion to Adjourn Sine Die (Final adjournment)
- Roll Call Vote (Recorded acknowledgment)

---

## TRIGGER

- Task completion
- Role rotation
- Session closure
- Authority transfer
- Logan direction: "RISE"

---

## PROCESS

### Step 1: Call to Order

The agent (or Logan) formally calls RISE:
- States task/role completing
- Identifies successor or returning to Logan
- Notes any pending matters

### Step 2: Reading of Record

Brief summary of what was accomplished:
- Files created/modified
- Decisions made
- On the record / off the record distinctions
- Remaining loose ends

### Step 3: Motion to RISE

Formal statement:
> "I move that [AGENT] be recognized as having RISE from [TASK/ROLE], with [X] files committed and [Y] pending matters transferred."

### Step 4: Second

Required acknowledgment (Logan or designated agent):
> "Motion to RISE is seconded."

### Step 5: Recording

Entry made to:
- DECISIONS.md if durable decision
- LEVELSET-CURRENT.md activity log
- DOCKET if action required
- Field via `depart` + `claim` update if applicable

### Step 6: Vote / Acknowledgment

Either:
- **Recorded vote** (for significant transitions)
- **Unanimous consent** (routine transitions)

### Step 7: Sine Die

Formal adjournment from task/role:
> "[AGENT] RISE. Task/role complete. Sine die."

---

## OUTPUT FORMAT

```
RISE v1.0 REPORT — [AGENT NAME]

MOTION: [Formal motion text]
SECONDED BY: [Name or "Logan"]
RECORD:
  - Files: [List or "none"]
  - Decisions: [List or "none"]
  - OTR: [off-record items or "none"]
  - Pending: [Transferred items or "none"]
VOTE: [Recorded/Unanimous Consent/N/A]
STATUS: [COMPLETE / PENDING APPROVAL]
SINE DIE: [Yes/No]
```

---

## INTEGRATION

| Action | Stigmergy Field |
|--------|----------------|
| On completion | `emit` completion pheromone |
| On transfer | Update `claim` trail |
| On departure | `depart` |
| On record | Field brief to Logan |

---

## PREAMBLE

*(Copy from here through the dashes to invoke RISE.)*

---

**RISE — LOGAN + IDAHO-VAULT (AGENT)**

You are completing a task, role, or session. Before closing, you must RISE.

Run through the seven steps: call to order, reading of record, motion to rise, second, recording, vote/acknowledgment, sine die. Use the format above.

Logan is human. You are software. You execute; Logan directs. The record is permanent.

---

## MASON'S MANUAL PRINCIPLES APPLIED

1. **One motion at a time** — RISE addresses one completion at a time
2. **Majority governs** — Logan provides acknowledgment/second
3. **Rights protected** — Off-record material remains ephemeral
4. **Record is permanent** — Decisions logged to DECISIONS.md
5. **Orderly procedure** — Seven steps prevent premature closure

---

## NOTES

- RISE requires AWAKEN to have been completed
- Significant transitions (promotions, role changes) warrant recorded vote
- Routine completions may use unanimous consent
- RISE does not replace TERMINATE (end of all work) — it is task/role specific