---
title: "XKCD Minimal Handoff"
date: 2026-05-17
status: active-minimal
authority: LOGAN
doc_class: protocol_implementation
related:
  - PROTOCOL-XKCD-DRAFT
  - VAULT-ZONES
  - "!-OPENCLAW-HERMES-MAC-WINDOWS-STABILITY-2026-05-17"
---

# XKCD Minimal Handoff - 2026-05-17

Logan approved a minimal implementation of [[PROTOCOL-XKCD-DRAFT]] for live Mac/Windows and cross-agent relay work.

This is not a full constitutional promotion of the draft. It is the smallest active operating rule needed to prevent false coordination between machines, sessions, and agents.

## Active Rule

No agent should assume another agent, machine, or chat session has received context unless Logan relays it or a durable vault note records it.

## Minimal Transfer Format

Use this block when passing live operational state between agents or machines:

```text
XKCD TRANSFER
FROM:
TO:
CLASS: SIGNAL | REQUEST | SYNC | PATCH | ECHO
TIME:
SUBJECT:
STATE:
ASK:
VERIFY:
```

## Class Meanings

- `SIGNAL`: one-way status update; no action required.
- `REQUEST`: asks another agent or machine to act.
- `SYNC`: aligns two active sessions or machines.
- `PATCH`: corrects stale or wrong state.
- `ECHO`: Logan-carried verbatim relay; durable only if written to a note.

## Current Use

For OpenClaw Mac/Windows work:

- Windows-to-Mac updates should name the tunnel state, node process state, OpenClaw version, node id, and whether token material stayed out of chat.
- Mac-to-Windows updates should name gateway health, node pairing state, command capabilities, invoke results, and any required restart action.
- Both sides should distinguish "TCP connected" from "paired, scoped, and command-capable."
- If an agent says "stable," it should include the verification used to prove that claim.

## Persistence Rule

- Ephemeral chat relay is acceptable during live troubleshooting.
- Any state needed after the session ends belongs in a dated status, handoff, or levelset note.
- Do not edit constitutional governance files only to capture transient coordination.

## Acknowledgement Rule

When receiving a transfer, the receiving agent should respond with:

```text
ACK:
PARSE:
NEXT:
```

This confirms receipt, states what was understood, and names the next action.

## Open Questions Deferred

- Whether to batch all XKCD traffic into a log.
- Whether to rename historical handoffs.
- Whether to promote the full draft into canonical governance.
- Whether to require self-identification in every commit message.

###### [["The world is quiet here."]]
