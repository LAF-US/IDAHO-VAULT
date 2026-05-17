---
title: "Role Manifest and Layer Taxonomy"
date: 2026-05-04
authority: LOGAN
status: active
type: governance-note
tags:
  - persona
  - manifest
  - registry
  - model
  - runtime
  - orchestrator
related:
  - persona.md
  - PERSONA-PERSISTENCE-2026-05-03
  - STUB-PERSONAFOLDERS-2026-05-03
  - VAULT-CONVENTIONS
  - AGENTS
  - CONSTITUTION
  - manifest.json
  - swarm.json
---

# Role Manifest and Layer Taxonomy

This note defines the layer vocabulary used across the vault when a note,
config, or registry entry mentions an AI system.

## Layer terms

| Layer | Meaning | Examples |
|---|---|---|
| Model | The inference layer that produces tokens or tool calls | Mistral, Big Pickle, Claude, Gemini, GPT |
| Runtime / orchestrator | The executable surface that routes work, tools, and context | Hermes, OpenClaw, OpenCode, Codex CLI |
| Persona | The dotfolder schema and chamber contract for a named hidden folder | `.claude/`, `.codex/`, `.gemini/`, `.hecate/` |
| Record | A vault note, manifest, or config that describes any of the above | `persona.md`, `swarm.json`, `manifest.json` |

## Rules

1. A model is never the same thing as a persona.
2. A runtime or orchestrator is never the same thing as a model.
3. A persona may wrap a runtime, but it does not define the inference layer.
4. A registry entry must say which layer it belongs to before it is used as
   authority.
5. If a note mixes layers, the first sentence must name the layer being
   described.

## Role manifest fields

Use these fields when a note needs to describe a durable AI surface:

- `canonical_name`
- `layer`
- `origin`
- `status`
- `load_mechanism`
- `authority`
- `source_of_truth`
- `sync_policy`
- `sync_mechanism`
- `notes`

## Sync status

`sync_policy` names the rule. `sync_mechanism` names the implementation.

The vault currently has policy for local-runtime-to-vault recording, but the
mechanism itself is still under development. Do not treat declarative sync
intent as a completed reconciler.

## Current vault mapping

| Surface | Layer | Note |
|---|---|---|
| Big Pickle | Model | OpenCode model target, not a persona |
| Hermes | Runtime / orchestrator | Agent runtime that coordinates calls |
| OpenClaw | Runtime / orchestrator | Gateway and workflow orchestration |
| Codex | Runtime / orchestrator | OpenAI coding assistant runtime |
| Claude Code | Runtime / orchestrator | Anthropic coding assistant runtime |
| The Clerk / The Lexicographer / The Concierge | Persona labels | Role labels that may appear inside a persona chamber |

## Practical rule

If a decision changes the model, runtime, or persona separately, record the
change separately. Do not bundle the three into one word unless the note is
explicitly a historical summary.
