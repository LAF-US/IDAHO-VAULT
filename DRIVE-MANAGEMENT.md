---
title: "DRIVE-MANAGEMENT — Strategy & Tooling for the Drive Fleet"
created: 2026-06-22
updated: 2026-06-22
status: draft
doc_class: misc_reference
authority: LOGAN
authors:
  - Claude Code CLI
related:
  - DRIVE-REGISTRY
  - TECH-REGISTRY
  - DEFRAG-MAP
  - VAULT-MEDIA-STORAGE
  - LAF-USB-PROTOCOL-FRAMEWORK
  - WITNESS-PENDING-NOT-DONE-2026-06-21
tags:
  - storage
  - drives
  - backup
  - doctrine
  - strategy
  - git-annex
  - homelab
---

# DRIVE-MANAGEMENT — Strategy & Tooling for the Drive Fleet

The **management doctrine** over the drives. Its sibling [[DRIVE-REGISTRY]] is the *device-plane
register* — the five drives as physical objects (the **what**). This note is the **how**: the
tools and strategy for managing that fleet holistically. It does not restate the drive identities
(see [[DRIVE-REGISTRY]]) or their contents (see [[DEFRAG-MAP]] §B2).

> Opened 2026-06-22 from a research pass requested by Logan: "research management tools and
> strategies for my hard drives." Logan's framing of the result: **git-annex is the interim
> spine until there's budget for a mini-PC / homelab server.** That two-phase trajectory is the
> spine of this note.

---

## The reframe: not RAID — a tracked, checksummed, location-aware archive

The drives were assembled aspirationally as a "poor man's RAID/NAS." But the fleet's actual shape
— **five single-purpose, bus-powered USB drives, hot-plugged ad hoc across a MacBook and a Windows
box** — is the opposite of what RAID/pooling wants. Pooling + parity (SnapRAID + StableBit
DrivePool on Windows, or mergerfs + SnapRAID on Linux) assumes drives that are **connected
together, on one host, more or less always on.** SnapRAID's own FAQ says that if the data fits on
a USB drive or cloud, SnapRAID is *unnecessary*.

What the fleet actually needs is something that knows **which drive holds which file, how many
copies exist, and whether the bytes have rotted — without mounting all five at once.** That is a
different tool category, and one option fits the vault's git-native habits almost exactly.

---

## Phase trajectory (Logan's framing)

| Phase | Trigger | Approach | What carries forward |
| --- | --- | --- | --- |
| **Phase 1 — NOW** | current budget, existing bus-powered fleet | **git-annex** spine + **Backblaze B2/restic** off-site + **checksums** for cold drives | the location DB + checksums + numcopies discipline |
| **Phase 2 — LATER** | budget for a **mini-PC / homelab server** | always-on host with real pooling/redundancy (NAS / DAS + SnapRAID+DrivePool, or TrueNAS) | git-annex can **stay as the catalog/location layer** on top of the pool; B2 stays the off-site leg |

The key continuity: **Phase 1 is not throwaway.** git-annex's location tracking, content
checksums, and copy-count discipline remain useful as the catalog layer even after a server
exists — the homelab becomes *one more (always-on, redundant) annex remote*, not a replacement.

---

## The three layers any version of this needs

1. **Inventory** — "where is file X, and on which drive?" answered with **zero drives mounted.**
2. **Redundancy / 3-2-1** — anything irreplaceable on ≥2 devices, ≥1 off-site/offline.
3. **Integrity** — detect (and ideally repair) silent bit-rot on cold drives.

### Layer 1 — Inventory: git-annex (the chosen spine)

[git-annex](https://git-annex.branchable.com/location_tracking/) tracks file *content* across many
repositories (each drive = a repo) while keeping only lightweight pointers in git. Why it fits
**this** fleet:

- **Location tracking without mounting.** Each repo records, by drive UUID, which drive last held
  each file's content — so "where is this?" is answerable with nothing plugged in, and it names the
  drive to grab.
- **`numcopies` directly retires the sole-copy risk.** Declare "keep ≥2 copies of the journalism
  archive" and git-annex refuses to drop below that and reports what is under-replicated. That is
  the Work-Desk `Expansion` exposure named in [[DRIVE-REGISTRY]] and
  [[WITNESS-PENDING-NOT-DONE-2026-06-21]], enforced mechanically.
- **Bit-rot detection built in.** Content is content-addressed (hashed); `git annex fsck` verifies
  bytes against their hashes — Layer 3 for free.
- **It is git.** The vault already *is* a git repo with a hardware register; DRIVE-REGISTRY is the
  human-readable companion to a git-annex location database. Cross-platform (Mac + Windows).

**Cost / caveat:** real learning curve, CLI habit. Lighter non-git substitute if that stalls: a
disk-catalog app — [NeoFinder](https://www.cdfinder.de/) (Mac; indexes offline disks across
exFAT/APFS/NTFS) or [catcli](https://github.com/deadc0de6/catcli) (cross-platform CLI). Those
answer "what's on the shelved drive?" but do **not** track copy-count or verify integrity, so
they must be paired with Layers 2–3 below.

### Layer 2 — Redundancy / 3-2-1: Backblaze **B2 + restic** (not Personal Backup)

- Use **Backblaze B2 + [restic](https://www.backblaze.com/docs/cloud-storage-integrate-restic-with-backblaze-b2)**
  (content-addressed, deduplicated, incremental, Object-Lock / ransomware-resistant) for the cold
  archive. This is the same B2 pattern already in the vault's storage manifests.
- **Avoid Backblaze *Personal Backup* for archive drives:** it treats an external drive detached
  >30 days as deleted and purges the cloud copy — fatal for drives you shelve
  ([Backblaze docs](https://help.backblaze.com/hc/en-us/articles/217664898)).
- **Local second copy:** the Work-Desk journalism archive (`Expansion`) should live on a second
  device — the 5 TB `storage` is the natural target — before it is trusted to one HDD.

### Layer 3 — Integrity: checksums + parity for cold drives

- Periodically verify cold trees with [`hashdeep`/md5deep](https://0x5.uk/2022/03/02/detecting-bit-rot-with-md5deep/).
- **PAR2** parity files repair *partial* corruption (RAID-for-a-single-file), not just detect it.
- git-annex folds detection into `fsck`; PAR2 still worth it for the most irreplaceable originals.

---

## Filesystem caveat (matters for a journalism archive)

The fleet is mostly **exFAT, which has no journaling** — an interrupted write (bad unplug, power
blip) can corrupt the volume with no recovery log
([OWC](https://software.owc.com/knowledge-base/why-not-exfat/),
[reliability notes](https://pawitp.medium.com/notes-on-exfat-and-reliability-d2f194d394c2)). Fine
for transfer/scratch; risky as the *system of record* for irreplaceable footage. Practical line:

- Keep exFAT only on the cross-platform **transfer** drives (`ExternalSSD`, `Vault`).
- For the **journalism archive**, either move to a journaled native FS (APFS if Mac-primary, NTFS
  if Windows-primary) **or** consciously accept exFAT + checksums + B2 as the mitigation.
- `timemachine` is already HFS+ — leave it.

---

## Mapped to the five drives

| Drive (role) | Recommendation |
| --- | --- |
| **`Expansion`** 4 TB · journalism archive | **Priority.** Into git-annex `numcopies ≥ 2` + B2/restic. This is the sole-copy exposure. |
| **`storage`** 5 TB · consolidation target | Primary annex repo and/or local 2nd copy of `Expansion`. |
| **`ExternalSSD`** (Samsung T5) · active scratch | Leave exFAT; the "never the only copy" rule already holds. |
| **`timemachine`** 1 TB · Mac backup | Leave as Time Machine / HFS+; do not repurpose. |
| **`Vault`** (LaCie Rugged) · staging/transfer | exFAT fine; transient only. |

---

## Phase 2 — when budget allows a mini-PC / homelab

When "always available + self-healing" outranks "grab-and-go portable," stop fighting bus-powered
USB and add an always-on host:

- **Cheap real NAS** (e.g. Ugreen NASync, Synology) — turnkey, lowest effort. `*` (models/prices
  not surveyed for this note — revisit at purchase time).
- **DAS + SnapRAID + StableBit DrivePool** on the Windows box — pooled volume with parity + monthly
  scrubs, reuses existing drives ([SnapRAID FAQ](https://www.snapraid.it/faq),
  [mergerfs+SnapRAID writeup](https://blog.dabbleden.com/index.php/2025/09/16/turning-my-home-server-into-a-nas/)).
- **TrueNAS / ZFS** mini-PC — strongest integrity (checksummed FS + scrubs), steeper setup.

In every Phase-2 option, **git-annex stays as the catalog/location layer** and the server becomes
one more always-on, redundant annex remote; **B2 stays the off-site leg.**

---

## Open decisions / next actions

- [ ] **Adopt git-annex** for the fleet (decision), or fall back to NeoFinder/catcli + manual
      Layers 2–3 if the CLI curve is unwanted.
- [ ] **Stand up B2 + restic** for the cold archive (retire any reliance on Personal Backup for
      shelved drives).
- [ ] **Resolve the `Expansion` sole-copy risk first** — mirror to `storage` and/or B2 before
      anything else.
- [ ] **Reclassify this note** — staged `doc_class: misc_reference` per VAULT-TEMPLATES §147 (no
      registered class for storage-management doctrine yet); Logan to register a `doctrine`/`strategy`
      class or leave as reference.
- [ ] **Phase 2 trigger** — revisit NAS/DAS/TrueNAS options when there's budget for a mini-PC; this
      note's Phase-2 section is a placeholder, not a survey.

---

## See also

[[DRIVE-REGISTRY]] (the hardware) · [[TECH-REGISTRY]] (parent index) · [[DEFRAG-MAP]] (the data
plane) · [[WITNESS-PENDING-NOT-DONE-2026-06-21]] (the durable-copy gap this strategy answers) ·
[[VAULT-MEDIA-STORAGE]] (size lanes) · [[LAF-USB-PROTOCOL-FRAMEWORK]] (carrier/topology)

---

## DOCUMENT METADATA

- **Created:** 2026-06-22
- **Last Updated:** 2026-06-22
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** First storage-management doctrine note, sibling to DRIVE-REGISTRY (hardware) — records the 2026-06-22 research pass. Core finding: the bus-powered single-purpose fleet wants a tracked/checksummed/location-aware archive (git-annex), not RAID pooling. Captures Logan's two-phase framing (git-annex + B2 + checksums now; mini-PC/homelab with real pooling later, git-annex surviving as the catalog layer), the three-layer model (inventory / 3-2-1 / integrity), the exFAT-no-journaling caveat, and a per-drive mapping that prioritizes the `Expansion` journalism-archive sole-copy risk. Staged `doc_class: misc_reference` pending a doctrine/strategy class decision. Phase-2 hardware options are placeholders (`*`), not a purchase survey.
