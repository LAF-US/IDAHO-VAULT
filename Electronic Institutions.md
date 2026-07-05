---
title: "Electronic Institutions"
date created: 2026-07-04
authority: "LOGAN (recorded; atomized by a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: reference-note
status: draft
related:
  - "[[!-RESEARCH-CONVERGENT-INSTITUTIONS-2026-07-04]]"
  - "[[Ostrom Design Principles]]"
  - "[[TimeStorm]]"
  - "[[Graphiti Bi-Temporal Memory]]"
tags: [reference-note, atomized, multi-agent-systems, e-institutions, norms, deontic]
---

# Electronic Institutions

*An atomized source note — the concept in its own field's terms (distributed AI /
multi-agent systems; IIIA-CSIC Barcelona, ~1997–2010: Noriega, Sierra,
Rodríguez-Aguilar, Esteva; with Vázquez-Salceda and Dignum). Vault mapping lives in
[[!-RESEARCH-CONVERGENT-INSTITUTIONS-2026-07-04]], deliberately not here.*

The problem, in their terms: **open multi-agent systems** — software agents written
by different parties, heterogeneous and self-interested, interacting in a shared
environment (the founding testbed was a computerized fish-market auction). The
agents' internals cannot be inspected or controlled, so how do you guarantee their
*interactions* stay lawful?

Their answer: mirror what human institutions do — make "the rules of the game"
explicit and enforceable. An **electronic institution** is a formal,
machine-executable specification consisting of:

- a **dialogical framework** — the shared vocabulary; all institutional action is a
  **speech act**;
- a **performative structure** — interaction divided into **scenes**,
  protocol-governed spaces that agents move between while adopting **roles**;
- **normative rules** in deontic terms — permissions, prohibitions, obligations —
  where uttering certain speech acts creates binding **commitments** the
  institution warrants.

Enforcement is infrastructural, not voluntary: *governor* middleware mediates every
message, so an illegal utterance simply cannot be made; norm engines detect
violations and apply sanctions (in one canonical design, a dedicated **Police
Agent**). Tooling: ISLANDER (graphical specification language), AMELI (runtime
middleware).

The school's thesis, in its own terms: for open agent societies, **regulate the
interaction, not the agent** — descriptively (conventions made explicit to
participants) and prescriptively (compliance warranted by the runtime).

## Provenance

Fetched abstracts 2026-07-04: García-Camino, Noriega & Rodríguez-Aguilar,
*Implementing Norms in Electronic Institutions* (AAMAS'05); Vázquez-Salceda, *The
Role of Norms and Electronic Institutions in MAS* (2004); Arcos, Esteva, Noriega,
Rodríguez-Aguilar & Sierra, *Engineering Open Environments with Electronic
Institutions* (EAAI 2005). Tooling names and the fish-market lineage are standing
literature knowledge.

###### [["The world is quiet here."]]
