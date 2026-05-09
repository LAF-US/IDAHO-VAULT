---
title: "Work Desk Manifest"
updated: 2026-05-08
status: draft
authority: "LOGAN"
related:
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
---

# Work Desk Manifest - 2026-05-08

Purpose: sanitized, non-destructive manifest for Logan's Work Desk external
drive. This records top-level storage shape and receiving-lane candidates for
professional material currently mixed across external drives.

Observed on this audit pass:

| Identity field         | Observed value            |
| ---------------------- | ------------------------- |
| Canonical role         | Work Desk                 |
| Windows mount observed | `E:`                      |
| Volume label observed  | Expansion                 |
| Device observed        | Seagate Expansion HDD USB |
| Filesystem observed    | exFAT                     |
| Used space             | 660.79 GB                 |
| Free space             | 3064.96 GB                |

The Windows mount path is an observation, not a persistent identity.

## Top-Level Buckets

| Bucket                      | Files | Approx. size | Initial routing                                                     |
| --------------------------- | ----: | -----------: | ------------------------------------------------------------------- |
| `Idaho Reports`             | 4,088 |    452.61 GB | Work Desk core archive                                              |
| `Legislature`               |   949 |     71.00 GB | Work Desk core archive                                              |
| `Social media experiments`  |   174 |     43.91 GB | Work Desk core/archive; duplicate candidate against Travel Bag copy |
| `Dialogue`                  | 1,382 |     38.30 GB | Work Desk archive candidate                                         |
| `FYIdaho`                   |   209 |     29.22 GB | Work Desk core archive                                              |
| `$RECYCLE.BIN`              |    61 |     20.63 GB | Cleanup candidate after Logan confirmation                          |
| `Idaho Debates`             |   153 |      3.28 GB | Work Desk archive candidate                                         |
| `IDEX`                      |    48 |      0.31 GB | Work Desk archive candidate                                         |
| `OI`                        |    50 |      0.20 GB | Work Desk archive candidate                                         |
| `Paperwork`                 |    91 |      0.02 GB | Manual review; may contain mixed records                            |
| `readme`                    |    41 |      0.02 GB | Keep/review                                                         |
| `il29`                      |     1 |     <0.01 GB | Manual review                                                       |
| `Seagate`                   |     1 |     <0.01 GB | Device/vendor support material                                      |
| `System Volume Information` |     2 |     <0.01 GB | Windows system metadata                                             |

## Storage Role Assessment

Work Desk is already strongly aligned with its target role. The dominant buckets
are professional Idaho/media archives, and the drive has enough free space to
receive durable professional material from Travel Bag after duplicate checks.

Known receiving-lane candidates from Travel Bag:

| Travel Bag bucket          | Approx. size | Work Desk receiving logic                                                                        |
| -------------------------- | -----------: | ------------------------------------------------------------------------------------------------ |
| `IR`                       |    261.62 GB | Compare against `Idaho Reports`; consolidate by project/date, not by name alone.                 |
| `Science Trek`             |    138.49 GB | Professional/media archive candidate; may need a new Work Desk bucket if no existing lane fits.  |
| `IDEX_Artifacts_temp`      |     57.08 GB | Compare against `IDEX`; review temp status before archive.                                       |
| `Social media experiments` |     43.91 GB | Same size and file count as Work Desk bucket in this pass; high-priority duplicate verification. |
| `PREMIERE EXPORTS`         |     <0.01 GB | Work/export candidate; review for project relevance.                                             |

## Recommended Non-Destructive Order

1. Verify `Social media experiments` across Work Desk and Travel Bag using a
   relative-path/size/mtime manifest, then checksum only if needed.
2. Build a subfolder-level map for Work Desk `Idaho Reports` and Travel Bag
   `IR` before merging anything.
3. Decide whether `Science Trek` belongs as a Work Desk top-level bucket or
   inside a broader production/archive lane.
4. Review `IDEX_Artifacts_temp` against existing Work Desk `IDEX` before
   treating temp artifacts as durable archive.
5. Confirm whether Work Desk `$RECYCLE.BIN` can be emptied.

## Guardrails

- No deletion in the first pass.
- No duplicate retirement without checksum or equivalent evidence.
- Do not equate `IR` and `Idaho Reports` solely by name similarity.
- Do not use `E:` as a persistent identity.
- Keep professional archives on Work Desk only after confirming the Work Desk
  role against volume/device evidence.
