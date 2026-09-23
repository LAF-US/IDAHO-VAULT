---
title: "CrewAI Python Layer Manifest"
date created: "2026-04-04"
date updated: "2026-04-09"
authority: crewai
doc_class: manifest
status: active
phase: refoundation
---

# CrewAI Python Layer Manifest

This file is the single live doctrine and topology surface for the CrewAI
Python layer in IDAHO-VAULT.

Current phase: a fresh re-foundation from scaffold. The initial demo harbor is
retired and historical. No legacy crew, runner, tool, or workflow claim
survives unless it is reintroduced here on purpose.

**Control-plane registration:** `swarm.json` (layer metadata only)
**Live staging/output surface:** `!/CREWAI/`
**Historical harbor records:** `!/CREWAI/HANDOFF-CREWAI-OPS.md`,
`!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md`,
`!/GRIMOIRE/HANDOFF-CREWAI-IGNITION-2026-04-04.md`

---

## Layer Boundaries

| Surface | Role | Authority |
|---|---|---|
| `swarm.json` | Cross-agent registration of the CrewAI layer | Durable control-plane facts only |
| `.crewai/MANIFEST.md` | Live doctrine, topology, and promotion rules | Current CrewAI truth |
| `!/CREWAI/` | Staged output surface | Live staging, on-record but not canonical |
| Historical harbor docs | Thought-history and superseded reasoning | Archive only |

---

## Layered Model

| Layer | Meaning | Writable By | Promotion Rule |
|---|---|---|---|
| `CANON` | Durable promoted authority in the vault | Logan or explicitly approved promotion paths | Canon changes require Logan approval |
| `DRIVE` | Active working surface for code, config, and human edits | Logan and assigned agents | Working changes become durable only when committed and promoted |
| `RUNTIME` | Disposable CrewAI execution slice | Local or remote runners | Runtime artifacts do not self-promote |
| `ARCHIVE` | Preserved historical memory | Human-curated archival work | Historical pages inform doctrine but do not overrule it |

The laptop is not the vault. Portable authority matters more than any single
machine, path, or runtime container.

---

## Current State

| Key | Value |
|---|---|
| Package | `crewai[tools,anthropic]>=1.12.0` |
| Python | 3.13+ |
| Environment | `.venv/` (repo-local) |
| Status | Active re-foundation from scaffold |
| Active runners | None |
| Active crews | None |
| Output staging | `!/CREWAI/` (live staging / output) |
| Runtime class | Linux-native disposable execution slice |
| Promotion gate | Logan approval required before staged output enters canon |

---

## Live Topology

### Active crews

No crews are registered yet. Any future crew introduced under `.crewai/` is new
implementation work, not a revived harbor assumption.

### Active runners

No runners are registered yet. Future runners must be declared here before they
count as live topology.

### Writable surfaces

| Surface | Purpose | Persistence |
|---|---|---|
| `.crewai/` | Committed CrewAI code, manifests, and topology | Durable in git |
| `!/CREWAI/` | Staged CrewAI outputs | Durable in git, not canonical by default |
| `.crewai/logs/` | Execution logs | Ephemeral / gitignored |
| `.crewai_cache/` | Runtime cache | Ephemeral / gitignored |
| `.venv/` | Local Python environment | Ephemeral / local runtime |

### Promotion rules

1. CrewAI may write staged outputs to `!/CREWAI/`.
2. Staged outputs are on-record but are not canonical by default.
3. Promotion from `!/CREWAI/` into canon requires Logan approval.
4. Runtime caches, logs, and secret-bearing material never self-promote.
5. `swarm.json` registers the CrewAI layer, but crew/task/runner topology lives here.

---

## Durable Doctrines

- Portable authority over local romance.
- Remote-first vault with a local runtime slice.
- Clear separation of `CANON`, `DRIVE`, `RUNTIME`, and `ARCHIVE`.
- Promotion rules matter more than storage format.
- Historical reasoning can illuminate doctrine without becoming doctrine.

---

## What Remains From The Scaffold

- `.crewai/__init__.py`
- `.crewai/manifest.json`
- `.crewai/crews/__init__.py`
- `.crewai/tools/__init__.py`

These files preserve the package boundary so the real implementation can be
built without reintroducing retired harbor assumptions.

---

## What Was Retired

- JFAC-specific runner code
- speculative crawler/linker crew definitions
- address-space proof-of-concept scripts
- demo-only tool wrappers

The retirement keeps CrewAI available as a Python-layer option without
pretending the earlier harbor is current.

---

## First Deployment Pass

The first deployment pass should begin from this scaffold and focus on:

1. bootstrap regeneration from `swarm.json`
2. `Gemini` / `Antigravity` live-file split cleanup
3. workflow and config patching
4. best-effort enterprise hookup with blockers recorded clearly

Any future crews, tools, or runners must be added as fresh re-foundation work
and registered here before they count as live topology.
