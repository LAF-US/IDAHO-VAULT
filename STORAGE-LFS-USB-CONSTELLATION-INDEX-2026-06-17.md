---
title: "Storage / LFS / USB Constellation — Phase Index & Closeout"
date: 2026-06-17
status: active
authority: LOGAN
doc_class: index
phase: "Local Storage Consolidation & Vault Reunification"
phase_window: "2026-04-01 → 2026-05-25"
related:
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - DEFRAG-MAP
  - MACBOOK-GROUND-ZERO-OBSERVATION-2026-05-15
  - "!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14"
  - HOME-DESK-MANIFEST-2026-05-08
  - WORK-DESK-MANIFEST-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - CROSS-DRIVE-OVERLAP-REPORT-2026-05-08
  - LOCAL-VAULT-REUNIFICATION-2026-05-08
  - VAULT-MEDIA-STORAGE
  - LAF-USB-PROTOCOL-FRAMEWORK
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - Universal Sync Bus
  - DISTRIBUTED-HASH-LEDGER
  - BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS
  - LAF-USB
  - USB
  - HANDOFF-abhorsen-codex-20260401
  - LEVELSET-LFS-SHUTDOWN-2026-05-06
  - HANDOFF-LFS-2GB-BLOCK-2026-05-08
  - GIT-CONTROL-SURFACES-2026-05-17
  - VAULT-CONVENTIONS.from-pushable-2026-05-08
  - WITNESS-ABHORSEN-2026-05-19-DEWEY-HAS-THE-USB
  - LOCAL-ARBORSCAPE-IDAHO-VAULT-SPLINTERS-2026-05-09
  - ARBORSCAPE-COMPLETION-REPORT-2026-05-17
tags: [index, storage, lfs, laf-usb, usb, migration, defrag, constellation, phase-closeout]
---

# Storage / LFS / USB Constellation — Phase Index & Closeout

This is the index the phase never had. The **Local Storage Consolidation &
Vault Reunification** phase (~2026-04-01 → 2026-05-25) produced roughly two
dozen artifacts but no single closeout document, so its answer lived
distributed across inventories, manifests, doctrine, a merged PR, and the
operator's own memory — retrievable only by triangulation. This node gathers
the constellation, records what is **closed and traceable** versus **open**, and
carries the **last-mile checkup** that only an agent on the local machines can
run.

> The original question that opened the trail: *"Did I finish moving/archiving
> my files from my work computer? There should be records of what agents helped
> me do."* — Answer: see [[#Outcomes ledger]]. Records of the agents: yes (see
> [[#Crew]]).

---

## The constellation

### ① Inventories & maps — "what exists"
- [[LOCAL-STORAGE-INVENTORY-2026-05-08]] — read-only folder-level audit of `C:/D:/E:/F:`. *(active)*
- [[DEFRAG-MAP]] — cross-device + cloud inventory; the live 5-drive table (updated 2026-05-25). *(live)*
- [[MACBOOK-GROUND-ZERO-OBSERVATION-2026-05-15]] — the MacBook surface and available tooling. *(active)*
- [[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]] — Mac hardware / SMART / capacity check. *(reference)*

### ② Drive-role manifests — "where things should live"
- [[HOME-DESK-MANIFEST-2026-05-08]] — `D:` LoganF: personal/history archive + staging. *(draft)*
- [[WORK-DESK-MANIFEST-2026-05-08]] — `E:` Expansion: Idaho Reports / Legislature / production. *(draft)*
- [[TRAVEL-BAG-MANIFEST-2026-05-08]] — `F:` ExternalSSD: lean portable active-work. *(draft)*

### ③ Plans & routing — "how to move it"
- [[EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08]] — role mapping + non-destructive routing order. *(draft)*
- [[CROSS-DRIVE-OVERLAP-REPORT-2026-05-08]] — overlap families; the one proven duplicate (`Social media experiments`, 174/174). *(draft)*
- [[LOCAL-VAULT-REUNIFICATION-2026-05-08]] — the closest prior attempt to tie the batch together (predates DEFRAG / Mac / pushable rebuild). *(active)*

### ④ Doctrine — the durable rules that outlived the phase ✅ live
- [[VAULT-MEDIA-STORAGE]] — storage lanes: ≤100 MB direct / >100 MB LFS / >2 GB external. *(in force; extended via PR #535)*
- [[LAF-USB-PROTOCOL-FRAMEWORK]] — staged carrier/sync framework for external objects.
- [[LAF-USB-OBJECT-MANIFEST-2026-05-08.json]] — registry of the oversized files >2 GB: **40 entries, 40/40 `pending`** (grew from the original 38 at the 2026-05-08 block as ghost OIDs were retired and entries added).
- [[Universal Sync Bus]] — transport-bus doctrine (alias "USB"). *(staged)*
- [[DISTRIBUTED-HASH-LEDGER]] — multi-provider verification model.
- [[BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS]] — rclone + 7 remotes + `op` stand-up (2026-04-23).
- [[LAF-USB]] / [[USB]] — disambiguation nodes for the carrier vs. the bus.

### ⑤ LFS remediation arc — the "38-file / 2 GB" thread
- [[HANDOFF-abhorsen-codex-20260401]] — origin: `git lfs migrate`, force-push blocked.
- [[LEVELSET-LFS-SHUTDOWN-2026-05-06]] — interrupted GitHub Desktop push (4.0/4.5 GiB).
- [[HANDOFF-LFS-2GB-BLOCK-2026-05-08]] — the wall: HTTP 422, 38 files > 2 GB; policy amended 5 GB → 2 GB.
- [[GIT-CONTROL-SURFACES-2026-05-17]] — operating frame for `.gitignore` / `.gitattributes` / LFS / manifests.
- [[VAULT-CONVENTIONS.from-pushable-2026-05-08]] — conventions snapshot captured at the pushable-main rebuild.
- **PR #317 "pushable main rebuild"** — merged by Logan 2026-05-09; the actual git-side resolution. ✅
- Enforcement: `.github/scripts/check_large_files.py`, `.github/workflows/large-file-policy.yml`, `.github/scripts/large_file_watchdog.py`, `.gitattributes`, `.github/scripts/laf_usb_manifest.py`, `.github/workflows/laf-usb-manifest-policy.yml`.

### ⑥ USB witness / signals
- [[WITNESS-ABHORSEN-2026-05-19-DEWEY-HAS-THE-USB]] — governance witness asserting archive integrity ("Dewey has the USB"). *(witness-grade claim, not a transfer receipt.)*

### ⑦ Repo / branch cleanup — adjacent housekeeping
- [[LOCAL-ARBORSCAPE-IDAHO-VAULT-SPLINTERS-2026-05-09]] — local clone splinter census.
- [[ARBORSCAPE-COMPLETION-REPORT-2026-05-17]] — branch/PR cleanup; logs the 322 GiB rclone transfer as *"status unknown."*

---

## Outcomes ledger

| Outcome | State | Grounding |
| --- | --- | --- |
| Storage doctrine (lanes, 2 GB ceiling) | ✅ **closed, live** | Files in force; extended in PR #535. `[EVIDENCE]` |
| Git push block / 38 files > 2 GB | ✅ **resolved** | PR #317 merged 2026-05-09; 0 oversized files tracked; pushes clean. `[EVIDENCE]` |
| Backup infrastructure (rclone + 7 remotes) | ✅ **stood up** | [[BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS]]. `[EVIDENCE]` |
| Drive inventory + roles + overlaps | ✅ **mapped** | ①②③ artifacts committed. `[EVIDENCE]` |
| Bulk transfer launched (322 GiB → gdrive) | ◐ **ran, outcome unverified** | [[ARBORSCAPE-COMPLETION-REPORT-2026-05-17]] logs start; outcome "unknown". `[CLAIM]` |
| Documents INGEST (321 GB LFS blobs) | ◐ **partial** | [[DEFRAG-MAP]]: stopped 2026-05-13 ~04:45, ~72% objects / ~40% bytes, 1,269 errors. `[EVIDENCE]` |
| Oversized originals on external durable storage | ☐ **unverified** | [[LAF-USB-OBJECT-MANIFEST-2026-05-08.json]] still 40/40 `pending`. `[RECORD]` |
| Cloud INGEST → 5 TB physical drive | ☐ **not confirmed** | DEFRAG §E pull stack; 5 TB not mounted in last session. `[RECORD]` |
| Phase closeout document | ☐ **this node** | — |

**Operator attestation (out-of-record):** Logan attests, firsthand, that the
backups were finished with `rclone`/`rsync` and that the 38-file remediation
resolved. This is valid provenance the vault does not itself contain; the
checkup below is what converts that attestation into a verified record.

---

## Crew

Agents who worked the phase (records exist and are traceable):

- **Mogget / Yrael** (`yrael.claude.mogget`, Windows-ZBFURY) — Windows-side transfers, manifest finalize, pushable-rebuild support. *Session since archived.*
- **Bellhop / Abhorsen** (`*.claude.abhorsen`, Mac) — Mac-side inventory, log reads from the Vault drive.
- **Codex** — git/branch surfaces.
- **OpenCode** — hit the original LFS push wall.

---

## Last-mile checkup — FOR A LOCAL MACHINE AGENT

> [!important] This cannot be done from a cloud/remote clone. It requires an
> agent on Logan's **Windows** and/or **MacBook** with the physical drives
> mounted. Resolve drives by **role + volume label/device evidence**, never by
> drive letter ([[EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08]]). Non-destructive
> first; no deletion or duplicate retirement without checksum evidence and
> Logan's approval.

- [ ] **Mount + identify** all storage drives; confirm `Home Desk` / `Work Desk` / `Travel Bag` / `Vault` / `storage` (5 TB) / `timemachine` by label+device against [[DEFRAG-MAP]] §B2.
- [ ] **Read the rclone receipt** — `D:\rclone-logs\documents-resume*.log` (Windows) or `/Volumes/Vault/rclone-logs/` (Mac). Capture the final `Transferred: … Errors: …` line.
- [ ] **Resume Documents INGEST if incomplete** —
      `rclone copy "<Documents>" "gdrive-personal:INGEST/windows-2026-05-12/Documents" --transfers 4 --log-file "<rclone-logs>/documents-resume2.log"`
- [ ] **Verify the transfer** — `rclone check "<local>" "gdrive-personal:INGEST/windows-2026-05-12/Documents"` → confirm **Differences: 0**.
- [ ] **The 40 oversized objects** — confirm each is on external durable storage (Work Desk/Expansion originals and/or `gcs:the-ledger-bucket`), then update [[LAF-USB-OBJECT-MANIFEST-2026-05-08.json]] `verification_state` `pending → verified` with real `storage_key` + `sha256`. Validate with `.github/scripts/laf_usb_manifest.py`.
- [ ] **Cloud → physical hop** — pull `gdrive-personal:INGEST/...` down onto the 5 TB `storage` drive (DEFRAG §E pull stack), then confirm the consolidated set is present.
- [ ] **Dedup the one proven duplicate** — `Social media experiments` (174/174 match across Work Desk + Travel Bag): checksum-confirm, then retire one copy only on Logan's approval.
- [ ] **Close the loop** — write a dated completion note (e.g. `STORAGE-MIGRATION-COMPLETE-<date>.md`), link it here, and flip this node's checklist + the manifest to `verified`.

---

## See also
[[VAULT-MEDIA-STORAGE]] · [[DEFRAG-MAP]] · [[LOCAL-STORAGE-INVENTORY-2026-05-08]] · [[LAF-USB-OBJECT-MANIFEST-2026-05-08.json]] · [[LOCAL-VAULT-REUNIFICATION-2026-05-08]]

*Provenance: assembled 2026-06-17 from a committed-record survey of the
constellation. `[EVIDENCE]` = verifiable artifact/command output; `[CLAIM]` =
asserted-but-unverified; `[RECORD]` = state of the committed record (which may
lag the live machines). Esto Perpetua.*
