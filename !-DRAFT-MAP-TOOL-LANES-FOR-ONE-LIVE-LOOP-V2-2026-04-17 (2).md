---
title: "DRAFT Map v2 - Tool Lanes for One Live Operator Loop"
date created: 2026-04-17
authority: codex
doc_class: proposal
status: draft
related:
  - IDAHO-VAULT
  - "!/AGENTS.md"
  - "!/PLUGIN-REGISTRY.md"
  - ".crewai/MANIFEST.md"
  - "TO DO LIST.md"
  - "DAILY NOTE TEMPLATE.md"
  - "swarm.json"
  - "pyproject.toml"
  - "src/idaho_vault/five_wizards/workflow.py"
  - "!/DRAFT-PROPOSAL-TOOL-USECASE-INTERSECTION-ANALYSIS-2026-04-17.md"
  - "!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-2026-04-17.md"
---

# DRAFT Map v2 - Tool Lanes for One Live Operator Loop

*Filed 2026-04-17 for Logan's review. Draft only. Not live doctrine.*

## Purpose

This draft turns the earlier tool-usecase proposal into a narrower decision
instrument.

It maps one live operator loop and names:

- the driver lane for each step
- the supporting lanes that may assist
- the lanes that should be discouraged
- the lanes that are out of jurisdiction

The point is not to describe every possible tool path.
The point is to reduce improvisation.

## Operator Loop Under Test

This map uses one concrete loop:

1. daily note or TODO intake
2. local classification or planning
3. staged artifact generation
4. GitHub transport if needed
5. Logan review gate

## Closed Vocabularies

All rows in the map must use only these declared values.

### Lifecycle posture

- `live`
- `staged`
- `runtime`
- `archive`

### Permission boundary

- `local read`
- `local write`
- `external read`
- `external write`

### Product shape

- `note`
- `plan`
- `staged artifact`
- `state update`
- `transport event`
- `recommendation`

### Lane status

- `driver`
- `supporting`
- `discouraged`
- `out-of-jurisdiction`

## Lane Key

For this loop, use only these lane families:

- `vault-note lane` = root notes, `!/`, Obsidian-adjacent record surfaces
- `python-core lane` = pure Python in `src/idaho_vault/`
- `crewai lane` = CrewAI runtime, crews, flows, staged output
- `github lane` = GitHub connector and transport surfaces
- `linear lane` = execution-state and case-tracking surfaces
- `plugin lane` = Obsidian/plugin affordances that are present but not default

## Driver Rule

Each step gets exactly one `driver` lane.

Choose the driver by this order:

1. already live in current doctrine
2. directly matches the product shape
3. lowest hidden state
4. easiest for Logan to review
5. least likely to create duplicate authority

If two lanes still tie, prefer the one closest to the live record.

## Map

| Step | Goal | Lifecycle posture | Permission boundary | Product shape | Driver | Supporting | Discouraged | Out-of-jurisdiction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Intake | Observe daily note / TODO state | `live` | `local read` | `note` | `vault-note lane` | `python-core lane` | `crewai lane`, `plugin lane` | `github lane`, `linear lane` |
| 2. Classify / plan | Turn raw note state into scoped next action | `live` | `local write` | `plan` | `vault-note lane` | `python-core lane`, `linear lane` | `crewai lane`, `plugin lane` | `github lane` |
| 3. Stage artifact | Materialize a report, companion, or workflow pack | `staged` | `local write` | `staged artifact` | `python-core lane` | `vault-note lane`, `crewai lane` | `plugin lane` | `github lane`, `linear lane` |
| 4. Transport if needed | Move reviewed work toward branch or PR surface | `staged` | `external write` | `transport event` | `github lane` | `python-core lane` | `crewai lane`, `plugin lane` | `linear lane`, `vault-note lane` |
| 5. Review gate | Present the work for Logan judgment | `live` | `external read` | `recommendation` | `vault-note lane` | `github lane`, `linear lane` | `crewai lane`, `plugin lane` | `python-core lane` |

## Fast Reads

### What this map now decides

- intake begins in the vault-note lane
- planning stays in the vault-note lane unless a narrower local Python helper
  is truly needed
- staged artifact generation is owned by python-core
- GitHub enters only at transport time
- review returns to the note layer, with GitHub and Linear as supporting
  context rather than primary meaning-makers

### What remains intentionally secondary

- CrewAI can assist staging, but it does not drive intake or planning
- plugins may assist ergonomics, but they should not silently define authority
- Linear can support planning and review, but it does not own first
  classification in this loop

## Why This Version Is Better

Compared with the earlier proposal and first map:

- it uses split axes instead of collapsing posture and permission
- it keeps row values inside closed vocabularies
- it assigns one driver lane per step
- it leaves support lanes visible without letting them compete for control

That makes it much closer to something an agent can follow without inventing
jurisdiction on the fly.

## Next Use

If this shape holds, use the same exact template for one more live loop, such
as:

- source-note refinement
- companion-note writing
- inbox triage
- GitHub review response

Do not widen to "all tools" until at least two real loops have been mapped with
the same grammar.

## Field Rule

When in doubt, pick the lane closest to the live record that can complete the
step without creating hidden state or duplicate authority.
