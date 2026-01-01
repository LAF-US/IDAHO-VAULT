---
name: macbook-cpu-machine-check-failures
description: "The 2015 MacBook Pro is throwing recurring uncorrectable CPU machine-check panics (L1D cache, MC bank 1) — failing hardware, accelerating"
metadata:
  type: project
---

The vault host (MacBookPro12,1, i7-5557U) has kernel-panicked six times between
2026-08-31 and 2026-09-05, every one an **uncorrectable machine check** logged in
MCA bank 1 (the data cache unit):

- `IA32_MC1_STATUS = 0xbf80000000000114` (one instance `0xff80…`, OVER set)
- Decodes to: VAL, UC, EN, MISCV, ADDRV, **PCC** (processor context corrupt),
  error code `0x0114` = cache-hierarchy read error, **data, level 0 (L1D)**
- `IA32_MC1_ADDR` differs on every panic — not one stuck cell
- Panicked process differs every time (fontd, Claude, Dock, mdbulkimport, Finder,
  compile) — no software common denominator
- Frequency: Aug 31 → Sep 3 → Sep 4 (×2) → Sep 5 (×2)

**Why it matters:** This is a CPU die fault, not software and not a reseatable
DIMM (RAM is soldered on this model; L1D is on-die anyway). It cannot be fixed by
reinstalling, resetting NVRAM/SMC, or removing kexts. The 2026-09-03 panic faulted
with RIP inside the kernel with `com.apple.filesystems.apfs` in the backtrace —
a machine check during an APFS write path is a **silent-corruption risk to vault
data**, which is the real hazard here, not the downtime.

**How to apply:** Treat every checksum, dedup, `git fsck`, and rewrite result
produced on this machine as unverified — a bad L1D read can corrupt data in
flight without git noticing. Do not run the single big vault rewrite
(see [[vault-order-of-operations]]) on this host. Migration off this machine is
now urgent rather than planned; see [[macbook-is-transitional-vault-host]] and
[[idaho-vault-storage-architecture]]. Preserve, do not delete
([[never-discard-vault-content]]).
