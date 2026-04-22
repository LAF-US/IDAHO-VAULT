---
authority: LOGAN
related:
  - INBOX
  - PHONE-LINK
  - AI-CAPTURES
  - MESHWEB
  - book-binding problem
status: active
date created: Sunday, April 12th 2026
---

# !/INBOX — Intake Automation Layer

**JANUS structure.** This folder holds the automation and protocol face of the intake system. The file-drop face lives at root `INBOX/`.

| Face | Location | Purpose |
|---|---|---|
| Protocol / automation | `!/INBOX/{SOURCE}/` | READMEs, scripts, intake rules — faces the swarm |
| File drops | root `INBOX/{SOURCE}/` | Where files actually land — faces Logan |

---

## Intake Sources

| Source | Automation | Drop target |
|---|---|---|
| `PHONE-LINK/` | `phone-link-auto-sweep.ps1` — watches `%USERPROFILE%\Downloads\Phone Link`, auto-moves to root `INBOX\PHONE-LINK\` | root `INBOX/PHONE-LINK/` |
| `AI-CAPTURES/` | Protocol and naming convention — Chrome extension drops Markdown exports | root `INBOX/AI-CAPTURES/` |

---

*See `!/INBOX/AI-CAPTURES/README.md` for the AI conversation capture protocol.*  
*See `!/INBOX/PHONE-LINK/phone-link-auto-sweep.ps1` for the phone sweep automation.*
