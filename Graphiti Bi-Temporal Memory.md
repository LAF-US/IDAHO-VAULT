---
title: "Graphiti Bi-Temporal Memory"
date created: 2026-07-04
authority: "LOGAN (recorded; atomized by a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: reference-note
status: draft
related:
  - "[[!-RESEARCH-CONVERGENT-INSTITUTIONS-2026-07-04]]"
  - "[[!-REPORT-MECHANIC-HOME-TRANSFER-2026-07-04]]"
  - "[[Ostrom Design Principles]]"
  - "[[Electronic Institutions]]"
  - "[[TimeStorm]]"
tags: [reference-note, atomized, agent-memory, temporal-knowledge-graph, zep, graphiti]
---

# Graphiti Bi-Temporal Memory (Zep)

*An atomized source note — the system in its own field's terms (applied ML
infrastructure, 2024–26). Vault mapping lives in
[[!-RESEARCH-CONVERGENT-INSTITUTIONS-2026-07-04]], deliberately not here.*

The problem, as the builders state it: LLMs are stateless and context windows are
finite, so "memory" done naively — dumping transcripts into a vector store and
retrieving by similarity — degrades as facts change: the store accumulates
contradictions with no model of *when anything was true*.

Their answer: a **temporal knowledge graph** as the memory substrate.

**Graphiti** (the open-source engine, Apache-2.0, Neo4j-backed) ingests
**episodes** — messages, documents, JSON — and extracts **entities** and **facts**
(graph edges) from them. The differentiator is **bi-temporal stamping**: every fact
carries validity time (`valid_at` / `invalid_at` — when it was true in the world)
*and* transaction time (when the system learned it). Contradictions are handled by
**edge invalidation**: a new conflicting fact does not delete the old one; it closes
the old fact's validity interval. "What was true on date X" remains a queryable
question, and the history stays auditable.

Retrieval is **hybrid** — semantic embeddings, BM25 keyword search, and graph
traversal, fused — with **no LLM in the read path**, which is how the vendor claims
sub-200 ms lookups at scale.

**Zep** is the managed platform built on Graphiti: per-user temporal context graphs
from which a compact "Context Block" (summary + most-relevant facts with their date
ranges) is assembled into each prompt turn.

Peer architectures for orientation, in the field's own comparison: **Mem0** — a
drop-in extract-at-write fact layer (vector-first, fastest adoption); **Letta**
(MemGPT lineage) — a stateful agent runtime where memory tiers are managed by the
agent itself, with a Jan-2026 Conversations API for shared memory across parallel
agents.

In their own terms: **memory is a data-engineering problem** — model change over
time explicitly, keep provenance, and treat retrieval as indexed query, not
generation.

## Provenance

Vendor docs and 2026 comparison literature fetched 2026-07-04 (getzep.com guide;
production memory-framework comparisons covering Letta/mem0/Zep/Graphiti). Neo4j
substrate and Apache-2.0 licensing per those sources.

###### [["The world is quiet here."]]
