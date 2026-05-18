---
title: "DRAFT Proposal - Multi-Pronged Tool-Usecase-Intersection Analysis"
date created: 2026-04-17
authority: codex
doc_class: proposal
status: draft
related:
  - IDAHO-VAULT
  - "!/AGENTS.md"
  - "!/PLUGIN-REGISTRY.md"
  - ".crewai/MANIFEST.md"
  - "swarm.json"
  - "pyproject.toml"
  - "!/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md"
  - "!/STUDIO-PACKET-SYNTHESIS-CIVIC-FANTASY-2026-04-17.md"
  - "src/idaho_vault/five_wizards/workflow.py"
---

# DRAFT Proposal - Multi-Pronged Tool-Usecase-Intersection Analysis

*Filed 2026-04-17 for Logan's review. Draft only. Not live doctrine.*

## Summary

The vault now has enough tool surface area that ad hoc reasoning is starting to
fail.

There are too many overlapping capabilities across:

- local Python machinery
- CrewAI
- connectors
- plugins
- MCP/tool surfaces
- shell scripts
- note-based protocol systems

The next useful analysis is not "what tools exist" in the abstract.
It is:

which tool classes intersect with which real use cases, under which
constraints, and with what authority cost.

## Proposed Goal

Build one compact analysis framework that can answer:

1. what a use case actually needs
2. which tool layers can satisfy it
3. where tool overlap is healthy versus redundant
4. where the vault lacks a lawful implementation path
5. which layer should be treated as canonical for each recurring kind of work

The aim is not to maximize optionality.
The aim is to reduce accidental framework multiplication.

## Proposed Analysis Axes

The analysis should read each candidate surface across multiple intersecting
axes.

### 1. Use case axis

Examples:

- root-first orientation
- source-note refinement
- exploratory companion writing
- staged report generation
- GitHub transport and PR work
- Linear state handling
- inbox or intake triage
- workflow orchestration
- threshold or standing checks
- local automation and batch scans

### 2. Tool-family axis

Examples:

- pure Python in `src/idaho_vault/`
- CrewAI crews and flows
- connector-native actions
- plugin-layer affordances
- shell or PowerShell utilities
- note-native or Obsidian-native surfaces
- future orchestration adapters such as LangGraph or OpenAI Agents SDK

### 3. Authority axis

For each intersection, ask:

- is this layer live doctrine
- staging only
- runtime only
- archive only
- external read surface
- external write surface

### 4. Outcome axis

For each intersection, ask what the tool actually produces:

- note
- staged artifact
- runtime effect
- GitHub transport event
- state update
- classification result
- recommendation only

### 5. Cost and risk axis

For each intersection, ask:

- setup cost
- runtime fragility
- reviewability
- portability
- hidden state
- promotion risk
- overreach risk

## Proposed Output Shape

The analysis should eventually yield four compact products.

### 1. Capability matrix

A simple crosswalk of:

`use case x tool family x authority posture`

This should show preferred, allowed, discouraged, and out-of-jurisdiction
combinations.

### 2. Canonical-lane recommendations

For each recurring use case, name one preferred implementation lane.

Example shape:

- GitHub transport -> connector lane
- staged workflow reports -> pure Python core + `!/CREWAI/`
- note companions -> note-native vault lane

### 3. Gap list

Identify use cases that currently have:

- no stable lane
- too many competing lanes
- a lane that exists only in theory

### 4. Retirement candidates

Identify tools or surfaces that are:

- redundant
- aspirational only
- historically interesting but non-live
- adding confusion without completing a real route

## Recommended First Pass

Keep the first analysis deliberately narrow.

Start with one bounded slice across the most relevant active systems:

- pure Python `5Wizards`
- CrewAI bootstrap and staging
- GitHub connector/transport lane
- Linear execution-state lane
- note-native root and `!/` documentation surfaces

Do not begin by trying to model every plugin, connector, and speculative future
framework at once.

## Initial Working Rule

When multiple tool layers can perform the same task, prefer the one that is:

1. already live
2. most reviewable
3. least stateful in hidden ways
4. closest to the vault's current source of truth

That rule should be treated as the default tie-breaker until the analysis says
otherwise.

## Why This Matters

Right now the vault risks acquiring:

- too many orchestration metaphysics
- too many overlapping transport layers
- too many tools with unclear jurisdiction

The result is not abundance.
It is ambiguous standing.

A tool-usecase-intersection analysis would make the system more lawful by
showing not just what can be done, but what should be done where.

## Recommendation

Adopt this as a draft analysis initiative.

Do not implement tooling changes from it yet.

First produce the matrix, the preferred lanes, the gaps, and the retirement
suspects. Then decide which overlaps are healthy, which ones are merely
romantic, and which ones should be buried.
