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
related:
  - STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17
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
| `Documents/` | 25,500 / 35,512 (72% objects) | ~163 MiB of 405 MiB current batch (40%) | **INCOMPLETE — STOPPED** 2026-05-13 ~04:45 after 9h20m. 1,269 errors. LFS blob cache almost certainly did not complete. Log read by Bellhop 2026-05-25 from Vault drive (D: on Windows = ExFAT 2TB drive, now visible from Mac). Vault splinter folders confirmed in `gdrive-personal:INGEST/windows-2026-05-12/Documents/`. Needs re-run from Windows to finish LFS blobs. |
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

*Inventoried 2026-05-25 by Claude (Mac session).*

### B1. MacBook Internal Drive

**Specs:** 2015 MacBook Pro 13", 932 GB internal, **836 GB used, 79 GB free** (92% full — tight)

| Folder | Size | Notes |
|---|---|---|
| `~/Desktop/` | 2.4 MB | ✅ Clean — previous defrag transfer complete. One `session-export-*.zip` file. |
| `~/Downloads/` | 61 GB | ⚠️ Needs triage. Top items: Idaho Debates Senate videos (979 MB), Photos-001 folder (583 MB), Louie Zong albums, music albums, Premiere Pro Workshop. Also `OneDrive_1_9-25-2024/` (1 MB — 3 SVWC author docs, already local). |
| `~/Documents/` | 21 GB | OBS recordings (15 GB), Zoom recordings (6.4 GB), Timberborn saves (274 MB), Twitch assets (50 MB). |
| `~/Pictures/` | 5.1 GB | Photos Library.photoslibrary present. iCloud set to `downloadAndKeepOriginals = 1` — originals should be local. **NOTE: memory from prior session listed Photos Library as 152 GB; current measurement is 5.1 GB for all of ~/Pictures. Discrepancy unexplained — Photos app may be locking the library from du, or bulk of library was already moved to Storage drive.** |
| `~/Music/` | 31 GB | iTunes library (31 GB), Amazon Music (93 MB). |
| `~/Movies/` | 8.7 GB | iMovie Library (5.8 GB), Final Cut bundle (2.1 GB), Final Cut Backups (769 MB). |
| `~/Library/CloudStorage/` | 8 KB | No cloud drives mounted locally. |
| **Internal total (approx)** | **~127 GB in key folders** | Remaining ~700 GB is system + apps + other Library content. |

### B2. Physical External Drives — Complete Inventory (updated 2026-05-25)

Five drives total. Mac sees 2; Windows sees 3. Drive letters are not permanent — they shift as drives are connected to different machines. During the 2026-05-12 Windows INGEST session the Vault was D:; in this session D: is the storage drive because the physical configuration changed.

| Volume Label | FS | Total | Used | Free | OS / Mount | Notes |
|---|---|---|---|---|---|---|
| `timemachine` | HFS+ | 1 TB | 853 GB | 78 GB | Mac `/Volumes/timemachine` | Hardware: My Passport for Mac (per Mac system report). Time Machine backup only — do not use for defrag. |
| `Vault` | exFAT | ~2 TB | ~28 MB | ~1.8 TB | Mac `/Volumes/Vault` (current) | Contains `rclone-logs/` with all INGEST transfer logs (read by Bellhop 2026-05-25). Was D: on Windows during 2026-05-12 INGEST session; currently on Mac only. Available as staging target from Mac. |
| `storage` | exFAT | 4,657 GB | 1,509 GB | 3,148 GB | Windows D: | Main content archive and consolidation target. Contains: `Photos Library.photoslibrary` (explains 152 GB vs 5.1 GB ~/Pictures discrepancy — library lives here, not Mac internal), old desktop transfer from 2026-05-12 INGEST (`Cloud/`, `home-root-files/`), extensive personal content dating to 2014. |
| `Expansion` | exFAT | 3,726 GB | 661 GB | 3,065 GB | Windows E: | **Journalism archive** — Idaho Reports, Idaho Legislature (il29), Idaho Debates, IDEX, FYIdaho, OI, Social media experiments, Dialogue, Paperwork. Date range 2020–2024. Work journalism projects. |
| `ExternalSSD` | exFAT | 931 GB | 769 GB | 162 GB | Windows F: | **Production scratch disk** — Adobe Media Cache & Scratch Disk, Premiere Exports, IDEX_Artifacts_temp (2025-07-14), Science Trek, DESKTOP dump (2024-08-01), temp, IR, personal. Was used as video production scratch; likely has recoverable project content mixed with cache. |

**Windows drive data source:** `Get-Volume` (PowerShell, 2026-05-25 session). **Mac drive data source:** Bellhop's `diskutil` / system report (2026-05-25 session).

**Note on rclone-logs:** Previously at `D:\rclone-logs\` (when Vault was D: on Windows, 2026-05-12). Now accessible from Mac at `/Volumes/Vault/rclone-logs/`. Windows reference in Section A1 reflects the original session path.

### B3. MacBook rclone Status

✅ rclone v1.73.5 installed at `/usr/local/bin/rclone`

| Remote | Status | Notes |
|---|---|---|
| `gdrive-personal:` | ✅ accessible | Confirmed reachable |
| `dropbox-personal:` | ✅ accessible | 5.3 GB, 936 files (Camera Uploads) |
| `onedrive-personal:` | ✅ accessible (partial) | Personal Vault errors; Imports+Pictures accessible |
| `gdrive-idahoptv:` | not tested | Work Drive — stable |
| `gdrive-professional:` | ❌ empty/inaccessible | Deprecated IT account |
| `gdrive-private:` | ❌ empty/inaccessible | — |

✅ `gdrive-personal:INGEST/windows-2026-05-12/` confirmed reachable from Mac — folders: Creative-Cloud-Files, Desktop-SCRATCH, Documents, Downloads, Videos.

**Note on 1Password files:** `1Password Emergency Kit`, `Recovery Code`, and `Google Passwords.csv` exist in both `onedrive-personal:Imports/...` AND `gdrive-personal:` root. gdrive-personal is canonical per Section E decision; no separate OneDrive pull needed.

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
- [ ] **Dropbox 304 GB gap** — not shared folders (API confirmed nothing). Check `dropbox.com` → left sidebar → "Paper" for doc count; Settings → Connected Devices for orphaned storage.
- [ ] **OneDrive Personal Vault** — locked. Open `onedrive.live.com` → Personal Vault → authenticate. Likely near-empty (Imports+Pictures already = 145 GB of 145 GB quota).
- [ ] **`2026-04-24.md` authentic record** — Orphan branch `bot/daily-rollover-2026-04-24` had an authentic rollover with FMLA paperwork + vault sync tasks. Trunk has template-unrendered version with cleared tasks. Orphan branch deleted; objects still in local reflog (blob `f3d616f35e8ae79f5be7ac61fe7351fd34b9c2fa`). Logan's call: restore authentic April 24 content, or keep trunk version?

**Requires Mogget (Windows):**
- [ ] **Documents INGEST re-run** — stopped 2026-05-13 04:45, 72% objects / ~40% bytes, 1,269 errors. LFS blob cache likely incomplete. Run: `rclone copy "C:\Users\loganf\Documents" "gdrive-personal:INGEST/windows-2026-05-12/Documents" --transfers 4 --log-file "D:\rclone-logs\documents-resume2.log"`

**Requires physical drive mount:**
- [ ] **5TB Storage drive** — not seen on Mac in this session. When mounted, pull: gdrive-personal content, Dropbox Camera Uploads, OneDrive Pictures.

**Resolved:**
- [x] ~~**GitHub LFS budget**~~ — Pushes working normally as of 2026-05-25 Mac session (5 commits pushed, including content files).
- [x] ~~Section B (MacBook local + 5TB inventory)~~ — Complete. Filled in 2026-05-25 Mac session; drive inventory from Windows session.
- [x] ~~What is OneDrive `Imports/` (139 GB)?~~ — Confirmed: direct copy of gdrive-personal from 2026-05-04. **Skip.**
- [x] ~~How much free space on the 5TB drive?~~ — Storage drive not on Mac; 4657 GB total, 3148 GB free per Windows `Get-Volume`.
- [x] ~~Is `gdrive-personal:Photos` Google Photos backup or a separate folder?~~ — Manual folder, personal/family media 2015–2020. NOT Google Photos.
- [x] ~~What's in `gdrive-personal:Takeout`?~~ — Google Takeout export 2026-05-03. Group 5 (~80 GB) = Google Photos library. Groups 7+9 = other services + 3 journalism videos.
- [x] **Arborscaping (Mac side)** — Complete 2026-05-25. All 7 orphan history branches deleted after cherry-picks: `2026-04-25.md`, `¿ The question is, has she been good to me.md` (VFD address node), `wayback_audit.py` CWE-20 fix, 2 ingest stubs. Local branch list: `* main` only.
- [x] **Force-closed PRs** (#356, #355, #354, #352) — All investigated. Content in trunk: #356 swarm MVP files blob-identical ✅; #354 SESSION-2026-05-22.md identical ✅; #352 urllib3 2.7.0 in trunk ✅; #355 pywin32 marker superseded (pywin32 removed from requirements entirely) ✅. No unique content lost.
- [x] **Open PR audit** — 4 previously-tracked PRs (#356, #355, #354, #352) were force-closed at rewrite time. New open PRs: #369 (Wayback Audit), #368 (topology census), #367–#359 (Dependabot stack). Awaiting Logan review on GitHub.

---

## Revision Log

| Date | Change | Author |
|---|---|---|
| 2026-05-12T12:30 | Initial inventory (Windows side) | Claude (Windows) |
| 2026-05-12T18:00 | Updated INGEST status; investigated Dropbox gap (no shared folders via API); identified OneDrive Imports as gdrive-personal duplicate; updated pull priority stack | Claude (Windows) |
| 2026-05-12T18:35 | Resumed Documents transfer (321 GB LFS blobs); clarified blockers requiring Logan vs MacBook action | Claude (Windows) |
| 2026-05-12T19:50 | Closed open questions: Takeout confirmed Google Photos export (2026-05-03); Photos folder is manual personal media; Camera Uploads date range 2025-09–2026-05; Archive contents identified | Claude (Windows) |
| 2026-05-12T21:10 | Updated Documents INGEST status (32% objects, running); memory files updated with key findings; branch returned to main | Claude (Windows) |
| 2026-05-25T01:30 | Filled in Section B: MacBook local inventory (127 GB in key folders, 79 GB free), rclone confirmed operational (6 remotes), INGEST reachable. 5TB not mounted — B2 pending. Confirmed 1Password files in gdrive-personal. OneDrive Imports emergency downgraded (known dedup per Section E). | Bellhop (Mac) |
| 2026-05-25T01:50 | Drives inserted: Vault (2TB ExFAT, D: on Windows, 1.8TB free) + My Passport timemachine (1TB). Storage (5TB) NOT present. Read documents-resume.log from Vault drive — INGEST Documents confirmed INCOMPLETE (stopped 2026-05-13 04:45, 72% objects, 1,269 errors, LFS blobs likely missing). Updated B2 with actual drive inventory. Updated INGEST status. 5TB Storage location unknown. | Bellhop (Mac) |
| 2026-05-25 (Windows session) | Completed B2 physical drive inventory from Windows PowerShell Get-Volume. All 5 drives confirmed: Vault + timemachine on Mac; storage (D:, 4657 GB) + Expansion (E:, 3726 GB) + ExternalSSD (F:, 931 GB) on Windows. **Drive letters shifted between sessions** — Vault was D: on Windows during 2026-05-12 INGEST (Bellhop's snapshot was accurate); in this session D: is the storage drive because drive config changed. Added Expansion + ExternalSSD which Mac couldn't see. Resolved Photos Library discrepancy: library is on D:/storage drive, not Mac internal. Dropped unverifiable "formerly LoganF" designation — current label is `storage`. | Claude (Windows session) |
| 2026-05-25 (Mac session — end of day) | Arborscaping complete: 7 orphan branches pruned, 4 cherry-picks pushed (including VFD address node, security fix, daily note, ingest stubs). Force-closed PR investigation complete — #356, #354, #352 content confirmed in trunk; #355 superseded. Open PR list corrected: 4 previously-tracked PRs force-closed at rewrite; new open stack: #369, #368, #367–#359. E3 updated: GitHub LFS resolved, Arborscaping/PR items closed, remaining blockers clarified. | Bellhop (Mac) |
