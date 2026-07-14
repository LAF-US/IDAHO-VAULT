---
title: "Triage - CLI Surfacing"
date created: 2026-04-17
authority: codex
doc_class: report
status: active
related:
  - "!/REPORT-SWARM-LEVEL-CLI-REVIEW-2026-04-17.md"
  - "AGENT-PROTOCOL.md"
  - "LEVELSET.md"
  - "!/WAKEUP.md"
  - "pyproject.toml"
  - "src/idaho_vault/main.py"
  - "!/agent.sh"
  - "agent.sh"
---

# Triage - CLI Surfacing

## Scope

This note triages the current CLI surfacing problem.

The issue is not only which commands exist.
The issue is which commands are being surfaced to operators, through which
documents, with what implied authority, and with what level of truthfulness
about their execution boundary.

## Current Surfacing Families

### 1. Bootstrap shell surfacing

This is the clearest current operator surface.

It is surfaced consistently in:

- `AGENT-PROTOCOL.md`
- `LEVELSET.md`
- `!/WAKEUP.md`
- `!/AGENTS.md`
- `!/agents.json`
- `!/agent.sh`
- root `agent.sh`

Current message:

- canonical local bootstrap = `!/agent.sh`
- root `agent.sh` = compatibility wrapper
- bootstrap is explicitly repo-local

This family is mostly truthful and low-risk.

### 2. Package script surfacing

This is surfaced primarily through `pyproject.toml` and the installed-script
contract it implies.

Current exported names:

- `idaho_vault`
- `run_crew`
- `train`
- `replay`
- `test`
- `run_with_trigger`
- `five_wizards_threshold`

Current problem:

the package surfacing implies a more general CLI than the implementation
actually supports.

### 3. Config-side CLI-adjacent surfacing

These surfaces shape the operator environment without being the operator CLI:

- `.codex/config.toml`
- `.vscode/mcp.json`
- `.vscode/settings.json`

These are not the core surfacing problem right now.
They are narrow and mostly honest.

## Triage Read

### Green surfacing

- `!/agent.sh`
- root `agent.sh`
- `AGENT-PROTOCOL.md`
- `LEVELSET.md`
- `!/WAKEUP.md`

Why:

- they tell the user this is local bootstrap
- they identify the canonical entrypoint
- they distinguish canonical from compatibility wrapper

### Yellow surfacing

- `idaho_vault`
- `run_crew`
- `run_with_trigger`

Why:

- these are real commands
- but they are surfaced as package scripts without strong checkout-bound
  disclaimers

### Yellow-red surfacing

- `test`
- `five_wizards_threshold`

Why:

- `test` sounds like a normal package command but depends on repo-local test
  discovery
- `five_wizards_threshold` is a strong real command, but its surfaced posture
  is incomplete because the public entrypoint does not expose dry-run vs
  materialize

### Red surfacing

- `train`
- `replay`

Why:

- these names are surfaced as installable commands
- they are intentionally unimplemented
- that makes them more misleading than useful at the current stage

## Main Mismatch

The shell/bootstrap layer and the package-script layer are telling different
truths.

The shell layer says:

- local
- rooted
- explicit
- compatibility-aware

The package layer currently says, by implication:

- installable
- general
- command-complete

The implementation does not justify that second message yet.

## Active Triage Queue

### Queue 1 - boundary truth

Decide which package scripts are:

- local-checkout only
- operator-safe by default
- too incomplete to surface yet

### Queue 2 - public posture

For any script that remains surfaced, decide whether it needs:

- a startup guardrail
- a clearer name
- explicit dry-run/write flags
- a better docstring and help contract

### Queue 3 - test truth

Add direct command-level tests for `src/idaho_vault/main.py` so the surfaced
names and their actual behavior stop drifting apart.

## Immediate Recommendation

Do not add new CLI names.

First fix surfacing truth in this order:

1. classify every current script as green / yellow / red
2. remove or demote red names, or mark them explicitly as stubs
3. expose operator posture for `five_wizards_threshold`
4. add direct CLI tests

## Bottom Line

The current CLI problem is a surfacing problem before it is a functionality
problem.

The bootstrap shell path already models the right behavior:

- canonical name
- compatibility wrapper
- explicit boundary

The package CLI should be brought up to that same standard before it grows.
