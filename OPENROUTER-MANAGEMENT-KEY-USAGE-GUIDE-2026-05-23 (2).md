---
title: "OpenRouter Management Key — Hermes Usage Guide"
date: 2026-05-23
status: live
authority: LOGAN
doc_class: reference
related:
  - Hermes
  - OpenRouter
  - BEEFSTACK
  - "PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23"
---

## Where the key lives

The Management Key is set as `OPENROUTER_MANAGEMENT_KEY` in
`~/.hermes/.env` on the Mac. Hermes loads this at startup.

The canonical source of truth for the key value is 1Password on Windows
(LOGAN-ZBFURY), item `OpenRouter Management Key` in the `Private` vault,
readable via `op read "op://Private/OpenRouter Management Key/credential"`.

## How Hermes calls the management API

All endpoints at `https://openrouter.ai/api/v1/keys`:

### List all keys
```
terminal: curl -s -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" https://openrouter.ai/api/v1/keys
```

### Inspect a specific key (by hash)
```
terminal: curl -s -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" https://openrouter.ai/api/v1/keys/<hash>
```

### Create a new runtime key
```
terminal: curl -s -X POST -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" -H "Content-Type: application/json" -d '{"name":"agent-label","limit":100,"limit_reset":"daily"}' https://openrouter.ai/api/v1/keys
```

### Disable a key
```
terminal: curl -s -X PATCH -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" -H "Content-Type: application/json" -d '{"disabled":true}' https://openrouter.ai/api/v1/keys/<hash>
```

### Update a key limit
```
terminal: curl -s -X PATCH -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" -H "Content-Type: application/json" -d '{"limit":50,"limit_reset":"daily"}' https://openrouter.ai/api/v1/keys/<hash>
```

### Delete a key
```
terminal: curl -s -X DELETE -H "Authorization: Bearer $OPENROUTER_MANAGEMENT_KEY" https://openrouter.ai/api/v1/keys/<hash>
```

## Safety rules

| Action | Autonomy | Notes |
|---|---|---|
| List keys, inspect metadata, check usage | Autonomous | Read-only, no Logan approval needed |
| Create runtime key with strict cap | Semi-autonomous | Inform Logan after creation |
| Disable a key | Semi-autonomous | Inform Logan after disabling |
| Delete a key | Requires Logan approval | Before execution |
| Raise a limit | Requires Logan approval | Before execution |
| Modify shared/production keys | Requires Logan approval | Before execution |

## Audit requirement

For any mutation (create, disable, delete, limit change), write an audit
entry with: timestamp, actor, action, key hash prefix, old value, new
value, reason, approval source. Do not include full secret values.

## Key context

- The Management Key is a control-plane root for runtime keys only.
- It cannot be used for inference (`/api/v1/chat/completions`).
- It operates at the account level and can manage keys across workspaces.
- Never print the raw key value in transcripts, vault files, or logs.

## Related docs

- `!/PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23.md` — transfer plan
- `!/OPENROUTER-RUNTIME-KEY-INVENTORY-WINDOWS-CODEX-2026-05-20.md` — Phase 1 inventory
- `!/BEEFSTACK-MODEL-ROUTING-2026-05-17.md` — BEEFSTACK architecture
