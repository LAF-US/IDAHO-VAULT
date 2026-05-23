---
title: "Plan: Management Key → Hermes (Direct Env Var)"
date: 2026-05-23
status: partial
authority: LOGAN
doc_class: operational_plan
---

## Goal

Put `OPENROUTER_MANAGEMENT_KEY` into `~/.hermes/.env` on the Mac so Hermes
can call the OpenRouter management API via `terminal` + `curl` or
`execute_code` + Python `requests`.

## Scope

One-time manual key transfer. No MCP server, no wrapper script, no new
infrastructure. The key came from the existing 1Password
`OpenRouter Management Key` item managed by OpenClaw on the Windows
machine (LOGAN-ZBFURY).

## Execution Record

### Step 1 — Transfer

Done. Key read from 1Password (via `op read`) and printed to stdout on
Windows. The raw value is now in the control of the operator for manual
copy to the Mac.

### Step 2 — Verify (operator action needed)

On the Mac, after adding to `~/.hermes/.env`:

1. `echo 'OPENROUTER_MANAGEMENT_KEY=<key>' >> ~/.hermes/.env`
2. Launch Hermes and run:
   `terminal: curl -s -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" https://openrouter.ai/api/v1/keys`
3. Expected output: JSON array of runtime key metadata.

### Step 3 — Hermes Usage Guide (see companion note)

See `!/OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE-2026-05-23.md` for the
canonical Hermes-usable management endpoint reference.

## Hard Boundaries (from prior plan, Logan-ratified)

- The Management Key cannot do inference — strict to `/api/v1/keys` endpoints.
- Mutations (create, disable, delete, limit changes) require Logan approval
  before execution.
- Do not print the key value in transcripts, logs, or vault files.
- Do not write the key to source control.
