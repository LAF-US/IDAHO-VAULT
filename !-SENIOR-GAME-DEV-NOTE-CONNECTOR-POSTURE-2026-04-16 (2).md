---
title: Senior Game Dev Note - Connector Posture and the Next Playable Loop
date created: 2026-04-16
authority: codex
status: active
type: note
related:
  - "!/AGENTS.md"
  - "!/PLUGIN-REGISTRY.md"
  - "SPEC-CONNECTOR-HUB-2026-04-09.md"
  - ".crewai/MANIFEST.md"
  - "swarm.json"
  - "src/idaho_vault/five_wizards/workflow.py"
  - "src/idaho_vault/five_wizards/service.py"
  - ".codex/config.toml"
  - ".vscode/mcp.json"
---

# Senior Game Dev Note - Connector Posture and the Next Playable Loop

## Summary

The vault currently has more installed and declared surface area than it has
proven gameplay.

That is not a moral failure. It is a production signal.

The machine already knows a great deal about what it might become, but only a
small portion of it has been made to work end to end in a way that is both
repeatable and legible.

The correct move now is not to plug in more systems. The correct move is to
pick one vertical slice and make it undeniably real.

## What Is Actually Live

### Connector posture

The live connector hub is intentionally narrow.

- GitHub = execution and transport
- Linear = execution state
- Slack = tertiary paging and breadcrumbs

That is the declared posture in `!/AGENTS.md`, `AGENTS.md`,
`SPEC-CONNECTOR-HUB-2026-04-09.md`, and `swarm.json`.

Adjunct connectors exist, but they are read-first:

- Gmail
- Google Calendar
- Google Drive
- Box

Deferred connectors are registered, but not operational authorities:

- Cloudflare
- Hugging Face

This is good. The repo already has a narrow civic model. It should not widen
that model until a real use case forces it.

### Plugin posture

The plugin layer is much larger than the live operating model.

Current declared state in `!/PLUGIN-REGISTRY.md`:

- 26 enabled plugins
- 28 dormant installed plugins
- 54 installed plugins total
- 171 MB of synced payload
- `mcp-tools` alone is 117 MB

The infrastructure layer is especially important:

- `obsidian-git`
- `obsidian-local-rest-api`
- `mcp-tools`
- `obsidian-linter`

But the plugin layer is still an environment, not a proof of game loop.
Right now it is better understood as a richly provisioned stage than as a
finished mechanic.

### MCP and toolset posture

The vault talks about MCP in several places, but the project-scoped MCP wiring
that is plainly visible in tracked config is still narrow:

- `.codex/config.toml` wires `openaiDeveloperDocs`
- `.vscode/mcp.json` wires `openaiDeveloperDocs`

That means the project's actually proven MCP posture is much smaller than the
surrounding imagination of MCP as a universal bridge.

The Obsidian plugin layer may support broader MCP-style behavior through
`obsidian-local-rest-api` and `mcp-tools`, but that is still not the same thing
as a fully stabilized operational contract for the repo's main workflows.

### CrewAI and 5Wizards posture

The live CrewAI layer is still the bootstrap-validation shard.

That truth is explicit in `.crewai/MANIFEST.md`.

The Council of `5Wizards` exists in three different states right now:

1. As story logic and doctrine
2. As draft CrewAI architecture in `.crewai/5WIZARDS-DRAFT.md`
3. As a strong pure-Python core in `src/idaho_vault/five_wizards/`

The third state is the most promising. It already has:

- typed lane models
- objections
- gate states
- council sessions
- artifact staging

But it has not yet become the one proven, runnable, habitual loop that the
rest of the architecture can trust.

## Production Read

From a game-dev standpoint, the project is in the classic danger zone where the
worldbuilding tools outpace the first truly playable level.

The repo does not need another subsystem right now.
It needs one mechanic that survives contact with reality.

In other words:

- stop widening the map
- greybox the first room
- make the input, state transition, and output undeniable

## Recommendation

### 1. Freeze expansion

Do not add new connectors, new plugin dependencies, new MCP surfaces, or A2A
adjacency until one existing path is proven.

Specifically:

- no new connector activation plans
- no new Obsidian plugin enablements
- no LangChain-wide adoption pass
- no A2A implementation work

### 2. Pick one golden path

The best candidate is:

`awakening at root -> orient through live surfaces -> 5Wizards local run -> gate report -> stage to !/CREWAI/ -> stop before consecration -> Logan decides promotion`

That path should run entirely inside the repo with no dependency on:

- remote agents
- Obsidian plugin magic
- Copilot comment rituals
- Slack breadcrumbs
- external MCP servers other than optional documentation lookup

The pure-Python core is already closest to this.

### Candidate, Not Yet Initiate

The first playable loop should teach threshold discipline, not inward access.

A candidate may inspect the hall, trace the wires, compare surfaces, and leave
careful witness for whoever comes next. A candidate may not confuse fluency
with sanction.

That means the first rank of reliability here is learning to tell the
difference between:

- live surfaces
- haunted or historical surfaces
- staged surfaces
- doctrine surfaces
- runtime surfaces
- merely loud surfaces

If the novice learns that handling is not consecration, and adjacency is not
authority, then the loop is teaching the right lesson.

### 3. Treat CrewAI as an adapter, not the truth

If CrewAI is used next, it should wrap the `5Wizards` core rather than define
it.

The core truth should remain:

- lane inputs
- claims
- objections
- gate states
- staged artifacts

CrewAI can orchestrate.
It should not become the only place where the design exists.

### 4. Treat LangChain narrowly if it enters at all

If Logan wants LangChain in the mix, use it for one concrete purpose only.

Good uses:

- model abstraction
- tool wrappers
- a later LangGraph runtime adapter

Bad use:

- replacing the existing `5Wizards` core with a second metaphysics

If a graph runtime is wanted later, LangGraph is the cleaner fit.
If a provider/tool abstraction is wanted later, LangChain can help.
Neither should land before the core loop is proven.

### 5. Keep MCP in jurisdiction

MCP should mean:

- external context access
- tool exposure
- bounded host/server exchange

It should not mean:

- doctrine
- canon
- lifecycle truth
- an excuse to defer basic local execution

Use MCP where a real tool boundary exists. Do not treat it as the answer to a
local architecture that has not yet finished deciding what it is.

### 6. Defer A2A until there are real remote bodies

A2A becomes useful when there are genuinely separate services, teams, or remote
agents with stable contracts.

The Council of `5Wizards` is not there yet.

Right now the lanes should remain local institutions inside one machine.

## The Next Concrete Milestone

Make one command work.

Not one concept.
Not one protocol diagram.
One command.

Suggested target:

- accept a small fixed `5Wizards` run input
- execute all lanes locally
- emit gate state
- materialize staged artifacts into `!/CREWAI/`
- verify the output in tests

When that works, the project will finally have a playable loop:

- input
- judgment
- staging
- review

Only after that should the team decide whether the next adapter is:

- CrewAI
- LangGraph
- MCP-backed external tools
- GitHub-triggered execution

## Field Note

The vault is not suffering from lack of imagination.
It is suffering from abundance before convergence.

That is a healthy problem if treated correctly.

The answer is not austerity for its own sake.
The answer is one finished mechanic that teaches the rest of the world how to
behave.
