---
name: machine-location-vocabulary
description: "Logan's three named locations on the MacBook: LAPTOP, VAULT, DRIVE"
metadata:
  type: project
---

Logan's shorthand for the three storage locations (established 2026-08-27). Use
these terms; do not conflate them.

- **LAPTOP** = `Macintosh HD`, the internal disk. Includes `~/Documents`,
  `~/Desktop`, `~/Music`, `~/Library` — everything on the boot volume that is
  *not* inside the vault directory.
- **VAULT** = `~/IDAHO-VAULT`, the git repository. Note that ~18 dotdirs in `~`
  are symlinks INTO it, so paths like `~/.ssh` and `~/.local` are VAULT, not
  LAPTOP. See [[idaho-vault-storage-architecture]].
- **DRIVE** = `/Volumes/storage`, the 5 TB ExFAT USB archive — a merge of several
  older drives, ~26 k files flat at root. Separate from `/Volumes/TimeMachine`
  (2 TB, case-sensitive APFS, Time Machine target).

**DRIVE and VAULT are both deliberately cross-platform.** ExFAT is the correct
choice for DRIVE precisely because it must mount on Logan's Mac *and* his Windows
machine (ZBFURY) — it carries a `$RECYCLE.BIN` (67 GB, Windows-side deletions he
handles there) alongside macOS `.Spotlight-V100`/`.fseventsd`/`._*` sidecars. Do
not treat ExFAT's lack of POSIX permissions, symlinks, or case-sensitivity as a
defect to warn about: it is the point. The same bridging intent governs VAULT,
which syncs between the Mac and Windows lines — hence `(WIN)`-suffixed files and
the `logan/obsidian/{macos,windows,linux}` branch scheme.

**Why:** Saying "out of the vault" is ambiguous — it can mean LAPTOP or DRIVE, and
identically-named files exist in more than one place at once (e.g. `pg84.epub` was
on both VAULT and DRIVE). Name the destination explicitly.
