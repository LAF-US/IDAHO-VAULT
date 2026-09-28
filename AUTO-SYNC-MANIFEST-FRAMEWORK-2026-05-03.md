---
title: "Auto-Sync Manifest Framework Research Note"
status: active
authority: LOGAN
date created: 2026-05-03
date modified: 2026-05-03
authors:
  - Codex
related:
  - manifest.json
  - swarm.json
  - coordination.md
  - Hermes
  - OpenClaw
  - OpenRouter
  - Pokemon HOME
  - LEVELSET-CURRENT
---

# Auto-Sync Manifest Framework Research Note

This note records the design gap Logan has been circling: the vault already
has local machine runtimes, a manifest, a registry, and a signal bus, but it
does not yet have a stable auto-sync framework that promotes specific runtime
state into canonical ledgers and registries in a controlled way.

## What already exists

- `~/.hermes/config.yaml` and `~/.openclaw/openclaw.json` hold machine-local
  runtime state.
- `manifest.json` tracks execution-state coordination in GitHub terms.
- `swarm.json` tracks machine-readable registry state and promotion rules.
- `!/SIGNALS/` and `DOCKET.md` carry durable coordination and live visibility.
- `coordination.md` now bridges the older `/SWARM/levelset/` language to the
  newer manifest/signal model.

## What is still missing

- A single explicit sync contract for moving selected runtime facts into canon.
- A canonical answer for which surfaces are machine-local only and which are
  eligible for promotion.
- A lock and conflict model for cross-machine edits on the same logical data.
- A machine-neutral way to track sync state across macOS and Windows without
  treating runtime folders as shared storage.
- A clear rule for when the manifest is the record of execution state and when
  the vault becomes the durable record of the decision.

## Design direction

The likely shape is a staged system:

1. Detect runtime changes on each machine.
2. Normalize them into manifest or registry entries.
3. Gate promotion through explicit rules and locks.
4. Keep secrets and volatile runtime caches out of the shared record.
5. Publish only durable outcomes into the vault, GitHub, or Linear.

## Working assumptions

- Runtime folders remain per-machine.
- Canonical doctrine remains vault-native.
- Execution state remains GitHub-native.
- Coordination remains explicit, not ambient.
- Sync should be promotable, reversible, and reviewable.

## Open questions

- Should sync be event-driven, poll-driven, or both?
- What is the minimum viable manifest for a two-laptop Mac/Windows setup?
- Which runtime fields deserve promotion: model choice, provider, gateway bind,
  auth provenance, health state, or only selected summaries?
- Should OpenClaw and Hermes share one sync vocabulary or keep separate
  manifests with a shared promotion layer?

## Conclusion

The vault already knows how to preserve records. The missing piece is the
explicit framework that decides which runtime facts become shared state and how
they do so without collapsing local machine configuration into canonical truth.
