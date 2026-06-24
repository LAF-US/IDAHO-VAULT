---
title: "TECH-REGISTRY — Hardware & Device Index"
created: 2026-06-21
updated: 2026-06-21
status: draft
doc_class: registry-note
authority: LOGAN
authors:
  - Claude Code CLI
related:
  - DRIVE-REGISTRY
  - DEFRAG-MAP
  - LOCAL-STORAGE-INVENTORY-2026-05-08
  - STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17
  - VAULT-MEDIA-STORAGE
  - LAF-USB-PROTOCOL-FRAMEWORK
  - MESHWEB
  - USB
  - VAULT-CONVENTIONS
  - CONSTITUTION
tags:
  - registry
  - hardware
  - infrastructure
  - tech
---

# TECH-REGISTRY — Hardware & Device Index

The standing index of Logan's **physical technology** — the devices as objects,
not the data on them. This is the parent register; each gear class is a
subcomponent. It exists because the vault has a mature **data plane** (what
files live where) but no **device plane** (the machines and drives themselves).

> [!note] Two planes, deliberately separate
> The storage constellation — [[DEFRAG-MAP]], [[LOCAL-STORAGE-INVENTORY-2026-05-08]],
> the role manifests, [[STORAGE-LFS-USB-CONSTELLATION-INDEX-2026-06-17]] — inventories
> **payload**: folders, sizes, free space, migration state. This registry inventories
> **hardware**: make, model, serial, interface, encryption, health, custody, and
> whether a device holds the only copy of anything. The device plane *points at* the
> data plane for contents; it does not restate it. Keep them distinct so neither drifts.

This note answers the empty slot named in [[USB]]: the disambiguation node records
that **Universal Serial Bus** (the hardware/local-machine bus sense) has no dedicated
hardware note and says to "use explicit prose unless a dedicated hardware note exists."
[[DRIVE-REGISTRY]] is that note for storage devices; this parent generalizes it to all gear.

---

## Subcomponent index

| Subcomponent | Scope | State | Note |
| --- | --- | --- | --- |
| [[DRIVE-REGISTRY]] | External & internal storage drives as physical devices | **drafted** | The first and only built child; see for the live drive table and last-mile verification checklist. |
| [[COMPUTE-REGISTRY]] | Computers & phones (2015 MacBook Pro, Windows `ZBFURY`, Pixel) | *planned stub* | Evidence already in vault: [[DEFRAG-MAP]] §B1, [[research/2026-06-17-macbook-pro-12-1-early-2015]], [[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]]. Not yet built. |
| [[PERIPHERAL-REGISTRY]] | Hubs, docks, cables, card readers | *planned stub* | The powered-USB-hub gap for a portable-drive fleet lives here. Not yet built. |
| [[NETWORK-REGISTRY]] | Router, NAS-if-it-ever-exists, local network | *planned stub* | Not yet built. |
| [[SOFTWARE-ACCOUNTS-REGISTRY]] | Licenses, cloud storage accounts, key software | *planned stub* | Overlaps [[PLUGIN-REGISTRY]] (Obsidian) and the `.op` credential layer; scope TBD. Not yet built. |

**Build rule:** subcomponents are built when there is a real need and real evidence,
not speculatively (per [[VAULT-CONVENTIONS]] § Guiding Principles — "only build what's
needed now"). Stubs above are a map of intent, not a backlog commitment.

---

## Doctrine this register binds to

| Source | Status | What it governs here |
| --- | --- | --- |
| [[VAULT-METADATA-STANDARD]] | active | Required header/footer, lifecycle enum. |
| [[VAULT-MEDIA-STORAGE]] | live (hook/CI-enforced) | Size lanes for any payload referenced from device rows. |
| [[LAF-USB-PROTOCOL-FRAMEWORK]] | staged | Carrier lanes, USB phase model (DISCOVER→…→RETIRE), object-reference shape. |
| [[MESHWEB]] | active | Runtime scope (`local`/`cloud`/`ci`). This file was authored from **cloud** — see caveat. |
| [[LOCAL-STORAGE-INVENTORY-2026-05-08]] | active | Identity-by-label-not-letter doctrine. |
| [[CONSTITUTION]] § VII | live | Lifecycle vocabulary; only Logan promotes `draft` → standing. |

> [!caution] The NET/WEB/MESH standards are NOT hard-locked
> As of 2026-06-21, **Logan has not hard-locked the definition of any of the six**
> NET/WEB/MESH portability standards — [[NETWEB]], [[WEBNET]], [[MESHWEB]], [[WEBMESH]],
> [[MESHNET]], [[NETMESH]]. The bindings above (NETWEB ≈ filesystem-path portability,
> MESHWEB ≈ runtime portability, MESHNET ≈ sync-topology portability) are **current
> observed readings from the present files, not ratified canon.** A file's `status: active`
> or its CI enforcement reflects that file's own lifecycle — not a locked *definition* of
> the standard. Treat every NET/WEB/MESH binding in this register as provisional and
> subject to change until Logan fixes it.

> [!warning] Authored from `cloud` — DISCOVER phase only
> Per [[MESHWEB]], a `cloud` agent cannot read device serials, SMART health, encryption
> state, or live disk contents. Fields requiring physical evidence carry the `*` wildcard
> (the vault convention for *name the gap, do not fill it*). Converting `*` → fact is a
> task for a **local-machine agent** with the hardware mounted. This register is a
> record-of-intent until then.

---

## Authority

This is a `draft` candidate, not canon. Roles, identities, and gaps recorded here
await Logan's verification and promotion. Agents may extend rows and add subcomponents
under existing house conventions; status elevation (`draft` → standing) is Logan's alone,
per [[CONSTITUTION]] § VII.

---

## DOCUMENT METADATA

- **Created:** 2026-06-21
- **Last Updated:** 2026-06-21
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** Established the parent hardware/device register and its subcomponent map; bound it to live storage, metadata, and runtime-portability doctrine; built [[DRIVE-REGISTRY]] as the first child. Device plane kept distinct from the existing data-plane storage constellation. Added the caveat that the NET/WEB/MESH standard definitions are NOT Logan-hard-locked — bindings here are provisional observed readings, not canon.
