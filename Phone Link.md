---
title: Phone Link
updated: 2026-04-02
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
4. **Watcher Triggers** — `phone-link-auto-sweep.ps1` detects the drop and calls the intake script.
5. **Script processes** files into `!/INBOX/` with metadata, classified by type.

## File Type Handling

| Type | Extensions | Vault destination | Notes |
| --- | --- | --- | --- |
| Photos | `.jpg`, `.jpeg`, `.png`, `.heic`, `.webp` | `!/INBOX/images/` | Renamed with date prefix |
| Screenshots | `.png` (if detected) | `!/INBOX/screenshots/` | Heuristic: filename contains "screenshot" |
| Voice memos | `.m4a`, `.ogg`, `.mp3`, `.wav`, `.aac` | `!/INBOX/audio/` | Ready for transcription pipeline |
| Documents | `.pdf`, `.docx`, `.txt` | `!/INBOX/docs/` | Copied as-is |
| Video | `.mp4`, `.mov`, `.3gp`, `.webm` | `!/INBOX/video/` | Large files — flagged for review |
| Other | `*` | `!/INBOX/other/` | Catch-all for unrecognized types |

## Intake Script

**Script:** `.github/scripts/phone_link_intake.py`
**Daemon:** `phone-link-auto-sweep.ps1` (local PowerShell watcher)
**Watcher log:** `!/INBOX/_phone-link-watcher.log`

### Usage

```bash
# From vault root (Preview mode)
python .github/scripts/phone_link_intake.py

# EXECUTE (Move files into vault)
python .github/scripts/phone_link_intake.py --live-write

# Process and auto-stage for git
python .github/scripts/phone_link_intake.py --live-write --git-add

# Ensure the watcher starts at login
START-PHONE-LINK-SWEEP.cmd --register-startup
```

## Conventions

- **Singular Authority:** The Python script is the sole mover. The PowerShell daemon is a thin trigger.
- **Flattened Intake:** Files land in `!/INBOX/` subfolders without source-specific segregation.
- **NETWEB Portability:** Filenames are lowercased and date-prefixed.
- **MCP Guardrails:** Execution requires the `--live-write` flag. Each batch emits a structured YAML `mcp_action_log`.
- **Durable Record:** A human-readable batch entry is appended to `!/INBOX/intake-log.md`.
- **Login Persistence:** `START-PHONE-LINK-SWEEP.cmd --register-startup` installs the user-level launcher; `STOP-PHONE-LINK-SWEEP.cmd` uses the watcher PID file instead of CIM process inspection.

## See Also

- VAULT-CONVENTIONS — Vault structure and naming rules
- `!/INBOX/` — Standard infrastructure intake staging
- `.github/scripts/phone_link_intake.py` — The intake automation script
- `mcp_guardrails.py` — Structured action logging interface
