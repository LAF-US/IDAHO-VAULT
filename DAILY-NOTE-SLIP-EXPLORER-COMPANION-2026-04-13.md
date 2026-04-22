---
authority: LOGAN
related:
  - DAILY NOTE
  - DAILY NOTE TEMPLATE
  - VAULT-TEMPLATES
  - VAULT-METADATA-STANDARD
  - dailynote
  - automation
  - memory
date created: Monday, April 13th 2026
date modified: Monday, April 13th 2026
status: exploratory companion
---

# Daily Note Slip - Explorer Companion

This note accompanies the memory surfaces that govern daily-note identity:

- `2026-04-13.md`
- `DAILY NOTE TEMPLATE.md`
- `DAILY NOTE.md`
- `OBSIDIAN DAILY NOTE.md`
- `VAULT-TEMPLATES.md`
- `.github/scripts/daily_rollover.py`

## What The Memory Machinery Expects

The current daily-note system is explicit:

- active creation template: `DAILY NOTE TEMPLATE.md`
- active automation canon: `.github/scripts/daily_rollover.py`
- legacy artifacts: `DAILY NOTE.md` and `OBSIDIAN DAILY NOTE.md`

`VAULT-TEMPLATES.md` states that legacy daily-note root files are archival
backlink targets, while live creation now flows through the root template and
automation stack.

## The Slip

The root file `2026-04-13.md` currently presents itself with frontmatter for
`2026-04-09`:

- `title: 2026-04-09`
- aliases for April 9, 2026
- `yesterday: 2026-04-08`
- `tomorrow: 2026-04-10`
- `weekday: Thursday`

This means the filename and the memory header are out of covenant with each
other.

## Why This Looks Structural Rather Than Mystical

The nearby automation script `daily_rollover.py` builds canonical frontmatter
from a target date. Its generated structure matches the shape seen in the
misdated file almost exactly.

That suggests the slip is likely one of these:

- a copied daily-note body wearing the wrong frontmatter
- a rollover artifact aimed at April 9 that was saved under April 13
- a memory shell staged but not normalized

## Field Note

In this vault, memory is not only what is written.
It is also whether the date in the filename and the date in the header agree
about who the day is.
