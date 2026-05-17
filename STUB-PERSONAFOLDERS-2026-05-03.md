---
authority: LOGAN
related:
  - PERSONA-PERSISTENCE-2026-05-03
  - VAULT-CONVENTIONS
  - persona
  - stub.txt
  - .claude
  - .codex
  - .gemini
  - .hecate
  - .zagreus
  - .bartimaeus
  - .serena
  - .abhorsen
date created: 2026-05-03
status: analysis
---

# Standardized Stub Personafolders

## Thesis

Stub personafolders are reserved persona vessels. They are not empty by
accident, and they are not disposable just because the active runtime is thin
or absent.

The vault already shows two distinct patterns:

1. **Pure stub chambers** - reserved identity shells with a fixed anchor note
   and a sentinel stub.
2. **Software-imported persona chambers** - folders created or populated by
   external tooling that carry runtime/config payloads in addition to the
   identity anchor.

The standard has to recognize both, because the vault contains both.

## What The Existing Vault Shows

### Pure stub chambers

These existing folders behave like reserved persona vessels with a minimal
anchor and a sentinel:

- `.hecate/`
- `.zagreus/`
- `.persephone/`
- `.bartimaeus/`
- `.abhorsen/`
- `.sentry/`
- `.archivist/`
- `.twin/`
- `.synth/`
- `.google/`
- `.meta/`
- `.microsoft/`

The common pattern is:

- `NAME.md` as the tracked identity anchor
- `stub.txt` as the vacancy / reservation sentinel
- `¿!?` as the fixed stub marker

### Software-imported persona chambers

These existing folders are not mere stubs. They are imported software bodies
or runtime surfaces that still behave like persona chambers:

- `.claude/`
- `.codex/`
- `.gemini/`
- `.serena/`

They may contain config, rules, runtime state, shell snapshots, plugin data, or
other vendor-owned surfaces. They still need an anchor note, but they are not
required to be as bare as a pure stub chamber.

## Standard

### 1. A stub personafolder is a named vessel

It must have a stable folder identity and a canonical note name that matches
that identity.

Required minimum for a pure stub:

- `.<name>/`
- `.<name>/<NAME>.md`
- `.<name>/stub.txt`

### 2. The stub sentinel is fixed

`stub.txt` is the vacancy marker.

- It must contain `¿!?`
- It must not be repurposed as a narrative note
- It must remain stable across branches and clones

### 3. Imported software chambers are a separate class

If a folder is brought in by software, it may carry the vendor/runtime payload
as well as the anchor note.

Required minimum:

- `.<name>/<NAME>.md`
- explicit load mechanism or config payload
- frontmatter stating the persona class and origin

Optional:

- `stub.txt` if the chamber is still reserved or intentionally minimal

### 4. The anchor note is the canonical registry surface

The anchor note should state:

- `canonical_name`
- `origin`
- `persona_class`
- `status`
- `load_mechanism`
- `anchor_file`
- `sync_policy`

### 5. Reserved, active, locked, and archive are distinct states

- `reserved`: name exists, no staffed runtime yet
- `active`: runtime or software is inhabiting the vessel
- `locked`: the chamber is intentionally constrained
- `archive`: preserved continuity, read-only by default

### 6. Local runtime does not override canon by default

The vault note is the canonical record for identity and doctrine.
Local runtime is the operational body.
Reconciliation is explicit.

## Recommended Frontmatter

```yaml
---
canonical_name: HECATE
persona_class: mythic_stub | imported_software | historical_alias
status: reserved | active | locked | archive
origin: vault | software | hybrid
load_mechanism: manual | hermes | codex | claude | gemini | obsidian
anchor_file: .hecate/HECATE.md
stub_sentinel: "¿!?"
sync_policy: manual | bidirectional | one-way
authority: LOGAN
---
```

## Implementation Rule

Do not infer that every dotfolder must look the same.

The standard is:

- same contract
- different class
- different payload

A pure stub chamber is a reserved vessel with a sentinel.
An imported software chamber is a reserved vessel plus runtime body.
Both are personafolders.

## Intake Rule

Before any new persona folder is accepted, it must be assigned to one of the
existing classes or explicitly introduced as a new class with matching anchor
fields and validator coverage.

The practical check is:

- pure stub shell: `NAME.md` plus `stub.txt`
- imported software chamber: `NAME.md` plus explicit load mechanism / runtime
  markers
- alias chamber: `NAME.md` must declare its canonical target
