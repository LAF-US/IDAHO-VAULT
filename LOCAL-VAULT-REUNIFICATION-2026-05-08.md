---
title: "Local Vault Reunification"
updated: 2026-05-08
status: active
authority: "LOGAN"
related:
  - VAULT-MEDIA-STORAGE
  - HANDOFF-LFS-2GB-BLOCK-2026-05-08
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - HOME-DESK-MANIFEST-2026-05-08
  - WORK-DESK-MANIFEST-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
  - CROSS-DRIVE-OVERLAP-REPORT-2026-05-08
---

# Local Vault Reunification - 2026-05-08

Purpose: reunify the local vault state before spending more effort on specific
tooling failures, CI failures, or push mechanics.

Local `main` is ahead of `origin/main`. These commits should be treated as one
coherent local stabilization batch, not as isolated tool fixes.

## Current Local Batch

The local commits since `origin/main` form these threads:

| Thread                       | Purpose                                                                                                                                                           | Key files                                                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Large-file governance        | Align Git/Git LFS policy with GitHub's 2 GB LFS object limit and preserve the rule that oversized objects move to external durable storage with vault references. | `VAULT-MEDIA-STORAGE.md`, `HANDOFF-LFS-2GB-BLOCK-2026-05-08.md`, `.github/scripts/check_large_files.py`     |
| OS/environment agnosticism   | Keep MESHNET/NETWEB/WEBMESH and storage doctrine portable across Windows, macOS, Linux, mount schemes, and local environments.                                    | portability checks, drive identity notes, external drive migration plan                                     |
| External-drive roles         | Convert local drive-letter observations into canonical storage roles.                                                                                             | `EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08.md`                                                               |
| Storage inventory            | Record a sanitized folder-level view of local and external storage before moving or deleting anything.                                                            | `LOCAL-STORAGE-INVENTORY-2026-05-08.md`                                                                     |
| Drive manifests              | Establish one non-destructive manifest for each canonical external-drive role.                                                                                    | `HOME-DESK-MANIFEST-2026-05-08.md`, `WORK-DESK-MANIFEST-2026-05-08.md`, `TRAVEL-BAG-MANIFEST-2026-05-08.md` |
| Cross-drive overlap          | Identify overlap families and the first safe verification targets before consolidation.                                                                           | `CROSS-DRIVE-OVERLAP-REPORT-2026-05-08.md`                                                                  |
| Local agent/tool diagnostics | Record OpenClaw, Ollama, router, and local environment findings without making those tooling issues the center of the storage migration.                          | diagnostic/source notes and router tests                                                                    |

## Unified Operating Model

The vault should now treat these as separate lanes:

1. **Git lane**: source text, notes, small records, manifests, guard scripts,
   references, and LFS pointers where appropriate.
2. **External object lane**: raw media objects too large or too operationally
   heavy for GitHub transport.
3. **Local storage lane**: Logan's external drives, identified by canonical role
   and device evidence, not by drive letter.
4. **Tooling lane**: CI, Dependabot, rollover automation, OpenClaw, and other
   mechanisms that support the vault but do not define its contents.

Tool-specific failures should be fixed, but they should not distract from the
larger local consolidation: the vault needs a coherent storage and publication
model first.

## Canonical External Roles

| Role       | Observed Windows mount in this audit | Observed label | Target meaning                                          |
| ---------- | ------------------------------------ | -------------- | ------------------------------------------------------- |
| Home Desk  | `D:`                                 | LoganF         | Home-base personal/history archive and staging surface. |
| Work Desk  | `E:`                                 | Expansion      | Professional Idaho/media archive and working surface.   |
| Travel Bag | `F:`                                 | ExternalSSD    | Lean portable active-work SSD.                          |

Drive letters are observations only. Future automation must resolve these roles
by role, volume label, device evidence, filesystem identity where available, and
operator confirmation.

## Publication And Push State

Remote `origin/main` does not yet contain this local batch.

Known remote/tooling failures exist, but they are not caused by the local storage
manifest commits because those commits have not been pushed.

Current push blocker remains large-object governance:

- 38 tracked files exceed GitHub's 2 GB LFS object limit.
- Do not bypass LFS.
- Do not remove history as a workaround.
- Do not delete local originals.
- Per-policy remedy is external durable storage plus committed vault
  notes/manifests, then remove oversized objects from Git tracking after Logan
  confirms external backup.

## Reunification Order

1. Keep the local storage doctrine coherent: 2 GB GitHub LFS ceiling, external
   object references, and role-based drive identity.
2. Finish non-destructive mapping before moving or deleting files:
   manifests first, overlap reports second, checksums only where needed.
3. Resolve the oversized-object push blocker using the governance policy, not
   history destruction or LFS bypass.
4. Push the coherent local batch only after the push blocker is resolved.
5. Then fix specific GitHub tooling failures such as Dependabot workflow parsing
   and daily rollover path assumptions.

## Current Safe Next Work

The next vault-level work should be one of:

- build subfolder-level maps for `IR` / `Idaho Reports` across Home Desk, Work
  Desk, and Travel Bag
- build external-object reference manifests for the 38 files blocked by GitHub's
  2 GB LFS limit after Logan confirms backup locations
- refine the cross-drive overlap report with checksum evidence for the already
  exact `Social media experiments` candidate

Avoid spending first energy on remote CI failures unless they block the
reunification lane.
