---
authority: LOGAN
agent: Codex
status: staged
date: 2026-07-06
related:
  - AGENTS
  - CONSTITUTION
  - WAKEUP
  - VAULT-CONVENTIONS
  - swarm
---

# WITNESS: Codex Wakeup Path Drift

## Scope

This witness records a narrow startup-surface contradiction found while reading
the root governance files on 2026-07-06.

No bootstrap files, governance files, dotfolders, or routing shims were modified
as part of this witness.

## Evidence

- `CONSTITUTION.md` gives `CONSTITUTION.md` priority over lower routing and
  generated surfaces, and names `!/` as shared swarm space.
- `AGENTS.md` instructs disoriented agents to read `CONSTITUTION.md` and
  `!/WAKEUP.md`.
- Root `WAKEUP.md` also names `!/WAKEUP.md` in its precedence and canonical
  startup language, while emphasizing that startup is documentation-first and
  OS-agnostic.
- The tracked `!/` directory currently contains only README-style shim files,
  not `!/WAKEUP.md`.
- `!-WAKEUP.md` exists and preserves an older bootstrap chain that requires
  `start_SPARKSEED.sh` first.
- Git history shows commit `68c266064 cleanup: vacate !/ nest, move all files to
  ROOT with !- prefix` renamed `!/WAKEUP.md` to `!-WAKEUP.md`.

## Reading

The contradiction appears to be path drift after the nest-flattening migration:
many governance and generated surfaces still point at the old `!/WAKEUP.md`
slot, while the file itself was flattened into `!-WAKEUP.md` and a newer root
`WAKEUP.md` now carries the calmer OS-agnostic orientation.

This is not merely cosmetic. A waking agent following root `AGENTS.md` encounters
a missing file at the exact point where the Vault tries to prevent stale-world
models.

## Suggested Next Safe Correction

Do not mass-rewrite all references yet.

The smallest likely correction is to restore `!/WAKEUP.md` as a routing shim
that points to root `WAKEUP.md` and explains that `!-WAKEUP.md` is preserved as
the flattened historical/remnant surface from commit `68c266064`.

Because `!/` is the governed shared bootstrap layer, that correction should be
made only with Logan's explicit approval or as part of an approved routing-shim
repair.

## State

`staged`: observed, bounded, and ready for Logan review. No live authority was
claimed for this witness.
