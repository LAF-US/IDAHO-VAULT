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
- **`*` = named gap, not blank.** A field requiring physical evidence the author could not
  obtain carries `*`. Read it as "unverified," not "none."
- **Identity source — now partly photographic.** Make/model/serial/capacity in Table A were
  read from **ten close-up drive-label photos (2026-06-21)** Logan supplied — direct
  physical evidence, an upgrade on the earlier `cloud`-only authoring ([[MESHWEB]]). Volume
  label, filesystem, encryption, SMART, and live mount state are **still `*`** (photos don't
  show them); those remain for a local-machine agent.
- **Fleet: six physical units = five HDDs + one SSD.** The 2026-06-21 photos resolve the
  fleet to six drives. Logan's "**five hard drives**" attestation reconciles exactly: the
  five spinning HDDs are the "hard drives"; the **Samsung T5 is an SSD**, the +1. (So the
  earlier "LaCie is one of five" framing is superseded — see Table A.)
- **The fleet has changed since the May catalogue.** Four drives map cleanly to
  [[DEFRAG-MAP]] §B2 (`storage`/`Expansion`/`ExternalSSD`/`timemachine`), but the catalogue's
  2 TB `Vault` drive **does not appear** in the photos, and a **new, never-catalogued** WD My
  Passport 1 TB does. Treat the catalogue as a prior snapshot, not the current fleet.
- **NET/WEB/MESH bindings are provisional.** Logan has **not hard-locked** the definition of
  any of the six standards ([[NETWEB]] / [[WEBNET]] / [[MESHWEB]] / [[WEBMESH]] / [[MESHNET]]
  / [[NETMESH]]); references here use current observed meanings, not fixed canon.
- **Capacities are nominal.** Vendor-label decimal TB (e.g. WD `0050` = 5 TB, `0010` = 1 TB),
  not measured TiB. Confirm exact byte counts at the machine.

---

## Table A — Hardware identity (from 2026-06-21 label photos)

| Role | Device (make / model) | Capacity | Media / interface | Serial | Volume label | Filesystem | Physical marks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Home Desk** | WD easystore — P/N `WDBKUZ0050BBK-…EA` | 5 TB | HDD / USB `*` | `WX21E…944029` (partial read) | `storage` (was `LoganF`) | exFAT | — |
| **Work Desk** | Seagate Expansion HDD — model `SRD0NF1`, P/N `3EAP9-500` | 4 TB | HDD / USB `*` | `NT199393E` | `Expansion` | exFAT | mfg 2022 |
| **Travel Bag** | Samsung Portable **SSD** T5 | ~1 TB | **SSD** / USB `*` | `*` (underside not shot) | `ExternalSSD` | exFAT | IPTV business card taped on |
| **Backup (Mac)** | WD My Passport for Mac | ~1 TB | HDD / USB `*` | `*` (underside not shot) | `timemachine` | HFS+ | marker: "TIME MACHINE / MacBook Pro backup / Logan Finney" |
| **Role TBD** | WD My Passport — P/N `WDBLUZ0010BSL-03` | 1 TB | HDD / USB `*` | `WX61EC3HYY90` | `*` | `*` | "Double Scorpio" sticker + "I ♥ Idaho PTV" |
| **Role TBD** | LaCie Rugged (orange bumper) | `*` | HDD (presumed) / USB `*` | `*` (label not shot) | `*` | `*` | trout, Idaho/pink-triangle, "The Flicks" stickers |

**Five HDDs** = Home Desk, Work Desk, Backup, and the two Role-TBD drives. **One SSD** = the
Samsung T5. Six units total; "five hard drives" = the five HDDs.

> [!important] Two open identity questions
> 1. **The catalogue `Vault` (2 TB) is unaccounted for.** No 2 TB drive is in the photos. It
>    is either the **LaCie** (capacity unread — possibly 2 TB) or **absent/elsewhere/retired**.
>    The earlier "LaCie = Vault" lead is now only one of two options, weakened because the
>    Double Scorpio proves the fleet gained uncatalogued drives.
> 2. **The "Double Scorpio" WD My Passport 1 TB is brand-new to the record** — not in
>    [[DEFRAG-MAP]] or [[LOCAL-STORAGE-INVENTORY-2026-05-08]]. It needs a role and a
>    data-plane contents check.

---

## Table B — Management overlay (the fleet-management value-add)

| Role | Custody / location | Encryption | Backup posture — sole copy? | SMART / health | Current contents (data plane) | Identity verified |
| --- | --- | --- | --- | --- | --- | --- |
| **Home Desk** | `*` | `*` | `*` — consolidation **target**; treat as archive | `*` | [[DEFRAG-MAP]] §B2 `storage`: Photos Library, 2014→ personal | label photo 2026-06-21 |
| **Work Desk** | `*` | `*` | `*` — **journalism archive**; sole-copy risk if not mirrored | `*` | [[DEFRAG-MAP]] §B2 `Expansion`: Idaho Reports, Legislature, IDEX | label photo 2026-06-21 |
| **Travel Bag** | `*` (portable) | `*` | **Not the only copy of anything** ([[TRAVEL-BAG-MANIFEST-2026-05-08]]) | `*` | [[DEFRAG-MAP]] §B2 `ExternalSSD`: Adobe cache, exports, scratch | photo (no serial) |
| **Backup (Mac)** | with MacBook | `*` | Time Machine **backup** of MacBook only — not an archive source | `*` | Time Machine sparsebundle | photo (no serial) |
| **Double Scorpio** (TBD) | `*` | `*` | `*` — **unknown; could be a sole copy** | `*` | `*` — not yet in data plane | label photo 2026-06-21 |
| **LaCie** (TBD) | MacBook desk | `*` | `*` — **unknown; could be a sole copy** | `*` | `*` | top-sticker photos only |

---

## Photographed evidence — 2026-06-21

Two rounds: a **stack photo** (all units on the MacBook) and **ten label close-ups**. The
close-ups resolve the earlier form-factor guesses to confirmed identities:

| Stack position (earlier guess) | Resolved identity |
| --- | --- |
| top — small flat black, sticker | Samsung **T5 SSD** (IPTV business card) |
| upper-mid — tall thick black box | WD **easystore** 5 TB |
| mid — slim black, silver band | WD **My Passport for Mac** ("TIME MACHINE") *or* Seagate Expansion |
| lower-mid — slim black | WD **My Passport** 1 TB ("Double Scorpio") *or* Seagate Expansion |
| bottom — orange | **LaCie Rugged** |

The earlier "one desktop box vs two catalogued desktop drives" tension **resolves**: only the
WD easystore is desktop-class; the Seagate Expansion here is the **portable** 2.5″ variant, not
a 3.5″ desktop unit. (Exact stack-to-drive order for the two slim blacks is not certain — both
are WD/Seagate 2.5″ portables; confirm at the machine.)

> Note: label photos are kept **chat-only**, not committed. Drive **serials are transcribed
> here** into the public record; the IPTV business-card contact details (email/phone on the
> Travel Bag T5) are **deliberately not transcribed** — only the fact a card is affixed.

---

## Role taxonomy & management policy

Each drive gets one canonical role. Four are set; two (Double Scorpio, LaCie) await a role.

| Role | Doctrine source | Rule |
| --- | --- | --- |
| **Home Desk** | [[HOME-DESK-MANIFEST-2026-05-08]] (draft) | Broad personal/history archive + staging. |
| **Work Desk** | [[WORK-DESK-MANIFEST-2026-05-08]] (draft) | Professional/journalism archive + working surface. |
| **Travel Bag** | [[TRAVEL-BAG-MANIFEST-2026-05-08]] (draft) | Lean portable active-work only — **never the sole copy**. |
| **Backup** | — | Mirror/Time Machine; protects a source, is not itself a source. |
| **(unassigned)** | — | Double Scorpio (WD 1 TB) and the LaCie Rugged — roles TBD by Logan. |

**The 3-2-1 overlay (this register's reason to exist):** anything irreplaceable should exist
on ≥2 devices with ≥1 copy off-site/offline. Every `*` in Table B's sole-copy column is an
unanswered "is this the only copy?" The most likely real exposure stays the **Work Desk
journalism archive** (Idaho Reports / Legislature originals): confirm it is mirrored before
trusting one HDD. Size lanes for anything pulled into the vault follow [[VAULT-MEDIA-STORAGE]]
(≤100 MB direct / ≤2 GB LFS / >2 GB external + [[LAF-USB-OBJECT-MANIFEST-2026-05-08]]).

---

## Last-mile checkup — FOR A LOCAL-MACHINE AGENT

> [!important] Cannot be done from `cloud`. Requires an agent on the **MacBook** and/or
> **Windows** with drives mounted. Resolve by **role + label/serial**, non-destructive only.

- [x] **Make / model / capacity / serial** — captured from 2026-06-21 label photos for 4 of 6
      drives; **partial** for the easystore serial; **missing** for the T5 + My Passport-for-Mac
      undersides and the **LaCie** (no label shot).
- [ ] **Shoot the missing undersides** — LaCie Rugged label, Samsung T5, WD My Passport for Mac.
- [ ] **Resolve the `Vault` question** — does the **LaCie** mount as `Vault` (~2 TB)? If not, is
      the 2 TB Vault retired/elsewhere? Record the LaCie's real capacity/label/serial.
- [ ] **Assign roles** to the Double Scorpio (WD 1 TB) and the LaCie.
- [ ] **Volume label + filesystem** per drive (mount + `diskutil`/`Get-Volume`) → Table A.
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
- **Change Note:** First device-plane drive register; doctrine, role taxonomy, 3-2-1 overlay, NET/WEB/MESH and cloud-authoring caveats, and a local-machine checklist. **Major identity update 2026-06-21:** ten drive-label close-up photos resolved the fleet to six physical units (five HDDs + one SSD), reconciling Logan's "five hard drives" via the Samsung T5 being the lone SSD. Captured real make/model/serial/capacity for the WD easystore (5 TB), Seagate Expansion (4 TB, SRD0NF1, NT199393E), and a newly-identified WD My Passport 1 TB ("Double Scorpio", WDBLUZ0010BSL, WX61EC3HYY90); confirmed Samsung T5 and WD My Passport-for-Mac by sight. Found the catalogue's 2 TB `Vault` unaccounted-for and weakened the prior "LaCie = Vault" lead. Serials transcribed to the record; label photos kept chat-only; business-card PII not transcribed.
