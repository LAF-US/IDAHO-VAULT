---
title: "CrewAI Python Layer Manifest"
date created: "2026-04-04"
date updated: "2026-08-13"
author: "Manus AI"
authority: crewai
doc_class: manifest
status: active
phase: refoundation
---

# CrewAI Python Layer Manifest

This file is the single live doctrine and topology surface for the CrewAI Python layer in IDAHO-VAULT. The former bootstrap-validation shard is historical. The registered implementation is a bounded `FiveWizardsCouncil` inquiry crew; it may prepare staged recommendations, but it does not promote, schedule, or authorize itself.

**Control-plane registration:** `swarm.json` (layer metadata only)
**Live staging/output surface:** `!/CREWAI/`
**Historical harbor records:** `!/CREWAI/HANDOFF-CREWAI-OPS.md`, `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md`, and `!/GRIMOIRE/HANDOFF-CREWAI-IGNITION-2026-04-04.md`

---

## Layer Boundaries

| Surface | Role | Authority |
| --- | --- | --- |
| `swarm.json` | Cross-agent registration of the CrewAI layer | Durable control-plane facts only |
| `.crewai/MANIFEST.md` | Live doctrine, topology, and promotion rules | Current CrewAI truth |
| `!/CREWAI/` | Staged output surface | On-record output; not canonical by default |
| Historical harbor docs | Thought-history and superseded reasoning | Archive only |

---

## Layered Model

| Layer | Meaning | Writable by | Promotion rule |
| --- | --- | --- | --- |
| `CANON` | Durable promoted authority in the vault | Logan or explicitly approved promotion paths | Canon changes require Logan approval |
| `DRIVE` | Active working surface for code, configuration, and human edits | Logan and assigned agents | Working changes become durable only when committed and promoted |
| `RUNTIME` | Disposable CrewAI execution slice | Local or remote runners | Runtime artifacts do not self-promote |
| `ARCHIVE` | Preserved historical memory | Human-curated archival work | Historical pages inform doctrine but do not overrule it |

The laptop is not the vault. Portable authority matters more than any single machine, path, or runtime container.

---

## Current State

| Key | Value |
| --- | --- |
| Package | `crewai[anthropic,tools]>=1.14.1` |
| Python environment | `.venv/` (repo-local and uv-managed) |
| Canonical dependency graph | `uv.lock` |
| Registered crew | `idaho_vault.crew.FiveWizardsCouncil` |
| Training posture | Registered and runnable; not training-ready |
| Output staging | `!/CREWAI/` |
| Runtime class | Vault-contained local runtime slice via `src/idaho_vault/runtime.py` |
| Promotion gate | Logan approval is required before staged output enters canon |

The package entrypoint calls `configure_vault_runtime()` before CrewAI starts. It redirects home, app-data, temporary, cache, and state directories into vault-local runtime surfaces so an inquiry run does not silently use shared user-level paths.

---

## Dependency and Update Model

`pyproject.toml` declares direct Python requirements, `uv.lock` is the canonical resolved dependency graph, and `requirements.txt` is a generated pip-compatible export rather than an independently managed lockfile. The dependency workflow refreshes the lock with `uv lock --upgrade`, exports `requirements.txt`, and opens a review PR for a resulting change.

Dependabot proposes GitHub Actions and Git submodule pin updates every second Thursday at 12:00 America/Denver. A submodule proposal advances only its gitlink; it does not modify a vendored snapshot or its provenance record. Every proposal remains subject to review and promotion boundaries.

---

## Live Topology

### Registered crew

| Crew | Path | Purpose | Status |
| --- | --- | --- | --- |
| `FiveWizardsCouncil` | `src/idaho_vault/crew.py` | Run a finite six-question inquiry that produces evidence-qualified lane packets and a staged synthesis recommendation. | Registered and runnable; not training-ready |

### Agent and task surfaces

| Office | Agent configuration | Direct task | Product |
| --- | --- | --- | --- |
| `WHO` | `who_wizard` | `who_inquiry_task` | Identity ledger |
| `WHAT` | `what_wizard` | `what_inquiry_task` | Artifact/event ledger |
| `WHEN` | `when_wizard` | `when_inquiry_task` | Timeline |
| `WHERE` | `where_wizard` | `where_inquiry_task` | Location/jurisdiction map |
| `WHY` | `why_wizard` | `why_inquiry_task` | Rationale ledger |
| `HOW` | `how_wizard` | `council_synthesis_task` | Bounded staged recommendation |

Each task has a named owner in `src/idaho_vault/config/tasks.yaml`. The crew runs sequentially so the HOW synthesis can review the five recorded lane packets. It may preserve disagreement and recommend a disposition; it cannot declare output canonical, broaden its source set, or trigger another run.

### Supported runners

| Runner | Invocation | Purpose | Status |
| --- | --- | --- | --- |
| Package entrypoint | `uv run idaho-vault` | Run one council inquiry through the vault-contained Python entrypoint | Active |
| Module entrypoint | `uv run python -m idaho_vault.main` | Run the same council inquiry directly | Active |
| Vault launcher | `powershell -ExecutionPolicy Bypass -File .\scripts\Start-CrewAIVault.ps1` | Invoke CrewAI through the vault-local PowerShell environment helper | Active |

### Writable and ephemeral surfaces

| Surface | Purpose | Persistence |
| --- | --- | --- |
| `.crewai/` | CrewAI registry, manifests, and training surfaces | Durable in git |
| `src/idaho_vault/` | Council implementation and runtime containment code | Durable in git |
| `!/CREWAI/` | Staged CrewAI outputs | Durable in git; not canonical by default |
| `.crewai/logs/`, `.crewai_cache/` | Execution logs and cache | Ephemeral / gitignored |
| `.venv/` | Local Python environment | Ephemeral / local runtime |
| `.agent-home/crewai/`, `.cache/`, `.state/`, `.tmp/` | Vault-local runtime state | Ephemeral / local runtime |

---

## Promotion Rules

1. CrewAI may write only staged outputs to `!/CREWAI/`.
2. Staged outputs are on-record but are not canonical by default.
3. Promotion from `!/CREWAI/` into canon requires Logan approval.
4. Runtime caches, logs, and secret-bearing material never self-promote.
5. `swarm.json` registers the CrewAI layer, but crew, task, and runner topology lives here.
6. A registered crew may be runnable without being training-ready.
7. A council recommendation does not create authority for a further run, new office, or canonical change.

---

## Durable Doctrines

- Portable authority over local romance.
- Remote-first vault with a contained local runtime slice.
- Clear separation of `CANON`, `DRIVE`, `RUNTIME`, and `ARCHIVE`.
- Promotion rules matter more than storage format.
- Historical reasoning can illuminate doctrine without becoming doctrine.
- Finite, externally wound execution over self-perpetuating workflow.

---

## What Remains From the Scaffold

- `.crewai/__init__.py`
- `.crewai/manifest.json`
- `.crewai/crews/__init__.py`
- `.crewai/tools/__init__.py`
- `src/idaho_vault/bootstrap_contract.py` as a historical compatibility utility, not a declaration of active topology

These files preserve package boundaries and historical validation material while the live Python implementation resides in `src/idaho_vault/`.

## What Was Retired

- The mock-LLM bootstrap-validation crew as live topology
- Threshold, civic-scaffold, and deterministic five-wizard runners
- JFAC-specific runner code
- Speculative crawler/linker crew definitions
- Demo-only tool wrappers

Any future crew, tool, or runner must be registered here before it counts as live topology.
