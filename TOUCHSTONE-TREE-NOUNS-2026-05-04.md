---
title: "Touchstone Tree Noun Registry"
created: 2026-05-04
updated: 2026-05-04
status: active
authority: LOGAN
authors:
  - Codex
type: tree-noun-registry
machine_registry: TOUCHSTONE-TREE-NOUNS-2026-05-04.json
related:
  - "!README"
  - TOUCHSTONE-TREE-NOUNS-2026-05-04
  - NEST
  - SOUL
tags:
  - touchstone
  - tree
  - registry
  - anchors
---

# Touchstone Tree Noun Registry

This note is the human-readable review surface for the Touchstone Tree noun
standard. The machine-readable source of truth is
`TOUCHSTONE-TREE-NOUNS-2026-05-04.json`.

The Tree noun standard is separate from persona chamber standards. Tree noun
dotfolders such as `.core/`, `.soul/`, and `.nest/` are symbolic anchors. They
do not require `stub.txt` vacancy sentinels unless Logan explicitly turns one
into a persona chamber.

## Enforced Contract

Every noun in the JSON registry must have:

- a root anchor note: `NOUN.md`
- a dotfolder anchor note: `.noun/NOUN.md`

The dotfolder anchor points back to the root anchor. Existing canonical root
notes do not need reciprocal edits unless they are already being revised for
another reason.

## Registered Nouns

| Branch | Nouns |
| --- | --- |
| CORE: MIND | CORE, MIND, CONSTITUTION, CHARTER, CORPUS |
| PERIPHERY: BODY | PERIPHERY, BODY, PROTOCOLS, PROCEDURES, PREFERENCES |
| GHOST: SOUL | GHOST, SOUL, GUIDELINES, GUESTBOOK, GRIMOIRE |
| NEST | NEST |

## Path And Ontology

`NEST` is the registered Tree noun. `!/` is the operational body, path, and
implementation surface for the Nest.

`!` is not a registry noun. Keeping `!` out of the noun registry preserves the
distinction between syntax and ontology.

## Enforcement

The current validator is `.github/scripts/check_touchstone_tree_nouns.py`.

It reads the JSON registry, checks that each noun is uppercase path-safe text,
and verifies the root/dotfolder anchor pair exists. It does not parse
`!README.md` as the primary contract. A separate drift check can be added later
if the orientation text and JSON registry need automated comparison.
