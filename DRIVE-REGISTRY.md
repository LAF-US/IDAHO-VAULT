---
title: "DRIVE-REGISTRY — Storage Devices as Hardware"
created: 2026-06-21
updated: 2026-06-21
status: draft
doc_class: registry-note
authority: LOGAN
authors:
  - Claude Code CLI
related:
  - TECH-REGISTRY
  - DRIVE-MANAGEMENT
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
  [[LOCAL-STORAGE-INVENTORY-2026-05-08]] (active): drive letters are local mount designators,
  not persistent identities; `D:`/`E:`/`F:` shift between sessions.
- **`*` = named gap, not blank** — a field whose physical evidence isn't in hand. Read it as
  "unverified," not "none."
- **`⟨redacted⟩` = known-but-withheld**, distinct from `*`. The per-unit serial numbers were
  read from the photos and are *known*, but are held out of the public record until the vault has
  a stable secrets/variables mechanism to carry them. Read it as "captured, not published," not
  "unverified." Restore from that store when it exists.
- **Identity source: 2026-06-21 label photos.** Make/model/serial/capacity were read from ten
  close-up photos — **two per drive, top and bottom of the same five drives** in the original
  stack. Each drive's two faces were paired by enclosure (not by sticker). The **Filesystem**
  column is **not** photo-derived — it is carried from the catalogue ([[DEFRAG-MAP]] §B2 /
  prior inventories). Volume label, encryption, SMART, and live mount state are still `*` (not
  shown in the photos and not yet read at the machine).
- **The fleet is five drives** (Logan, firsthand). Four spinning HDDs + one SSD (the Samsung
  T5). This maps 1:1 onto the five drives in [[DEFRAG-MAP]] §B2 — see the Role/label column.
- **NET/WEB/MESH bindings are provisional.** Logan has not hard-locked the definitions of
  [[NETWEB]] / [[WEBNET]] / [[MESHWEB]] / [[WEBMESH]] / [[MESHNET]] / [[NETMESH]].
- **Capacities** are vendor-label decimal TB where the model/label is known (WD `0050`=5 TB,
  `0010`=1 TB); where the label wasn't photographed they are OS-reported (`~931 GB`, the T5) or
  estimated-until-verified (`~2 TB *`, the LaCie) — never measured TiB.

---

## Table A — Hardware identity (five drives, from 2026-06-21 label photos)

| Role / volume label | Make / model | Capacity | Media | Serial | Filesystem | Photos | Physical marks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Home Desk** · `storage` | WD easystore — P/N `WDBKUZ0050BBK-…EA` | 5 TB | HDD | `⟨redacted⟩` | exFAT | top+label (3,4) | — |
| **Work Desk** · `Expansion` | Seagate Expansion HDD — `SRD0NF1`, P/N `3EAP9-500` | 4 TB | HDD | `⟨redacted⟩` | exFAT | top+label (7,8) | mfg 2022 |
| **Travel Bag** · `ExternalSSD` | Samsung Portable SSD **T5** | ~931 GB | **SSD** | `*` (not on shown faces) | exFAT | both faces (9,10) | "I ♥ Idaho PTV" · IPTV business card |
| **Backup** · `timemachine` | WD **My Passport for Mac** — P/N `WDBLUZ0010BSL-03` | 1 TB | HDD | `⟨redacted⟩` | HFS+ | lid+underside (5,6) | silver lid marker "TIME MACHINE / MacBook Pro backup" · underside "Double Scorpio" sticker |
| **Staging** · `Vault` | **LaCie Rugged** (orange bumper) | ~2 TB `*` | HDD (likely) `*` | `*` (label not shot) | exFAT | both faces (1,2) | trout/Idaho · "The Flicks" stickers |

**Four HDDs + one SSD** (the T5). The earlier "Double Scorpio" and "I ♥ Idaho PTV" were **not**
separate drives — they are the underside of the Time Machine drive and a face of the T5,
respectively. Pairing proof: photo 10 is the T5, so its only possible second face is 9 (5 and
6 are WD); that leaves 5+6 as the one My Passport for Mac.

> [!note] `Vault` resolved
> The 2026-06-21 photos confirm the **LaCie Rugged is the catalogue's `Vault` drive** — the
> five photographed drives map 1:1 onto [[DEFRAG-MAP]] §B2 (`storage`, `Expansion`,
> `ExternalSSD`, `timemachine`, `Vault`). Its own capacity/serial label was not photographed;
> `~2 TB` is carried from the catalogue, to confirm at the machine.

---

## Table B — Management overlay (the fleet-management value-add)

| Role | Custody / location | Encryption | Backup posture — sole copy? | SMART / health | Current contents (data plane) |
| --- | --- | --- | --- | --- | --- |
| **Home Desk** · `storage` | `*` | `*` | `*` — consolidation **target**; treat as archive | `*` | [[DEFRAG-MAP]] §B2 `storage`: Photos Library, 2014→ personal |
| **Work Desk** · `Expansion` | `*` | `*` | `*` — **journalism archive**; sole-copy risk if not mirrored | `*` | [[DEFRAG-MAP]] §B2 `Expansion`: Idaho Reports, Legislature, IDEX |
| **Travel Bag** · `ExternalSSD` | portable | `*` | **Not the only copy of anything** ([[TRAVEL-BAG-MANIFEST-2026-05-08]]) | `*` | [[DEFRAG-MAP]] §B2 `ExternalSSD`: Adobe cache, exports, scratch |
| **Backup** · `timemachine` | with MacBook | `*` | Time Machine **backup** of the MacBook only — not an archive source | `*` | Time Machine sparsebundle |
| **Staging** · `Vault` | Mac-side | `*` | `*` — scratch/staging; held `rclone-logs/` | `*` | [[DEFRAG-MAP]] §B2 `Vault`: transfer logs, mostly empty |

---

## Photographed evidence — 2026-06-21

Two rounds: a **stack photo** (all five on the MacBook) and **ten label close-ups** (top +
bottom of each of the five). The pairing that resolves the ten to five:

| Drive | Top face | Bottom / label face |
| --- | --- | --- |
| LaCie Rugged (`Vault`) | trout + Idaho sticker | "The Flicks" + eye sticker (no printed label visible) |
| WD easystore (`storage`) | WD easystore logo | regulatory label `WDBKUZ0050BBK`, 5 TB |
| WD My Passport for Mac (`timemachine`) | silver lid, "TIME MACHINE" | black underside `WDBLUZ0010BSL`, 1 TB + "Double Scorpio" |
| Seagate Expansion (`Expansion`) | Seagate logo (ribbed) | regulatory label `SRD0NF1`, 4 TB |
| Samsung T5 (`ExternalSSD`) | "I ♥ Idaho PTV" sticker | business card; "Samsung T5" on the side edge |

> Note: label photos are kept **chat-only**, not committed. Drive **serials were captured but
> are now `⟨redacted⟩`** in the public record (held until a stable secrets/variables mechanism
> exists); the IPTV business-card contact details on the T5 are **not** transcribed — only the
> fact a card is affixed.

*Sticker note: the `timemachine` drive's **"Double Scorpio"** sticker is the owner's chart —
Scorpio Moon + Scorpio Rising (see [[Logan Finney]]).*

---

## Role taxonomy & management policy

Each drive has one canonical role; all five are now assigned (matching the draft manifests
and the catalogue labels).

| Role | Doctrine source | Rule |
| --- | --- | --- |
| **Home Desk** · `storage` | [[HOME-DESK-MANIFEST-2026-05-08]] (draft) | Broad personal/history archive + staging. |
| **Work Desk** · `Expansion` | [[WORK-DESK-MANIFEST-2026-05-08]] (draft) | Professional/journalism archive + working surface. |
| **Travel Bag** · `ExternalSSD` | [[TRAVEL-BAG-MANIFEST-2026-05-08]] (draft) | Lean portable active-work only — **never the sole copy**. |
| **Backup** · `timemachine` | — | Time Machine; protects the MacBook, is not itself a source. |
| **Staging** · `Vault` | — | Transient transfer/scratch; not a durable archive. |

**The 3-2-1 overlay (this register's reason to exist):** anything irreplaceable should exist on
≥2 devices with ≥1 copy off-site/offline. Every `*` in Table B's sole-copy column is an
unanswered "is this the only copy?" The most likely real exposure is the **Work Desk journalism
archive** (Idaho Reports / Legislature originals): confirm it is mirrored before trusting one
HDD. Size lanes for anything pulled into the vault follow [[VAULT-MEDIA-STORAGE]] (≤100 MB direct
/ ≤2 GB LFS / >2 GB external + [[LAF-USB-OBJECT-MANIFEST-2026-05-08]]).

---

## Last-mile checkup — FOR A LOCAL-MACHINE AGENT

> [!important] Cannot be done from `cloud`. Requires an agent on the **MacBook** and/or
> **Windows** with drives mounted. Resolve by **role + label/serial**, non-destructive only.

- [x] **Identify all five** — done from 2026-06-21 label photos; fleet = 5 (4 HDD + 1 SSD).
- [x] **Resolve `Vault`** — it is the LaCie Rugged.
- [ ] **Capture the two missing serials** — the **LaCie** (`Vault`) and **Samsung T5** labels
      weren't in frame; confirm capacity too (LaCie `~2 TB` is from the catalogue, not the label).
- [ ] **Volume label + filesystem** per drive (mount + `diskutil`/`Get-Volume`).
- [ ] **Encryption + SMART + USB generation** → Table B.
- [ ] **Sole-copy answer** for each archive drive, especially **Work Desk**.
- [ ] **Promote** — once verified, flip `status` and report to Logan for standing elevation per
      [[CONSTITUTION]] § VII; update [[TECH-REGISTRY]] subcomponent state.

---

## DOCUMENT METADATA

- **Created:** 2026-06-21
- **Last Updated:** 2026-06-21
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** First device-plane drive register; doctrine, role taxonomy, 3-2-1 overlay, and a local-machine checklist. **Identity corrected 2026-06-21:** the ten label photos are top+bottom of **five** drives (not six). An earlier pass mis-read two faces of the Time Machine drive (silver "TIME MACHINE" lid + black "Double Scorpio" underside, `WDBLUZ0010BSL`) as two drives and mis-attached the Samsung T5's "I ♥ Idaho PTV" face to the phantom; corrected by pairing each drive's faces by enclosure and by elimination. Confirmed the **LaCie Rugged is the `Vault` drive**, giving a clean 1:1 map onto the [[DEFRAG-MAP]] five (storage / Expansion / ExternalSSD / timemachine / Vault). Captured serials for easystore (5 TB), Seagate (4 TB), and the My Passport for Mac (1 TB); LaCie and T5 serials/capacity still `*`. **Serials redacted 2026-06-21** at Logan's direction — the three captured serials are now `⟨redacted⟩` (known-but-withheld, distinct from `*`), held out of the public record until the vault has a stable secrets/variables mechanism to carry them.
