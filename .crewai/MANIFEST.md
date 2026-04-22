---
title: "CrewAI Python Layer Manifest"
date created: "2026-04-04"
date updated: "2026-04-12"
authority: crewai
doc_class: manifest
status: active
phase: refoundation
---

# CrewAI Python Layer Manifest

This file is the single live doctrine and topology surface for the CrewAI
Python layer in IDAHO-VAULT.

Current phase: a fresh re-foundation from scaffold, now with a live
bootstrap-validation shard. The initial demo harbor is retired and historical.
No legacy crew, runner, tool, or workflow claim survives unless it is
reintroduced here on purpose.

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
| Package | `crewai[tools,anthropic]>=1.14.1` |
| Python | 3.13+ |
| Environment | `.venv/` (repo-local, uv-managed) |
| Status | Active re-foundation from scaffold |
| Active runners | `uv run crewai run`, `uv run idaho_vault` |
| Active crews | `idaho_vault.bootstrap` |
| Training-ready crews | None yet |
| Output staging | `!/CREWAI/` (live staging / output) |
| Runtime class | Vault-contained local runtime slice |
| Promotion gate | Logan approval required before staged output enters canon |

---

## Live Topology

### Active crews

| Crew | Path | Purpose | Status |
|---|---|---|---|
| `idaho_vault.bootstrap` | `src/idaho_vault/crew.py` | Validate the project contract, lockfile, and package wiring without external model credentials | Active |

### Active crew internals

| Crew | Agent surface | Task surface | Training posture |
|---|---|---|---|
| `idaho_vault.bootstrap` | `src/idaho_vault/config/agents.yaml` -> `bootstrap_validator` | `src/idaho_vault/config/tasks.yaml` -> `deployment_probe` | Registered and runnable, but not a live human-feedback training target |

### Active runners

| Runner | Invocation | Purpose | Status |
|---|---|---|---|
| CrewAI CLI | `uv run crewai run` | Canonical local bootstrap validation run | Active |
| Package entrypoint | `uv run idaho_vault` | Direct invocation of the same bootstrap shard | Active |
| Threshold slice runner | `uv run five_wizards_threshold` | Root-first local `5Wizards` threshold run that stages only to `!/CREWAI/` and leaves promotion to Logan | Active |
| Vault launcher | `powershell -ExecutionPolicy Bypass -File .\scripts\Start-CrewAIVault.ps1` | Vault-contained local invocation with isolated home/AppData paths | Active |

### Writable surfaces

| Surface | Purpose | Persistence |
|---|---|---|
| `.crewai/` | CrewAI registry, manifests, and training surfaces | Durable in git |
| `src/idaho_vault/` | CrewAI Python package, bootstrap crew, and runtime containment code | Durable in git |
| `!/CREWAI/` | Staged CrewAI outputs | Durable in git, not canonical by default |
| `.crewai/logs/` | Execution logs | Ephemeral / gitignored |
| `.crewai_cache/` | Runtime cache | Ephemeral / gitignored |
| `.venv/` | Local Python environment | Ephemeral / local runtime |
| `.agent-home/crewai/` | Vault-local AppData/Home indirection for CrewAI runtime storage | Ephemeral / local runtime |
| `.cache/`, `.state/`, `.tmp/` | Shared vault-local cache/state/temp surfaces | Ephemeral / local runtime |

### Promotion rules

1. CrewAI may write staged outputs to `!/CREWAI/`.
2. Staged outputs are on-record but are not canonical by default.
3. Promotion from `!/CREWAI/` into canon requires Logan approval.
4. Runtime caches, logs, and secret-bearing material never self-promote.
5. `swarm.json` registers the CrewAI layer, but crew/task/runner topology lives here.
6. A crew may be active without being training-ready.

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

These files preserve the package boundary and local CrewAI registry layer while
the Python implementation lives under `src/idaho_vault/`.

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

The current deployment pass is focused on:

1. keeping the bootstrap shard runnable under a vault-contained local runtime
2. validating the package, lockfile, and entrypoint contract without external model credentials
3. recording blockers clearly before any expansion into additional crews or tools
4. extending topology only after new crews are registered here on purpose

Any future crews, tools, or runners must be added as fresh re-foundation work
and registered here before they count as live topology.

Training doctrine note:

- `idaho_vault.bootstrap` is the first live crew, but it exists to validate the
  deployment contract and runtime containment.
- Credentialed or human-feedback training work begins only after a future crew
  is both registered here and explicitly treated as training-ready.
