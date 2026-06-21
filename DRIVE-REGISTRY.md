---
title: "DRIVE-REGISTRY — Storage Devices as Hardware"
updated: 2026-06-21
status: draft
doc_class: registry-note
authority: LOGAN
authors:
  - Claude Code CLI
related:
  - TECH-REGISTRY
  - DEFRAG-MAP
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - HOME-DESK-MANIFEST-2026-05-08
  - WORK-DESK-MANIFEST-2026-05-08
  - TRAVEL-BAG-MANIFEST-2026-05-08
  - STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - VAULT-MEDIA-STORAGE
  - LAF-USB-PROTOCOL-FRAMEWORK
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - MESHWEB
  - USB
tags:
  - registry
  - hardware
  - storage
  - drives
  - usb
---

# DRIVE-REGISTRY — Storage Devices as Hardware

A subcomponent of [[TECH-REGISTRY]]. This is the **device-plane** record of Logan's
storage drives — each drive as a physical object with a role, an identity, and a
custody/backup posture. For *what is on each drive*, follow the pointer to the
**data plane** ([[DEFRAG-MAP]] §B2); this register does not restate contents.

> Origin: opened 2026-06-21 from a photo of a stack of bus-powered USB drives on the
> MacBook — aspirationally a "poor man's RAID/NAS," actually a fleet of single-purpose
> portable drives needing one holistic management surface. This is that surface.

---

## Reading rules (read before trusting a cell)

- **Identity is by role + label + serial/device, never drive letter.** Per
  [[LOCAL-STORAGE-INVENTORY-2026-05-08]] (active): *"drive letters are local Windows
  mount designators, not persistent device identities."* `D:`/`E:`/`F:` are observations,
  not identities, and shift between sessions ([[DEFRAG-MAP]] revision log).
- **`*` = named gap, not blank.** Per [[TECH-REGISTRY]] and vault epistemic doctrine, a
  field requiring physical evidence the author could not obtain carries `*`. This file was
  authored from a **`cloud`** runtime ([[MESHWEB]]) with **no drive mounted** — so serial,
  SMART health, encryption state, USB generation, and exact live contents are all `*`,
  pending a local-machine agent. Do not read `*` as "none"; read it as "unverified."
- **Grounded cells** cite an active/live source. Capacity, label, device model, and
  filesystem come from [[LOCAL-STORAGE-INVENTORY-2026-05-08]] and [[DEFRAG-MAP]] §B2.
- **NET/WEB/MESH bindings are provisional.** Logan has **not hard-locked** the definition
  of any of the six standards ([[NETWEB]] / [[WEBNET]] / [[MESHWEB]] / [[WEBMESH]] /
  [[MESHNET]] / [[NETMESH]]). The references below to [[NETWEB]] (portable filenames) and
  [[MESHWEB]] (cloud-authoring caveat) use their **current observed meanings, not fixed
  canon** — they may be redefined.
- **Fleet count: five drives total** — Logan, firsthand, 2026-06-21. Authoritative
  operator provenance the vault did not itself contain. Table A lists five catalogued
  drives **plus** a witnessed LaCie Rugged row; per this attestation the LaCie is **not a
  sixth device** — it is one of the five (identity TBD). ("Hard drives" reads as the drive
  fleet generally; note the Samsung T5 is an SSD and the `Vault` drive's media is `*` —
  media type stays a machine-verification field.)

---

## Table A — Hardware identity

| Role | Device (make / model) | Volume label | Capacity | Media / interface | Filesystem | Serial / UUID |
| --- | --- | --- | --- | --- | --- | --- |
| **Home Desk** | WD easystore 2624 USB HDD | `storage` (was `LoganF`) | ~4.55 TB | HDD / USB `*` | exFAT | `*` |
| **Work Desk** | Seagate Expansion HDD USB | `Expansion` | ~3.64 TB | HDD / USB `*` | exFAT | `*` |
| **Travel Bag** | Samsung Portable SSD T5 | `ExternalSSD` | 931 GB | SSD / USB `*` | exFAT | `*` |
| **Staging** | `*` (model not recorded) | `Vault` | ~2 TB | `*` | exFAT | `*` |
| **Backup (Mac)** | WD My Passport for Mac | `timemachine` | 1 TB | HDD / USB `*` | HFS+ | `*` |
| **one of 5 · TBD** | LaCie Rugged (orange bumper) | `*` | `*` | SSD or HDD `*` | `*` | `*` |

> [!important] The LaCie Rugged is one of the five — not a sixth drive
> Logan attests **five drives total** (2026-06-21), so the orange LaCie Rugged is **one of
> the five**, not a new device. It matches **no catalogued drive by recorded model** in
> [[DEFRAG-MAP]] §B2 / [[LOCAL-STORAGE-INVENTORY-2026-05-08]], so its identity is still TBD.
> **Leading hypothesis:** it is the **`Vault`** drive — the only catalogued drive whose
> device model was never recorded (`*`), making it the sole slot an unidentified LaCie can
> occupy without contradiction. This is a hypothesis, not a confirmed merge; the LaCie row
> below collapses into one catalogued row once verified at the machine.

---

## Table B — Management overlay (the fleet-management value-add)

| Role | Custody / location | Encryption | Backup posture — sole copy? | SMART / health | Current contents (data plane) | Last physically verified |
| --- | --- | --- | --- | --- | --- | --- |
| **Home Desk** | `*` (Windows-side) | `*` | `*` — consolidation **target**; treat as archive | `*` | [[DEFRAG-MAP]] §B2 `storage`: Photos Library, 2014→ personal | 2026-05-25 (Win `Get-Volume`) |
| **Work Desk** | `*` (Windows-side) | `*` | `*` — **journalism archive**; sole-copy risk if not mirrored | `*` | [[DEFRAG-MAP]] §B2 `Expansion`: Idaho Reports, Legislature, IDEX | 2026-05-25 (Win `Get-Volume`) |
| **Travel Bag** | `*` (portable) | `*` | **Not the only copy of anything** (doctrine, [[TRAVEL-BAG-MANIFEST-2026-05-08]]) | `*` | [[DEFRAG-MAP]] §B2 `ExternalSSD`: Adobe cache, exports, scratch | 2026-05-25 (Win `Get-Volume`) |
| **Staging** | `*` (Mac-side last seen) | `*` | `*` — scratch/staging; holds `rclone-logs/` | `*` | [[DEFRAG-MAP]] §B2 `Vault`: transfer logs, mostly empty | 2026-05-25 (Mac) |
| **Backup (Mac)** | `*` (with MacBook) | `*` | Time Machine **backup** of MacBook only — not for archive | `*` | Time Machine sparsebundle | 2026-05-25 (Mac) |
| **one of 5 · TBD** | MacBook desk (photo) | `*` | `*` — **unknown; could be a sole copy** | `*` | `*` | 2026-06-21 (photo only, not mounted) |

---

## Photographed stack — 2026-06-21

A second photo shows **all five drives** in one stack on the MacBook, confirming the
five-total count visually. Read top → bottom (labels and serials are not legible in the
photo — identity stays `*`):

| # | Position | Observed appearance | Observed form factor | Identity |
| --- | --- | --- | --- | --- |
| 1 | top | small, flat, black; blue sticker w/ red mark | portable SSD (small footprint) | `*` |
| 2 | upper-mid | tall, thick black box | 3.5" desktop HDD | `*` |
| 3 | mid | slim black with a silver/aluminum side band | 2.5" portable HDD | `*` |
| 4 | lower-mid | slim plain black | 2.5" portable | `*` |
| 5 | bottom | **orange LaCie Rugged**, activity LED lit | 2.5" rugged portable | the LaCie |

> [!warning] One desktop box, but two desktop-class drives are catalogued
> Only **one** tall 3.5"-desktop enclosure appears in the stack, yet [[DEFRAG-MAP]] §B2
> lists **two** desktop-class drives (`storage` ~4.6 TB WD easystore, `Expansion` ~3.7 TB
> Seagate). So the photographed five may **not** be a 1:1 match to the DEFRAG-MAP five — a
> desktop drive may be off-frame / on the Windows machine, and a portable in this stack may
> be one the data plane never catalogued. Do not assume a mapping; resolve by label + serial
> at the machine. (Form factors above are read from the photo; treat as observation with some
> inference, not confirmed spec.)

---

## Role taxonomy & management policy

The fleet's problem is mixed-duty drives. Each drive gets one canonical role, and the
role sets the rule. Roles below are the ones already named in the (draft) manifests,
plus the two unroled drives:

| Role | Doctrine source | Rule |
| --- | --- | --- |
| **Home Desk** | [[HOME-DESK-MANIFEST-2026-05-08]] (draft) | Broad personal/history archive + staging. |
| **Work Desk** | [[WORK-DESK-MANIFEST-2026-05-08]] (draft) | Professional/journalism archive + working surface. |
| **Travel Bag** | [[TRAVEL-BAG-MANIFEST-2026-05-08]] (draft) | Lean portable active-work only — **never the sole copy**. |
| **Staging** | — | Transient transfer/scratch; not durable archive. |
| **Backup** | — | Mirror/Time Machine; protects a source, is not itself a source. |

**The 3-2-1 overlay (this register's reason to exist):** anything irreplaceable should
exist on ≥2 devices with ≥1 copy off-site/offline. The **sole-copy** column in Table B is
the risk surface — every `*` there is an unanswered "is this the only copy?" The most
likely real exposure is the **Work Desk journalism archive** (Idaho Reports / Legislature
originals): confirm it is mirrored before trusting one HDD. Size lanes for anything pulled
into the vault follow [[VAULT-MEDIA-STORAGE]] (≤100 MB direct / ≤2 GB LFS / >2 GB external
+ [[LAF-USB-OBJECT-MANIFEST-2026-05-08]]).

---

## Last-mile checkup — FOR A LOCAL-MACHINE AGENT

> [!important] Cannot be done from `cloud`. Requires an agent on the **MacBook** and/or
> **Windows** with drives mounted. Resolve drives by **role + label/serial**, never by
> letter ([[EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08]]). Non-destructive only.

- [ ] **Mount + identify** every drive; capture **serial/UUID + device model** (macOS
      `diskutil info`, `system_profiler SPUSBDataType`; Windows `Get-Disk`/`Get-Volume`)
      and fill the `*` identity cells in Table A.
- [ ] **Resolve the LaCie Rugged** — Logan attests five total, so it is one of the five.
      Test the **`Vault`** hypothesis first (does the orange LaCie mount as `Vault`, ~2 TB
      exFAT?). Record model, capacity, filesystem, label, serial; then **merge** its row
      into the matching catalogued drive so the table shows five.
- [ ] **Encryption state** per drive (FileVault/BitLocker/hardware) → Table B.
- [ ] **SMART health** (`smartctl -a`, or LaCie/WD/Seagate tools) → Table B.
- [ ] **USB generation / interface** (USB 3.0 / 3.1 / etc.) → Table A.
- [ ] **Answer the sole-copy question** for each archive drive, especially **Work Desk**;
      flag every drive that holds the only copy of anything irreplaceable.
- [ ] **Promote** — once verified, change `status: draft` and report to Logan for standing
      elevation per [[CONSTITUTION]] § VII. Update [[TECH-REGISTRY]] subcomponent state.

---

## DOCUMENT METADATA

- **Created:** 2026-06-21
- **Last Updated:** 2026-06-21
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** First device-plane drive register. Grounded identity from active storage inventories; all physical-evidence fields marked `*` (authored from `cloud`, no drive mounted). Flagged the orange LaCie Rugged as an unlogged device witnessed in the 2026-06-21 photo. Added role taxonomy, 3-2-1 sole-copy overlay, and a local-machine verification checklist. Added the caveat that NET/WEB/MESH standard definitions are not hard-locked by Logan. Recorded Logan's firsthand attestation of five drives total (2026-06-21) and reconciled the LaCie Rugged from a presumed sixth device to one of the five (identity TBD; `Vault` the leading hypothesis). Added a photographed-stack observation (five physical units by form factor, top→bottom) and flagged the one-desktop-box-vs-two-catalogued tension.
