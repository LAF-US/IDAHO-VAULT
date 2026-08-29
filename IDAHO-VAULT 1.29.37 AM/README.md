---
updated: 2026-03-25
status: active
related:
- '2026-03-25'
- AGENTS
- CONSTITUTION
- DECISIONS
- LEVELSET
- PROTOCOL
- VAULT-CONVENTIONS
- VAULT-METADATA-STANDARD
- VAULT-TEMPLATES
- VAULT-ZONES
- agent
- chain
- template
authority: LOGAN
---
# `IDAHO-VAULT/!` canonical anchor

This folder is the canonical anchor for orientation inside the vault.
It is a pointer, not a separate constitution or duplicate governance layer.

## Meaning

- Canonical reference form: `IDAHO-VAULT/!`
- Use this path as the top-level orientation marker when describing where the vault "starts"
- Do not assume older path language (`!ADMINISTRATION/`) is still authoritative

## Current adjacent anchors

- `VAULT-METADATA-STANDARD.md` — canonical metadata authority for governed notes

- `CONSTITUTION.md` — canonical constitution
- `PROTOCOL.md` — swarm operational vocabulary
- `AGENTS.md` — agent registry and boundary rules
- `LEVELSET.md` — current living ecosystem status
- `DECISIONS.md` — structural decision log
- `VAULT-CONVENTIONS.md` — shared naming, frontmatter, and structure for all agents
- `VAULT-ZONES.md` — routing grammar for `!`, `!/!`, and `!/!/!`
- `VAULT-TEMPLATES.md` — document class registry and canonical template system
- `!/` — routing layer: DOCKET, LEVELSET, handoffs, context bundles

## Authority chain

- `!/README.md` anchors orientation and canonical path language.
- `VAULT-CONVENTIONS.md` is the shared delegation layer for routing, naming, and write behavior.
- `VAULT-METADATA-STANDARD.md` is the source of truth for governed-note metadata and lifecycle fields.
- `VAULT-TEMPLATES.md` defines note classes and template expectations, subordinate to the metadata standard when fields overlap.
- Live implementation wiring in `.obsidian/`, `.github/`, and `manifest.json` must conform to the vault governance stack and does not replace it.

## Stability note

If instructions, automation, or handoff text drift from this anchor, correct them toward `IDAHO-VAULT/!` and the current root governance stack before adding new process.
Treat older root-level orientation notes such as `!README.md` as historical breadcrumbs, not active metadata/template authority.
