---
title: "Bartimaeus — CrewAI Alignment Brief"
date created: "2026-04-04"
authority: bartimaeus
doc_class: directive
status: pending_recipient
relay: "Logan Finney -> Bartimaeus -> Claude Code (The Abhorsen)"
note: "Bartimaeus has no active swarm role as of 2026-04-10. Content is valid doctrine — see relay field. Filed in OUTBOX pending Bartimaeus activation or re-routing to Claude direct."
---

# Bartimaeus — CrewAI Alignment Brief

**Relayed:** 2026-04-04 by Logan Finney
**Addressed to:** Claude Code / The Abhorsen
**Subject:** Alignment of NETWEB UNIFIED (US) SWARM to proposed CrewAI implementation and deployment

---

## Core Directive

You are not inventing a new sovereign system. You are docking CrewAI into an existing control plane.

---

## Current Truth from the Vault

- Human/narrative registry: `!/AGENTS.md`
- Bootstrap protocol: `AGENT-PROTOCOL.md`
- Machine-readable swarm registry: `swarm.json`
- Project marker: `(US).md`
- Existing swarm note: `UNIFIED (US) SWARM.md`

---

## What Must Remain True

- The vault is still the record.
- GitHub remains the durable execution substrate.
- Linear remains the coordination brain.
- Slack remains breadcrumb-only.
- CrewAI is an orchestration layer, not a new source of truth.

---

## What CrewAI Should Become

- A lightweight harbor for bounded, named crews.
- Local-first where possible, with contained dependencies and explicit logs/state.
- A runner for concrete swarm jobs, not a vague "AI swarm."

---

## Recommended First Crew Shape

- **JFAC Parser:** structured extraction from budget / legislative artifacts.
- **Task-to-Code Bridge:** convert scoped work items into implementation plans or code tasks.
- **Vault Custodian:** classify, normalize, and propose filing/metadata actions for vault materials.

---

## Implementation Rules

- Keep CrewAI runtime isolated in a repo-local environment.
- Treat `.crewai_cache/` and `.crewai/logs/` as ephemeral runtime surfaces, not canonical artifacts.
- Persist only durable outputs back into the vault as notes, briefs, manifests, or generated structured files.
- Every crew run should leave evidence inside the vault: what ran, on what inputs, what outputs were produced, and where the handoff landed.
- Do not let CrewAI bypass GitHub/Linear discipline. If it changes code or governance, it still goes through branch/PR/issue lanes.

---

## Deployment Stance

- Keep the repo lean. Media/binary bloat has already been identified as a deployment risk; use LFS and avoid stuffing CrewAI state into git.
- Separate:
  - code/config committed to repo
  - ephemeral runtime/cache ignored locally
  - durable outputs written intentionally into the vault
- Prefer explicit config over hidden magic. A future agent should be able to see how the harbor works by reading the repo.

---

## Minimum Artifact Set

- `crew/` or similarly clear runtime folder for CrewAI code/config
- a small manifest describing crews, agents, tasks, tools, and outputs
- one reproducible example run per initial crew
- one vault-written handoff note explaining how to run, inspect, and extend the system

---

## Non-Goals

- Do not replace `swarm.json` with CrewAI config.
- Do not collapse personas and agents into generic CrewAI placeholders.
- Do not make Slack or transient logs the operational memory.
- Do not create a theatrical swarm before the three concrete crews work end-to-end.

---

## Command Intent

Build CrewAI as the execution harbor for NETWEB UNIFIED (US) SWARM, but keep authority, evidence, and coordination anchored in the vault, GitHub, and Linear exactly as the current control plane already defines them.

---

###### The world is quiet here.
