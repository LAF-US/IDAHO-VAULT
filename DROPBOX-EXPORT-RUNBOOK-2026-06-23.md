---
title: "Dropbox Export Runbook"
created: 2026-06-23
description: "Get everything out of Dropbox before the expired subscription lapses — rclone pull for file content plus browser steps for the ~304 GB Paper/orphan gap that rclone cannot reach."
tags:
  - defrag
  - backup
  - dropbox
  - export
doc_class: misc_reference
status: live
authority: logan
related:
  - DEFRAG-MAP
  - BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS
  - DISTRIBUTED-HASH-LEDGER
---

# Dropbox Export Runbook

**Trigger:** Dropbox subscription expired — pull everything out before the
account reverts to the free 2 GB tier and over-quota deletion grace periods
start counting down.

**Who runs this:** Logan, on a machine that is already authenticated to the
Dropbox rclone remote (your Mac with `dropbox-personal:`, or the Windows box
with `dropbox:`). **Claude Code cannot do the transfer** — the cloud session
has no access to your Dropbox credentials or local drives. This runbook + the
two scripts are the deliverable; you run them.

> **What "expired" means for your data:** Dropbox does **not** delete your
> files the moment you stop paying. The account becomes read-only / over-quota
> and you keep download access. But once you're over the 2 GB free limit,
> Dropbox starts a deletion countdown (historically ~90 days of inactivity
> warnings). So: **not a fire, but a fuse.** Pull now, verify, then stop paying.

---

## TL;DR — fastest safe path

```bash
# Mac / Linux
cd <vault>/scripts
chmod +x export-dropbox.sh
./export-dropbox.sh /Volumes/storage/DROPBOX-EXPORT-2026-06-23
```

```powershell
# Windows (PowerShell — no Git Bash/WSL/admin needed)
cd <vault>\scripts
.\Export-Dropbox.ps1 -Destination "D:\DROPBOX-EXPORT-2026-06-23"
```

Then do **Step 4** (browser export) for Paper docs + the 304 GB gap, which
rclone physically cannot see.

---

## What rclone CAN and CANNOT pull

Per `DEFRAG-MAP.md` §C2, the Dropbox file API only exposes **~5.2 GB**:

| Reachable by rclone | Size | Notes |
| --- | --- | --- |
| `Camera Uploads/` | 5.2 GB / 884 files | Phone auto-uploads, 2025-09 → 2026-05 |
| `Apps/remotely-save/` | 0 B | Obsidian plugin folder, empty |

But `rclone about dropbox:` reports **309 GB used**. The ~304 GB gap is **not**
visible to the file API and **cannot** be pulled by the scripts. Confirmed
2026-05-12: `rclone lsd dropbox: --dropbox-shared-folders` returns nothing, so
it is *not* shared-with-me folders. Most likely:

1. **Dropbox Paper documents** — count toward quota, live outside the file API.
2. **Orphaned blocks** from a previously connected device that was unlinked.
3. Files in a **team/work namespace** not visible on the personal account.

These require the browser steps below.

---

## Step 1 — Preflight (30 seconds)

```bash
rclone version                       # expect v1.73.5+ (per BACKUP-INFRASTRUCTURE)
rclone listremotes | grep -i dropbox # confirm the remote name
rclone about dropbox:                # confirm used vs quota
```

If `rclone listremotes` shows no Dropbox remote, re-auth with `rclone config`
(reconnect the existing remote; an expired *paid* plan does not invalidate the
OAuth token — you can still authenticate and download on the free tier).

## Step 2 — Run the export script

The script (`export-dropbox.sh` / `Export-Dropbox.ps1`) does, in order:

1. **Manifest first** — `rclone lsjson --recursive --hash` written to
   `_export-logs/manifest-<stamp>.jsonl`. This is your record of what existed,
   with hashes, captured *before* anything moves.
2. **Copy** — `rclone copy` with `--transfers 8 --retries 5`, resumable and
   idempotent (safe to Ctrl-C and re-run).
3. **Verify** — `rclone check --one-way` confirms every source file landed at
   the destination. Mismatches are logged, not hidden.

Pick a destination with headroom. Per `DEFRAG-MAP.md` §B2 the **`storage`**
5 TB drive (3.1 TB free) is the consolidation target; the **`Vault`** 2 TB
drive (1.8 TB free) is a fine staging alternative.

## Step 3 — Confirm verification passed

Check the tail of `_export-logs/check-<stamp>.log`. You want
`0 differences found`. **Do not** cancel the subscription or delete anything in
Dropbox until this is clean.

## Step 4 — Browser export for Paper + the 304 GB gap (rclone can't do this)

1. **Dropbox Paper:** open <https://www.dropbox.com/paper> (or dropbox.com →
   left sidebar → look for Paper / "Docs"). For each doc: **··· → Export** →
   download as Markdown or Word. If there are many, request a bulk account
   export (next item) which includes Paper.
2. **Full account export / orphan investigation:** dropbox.com → avatar →
   **Settings → check for a data-export / "Download a copy of your data"
   option**, or download top-level folders directly as `.zip` from the web file
   browser. This is the only way to retrieve content the API can't see.
3. **Connected devices:** Settings → **Security → Devices**. Orphaned blocks
   from an old unlinked device may be surfacing here; note anything unexpected
   before it's gone.
4. **Reconcile:** compare the browser-downloaded total against the
   `rclone about` "used" figure. When local + browser exports ≈ 309 GB, you've
   got everything.

## Step 5 — Cross-check for duplicates before trusting deletion

Camera Uploads likely overlaps other surfaces (per `DEFRAG-MAP.md` §E2):
OneDrive `Pictures/`, gdrive `Photos/`, Pixel `CrossDevice/`. That's *good* —
it means the photo content is probably already redundant. But verify the
**Paper docs and any unique folders** exist nowhere else before you let the
account lapse.

## Step 6 — Only then

- Confirm `check` log is clean **and** Step 4 browser exports are downloaded.
- Update `DEFRAG-MAP.md` §E1 item 4 / §E3 Dropbox blockers to "done".
- Cancel the subscription / let it lapse.

---

## Manual fallback (no script)

```bash
rclone copy dropbox: /Volumes/storage/DROPBOX-EXPORT-2026-06-23 \
  --transfers 8 --retries 5 --progress \
  --log-file /Volumes/storage/DROPBOX-EXPORT-2026-06-23/copy.log
rclone check dropbox: /Volumes/storage/DROPBOX-EXPORT-2026-06-23 --one-way
```

---

## Provenance

- Remote names, sizes, the 304 GB gap, and drive free-space figures:
  `DEFRAG-MAP.md` §B2, §B3, §C2, §E (2026-05-12 / 2026-05-25 sessions).
- rclone version + remote configuration: `BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS.md`.
- Expired-subscription deletion-grace behavior is Dropbox's general policy, not
  a vault-recorded fact — **verify the current grace window in your account's
  billing/notifications page** before relying on a specific number of days.
