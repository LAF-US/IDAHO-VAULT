---
title: "Phone Link"
updated: 2026-04-02
status: active
tags:
  - infrastructure/intake
  - tools/phone-link
aliases:
  - Phone Link intake
  - phone to laptop
---

# Phone Link

**Vector:** Phone → Laptop (reliable)
**Local path:** `C:\Users\loganf\Downloads\Phone Link`
**Platform:** Windows Phone Link app (Microsoft)

## What It Is

[[Phone Link]] is the Windows built-in app that bridges an Android phone to a Windows laptop. Among other features, it syncs files transferred from the phone into a dedicated folder at `C:\Users\loganf\Downloads\Phone Link`.

This makes it a **reliable, zero-config intake vector** for getting phone-captured content (photos, screenshots, voice memos, documents) onto the laptop and into the vault.

## Intake Workflow

1. **Capture** on phone — photo, screenshot, voice memo, document
2. **Send** via Phone Link (share → Phone Link, or it syncs automatically depending on settings)
3. **Files land** at `C:\Users\loganf\Downloads\Phone Link\`
4. **Run intake script** — `python .github/scripts/phone_link_intake.py` (or double-click `phone-link-intake.bat`)
5. **Script processes** files into `INBOX/phone-link/` with metadata, then stages for vault triage

## File Type Handling

| Type | Extensions | Vault destination | Notes |
| --- | --- | --- | --- |
| Photos | `.jpg`, `.jpeg`, `.png`, `.heic`, `.webp` | `INBOX/phone-link/images/` | Renamed with date prefix |
| Screenshots | `.png` (if detected) | `INBOX/phone-link/screenshots/` | Heuristic: filename contains "screenshot" |
| Voice memos | `.m4a`, `.ogg`, `.mp3`, `.wav`, `.aac` | `INBOX/phone-link/audio/` | Ready for transcription pipeline |
| Documents | `.pdf`, `.docx`, `.txt` | `INBOX/phone-link/docs/` | Copied as-is |
| Video | `.mp4`, `.mov`, `.3gp`, `.webm` | `INBOX/phone-link/video/` | Large files — flagged for review |
| Other | `*` | `INBOX/phone-link/other/` | Catch-all for unrecognized types |

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

# Process and auto-stage for git
python .github/scripts/phone_link_intake.py --git-add
```

## Conventions

- Files are **moved** (not copied) from Phone Link into the vault by default. Use `--copy` to preserve originals.
- Filenames are normalized: lowercased, spaces replaced with hyphens, date-prefixed.
- A manifest entry is written to `INBOX/phone-link/intake-log.md` for each batch.
- Large files (>50 MB) are flagged but not moved automatically. Use `--include-large` to override.
- The script is idempotent — re-running skips files already present in the vault.

## See Also

- [[VAULT-CONVENTIONS]] — Vault structure and intake rules
- `INBOX/` — General intake staging area
- `.github/scripts/phone_link_intake.py` — The intake automation script
