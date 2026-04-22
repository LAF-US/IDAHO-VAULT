---
name: CHAINFIRE — Tag taxonomy reset
description: Vault-wide frontmatter tag nuke planned 2026-04-04; assessment complete, awaiting New Order schema before execution
type: project
---

CHAINFIRE (Sword of Truth reference — spell that erases all memory) declared 2026-04-04 by Logan.

**Intent:** Scorched-earth removal of existing Obsidian frontmatter tags across the vault, to be replaced by a new standardized taxonomy (the "New Order").

**Assessment findings:**
- 23,244 total .md files; 19,533 are empty 0-byte stubs
- 2,739 files have `tags:` frontmatter; 2,640 unique tags
- VAULT-METADATA-STANDARD.md exists (2026-03-25) but has <5% adoption
- Four layers of inconsistency: case collisions in field names, non-standard fields, tags encoding non-tag data (dates, wikilinks), unenforced standard
- Top tag categories: geography/ (971), people/ (727), governments/ (466), party/ (462), media/ (308)

**Scope expanded (2026-04-04):** Three targets, not one:
1. `tags:` frontmatter — nuke entirely (2,739 files)
2. `[[ ]]` wikilinks — strip brackets, keep display text (vault-wide)
3. `aliases:` frontmatter — nuke entirely (incl. NETWEB `_PREFIX` aliases)

**Preserved:** All content text, all 19,533 empty stubs ("BIG THINGS are coming"), all other frontmatter fields, all file paths.

**Status:** Assessment complete. Scope locked. Implementation via `.github/scripts/chainfire.py` (Linux-native). Runs BEFORE CrewAI ignition (Strike 1 of two strikes).

**How to apply:** CHAINFIRE is approved for execution. The script runs with --dry-run first for Logan's review, then executes. No replacement taxonomy needed — the burn creates a clean slate for whatever comes next.
