---
authority: Codex
date created: 2026-04-09
status: active
source: ground-truth
---

# Flatten Prep - 2026-04-09

This note records the post-rewrite flatten readiness snapshot.

It does not authorize or execute the flatten.

## Current Preconditions

- Live repo is clean on `main`.
- Open PR count is `0`.
- Remote heads are:
  - `main`
  - `codex/rewrite-main-2026-04-09`
- The disposable rewrite mirror has been refreshed against current `main`.
- Current refreshed rewrite mirror size: `32.78 MiB`.

## Protected Top-Level Directories

These are out of scope for Logan's flatten operation:

- `!/`
- all dotfolders
- all underscore-prefixed folders

Protected directories currently present:

- `!`
- `.abhorsen`
- `.bartimaeus`
- `.claude`
- `.coderabbit`
- `.codex`
- `.crewai`
- `.cursor`
- `.deepseek`
- `.dionysus`
- `.gemini`
- `.git`
- `.github`
- `.google`
- `.grok`
- `.makemd`
- `.meta`
- `.microsoft`
- `.obsidian`
- `.op`
- `.perplexity`
- `.persephone`
- `.qodo`
- `.reference-map`
- `.remember`
- `.slack`
- `.smart-env`
- `.space`
- `.venv`
- `.vscode`
- `.zagreus`
- `_private`
- `_templates`

## In-Scope Top-Level Directories

These are currently in scope for doctrinal absorption after rewrite cutover:

- `01 Comm Plan presentation`
- `8-23 fire presser pics`
- `BMO`
- `Bobby Montoya smokejumper photos for Marcia`
- `Camera Roll`
- `counties`
- `crow-2023-11-27-05-01-54-utc`
- `D.Idaho_1_25-cv-00061-AKB_36`
- `futura`
- `FY 2027 Budget Requests`
- `FYIdaho`
- `hydrate-chats`
- `idex greater idaho`
- `INBOX`
- `Lightroom Saved Photos`
- `Liscense Plate Reports`
- `LoganF IPT PRR`
- `Photos-001`
- `Photos-001 (1)`
- `Photos-1-001 (1)`
- `PICS-Pettinger`
- `PKG Scholarships`
- `rabbit-hiding-in-forest-grass-2023-11-27-05-28-50-utc`
- `Saved Pictures`
- `science trek skin`
- `SCRATCH FOLDER`
- `Screenshots`
- `scripts`
- `Social Media Videos`
- `STATE PROPERTIES`
- `Tags`
- `Zaudi-cam`
- `Zoom`

## File Count and Collision Risk

Current first-pass inventory:

- total in-scope files: `1,970`
- direct collisions with existing root filenames: `298`
- duplicate basenames across in-scope folders: `210`
- total duplicate-file instances inside those duplicate groups: `437`

This means the flatten can be done, but not safely as a blind move.

It requires:

- deterministic rename policy for incoming collisions
- a manifest recording original path -> destination path
- special handling for `INBOX/`

## Highest-Volume In-Scope Directories

Top file-bearing directories by count:

| Directory | Files | Root-name collisions |
| --- | ---: | ---: |
| `SCRATCH FOLDER` | 1452 | 287 |
| `idex greater idaho` | 129 | 0 |
| `FY 2027 Budget Requests` | 73 | 0 |
| `Photos-1-001 (1)` | 48 | 0 |
| `Bobby Montoya smokejumper photos for Marcia` | 42 | 0 |
| `Zoom` | 36 | 0 |
| `counties` | 33 | 0 |
| `LoganF IPT PRR` | 28 | 0 |
| `futura` | 20 | 0 |
| `PICS-Pettinger` | 19 | 1 |
| `01 Comm Plan presentation` | 16 | 0 |
| `INBOX` | 15 | 4 |

## INBOX Rule

`INBOX/` should not be flattened into root.

Current doctrinal rule:

- rehome `INBOX/` under `!/INBOX/`
- preserve intake semantics there
- do not treat `INBOX/` as normal corpus flatten material

Current `INBOX/` file count:

- `15`

Observed current `INBOX/PHONE-LINK/` contents include:

- screenshots
- gifs
- helper scripts
- one log file

This further supports treating `INBOX/` as intake, not corpus.

## Collision Shape

Most collision pressure is concentrated in `SCRATCH FOLDER`.

Examples of duplicate basenames across in-scope folders:

- `Thumbs.db` (`9`)
- `recording.conf` (`8`)
- `desktop.ini` (`3`)
- many repeated geography/topic note names inside `SCRATCH FOLDER`

Examples of direct collisions against existing root files:

- `BMO/BMO.md`
- `PICS-Pettinger/images.jpg`
- `INBOX/PHONE-LINK/McGrane.webp`
- `INBOX/PHONE-LINK/phone-link-auto-sweep.ps1`
- `INBOX/PHONE-LINK/START-PHONE-LINK-SWEEP.cmd`

## Path-Portability Notes

High-probability portability trouble spots during flatten:

- filenames with spaces plus near-duplicates
- Windows shell junk like `desktop.ini` and `Thumbs.db`
- mixed-case or punctuation-heavy names
- duplicate basenames that would force deterministic renaming

The flatten should continue obeying NETWEB path rules:

- ASCII-safe preferred for generated names
- no reserved Windows names
- no silent overwrite behavior
- deterministic rename output for repeatability

## Recommended Rename Rule

When an incoming file collides with an existing root filename:

- keep the existing root filename
- rename the incoming file as:
  - `<stem>__src_<top-level-folder-slug>__<hash8><ext>`

The hash should derive from the original relative path so the result is stable.

## Accuracy and Precision Check

This flatten has two separate success tests:

- accuracy:
  - preserve the real meaning of the corpus and intake layers
  - do not misclassify `INBOX/`
  - do not lose source-folder provenance

- precision:
  - move only intended in-scope files
  - touch no protected directories
  - overwrite nothing silently
  - produce stable deterministic rename results

## Next Logan Gate

The next true human decision is still:

1. authorize protected-branch rewrite cutover on `main`
2. then execute the doctrinal flatten on the clean rewritten base

Until that cutover is approved, flatten work should remain planning, manifest design, and collision-policy prep only.
