---
title: "Plain Minimal Handoff"
date: 2026-05-17
updated: 2026-05-18
status: guidance
authority: LOGAN
doc_class: guidance
related:
  - PROTOCOL-XKCD-DRAFT
  - VAULT-ZONES
  - "!-OPENCLAW-HERMES-MAC-WINDOWS-STABILITY-2026-05-17"
---

# Plain Minimal Handoff - 2026-05-17

Logan approved a minimal handoff aid for live Mac/Windows and cross-agent relay work.

This is not a full constitutional promotion of [[PROTOCOL-XKCD-DRAFT]]. It is not a new protocol suite. "XKCD" here refers to the standards-proliferation warning from xkcd 927: do not create a new standard when plain communication is enough.

## Guidance

No agent should assume another agent, machine, or chat session has received context unless Logan relays it or a durable vault note records it.

Agents must not expand, strengthen, rename, or promote XKCD from inference. If Logan asks for protocol work, the agent should either make the specifically requested edit or mark broader ideas as proposed for Logan review.

Borrowed shorthand is not active unless the receiving party has been given the protocol. Use plain language by default.

## Minimal Transfer Format

Use this block when it helps. Do not require it when ordinary plain language is clearer.

```text
PLAIN TRANSFER
FROM:
TO:
CLASS: SIGNAL | REQUEST | SYNC | PATCH | ECHO
TIME:
SUBJECT:
STATE:
ASK:
VERIFY:
```

## Optional Class Meanings

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

## Receipt Pattern

When receiving a transfer, the receiving agent may respond with:

```text
RECEIVED:
UNDERSTOOD:
NEXT:
```

This confirms receipt, states what was understood, and names the next action. It is a readability aid, not ritual language.

Do not substitute `ACK` or other protocol abbreviations unless Logan explicitly asks for that vocabulary in the current coordination thread.

## Open Questions Deferred

- Whether to batch handoff notes into a log.
- Whether to rename historical handoffs.
- Whether to promote the full draft into canonical governance.
- Whether to require self-identification in every commit message.

###### [["The world is quiet here."]]
