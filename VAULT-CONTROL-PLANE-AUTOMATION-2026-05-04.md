---
title: "Vault Control Plane Automation"
created: 2026-05-04
updated: 2026-05-04
status: active
authority: LOGAN
authors:
  - Codex
type: automation-registry-note
machine_registry: VAULT-CONTROL-PLANE-AUTOMATION-2026-05-04.json
related:
  - MANIFEST-SPEC
  - manifest.json
  - swarm.json
  - FANDOM-CANON-RULESYSTEMS-2026-05-03
  - TOUCHSTONE-TREE-NOUNS-2026-05-04
  - STUB-PERSONAFOLDERS-2026-05-03
tags:
  - automation
  - control-plane
  - manifest
  - registry
  - validation
---

# Vault Control Plane Automation

This note defines the control-plane automation layer for IDAHO-VAULT.

The machine-readable contract is
`VAULT-CONTROL-PLANE-AUTOMATION-2026-05-04.json`. The runner is
`.github/scripts/check_vault_control_plane.py`.

## Purpose

The vault now has several focused registries and validators:

- FANDOM canon rulesystems
- Touchstone Tree noun anchors
- Touchstone Tree README drift
- durable dotfolder anchors
- stub personafolder standards
- persona anchor frontmatter contracts
- MESHWEB runtime-scope annotations
- Linear gateway dry-run/live-write contract
- backup/hash-ledger verification-first contract
- manifest and bootstrap surfaces

Those lanes should remain separate. The control-plane automation layer does not
merge their doctrine. It composes their checks and verifies that the required
manifests, registries, controls, surfaces, and protocols still exist.

## Rule

Automation should bind the vault like Charter law:

- **Manifests** describe execution and generated state.
- **Registries** list enforceable canonical sets.
- **Controls** run checks and prevent drift.
- **Surfaces** orient agents and humans.
- **Protocols** describe lawful behavior.

When a new lane becomes enforceable, add it to the JSON registry and, where
appropriate, add a dedicated checker. Keep domain logic in the dedicated checker
and let the control-plane runner compose the result.

## Current Gate

The current gate runs:

- durable dotfolder anchor validation
- stub personafolder validation
- persona anchor frontmatter validation
- Touchstone Tree noun validation
- Touchstone Tree README drift validation
- FANDOM canon rulesystem validation
- MESHWEB scope validation
- Linear gateway contract validation
- backup verification-first validation
- control-plane runner syntax validation

The GitHub Actions surface is
`.github/workflows/check-vault-control-plane.yml`.

## Boundary

This is not a replacement for `CONSTITUTION.md`, `!/AGENTS.md`, or
`MANIFEST-SPEC.md`.

It is an automation harness: it confirms that the named control-plane surfaces
exist and that the lane validators pass.
