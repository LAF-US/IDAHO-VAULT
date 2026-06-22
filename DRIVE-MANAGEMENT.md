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
- **Avoid Backblaze *Personal Backup* for archive drives:** by **default** it treats an external
  drive detached >30 days as deleted and purges the cloud copy — fatal for drives you shelve.
  (Extended Version History lengthens retention, but the periodic-reattach expectation remains;
  **B2 avoids the re-attach requirement entirely**.) ([Backblaze docs](https://help.backblaze.com/hc/en-us/articles/217664898)).
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
- **`timemachine`** — don't repurpose or reformat the Time Machine volume; let Time Machine own
  it (its on-disk format, HFS+ or APFS, follows the macOS version).

---

## Encryption (high priority — some keys already in 1Password)

Encryption is a top priority, so it gets its own layer model rather than a footnote. Use **three
independent encryption boundaries** (defense in depth — a break in one doesn't expose the data):

1. **Volume encryption — the foundation, do this first.** Every drive gets full-volume
   encryption: **FileVault / APFS-encrypted** on the Mac, **BitLocker or VeraCrypt** on the
   Windows-side drives. This protects *everything* at rest — annex working files, the backup repo,
   scratch — against a lost or seized disk, independent of any tool above it.
2. **Backup-repo encryption.** **restic encrypts by default** (AES-256 + authenticated), gated by
   a repo password — so the backup is safe even on an untrusted target (a cloud bucket, a drive
   that walks). This is **why the history layer is restic, not bup:** bup has **no native
   encryption**, and git-annex's bup special remote *requires* `encryption=none`. restic is also
   **natively cross-platform** (Mac + Windows, no WSL), so the Windows box stops being a special
   case. (bup only earns a place for VM-image-scale hashsplitting — not a footage/document archive.)
3. **Off-site / cloud encryption — GPG-free *at this stage* (an implementation choice, not a design rule).**
   The restic repo is already encrypted (layer 2), so it can go straight to B2. If git-annex
   *itself* needs an encrypted cloud remote, the lowest-friction option **right now** is an
   **`rclone` special remote over an `rclone crypt` backend** (NaCl/secretbox — no GPG) rather than
   git-annex's GPG `encryption=hybrid`. Rationale (surveyed 2026-06-22): the vault's **current**
   signing/encryption implementation is SSH-key commit signing via the 1Password agent, with **no
   GPG keyring stood up yet** (`.gnupg/` gitignored, `gpg.format=ssh`, `required_signatures` met by
   SSH). That's a stage, **not a deliberate GPG-free design** — GPG isn't excluded, just not
   deployed — so at this stage it's simpler not to introduce GPG for a single annex remote.
   **If/when GPG gets stood up vault-wide** (e.g. for broader at-rest encryption or PGP-based
   workflows), git-annex's `encryption=hybrid` becomes a natural option to revisit.

### Key management — keys in 1Password (`op`)

Encryption is only as strong as where the keys live, and the vault already runs **1Password**
(some keys are already in `op`). Keep every passphrase out of plaintext config and inside `op`:

- **restic repo password** → `RESTIC_PASSWORD_COMMAND="op read op://Vault/restic/password"`.
- **B2 application keys** and **git-annex remote creds** (the `rclone crypt` password / B2 keys —
  no GPG key needed *at this stage*) → `op` (same pattern as the vault's existing `OP_SERVICE_ACCOUNT_TOKEN` flow).
- **Volume recovery keys** (FileVault / BitLocker) → `op`.

This is the same "stable secrets mechanism" flagged for the redacted drive serials in
[[DRIVE-REGISTRY]] (`⟨redacted⟩`) — one secrets store, fetched at runtime, nothing in cleartext.

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
- [ ] **Stand up restic → B2** for the encrypted versioned history (the chosen history layer over
      bup; retire any reliance on Personal Backup for shelved drives).
- [ ] **Encrypt every drive volume** (FileVault / BitLocker / VeraCrypt) — the foundation layer,
      do this before trusting any drive with source-sensitive material.
- [ ] **Put backup/remote keys in 1Password** (some already in `op`): restic password, B2 app
      keys, git-annex GPG/remote creds, FileVault/BitLocker recovery keys.
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
- **Change Note:** First storage-management doctrine note, sibling to DRIVE-REGISTRY (hardware) — records the 2026-06-22 research pass. Core finding: the bus-powered single-purpose fleet wants a tracked/checksummed/location-aware archive (git-annex), not RAID pooling. Captures Logan's two-phase framing (git-annex + B2 + checksums now; mini-PC/homelab with real pooling later, git-annex surviving as the catalog layer), the three-layer model (inventory / 3-2-1 / integrity), the exFAT-no-journaling caveat, and a per-drive mapping that prioritizes the `Expansion` journalism-archive sole-copy risk. Staged `doc_class: misc_reference` pending a doctrine/strategy class decision. Phase-2 hardware options are placeholders (`*`), not a purchase survey. **Encryption pass 2026-06-22:** added a dedicated three-layer encryption model (volume / restic-repo / git-annex encrypted off-site), recorded the **restic-over-bup** decision (bup has no native encryption and is Windows-via-WSL only; restic encrypts by default and is natively cross-platform), and the 1Password (`op`) key-management tie-in — keys partly in `op` already, same secrets mechanism as the redacted serials. **GPG-posture pass 2026-06-22:** surveyed existing vault signing/encryption deployment and found the **current implementation** is SSH/1Password signing with **no GPG keyring stood up yet** (`.gnupg/` gitignored, `gpg.format=ssh`, `required_signatures` met by SSH) — and **no documented decision to avoid GPG**, so this is a stage, not a GPG-free *design*. Revised the off-site layer to stay GPG-free *at this stage* (restic AES + an `rclone crypt` special remote, not git-annex's GPG `encryption=hybrid`) to avoid a net-new dependency for now, while explicitly leaving `encryption=hybrid` on the table if/when GPG is deployed vault-wide.
