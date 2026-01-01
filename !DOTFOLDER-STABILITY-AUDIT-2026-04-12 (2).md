---
title: "Dotfolder Stability Audit 2026-04-12"
updated: 2026-04-12
status: active
authority: "Logan Finney"
related:
  - AGENTS
  - VAULT-CONVENTIONS
  - swarm
  - The Abhorsen
  - The Architect
---

# Dotfolder Stability Audit

*Filed by Codex - 2026-04-12*

## Reading

The disappearing-dotfolder problem is real, but it is not one single bug.
There are two different classes of dotfolders in the vault:

1. **Durable dotfolders**: identity, governance, shim, and continuity chambers
   that should survive clones, branch switches, and repo transport.
2. **Ephemeral dotfolders**: runtime, cache, state, and local-machine surfaces
   that are allowed to disappear because they are ignored or regenerated.

The confusion comes when a durable chamber is missing a tracked anchor file and
therefore behaves like an ephemeral one.

## Durable Chambers

These should persist because they now have tracked anchors:

- `.claude/`
- `.gemini/`
- `.codex/`
- `.github/`
- `.crewai/`
- `.grok/`
- `.deepseek/`
- `.perplexity/`
- `.serena/`
- `.bartimaeus/`
- `.zagreus/`
- `.persephone/`
- `.google/`
- `.meta/`
- `.microsoft/`
- `.slack/`
- `.dionysus/`
- `.abhorsen/`

## Ephemeral Chambers

These currently behave as local runtime or cache surfaces and may disappear
without indicating doctrinal loss:

- `.agent-home/`
- `.cache/`
- `.state/`
- `.tmp/`
- `.uv-cache/`
- `.venv/`
- `.npm-cache/`
- `.pip-cache/`
- `.pycache/`
- `.remember/`
- `.smart-env/`
- `.space/`
- `.makemd/`

## Cause

Git does not preserve empty directories. A dotfolder with no tracked anchor can
vanish when:

1. branches switch
2. a fresh clone is made
3. cleanup tooling removes untracked or empty state
4. ignored local runtime content is regenerated somewhere else

## Repairs Made

1. `.serena/SERENA.md` now exists as a real local shim.
2. `.abhorsen/README.md` now anchors the historical alias chamber.
3. `.dionysus/ZAGREUS.md` is now explicitly a historical alias anchor.
4. `.github/scripts/check_dotfolder_anchors.py` validates durable chambers.
5. `.github/workflows/check-dotfolder-anchors.yml` fails CI if a required
   durable dotfolder loses its anchor.

## Remaining Rule

If Logan wants a dotfolder to survive branch churn, it must contain at least one
tracked anchor file. If a dotfolder is meant to remain local-only and
regenerable, it should stay ignored and be treated as ephemeral on purpose.
