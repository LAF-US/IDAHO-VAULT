# Trash Walkby - 2026-07-03

Local observation pass over `/Users/logan/.Trash` before adding any new quarantine bundles to Trash.

No Trash contents were moved, restored, opened, or deleted during this pass. Sensitive-looking filenames were inspected by metadata only.

## Snapshot

- Time: 2026-07-03 21:11 MDT
- Trash total: about 179G
- Data volume free space: about 144Gi available
- Top-level Trash entries: 7,212
- Top-level directories: 671
- Top-level files: 6,540

## Largest Buckets

- `Traffyk Jam`: 39G
- `IDLEG 2021`: 22G
- `Sand Dunes`: 18G
- `SWEET LAND`: 14G
- `Adobe`: 11G
- `Borah polls Nov 2020`: 5.2G
- `FREELANCE`: 2.5G
- loose top-level media files: about 30G
- top-level apps/installers/packages/archives: about 18G
- top-level Markdown files: about 20M across 4,843 files

The top five human media/project folders alone total about 99G. They appear to be old production or personal media material and should be treated as human-review, not mechanical cleanup.

## Human-Review Zones

Large media/project material:

- `Traffyk Jam`: large Canon MOV clips and related project material.
- `IDLEG 2021`: legislative and interview footage, including very large MXF files.
- `Sand Dunes`: many Canon MOV/JPG camera originals.
- `SWEET LAND`: large `SweetLandOfLiberty` MXF/MOV exports.
- `Borah polls Nov 2020`: camera footage.
- `Dialogue.fcpbundle` and `Untitled.fcpbundle`: Final Cut bundles.

Vault-like and repo-like material:

- `.Trash/.git`: standalone Git directory for `loganfinney27/THE-GEMSTONE.git`, branch `main`, last observed commit `1d8e841 Delete README.md`.
- `.Trash/.obsidian`: Obsidian config files including `app.json`, `appearance.json`, plugin/core settings, and `workspace.json`.
- `.Trash/IDAHO-VAULT`: Git checkout on `main`, status showed untracked `go/` and `google-cloud-sdk/`.
- `.Trash/IDAHO-VAULT 1.29.37 AM`: smaller vault-like snapshot.
- `.Trash/THE-GEMSTONE` and `.Trash/THE-GEMSTONE 14-20-14-364`: repo/project material.
- `.Trash/LAF-US`: tiny but semantically named project material.

These should not be emptied as anonymous debris without a separate review or restore/dispose decision.

## Sensitive-Name Signals

Filename-only scan found likely sensitive or security-themed entries. Contents were not opened.

Notable top-level items:

- `Passwords.csv`: 11,090 bytes, modified 2026-04-25.
- `Passwords 9.54.43 PM.csv`: 11,090 bytes, modified 2026-07-02.
- `credentials.md`, `iamcredentials.md`, `auth_tokens.md`, `tokens.md`, `secrets`, `secretsmanager.md`, `secretmanager.md`, and related timestamped copies.

Additional hits inside trashed vault snapshots included 1Password/security reference notes and zero-byte `passwords.md` files. The CSVs deserve a special secure-disposal or secure-restore decision before any broad Trash empty.

## Software-Like Trash

The top-level app/installer/archive bucket totals about 18G. Largest entries include:

- Microsoft Office app bundles: Word 2.3G, Outlook 2.2G, Excel 2.0G, PowerPoint 1.8G, OneNote 1.1G.
- `Tableau Public.app`: 1.6G.
- `android-studio-quail1-patch2-mac.dmg`: 1.4G.
- `Granola.app`: 604M.
- `TableauPublic-2020-2-2.dmg`: 523M.
- `GitHub Desktop.app`: 400M.
- `GitHub Copilot.app`: 396M.
- `Codex.dmg` and `Codex (1).dmg`: 331M each.
- `Claude.dmg`: 295M.
- Webex, GoToMeeting, MusicManager, Backup and Sync, older Obsidian DMGs, Tailscale installers, Node installers, and other old packages.

These are mechanically more plausible disposal candidates than the media/project material, but still should be reviewed as a batch before deletion.

## Adobe In Trash

The existing `.Trash/Adobe` folder is about 11G and appears dominated by Premiere Pro state/cache:

- `Adobe/Premiere Pro/14.0`: 11G
- `Adobe/Premiere Pro/12.0`: 39M
- small Adobe Media Encoder, Premiere Rush, Lumetri, and dynamiclinkmediaserver folders

This resembles cache/state rather than current Acrobat material, but it predates the current quarantine pass and should stay labeled separately.

## Current Non-Trash Quarantine Nearby

Existing quarantine bundles under `~/.local/state/startup-cleanup`:

- `2026-07-03-adobe-user-cache-quarantine`: 27G
- `2026-07-03-maxon-cinema4d-quarantine`: 1.5G
- `2026-07-03-adobe-service-quarantine`: 1.4G
- `2026-07-03-adobe-launchpad-cleanup`: 3.9M

Do not add these to Trash until the Trash strategy is chosen.

## Preliminary Classification

- Do not bulk-empty: large media/project folders, vault/repo-like material, sensitive-name items.
- Plausible first disposal batch after review: old app bundles, installers, duplicate DMGs, old conferencing/software packages already in Trash.
- Plausible special handling: password/credential/token-named files, especially the two `Passwords*.csv` files.
- Plausible separate Adobe decision: `.Trash/Adobe` Premiere cache/state, distinct from Acrobat/Reader.

