# 5Wizards Council — Historical CrewAI Design

> **Status:** Retired implementation note. This document records a CrewAI-based design explored on `manus/self-testing`; it does not describe an installed runtime, a registered crew, or an approved agent topology.

## Disposition

The experimental CrewAI implementation and its configuration surfaces were removed from the repository on 2026-08-13. CrewAI required ChromaDB, whose then-current supported versions carried an unpatched critical security finding. The removal applies to the package dependency, lockfile, compatibility export, council code, task configuration, and executable entrypoints.

| Historical component | Disposition |
| --- | --- |
| WHO, WHAT, WHEN, WHERE, WHY, and HOW Wizard roles | Retained as conceptual inquiry lanes only |
| Familiar roles | Draft design material only |
| CrewAI sequential council | Removed; no runner remains |
| Vault-local CrewAI runtime path configuration | Removed with the runtime |
| CrewAI task YAML | Removed |

## Architectural residue

The design’s useful non-framework claims remain available for future work: inquiries should be bounded, role responsibilities should be explicit, uncertainty should be preserved, and a synthesis should remain a staged recommendation rather than a self-authorizing decision. These claims do not select a replacement framework or authorize implementation work.

Any future orchestration proposal must begin with a new dependency and security review, identify a finite input and output boundary, define validation and failure handling, and be registered only after explicit approval. No command in this document is executable in the current repository.
