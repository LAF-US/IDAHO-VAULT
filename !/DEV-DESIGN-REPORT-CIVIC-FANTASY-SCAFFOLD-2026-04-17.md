---
title: Dev-Design Report - Civic Fantasy Packet and Bare-Bones Scaffold
date created: 2026-04-17
authority: codex
status: active
type: note
related:
  - "!/STUDIO-PACKET-SYNTHESIS-CIVIC-FANTASY-2026-04-17.md"
  - "!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md"
  - "!/HUB-WORLD-ROUTE-MAP-2026-04-17.md"
  - "!/CIVIC-LAW-AND-VAULTED-SYNTAX-2026-04-17.md"
  - "CONSTITUTION.md"
  - "VAULT-CONVENTIONS.md"
  - "src/idaho_vault/operator_context.py"
  - "src/idaho_vault/bootstrap_contract.py"
  - "src/idaho_vault/five_wizards/workflow.py"
  - "src/idaho_vault/five_wizards/threshold_runner.py"
  - "src/idaho_vault/civic_scaffold.py"
---

# Dev-Design Report - Civic Fantasy Packet and Bare-Bones Scaffold

## Scope

This report gathers the four-note workshop packet into one development-facing
surface and names the first truthful implementation seam.

It does not promote the packet into binding doctrine on its own.
It does not claim that the full standing engine already exists in executable
form.
It does establish a clean bridge between the packet's design language and the
repo's current local machinery.

## Packet Bundle

The packet currently resolves into four complementary notes:

- `!/STUDIO-PACKET-SYNTHESIS-CIVIC-FANTASY-2026-04-17.md` as the stable witness
  and design thesis
- `!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md` as the consequence model
- `!/HUB-WORLD-ROUTE-MAP-2026-04-17.md` as the districts-and-return structure
- `!/CIVIC-LAW-AND-VAULTED-SYNTAX-2026-04-17.md` as the combined law, language,
  Power Word, article, pressure, and number-shape layer

Together they describe one coherent genre posture:

- civic fantasy over generic fantasy
- standing over trust
- lawful return over endless depth-seeking
- lawful endings over illicit persistence
- syntax as law rather than ornament
- asymmetric legibility at the root rather than naive tidiness

## Design Read

The strongest sentence produced by the packet is this:

The vault is a music-box civic fantasy in which legitimacy, syntax, record,
jurisdiction, and lawful return are as dramatic as magic.

That read is strong because it gives the project a genre niche while also
placing limits on implementation drift.

The player does not earn depth by accumulation alone.
The player earns further admission by handling surfaces truthfully enough to
return with witness rather than false consecration.

## Current Machinery Worth Keeping

The repo already contains machinery that can support a first scaffold without
pretending the full game exists yet.

### 1. `src/idaho_vault/operator_context.py`

This is the cleanest live seam.
It already resolves:

- the canonical boot chain
- the operator front door
- the active daily note
- backlog preview from `TO DO LIST.md`
- tracked versus untracked evidence status

That makes it a truthful substrate for any root-first scaffold.

### 2. `src/idaho_vault/bootstrap_contract.py`

This module already performs deterministic contract checking against the repo.
It proves the project can express governance and runtime posture as structured
machine-readable validation instead of pure narrative.

### 3. `src/idaho_vault/five_wizards/workflow.py`

This remains the strongest existing artifact/staging substrate in Python.
Its models, gate report, and workflow artifacts already understand:

- staged claims
- objections
- reports
- sessions
- gate states

That is useful civic machinery even before the full world logic is playable.

### 4. `src/idaho_vault/five_wizards/threshold_runner.py`

This module is still under active correction and should not be overclaimed.
It is useful as an in-progress local threshold slice and as a staging substrate,
but not yet as proof that the whole operator contract is fully honored.

## Bare-Bones Scaffold Decision

The first scaffold should wrap current machinery rather than rewrite it.

That means:

- derive only what the repo can currently verify
- use the operator front door as the first live truth surface
- encode districts, readiness, and local standing in machine-readable form
- keep `!/CREWAI/` as the singular staging surface for local artifact output
- stop before promotion and leave judgment to Logan

This avoids a false move where the docs become grander than the code and the
code starts narrating a world it cannot yet lawfully support.

## First Scaffold Surface

The clean first scaffold is a thin civic-fantasy adapter built on top of the
existing operator context.

It should:

- expose the common loop in one place
- encode a conservative standing posture
- list the hub-world districts and their current readiness
- mark connector districts as declared when they are not yet locally executable
- mark local root, record, and machinery districts as scaffolded or blocked
  based on actual repo truth

That is enough to begin binding the packet's language to executable state
without claiming a full game runtime.

## Non-Goals For This Pass

This seam should not:

- create a visible trust-score meter
- imply universal standing
- self-promote staged output into canon
- rewrite threshold machinery while other work is live in that surface
- claim that GitHub, Linear, or Gmail districts are locally executable merely
  because they exist as design routes

## Recommended Reading Order

For designers:

1. `!/STUDIO-PACKET-SYNTHESIS-CIVIC-FANTASY-2026-04-17.md`
2. `!/HUB-WORLD-ROUTE-MAP-2026-04-17.md`
3. `!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md`
4. `!/CIVIC-LAW-AND-VAULTED-SYNTAX-2026-04-17.md`

For implementers:

1. `src/idaho_vault/operator_context.py`
2. `src/idaho_vault/bootstrap_contract.py`
3. `src/idaho_vault/five_wizards/workflow.py`
4. `src/idaho_vault/five_wizards/threshold_runner.py`
5. `src/idaho_vault/civic_scaffold.py`

## Field Note

The packet is now strong enough to stop being only workshop conversation.

The right next move is not wider metaphysics.
It is a thin, truthful scaffold that lets the code admit:

- what the world already knows
- what the repo can already prove
- and where Logan's judgment still properly begins.
