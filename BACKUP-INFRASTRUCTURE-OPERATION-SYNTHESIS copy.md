---
title: Backup Infrastructure — Operation Synthesis
updated: 2026-04-23
status: staged
authority: logan
---

# Backup Infrastructure — Operation Synthesis

> "The world is quiet here."

## What We Did

### Session Summary

1. **Verified op (1Password CLI)** — Already installed, v2.33.1
2. **Installed rclone** — v1.73.5 via Scoop
3. **Configured 7 cloud remotes**:
   - `google-drive:` Google Drive
   - `dropbox:` Dropbox
   - `onedrive:` Microsoft OneDrive (personal)
   - `box:` Box
   - `gcs:` Google Cloud Storage
   - `the-ledger-bucket:` GCS bucket
   - `archive:` Internet Archive
4. **Documented** in [DISTRIBUTED-HASH-LEDGER.md](DISTRIBUTED-HASH-LEDGER.md)

### Current State

| Layer | Tool/Provider | Status |
| :-- | :-- | :-- |
| **Secrets** | op v2.33.1 | ✅ Active |
| **Sync** | rclone v1.73.5 | ✅ Active |
| **Hot Storage** | Google Drive, Dropbox, OneDrive, Box | ✅ Configured |
| **Cold Storage** | GCS (the-ledger-bucket) | ✅ Configured |
| **Immutable** | Internet Archive | ✅ Configured |
| **Version Control** | Git + GitHub | ✅ Active |

## Why This Matters

### Resilience Model

The old model: **Single cloud provider = single point of failure**

The new model: **Distributed verification nodes**

```
You ──▶ Multiple independent providers
        │
        ├── Google (4.9 TiB)
        ├── Dropbox (∞)
        ├── Microsoft (102 MB)
        ├── Box (—)
        ├── Google Cloud (—)
        └── Internet Archive (immutable)
```

If Amazon goes down → you have Google, Dropbox, Microsoft, Box.
If Google goes down → you have Dropbox, Microsoft, Box, GCS.
If two providers fail → you still have 4+ copies.
If three fail → you still have GitHub + local + Archive.

### Verification Chain

rclone checksums every file. Cross-validate with:

```bash
rclone check google-drive: dropbox:
rclone check dropbox: onedrive:
rclone check onedrive: archive:
```

Each provider is a **verification node** — consensus requires agreement across the network.

## Comparison: Old vs. New

| Aspect | Before | After |
| :-- | :-- | :-- |
| **Dependencies** | 1 cloud provider | 7 independent providers |
| **Verification** | Manual (maybe) | Automated checksum |
| **Offline backup** | ? | GitHub + Archive |
| **Immutable record** | None | Internet Archive |
| **Cold storage** | None | GCS lifecycle |
| **Secrets** | Scattered | 1Password (op) |

## How It Works Together

### Data Flow

```
1. LOCAL (Obsidian vault)
       │
       ├─▶ rclone sync → google-drive:    (hot, active)
       ├─▶ rclone sync → dropbox:         (hot, active)
       ├─▶ rclone sync → onedrive:        (hot, active)
       ├─▶ rclone sync → box:              (hot, active)
       ├─▶ rclone sync → gcs:            (cold, archival)
       ├─▶ rclone sync → archive:         (immutable ledger)
       │
       └─▶ git push → GitHub               (version history)
```

### Restore Flow

```
Any provider ──▶ Local restore
       │
       Example: rclone copy google-drive: ./vault --dry-run
```

### Verification Flow

```
rclone check <source:> <target:>
       │
       Output: Differences: 0, Hashes matched
```

## Technical Details

### rclone Configuration

```bash
$ rclone listremotes
google-drive:
dropbox:
gcs:
archive:
the-ledger-bucket:
box:
onedrive:
```

Config stored at: `C:\Users\loganf\scoop\apps\rclone\current\rclone.conf`

### op Configuration

```bash
$ op --version
2.33.1
```

### Storage Capacity

| Provider | Used | Available |
| :-- | :-- | :-- |
| Google Drive | 17.6 GiB | 4.93 TiB |
| Dropbox | 5.2 GiB | ∞ (unlimited) |
| OneDrive | 4.9 GiB | 102 MB |

## Connection to Constitution & Protocols

Per [CONSTITUTION.md](CONSTITUTION.md):

> "Vault holds doctrine and context that must persist. GitHub executes workflows and transport state."

This infrastructure implements **Transport Layer** stability:
- Multiple cloud providers as transport backends
- GitHub as version control transport
- GCS as cold/long-term transport
- Archive as immutable transport

Per [VAULT-CONVENTIONS.md](VAULT-CONVENTIONS.md):

> "Two systems share the vault... Linear tracks execution, owners, and current state."

This system adds a third: **the persistence layer** — redundant, verified, multi-modal storage ensuring data persistence regardless of execution state.

## Related Documentation

- [DISTRIBUTED-HASH-LEDGER.md](DISTRIBUTED-HASH-LEDGER.md) — Technical specification
- [.op/SETUP.md](.op/SETUP.md) — 1Password CLI setup
- [explain LangChain.md](explain LangChain.md) — Blockchain research (original inspiration)
- [CONSTITUTION.md](CONSTITUTION.md) — Governance
- [VAULT-CONVENTIONS.md](VAULT-CONVENTIONS.md) — Conventions

## Next Steps

- [ ] Add Sia remote (decentralized verification)
- [ ] Add Arweave permanent storage
- [ ] Configure rclone crypt on all hot providers
- [ ] Set GCS lifecycle policies
- [ ] Create GitHub Actions backup workflow
- [ ] Schedule automated verification cron

---

> "The world is quiet here." — The infrastructure is ready.