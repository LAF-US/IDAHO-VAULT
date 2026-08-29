# Maxon Cinema 4D Quarantine

Date: 2026-07-03

Purpose: Quarantine old Maxon Cinema 4D app-folder installs and remove their Launchpad rows.

Moved:

- `/Applications/Maxon Cinema 4D R21`
- `/Applications/Maxon Cinema 4D R22`

Destination:

- `/Users/logan/.local/state/startup-cleanup/2026-07-03-maxon-cinema4d-quarantine/Applications/`

Launchpad DB backup:

- `/Users/logan/.local/state/startup-cleanup/2026-07-03-maxon-cinema4d-quarantine/Launchpad-DB-Backup/db.before-maxon-cleanup`

Removed Launchpad rows:

- `Cineware` / `net.maxon.Cineware` (2 rows)
- `Cinema 4D` / `net.maxon.cinema4d` (2 rows)
- `Cinema 4D Lite` / `net.maxon.cinema4dlite`
- `Cinema 4D Team Render Client` / `net.maxon.cinema4dclient` (2 rows)
- `Cinema 4D Team Render Server` / `net.maxon.cinema4dserver` (2 rows)
- `Commandline` / `net.maxon.commandline` (2 rows)
- `c4dpy` / `net.maxon.python` (2 rows)

Notes:

- No Maxon/Cinema 4D launch agents, package receipts, running processes, or obvious Library support folders were found before quarantine.
- Approximate quarantine size: `1.5G`.
- Restore by moving the two app folders back to `/Applications` with administrator privileges and restoring/rebuilding Launchpad if needed.
