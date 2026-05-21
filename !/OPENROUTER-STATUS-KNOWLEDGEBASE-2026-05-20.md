---
title: "OpenRouter Status Knowledgebase"
date: 2026-05-20
status: current
authority: LOGAN
doc_class: knowledgebase
actor: Windows Codex
related:
  - !/PLAN-OPENROUTER-MANAGEMENT-KEY-WINDOWS-CODEX-2026-05-20.md
  - !/OPENROUTER-RUNTIME-KEY-INVENTORY-WINDOWS-CODEX-2026-05-20.md
  - !/OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20.md
  - !/SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md
  - !/BEEFSTACK-MODEL-ROUTING-2026-05-17.md
  - OpenRouter
  - Hermes
  - OpenClaw
  - OpenCode
  - BEEFSTACK
---

# OpenRouter Status Knowledgebase - 2026-05-20

## Current Standing

OpenRouter is the cloud routing leg of the BEEFSTACK model stack. It is not the only model path. The stable model stack remains:

- Ollama for local-first calls where hardware can carry the workload.
- OpenRouter for cloud breadth, fallback routing, and provider resilience.
- OpenCode as a separate coding-agent/workflow lane where it fits.

The current OpenRouter key estate has been inventoried from Windows using the Management Key. No key mutations were made.

## Key Distinction

There are two relevant 1Password items in the `Vault` vault:

| 1Password item | Operational role | Use |
| --- | --- | --- |
| `OpenRouter API Key` | Runtime/model API key | Used for inference and OpenAI-compatible model calls. |
| `OpenRouter Key` | Management Key | Used for OpenRouter key inventory and key administration through `/api/v1/keys`. |

The names are easy to confuse. Operationally:

```text
OpenRouter API Key = runtime/model key
OpenRouter Key     = management key
```

The Management Key must not be handed to Hermes, OpenClaw, OpenCode, or any general-purpose agent. It is a control-plane credential.

## Current Runtime Inventory

The Management API currently lists exactly one runtime key:

| label | hash_prefix | workspace_id | disabled | limit | limit_remaining | limit_reset | usage_daily | byok_usage_daily |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SWARM ROUTER KEY` | `160f2dcf` | `79a8f7cd-9292-5dcf-8450-1419dbee5920` | false | null | null | null | 0 | 0 |

Interpretation:

- `SWARM ROUTER KEY` is enabled.
- It has no key-level spending limit.
- It has no key-level reset window.
- It is currently the only visible runtime key, even with disabled keys included.
- The prior daily-budget failure is not explained by this key's own key-level limit.

## Known Runtime Mapping

The Windows runtime path maps to `SWARM ROUTER KEY`.

Known mappings:

| surface | path | status |
| --- | --- | --- |
| Windows 1Password runtime item | `op://Vault/OpenRouter API Key/credential` | Matches `SWARM ROUTER KEY`. |
| Vault OpenRouter env path | `.op/openrouter.env -> op://Vault/OpenRouter API Key/credential` | Matches `SWARM ROUTER KEY`. |

Unknown or not fully mapped:

| surface | status |
| --- | --- |
| Hermes Mac | Needs Mac-side confirmation against `~/.hermes/.env` or another redacted `/api/v1/key` check. |
| OpenCode | Needs credential-path inspection before it can be mapped. |
| OpenClaw Mac gateway | No current evidence that the gateway itself uses OpenRouter directly. |
| OpenClaw Windows node | Not a model caller unless invoked by a higher-level workflow. |

## Budget Failure Status

Earlier Mac-side raw OpenRouter and Hermes calls returned:

```text
403 Budget limit exceeded (daily limit). Contact your org admin.
```

Current Windows evidence says:

- The runtime key is enabled.
- The runtime key has no key-level cap.
- The runtime key has no key-level remaining balance field.
- Windows raw OpenRouter calls later succeeded for Mistral, Claude, and OpenAI/Codex routes.

Current best interpretation:

- The earlier 403 was likely reset-window timing, workspace/account budget state, provider/BYOK policy, provider route rejection, or a different runtime path.
- It was not proven to be a Hermes bug.
- It was not reproduced in the later Windows raw OpenRouter test.

## Safe Operating Rules

Read-only actions are allowed for diagnostics:

- `GET /api/v1/key`
- `GET /api/v1/keys?include_disabled=true`
- Redacted inventory reports.
- Runtime-key mapping by label/hash prefix/workspace id.

Mutation actions require explicit Logan approval:

- create key
- rename key
- disable key
- delete key
- rotate key
- raise or lower spending limit
- change workspace policy
- change Hermes/OpenClaw/OpenCode routing config

The Management Key must remain in the secret store or in process memory only. It must not be written to scripts, vault notes, logs, chat, config files, or OpenClaw command surfaces.

## Recommended Near-Term Plan

1. Ask Mac Codex to confirm whether Hermes Mac currently maps to the same `SWARM ROUTER KEY` using a redacted `/api/v1/key` check.
2. Inspect OpenCode credential path separately and map it to an OpenRouter key if present.
3. Keep `SWARM ROUTER KEY` as the shared fallback until every active surface is mapped.
4. After mapping, propose separate capped runtime keys for distinct surfaces.
5. Do not mutate OpenRouter key state until Logan explicitly approves the specific mutation plan.

## Proposed Future Key Shape

Provisional labels only:

- `Hermes Mac Runtime Key`
- `Windows Codex Runtime Key`
- `OpenCode Runtime Key`
- `Emergency Shared Fallback Key`

Each non-emergency runtime key should have an explicit daily or monthly cap.

## Current Conclusion

OpenRouter is usable. The Management Key works for read-only inventory. The current runtime estate is simple but too shared for mature agentic operations. The next mature step is not immediate mutation; it is completing runtime mapping, then splitting runtime keys by surface with Logan-approved caps and audit logging.
