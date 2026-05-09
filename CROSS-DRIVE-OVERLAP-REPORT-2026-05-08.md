---
title: "Cross-Drive Overlap Report"
updated: 2026-05-08
status: draft
authority: "LOGAN"
related:
  - HOME-DESK-MANIFEST-2026-05-08
  - WORK-DESK-MANIFEST-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
---

# Cross-Drive Overlap Report - 2026-05-08

Purpose: identify likely overlaps among Logan's three external-drive roles
before migration, cleanup, or duplicate retirement.

This pass is non-destructive. No files were moved, copied, deleted, renamed,
deduplicated, or checksummed.

Observed local mounts during this pass:

| Canonical role | Observed Windows mount | Observed volume label |
| -------------- | ---------------------- | --------------------- |
| Home Desk      | `D:`                   | LoganF                |
| Work Desk      | `E:`                   | Expansion             |
| Travel Bag     | `F:`                   | ExternalSSD           |

The mount paths are local observations, not persistent device identities.

## Summary

The safest first overlap is `Social media experiments` across Work Desk and
Travel Bag. A live relative-path-and-size comparison found 174 files on each
side, with all 174 matching by relative path and byte size.

The largest unresolved professional overlap is the `IR` / `Idaho Reports` family
across all three drives. It is not safe to treat these as duplicates by name
alone: sizes and file counts differ substantially.

Second-pass light comparisons found that `Idaho Debates`, `Legislature`, and
`Dialogue` are partial overlaps between Home Desk and Work Desk. They contain
some matching relative paths and sizes, but also substantial role-specific
material.

## High-Priority Overlaps

| Overlap family                 | Roles observed                   | Live size/count signal                                                                                                                                                | Risk       | Recommended next action                                                                                              |
| ------------------------------ | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------- |
| `Social media experiments`     | Work Desk, Travel Bag            | Work Desk: 174 files / 43.91 GB. Travel Bag: 174 files / 43.91 GB. Relative path + size match: 174/174.                                                               | Low        | Optional checksum sample or full checksum, then mark Travel Bag copy as retirement candidate after Logan approval.   |
| `IR` / `Idaho Reports`         | Home Desk, Work Desk, Travel Bag | Home Desk `IR`: 1,488 files / 58.34 GB. Work Desk `Idaho Reports`: 4,088 files / 452.61 GB. Travel Bag `IR`: 10,557 files / 261.62 GB.                                | High       | Build subfolder-level maps before any merge. Do not equate by name alone.                                            |
| `Legislature`                  | Home Desk, Work Desk             | Home Desk: 708 files / 29.21 GB. Work Desk: 949 files / 71.00 GB. Relative path + size match: 515. Size mismatches: 2. Home Desk only: 191. Work Desk only: 432.      | Medium     | Treat as partial overlap. Preserve both sides until unmatched files are reviewed.                                    |
| `Dialogue`                     | Home Desk, Work Desk             | Home Desk: 1,345 files / 12.28 GB. Work Desk: 1,382 files / 38.30 GB. Relative path + size match: 634. Size mismatches: 27. Home Desk only: 684. Work Desk only: 721. | Medium     | Treat as partial overlap with divergent content. Review mismatches and unmatched sets before consolidation.          |
| `Idaho Debates`                | Home Desk, Work Desk             | Home Desk: 72 files / 3.07 GB. Work Desk: 153 files / 3.28 GB. Relative path + size match: 61. Size mismatches: 0. Home Desk only: 11. Work Desk only: 92.            | Medium-low | Treat as partial overlap. Work Desk appears more complete by count; verify unmatched files before retiring anything. |
| `IDEX` / `IDEX_Artifacts_temp` | Work Desk, Travel Bag            | Work Desk `IDEX`: 48 files / 0.31 GB. Travel Bag `IDEX_Artifacts_temp`: 10 files / 57.08 GB.                                                                          | High       | Review temp artifacts manually before archive classification. Size profile implies different payloads.               |

## Cleanup-Adjacent Overlaps

These are not duplicate families, but they affect migration capacity:

| Category              | Roles observed                   |                                                                                                              Size signal | Recommended next action                                                                          |
| --------------------- | -------------------------------- | -----------------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------ |
| Recycle/trash buckets | Work Desk, Travel Bag, Home Desk | Travel Bag `$RECYCLE.BIN`: 45.67 GB; Work Desk `$RECYCLE.BIN`: 20.63 GB; Home Desk recycle/trash negligible in manifest. | Empty only after Logan confirmation.                                                             |
| Adobe cache/scratch   | Travel Bag                       |                                                                                                                103.43 GB | Confirm whether disposable scratch. This is likely the fastest safe way to make Travel Bag lean. |
| macOS metadata        | Home Desk, Travel Bag            |                                                                                                                    Small | Leave alone unless a later cleanup pass targets cross-OS metadata intentionally.                 |

## Role Routing Implications

### Home Desk

Home Desk should retain personal/history anchors such as `School`, `personal`,
`!Photos`, `!Filing Cabinet`, music, and older creative material.

Professional buckets on Home Desk should be considered Work Desk candidates only
after comparison:

- `IR`
- `IDLEG.fcpbundle`
- `IDAHO PTV 5-15-2020`
- `Legislature`
- `Dialogue`
- `Idaho Debates`
- `PREMIERE EXPORTS`

### Work Desk

Work Desk is the professional receiving lane. It already contains the strongest
professional archive shape and has enough free space to receive verified durable
professional material from Travel Bag and Home Desk.

Work Desk should not absorb material blindly. The `IR` / `Idaho Reports` family
requires subfolder-level comparison first.

### Travel Bag

Travel Bag should be made lean. The report identifies three different classes:

- verified duplicate candidate: `Social media experiments`
- durable professional offload candidates: `IR`, `Science Trek`,
  `IDEX_Artifacts_temp`
- likely cleanup/scratch candidates: `Adobe Media Cache and Scratch Disk`,
  `$RECYCLE.BIN`, `temp`, `.Trashes`

## Recommended Verification Order

1. Finish `Social media experiments` verification because the relative-path and
   size match is already exact.
2. Build subfolder-level maps for `IR` / `Idaho Reports` across all three
   roles.
3. Review unmatched `Idaho Debates`, `Legislature`, and `Dialogue` sets before
   any consolidation.
4. Review `IDEX_Artifacts_temp` manually before deciding whether it belongs in
   Work Desk `IDEX`, another Work Desk lane, or a temporary cleanup lane.
5. Only after Logan approval, perform cleanup actions for recycle/trash or
   cache/scratch categories.

## Guardrails

- No deletion without Logan approval.
- No duplicate retirement without checksum or equivalent evidence.
- No public file-level manifest for personal folders.
- No reliance on `D:`, `E:`, or `F:` as persistent identities.
- No Final Cut bundle movement without preserving bundle integrity.
- Same names across drives are evidence of overlap, not proof of duplication.
