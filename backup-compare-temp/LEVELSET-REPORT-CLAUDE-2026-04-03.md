# LEVELSET REPORT — Claude Code (The Abhorsen)
**Date:** 2026-04-03
**Branch:** `claude/eloquent-lichterman`
**Session:** Dev server detection → Dispatch debugging → hardware/auth inventory

---

## Work Completed This Session

### 1. Dev Server Detection + launch.json
- Detected one dev server: Flask webhook listener (`main.py`) — the Nest Bridge
- Created `.claude/launch.json` per schema (version 0.0.1, Flask on port 8080)
- Installed project dependencies (`pip install -r requirements.txt`) — Flask, gunicorn, GCP libs
- Started Flask Dev Server via `preview_start` — confirmed healthy (Method Not Allowed on GET = expected, POST-only route)

### 2. Claude Code Dispatch — Debugging
- **Symptom:** Messages sent via Dispatch marked ✓ Read but no replies
- **Root cause:** No active Code session was running to receive Dispatch tasks; Dispatch routes to a running Desktop session
- **Blocker discovered:** Desktop app out of date — "Cowork needs newer installation"
- **Upgrade blocked:** IT-managed work machine; unapproved `.exe` publishers blocked; no admin credentials
- **MSIX investigated:** Not available via Microsoft Store; Intune-only enterprise path
- **Resolution path:** MacBook Pro 2015 (personal) — MagSafe 2 charger ordered, arriving Wednesday

### 3. Hardware Inventory — Logged to Memory
- **Active:** Pixel 10, Samsung S10e, Light Phone, reMarkable
- **Laptop:** MacBook Pro 13" 2015 (Silver) — 3.1GHz i7, 16GB, 1TB; MagSafe 2; swollen battery; charger ordered ($25.98, arriving Wednesday)
- **Second Mac:** Older model, faulty RAM — data recovery (photos) pending
- **Potential server:** Old Wii (homebrew); Plex server aspirational
- **To-buy:** Raspberry Pi, YubiKey, Flipper Zero

### 4. Auth Stack — Logged to Memory
- 1Password: new, housekeeping in progress; TOTP consolidation target
- 2FA split: Google Authenticator (migrate out), Duo (work, keep), Microsoft Authenticator (work, keep)
- YubiKey pending purchase → hardware root for 1Password + git signing

### 5. GCP Project ID Confirmed
- `idaho-vault` — confirmed by Logan
- "affable-bastion" origin unknown, discarded

---

## Files Added This Session
- `.claude/launch.json` — dev server configuration (Flask Nest Bridge, port 8080)

---

## Blockers / Open Items
- **Dispatch/Cowork:** Unblocked when MagSafe 2 charger arrives (Wednesday) + MacBook brought online
- **MacBook battery:** Swollen — check Apple service program; run on AC only until replaced
- **Auth consolidation:** 1Password housekeeping in progress — do not assume it holds all secrets yet
- **Second Mac data recovery:** Deferred — PCIe SSD + USB enclosure when ready
- **Plex/Pi server:** Deferred pending cash

---

## Handoff to Copilot
Branch `claude/eloquent-lichterman` ready for PR → `main`.
One new untracked file: `.claude/launch.json` — staged and committed below.

**-C** (The Abhorsen)
