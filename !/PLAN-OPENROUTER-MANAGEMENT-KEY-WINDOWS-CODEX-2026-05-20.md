---
title: "Plan OpenRouter Management Key Windows Codex"
date: 2026-05-20
status: handoff
authority: LOGAN
doc_class: operational_plan
target_agent: Windows Codex
related:
  - OpenRouter
  - Hermes
  - OpenClaw
  - BEEFSTACK
  - Windows-ZBFURY
  - "OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20"
---

# OpenRouter Management Key Plan For Windows Codex - 2026-05-20

This is a handoff plan for Windows Codex.

Logan is interested in using the OpenRouter Management Key to understand and eventually manage the OpenRouter runtime keys used by the current agent stack. The immediate goal is **not** to let a general-purpose agent freely mutate OpenRouter. The immediate goal is to build a narrow, auditable, read-only-first management workflow.

## Context

The current stack under active work is:

- Hermes on the Mac.
- OpenClaw on the Mac and Windows.
- Windows-ZBFURY as a paired OpenClaw node over SSH tunnel.
- OpenRouter as the cloud fallback/provider layer in the BEEFSTACK model-calling doctrine.
- Ollama and direct provider calls as redundancy paths.

The relevant research note is:

- [[OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20]]

The key architectural finding from that note:

- Runtime API keys are for inference.
- Management API keys are for administrative control of runtime keys.
- The management key is a control-plane root and should not be handed directly to an unconstrained agent.
- Agentic use is appropriate only through a narrow command surface, redacted outputs, and audit logging.

## Logan's Intent

Use an agent, preferably Windows Codex for this stage, to inspect and eventually help manage the OpenRouter API keys related to the active Hermes/OpenClaw/OpenCode routing work.

The desired end state is likely a set of clearly labeled, scoped runtime keys instead of one shared key doing all work.

Possible runtime-key shape:

- `Hermes Mac Runtime Key`
- `OpenClaw Mac Gateway Runtime Key`
- `Windows Codex Runtime Key`
- `OpenCode Runtime Key`
- `Emergency Shared Fallback Key`

Those names are provisional. Do not create or rename keys yet.

## Hard Boundaries

Do not print secrets.

Do not write the management key to the vault, logs, chat, or temporary scripts.

Do not disable, delete, rotate, rename, create, or raise limits on any OpenRouter key without Logan approval.

Do not give Hermes, OpenClaw, or a general agent direct access to the Management Key.

Do not treat `SWARM ROUTER KEY` as wrong or obsolete until the live runtime mapping is proven.

Do not change Hermes/OpenClaw/OpenCode config as part of the read-only inventory phase.

## Phase 1 - Read-Only Inventory

Goal: produce a redacted inventory of the OpenRouter runtime-key estate using the Management Key.

Use the Windows secret store path already proven by Windows Codex. Keep the key out of stdout.

Collect:

- key label or name
- key hash prefix only
- workspace id
- disabled status
- limit
- limit remaining
- limit reset
- include BYOK in limit
- usage daily
- usage weekly
- usage monthly
- BYOK usage daily
- expiration, if present

Do not collect or display full key secrets.

Recommended output format:

```text
label | hash_prefix | workspace_id | disabled | limit | remaining | reset | usage_daily | usage_monthly | byok_daily | notes
```

## Phase 2 - Runtime Mapping

Goal: identify which OpenRouter runtime key is actually used by each active surface.

Surfaces to map:

- Hermes Mac
- OpenClaw Mac gateway
- OpenClaw Windows node if applicable
- Windows Codex/OpenCode launch path
- any `.op/openrouter.env` fallback path
- any 1Password `OpenRouter API Key` item path

Use `/api/v1/key` with each runtime path where possible. Redact the full key and report only:

- key label/name
- hash prefix
- workspace id
- disabled status
- limits
- usage fields
- whether it matches the inventory from Phase 1

If a path cannot be checked without exposing a secret, report that limitation instead of forcing it.

## Phase 3 - Findings Report

Create a vault note, not a config change.

Suggested filename:

```text
!/OPENROUTER-RUNTIME-KEY-INVENTORY-WINDOWS-CODEX-YYYY-MM-DD.md
```

The report should include:

- inventory table
- runtime mapping table
- suspected shared-key risks
- disabled/stale/unknown keys
- keys with no explicit spending limit
- keys with surprising usage
- whether the prior `403 Budget limit exceeded (daily limit)` is explainable by key-level limits
- recommended key plan
- proposed mutations requiring Logan approval

## Phase 4 - Proposed Mutations, Approval Required

After the inventory report, propose a change plan. Do not execute it until Logan explicitly approves.

Possible low-risk proposals:

- create a new capped runtime key for one agent/service
- lower an excessive key limit
- disable a clearly stale key after confirmation
- add labels that clarify ownership

Possible high-risk proposals:

- delete a key
- raise a spending limit
- rotate a shared production key
- change workspace-level policy
- change routing defaults

High-risk actions require explicit Logan approval in the current chat/session before execution.

## Audit Log Requirement

For any management-key action beyond read-only inventory, write an audit entry with:

- timestamp
- actor
- machine
- action
- key hash prefix
- workspace id
- old value
- new value
- reason
- approval source

Never include full secret values.

## Acceptance Criteria For Phase 1

Windows Codex can call the OpenRouter Management API without printing the key.

Windows Codex produces a redacted inventory table.

Windows Codex confirms whether the known `SWARM ROUTER KEY` is enabled, limited, and actively used.

Windows Codex makes no OpenRouter mutations.

Windows Codex makes no Hermes/OpenClaw/OpenCode config edits.

Windows Codex writes findings to the vault and commits them.

## Mac Codex Notes

Mac Codex found the Windows node connected, but generic shell execution through `openclaw nodes invoke` remains intentionally constrained. That is the correct security posture for management-key work.

Prefer running this inventory directly on Windows Codex, where the OpenRouter Management Key path has already been proven, rather than trying to tunnel arbitrary secret-bearing shell commands through OpenClaw.

---

```text
The world is quiet here．Esto Perpetua!
```
