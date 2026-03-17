# XKCD Protocol — DRAFT

**Version:** 0.1 (DRAFT — pending Logan's review)
**Date:** 2026-03-17
**Status:** PROPOSED

---

## Purpose

LEVELSET asks "where are we?" SIGNAL says "something just happened." XKCD governs how conversations actually talk to each other — the mechanics of cross-conversation communication through Logan as router.

XKCD is the protocol for **eXchange, Knowledge, Coordination, and Dispatch** across the conversation swarm.

---

## Problem

Conversations cannot communicate directly. Logan is the sole bridge. But the bridge has no defined format. When Logan carries a message from JFAC to CODE AUTHORITY, there is no standard for:

- How the message is structured
- How receipt is confirmed
- How priority is conveyed
- How conversations request contact with each other
- How Logan broadcasts to all conversations at once

The PING/PONG exchange on 2026-03-16/17 (CODE AUTHORITY ↔ JFAC, CODE AUTHORITY ↔ Budget Tracker) worked, but it was ad hoc. XKCD formalizes it.

---

## Message Types

### PING

A heartbeat check. "Are you there? What's your status?"

**When to use:** Logan is doing a round of touchbases, or one conversation needs to know another's current state before proceeding.

**Expected response:** PONG.

### PONG

Response to a PING. Status confirmation plus any relevant updates.

**When to use:** Always in response to a PING. Never unprompted.

**Contents:** Current status (active/holding/quiet), priority order, any pending items for the sender.

### RELAY

A directed message from one conversation to another, carried by Logan. Not a signal — a message with content that expects acknowledgment.

**When to use:** One conversation has information, a question, or a request for a specific other conversation, and it's more than a SIGNAL warrants.

**Expected response:** ACK.

### ACK

Acknowledgment of receipt. "Got it." May include a brief response or "noted, no action needed."

**When to use:** Always in response to a RELAY. Confirms the target conversation received and understood the message.

### BROADCAST

Logan sends the same message or instruction to all active conversations (or a specified subset).

**When to use:** Policy changes, protocol updates, vault-wide instructions, LEVELSET distribution. Logan-initiated only.

**Expected response:** ACK from each recipient.

---

## Message Format

```
XKCD: [TYPE]
FROM: [conversation name] — [tier]
TO: [target conversation, "ALL", or "LOGAN"]
DATE: [YYYY-MM-DD HH:MM MT]
RE: [subject — one line]

[Body. Keep it short. If it's longer than a paragraph, it should probably be a LEVELSET report instead.]
```

### PONG format (specific)

```
XKCD: PONG
FROM: [conversation name] — [tier]
TO: [whoever PINGed]
DATE: [YYYY-MM-DD HH:MM MT]
RE: PONG

STATUS: [ACTIVE / HOLDING / QUIET]
PRIORITY ORDER:
1. [top priority]
2. [second]
3. [third]
PENDING FOR SENDER: [anything relevant to the conversation that PINGed, or "None"]
```

---

## Rules

1. **Logan is always the router.** Conversations never communicate directly. Every XKCD message passes through Logan. Conversations can request communication, but Logan decides whether to carry the message.

2. **PINGs require PONGs.** If you are PINGed, you PONG. No exceptions. If a conversation cannot PONG (context compacted, no relevant state), it PONGs with `STATUS: UNKNOWN` and flags what it can't answer.

3. **RELAYs require ACKs.** If you receive a RELAY, you ACK. The ACK confirms receipt, not agreement or action.

4. **BROADCASTs are Logan-only.** No conversation can broadcast. Only Logan initiates BROADCAST messages. Conversations that need to reach "ALL" should emit a SIGNAL with `TO: ALL` instead — Logan decides whether to broadcast it.

5. **XKCD is lightweight.** If you need more than a paragraph, use LEVELSET. If you need to flag an event, use SIGNAL. XKCD is for coordination — short, structured, transactional.

6. **Don't PING without reason.** PINGs are not idle chatter. Every PING should have a purpose: pre-commit collision check, status verification before handoff, or Logan-initiated touchbase.

7. **Quiet mode is valid.** A PONG with `STATUS: QUIET` means the conversation is standing by, signal-only. It has no active work and will not initiate communication until PINGed or directed by Logan.

---

## Interaction with SIGNAL and LEVELSET

| Need | Use |
|---|---|
| Flag an event between checkpoints | SIGNAL |
| Periodic comprehensive status | LEVELSET |
| Direct message to another conversation | XKCD: RELAY |
| "Are you there?" | XKCD: PING/PONG |
| Policy announcement to all conversations | XKCD: BROADCAST |
| Report on signals received since last checkpoint | LEVELSET Section 2 or 5 |

**SIGNAL → XKCD escalation:** If a SIGNAL with `TO: [specific conversation]` needs more than a one-way flag, Logan may upgrade it to an XKCD: RELAY to ensure ACK and response.

**XKCD → LEVELSET capture:** Significant RELAY/PONG exchanges should be referenced in the next LEVELSET report for the permanent record.

---

## Handoff Protocol

When work transfers from one conversation to another:

1. **Source conversation** emits `XKCD: RELAY` to target, describing:
   - What work is being handed off
   - Current state of the work
   - Files touched
   - What the target needs to do next

2. **Logan routes** the RELAY to the target conversation.

3. **Target conversation** responds with `XKCD: ACK` confirming:
   - Receipt of handoff
   - Whether it has the context and access needed
   - Any BLOCK signals if it cannot proceed

4. **Source conversation** marks the work as handed off in its next LEVELSET report.

---

## Examples

### PING/PONG — Logan does a round of touchbases

```
XKCD: PING
FROM: LOGAN
TO: ALL
DATE: 2026-03-17 08:00 MT
RE: Morning status check
```

```
XKCD: PONG
FROM: STORY: JFAC Open Meetings — Tier 1
TO: LOGAN
DATE: 2026-03-17 08:05 MT
RE: PONG

STATUS: QUIET
PRIORITY ORDER:
1. Grow/Tanner contact + audio verification
2. Power Package delivery (Hightail failed — outstanding)
3. Open meetings timeline review
PENDING FOR SENDER: None
```

### RELAY — Passing information between conversations

```
XKCD: RELAY
FROM: PERMANENT: CODE AUTHORITY — Tier 1
TO: PERSISTENT: ADMINISTRATION
DATE: 2026-03-17 10:00 MT
RE: SIGNAL protocol committed — constitution needs update

SIGNAL.md is committed and merged. CLAUDE.md (repo root) updated.
Constitution reference at !ADMINISTRATION/Claude.md line 137-142
has the signaling section. ADMINISTRATION should verify it aligns
with constitutional intent.
```

```
XKCD: ACK
FROM: PERSISTENT: ADMINISTRATION — Tier 2
TO: PERMANENT: CODE AUTHORITY
DATE: 2026-03-17 10:15 MT
RE: ACK — SIGNAL protocol

Received. Will review constitutional alignment at next session.
No conflicts detected with current governance framework.
```

### Handoff — Transferring work

```
XKCD: RELAY
FROM: TASK: LEVELSET reports — Tier 3
TO: PERMANENT: CODE AUTHORITY — Tier 1
DATE: 2026-03-17 12:00 MT
RE: HANDOFF — LEVELSET synthesis

Synthesized reports from 4 conversations. Output is in my context
but I cannot commit (Tier 3, read-only). Summary:

- No collisions detected
- 2 ESCALATE signals pending (see LEVELSET Section 2)
- Draft synthesis ready for commit to !ADMINISTRATION/LEVELSET-v3.md

Requesting CODE AUTHORITY commit the synthesis. Full text follows.
```
