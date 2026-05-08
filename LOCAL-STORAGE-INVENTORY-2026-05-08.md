---
title: "Local Storage Inventory"
updated: 2026-05-08
status: active
authority: "LOGAN"
---

# Local Storage Inventory - 2026-05-08

Purpose: sanitized, folder-level inventory for later drive-role and migration planning.

This pass was read-only. No files were moved, copied, deleted, renamed, repaired,
formatted, deduplicated, or rewritten.

## Drive Summary

| Drive | Label | Device | Filesystem | Approx. size | Approx. free | Health |
| --- | --- | --- | --- | ---: | ---: | --- |
| `C:` | Windows | Samsung SSD 990 PRO 2TB | NTFS | 1.82 TB | 578 GB | Healthy |
| `D:` | LoganF | WD easystore 2624 USB HDD | exFAT | 4.55 TB | 3.49 TB | Healthy |
| `E:` | Expansion | Seagate Expansion HDD USB | exFAT | 3.64 TB | 2.99 TB | Healthy |
| `F:` | ExternalSSD | Samsung Portable SSD T5 USB SSD | exFAT | 931 GB | 162 GB | Healthy |

## Top-Level Folder Summary

### `D:` LoganF

Largest top-level buckets:

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `School` | 48,267 | 788.89 GB |
| `IR` | 1,488 | 58.34 GB |
| `IDLEG.fcpbundle` | 3,219 | 51.26 GB |
| `IDAHO PTV 5-15-2020` | 1,556 | 39.89 GB |
| `Legislature` | 708 | 29.21 GB |
| `Videos2` | 500 | 28.63 GB |
| `personal` | 209 | 18.31 GB |
| `!Photos` | 4,515 | 12.76 GB |
| `Dialogue` | 1,345 | 12.28 GB |
| `!Manuals/Installers` | 44 | 9.86 GB |
| `Idaho Debates` | 72 | 3.07 GB |
| `!Filing Cabinet` | 7,725 | 2.16 GB |

Notes:
- Contains many macOS sidecar files (`._*`) and macOS metadata folders.
- Contains historical personal, school, media, and production buckets.

### `E:` Expansion

Largest top-level buckets:

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `Idaho Reports` | 4,088 | 452.61 GB |
| `Legislature` | 949 | 71.00 GB |
| `Social media experiments` | 174 | 43.91 GB |
| `Dialogue` | 1,382 | 38.30 GB |
| `FYIdaho` | 209 | 29.22 GB |
| `$RECYCLE.BIN` | 61 | 20.63 GB |
| `Idaho Debates` | 153 | 3.28 GB |
| `IDEX` | 48 | 0.31 GB |
| `OI` | 50 | 0.20 GB |

Notes:
- Strong Idaho Reports / Legislature / production-media profile.
- `$RECYCLE.BIN` is large enough to matter in future cleanup planning.

### `F:` ExternalSSD

Largest top-level buckets:

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `IR` | 10,557 | 261.62 GB |
| `Science Trek` | 1,138 | 138.49 GB |
| `Adobe Media Cache and Scratch Disk` | 14,722 | 103.43 GB |
| `DESKTOP` | 3,085 | 70.17 GB |
| `IDEX_Artifacts_temp` | 10 | 57.08 GB |
| `$RECYCLE.BIN` | 631 | 45.67 GB |
| `Social media experiments` | 174 | 43.91 GB |
| `personal` | 174 | 39.87 GB |
| `misc` | 39 | 5.28 GB |
| `temp` | 58 | 1.17 GB |

Notes:
- Least free space of the three external drives.
- Contains active/scratch-looking buckets plus large durable media buckets.
- Future planning should separate true scratch/cache from archive-worthy material.

## Local And Cloud-Synced Roots

### Local User Buckets

| Bucket | Files | Approx. size |
| --- | ---: | ---: |
| `AppData/Local` | 616,944 | 56.25 GB |
| `Desktop` | 1,458 | 37.97 GB |
| `AppData/Roaming` | 89,486 | 27.58 GB |
| `Videos` | 39 | 8.61 GB |
| `Downloads` | 18 | < 0.01 GB |
| `Pictures` | 2 | < 0.01 GB |
| `Music` | 2 | 0.01 GB |

Notes:
- `AppData` is high-churn application state, not a normal migration target.
- `Desktop` is the largest normal user-facing local bucket outside `Documents`.

### `Documents`

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `IDAHO-VAULT` | 145,040 | 665.47 GB |
| `IDAHO-VAULT-history-rewrite.git` | 812 | 0.39 GB |
| `IDAHO-VAULT-agent-fix` | 35,018 | 0.07 GB |
| `IDAHO-VAULT-CLEAN` | 20,587 | 0.07 GB |
| `IDAHO-VAULT-pr-high` | 35,017 | 0.07 GB |
| `IDAHO-VAULT-pr-low` | 35,017 | 0.07 GB |
| `Codex` | 3 | < 0.01 GB |

Notes:
- `IDAHO-VAULT` dominates local `Documents` by size.
- Git worktrees/history-rewrite siblings should be treated as development surfaces,
  not ordinary document folders.

### OneDrive - Idaho Public Television

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `Documents` | 868 | 5.96 GB |
| `IR Online` | 119 | 1.31 GB |
| `Interview Questions` | 45 | < 0.01 GB |
| `Pictures` | 3 | < 0.01 GB |
| `Show Bites` | 1 | < 0.01 GB |

Notes:
- This root is much smaller than the external media drives.
- Treat as cloud-synced working material, not bulk archive.

### Creative Cloud Files

| Top-level bucket | Files | Approx. size |
| --- | ---: | ---: |
| `Blog-Podcast Promo Assets` | 242 | 6.19 GB |
| `Adobe` | 6 | 0.07 GB |
| `IR YouTube-Podcast` | 6 | 0.05 GB |
| `Audition` | 3 | < 0.01 GB |

Notes:
- Small enough for targeted review rather than bulk drive-role migration.
- Likely tied to Adobe/cloud workflows; do not move without checking sync behavior.

## Broad File-Type Profile

Largest extension groups across inventoried local/external roots:

| Extension/category | Files | Approx. size |
| --- | ---: | ---: |
| `.mov` | 3,798 | 895.77 GB |
| `.mp4` | 1,783 | 803.18 GB |
| `[no extension]` | 29,879 | 543.70 GB |
| `.mxf` | 420 | 520.17 GB |
| `.aecache` | 14,126 | 101.61 GB |
| `.cfa` | 4,844 | 82.94 GB |
| `.wav` | 646 | 80.83 GB |
| `.mp3` | 1,837 | 37.40 GB |
| `.mts` | 114 | 19.27 GB |
| `.cr2` | 2,050 | 18.15 GB |
| `.jpg` | 18,407 | 17.71 GB |
| `.zip` | 354 | 15.07 GB |
| `.iso` | 6 | 9.79 GB |
| `.psd` | 450 | 8.83 GB |
| `.mkv` | 35 | 8.58 GB |
| `.pdf` | 1,864 | 3.01 GB |
| `.prproj` | 1,779 | 1.75 GB |

Notes:
- Video and production media dominate total storage.
- Adobe cache/proxy artifacts are large enough to deserve separate retention rules.
- `[no extension]` is too large to classify from extension alone; review by top-level
  bucket before moving or deleting anything.

## Cross-Drive Overlap Candidates

These top-level names or categories appear on multiple drives and should be
reviewed before assigning drive roles:

| Candidate | Seen on | Planning note |
| --- | --- | --- |
| `IR` / `Idaho Reports` | `D:`, `E:`, `F:`, OneDrive | likely same domain, not proven duplicates |
| `Legislature` | `D:`, `E:` | likely public-affairs source/media category |
| `Dialogue` | `D:`, `E:` | likely duplicated or related historical material |
| `Idaho Debates` | `D:`, `E:` | likely related production/media set |
| `Paperwork` | `D:`, `E:` | low-size, review manually |
| `personal` | `D:`, `F:` | sensitive category; avoid public detailed manifests |
| `PREMIERE EXPORTS` | `D:`, `F:` | likely production output, low reported current size |
| `Social media experiments` | `E:`, `F:` | same size and file count in this pass; strong duplicate candidate |
| `$RECYCLE.BIN` | `E:`, `F:` | cleanup candidate, but only after manual confirmation |

## Draft Routing Candidates

Non-binding hypotheses for Phase 2:

- Keep `C:` focused on operating system, applications, active git/dev work, and
  current sync roots.
- Treat `F:` as too full for additional archive intake until scratch/cache and
  recycle-bin contents are reviewed.
- Treat `D:` as the largest available archive candidate, but note that it already
  contains large historical personal/school/photo material.
- Treat `E:` as a strong Idaho Reports / Legislature / production-media candidate,
  pending duplicate review against `D:` and `F:`.
- Separate Adobe cache/scratch material from durable production masters before
  any migration.

## Deferred Decisions

No decisions were made in this phase about:

- canonical drive roles
- duplicate deletion
- archive vs. active-working status
- cloud sync restructuring
- git/LFS remediation
- moving or splitting `IDAHO-VAULT`

Recommended next phase: choose drive roles using this report, then build a private
detailed manifest only for the specific buckets selected for migration or dedupe.
