---
authority: LOGAN
related:
  - swarm.json
  - AGENTS
  - CODEX
  - bootstrap
  - agent
  - scripts
  - GitHub
date created: Monday, April 13th 2026
date modified: Monday, April 13th 2026
status: exploratory companion
---

# Agent Bootstrap - Explorer Companion

This note accompanies the machinery that turns the vault's registry into a
usable local bootstrap chain.

Primary nearby source:

- `.github/scripts/generate_agents_bootstrap.py`

Primary downstream records:

- `swarm.json`
- `!/agents.json`
- `agents.json`
- `!/agent.sh`
- `agent.sh`

## Source Of Truth And Mirrors

The observed hierarchy is:

1. `swarm.json` is the machine-readable source of truth
2. `.github/scripts/generate_agents_bootstrap.py` renders bootstrap data from it
3. `!/agents.json` is the canonical generated bootstrap index
4. `agents.json` is a compatibility mirror kept byte-for-byte aligned
5. `!/agent.sh` is the canonical local bootstrap entrypoint
6. `agent.sh` is a root wrapper that sources the canonical entrypoint

This is not duplication by accident. It is compatibility by design.

## What The Generator Preserves

The generator lifts a smaller practical subset from `swarm.json`:

- invoke name
- instructions file
- git identity
- capability tier
- required and optional context
- control-plane role labels

It does not try to reproduce the entire vault cosmology. It extracts only what
the local bootstrap path needs.

## What The Canonical Bootstrap Does

`!/agent.sh` behaves like a shell-side interpreter for the generated index.

Observed responsibilities:

- resolve a Python 3 interpreter
- read agent records from `!/agents.json`
- export agent identity fields into the current shell
- provide describe and validation paths
- preserve shell-level behavior by being sourced rather than merely executed

The root `agent.sh` wrapper exists to keep older calls working while routing
them back to the canonical `!/agent.sh`.

## Field Note

This corridor reveals a careful vault habit: doctrine is large, but executable
truth is intentionally narrowed before use.

The registry may tell the full story. The bootstrap only carries what must
cross the threshold.
