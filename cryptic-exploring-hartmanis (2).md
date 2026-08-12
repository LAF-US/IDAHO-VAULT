# Plan: Gemini Calibration — Turn 3 Message + Sequence

## Context

ChatGPT drafted the first two Gemini calibration turns. Logan wants Claude to take over as the turn-drafter going forward. Gemini has correctly oriented itself (ORIENTATION format, all 4 files read), confirmed its canonical role as "The Vault Advisor," and asked for DOCKET.md next. The goal is to move Gemini from calibration into actual productive work via the Linear-first pilot.

## Current State

- Gemini answered correctly: role confirmed, inventory understood, Linear pilot endorsed, DOCKET.md requested
- DOCKET shows gap: "Gemini vault activity undefined"
- Largest open task matching Gemini's role: **LAF-7 Decomposition + routing plan** (All agents, Drafting)
- Plugin auth inventory (`!/PLUGIN-AUTH-INVENTORY-2026-03-28.md`) is untracked — a small concrete deliverable Gemini could help document
- Gemini is authorized: Direct write (support), but no write task assigned yet

## Turn 3 Message (to send to Gemini)

```text
Read this file:
  !/!/!/! The world is quiet here/DOCKET.md

Then reply in exactly this format:
- `DOCKET READ`
- `What I understand to be my active gap:` one sentence
- `Proposed first task this session:` one sentence naming the specific deliverable
- `Files I need to read before starting:` flat list (paths only)
- `Write scope:` one sentence describing exactly what I would create or modify
- `Waiting for go-ahead`

Do not start the task yet. Do not edit files. Do not propose alternatives.
```

## Why This Message

- Keeps Gemini constrained to read-only until Logan gives explicit go-ahead
- Forces Gemini to name one concrete deliverable (not a vague "I can help with...")
- The "gap" prompt steers it toward "Gemini vault activity undefined" without hand-holding
- "Files I need to read before starting" surfaces any missing context before work begins
- "Waiting for go-ahead" gates the write — Logan approves before execution

## Turn 4 (after Gemini proposes task)

Logan reviews Gemini's proposed task. If approved:

```text
Go ahead. One PR, one branch, one deliverable. Report back with branch name and what changed.
```

If Gemini proposes something too broad or wrong:

```text
Narrow the scope. [specific constraint]. Re-propose.
```

## Critical Files

- `c:\Users\loganf\Documents\IDAHO-VAULT\!/!/!/! The world is quiet here\DOCKET.md`
- `c:\Users\loganf\Documents\IDAHO-VAULT\!/PLUGIN-AUTH-INVENTORY-2026-03-28.md`
- `c:\Users\loganf\Documents\IDAHO-VAULT\!/AGENTS.md`

## Verification

- Gemini responds with DOCKET READ format
- Proposed task is specific, scoped to one file or deliverable
- No edits occur until Logan sends go-ahead
- After go-ahead: new branch appears in GitHub, PR opened, DOCKET updated
