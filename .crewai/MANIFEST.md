---
title: "CrewAI Python Layer Manifest"
date created: "2026-04-04"
authority: crewai
doc_class: manifest
---

# CrewAI Python Layer Manifest

This directory is reserved for a future CrewAI-backed Python layer, but the initial demo harbor was retired pending redesign.

**Upstream authority:** `swarm.json` (root)

---

## Current State

| Key | Value |
|---|---|
| Package | `crewai[tools,anthropic]>=1.12.0` |
| Python | 3.13+ |
| Environment | `.venv/` (repo-local) |
| Status | Scaffold only |
| Active runners | None |
| Active crews | None |
| Output staging | `!/CREWAI/` (reserved / historical) |

---

## What Remains

- `.crewai/__init__.py`
- `.crewai/manifest.json`
- `.crewai/crews/__init__.py`
- `.crewai/tools/__init__.py`

These files preserve the package boundary so a real implementation can be rebuilt without reintroducing the earlier demo assumptions.

---

## What Was Retired

- JFAC-specific runner code
- speculative crawler/linker crew definitions
- address-space proof-of-concept scripts
- demo-only tool wrappers

The reset keeps CrewAI available as a Python-layer option without pretending the earlier harbor is production-ready.
