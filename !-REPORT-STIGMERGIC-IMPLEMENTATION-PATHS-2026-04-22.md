---
title: "Report - Stigmergic Implementation Paths"
date created: 2026-04-22
authority: copilot
doc_class: report
status: active
related:
  - "scripts/vault-pheromones.py"
  - "!/sbp-blackboard.json"
  - "!/sbp-field.db"
  - "AGENTS.md"
  - "VAULT-CONVENTIONS.md"
  - "CONSTITUTION.md"
  - "SWARM.md"
  - "src/idaho_vault/civic_scaffold.py"
  - "src/idaho_vault/five_wizards/threshold_runner.py"
  - "MISTRAL.md"
  - "OpenAI Swarm.md"
  - "PROTOCOL.md"
  - "LEVELSET.md"
  - "ORIENT-v0.1.md"
---

# Report - Stigmergic Implementation Paths

## Scope

This report records the comparative read of several external stigmergy-adjacent
systems and translates that read into concrete implementation paths for
`IDAHO-VAULT`.

The question is not whether the external projects are impressive.
The question is which underlying patterns are actually load-bearing here.

## Systems Reviewed

- `PheroPath`
- `Termite Protocol`
- `markspace`
- `pressure-field-experiment`
- `claw-swarm`
- `autonomous-agents`

## Executive Read

The strongest near-term path is not to copy a full swarm operating system.

The strongest near-term path is:

1. adopt a **Termite-style live coordination field**
2. adopt a **markspace-style external guard layer**
3. borrow a **light PheroPath-style file scent layer**
4. add **pressure / decay logic** only after the first three are stable

That gives the vault a real stigmergic substrate without overbuilding.

## Protocol Integration

The stigmergy field is not separate from the vault's protocol stack - it serves as the live backend for the Constitution's protocol system (Section III).

| Protocol (CONSTITUTION.md) | Stigmergy Hook | Implementation |
|----------------------------|----------------|---------------|
| AWAKEN v0.0 | `arrive` | Agent registration on wake |
| ORIENT v0.1 | `brief` | Field briefing at startup |
| HANDSHAKE | `arrive` + `claim` | Triune sync preparation |
| CONTEXT v0.0 | `emit`/`sniff` | State broadcast across sessions |
| HANDOFF | `brief` | Context package for handoff |
| FLAG | `guard` | Boundary enforcement before action |
| RISE v0.0 | `claim` | Trail graduation |
| TERMINATE | `depart` | Session close, status update |

The field makes these protocols **machine-readable and cross-session persistent** - not just chat-based prompts but observable, queryable state.

## Core Pattern By Project

### 1. `PheroPath`

`PheroPath` is most useful here as a reminder that coordination traces do not
need to live inside the prompt and do not always need to live inside the file
body.

Its strongest contribution is:

- file-attached or path-attached local traces
- typed signals such as warning, todo, insight, danger
- lightweight environmental memory that follows the artifact itself

That is valuable for a vault built from notes, scripts, and chambers.

### 2. `Termite Protocol`

`Termite Protocol` is the strongest fit for immediate architectural use.

Its strongest contribution is:

- environment-first coordination
- SQLite-backed shared state
- atomic claims
- computed arrival / birth snapshot
- cross-session continuity without relying on chat history

This aligns closely with the current blackboard direction and with the vault's
need to survive context resets cleanly.

### 3. `markspace`

`markspace` is the strongest fit for the safety and workflow side.

Its strongest contribution is:

- coordination guarantees that do not depend on LLM obedience
- identity and scope enforced outside the model
- trust weighting
- conflict policy
- temporal decay for stale signals

This maps directly onto existing repo pain:

- secret-backed side effects
- PR and branch trust boundaries
- workflow gates
- chamber access and authority surfaces

### 4. `pressure-field-experiment`

This project matters less as a full product model and more as a design lesson.

Its strongest contribution is:

- local action plus shared artifact
- pressure rather than explicit command
- decay so stale observations stop dominating the field

This is especially useful for triage, ranking, and re-prioritization.

### 5. `claw-swarm`

`claw-swarm` is conceptually aligned but operationally too large for immediate
adoption.

Its strongest contribution is not its exact implementation.
Its strongest contribution is proof that field-mediated coordination can be made
systemic across many subsystems.

For `IDAHO-VAULT`, it should be treated as an upper-bound inspiration, not a
copy target.

### 6. `autonomous-agents`

This is useful as a low-complexity fallback model.

Its strongest contribution is:

- Git as distributed mutex
- shared files as coordination lane
- no message bus requirement

That model is simpler than the others, but it is weaker than SQLite for live
state, claims, and fine-grained signal history.

## Recommended Architecture For IDAHO-VAULT

The likely stable architecture is:

- **vault files** as durable readable memory
- **SQLite field** as live coordination state
- **arrival snapshot** as low-token startup orientation
- **guard layer** as deterministic trust and scope enforcement
- **optional file pheromones** as artifact-local hints

In other words:

The vault should remain the record.
The field should become the live coordination medium.

## Immediate Implementation Paths

### Path A - Blackboard Plus

Keep `!/sbp-blackboard.json`, but add:

- typed marks
- explicit owner / claim state
- TTL
- stale signal expiry
- basic event sniffing

This is the smallest change and the weakest long-term substrate.

### Path B - SQLite Field

Replace the single-file board with a SQLite-backed field.

Add operations like:

- `arrive`
- `claim`
- `deposit`
- `pulse`
- `decay`
- `need-human`

This is the best next step if the goal is durable cross-session swarm behavior.

### Path C - Guarded Coordination Layer

Add a deterministic boundary around sensitive actions:

- workflow-triggered side effects
- PR automation
- branch trust
- secret-backed sync
- chamber write scope

This is the best answer to the repo's current failstates.

### Path D - Pressure Routing

Score tasks and surfaces by dimensions such as:

- urgency
- risk
- confidence
- ownership
- staleness

Then let decay lower the weight of old unresolved observations.

This should come after SQLite and guard semantics exist.

## Recommended Order

The most truthful sequence is:

1. stabilize the current blackboard work into a real field substrate
2. move that substrate to SQLite
3. generate a compact arrival snapshot for new sessions
4. enforce trust and scope outside the model
5. add decay and pressure-based routing
6. only then consider richer field dimensions or larger swarm behavior

## Status Addendum - Current Freeze Point

The implementation forecast above is now partially fulfilled.

As of this writing:

- **Path A / Phase 1** is complete: the vault has a live blackboard substrate in
  `!/sbp-blackboard.json`
- **Path B / Phase 2** is complete: the field has moved to SQLite in
  `!/sbp-field.db`
- **Path C / Phase 3** is complete: guard semantics for capabilities and trust
  exist in `scripts/vault-pheromones.py`

The built system therefore already includes:

- field memory for pheromones, scents, and agents
- guard surfaces for capabilities and trust
- cross-session persistence through the SQLite field

What remains unfinished:

- **arrival snapshot** for compact startup orientation - DONE
- **decay / pressure routing** so old signals lose weight over time - DONE
- **route tracking** for entry, return, and adjudication
- **file pheromones / artifact-local traces**
- **civic bridge** connecting the field to standing and jurisdiction

This means the field and guard are no longer the primary unknowns.
The primary missing layer is now the lawful bridge between field activity and
the vault's civic institutions.

## Architectural Convergence

Subsequent review of the vault's constitutional and executable Python surfaces
sharpens the meaning of this work.

The constitutional tenet in play is explicit:

- the **journalistic 5W's guide all inquiry**

That matters because the `five_wizards` package is not merely an automation
helper. It is better read as a **Civic Institution** operationalizing that
constitutional inquiry mandate.

In that light:

- `src/idaho_vault/five_wizards/workflow.py` is institutional procedure
- `src/idaho_vault/five_wizards/threshold_runner.py` is lawful staging and
  return procedure
- `src/idaho_vault/civic_scaffold.py` is the jurisdictional world model
- `scripts/vault-pheromones.py` is the shared environmental memory substrate

The next major phase is therefore not "more swarm features."

It is the **civic bridge**:

- field -> standing
- field -> jurisdiction
- entry -> return -> adjudication

Until that bridge exists, the field can remember and guard, but it cannot yet
fully distinguish lawful action from merely recorded action.

## Recommended Pause Reading

The truthful freeze-point is:

- **Field built** (Path A, B, C, D complete)
- **Guard built** (capabilities, trust)
- **Arrival snapshot built** ("brief" command)
- **Pressure routing built** ("pressure", "prune" commands)
- **Protocol integration mapped** (field = live backend for Constitution Section III protocols)
- **Civic code present but separate**

### What the Field Does

The stigmergy field (`!/sbp-field.db` via `scripts/vault-pheromones.py`) provides:

- **Pheromones**: Typed signals (trail/ptype) with intensity and pressure scoring
- **Scents**: Trigger conditions that fire when thresholds met
- **Agents**: Registration, claims, departure tracking
- **Capabilities**: Scope-bound permissions (read/write/execute)
- **Trust**: Relationship tracking between agents

### What Remains

- route tracking for entry, return, adjudication
- file pheromones / artifact-local traces
- civic bridge integration (field -> standing/jurisdiction)

If work resumes, the safest next step is the civic bridge.

## What Should Not Happen

The vault should not jump directly to a grand 12-dimensional swarm framework
without first earning:

- durable live state
- lawful claims
- truthful startup
- deterministic guardrails

If those are missing, complexity will amplify drift instead of reducing it.

## Bottom Line

The best composite pattern is clear:

- **Termite Protocol** supplies the field substrate
- **markspace** supplies the guard logic
- **PheroPath** supplies artifact-local traces
- **pressure-field-experiment** supplies decay logic

`claw-swarm` remains a useful horizon, but not the next truthful build step.

The next real machine for `IDAHO-VAULT` is therefore not "more agents."

It is a smaller, stricter, more durable coordination medium that survives
context loss, enforces scope externally, and lets signals fade when the world
changes.
