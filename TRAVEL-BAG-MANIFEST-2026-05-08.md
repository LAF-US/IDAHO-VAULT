---
title: "Travel Bag Manifest"
updated: 2026-05-08
status: draft
authority: "LOGAN"
related:
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - LOCAL-STORAGE-INVENTORY-2026-05-08
---

# Travel Bag Manifest - 2026-05-08

Purpose: sanitized, non-destructive manifest for Logan's Travel Bag external
SSD. This records top-level storage pressure and routing candidates without
publishing private file-level detail.

Observed on this audit pass:

| Identity field         | Observed value                  |
| ---------------------- | ------------------------------- |
| Canonical role         | Travel Bag                      |
| Windows mount observed | `F:`                            |
| Volume label observed  | ExternalSSD                     |
| Device observed        | Samsung Portable SSD T5 USB SSD |
| Filesystem observed    | exFAT                           |
| Used space             | 768.99 GB                       |
| Free space             | 162.49 GB                       |

The Windows mount path is an observation, not a persistent identity.

## Top-Level Buckets

| Bucket                               |  Files | Approx. size | Initial routing                                       |
| ------------------------------------ | -----: | -----------: | ----------------------------------------------------- |
| `IR`                                 | 10,557 |    261.62 GB | Work Desk durable archive candidate                   |
| `Science Trek`                       |  1,138 |    138.49 GB | Work Desk durable archive candidate                   |
| `Adobe Media Cache and Scratch Disk` | 14,722 |    103.43 GB | Scratch/cache review                                  |
| `DESKTOP`                            |  3,085 |     70.17 GB | Mixed dump; classify before moving                    |
| `IDEX_Artifacts_temp`                |     10 |     57.08 GB | Work/temp review; likely Work Desk after verification |
| `$RECYCLE.BIN`                       |    631 |     45.67 GB | Cleanup candidate after Logan confirmation            |
| `Social media experiments`           |    174 |     43.91 GB | Work Desk; duplicate candidate against Work Desk copy |
| `personal`                           |    174 |     39.87 GB | Home Desk sensitive category                          |
| `misc`                               |     39 |      5.28 GB | Manual review                                         |
| `temp`                               |     58 |      1.17 GB | Cleanup/review candidate                              |
| `Assets`                             |     15 |      0.13 GB | Manual review                                         |
| `readme`                             |      3 |      0.02 GB | Keep/review                                           |
| `.Spotlight-V100`                    |     95 |      0.02 GB | macOS metadata                                        |
| `.Trashes`                           |     40 |      0.01 GB | Cleanup candidate after Logan confirmation            |
| `PREMIERE EXPORTS`                   |      7 |     <0.01 GB | Work Desk or retire after review                      |
| `PSAutoRecover`                      |      0 |     <0.01 GB | Application recovery folder; review                   |
| `.TemporaryItems`                    |      0 |     <0.01 GB | macOS temporary metadata                              |
| `System Volume Information`          |      2 |     <0.01 GB | Windows system metadata                               |
| `.fseventsd`                         |      9 |     <0.01 GB | macOS filesystem metadata                             |

## Pressure Summary

Travel Bag is not currently lean. It is carrying:

- about 501 GB of durable professional/media archive candidates:
  `IR`, `Science Trek`, `IDEX_Artifacts_temp`, and
  `Social media experiments`
- about 150 GB of likely scratch/cleanup candidates:
  `Adobe Media Cache and Scratch Disk`, `$RECYCLE.BIN`, `temp`, and `.Trashes`
- about 40 GB of sensitive personal material that should route toward Home Desk
  after confirmation
- about 70 GB of unclassified desktop dump material requiring subfolder review

## Recommended Non-Destructive Order

1. Confirm whether `Adobe Media Cache and Scratch Disk` can be treated as
   disposable scratch.
2. Confirm whether `$RECYCLE.BIN` and `.Trashes` can be emptied.
3. Compare `Social media experiments` with the Work Desk copy before deleting or
   retiring either side.
4. Treat `IR`, `Science Trek`, and verified IDEX artifacts as Work Desk offload
   candidates.
5. Treat `personal` as Home Desk offload candidate and avoid public detailed
   manifests.
6. Classify `DESKTOP` and `misc` by subfolder before deciding any movement.

## Guardrails

- No deletion in the first pass.
- No file-level public manifest for `personal`.
- No reliance on `F:` as a persistent identity.
- No cache/recycle cleanup without Logan confirmation.
- No duplicate retirement without checksum or equivalent evidence.
