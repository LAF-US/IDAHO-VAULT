---
title: CENSUS — Enumeration Doctrine of the Unified Swarm
date created: Wednesday, June 3rd 2026, 2:07:38 pm
authority: LOGAN
doc_class: doctrine
status: draft
related:
  - CHARTER
  - CONSTITUTION
  - "!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md"
  - "!/EMANATIONISM-PRINCIPLE-2026-05-18.md"
  - "!/PERSONAE-ENGINE-v1-2026-05-20.md"
  - "!/ADDRESS-GRAMMAR-v1-2026-05-22.md"
  - "!/AGENTS.md"
  - VAULT-CONVENTIONS
tags:
  - census
  - doctrine
  - enumeration
  - topology
  - tri-anchor
  - governance
date modified: Wednesday, June 3rd 2026, 2:18:11 pm
---

# CENSUS

## Census Within the Loganic Frame

Authority emanates from Logan outward through layers: doctrine, registry,
protocol, transport, runtime, agent, tool call, artifact.

The Enumeration Clause in [[CHARTER]] mandates a regular census. This doctrine
defines the mechanism.

### Why a Census

Emanation without inventory cannot be audited. If authority flows outward but
the surfaces at each layer are not counted, the flow cannot be verified. The
census is the accounting arm of emanation — a structural body count, performed
periodically, deterministically, per scope.

### What Is Counted

A census counts **bodies** — chambers, surfaces, top-level members of a scope.
It does not classify authority, assign offices, or adjudicate registry claims.
Those are [[CROSSFRAMING]] operations.

| Scope | What Is Counted |
|---|---|
| Nest (`!/`) | Collective routing surfaces, DOCKET entries, bootstrap files |
| Persona chambers (`.*/`) | Dotfolders with tri-anchor presence |
| Root | Top-level root folders (per `topology_census.py`'s `root.iterdir()` scan) |
| Git refs | Named branches, PR refs, orphan lineages (see [[ARCHIPELAGO]]) |

### The Tri-Anchor Status Matrix

Each persona chamber is assessed for three anchors per [[PERSONAE ENGINE]]:

1. **ENTITY-RUNTIME** — actual runtime/config payload, present only for
   software-imported chambers (per [[STUB-PERSONAFOLDERS-2026-05-03]]); a pure
   stub vessel carries no runtime and is marked instead by its `stub.txt`
   vacancy sentinel (`¿!?`)
2. **SELF-IDENTITY** — the chamber's canonical `<NAME>.md` anchor
   (`.<name>/<NAME>.md`, e.g. `.claude/CLAUDE.md`) with `[ ? ]` pattern
3. **ADDRESS** — inscribed only by Logan

A census row records: present / absent / malformed for each anchor. It does
not infer what the presence or absence means.

### Relation to CROSSFRAMING

CROSSFRAMING is a separate seam: closed enums, typed models, validators that
consume census output plus registry manifests. Census produces the substrate.
CROSSFRAMING produces the delta analysis.

---

## Seed

This document is a seed. It will grow into the full census mechanism:

- Schema definition for census output rows
- Per-scope enumeration procedures
- Output format (deterministic, timestamp-free)
- Integration with existing `topology_census.py` and `check_dotfolder_anchors.py`
- CI workflow definition

---

###### [["The world is quiet here."]]
