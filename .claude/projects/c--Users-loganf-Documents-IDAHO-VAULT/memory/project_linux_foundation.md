---
name: "LINUX }!{ — execution layer foundation"
description: "Linux is the connective tissue of all vault automation — CI, cloud, WSL, mobile, gaming. All tooling targets Linux-native execution."
type: project
---

LINUX }!{ declared 2026-04-04 by Logan.

**Why:** Every automated process in the vault runs on Linux — GitHub Actions (Ubuntu), GCP Cloud Run (Linux containers), CrewAI Enterprise (Linux servers), WSL (Linux inside Windows), Android/Pixel 10 (Linux kernel), and future Steam Machine (SteamOS/Linux). Windows is the local editor; Linux is the engine room.

**How to apply:** All scripts, crews, and tooling must target Linux-native execution: bash, POSIX paths, `/bin/activate`, `#!/usr/bin/env python3`. Local development uses WSL or Git Bash. Never target Windows-native (PowerShell, `Scripts\activate`) as the primary path. NETWEB made files portable; LINUX }!{ makes execution portable.

**The Penguin Principle:** "All roads lead to the penguin." — vault canon, 2026-04-04.
