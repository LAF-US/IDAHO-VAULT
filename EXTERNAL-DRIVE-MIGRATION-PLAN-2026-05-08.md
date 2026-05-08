---
title: "External Drive Migration Plan"
updated: 2026-05-08
status: draft
authority: "LOGAN"
related:
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - VAULT-MEDIA-STORAGE
---

# External Drive Migration Plan - 2026-05-08

Purpose: turn Logan's three mixed external drives into role-specific working
surfaces without deleting, rewriting, or publishing private detail.

This plan is non-destructive. It records intended routing and review order only.

## Canonical Roles

| Drive | Role       | Target behavior                                                                                                                                       |
| ----- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `D:`  | Home Desk  | Broad home-base archive and staging surface for personal, school, paperwork, photos, music, older projects, and material needing slower review.       |
| `E:`  | Work Desk  | Professional archive and working surface for Idaho Reports, Legislature, IDEX, FYIdaho, OI, production media, exports, and source/reference packages. |
| `F:`  | Travel Bag | Portable active-work SSD. Keep lean. Carry current field/project files only, then offload back to Home Desk or Work Desk.                             |

## Current Pressure

| Drive | Current signal                                                                      | Operational implication                                                                          |
| ----- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `D:`  | Largest free-space pool. Mixed personal/professional history.                       | Best temporary staging drive during sorting, but do not let it become a permanent unsorted dump. |
| `E:`  | Strongest professional Idaho/media profile. Plenty of free space.                   | Best candidate for professional/work consolidation.                                              |
| `F:`  | Least free space. Contains active-looking buckets plus cache/temp/recycle material. | Audit first. Offload durable work, then trim to portable active material.                        |

## Bucket Routing Draft

| Bucket/category                      | Seen on                    | Target role                         | Review note                                                                                                  |
| ------------------------------------ | -------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `Idaho Reports` / `IR`               | `D:`, `E:`, `F:`, OneDrive | Work Desk                           | Consolidate carefully by project/date; not proven duplicate.                                                 |
| `Legislature`                        | `D:`, `E:`                 | Work Desk                           | Professional public-affairs source/media category.                                                           |
| `IDEX` / `IDEX_Artifacts_temp`       | `E:`, `F:`                 | Work Desk                           | Review temp suffix before treating as archive-worthy.                                                        |
| `FYIdaho`                            | `E:`                       | Work Desk                           | Keep with professional Idaho material.                                                                       |
| `OI`                                 | `E:`                       | Work Desk                           | Keep with professional Idaho material unless later reclassified.                                             |
| `Science Trek`                       | `F:`                       | Work Desk                           | Professional/media archive candidate; likely should not remain on Travel Bag long term.                      |
| `Social media experiments`           | `E:`, `F:`                 | Work Desk                           | Same file count and size in prior inventory; strong duplicate candidate. Verify before deleting either copy. |
| `PREMIERE EXPORTS`                   | `D:`, `F:`                 | Work Desk                           | Production output. Review for duplicates and project ownership.                                              |
| `Adobe Media Cache and Scratch Disk` | `F:`                       | Travel Bag scratch or discard       | Cache/scratch class, not durable archive unless specific files are intentionally retained.                   |
| `temp` / `IDEX_Artifacts_temp`       | `F:`                       | Review before routing               | Temp name means inspect before archive, copy, or deletion.                                                   |
| `$RECYCLE.BIN`                       | `D:`, `E:`, `F:`           | Cleanup candidate                   | Empty only after Logan confirms no needed recovery material.                                                 |
| `School`                             | `D:`                       | Home Desk                           | Personal/education archive.                                                                                  |
| `personal`                           | `D:`, `F:`                 | Home Desk                           | Sensitive category; avoid detailed public manifests.                                                         |
| `!Photos`                            | `D:`                       | Home Desk                           | Personal/photo archive unless specific professional shoots are found.                                        |
| `Paperwork`                          | `D:`, `E:`                 | Home Desk by default                | Manual review; may contain both personal and professional records.                                           |
| `Phi Mu Alpha` / `Sheet Music`       | `D:`                       | Home Desk                           | Personal/music archive.                                                                                      |
| `Things I Made`                      | `D:`                       | Home Desk by default                | Review for publication/work exceptions.                                                                      |
| `DESKTOP`                            | `F:`                       | Home Desk or Work Desk after review | Imported desktop dump; classify subfolders before moving.                                                    |
| `misc`                               | `F:`                       | Review before routing               | Name is not enough to classify.                                                                              |

## Non-Destructive Migration Order

1. Stabilize `F:` Travel Bag first: classify cache, recycle, temp, active work,
   and durable archive candidates.
2. Move or copy durable professional media from `F:` to `E:` Work Desk only
   after checksums or duplicate evidence exist.
3. Move or copy personal material from `F:` to `D:` Home Desk only after folder
   intent is clear.
4. Compare cross-drive professional overlaps: `IR` / `Idaho Reports`,
   `Legislature`, `Dialogue`, `Idaho Debates`, `PREMIERE EXPORTS`, and
   `Social media experiments`.
5. Only after duplicate checks, consider cleanup actions such as emptying
   recycle bins, removing disposable cache, or retiring redundant copies.

## Guardrails

- Do not delete originals during the first migration pass.
- Do not publish detailed manifests of personal folders.
- Do not move cloud-synced roots without checking sync behavior.
- Do not rely on drive letters alone in future automation; use role plus volume
  label/device identity where possible.
- Treat `F:` as portable and fallible: it should carry active working sets, not
  the only copy of anything important.
