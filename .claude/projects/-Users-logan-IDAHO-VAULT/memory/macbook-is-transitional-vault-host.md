---
name: macbook-is-transitional-vault-host
description: "The 2015 MacBook Pro is a temporary host for IDAHO-VAULT, not its permanent storage medium"
metadata:
  type: project
---

Logan's MacBookPro12,1 (Early 2015, Broadwell i7-5557U, 16 GB, 1 TB SSD) is an
aged desk machine left running at home — **not** the vault's permanent physical
medium (stated 2026-08-20). macOS 12.7.6 is the terminal OS for this hardware
(Ventura dropped 2015 MBPs), so it is permanently off Apple's patch track and
Homebrew classes it Tier 3.

**Why it matters:** Do not optimize storage decisions around fitting the vault on
this disk. The vault is 475 GB (205 GB of it `.git`, 145 GB of that LFS) against a
1 TB volume that hit 100% on 2026-08-19. Disk pressure here is a transitional
constraint, not a reason to destroy data — in particular not a reason to
`git gc --prune=now` (which would delete 94 recoverable dangling commits including
the Aug 12 reunification merge `440dfbebf`) or `git lfs prune` (145 GB that may
exist nowhere else).

**How to apply:** Frame `.git` size questions as "what migrates" rather than "what
fits." Prefer archiving to external media over deletion — `/Volumes/Time_Machine`
(1.8 TB, ~1.1 TB free) and `/Volumes/My_Passport` are attached. Work product is on
ZBFURY, the employer-supplied machine. See [[idaho-vault-storage-architecture]].

**Migration rationale (2026-08-20):** Time Machine was moved to the 2 TB LaCie
Rugged because the 1 TB My_Passport could not hold more than a single full laptop
backup. Migrating the vault off the internal drive fixes both ends — the laptop's
867 GB drops by ~475 GB, and the shrunken backup set fits comfortably again.
Sequence matters: migrate and verify FIRST, then exclude the vault from Time
Machine. TM is currently the only thing backing up a vault with no verified clean
copy elsewhere. Logan has multiple drives; destination is his call.
