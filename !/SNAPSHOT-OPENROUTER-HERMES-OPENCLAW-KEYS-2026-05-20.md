---
title: "Snapshot OpenRouter Hermes OpenClaw Keys"
date: 2026-05-20
status: current
authority: LOGAN
doc_class: operational_snapshot
related:
  - OpenRouter
  - Hermes
  - OpenClaw
  - OpenCode
  - BEEFSTACK
  - Windows-ZBFURY
  - "!/OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20.md"
  - "!/OPENROUTER-RUNTIME-KEY-INVENTORY-WINDOWS-CODEX-2026-05-20.md"
  - "!/PLAN-OPENROUTER-MANAGEMENT-KEY-WINDOWS-CODEX-2026-05-20.md"
  - "!/SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md"
---

# OpenRouter / Hermes / OpenClaw Key Snapshot - 2026-05-20

This note records the current working knowledgebase for OpenRouter key management and model-routing reliability across Mac Hermes, Mac OpenClaw, Windows Codex, and the BEEFSTACK direction.

No secret values are recorded here.

## Executive Status

The OpenRouter key ambiguity is resolved.

There are two distinct 1Password items:

| 1Password item | Current understanding | Purpose |
| --- | --- | --- |
| `Vault/OpenRouter API Key` | `SWARM ROUTER KEY` | Runtime inference key for model calls. |
| `Vault/OpenRouter Key` | OpenRouter Management Key | Administrative key for listing/managing runtime keys through `/api/v1/keys`. |

The `SWARM ROUTER KEY` is **not** a management key.

The Management Key is **not** for model calls.

## Confirmed Runtime Key Facts

Windows Codex read-only inventory found exactly one visible runtime key through the OpenRouter Management API:

| label | hash prefix | disabled | key-level limit | reset | expiration |
| --- | --- | --- | --- | --- | --- |
| `SWARM ROUTER KEY` | `160f2dcf` | false | null | null | null |

Windows Codex confirmed:

- The runtime item `op://Vault/OpenRouter API Key/credential` maps to `SWARM ROUTER KEY`.
- The vault `.op/openrouter.env` fallback path maps to the same runtime item.
- The Management Key call succeeded for read-only inventory.
- No keys were created, renamed, rotated, disabled, deleted, or limit-modified.

Mac Codex confirmed:

- Mac Hermes `OPENROUTER_API_KEY` is also a runtime key, not a management key.
- `/api/v1/key` returned `is_management_key: false`.
- `/api/v1/key` returned `is_provisioning_key: false`.
- Usage metadata matched the Windows inventory values for `SWARM ROUTER KEY`.

Therefore, current evidence indicates Mac Hermes and Windows runtime paths are using the same shared OpenRouter runtime key.

## Current Risk Picture

The shared runtime key is operationally simple but weak for attribution and blast-radius control.

If Hermes, Codex, OpenCode, and OpenClaw-adjacent tools all use `SWARM ROUTER KEY`, OpenRouter usage cannot be cleanly attributed by key metadata. A future runaway or misconfigured agent would be harder to isolate.

The prior Hermes `403 Budget limit exceeded (daily limit)` is **not explained by the runtime key's own key-level limit**, because:

- `SWARM ROUTER KEY` is enabled.
- `SWARM ROUTER KEY` has no key-level limit.
- `SWARM ROUTER KEY` has no key-level remaining cap.
- BYOK daily usage was zero during the Windows inventory.

More likely explanations remain:

- account-level or workspace-level budget policy
- reset-window timing
- upstream provider or BYOK policy
- model/provider-route-specific rejection
- a different runtime path at the time of the failure
- unclear OpenRouter error surfacing from a provider-layer rejection

## Hermes Status

Hermes on Mac is currently usable again.

Recent reliability work established:

- Hermes can converse interactively.
- Messaging smoke tests through Discord, Telegram, and WhatsApp succeeded from Hermes.
- Hermes OpenRouter calls encountered the budget-related `403`, but fallback routing recovered after configuration/code fixes.
- Mac Hermes can use direct Mistral fallback when OpenRouter fails.
- `hermes -z` one-shot mode was patched to actually pass configured fallback chains into `AIAgent`.
- Hermes title generation was moved off the noisy OpenRouter path to avoid secondary `403` failures after successful fallback.

Current practical meaning:

- OpenRouter is still useful, but not the only route.
- Direct Mistral fallback is an important reliability leg.
- Hermes should not be treated as fully OpenRouter-reliable until OpenRouter account/workspace/provider behavior is better understood.

## OpenClaw / Windows Link Status

OpenClaw Mac-to-Windows pairing is stable at the transport level.

Known stable state from prior verification:

- Mac OpenClaw gateway: `2026.5.16-beta.3`.
- Windows OpenClaw node: `2026.5.16-beta.3`.
- Windows node: `Windows-ZBFURY`.
- Mac gateway is loopback-bound.
- Windows reaches Mac gateway through SSH tunnel.
- Windows node is paired and connected.
- Prior stress test: `15/15` successful Mac-to-Windows invokes.

Important caveat:

- Generic shell execution through `openclaw nodes invoke` remains intentionally constrained.
- This is the right security posture for management-key work.
- Do not tunnel arbitrary secret-bearing shell commands through OpenClaw unless a scoped, approved execution path exists.

## BEEFSTACK Alignment

The current state supports Logan's redundancy doctrine:

```text
Ollama + OpenRouter + OpenCode
```

Interpreted as:

- Ollama for local/simple calls where hardware and latency permit.
- OpenRouter for cloud model breadth, complex calls, and hosted fallback.
- OpenCode as a coding execution surface.
- Direct provider calls, especially Mistral direct, as a contingency when OpenRouter or local models fail.

Preference order remains:

1. Mistral
2. Claude
3. ChatGPT/OpenAI

Avoid for active routing:

- Phi
- Qwen
- Gemma
- Gemini

Gemini/Google credentials may still be appropriate for TTS or Google Cloud infrastructure when explicitly scoped.

## Management Key Doctrine

The OpenRouter Management Key should be treated as privileged infrastructure control.

Good agentic uses:

- list runtime keys
- inspect key metadata
- produce usage reports
- detect stale/disabled/over-budget keys
- propose key separation plans
- create capped runtime keys after approval
- disable compromised keys after approval

Do not allow:

- arbitrary agents directly holding the Management Key
- unapproved key deletion
- unapproved key rotation
- unapproved limit increases
- silent workspace policy changes
- broad mutation without audit logs

Preferred architecture:

```text
agent request
-> local policy gate / broker
-> OpenRouter Management API
-> redacted result
-> durable audit log
-> Logan approval for mutations
```

## Known Unknowns

Still needs mapping:

- OpenCode runtime key path.
- Whether Mac OpenClaw gateway is using OpenRouter directly or only through agent/provider config.
- Whether any old scripts still read `.op/openrouter.env` as plaintext fallback rather than 1Password reference.
- Whether a future dedicated Hermes runtime key should be created before changing Hermes config.
- Whether OpenRouter workspace-level budgets or guardrails explain the prior `403`.

## Proposed Next Steps

1. Complete read-only runtime mapping for OpenCode.
2. Complete read-only OpenClaw model-provider mapping.
3. Decide whether `SWARM ROUTER KEY` should remain the emergency shared fallback.
4. If Logan approves, use the Management Key to create separate capped runtime keys:
   - `Hermes Mac Runtime Key`
   - `Windows Codex Runtime Key`
   - `OpenCode Runtime Key`
5. Update configs one surface at a time, testing after each change.
6. Record each mutation in an audit note with hash prefixes only.

## Standing Rule

Until Logan approves otherwise:

- read-only inventory is allowed
- redacted reporting is allowed
- key mutation is not allowed
- runtime config changes are not allowed
- full key values stay out of chat, vault, and logs

The world is quiet here.
