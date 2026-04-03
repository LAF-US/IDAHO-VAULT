---
tags:
  - administration/levelset
updated: 2026-04-02
status: active
source: ground-truth
---

# LEVELSET

Current status of the IDAHO-VAULT ecosystem as of **2026-04-02 (America/Denver)**.
This file is intentionally rewritten as a fresh snapshot to remove stale assumptions.

## Ground Truth Snapshot

- **Repository:** `IDAHO-VAULT`
- **Current branch:** `codex/repair-agent-registry-breadcrumbs`
- **Working tree:** mixed local work is present; do not assume a clean tree
- **Coordination hub:** `LAF-25`
- **Scoped registry lane:** `LAF-28`
- **Registry source of truth:** `swarm.json`

## What Changed In This Refresh

This snapshot closes a split-doctrine problem in the registry/bootstrap layer:

1. Missing `!/` registry files were materialized.
2. Root governance docs stayed authoritative.
3. `!/` gained explicit routing shims for bootstrap stability.
4. The canonical local bootstrap path is now coherent again.

## Current Governance Anchors

Use these files as the active orientation stack:

1. `!/README.md`
2. `AGENTS.md` (root auto-loaded pointer)
3. `!/AGENTS.md`
4. `CONSTITUTION.md`
5. `DECISIONS.md`
6. `LEVELSET.md` (this file)
7. `VAULT-CONVENTIONS.md`
8. `AGENT-PROTOCOL.md`
9. `swarm.json`

## Active Notes

- Root `AGENTS.md` remains the cross-tool pointer; `!/AGENTS.md` is the canonical narrative registry.
- `!/agents.json` is the canonical generated bootstrap index; root `agents.json` is the compatibility mirror.
- `!/agent.sh` is the canonical local bootstrap entrypoint; root `agent.sh` is the compatibility wrapper.
- Registry-critical conflict markers were removed from `CONSTITUTION.md`, `DECISIONS.md`, `LEVELSET.md`, `VAULT-CONVENTIONS.md`, and `agents.json`.
- The live coordination triptych remains stable:
  - GitHub: execution transport
  - Linear: active coordination
  - Slack: breadcrumb-only

## Operator Guidance (Now)

When resuming work in a new session:

1. Re-check branch and local state (`git branch --show-current`, `git status --short`).
2. Confirm the registry chain before using local bootstrap (`AGENTS.md`, `!/AGENTS.md`, `swarm.json`, `!/agents.json`, `!/agent.sh`).
3. Treat root governance files as doctrine and `!/` as routing/bootstrap aliases unless Logan directs otherwise.
