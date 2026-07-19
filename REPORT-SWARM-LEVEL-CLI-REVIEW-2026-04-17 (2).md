---
title: "Report - Swarm-Level CLI Review"
date created: 2026-04-17
authority: codex
doc_class: report
status: active
related:
  - "pyproject.toml"
  - "src/idaho_vault/main.py"
  - "src/idaho_vault/bootstrap_contract.py"
  - "src/idaho_vault/five_wizards/threshold_runner.py"
  - "tests/test_threshold_runner.py"
  - "!/agent.sh"
  - "!/agents.json"
  - "agent.sh"
  - ".codex/config.toml"
  - ".vscode/mcp.json"
  - "!/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md"
---

# Report - Swarm-Level CLI Review

## Scope

This is a swarm-level review of the current CLI implementation surfaces and
their config seams.

The goal is not to inventory every script-shaped object in the vault.
The goal is to identify the live command surfaces that present themselves as
operator-facing or package-facing control points and to reduce them to one
truthful read.

## Active Flagged Pin In The 5Ws

### WHO

The current CLI surface is for already-oriented local operators inside a live
repo checkout.

It is not yet an honest general-purpose installed CLI for arbitrary
environments.

### WHAT

There are really three CLI families present:

- package entrypoints from `pyproject.toml`
- shell bootstrap surfaces around `!/agent.sh`
- editor or MCP-side config surfaces that shape tool access but are not the
  same thing as runtime commands

These are adjacent, but not identical.

### WHEN

The package scripts are usable now for local, checkout-bound work.

They are not yet normalized enough to be treated as a stable public command
contract outside that local repo posture.

### WHERE

The truthful execution boundary is the vault root.

Several commands assume:

- repo-local files
- live doctrine surfaces
- local staging paths
- tracked root structure

That means the commands are strongest when run from a real `IDAHO-VAULT`
checkout, not from a thin installed wheel.

### WHY

The current CLI layer overpromises portability.

The command suite is trying to do honest repo-local work, but the packaging
surface makes it look more general than it is.

That mismatch is the main CLI risk right now.

## Core Surfaces

### 1. Package entrypoints

`pyproject.toml` currently exports:

- `idaho_vault`
- `run_crew`
- `train`
- `replay`
- `test`
- `run_with_trigger`
- `five_wizards_threshold`

This is the main package-facing command surface.

### 2. Python CLI handler

`src/idaho_vault/main.py` is the live implementation hub behind those script
names.

It currently does four different jobs:

- bootstrap crew execution
- relaxed trigger payload parsing
- repo test discovery
- 5Wizards threshold staging

That is workable, but it means one file currently fronts multiple command
contracts with very different side-effect profiles.

### 3. Bootstrap shell layer

`!/agent.sh` is the canonical local bootstrap entrypoint.

The root `agent.sh` is a compatibility wrapper that delegates to the canonical
script so shell exports land in the current session.

This part of the CLI posture is actually fairly coherent.
It is explicitly repo-local and tells the truth about what it is.

### 4. MCP/editor config layer

`.codex/config.toml` and `.vscode/mcp.json` define a narrow MCP posture around
`openaiDeveloperDocs`.

These are important CLI-adjacent surfaces, but they are not interchangeable
with the command entrypoints above.

They shape the tool environment.
They are not themselves the operator CLI.

## Review Read

### Strengths

- The shell bootstrap surfaces are clearly repo-local and are documented that
  way.
- The 5Wizards threshold slice is materially real and tested at the logic
  level.
- The package entrypoint table is small enough to reason about.
- The MCP config posture is narrow and honest.

### Weaknesses

- the packaged command surface suggests more portability than the implementation
  truly supports
- `train` and `replay` are exported even though they intentionally terminate as
  unimplemented
- `test` claims installed-environment utility while relying on repo-local test
  discovery
- `five_wizards_threshold` defaults to write/materialize behavior without an
  explicit CLI posture for dry-run versus staging
- `main.py` has no direct command-level test coverage

## Current Triage

### Green

- `!/agent.sh`
- root `agent.sh` compatibility wrapper
- `.codex/config.toml`
- `.vscode/mcp.json`
- `five_wizards` internal workflow and threshold logic

These surfaces are narrow enough and truthful enough for their current office.

### Yellow

- `idaho_vault`
- `run_crew`
- `run_with_trigger`

These work best as local checkout commands, but their package posture should be
made more explicit.

### Yellow-Red

- `test`
- `five_wizards_threshold`

`test` is honest only in a checkout.
`five_wizards_threshold` is real, but the public command currently hardwires
materialization instead of exposing run posture.

### Red-In-Truthfulness, Not In Function

- `train`
- `replay`

These are not broken in the sense of crashing unpredictably.
They are misleading because they are exported as commands while intentionally
not existing as workflows.

## Big IFs

### BIG IF 1

The swarm-level CLI is not primarily broken.
It is primarily boundary-blurry.

### BIG IF 2

The shell bootstrap layer is more honest than the packaged Python CLI layer.

That is useful because it shows the project already knows how to tell the truth
about repo-local commands when it chooses to.

### BIG IF 3

`five_wizards_threshold` is the strongest real candidate for a future flagship
CLI surface, but only if its operator posture becomes explicit:

- dry-run
- materialize
- maybe later stage-root override

### BIG IF 4

The main risk is not missing metaphysics.
It is shipping repo-shaped commands behind package-shaped names.

## Recommended Next Move

Do not widen the CLI.
Narrow it and name it honestly.

Smallest good follow-up pass:

1. decide which package scripts are truly checkout-only
2. add explicit guardrails or wording for checkout-only commands
3. expose dry-run vs materialize for `five_wizards_threshold`
4. add direct tests for `main.py` command behavior
5. keep shell bootstrap and package CLI as separate surfaces in doctrine and
   code comments

## Bottom Line

This review should stand as an active flagged pin:

the current swarm-level CLI is a real local operator surface, but it is not yet
a fully honest public package CLI.

The clean path forward is not more commands.
It is better boundary truth.
