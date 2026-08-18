---
title: "OpenRouter Runtime Key Inventory - Windows Codex"
date: 2026-05-20
status: filed
authority: LOGAN
doc_class: operational_report
actor: Windows Codex
machine: LOGAN-ZBFURY
related:
  - "!/PLAN-OPENROUTER-MANAGEMENT-KEY-WINDOWS-CODEX-2026-05-20.md"
  - "!/OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20.md"
  - "!/SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md"
  - OpenRouter
  - Hermes
  - OpenClaw
  - BEEFSTACK
---

# OpenRouter Runtime Key Inventory - Windows Codex

## Scope

This report completes the read-only Windows Codex inventory requested in `!/PLAN-OPENROUTER-MANAGEMENT-KEY-WINDOWS-CODEX-2026-05-20.md`.

Actions taken:

- Read the OpenRouter Management Key from the Windows 1Password secret reference into process memory only.
- Called OpenRouter Management API endpoints for read-only metadata and key inventory.
- Read the known Windows runtime-key reference into process memory only.
- Called `/api/v1/key` for the known runtime key.
- Produced redacted metadata only.

Actions not taken:

- No OpenRouter keys were created, renamed, rotated, disabled, deleted, or limit-modified.
- No Hermes, OpenClaw, OpenCode, or BEEFSTACK runtime config was changed.
- No full secret value was printed, written to the vault, or logged by this report.

## Inventory Table

| label | hash_prefix | workspace_id | disabled | limit | remaining | reset | usage_daily | usage_weekly | usage_monthly | byok_daily | expires_at | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWARM ROUTER KEY | 160f2dcf | 79a8f7cd-9292-5dcf-8450-1419dbee5920 | false | null | null | null | 0 | 3.2115446 | 6.95189201 | 0 | null | Only runtime key listed by the Management API with `include_disabled=true`. |

## Management Key Metadata

The Management Key was accepted by OpenRouter and successfully listed runtime keys.

Redacted metadata:

| field | value |
| --- | --- |
| label | redacted OpenRouter key label |
| disabled | null |
| limit | null |
| limit_remaining | null |
| limit_reset | null |
| include_byok_in_limit | false |
| usage_daily | 0 |
| usage_weekly | 0 |
| usage_monthly | 0 |
| byok_usage_daily | 0 |
| workspace_id | null |

## Runtime Mapping Table

| surface | path | matched inventory | hash_prefix | disabled | limit | usage_daily | usage_weekly | usage_monthly | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Windows 1Password runtime item | `op://Vault/OpenRouter API Key/credential` | yes | 160f2dcf | not reported by `/api/v1/key`; inventory says false | null | 0 | 3.2115446 | 6.95189201 | Matches `SWARM ROUTER KEY` by redacted label metadata and inventory entry. |
| Vault `.op/openrouter.env` fallback path | `.op/openrouter.env -> op://Vault/OpenRouter API Key/credential` | yes | 160f2dcf | not reported by `/api/v1/key`; inventory says false | null | 0 | 3.2115446 | 6.95189201 | Uses the same 1Password runtime reference as the Windows runtime item. |
| Hermes Mac | `~/.hermes/.env` on Mac | not checked in this Windows pass | unknown | unknown | unknown | unknown | unknown | unknown | Requires Mac-side confirmation or a separate redacted Mac-side `/api/v1/key` check. |
| OpenClaw Mac gateway | Mac gateway environment/config | not checked in this Windows pass | unknown | unknown | unknown | unknown | unknown | unknown | No Windows-side evidence that OpenClaw Mac gateway uses an OpenRouter runtime key. |
| OpenClaw Windows node | Windows node runtime | not applicable unless node itself performs model calls | unknown | unknown | unknown | unknown | unknown | unknown | Current OpenClaw node work is transport/command execution, not model inference. |
| OpenCode runtime | Windows OpenCode launch path | not checked in this Windows pass | unknown | unknown | unknown | unknown | unknown | unknown | Needs separate inspection of OpenCode credential path before mapping. |

## Findings

The OpenRouter Management Key works for read-only inventory.

The Management API returned exactly one runtime key:

- `SWARM ROUTER KEY`
- hash prefix `160f2dcf`
- workspace id `79a8f7cd-9292-5dcf-8450-1419dbee5920`
- disabled `false`
- no key-level spending limit
- no key-level remaining limit
- no reset window
- no expiration reported

The known Windows runtime key path matches the inventory entry for `SWARM ROUTER KEY`.

The vault `.op/openrouter.env` path also resolves to the same runtime-key reference.

## Shared-Key Risk

Current evidence indicates Windows runtime use and the vault fallback path both point to the same shared runtime key: `SWARM ROUTER KEY`.

This is operationally simple but weak for attribution and blast-radius control. If Hermes, OpenCode, OpenClaw-adjacent tooling, and Codex all share this key, OpenRouter usage cannot be cleanly attributed by agent or service from key metadata alone.

## Disabled, Stale, Or Unknown Keys

No disabled runtime keys were returned by the Management API, even with `include_disabled=true`.

No stale runtime keys were visible from this inventory.

Mac Hermes, OpenCode, and any direct-provider fallback paths remain unknown in this Windows-only pass.

## Keys With No Explicit Spending Limit

`SWARM ROUTER KEY` has:

- `limit: null`
- `limit_remaining: null`
- `limit_reset: null`

This means the key has no key-level cap visible through the Management API. That may be intentional, but it is not ideal for long-term agentic operation if the key is shared across multiple surfaces.

## Prior 403 Budget Limit Finding

The prior `403 Budget limit exceeded (daily limit)` is not explainable by the runtime key's key-level limit.

Evidence:

- `SWARM ROUTER KEY` is enabled.
- `SWARM ROUTER KEY` has no key-level limit.
- `SWARM ROUTER KEY` has no key-level remaining cap.
- `usage_daily` was 0 during this inventory.
- `byok_usage_daily` was 0 during this inventory.

The earlier 403 is more consistent with one of:

- reset-window timing
- workspace/account-level budget outside the runtime key limit
- provider/BYOK policy at the upstream provider layer
- model/provider route-specific rejection
- a different runtime path than the Windows key path checked here

## Recommended Key Plan

Do not mutate yet. Proposed direction for Logan approval:

1. Keep `SWARM ROUTER KEY` as the emergency shared fallback until all active surfaces are mapped.
2. Create separate capped runtime keys for distinct surfaces only after mapping is complete.
3. Suggested eventual labels:
   - `Hermes Mac Runtime Key`
   - `Windows Codex Runtime Key`
   - `OpenCode Runtime Key`
   - `Emergency Shared Fallback Key`
4. Give each non-emergency key an explicit daily or monthly limit.
5. Keep the Management Key confined to 1Password and a narrow broker/tool surface.

## Proposed Mutations Requiring Logan Approval

No mutations are approved by this report.

Candidate future actions:

- Create a capped `Windows Codex Runtime Key`.
- Create a capped `Hermes Mac Runtime Key` after Mac confirms the current Hermes runtime path.
- Rename `SWARM ROUTER KEY` only if Logan decides it should become the emergency fallback.
- Add explicit limits to any new runtime keys at creation time.

High-risk actions requiring explicit approval:

- delete any key
- rotate the shared production key
- raise any spending limit
- change workspace-level policy
- change Hermes/OpenClaw/OpenCode routing defaults

## Verification

Read-only OpenRouter endpoints used:

```text
GET https://openrouter.ai/api/v1/key
GET https://openrouter.ai/api/v1/keys?include_disabled=true
```

Result:

- Management Key call succeeded.
- Runtime-key metadata call succeeded.
- Inventory produced redacted output.
- No mutations were made.
