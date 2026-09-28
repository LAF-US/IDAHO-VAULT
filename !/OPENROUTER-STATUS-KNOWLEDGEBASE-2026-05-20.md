---
title: "OpenRouter Status Knowledgebase"
date: 2026-05-20
status: current
authority: LOGAN
doc_class: knowledgebase
actor: Windows Codex
related:
  - "!/PLAN-OPENROUTER-MANAGEMENT-KEY-WINDOWS-CODEX-2026-05-20.md"
  - "!/OPENROUTER-RUNTIME-KEY-INVENTORY-WINDOWS-CODEX-2026-05-20.md"
  - "!/OPENROUTER-KEYS-WINDOWS-CODEX-REPORT-2026-05-20.md"
  - "!/SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md"
  - "!/BEEFSTACK-MODEL-ROUTING-2026-05-17.md"
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
| OpenCode Windows credential store | `~/.local/share/opencode/auth.json` provider `openrouter` | Matches `SWARM ROUTER KEY` by SHA256 prefix `160f2dcf`; secret value not printed. |
| OpenClaw Windows provider env | `~/.openclaw/openclaw.json` `env.vars.OPENROUTER_API_KEY` | Matches `SWARM ROUTER KEY` by SHA256 prefix `160f2dcf`; secret value not printed. |

Unknown or not fully mapped:

| surface | status |
| --- | --- |
| Hermes Mac | Mac-side snapshot says Hermes maps to the same `SWARM ROUTER KEY`; Windows has not directly inspected Mac `~/.hermes/.env`. |
| OpenClaw Mac gateway | No current evidence that the gateway itself uses OpenRouter directly. |
| OpenClaw Windows node | Node transport identity is separate from model routing; Windows config does have an OpenRouter provider wired to `OPENROUTER_API_KEY`. |

## 2026-05-20 Windows Surface Mapping Addendum

Windows Codex performed a read-only mapping pass across OpenCode and OpenClaw after Mac pushed the key/status snapshot. No key, model, OpenClaw, Hermes, or OpenCode configuration was changed.

OpenCode:

- `opencode providers list` reports three stored API credentials: OpenCode Zen, OpenRouter, and Mistral.
- The global OpenCode config at `~/.config/opencode/opencode.jsonc` currently contains only the schema pointer.
- The stored OpenCode `openrouter` credential hashes to SHA256 prefix `160f2dcf`, matching `SWARM ROUTER KEY`.
- The stored OpenCode `mistral` credential hashes to SHA256 prefix `d4d78398`.
- The stored OpenCode `opencode` credential hashes to SHA256 prefix `c66b70ef`.

OpenClaw Windows:

- `~/.openclaw/node.json` identifies the Windows node as `Windows-ZBFURY`, node id `windows-zbfury-20260516`, targeting gateway host `127.0.0.1` port `18790`.
- `~/.openclaw/openclaw.json` includes model providers for `openrouter` and `ollama`.
- The OpenClaw `openrouter` provider uses `https://openrouter.ai/api/v1` and `apiKey: env:OPENROUTER_API_KEY`.
- `env.vars.OPENROUTER_API_KEY` hashes to SHA256 prefix `160f2dcf`, matching `SWARM ROUTER KEY`.
- The Windows OpenClaw config currently stores provider env values directly in the user-profile config, not only as `op://` references. This is an observation, not a mutation request.

Current interpretation:

- Windows OpenCode and Windows OpenClaw are both mapped to the same OpenRouter runtime key as the vault runtime item.
- The OpenCode and OpenClaw findings reinforce that the earlier `403 Budget limit exceeded (daily limit)` was not caused by an unknown Windows runtime key.
- The remaining mature-hardening question is key separation and cap design by surface, not emergency key repair.

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

## BYOK Rate-Limit Addendum

Later Hermes evidence showed a different failure mode:

```text
HTTP 429 Provider returned error
provider_name: Mistral
is_byok: true
raw provider code: 1300
```

The next direct Mistral fallback also returned `429 Rate limit exceeded` with the same provider code. A later OpenRouter Mistral Small route succeeded.

Interpretation:

- This is not the same as the earlier OpenRouter `403 Budget limit exceeded`.
- This is not explained by the OpenRouter runtime key's own key-level cap.
- This is a provider-side Mistral BYOK rate limit.
- OpenRouter BYOK Mistral and direct Mistral can share the same upstream rate-limit bucket.
- Fallback chains should diversify by provider bucket, not merely by model family.

Operational implication:

After a Mistral BYOK `429`, the next automatic fallback should usually move to a different provider bucket, such as non-BYOK OpenRouter capacity if available, Claude, OpenAI/Codex, or local Ollama. Direct Mistral is still useful for OpenRouter transport/account failures, but it is not a good immediate fallback for exhausted Mistral BYOK capacity.

## Hermes Routing Adjustment - 2026-05-21

Mac Codex adjusted Hermes on the MacBook to make the fallback chain BYOK-aware.

Previous problem:

```text
OpenRouter Mistral BYOK 429
-> direct Mistral fallback
-> same upstream Mistral 429
```

Current Hermes fallback order:

```text
primary: openrouter / mistralai/mistral-medium-3-5
1. openrouter / mistralai/mistral-small-2603
2. openrouter / anthropic/claude-haiku-4.5
3. openrouter / anthropic/claude-sonnet-4.6
4. openrouter / openai/gpt-5.3-codex
5. custom direct Mistral / mistral-small-2603
6. openrouter / mistralai/mistral-large-2512
```

Title generation was also moved from direct Mistral to OpenRouter Mistral Small.

Verification:

- `hermes fallback list` showed the new order.
- `hermes -z "Reply with exactly: HERMES_BYOK_ROUTING_OK"` returned the exact expected response.
- `hermes gateway restart` succeeded.
- `hermes gateway status` showed the service loaded with a fresh PID.

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
2. Keep `SWARM ROUTER KEY` as the shared fallback until every active surface is mapped and Logan approves separation.
3. After mapping, propose separate capped runtime keys for distinct surfaces.
4. Decide whether Windows OpenClaw should continue carrying plaintext provider env values in `~/.openclaw/openclaw.json`, or move to a 1Password-backed launch path.
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
