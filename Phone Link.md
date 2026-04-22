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
**Local path:** `C:\Users\loganf\Downloads\Phone Link`
**Platform:** Windows Phone Link app (Microsoft)

## What It Is

Phone Link is the Windows built-in app that bridges an Android phone to a Windows laptop. Among other features, it syncs files transferred from the phone into a dedicated folder at `C:\Users\loganf\Downloads\Phone Link`.

This makes it a **reliable, zero-config intake vector** for getting phone-captured content (photos, screenshots, voice memos, documents) onto the laptop and into the vault.

## Intake Workflow

1. **Capture** on phone — photo, screenshot, voice memo, document
2. **Send** via Phone Link (share → Phone Link, or it syncs automatically depending on settings)
3. **Files land** at `C:\Users\loganf\Downloads\Phone Link\`
4. **Run intake script** — `python .github/scripts/phone_link_intake.py` (or double-click `phone-link-intake.bat`)
5. **Script moves** files directly into the vault root, preserving the original filenames whenever possible

## Intake Script

**Script:** `.github/scripts/phone_link_intake.py`
**Wrapper:** `phone-link-intake.bat` (repo root, for Windows double-click)

### Usage

```bash
# From vault root
python .github/scripts/phone_link_intake.py

# With custom source path
python .github/scripts/phone_link_intake.py --source "C:\Users\loganf\Downloads\Phone Link"

# Dry run (show what would happen, don't move files)
python .github/scripts/phone_link_intake.py --dry-run

# Process and auto-stage the moved files for git
python .github/scripts/phone_link_intake.py --git-add
```

## Conventions

- Files are **moved** (not copied) from Phone Link into the vault by default. Use `--copy` to preserve originals.
- Files land in the **vault root** with their original filenames preserved.
- If an identical file is already present at root, intake skips it.
- If a different file already uses that name, intake appends a timestamp and short hash suffix.

## See Also

- VAULT-CONVENTIONS — Vault structure and intake rules
- `.github/scripts/phone_link_intake.py` — The intake automation script
