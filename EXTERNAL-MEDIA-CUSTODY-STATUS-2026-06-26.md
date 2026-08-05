---
date: 2026-06-26
authority: LOGAN
status: active
related:
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - VAULT-MEDIA-STORAGE
  - DOTFOLDER-PORT-RUNBOOK
  - rclone
  - Git LFS
---

# External Media Custody Status - 2026-06-26

This note records the current state of the large media custody question during
the employer-laptop evacuation.

## Current Vault Copy Status

The current filesystem contents of:

- `C:\Users\loganf\Documents\IDAHO-VAULT`
- `E:\`
- `D:\Vault`

were compared during the evacuation work. The working conclusion was that the
current C: Vault contents were represented on both external destinations.

Evidence recorded in-session:

- robocopy list-only checks from C: to E: and D: reported no missing source
  files, no mismatches, and no failures.
- rclone size-only checks from C: to E: and D: reported `0 differences found`
  and `308356 matching files` after one small file was repaired.
- targeted media checks found `2247` conventional media files in the C: Vault
  and found no missing or size-mismatched copies on E: or D:.
- targeted checks for current C: Vault files over 5 GB found only extensionless
  `.ollama\models\blobs\sha256-*` files; each was present on E: and D: by
  matching size.

This establishes custody for the current C: Vault filesystem contents. It does
not establish custody for historical large media that had already been removed
from the C: Vault before this evacuation pass.

## Large External Media Manifest

`LAF-USB-OBJECT-MANIFEST-2026-05-08.json` lists `40` oversized external media or
archive objects:

| Type | Count |
| --- | ---: |
| `.mp4` | 31 |
| `.mxf` | 4 |
| `.mov` | 4 |
| `.zip` | 1 |

All 40 manifest entries were still marked `verification_state: pending` when
checked on 2026-06-26.

The manifest is useful as a recovery and custody index because it records:

- original filename
- expected size
- SHA-256 checksum
- rough sensitivity/routing class
- intended storage lane

The manifest does not currently provide verified payload custody. It does not
contain confirmed public URLs, Google Drive file IDs, GCS object generations, or
Internet Archive file identifiers for the unresolved objects.

## Confirmed Absence From Current C: Vault

The manifest-listed `.mxf`, `.mp4`, `.mov`, and `.zip` payload files are not
present as payload files under `C:\Users\loganf\Documents\IDAHO-VAULT` under
their manifest filenames.

Evidence recorded in-session:

- direct filesystem search in the C: Vault for `*.mxf` and `*.mp4` returned no
  files.
- the media inventory found no `.mxf` or `.mp4` files in the C: Vault.
- the only current C: Vault files over 5 GB were `.ollama` model blobs.
- `git lfs ls-files` did not list `.mxf` or `.mp4` entries in the current
  checkout.

Deleting the current C: Vault directory would not delete those manifest-listed
media payloads from C:, because those payloads are not in that directory now.
Their custody question is separate from the C: to E:/D: Vault copy question.

## Verified External Payload Locations

The following manifest objects were found with exact expected size.

### Local External Drive `F:`

- `F:\Science Trek\MEDIA\0305 Biomimicry 2\female-hand-on-touch-screen-2023-11-27-04-52-48-utc.mov`
- `F:\DESKTOP\idex greater idaho\PETERSEN VIDEO\XD4_6594.MXF`
- `F:\DESKTOP\idex greater idaho\PETERSEN VIDEO\XD4_6595.MXF`
- `F:\DESKTOP\idex greater idaho\PETERSEN VIDEO\XD4_6597.MXF`
- `F:\DESKTOP\idex greater idaho\PETERSEN VIDEO\XD4_6602.MXF`

### `gdrive-personal:`

Exact-name Google Drive queries found these manifest objects with matching
expected size:

- `260303_schr_0130PM-Meeting.mp4`
- `260313_jloc_1215PM-Meeting.mp4`
- `SenateChambers03-02-2026.mp4`
- `SenateChambers03-25-2026.mp4`

The Google Drive file IDs were observed during the 2026-06-26 verification pass,
but this note intentionally records only the custody result and filenames. A
future private manifest can store provider-specific IDs if needed.

## Suspicious Same-Name Finding

`gdrive-personal:` also contained a file named:

- `260309_hjud_0130PM-Meeting.mp4`

Its size did not match the manifest entry. Do not count it as verified custody
without a checksum comparison or manual review.

## Checked But Not Verified

The following locations did not establish additional verified custody during the
2026-06-26 pass:

- `D:\` and `E:\` outside the current Vault copies: no exact manifest media
  filename hits.
- `archive:idaho-vault-media`: listed empty through rclone.
- `gcs:the-ledger-bucket/IDAHO-VAULT/oversize`: no exact filename hits.
- `gdrive-ptv:`: no exact filename hits.
- `dropbox:` and `box:`: no exact filename hits.
- `onedrive:`: search failed on a `Personal Vault` listing error.
- `proton-drive:`: rclone reported an invalid token.

`D:\rclone-logs` was not present during this pass. `E:\rclone-logs` existed, but
the available logs were May 12-13 document transfers and did not prove the May
17 note that mentioned a `322 GiB LFS objects -> gdrive-personal` transfer.

## Current Conclusion

Resolved:

- The current C: Vault filesystem contents were copied to E: and D:.
- The historical manifest-listed large media payloads are not present in the
  current C: Vault directory.

Unresolved:

- Full custody of the `40` manifest-listed external media/archive objects.
- `9` objects have confirmed custody by exact size.
- `1` same-name Google Drive object is suspicious because size differs.
- `30` objects remain unlocated or otherwise unverified from this pass.

Do not treat the manifest's `pending:*` storage keys as proof of upload. Treat
them as intended lanes and recovery search keys until verified by size and
checksum or by provider-native metadata plus checksum.
