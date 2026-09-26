---
title: "CrewAI Python Layer Manifest"
date created: "2026-04-04"
date updated: "2026-08-13"
author: "Manus AI"
authority: crewai
doc_class: manifest
status: retired
phase: dependency-removal
---

# CrewAI Python Layer Manifest

> **Current disposition:** IDAHO-VAULT has no installed, registered, or runnable CrewAI runtime. The prior experimental Council and bootstrap surfaces were removed when CrewAI's mandatory ChromaDB dependency introduced an unpatched critical finding. This record preserves the decision boundary; it does not reserve a live authority or runner.

## Retired surfaces

| Surface | Former purpose | Current disposition |
| --- | --- | --- |
| `src/idaho_vault/crew.py` and `src/idaho_vault/main.py` | Bounded 5Wizards CrewAI inquiry entrypoint | Removed |
| `src/idaho_vault/config/` | CrewAI agent and task configuration | Removed |
| `src/idaho_vault/runtime.py` | CrewAI-local runtime path containment | Removed with runtime |
| `pyproject.toml` CrewAI dependency | Role/task orchestration package | Removed |
| `.crewai/manifest.json` | Machine-readable CrewAI registry | Retained as an empty retired registry |

## Governance boundary

The 5Wizards and Familiar concepts remain design material, not executable topology. They may inform a future evaluation of a dependency-safe orchestrator, but no framework, runner, agent role, or training regimen is active merely because historical design files remain in the vault.

Any future runtime must be introduced through a separately reviewed dependency decision, a bounded implementation, validation, and a fresh registration decision. No archived CrewAI material authorizes automatic reinstatement, output promotion, autonomous scheduling, or credential use.
