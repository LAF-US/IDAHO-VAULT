---
title: "DRAFT Map - Tool Lanes for One Live Operator Loop"
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
---

# DRAFT Map - Tool Lanes for One Live Operator Loop

*Filed 2026-04-17 for Logan's review. Fresh draft only. Not live doctrine.*

## Purpose

This draft does not try to map every tool in the vault.

It maps one live operator loop and asks:

- what happens here
- which lane should handle it
- what other lanes may assist
- which lanes should not be driving

If this map is useful, it can later be widened.

## Operator Loop Under Test

This draft uses one concrete loop:

1. daily note or TODO intake
2. local classification or planning
3. staged artifact generation
4. GitHub transport only if needed
5. Logan review gate

## Axes

Every lane should be read on four separate axes.

### 1. Use case

What kind of work is being done right now.

### 2. Lifecycle posture

What kind of surface the work belongs to:

- `live`
- `staged`
- `runtime`
- `archive`

### 3. Permission boundary

What kind of reach the lane has:

- `local read`
- `local write`
- `external read`
- `external write`

### 4. Product shape

What comes out of the lane:

- note
- plan
- staged artifact
- state update
- transport event
- recommendation

## Label Rule

Each lane at each step should be marked as one of:

- `preferred`
- `allowed`
- `discouraged`
- `out-of-jurisdiction`

Use this decision rule:

- `preferred` = already live, directly matches the product shape, low hidden
  state, easy for Logan to review
- `allowed` = can do the work, but adds indirection or depends on another lane
- `discouraged` = technically possible, but introduces duplicate authority,
  unnecessary state, or framework sprawl
- `out-of-jurisdiction` = crosses a boundary this step does not authorize

## Lane Key

For this first map, use only these lanes:

- `vault-note lane` = root notes, `!/`, Obsidian-adjacent record surfaces
- `python-core lane` = pure Python in `src/idaho_vault/`
- `crewai lane` = CrewAI runtime, crews, flows, staged output
- `github lane` = GitHub connector and transport surfaces
- `linear lane` = execution-state and case-tracking surfaces
- `plugin lane` = Obsidian/plugin affordances that are present but not default

## Map

| Step | Goal | Lifecycle posture | Permission boundary | Product | Preferred | Allowed | Discouraged | Out-of-jurisdiction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Intake | Observe daily note / TODO state | `live` | `local read` | note context | `vault-note lane` | `python-core lane` | `crewai lane`, `plugin lane` | `github lane`, `linear lane` |
| 2. Classify / plan | Turn raw note state into scoped next action | `live` | `local read`, `local write` | plan or classification | `vault-note lane`, `python-core lane` | `linear lane` | `crewai lane`, `plugin lane` | `github lane` |
| 3. Stage artifact | Materialize a report, companion, or workflow pack | `staged` | `local write` | staged artifact | `python-core lane`, `vault-note lane` | `crewai lane` | `plugin lane` | `github lane`, `linear lane` |
| 4. Transport if needed | Move reviewed work toward PR or branch surface | `staged` -> `transport` | `external write` | transport event | `github lane` | `python-core lane` | `crewai lane`, `plugin lane` | `linear lane` |
| 5. Review gate | Hold for Logan judgment | `live` / `staged` boundary | `local read`, `external read` | decision context | `vault-note lane`, `github lane` | `linear lane` | `crewai lane`, `plugin lane` | any self-promoting lane |

## Fast Reads

### What this map already says

- Daily note and TODO intake are not a CrewAI-first problem.
- Planning should default to vault-note and python-core lanes.
- CrewAI is mainly a staging/runtime helper here, not the first classifier.
- GitHub should enter late, at transport time, not at intake time.
- Linear is useful for state and queue context, but not as the primary place
  where meaning is first formed.

### What this map is warning against

- using external-write lanes too early
- letting runtime layers define live meaning
- letting plugin affordances become silent authority
- letting every step become "agent orchestration" by habit

## Gaps Exposed By The Map

This one-loop map suggests three real follow-ups:

- a clearer local classification lane between note intake and staged output
- a stable rule for when planning remains a note versus when it becomes a
  staged artifact
- a narrower statement of where Linear enters the loop so it does not compete
  with note-native planning

## If This Draft Holds

The next widening pass should not be "all tools."

It should be one added loop at a time, such as:

- source-note refinement
- companion-note writing
- `5Wizards` threshold run
- inbox triage
- GitHub review response

## Field Rule

When in doubt, start with the lane closest to the live record and the fewest
hidden moving parts.

That is usually the right first map in this vault.
