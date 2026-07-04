---
title: Adobe Inventory 2026-07-03
aliases:
  - 2026-07-03 Adobe inventory
  - Adobe cleanup inventory
tags:
  - workstation
  - macos
  - adobe
  - inventory
  - cleanup
  - codex
date: 2026-07-03
recorded: 2026-07-03 08:59:38 MDT
service_cleanup: 2026-07-03 19:37:16 MDT
cache_cleanup: 2026-07-03 19:39:41 MDT
launchpad_cleanup: 2026-07-03 20:05:33 MDT
status: service-cache-and-launchpad-quarantined
---

# Adobe Inventory 2026-07-03

Inventory record of the Adobe presence on Logan's Mac after the low-hanging workstation cleanup. It began as inventory-only and was later updated after a non-Acrobat Adobe service-layer quarantine.

Decision boundary from Logan: keep Adobe Acrobat for PDF edge cases where Preview may not be enough.

## Executive Shape

- Acrobat is current/present and should be preserved unless Logan later changes the decision.
- Creative Cloud desktop itself appeared partially removed/broken: launch agents pointed to missing Creative Cloud and CCXProcess executables.
- Adobe Genuine Service and Creative Cloud/Finder extension service pieces were quarantined after the initial inventory.
- Post-quarantine live Adobe process state was down to Acrobat `AdobeResourceSynchronizer`.
- A 27 GB user-level Adobe cache/state pass was quarantined after the service cleanup.
- Remaining large Adobe user support is mostly `Creative Cloud Libraries`, left for human review.
- Launchpad was cleaned so only Acrobat-family Adobe icons remain.
- Separate from application support, Creative Cloud Files folders contain about 27.7 GB of user/content data and should be reviewed as documents, not blindly treated as app residue.
- Trash contains additional Adobe material, including an 11 GB `~/.Trash/Adobe` folder.

## Keep Bucket

Preserve unless explicitly reconsidered:

- `/Applications/Adobe Acrobat DC/Adobe Acrobat.app`
  - bundle id: `com.adobe.Acrobat.Pro`
  - version: `26.001.21563`
- `/Applications/Adobe Acrobat DC/Acrobat Distiller.app`
  - bundle id: `com.adobe.distiller`
  - version: `26.001.21563`
- `/Applications/Adobe Acrobat Reader.app`
  - bundle id: `com.adobe.Reader`
  - version: `26.001.21563`

Size:

```text
1.3G  /Applications/Adobe Acrobat Reader.app
2.6G  /Applications/Adobe Acrobat DC
```

Acrobat-related system support that may be needed if Acrobat stays:

- `/Library/Application Support/Adobe/Acrobat`
- `/Library/Application Support/Adobe/Reader`
- `/Library/Application Support/Adobe/ARMDC`
- `/Library/Application Support/Adobe/Acrobat DC Helper Frameworks`
- `/Library/Application Support/Adobe/MACPDFM`
- `/Library/LaunchAgents/com.adobe.ARMDCHelper...plist`
- `/Library/LaunchDaemons/com.adobe.ARMDC.Communicator.plist`
- `/Library/LaunchDaemons/com.adobe.ARMDC.SMJobBlessHelper.plist`
- `/Library/PrivilegedHelperTools/com.adobe.ARMDC.Communicator`
- `/Library/PrivilegedHelperTools/com.adobe.ARMDC.SMJobBlessHelper`
- `/Library/PDF Services/Save as Adobe PDF.app`
- `/Library/Internet Plug-Ins/AdobePDFViewer.plugin`
- `/Library/Internet Plug-Ins/AdobePDFViewerNPAPI.plugin`

## Broken Or Clearly Legacy Adobe Layer

Launch agents with missing targets:

```text
/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
  -> /Applications/Utilities/Adobe Creative Cloud/ACC/Creative Cloud.app/Contents/MacOS/Creative Cloud [missing]

/Library/LaunchAgents/com.adobe.ccxprocess.plist
  -> /Applications/Utilities/Adobe Creative Cloud Experience/CCXProcess/CCXProcess.app/Contents/MacOS/CCXProcess [missing]
```

Old Creative Cloud / Application Manager components:

```text
161M  /Applications/Utilities/Adobe Application Manager
94M   /Applications/Utilities/Adobe Sync
0B    /Applications/Utilities/Adobe Genuine Service
0B    /Applications/Adobe Lightroom Classic
```

Notes:

- `/Applications/Adobe Lightroom Classic` is an empty directory.
- `/Applications/Utilities/Adobe Genuine Service` contains symlinks into `/Library/Application Support/Adobe/AdobeGCClient`.
- `/Applications/Utilities/Adobe Application Manager` contains old 2018-era updater/licensing components.
- No Photoshop, Illustrator, Premiere, InDesign, After Effects, Media Encoder, or Digital Editions app bundles were found directly under `/Applications`.

## Active Background Processes

Observed during inventory:

```text
/Library/Application Support/Adobe/AdobeGCClient/AGSService
/Applications/Utilities/Adobe Sync/CoreSync/Core Sync.app/.../ACCFinderSync
/Library/Application Support/Adobe/Adobe OS Extension/Creative Cloud.app/.../Adobe Context Menu Extension
/Applications/Adobe Acrobat DC/Adobe Acrobat.app/.../AdobeResourceSynchronizer
```

Launchd detail:

- `Adobe_Genuine_Software_Integrity_Service` is running from `/Library/LaunchDaemons/com.adobe.agsservice.plist`.
- It runs `/Library/Application Support/Adobe/AdobeGCClient/AGSService`.
- It has `RunAtLoad` and `StartInterval = 21600`.
- `com.adobe.AdobeCreativeCloud` and `com.adobe.ccxprocess` are spawn-scheduled but fail because their executable targets are missing.
- `com.adobe.ARMDCHelper...` is Acrobat updater support; it exists and has run.

## Launch Items

Launch agents:

```text
/Library/LaunchAgents/com.adobe.ARMDCHelper.cc24aef4a1b90ed56a725c38014c95072f92651fb65e1bf9c8e43c37a23d420d.plist
/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist
/Library/LaunchAgents/com.adobe.ccxprocess.plist
/Users/logan/Library/LaunchAgents/com.adobe.AAM.Updater-1.0.plist
/Users/logan/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist
```

Launch daemons:

```text
/Library/LaunchDaemons/com.adobe.ARMDC.Communicator.plist
/Library/LaunchDaemons/com.adobe.ARMDC.SMJobBlessHelper.plist
/Library/LaunchDaemons/com.adobe.acc.installer.v2.plist
/Library/LaunchDaemons/com.adobe.agsservice.plist
```

Helper tools:

```text
/Library/PrivilegedHelperTools/com.adobe.ARMDC.Communicator
/Library/PrivilegedHelperTools/com.adobe.ARMDC.SMJobBlessHelper
/Library/PrivilegedHelperTools/com.adobe.acc.installer.v2
```

## Disk Mass

Top-level application/support sizes:

```text
94M   /Applications/Utilities/Adobe Sync
161M  /Applications/Utilities/Adobe Application Manager
1.3G  /Applications/Adobe Acrobat Reader.app
2.6G  /Applications/Adobe Acrobat DC
3.5G  /Library/Application Support/Adobe
43G   /Users/logan/Library/Application Support/Adobe
```

User Adobe Application Support breakdown:

```text
21M   /Users/logan/Library/Application Support/Adobe/Acrobat
122M  /Users/logan/Library/Application Support/Adobe/OOBE
17G   /Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries
26G   /Users/logan/Library/Application Support/Adobe/Common
```

Largest subfolders:

```text
24G   /Users/logan/Library/Application Support/Adobe/Common/Media Cache Files
1.6G  /Users/logan/Library/Application Support/Adobe/Common/Team Projects Local Hub
568M  /Users/logan/Library/Application Support/Adobe/Common/Motion Graphics Templates
218M  /Users/logan/Library/Application Support/Adobe/Common/Peak Files
212M  /Users/logan/Library/Application Support/Adobe/Common/PTX
17G   /Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries/LIBS
```

Cache/log mass:

```text
557M  /Users/logan/Library/Caches/Adobe
485M  /Users/logan/Library/Caches/CSXS
121M  /Users/logan/Library/Logs/CreativeCloud
42M   /Users/logan/Library/Logs/Adobe
45M   /Users/logan/Library/Caches/com.adobe.Photoshop
23M   /Users/logan/Library/Caches/com.adobe.PremierePro.14
17M   /Users/logan/Library/Caches/com.adobe.illustrator
15M   /Users/logan/Library/Caches/com.adobe.Reader
```

## User Data / Review Before Deleting

These look like user/content sync folders, not ordinary app support:

```text
18G   /Users/logan/Creative Cloud Files
9.7G  /Users/logan/Creative Cloud Files  avid4@idahoptv.org A5AC8FDA59D3C96E0A495C84@AdobeID
0B    /Users/logan/loganfinney27@gmail.com Creative Cloud Files
```

Trash also contains Adobe material:

```text
11G   /Users/logan/.Trash/Adobe
331M  /Users/logan/.Trash/Adobe Creative Cloud 9.53.54 PM
161M  /Users/logan/.Trash/Adobe Creative Cloud Experience
100K  /Users/logan/.Trash/Adobe Creative Cloud
16K   /Users/logan/.Trash/Adobe Installers
```

## Receipts

`pkgutil` shows 162 Adobe/Acrobat-related package receipts:

```text
total=162
reader_update_receipts=101
acrobat_update_receipts=54
reader_base_receipts=3
other_adobe_receipts=4
```

This mostly reflects a long Acrobat/Reader update history.

## Likely Next Cleanup Buckets

Conservative next pass, keeping Acrobat:

1. Disable/remove broken Creative Cloud launch agents:
   - `/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist`
   - `/Library/LaunchAgents/com.adobe.ccxprocess.plist`
2. Consider removing Adobe Genuine Service and Creative Cloud installer/sync layers if Acrobat works without them:
   - `/Library/LaunchDaemons/com.adobe.agsservice.plist`
   - `/Library/Application Support/Adobe/AdobeGCClient`
   - `/Applications/Utilities/Adobe Genuine Service`
   - `/Applications/Utilities/Adobe Application Manager`
   - `/Applications/Utilities/Adobe Sync`
   - `/Library/LaunchDaemons/com.adobe.acc.installer.v2.plist`
   - `/Library/PrivilegedHelperTools/com.adobe.acc.installer.v2`
3. Quarantine old creative-app caches and support folders that are not Acrobat:
   - `Common/Media Cache Files`
   - `Common/Team Projects Local Hub`
   - `Creative Cloud Libraries/LIBS`
   - old Photoshop/Premiere/Illustrator/InDesign caches, logs, preferences, WebKit, saved states
4. Separately review the Creative Cloud Files folders as user/project data.
5. Empty or review Adobe material already in Trash.

## Open Questions

- Is Acrobat Pro actually licensed/usable on this personal machine, or is Reader sufficient for the "keep Adobe for edge-case PDFs" requirement?
- Are the `Creative Cloud Files` folders still needed as archives of IdahoPTV/work assets?
- Should Adobe Genuine Service remain if Acrobat stays, or should Acrobat be tested after quarantining that service layer?

## Service-Layer Cleanup Update

At 2026-07-03 19:37:16 MDT, Codex quarantined the non-Acrobat Adobe service layer to:

```text
/Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-service-quarantine
```

Size after quarantine:

```text
1.4G  /Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-service-quarantine
```

Quarantined:

- Broken Creative Cloud launch agents:
  - `/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist`
  - `/Library/LaunchAgents/com.adobe.ccxprocess.plist`
- Adobe Genuine / GC service layer:
  - `/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist`
  - `/Library/LaunchDaemons/com.adobe.agsservice.plist`
  - `/Library/Application Support/Adobe/AdobeGCClient`
  - `/Applications/Utilities/Adobe Genuine Service`
- Creative Cloud installer/sync/service layer:
  - `/Library/LaunchDaemons/com.adobe.acc.installer.v2.plist`
  - `/Library/PrivilegedHelperTools/com.adobe.acc.installer.v2`
  - `/Applications/Utilities/Adobe Application Manager`
  - `/Applications/Utilities/Adobe Sync`
  - `/Library/Application Support/Adobe/Adobe OS Extension`
  - `/Library/Application Support/Adobe/Adobe Desktop Common`
  - `/Library/Application Support/Adobe/Creative Cloud Libraries`
  - `/Users/logan/Library/LaunchAgents/com.adobe.AAM.Updater-1.0.plist`
  - `/Users/logan/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist`

Preserved:

- Acrobat DC, Acrobat Distiller, and Acrobat Reader app bundles.
- Acrobat ARMDC launch agents/daemons and privileged helper tools.
- User-level Adobe media/cache payloads under `/Users/logan/Library/Application Support/Adobe`.
- Creative Cloud Files folders.

Post-check:

- Live Adobe launch roster only showed Acrobat helper/update launch items.
- Live Adobe process list only showed Acrobat `AdobeResourceSynchronizer`.
- Acrobat DC and Reader still reported version `26.001.21563`.
- `/Library/Application Support/Adobe` dropped to about 2.3G.
- `/Users/logan/Library/Application Support/Adobe` remained about 43G because the large user cache/data payload was not moved.

Not moved:

- `/Applications/Adobe Lightroom Classic`, an empty 0B folder, remains. An admin prompt to move it was cancelled because it was nonessential and the main service quarantine was already complete.

## User Cache-State Cleanup Update

At 2026-07-03 19:39:41 MDT, Codex quarantined high-confidence user-level Adobe cache/state to:

```text
/Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-user-cache-quarantine
```

Size after quarantine:

```text
27G  /Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-user-cache-quarantine
```

Quarantined:

- Premiere / Media Encoder cache-state:
  - `/Users/logan/Library/Application Support/Adobe/Common/Media Cache Files`
  - `/Users/logan/Library/Application Support/Adobe/Common/Media Cache`
  - `/Users/logan/Library/Application Support/Adobe/Common/Peak Files`
  - `/Users/logan/Library/Application Support/Adobe/Common/Team Projects Cache`
  - `/Users/logan/Library/Application Support/Adobe/Common/Team Projects Local Hub`
  - `/Users/logan/Library/Application Support/Adobe/Premiere Pro`
  - `/Users/logan/Library/Application Support/Adobe/dynamiclinkmediaserver`
- CEP/CSXS and creative-app caches/logs/state for Photoshop, Premiere, InDesign, Illustrator, Lightroom, Rush, and Media Encoder.

Preserved:

- Acrobat user support:
  - `/Users/logan/Library/Application Support/Adobe/Acrobat`
  - `/Users/logan/Library/Application Support/Adobe/AcroCef`
  - `/Users/logan/Library/Application Support/Adobe/com.adobe.ARMDCHelper`
- `/Users/logan/Library/Application Support/Adobe/OOBE`
- `/Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries`
- `/Users/logan/Creative Cloud Files`
- `/Users/logan/Creative Cloud Files  avid4@idahoptv.org A5AC8FDA59D3C96E0A495C84@AdobeID`

Post-check:

- `/Users/logan/Library/Application Support/Adobe` dropped from about `43G` to about `18G`.
- Remaining bulk is `/Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries` at about `17G`.
- Live Adobe process state remained Acrobat-only.
- Live Adobe launch roster remained Acrobat helper/update only.

## Launchpad Cleanup Update

At 2026-07-03 20:05:33 MDT, Codex removed stale non-Acrobat Adobe rows from the Launchpad database after backing it up to:

```text
/Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-launchpad-cleanup/Launchpad-DB-Backup/db.before-adobe-launchpad-cleanup
```

Removed Launchpad icons:

- `AAM Registration Notifier`
- `AASIapp`
- `AdobeGCClient`
- `AdobeIPCBroker`
- `Core Sync`
- `Setup`
- `Uninstall Product`
- `adobe_licutil`
- `AdobeCleanUpUtility`

Preserved Launchpad icons:

- `Adobe Acrobat`
- `Acrobat Distiller`
- `Adobe Acrobat Reader`

Post-check:

- Launchpad DB showed only the three Acrobat-family Adobe rows.
- Dock was restarted so Launchpad would refresh.
