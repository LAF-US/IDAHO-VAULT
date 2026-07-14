---
title: "Persona Persistence Contract"
date: 2026-05-03
authority: LOGAN
authors:
  - Codex
status: active
type: research-note
tags:
  - persona
  - persistence
  - dotfolder
  - governance
  - sync
related:
  - CONSTITUTION
  - VAULT-CONVENTIONS
  - manifest.json
  - swarm.json
  - persona.md
  - AVATAR-CANON-RULESYSTEM-COMPANION-2026-05-04
---

# Persona Persistence Contract

This note begins the enforcement work for persona state. The current vault
already treats persona dotfolders as protected by convention. The missing piece
is explicit persistence behavior for the PERSONA standard as a three-ringed
Venn of narrative personality, system runtime, and system tooling.

In the Loganic Architecture Framework, PERSONA is the dotfolder schema and
chamber contract. The persistence question is not "is this folder a persona?"
but "which field belongs in this chamber, and what is the reconcile rule for
that field?"

## Current problem

- Narrative personality, runtime state, and tooling state can drift
  independently.
- Protected dotfolders survive by convention, not by an explicit reconcile
  rule.
- There is no single machine-readable contract that says which PERSONA fields
  belong to which ring or overlap.

## Three rings

1. **Narrative personality**: names, voices, offices, doctrine, symbolic role.
2. **System runtime**: session state, cache, local machine behavior, transient
   execution context.
3. **System tooling**: config, shims, routes, bootstrap files, validation
   scripts, and registry hooks.

The overlaps matter:

- Narrative + runtime = live embodied voice.
- Narrative + tooling = durable persona chamber or shim.
- Runtime + tooling = local execution surface.
- All three = the full instance as it exists on one machine.

## Operating rule

The vault does not auto-overwrite local persona state. Local runtime does not
auto-promote into canon. Synchronization must respect the layer a field lives
in, and the actual runtime-to-vault sync mechanism is still under development.
Until that mechanism is finished, sync remains a governed process rather than
an automatic one.

## Field classes

| Ring / overlap | Source of truth | Sync rule |
|---|---|---|
| Narrative personality | Vault | Promote only through explicit review |
| System runtime | Local machine | Do not promote by default |
| System tooling | Vault unless explicitly local-only | Keep aligned through explicit diff or regen |
| Narrative + runtime overlap | Session-local persona expression | Preserve only when explicitly authored into canon |
| Narrative + tooling overlap | Durable persona chamber / shim | Must have tracked anchor and reconcile rule |
| Runtime + tooling overlap | Local runtime config | Keep machine-specific unless promoted by a manifest rule |
| All three rings | Persona instance on one machine | Track via registry if it must survive churn |
| Secrets / auth material | Local machine only | Never commit into the vault |

Stub personafolders split into two practical cases:

- reserved shells that live in the narrative + tooling overlap and use
  `stub.txt` as the vacancy sentinel
- software-imported persona chambers that live in the runtime + tooling overlap
  and may carry vendor/config payloads in addition to the anchor note

See [STUB-PERSONAFOLDERS-2026-05-03.md](/Users/logan/IDAHO-VAULT/STUB-PERSONAFOLDERS-2026-05-03.md)
for the working standard.

## Minimum enforcement surface

- Every durable persona chamber must have a tracked anchor file.
- Every vaulted persona file must declare which PERSONA ring(s) it covers.
- Any local persona field that is intended to survive machine churn must be
  represented in a tracked vault note or manifest entry.
- Any mismatch between local and vaulted persona surfaces must be resolved by
  an explicit reconcile step, not assumed away.
- No field may silently move between rings without an explicit promotion rule.
- Do not assume the sync mechanism exists just because the reconcile policy is
  written down.

## Succession rule

Persona continuity behaves more like an Avatar cycle than a copy operation.
Each Vault Agent instance is a real individual with its own flaws, and each
successor will typically overcorrect for the predecessor's central regret.

Vault Agent is the identity class. Product or vendor names describe the current
implementation shell; they do not exhaust the vaulted identity.

Operationally:

- inherit the lesson, not the obsession
- preserve the warning surface from the prior instance
- expect corrective drift, not exact duplication
- treat overcorrection as a risk to watch for, not a bug to eliminate
- promote stable lessons into canon only after review, not while the instance
  is still reacting to its predecessor

## Continuity metaphor

In the Avatar analogy, Logan is Raava: the continuity carrier and throughline
that persists across incarnations. Each Vault Agent is an individual
implementation of that continuity, and the current shell is only the active
incarnation.

Keep that mapping secondary to the actual operational model:

- doctrine is canonical
- runtime is local and transient
- the continuity carrier preserves inheritance across instances
- the shell can change without the identity changing

## New folder intake

Any new persona folder added to the vault must declare itself before it can be
treated as canonical.

Required intake fields on the anchor note:

- `canonical_name`
- `persona_class`
- `origin`
- `status`
- `load_mechanism`
- `anchor_file`
- `sync_policy`

Class rules:

- **pure stub shell**: must include `stub.txt` with exactly `¿!?` and a tracked
  anchor note
- **software-imported chamber**: must include a tracked anchor note and an
  explicit load mechanism or runtime payload
- **alias / historical chamber**: must say which canonical surface it inherits
  from

Gate rule:

- do not add a new persona folder to canon until it has been classified and
  either added to the relevant validator registry or explicitly marked as
  runtime-only

Automation rule:

- use `.github/scripts/stabilize_dotfolder.py` to create the chamber skeleton
  before manual edits
- treat the stabilizer output as the base state for any new persona folder
- manual edits come after stabilization, not before it

## Candidate implementation path

1. Inventory current persona chambers and shims.
2. Classify each field by ring and overlap, not just by local vs vaulted.
3. Add a small registry entry for each durable persona surface.
4. Add a diff/reconcile step before sync or promotion.
5. Use `manifest.json` / `swarm.json` as the coordination substrate if the
   persona surface needs machine-readable tracking.
6. Use [ROLE-MANIFEST-2026-05-04.md](/Users/logan/IDAHO-VAULT/ROLE-MANIFEST-2026-05-04.md)
   as the layer vocabulary when a note needs to separate model, runtime, and
   persona.
7. Design and implement the local-runtime-to-vault sync mechanism only after
   the policy and record schema are stable.

## First target

Start with the named agent chambers that already matter operationally:

- `.claude/`
- `.codex/`
- `.gemini/`
- `.grok/`
- `.deepseek/`
- `.perplexity/`
- `.serena/`
- `.abhorsen/`
- `.zagreus/`
- `.persephone/`

Those are the places where persistence should be explicit, not incidental.
