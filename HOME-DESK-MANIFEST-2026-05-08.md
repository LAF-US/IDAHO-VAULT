---
title: "Home Desk Manifest"
updated: 2026-05-08
status: draft
authority: "LOGAN"
related:
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
  - WORK-DESK-MANIFEST-2026-05-08
---

# Home Desk Manifest - 2026-05-08

Purpose: sanitized, non-destructive manifest for Logan's Home Desk external
drive. This records top-level storage shape and routing candidates without
publishing personal file-level detail.

Observed on this audit pass:

| Identity field         | Observed value            |
| ---------------------- | ------------------------- |
| Canonical role         | Home Desk                 |
| Windows mount observed | `D:`                      |
| Volume label observed  | LoganF                    |
| Device observed        | WD easystore 2624 USB HDD |
| Filesystem observed    | exFAT                     |
| Used space             | 1111.53 GB                |
| Free space             | 3545.67 GB                |

The Windows mount path is an observation, not a persistent identity.

## Top-Level Buckets

| Bucket                              |  Files | Approx. size | Initial routing                                  |
| ----------------------------------- | -----: | -----------: | ------------------------------------------------ |
| `School`                            | 48,267 |    788.89 GB | Home Desk core archive                           |
| `IR`                                |  1,488 |     58.34 GB | Work Desk candidate; compare before moving       |
| `IDLEG.fcpbundle`                   |  3,219 |     51.26 GB | Work Desk candidate; Final Cut bundle            |
| `IDAHO PTV 5-15-2020`               |  1,556 |     39.89 GB | Work Desk candidate                              |
| `Legislature`                       |    708 |     29.21 GB | Work Desk candidate                              |
| `Videos2`                           |    500 |     28.63 GB | Manual review; likely mixed media                |
| `personal`                          |    209 |     18.31 GB | Home Desk sensitive category                     |
| `!Photos`                           |  4,515 |     12.76 GB | Home Desk photo archive unless reclassified      |
| `Dialogue`                          |  1,345 |     12.28 GB | Work Desk candidate; compare with Work Desk copy |
| `!Manuals/Installers`               |     44 |      9.86 GB | Home Desk tools/archive candidate                |
| `Idaho Debates`                     |     72 |      3.07 GB | Work Desk candidate; compare with Work Desk copy |
| `!Filing Cabinet`                   |  7,725 |      2.16 GB | Home Desk records archive                        |
| `~Gilberto`                         |     27 |      0.49 GB | Manual review                                    |
| `Quotes & Words`                    |    227 |      0.48 GB | Home Desk creative/personal archive              |
| `Phi Mu Alpha`                      |    300 |      0.31 GB | Home Desk music/personal archive                 |
| `!FREELANCE`                        |     48 |      0.21 GB | Manual review; may bridge personal/professional  |
| `Design`                            |  8,329 |      0.18 GB | Manual review                                    |
| `Things I Made`                     |    289 |      0.13 GB | Home Desk creative/personal archive by default   |
| `Mother's Day 2014.pages`           |    162 |      0.10 GB | Home Desk personal archive                       |
| `DSA`                               |     81 |      0.06 GB | Manual review                                    |
| `~LaCie_readme (orange hard drive)` |     26 |      0.02 GB | Legacy drive note/reference                      |
| `.Spotlight-V100`                   |     75 |      0.02 GB | macOS metadata                                   |
| `Sheet Music`                       |    134 |      0.02 GB | Home Desk music/personal archive                 |
| `Pride`                             |     12 |      0.01 GB | Home Desk personal archive by default            |
| `.TemporaryItems`                   |      0 |     <0.01 GB | macOS temporary metadata                         |
| `PREMIERE EXPORTS`                  |     10 |     <0.01 GB | Work Desk candidate                              |
| `$RECYCLE.BIN`                      |      1 |     <0.01 GB | Cleanup candidate after Logan confirmation       |
| `System Volume Information`         |      2 |     <0.01 GB | Windows system metadata                          |
| `Paperwork`                         |     19 |     <0.01 GB | Home Desk records archive by default             |
| `.Trashes`                          |      4 |     <0.01 GB | Cleanup candidate after Logan confirmation       |

## Storage Role Assessment

Home Desk has the largest free-space pool and the broadest personal/history
profile. It is suitable for personal archive, older school material, paperwork,
photos, music, creative material, and temporary staging during careful sorting.

It also contains professional/media buckets that probably belong on Work Desk
after review:

- `IR`
- `IDLEG.fcpbundle`
- `IDAHO PTV 5-15-2020`
- `Legislature`
- `Dialogue`
- `Idaho Debates`
- `PREMIERE EXPORTS`

These are routing candidates only. They are not proven duplicates and should not
be merged or deleted without comparison evidence.

## Recommended Non-Destructive Order

1. Keep `School`, `personal`, `!Photos`, `!Filing Cabinet`, `Phi Mu Alpha`,
   `Sheet Music`, and similar personal/history buckets on Home Desk unless
   Logan reclassifies specific subfolders.
2. Compare Home Desk `IR` against Work Desk `Idaho Reports` and Travel Bag `IR`
   before moving any professional media.
3. Compare Home Desk `Dialogue`, `Idaho Debates`, and `Legislature` against Work
   Desk equivalents before consolidation.
4. Review `IDLEG.fcpbundle` and `IDAHO PTV 5-15-2020` as professional media
   candidates for Work Desk.
5. Treat `!FREELANCE`, `Design`, `Videos2`, `DSA`, and `~Gilberto` as manual
   review buckets before assigning final lanes.

## Guardrails

- No deletion in the first pass.
- No file-level public manifest for personal/history buckets.
- Do not use `D:` as a persistent identity.
- Do not move Final Cut bundles without preserving bundle integrity.
- Do not merge same-named or related professional buckets without checksum or
  equivalent evidence.
