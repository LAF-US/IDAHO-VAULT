---
title: "DEFRAG-MAP"
created: 2026-05-12
description: "Full inventory of digital assets across all services and devices — the coordination document for life defrag consolidation to MacBook 5TB drive."
tags:
  - defrag
  - inventory
  - consolidation
doc_class: misc_reference
status: live
---

# DEFRAG-MAP — Digital Life Inventory

**Purpose:** Map everything that exists, everywhere, before moving anything. Once both sides (Windows + MacBook) are filled in, use this to build the pull priority stack.

**Snapshot date:** 2026-05-12  
**Windows inventory by:** Claude (Windows session)  
**MacBook inventory by:** *MacBook Claude — fill in Section B*

---

## Section A — Windows Machine Inventory (loganfinney27@gmail.com)

### A1. Windows Local (`C:\Users\loganf\`)

| Folder | Size | Disposition |
|---|---|---|
| `Documents\` | 317 GB | Being pushed → INGEST now (~7% done) |
| `Desktop\` (SCRATCH FOLDER) | 38 GB | Being pushed → INGEST now |
| `Videos\` | 8.6 GB | Being pushed → INGEST now |
| `Creative Cloud Files …avid4@idahoptv.org…\` | 6.32 GB | Being pushed → INGEST now (work Adobe assets) |
| `OneDrive - Idaho Public Television\` | 7.27 GB | **Work-managed — do NOT include in personal consolidation** |
| `CrossDevice\` (Pixel 10 Pro) | 5.22 GB | Phone Link mirror — ephemeral, skip |
| `Downloads\` | ~43 MB | Pushed → INGEST (done — HR/FMLA docs, resume) |
| `.ssh\` | ~470 B | Pushed → INGEST (done) |
| `node_modules\`, `scoop\`, `openclaw_env\`, `.sbx-denybin\`, `.ollama\` | — | Rebuild artifacts — **skip** |
| `OneDrive\` (personal stub) | 0 B | Not synced locally; cloud copy is canonical |

**INGEST transfer status as of ~12:30:**
- 25.5 GB transferred of ~370 GB total (~7% complete)
- Folders in INGEST: `Documents/`, `Desktop-SCRATCH/`, `Videos/`, `Creative-Cloud-Files/`, `Downloads/`, `.ssh/`
- ETA: ~1-2 hours remaining (Videos + CC-Files are the tail)

### A2. Work OneDrive (`OneDrive - Idaho Public Television\`, 7.27 GB)

Active journalism folders — work-managed by Idaho PTV, NOT for personal consolidation:

| Folder | Last Modified | Notes |
|---|---|---|
| `Documents\` | 2026-05-08 | Active work docs |
| `Interview Questions\` | 2026-05-08 | Active reporting |
| `IR Online\` | 2026-05-08 | Idaho Reports online content |
| `Show Bites\` | 2026-05-08 | Active show content |
| `Meetings\` | 2026-02-10 | Meeting notes |
| `Recordings\` | 2026-02-10 | Audio/video recordings |
| `Pictures\` | 2026-05-08 | Work photos |
| `Scans\` | 2024-10-01 | Scanned docs |
| `Whiteboards\` | 2026-04-06 | |
| `Microsoft Teams Chat Files\` | 2026-04-06 | |
| `Attachments\` | 2026-04-15 | |

**Decision:** Include in archaeology for awareness, but keep separate from personal archive. Do NOT mix with personal content on 5TB.

---

## Section B — MacBook / 5TB External Inventory

*MacBook Claude: please fill this section in and commit.*

### B1. MacBook Local (`~/` or equivalent)

| Folder | Size | Notes |
|---|---|---|
| *(MacBook Claude to fill in)* | | |

### B2. 5TB External Drive

| Location | Size | Notes |
|---|---|---|
| *(MacBook Claude to fill in)* | | |

**Key questions for MacBook Claude:**
- What's already on the 5TB drive? Any prior consolidation attempts?
- How much free space is available on the 5TB?
- Is rclone configured on the MacBook? (`rclone listremotes`)
- Can it reach `gdrive-personal:INGEST/windows-2026-05-12/` to pull the Windows content?

---

## Section C — Cloud Services Inventory

### C1. Google Drive Personal (`gdrive-personal:`, ~526 GB used / 5 TB total)

**Top-level folders:**

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Archive/` | 12.6 GB | 1,891 | 123 Google Docs/Sheets (unknown size — underestimate). 2 dangling shortcuts. Oldest content (2018). |
| `FINNEY FaVS News/` | 46 MB | 26 | FaVS News journalism content, 10 Google native docs |
| `Google Earth/` | 0 B | 0 | Empty |
| `Idaho PTV/` | 14.6 GB | 648 | 181 Google native docs (underestimate). 3 dangling shortcuts. Journalism/production files. |
| `Photos/` | 2.5 GB | 989 | Drive-linked photos only. Actual Google Photos library much larger — see Takeout. |
| `Saved from Chrome/` | 3.3 MB | 3 | Tiny |
| `Takeout/` | 121.4 GB | 57 | **54 Takeout zips from 2026-05-03 + 3 journalism video files.** Almost certainly a Google Photos export. This may explain the "missing" ~350 GB in Drive quota (Google Photos stored separately but counted in quota). |
| `INGEST/windows-2026-05-12/` | 25.5 GB (growing) | 12,545 | Active Windows push — in progress |

**Google Drive native files** (Docs, Sheets, Slides) have unknown size in rclone — counts are underestimates. Actual Drive storage is ~526 GB per account settings.

### C2. Dropbox (`dropbox:`)

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Camera Uploads/` | 5.2 GB | 884 | Phone camera auto-uploads |
| `Apps/remotely-save/` | 0 B | 0 | Obsidian Remotely Save plugin — empty/unused |

**Total accessible via rclone: ~5.2 GB**

**Important discrepancy:** Dropbox account dashboard shows ~309 GB used. The gap (~304 GB) is likely in **shared/team folders** that rclone cannot see with default settings. To access: `rclone config` → set `shared_folders = true` for the dropbox remote, or use `rclone lsd dropbox: --drive-shared-with-me`. Investigate before assuming Dropbox is small.

### C3. OneDrive Personal (`onedrive:`)

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Imports/` | 139.3 GB | 1,539 | **The bulk** — likely large media/photo import |
| `Pictures/` | 5.7 GB | 788 | Photo library |
| `Attachments/` | 0 B | 0 | Empty |
| `Documents/` | 0 B | 0 | Empty |
| `Personal Vault/` | *(locked)* | — | Requires additional auth — rclone errors on it |

**Total accessible: ~145 GB** (matches account size — Personal Vault likely small)

---

## Section D — Excluded / Out of Scope

| Service/Location | Size | Reason |
|---|---|---|
| `gcs:` (Google Cloud Storage) | — | IDAHO-VAULT infrastructure — **never include in personal backup** |
| `the-ledger-bucket:` | — | IDAHO-VAULT infrastructure — **never include in personal backup** |
| `archive:` (Internet Archive) | — | Publishing endpoint, not personal storage |
| `box:` | — | Not yet inventoried; low priority |
| Work Adobe CC (`Creative Cloud Files…avid4@idahoptv.org…`) | 6.32 GB | Work assets — pushed to INGEST for awareness, but note work account |

---

## Section E — Consolidation Decision Layer

*To be filled in after MacBook Claude completes Section B.*

### E1. Pull Priority Stack (draft)

1. **INGEST/windows-2026-05-12/** → 5TB (after transfers complete, ~today)
2. **OneDrive personal Imports/** → 5TB (139 GB — largest single unknown)
3. **OneDrive personal Pictures/** → 5TB (5.7 GB)
4. **Dropbox Camera Uploads/** → 5TB (5.2 GB — likely photo duplicates)
5. **gdrive-personal existing content** → 5TB (Archive, Photos, Takeout, etc.)
6. **Dropbox shared folders** → investigate size first, then pull if personal

### E2. Known Dedup Hotspots

- Phone camera photos likely appear in: Dropbox Camera Uploads + OneDrive Pictures + gdrive Photos + CrossDevice
- Work Adobe content appears in: CC Files local + INGEST (already pushed) — flag as work
- IDAHO-VAULT git repos: in Documents → INGEST; also on GitHub — git history is canonical

### E3. Open Questions

- [ ] What is OneDrive `Imports/` (139 GB)? Media? Email archive? Needs investigation.
- [ ] What is in Dropbox shared folders (~304 GB)? Personal or work?
- [ ] How much space is free on the 5TB drive?
- [ ] Is `gdrive-personal:Photos` Google Photos backup or a separate folder?
- [ ] What's in `gdrive-personal:Takeout`? Which services/dates?
- [ ] Personal Vault contents (OneDrive) — what's locked inside?

---

## Revision Log

| Date | Change | Author |
|---|---|---|
| 2026-05-12 | Initial inventory (Windows side) | Claude (Windows) |
| | *(MacBook Claude: add your entry here)* | |
