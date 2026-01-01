---
name: vault-repo-hazards
description: "Live hazards in the IDAHO-VAULT git repo — corrupt pack, auto-gc disk blowout, 1015 packs, pre-push hook defects. Check these before acting on the repo."
metadata:
  node_type: memory
  type: project
---

Hazards discovered 2026-08-28..31 on the MacBook clone. Not derivable from the
repo — they are states and causes that only show up when something breaks.

**Auto-gc fills the disk.** A SINGLE one-file commit triggered git's automatic
repack, which wrote 56 GiB of `tmp_pack_*` files and died out of disk. Across a
few days this accumulated 130.6 GiB of abandoned temp packs and took the machine
to 180 MiB free, which killed Time Machine (BACKUP_FAILED_NO_SPACE_FOR_LOCAL_
SNAPSHOT, hourly). Now disabled: `gc.auto=0`, `gc.autoDetach=false`,
`maintenance.auto=false`, `gc.pruneExpire=never`. DO NOT re-enable.
Killed pushes leave temp packs too — always check
`ls .git/objects/pack/tmp_pack_*` after interrupting any git operation.

**One corrupt object, unrepaired.** `pack-37e2012216245ebc0a8cf29fe48ed11a31bce527`
holds 100,168 objects; ZERO of them exist in any of the other 1,014 packs, so the
pack cannot simply be removed. Exactly one object is damaged — blob
`89f439b3fae553ff685afcd5bb8b9813462c98ab`, 6,862,398 bytes, at pack offset
15290714236. Everything else in that pack reads fine. A verified-good copy came
from the Windows clone and sits at `/tmp/89f439b3.blob` (sha256
687f00c95dad97468dace6787f464392a31239ca3c67086db444bcd58e18b62e) — /tmp does not
survive reboot, re-fetch from Windows if gone. `git hash-object -w` is INERT here:
git resolves via pack indexes first, sees the SHA listed, and writes nothing.
Repair shape: unpack-objects to recover the 100,167 readable ones, then write the
good blob, then repack. Not done, Logan's call.

**1,015 packs.** Most are a few hundred bytes. Consolidating is `repack` WITHOUT
prune — and prune is the dangerous half here, not repack.

**114,974 dangling objects.** Normal for this repo given gc is off. NOT litter to
clean: this history has been severed and re-stitched repeatedly, so unreachable
does not mean worthless. `git prune --dry-run` wants to remove essentially
nothing.

**Grafts are NOT gc-fragile.** Earlier sessions (including this one) claimed gc
would destroy the 7 replace grafts. Measured false — `refs/replace` are ordinary
refs and count as reachability roots. Their real limitation is only that they do
not travel on push or clone. See [[vault-history-grafts]].

**Pre-push hook has two structural defects** (`.githooks/pre-push`):
1. Its file list comes from a git RANGE but `trufflehog filesystem` reads the
   WORKING TREE. They only agree when the pushed ref IS the checkout. A 2026-08-30
   fix filtering to existing paths stopped the crash but made it scan current
   content instead of the ref's content — a secret present at the pushed ref and
   cleaned later now passes SILENTLY. That is worse than the loud failure.
2. gitleaks and trufflehog use DIFFERENT baselines on ref creation
   (`--not --remotes=origin` vs `merge-base` with origin/main), so a ref rename
   scans 0 commits for one scanner and 3,008 for the other.
Windows committed a combined fix; it arrives when that branch lands.

Related: [[vault-order-of-operations]], [[vault-history-grafts]],
[[never-discard-vault-content]].
