---
authority: Codex
date created: 2026-04-09
status: active
source: ground-truth
---

# Flatten Run - 2026-04-09

This note records the first doctrinal flatten pass executed on the clean rewritten base.

## Outcome

- root moves without rename: `1495`
- root moves with deterministic rename: `424`
- `INBOX/` files rehomed under `!/INBOX/`: `15`
- machine-state files skipped in place: `12`

## Provenance Preservation

Folder attribution is preserved in both forms:

- machine manifest: `!/RESTRUCTURE-MANIFEST-2026-04-09.jsonl`
- human-readable attribution:
  - `!/RESTRUCTURE-ATTRIBUTION-2026-04-09.csv`
  - `!/RESTRUCTURE-ATTRIBUTION-2026-04-09.md`

## Rules Applied

- protected surfaces untouched:
  - `!/`
  - dotfolders
  - underscore-prefixed top-level folders
- `INBOX/` was rehomed under `!/INBOX/`, not flattened into root
- incumbent root filenames were preserved
- incoming collisions were renamed deterministically using source-folder slug plus path-derived hash
- Windows / machine junk like `Thumbs.db` and `desktop.ini` was not promoted into root

## Dominant Entropy Source

`SCRATCH FOLDER` remained the dominant collision source in this pass.

Observed attribution summary:

- `SCRATCH FOLDER`: `1036` direct root moves, `409` deterministic renames, `5` skipped machine-state files

## Next Lane

The next major delivery lane after this flatten pass is CrewAI deployment from the scaffold-only base.
