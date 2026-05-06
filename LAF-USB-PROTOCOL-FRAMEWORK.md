---
title: "LAF-USB Universal Sync Bus Protocol Framework"
status: proposed
type: framework
authority: LOGAN
date: 2026-05-06
related:
- LAF-USB
- Universal Sync Bus
- LAF-USB-FIVE-CORES-MIGRATION
- Git
- Git LFS
- GitHub
- gcloud
- rclone
- rsync
- SBP
- NETWEB
- MESHWEB
- MESHNET
- VAULT-MEDIA-STORAGE
- DISTRIBUTED-HASH-LEDGER
- SPEC-CONNECTOR-HUB-2026-04-09
---

# LAF-USB Universal Sync Bus Protocol Framework

This is a high-level framework for the Universal Sync Bus. It is not an active
automation contract and does not reprovision the disabled Project Courier path.

## LAF-USB Naming Boundary

`LAF-USB` already has live meaning in the vault. The current migration context
is `!-LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md`, where LAF-USB names both a
Five Cores migration current and part of the GitHub team topology.

The Universal Sync Bus is therefore a subordinate capability inside the broader
LAF-USB migration, not a replacement definition for LAF-USB.

## Purpose

The Universal Sync Bus is the proposed connector-core transport framework for
moving, mirroring, caching, verifying, and restoring vault objects across Git,
GitHub, local filesystems, cloud remotes, and cold storage.

The core idea is simple: Git tracks the map and the small record; governed
carrier tools move the heavy payloads.

## Architecture Layers

| Layer | Role | Authority |
| --- | --- | --- |
| Authority | Logan, Constitution, Five Cores doctrine, connector posture | Human and governance surfaces |
| Index | Git, Git LFS, Markdown/YAML manifests, object references | Vault and GitHub record |
| Carrier | `rclone`, `rsync`, `gcloud storage rsync` | Transfer tools only |
| Awareness | SBP pheromone trails, liveness, alerts, coordination pressure | Observation only |

Carrier tools do not decide what belongs in the record. SBP trails do not
authorize transfers. GitHub remains the execution and transport authority for
this repository under the connector posture in `SPEC-CONNECTOR-HUB-2026-04-09.md`.

## Portability Standards

USB artifacts must satisfy the portability trifecta.

| Standard | Scope | USB requirement |
| --- | --- | --- |
| NETWEB | Filesystem portability | Use safe filenames, no Windows reserved names, no case-only path distinctions, repo-relative forward-slash paths in docs and manifests |
| MESHWEB | Runtime portability | Every carrier lane declares whether it is available in `local`, `cloud`, `ci`, or unavailable |
| MESHNET | Sync topology portability | Every storage or mirror lane declares a topology role: hot, cold, immutable, local cache, staging mirror, or disabled |

No USB manifest should use absolute local-only paths as durable identifiers.
Local paths may appear only as temporary operator notes, and should be replaced
with repo-relative paths or storage keys before the reference becomes durable.

## Connector Posture

| Surface | USB role | Authority posture |
| --- | --- | --- |
| GitHub | Execution, workflows, transport state, PR/issue coordination | Core authority for repo execution |
| Git | Durable local index and history | Versioned record |
| Linear | Planning and execution mirror | Not authoritative |
| Slack | Paging and breadcrumbs | Not durable |
| Google Drive, Dropbox, OneDrive, Box | Hot provider mesh | Storage carrier only |
| Google Cloud Storage | Cold/archive lane | Storage carrier only |
| Internet Archive | Immutable/public ledger lane | Storage carrier only |

Use of a storage provider does not promote that provider into governance
authority.

## Carrier Lanes

| Lane | Tool | Runtime scope | Topology role | Primary use | Not for |
| --- | --- | --- | --- | --- | --- |
| Index | Git + GitHub | local, cloud, ci | durable index | Notes, manifests, scripts, small files, LFS pointers | Raw objects beyond GitHub/LFS limits |
| Supported large objects | Git LFS | local, cloud, ci | durable object pointer | Large source files below the active LFS ceiling | Files over the LFS ceiling |
| Provider mesh | rclone | local active; cloud/ci only with injected config | hot/cold/immutable provider mesh | Multi-cloud copy, sync, check, provider abstraction | Committed config or token storage |
| Filesystem mirror | rsync | local only unless explicitly provisioned elsewhere | local cache or staging mirror | Disk/NAS/SSH delta transfer and staging mirrors | Cloud identity or governance policy |
| GCS-native archive | `gcloud storage rsync` | local and ci only after credential reprovisioning | cold archive | GCS bucket sync, IAM, lifecycle policy lanes | Universal protocol authority |
| Project Courier | `.github/scripts/vault-courier-sync.sh` | unavailable | disabled | Historical scaffold only | Any live sync |

`vault-courier-sync.sh` is currently `DISABLED` because its credential leaked
and has not been reprovisioned.

## USB Phases

| Phase | Meaning | Typical carriers |
| --- | --- | --- |
| DISCOVER | Inspect repo, manifests, local payloads, and remote availability | Git, rclone listing, rsync dry-run, gcloud dry-run |
| PLAN | Choose target lane, storage key, verification method, and approval path | Markdown/YAML manifest |
| STAGE | Prepare a non-destructive transfer plan | rclone dry-run, rsync dry-run, gcloud dry-run |
| TRANSFER | Move or mirror payload after approval | rclone, rsync, gcloud |
| VERIFY | Reconcile object presence, size, checksum, and manifest state | rclone check, local hash, gcloud metadata |
| REPORT | Commit durable result, failure, exception, or human-readable note | Markdown, JSON/YAML manifest, GitHub issue/PR |
| RETIRE | Deprecate stale lanes, pointers, credentials, or mirrors | Git note plus approved cleanup |

Delete-capable sync is prohibited unless it has an explicit staged plan and
Logan approval.

## SBP Mapping

SBP is the Stigmergic Blackboard Protocol. Its terms are pheromone-field
loanterms, not USB-native transfer authority.

| SBP term | SBP meaning | USB interpretation |
| --- | --- | --- |
| SNIFF | Read environmental pheromone state | Observe sync status, risk, liveness, or pending transfer pressure |
| EMIT | Deposit a pheromone | Publish a coordination signal about a USB phase or result |
| REGISTER_SCENT | Declare a trigger condition | Watch for state such as failed verification or missing manifest |
| TRIGGER | Blackboard activates an agent | Notify or page for human/agent attention |
| DEREGISTER | Remove a trigger | Retire a watch condition |

SBP may observe USB events, but it must not authorize a credentialed transfer
or substitute for manifest truth.

## Object Reference Shape

The exact schema is TBD, but an LAF-USB reference should be able to answer:

- what object is being referenced
- why it is outside ordinary Git
- which carrier lane applies
- what topology role the destination serves
- where the durable storage key lives
- how integrity is verified
- whether the object is public, private, sensitive, draft, or publishable
- what human note, episode, meeting, source, or package gives it context

Example conceptual shape:

```yaml
laf_usb_objects:
  - id: laf-usb:IDAHO-VAULT:2026:XD4_6602
    original_filename: XD4_6602.MXF
    git_policy: external-over-lfs-limit
    carrier_lane: rclone
    topology_role: cold
    runtime_scope: local
    storage_key: media-archive:IDAHO-VAULT/2026/XD4_6602.MXF
    size_bytes: null
    checksum:
      algorithm: sha256
      value: null
    verification_state: pending
    sensitivity: publishable
    related: []
```

Manifests may contain storage keys, sizes, checksums, lane state, and topology
roles. They must not contain tokens, signed URLs, credential configs, or local
absolute paths as durable references.

## Lane States

| State | Meaning |
| --- | --- |
| PROPOSED | Doctrine or design only; no execution promise |
| STAGED | Configured enough for dry-run planning |
| ACTIVE | Credentialed, tested, documented, and approved for use |
| DEGRADED | Works partially, with known limitations |
| DISABLED | Must not be invoked until reapproved |
| RETIRED | Historical only |

## Open Design Questions

- What is the canonical manifest filename and location?
- Should object references live beside source notes, in a central manifest, or
  both?
- Which remotes are hot, cold, immutable, public, or private?
- What checksum algorithm is mandatory for large external payloads?
- What is the approval threshold for delete-capable sync?
- How should 1Password/op provide credentials without committing config state?
- Which provider is authoritative during restore when mirrors disagree?
- Should MESHNET become a standalone doctrine file, or remain defined inside
  this USB framework until it stabilizes?
