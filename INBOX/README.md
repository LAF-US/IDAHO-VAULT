---
authority: LOGAN
related:
  - AI-CAPTURES
  - PHONE-LINK
  - MESHWEB
status: active
date created: Sunday, April 12th 2026
---

# INBOX — File Drop Zone

Raw intake. Files land here before they are processed into the vault, except for Phone Link, which now lands directly at the vault root.

**Automation and protocol live in `!/INBOX/` — this is the drop face only.**

| Subdirectory | Source | Protocol |
|---|---|---|
| `AI-CAPTURES/` | Chrome extension exports, AI conversation Markdown | See `!/INBOX/AI-CAPTURES/README.md` |
| `PHONE-LINK/` | Windows Phone Link auto-sweep to vault root | See root `phone-link-auto-sweep.ps1` |

**Rules:** Do not auto-empty. Do not normalize. Files stay until explicitly processed and cleared.
