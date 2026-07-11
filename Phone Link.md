---
title: Phone Link
updated: 2026-04-22
status: active
related:
- '2026-04-02'
- VAULT-CONVENTIONS
- bridges
- voice
authority: LOGAN
---
# Phone Link

**Vector:** Phone → Laptop (reliable)
**Observed local drop path:** `C:\Users\loganf\Downloads\Mobile Devices`
**Legacy drop path also watched:** `C:\Users\loganf\Downloads\Phone Link`
**Platform:** Windows Phone Link app (Microsoft)

## What It Is

Phone Link is the Windows built-in app that bridges an Android phone to a Windows laptop. On this device, files sent from the phone land in `C:\Users\loganf\Downloads\Mobile Devices`. The watcher also monitors the legacy `C:\Users\loganf\Downloads\Phone Link` folder so older mappings do not silently break.

This makes it a **reliable, zero-config intake vector** for getting phone-captured content (photos, screenshots, voice memos, documents) onto the laptop and into the vault.

## Background Sweep Workflow

1. **Capture** on phone — photo, screenshot, voice memo, document
2. **Send** via Phone Link (share → Phone Link, or it syncs automatically depending on settings)
3. **Files land** at `C:\Users\loganf\Downloads\Mobile Devices\` or the legacy `C:\Users\loganf\Downloads\Phone Link\`
4. **Startup launches watcher** — this laptop's user Startup folder contains `IDAHO VAULT Phone Link Sweep.lnk`, which calls `phone-link-sweep-launcher.vbs` and opens `START-PHONE-LINK-SWEEP.cmd`
5. **Watcher sweeps once on startup**, then waits for Windows file-change events in the drop folder
6. **Sweeper moves** files from the drop folder into the vault root, preserving the original filenames whenever possible

## Sweeper Script

**Script:** `.github/scripts/phone_link_auto_sweep.py`
**Launcher:** `START-PHONE-LINK-SWEEP.cmd`
**Compatibility wrapper:** `phone-link-auto-sweep.ps1`

### Usage

```bash
# From vault root
python .github/scripts/phone_link_auto_sweep.py

# With custom drop folders
python .github/scripts/phone_link_auto_sweep.py --source "C:\Users\loganf\Downloads\Mobile Devices"
python .github/scripts/phone_link_auto_sweep.py --source "C:\Users\loganf\Downloads\Mobile Devices" --source "C:\Users\loganf\Downloads\Phone Link"

# Sweep once and exit
python .github/scripts/phone_link_auto_sweep.py --once

# Start hidden/background watcher through the existing launcher
START-PHONE-LINK-SWEEP.cmd

# Stop the watcher
STOP-PHONE-LINK-SWEEP.cmd
```

## Conventions

- Files are **moved** from Phone Link into the vault root.
- Files land in the **vault root** with their original filenames preserved.
- If an identical file is already present at root, intake deletes the duplicate from the drop folder after verifying the matching content already exists in the vault.
- If a different file already uses that name, intake appends a timestamp and short hash suffix.
- On Windows, the background mode uses directory-change watchers for the two configured drop folders rather than recursively scanning or continuously polling the vault.
- The script does not create the Phone Link source folder; if the Microsoft app has not created it, startup should fail visibly.
- `CrossDevice` is a separate Windows/Android file surface and is not swept by this tool.

## See Also

- VAULT-CONVENTIONS — Vault structure and intake rules
- `.github/scripts/phone_link_auto_sweep.py` — The background sweep script
