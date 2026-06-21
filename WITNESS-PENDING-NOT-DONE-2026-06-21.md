---
title: "Witness — Pending ≠ Done: the referenced-but-unverified durable-copy gap"
created: 2026-06-21
updated: 2026-06-21
status: draft
authority: LOGAN
doc_class: witness
authors:
  - Claude Code CLI
related:
  - STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - VAULT-MEDIA-STORAGE
  - DEFRAG-MAP
  - DRIVE-REGISTRY
  - VAULT-CONVENTIONS
tags:
  - witness
  - storage
  - verification
  - durability
---

# Witness — Pending ≠ Done

A short, on-the-record note that the vault **references** durable external copies of
material it no longer holds in Git, but those copies are **declared, not verified**. The
committed record describes an intended state; the verified state is, in several places,
still empty. This note names the gap so "pending" is not mistaken for "done."

> Surfaced 2026-06-21 during a storage/LFS review. It corrects a looser phrasing
> ("moved to external storage") with the precise status: the move is planned and
> awaiting execution/verification — incomplete.

---

## The gap, by surface

| Surface | What the record references | What is actually verified | State |
| --- | --- | --- | --- |
| **Oversized objects** ([[LAF-USB-OBJECT-MANIFEST-2026-05-08]], `status: staged`) | 40 files >2 GB routed to external homes: **19** → Internet Archive (`idaho-vault-media`), **15** → GCS `the-ledger-bucket` (cold), **6** → `REVIEW-REQUIRED` | All 40 are `verification_state: pending`; every `storage_key` is prefixed `pending:`. The bytes are **confirmed present only in local `.git/lfs/objects/`** (~323 GB). `gs://the-ledger-bucket` was probed **empty** (Apr 2026). Manifest: *"Logan must approve before any carrier transfer executes."* | ☐ **not moved** `[RECORD]` |
| **Screenshots** ([[Screenshots/Screenshots.md]] + root `screenshots.md` MOCs) | Folder-index notes that render a screenshot collection in Obsidian | Reachable Git history shows **0 image blobs** ever under `Screenshots/`; the folder is empty in the repo. The collection lives in **Obsidian Sync** (a courier, not a backup) | ☐ **not in the durable record** `[EVIDENCE]` |
| **Work Desk journalism archive** ([[DRIVE-REGISTRY]], `Expansion`) | Idaho Reports / Legislature originals on one HDD | Sole-copy status unconfirmed; no second-copy evidence captured | ☐ **sole-copy unverified** `[RECORD]` |
| **Cloud → 5 TB consolidation** ([[DEFRAG-MAP]]) | A 322 GiB rclone transfer + Documents INGEST → 5 TB physical | INGEST stopped 2026-05-13 at ~72% objects / 1,269 errors; the 322 GiB transfer logged as *"status unknown"*; 5 TB drive not mounted last session | ◐ **partial / unverified** `[EVIDENCE]` |

The recurring shape: the vault is honest that these are pending, but the *language* around
them (and around storage generally) can read as completed. Four independent surfaces, one
risk class — **a referenced copy is not a verified copy.**

---

## The one counter-attestation

Logan attests, **firsthand and out-of-record**, that the backups were finished with
`rclone`/`rsync`. That is valid provenance the vault does not itself contain. If accurate,
the durable copies exist and only the *verification record* is missing — not the data. This
note does not dispute the attestation; it marks that the **committed record cannot yet
corroborate it.**

---

## What converts pending → done

Per the last-mile checklist in [[STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17]] (which
this note feeds, not replaces) — requires a **local-machine agent**, non-destructive:

- **Manifest objects:** list each `storage_key`'s real destination (Archive item / GCS
  object), confirm presence + `sha256` match, then flip `verification_state` `pending →
  verified` and drop the `pending:` prefix. Validate with `.github/scripts/laf_usb_manifest.py`.
- **Screenshots:** open `Screenshots/` in desktop Obsidian; if populated, they are Sync-only
  — decide whether any belong on the durable record.
- **Work Desk / 5 TB:** mount by label+serial, confirm the journalism archive exists on ≥2
  surfaces, and read the rclone receipt (`Transferred / Errors`, then `rclone check` →
  `Differences: 0`).

Until then: **pending.** Esto Perpetua.

---

## DOCUMENT METADATA

- **Created:** 2026-06-21
- **Last Updated:** 2026-06-21
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** Witnessed the referenced-but-unverified durable-copy gap across the LAF-USB manifest (40/40 pending, bucket empty), the Sync-only screenshots, the Work Desk sole-copy, and the partial cloud→5 TB consolidation; recorded Logan's firsthand backup attestation as uncorroborated-but-valid provenance.
