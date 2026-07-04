---
title: Workstation Cleanup Record 2026-07-03
aliases:
  - 2026-07-03 workstation cleanup
  - startup cleanup quarantine record
  - laptop cleanup bureaucracy record
tags:
  - workstation
  - macos
  - cleanup
  - quarantine
  - bureaucracy
  - codex
date: 2026-07-03
recorded: 2026-07-03 04:21:40 MDT
disposed: 2026-07-03 04:26:03 MDT
maxon_cleanup: 2026-07-03 21:03:29 MDT
status: active-cleanup-continued
---

# Workstation Cleanup Record 2026-07-03

This note records the local Mac startup and application-residue cleanup performed with Codex on 2026-07-03. The purpose is not merely "cleanup" but accounting: the Vault is the bureaucracy that records what happens.

## Machine Context

- Host context: Logan's long-running MacBook Pro, a decade-old workstation still in active use.
- Working root during cleanup: `/Users/logan`
- Quarantine root: `/Users/logan/.local/state/startup-cleanup`
- Time Machine state at record time: backup finished, drive disconnected, `tmutil status` reported `Running = 0`.
- Battery context: known poor retention; previously checked by Apple Genius Bar and not considered an active fire risk.

## Completed Cleanup

The cleanup focused on old startup items, abandoned app residue, and Launchpad ghosts. Changes were made as reversible quarantines first, with manifests where practical.

Removed or quarantined:

- GoToMeeting / LogMeIn residue.
- Cisco Webex residue.
- Epson app, scanner, printer-driver, event-manager, and remaining fax PPD residue.
- Epic Games Launcher residue.
- Microsoft Silverlight plugin and Launchpad artifact.
- Old Audacity install, replaced by current Homebrew cask install.
- Old Spotify install, replaced by current Homebrew cask install.
- Broken Canon MasterInstaller daemon only.
- Launchpad ghost rows for old Audacity, Epson utilities, Silverlight, Epic Games Launcher, Event Manager, Canon IJ manual artifact, and duplicate old Spotify.

Kept intentionally:

- Canon MG2500 printer utilities.
- Canon EOS Webcam Utility, because it belongs to the OBS / streaming stack.
- Zoom application, with startup daemon disabled.
- Amazon Music application, with startup disabled.
- Apple `com.apple.installer.osmessagetracing`, interpreted as inert Apple installer residue rather than a cleanup target.

## Quarantine Inventory Before Disposal

Snapshot from `du -sh /Users/logan/.local/state/startup-cleanup/*` at 2026-07-03 04:21:40 MDT:

```text
4.0K  2026-07-03-canon-broken-daemon-quarantine
4.0K  2026-07-03-canon-broken-daemon-quarantine.MANIFEST.md
4.0K  2026-07-03-epson-driver-quarantine.MANIFEST.md
12K   2026-07-03-epson-ppd-residue-quarantine
3.9M  2026-07-03-launchpad-grey-icons-followup
39M   2026-07-03-audacity-update
57M   2026-07-03-silverlight-launchpad-quarantine
82M   2026-07-03-epson-driver-quarantine
391M  2026-07-03-spotify-update
560M  2026-07-03-anomaly-quarantine
1.8G  2026-07-02-low-hanging-uninstalls
```

Approximate total pending disposal: 2.9 GB.

Manifest files present:

```text
/Users/logan/.local/state/startup-cleanup/2026-07-02-low-hanging-uninstalls/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-anomaly-quarantine/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-audacity-update/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-canon-broken-daemon-quarantine.MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-epson-driver-quarantine.MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-epson-ppd-residue-quarantine/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-launchpad-grey-icons-followup/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-silverlight-launchpad-quarantine/MANIFEST.md
/Users/logan/.local/state/startup-cleanup/2026-07-03-spotify-update/MANIFEST.md
```

## Disposal

At 2026-07-03 04:26:03 MDT, Logan approved permanent quarantine disposal. Codex removed the contents of `/Users/logan/.local/state/startup-cleanup`.

Verification:

- `/Users/logan/.local/state/startup-cleanup` remained present as an empty directory.
- `du -sh /Users/logan/.local/state/startup-cleanup` reported `0B`.
- Root-owned quarantine remnants required an administrator-authenticated removal.
- A follow-up residue sweep produced only known false-positive Apple/iWork substring matches.

## Remaining Work

One main work item remains after this record:

1. Address the Adobe cluster separately.

Adobe remains intentionally unresolved because it is larger and riskier than the low-hanging cleanup batch. Known Adobe issues include broken Creative Cloud launch agents, Acrobat / Reader overlap, and large Adobe support folders.

## Notes

- Time Machine had completed and the backup drive had been disconnected before this record was written.
- No Time Machine backup bundle was modified during Epson residue cleanup.
- This note began as a pre-disposal accounting record and was updated after quarantine disposal completed.

## Maxon Cinema 4D Cleanup Update

At 2026-07-03 21:03:29 MDT, Codex quarantined old Maxon Cinema 4D app-folder installs discovered through Launchpad cleanup:

```text
/Users/logan/.local/state/startup-cleanup/2026-07-03-maxon-cinema4d-quarantine
```

Moved:

- `/Applications/Maxon Cinema 4D R21`
- `/Applications/Maxon Cinema 4D R22`

Approximate quarantine size:

```text
1.5G
```

Launchpad rows removed:

- `Cineware`
- `Cinema 4D`
- `Cinema 4D Lite`
- `Cinema 4D Team Render Client`
- `Cinema 4D Team Render Server`
- `Commandline`
- `c4dpy`

Post-check:

- No Maxon/Cinema 4D Launchpad rows remained.
- No Maxon/Cinema 4D paths remained under `/Applications` or `/Applications/Utilities`.
- No Maxon/Cinema 4D launch agents, package receipts, running processes, or obvious Library support folders were found before quarantine.
- Dock was restarted so Launchpad would refresh.
