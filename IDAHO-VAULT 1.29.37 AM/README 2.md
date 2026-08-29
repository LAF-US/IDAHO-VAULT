---
updated: 2026-04-02
status: active
related:
- '2026-04-02'
- AGENTS
- CONSTITUTION
- DECISIONS
- LEVELSET
- README
- README 1
- VAULT-CONVENTIONS
- VAULT-METADATA-STANDARD
- VAULT-TEMPLATES
- agent
- chain
- doctrine
- index
- links
- template
authority: LOGAN
---
# `IDAHO-VAULT/!` canonical anchor

This folder is the canonical anchor for orientation inside the vault.
It is a routing and bootstrap layer, not a duplicate governance corpus.

## Meaning

- Canonical reference form: `IDAHO-VAULT/!`
- Use this path as the top-level orientation marker when describing where the vault "starts"
- Use `!/` aliases when a stable bootstrap path matters across tools
- Do not assume older path language (`!ADMIN/`, `!ADMINISTRATION/`) is still authoritative

## Current adjacent anchors

- `CONSTITUTION.md` at repo root - canonical constitution
- `DECISIONS.md` at repo root - canonical decision log
- `LEVELSET.md` at repo root - current ecosystem state
- `VAULT-CONVENTIONS.md` at repo root - shared routing, naming, and write conventions
- `VAULT-METADATA-STANDARD.md` at repo root - metadata authority for governed notes
- `VAULT-TEMPLATES.md` at repo root - document class registry and canonical template system
- `swarm.json` at repo root - canonical machine-readable registry
- `!/AGENTS.md` - canonical narrative agent registry
- `!/agents.json` - generated bootstrap index
- `!/agent.sh` - canonical local bootstrap entrypoint

## Authority chain

1. `AGENTS.md` at repo root is the auto-loaded cross-tool pointer.
2. `!/AGENTS.md` is the canonical narrative registry.
3. `swarm.json` is the machine-readable source of truth.
4. `!/agents.json` is the generated bootstrap index.
5. `!/agent.sh` is the canonical local bootstrap entrypoint.
6. Root governance files remain the doctrine layer; `!/CONSTITUTION.md`, `!/DECISIONS.md`, `!/LEVELSET.md`, and `!/VAULT-CONVENTIONS.md` are routing shims.

## Stability note

If instructions, automation, or handoff text drift from this anchor, correct them toward `IDAHO-VAULT/!` and the current root governance stack before adding new process.
Treat older root-level orientation notes such as `!README.md` as historical breadcrumbs, not active metadata or template authority.

`README 1.md` remains in this folder only as a temporary compatibility artifact while older links are cleaned up.
