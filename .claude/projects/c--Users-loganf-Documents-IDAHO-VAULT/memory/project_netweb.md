---
name: NETWEB — cross-platform path portability standard
description: Vault-wide standard for filesystem-agnostic paths (reserved names, case collisions, trailing periods). Established 2026-04-04.
type: project
---

**NETWEB** is the cross-platform path portability standard for IDAHO-VAULT, established 2026-04-04.

**Why:** PR #156 ("abhorsen awakens") introduced ~19,225 Obsidian wikilink stub files (A-ZZZ, 1-1000). Four had Windows-reserved names (AUX.md, CON.md, NUL.md, PRN.md), 16 had case collisions (Act.md/ACT.md), and one directory had a trailing period. Together these blocked `git merge` on Logan's Windows machine entirely.

**How to apply:** Before creating any file, check the rules in `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)". The CI workflow `check-portable-paths.yml` is the hard gate.

## Core rules

1. **Reserved device names** (AUX, CON, NUL, PRN, COM0-9, LPT0-9): alias with `_` prefix + `aliases: [ORIGINAL]` frontmatter
2. **Case uniqueness**: filenames within any directory must be case-unique (NTFS + APFS both case-insensitive)
3. **No trailing periods/spaces** in path components
4. **No illegal chars**: `< > : " | ? *` (Windows), `:` in filenames (macOS)
5. **Path length**: max 218 chars from repo root (260 NTFS MAX_PATH minus ~42 char local prefix)

## Enforcement layers

| Layer | File | Scope |
|---|---|---|
| .gitignore | `.gitignore` (NETWEB section) | Advisory — case-insensitive patterns for reserved names |
| CI guard | `.github/workflows/check-portable-paths.yml` | Hard gate on PRs and pushes to main |
| Documentation | `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)" | All agents |

## Implementation technique (2026-04-04)

The fix was done via **Git Data API** (`gh api` from Windows) — single atomic commit creating new tree with 48 path changes. This bypasses Windows's inability to manipulate reserved-name files locally. Useful pattern for any future cross-platform path surgery.

## Horizon

Logan's stated goal: **system and device agnosticism**. The vault should work identically on Windows, macOS, Linux, iOS/Android, and CI runners. NETWEB is the first enforcement layer of this vision.
