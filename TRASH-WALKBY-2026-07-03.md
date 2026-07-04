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

## Mounted Drive Context

Mounted volumes observed after the first walkby:

- Internal APFS Data volume: about 768Gi used, 144Gi available.
- `/Volumes/timemachine`: external 1TB Journaled HFS+ Time Machine destination, about 943GB used and 56.7GB free. Time Machine reported `Running = 0`.
- `/Volumes/Vault`: external 2TB exFAT volume, about 361.9GB used and 1.6TB free. Mounted writable with no ownership semantics.
- Local Time Machine snapshots existed through `com.apple.TimeMachine.2026-07-03-210454.local`.

`tmutil latestbackup` returned an XPC connection error during the check, so the latest external backup path was not confirmed by that command. The mounted Time Machine destination and local snapshot list were confirmed separately.

The `Vault` external has ample space but was slow to enumerate at the root, so it should be treated as an archive drive rather than casual scratch space. The Time Machine disk is nearly full and should not be used as a staging destination.

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

Installed-app comparison:

- Installed copies currently exist for `Gemini 2.app`, `GitHub Desktop.app`, and `Steam.app`.
- Installed active tools exist for `Claude.app`, `Codex.app`, `Obsidian.app`, `Android Studio.app`, and `zoom.us.app`; matching DMGs/installers in Trash look like installers, not the live apps.
- `Tailscale.app` and Tailscale installer packages are in Trash, but Tailscale work was active in a parallel agent thread, so leave these out of any first disposal batch.

Plausible software-only first batch, pending explicit approval:

- Old conferencing and sync tools already in Trash: `Cisco Webex Meetings.app`, `Webex (1).pkg`, `Webex (2).pkg`, `GoToMeeting.app`, `Backup and Sync.app`, `MusicManager.app`, `MusicManager.prefPane`.
- Old app installers/downloads: `Obsidian 1.6.5.dmg`, `Obsidian 1.6.5 (1).dmg`, `Git 2.23.0 for Mavericks.dmg`, `Node v20.15.0.pkg`, `node-v24.15.0.pkg`, `MacPorts-2.12.5-12-Monterey.pkg`, `Dropbox Installer.dmg`, `DropboxInstaller.dmg`.
- Duplicate/current-tool installers, likely re-downloadable: `Codex.dmg`, `Codex (1).dmg`, `Claude.dmg`, `GitHub-Copilot-darwin-x64.dmg`.
- Old app bundles where a current or alternative install exists or the app was already discarded: `GitHub Desktop.app`, `GitHub Copilot.app`, `Gemini 2.app`, `Steam.app`, `Steam 1.03.35 AM.app`, `Steam 7.12.16 PM.app`.

Hold out of first batch:

- `Tailscale.app`, `Tailscale-latest-macos.pkg`, `Tailscale-1.98.5-macos.pkg`: parallel Tailscale work in progress.
- `EOSWebcamUtility-MAC1.0.pkg`: camera/OBS stack relevance.
- `obs-streamelements-setup.pkg`: OBS/streaming stack relevance.
- Microsoft Office app bundles: large and probably old, but keep as a distinct human decision because the total is about 9.4G.
- `android-studio-quail1-patch2-mac.dmg`: Android Studio is installed; likely disposable, but large enough to ask explicitly.
- Archive-like ZIPs with personal/project names: `FINNEY.zip`, `ReclaimID-BorahPark-photos.zip`, `Mockups-round-2.zip`, `7_23_press_conference_audio.zip`.

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
