---
authority: LOGAN
related:
  - AGENT-RUNTIME
  - CLI
  - CODEX
  - scripts
  - agent
  - runtime
  - containment
date created: Monday, April 13th 2026
date modified: Monday, April 13th 2026
status: exploratory companion
---

# Agent Runtime - Explorer Companion

This note accompanies the local runtime containment surfaces in this directory:

- `AGENT-RUNTIME.md`
- `Use-VaultAgentEnv.ps1`
- `Start-CodexVault.ps1`
- `Start-ClaudeVault.ps1`
- `Start-GeminiVault.ps1`
- `Start-CrewAIVault.ps1`

## What This Machine Does

The launcher scripts in `scripts/` are intentionally thin. Their main purpose is
to send each agent through `Use-VaultAgentEnv.ps1`, which redirects temp,
cache, and home-like state into vault-local paths instead of letting those
artifacts spill into Logan's wider user profile.

In plain terms: this rig keeps the dust of invocation inside the temple.

## Observed Runtime Pattern

Shared paths are redirected into the vault:

- `.tmp/`
- `.uv-cache/`
- `.pip-cache/`
- `.npm-cache/`
- `.cache/`
- `.state/`
- `.pycache/`
- `.agent-home/`

Agent-specific behavior:

- `codex` sets `CODEX_HOME` under `.agent-home/codex/`
- `gemini` isolates both AppData and home paths under `.agent-home/gemini/`
- `crewai` isolates both AppData and home paths under `.agent-home/crewai/`
- `claude` gets vault-local temp and AppData paths by default, with optional
  full home isolation via `-IsolateHome`

## Distinction Worth Preserving

This runtime containment layer is not the same thing as the agent bootstrap
chain.

- Runtime containment lives here in `scripts/`
- Bootstrap identity and shell export logic live in `!/agent.sh`,
  `!/agents.json`, and the compatibility mirrors at repo root

Those two systems cooperate, but they solve different problems:

- containment decides where residue goes
- bootstrap decides who is being invoked and with what declared identity

## Field Note

The important mechanical insight here is restraint. The scripts do not try to
be the agents; they prepare a bounded room for the agents to enter.

That feels like a recurring vault value: keep authority clear, keep side
effects local, and let the invocation surface remain small enough to trust.
