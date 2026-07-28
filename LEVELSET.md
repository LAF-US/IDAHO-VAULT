---
title: "PROTOCOL — LEVELSET"
doc_class: protocol
version: 0.1
status: draft
authority: LOGAN
date created: 2026-04-27
related:
  - PROTOCOL
  - CONSTITUTION
  - AGENTS
  - LEVELSET-CURRENT-deprecated
  - LEVELSET-2026-04-27
  - DECISIONS
  - REPORT
  - RISE
  - !/AGENTS.md
  - swarm.json
---

# PROTOCOL — LEVELSET

## Status: Draft

## Version: 0.1

## Authority: Loganic Swarm

---

## Overview

LEVELSET is the **session briefing and context-recording protocol** for the IDAHO-VAULT agentic swarm.

It serves as the moment of pause and orientation — the equivalent of gavel-down before committee work begins. LEVELSET captures the current state of the world so that subsequent actions have a durable anchor and future agents can orient without stale assumptions.

**Correction, 2026-05-17:** `LEVELSET-CURRENT.md` is deprecated as an active
output surface. It caused active confusion by presenting a momentary record as
a live current-state authority. Do not update, archive, rotate, or use
`LEVELSET-CURRENT.md` as the target for new LEVELSET work. Use an explicit,
dated, scoped snapshot or handoff note instead.

---

LEVELSET executes:

- **At session start** — before any substantive work begins
- **Before handoff** — when work is passed to another agent
- **Before REPORT** — as the briefing layer for work presentation
- **On demand** — when Logan or an agent requests a fresh snapshot
- **Periodically** — as a standing cadence for long-running sessions

---

## Integration Points

| Document | Relationship |
| --- | --- |
| `LEVELSET.md` (this file) | Protocol definition — what LEVELSET is and does |
| `LEVELSET-CURRENT.md` | Deprecated historical surface — do not update or use as active current state |
| `LEVELSET-2026-04-27.md` | Archived status reports — historical ground truths |
| `CONSTITUTION.md` | Authoritative governance — defines LEVELSET in Section III |
| `AGENTS.md` / `!/AGENTS.md` | Agent registry — confirms authorized voices |
| `swarm.json` | Machine-readable registry — canonical boot chain |
| `DECISIONS.md` | Decision log — durable confirmations |
| `!/!/` | Handoff artifacts — context packages from LEVELSET rounds |

---

## Outputs

| Output | Location | Purpose |
| --- | --- | --- |
| Explicit dated/scoped snapshot | root or scoped protocol folder | Momentary record with stable date/scope |
| Decision entries | DECISIONS.md | Durable record of choices made |
| Handoff packages | `!/!/` | Context bundles for receiving agents |
| Archived snapshots | root or scoped archive path | Historical ground truths |

---

## Constraints

- LEVELSET is a **recording and contextualizing device**, not a live dashboard
- Do not use `LEVELSET-CURRENT.md` as an active output or live dashboard
- Do not accumulate doctrine in snapshots — doctrine returns to canonical governance files
- The Heisenberg principle applies: the act of observing state changes state — acknowledge staleness
- Stale assumptions are the enemy; fresh snapshots are the cure

---

## Draft Status

This document is a **stub** under development. Adoption pending:

- [ ] Logan review and approval
- [ ] Integration with stigmergy field (`scripts/vault-pheromones.py`)
- [ ] Stabilization of protocol steps
- [ ] Constitutional codification update

---

## See Also

- `LEVELSET-CURRENT.md` — deprecated historical surface; do not update
- `LEVELSET-2026-04-27.md` — archived status reports
- `PROTOCOL-SUITE-AWR.md` — AWAKEN/RISE/REPORT lifecycle
- `CONSTITUTION.md` Section III — protocol definitions

---

###### [["The world is quiet here."]]
