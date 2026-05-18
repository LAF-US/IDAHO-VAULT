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
| `Documents\` | 317 GB | INGEST running — 32% objects transferred as of ~21:09; LFS blobs are bulk of remaining size. Check `D:\rclone-logs\documents-resume.log`. |
| `Desktop\` (SCRATCH FOLDER) | 38 GB | Being pushed → INGEST now |
| `Videos\` | 8.6 GB | Being pushed → INGEST now |
| `Creative Cloud Files …avid4@idahoptv.org…\` | 6.32 GB | Being pushed → INGEST now (work Adobe assets) |
| `OneDrive - Idaho Public Television\` | 7.27 GB | **Work-managed — do NOT include in personal consolidation** |
| `CrossDevice\` (Pixel 10 Pro) | 5.22 GB | Phone Link mirror — ephemeral, skip |
| `Downloads\` | ~43 MB | Pushed → INGEST (done — HR/FMLA docs, resume) |
| `.ssh\` | ~470 B | Pushed → INGEST (done) |
| `node_modules\`, `scoop\`, `openclaw_env\`, `.sbx-denybin\`, `.ollama\` | — | Rebuild artifacts — **skip** |
| `OneDrive\` (personal stub) | 0 B | Not synced locally; cloud copy is canonical |

**INGEST transfer status as of 17:53 on 2026-05-12 (all rclone processes stopped):**

| INGEST Folder | Objects | Size | Status |
|---|---|---|---|
| `Documents/` | 17,949+ | 4.759 GiB+ | **RESUMING** — restarted 2026-05-12 ~18:00. Remaining ~310 GB is `.git/lfs/objects` (321 GB LFS blob cache). Long-running. Check `D:\rclone-logs\documents-resume.log` for progress. |
| `Desktop-SCRATCH/` | 1,199 | 31.810 GiB | Complete (100%) |
| `Videos/` | 123 | ~16.6 GiB | Complete (100%) |
| `Creative-Cloud-Files/` | 259 | 12.309 GiB | Complete (100%) |
| `Downloads/` | 103 | 43 MiB | Complete (100%) |
| `.ssh/` | 2 | 470 B | Complete (100%) |
| **TOTAL** | **19,521** | **51.491 GiB** | Documents transfer must be resumed |

**Note on Documents:** 315 of the 317 GB is `IDAHO-VAULT/.git/lfs/objects` (321 GB LFS blob cache — mp4 videos, PDFs stored as SHA256-named binary files). Working tree markdown content transferred in first run. Second run (resumed 2026-05-12 ~18:00) uploading the LFS blob store. Will run for many hours. Log: `D:\rclone-logs\documents-resume.log`.

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
| `Archive/` | 12.6 GB | 1,891 | 123 Google Docs/Sheets (unknown size — underestimate). 2 dangling shortcuts. Personal/misc storage: Finney Project FARE, car insurance, NIDSA, Reclaim ID, School. Oldest content (2018). |
| `FINNEY FaVS News/` | 46 MB | 26 | FaVS News journalism content, 10 Google native docs |
| `Google Earth/` | 0 B | 0 | Empty |
| `Idaho PTV/` | 14.6 GB | 648 | 181 Google native docs (underestimate). 3 dangling shortcuts. Journalism/production files. |
| `Photos/` | 2.5 GB | 989 | **Manual folder, NOT Google Photos library.** 10 subfolders of personal/family media (2015–2020): PILLOWMAN videos, Adam Dunes 2015, Boise Women's March 2020, Cody Finney, Mom, Tracie Finney, Tim Malm, Uni-Presidents-JFAC, etc. Google Photos library is in Takeout group 5. |
| `Saved from Chrome/` | 3.3 MB | 3 | Tiny |
| `Takeout/` | 121.4 GB | 57 | **Google Takeout export from 2026-05-03T18:29Z.** 54 zips in 3 service groups: group 5 (40 zips ~80 GB = Google Photos), group 7 (13 zips ~26 GB), group 9 (3 zips ~6 GB, probably Drive/Mail/etc.), 1 index zip (1 MB). Plus 3 journalism video files (Sweet Land of Liberty, Pillowman reel, IDEX Artifacts). |
| `INGEST/windows-2026-05-12/` | 25.5 GB (growing) | 12,545 | Active Windows push — in progress |

**Google Drive native files** (Docs, Sheets, Slides) have unknown size in rclone — counts are underestimates. Actual Drive storage is ~526 GB per account settings.

### C2. Dropbox (`dropbox:`)

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Camera Uploads/` | 5.2 GB | 884 | Phone camera auto-uploads. Date range: **2025-09-06 to 2026-05-12** — recent 8 months only. Likely overlaps with CrossDevice/OneDrive Pictures. |
| `Apps/remotely-save/` | 0 B | 0 | Obsidian Remotely Save plugin — empty/unused |

**Total accessible via rclone: ~5.2 GB**

**304 GB gap — investigated 2026-05-12:**
- `rclone about dropbox:` confirms 309 GB used against 2 TB quota
- `rclone lsd dropbox: --dropbox-shared-folders` returns **nothing** — no shared folders accessible via API
- This means the 304 GB is **not** shared-with-me folders (those would surface via the flag)
- Most likely candidates: (a) **Dropbox Paper documents** (count toward quota but aren't in the file API), (b) orphaned blocks from a previously connected device that has since been unlinked, or (c) files in a team/work Dropbox namespace not visible on personal account
- **Action required:** Check Dropbox web → left sidebar → "Paper" for documents; and Settings → Connected devices for orphaned storage. Until confirmed personal content, treat Dropbox as 5.2 GB accessible.

### C3. OneDrive Personal (`onedrive:`)

| Folder | Size | Files | Notes |
|---|---|---|---|
| `Imports/` | 139.3 GB | 1,539 | **⚠️ DUPLICATE of gdrive-personal** — see note below |
| `Pictures/` | 5.7 GB | 788 | Photo library |
| `Attachments/` | 0 B | 0 | Empty |
| `Documents/` | 0 B | 0 | Empty |
| `Personal Vault/` | *(locked)* | — | Requires additional Microsoft auth — rclone returns `invalidResourceId` error |

**Total accessible: ~145 GB** (matches account size — Personal Vault likely small or empty)

**⚠️ CRITICAL DEDUP FINDING — OneDrive Imports:**
`onedrive:Imports/loganfinney27@gmail.com - Google Drive/` contains the **exact same folder structure** as `gdrive-personal:`:
- Archive, FINNEY FaVS News, Google Earth, Idaho PTV, Photos, Saved from Chrome, Takeout
- This was a Microsoft OneDrive import of Google Drive (run ~2026-05-04, matching last modified dates)
- **139.3 GB of OneDrive Imports is a direct copy of gdrive-personal content**
- **Decision: gdrive-personal is canonical. Do NOT pull OneDrive Imports to 5TB separately — it would create pure redundancy. Skip or delete the OneDrive import after verifying gdrive-personal is intact.**

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

### E1. Pull Priority Stack (updated 2026-05-12)

1. **Resume Documents INGEST** → run `rclone copy "C:\Users\loganf\Documents" "gdrive-personal:INGEST/windows-2026-05-12/Documents"` (stopped at 64%)
2. **INGEST/windows-2026-05-12/** → MacBook pull to 5TB (after Documents transfer completes)
3. **gdrive-personal existing content** → 5TB (Archive 12.6GB, Idaho PTV 14.6GB, Photos 2.5GB, Takeout 121.4GB)
4. **Dropbox Camera Uploads/** → 5TB (5.2 GB — likely photo duplicates, dedupe after pull)
5. **OneDrive Pictures/** → 5TB (5.7 GB — check for overlap with Dropbox Camera Uploads)
6. **~~OneDrive Imports/~~** → **SKIP** — confirmed duplicate of gdrive-personal
7. **Dropbox Paper + orphan investigation** → web interface only; not pullable via rclone

### E2. Known Dedup Hotspots

- **OneDrive Imports = gdrive-personal copy** (139.3 GB duplicated) — delete Imports after verifying gdrive is intact
- Phone camera photos likely appear in: Dropbox Camera Uploads + OneDrive Pictures + gdrive Photos + CrossDevice
- Work Adobe content: CC Files local + INGEST (already pushed) — flag as work
- IDAHO-VAULT git repos: in Documents → INGEST; also on GitHub — git history is canonical
- `gdrive-personal:Takeout/` (121.4 GB, 54 zips from 2026-05-03) — likely Google Photos export; don't double-import if Photos are already in drive/INGEST

### E3. Open Questions / Blockers

**Requires Logan action in browser:**
- [ ] **GitHub LFS budget** — push blocked. Buy data pack at `github.com/settings/billing` → "Git LFS Data" ($5/mo, 50 GB). One pack should unblock `git push origin main`.
- [ ] **Dropbox 304 GB gap** — not shared folders (API confirmed nothing). Check `dropbox.com` → left sidebar → "Paper" for doc count; Settings → Connected Devices for orphaned storage.
- [ ] **OneDrive Personal Vault** — locked. Open `onedrive.live.com` → Personal Vault → authenticate. Likely near-empty (Imports+Pictures already = 145 GB of 145 GB quota).

**Requires MacBook Claude:**
- [ ] Section B (MacBook local + 5TB inventory) — `git pull` IDAHO-VAULT then fill in and commit.

**Resolved/In-progress:**
- [x] ~~Documents transfer needs resumption~~ — **RUNNING** as of ~18:00. Check `D:\rclone-logs\documents-resume.log`.
- [x] ~~What is OneDrive `Imports/` (139 GB)?~~ — Answered: direct copy of gdrive-personal from 2026-05-04.
- [ ] How much free space on the 5TB drive? (MacBook Claude to answer in Section B)
- [x] ~~Is `gdrive-personal:Photos` Google Photos backup or a separate folder?~~ — **Manual folder, personal/family media 2015–2020. NOT Google Photos.**
- [x] ~~What's in `gdrive-personal:Takeout`?~~ — **Confirmed: Google Takeout export from 2026-05-03. Group 5 (40 zips, ~80 GB) = Google Photos library. Groups 7+9 = other services. Plus 3 journalism videos.**

---

## Revision Log

| Date | Change | Author |
|---|---|---|
| 2026-05-12T12:30 | Initial inventory (Windows side) | Claude (Windows) |
| 2026-05-12T18:00 | Updated INGEST status; investigated Dropbox gap (no shared folders via API); identified OneDrive Imports as gdrive-personal duplicate; updated pull priority stack | Claude (Windows) |
| 2026-05-12T18:35 | Resumed Documents transfer (321 GB LFS blobs); clarified blockers requiring Logan vs MacBook action | Claude (Windows) |
| 2026-05-12T19:50 | Closed open questions: Takeout confirmed Google Photos export (2026-05-03); Photos folder is manual personal media; Camera Uploads date range 2025-09–2026-05; Archive contents identified | Claude (Windows) |
| 2026-05-12T21:10 | Updated Documents INGEST status (32% objects, running); memory files updated with key findings; branch returned to main | Claude (Windows) |
| | *(MacBook Claude: add your entry here)* | |
