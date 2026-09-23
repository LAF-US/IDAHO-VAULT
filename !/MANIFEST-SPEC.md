---
tags:
  - administration/manifest
updated: 2026-03-25
status: active
source: codex
---

# MANIFEST.json v1 Specification

This file defines the coordination layer for multi-agent operation in IDAHO-VAULT.

## Purpose

`manifest.json` is the shared state record used to prevent:

- duplicate writes
- stale reads
- conflicting outputs

MCP is a transport/interface layer. Coordination remains manifest-driven.

## Canonical Authority Model

- **GitHub repository is canonical state** and automation surface.
- **Obsidian is an interface** (synced view), not source of truth.
- **Filesystem access remains baseline fallback** when MCP is unavailable.

## v1 Top-Level Schema

```json
{
  "manifest_version": "1.0.0",
  "generated_at": "ISO-8601 UTC",
  "authority": {
    "canonical_system": "github",
    "interface_system": "obsidian",
    "fallback_mode": "filesystem"
  },
  "sync": {
    "primary_dataset": "vault",
    "sync_unit": ["file", "manifest_entry"],
    "trigger_model": "event_based_write_read_cycle"
  },
  "mcp": {
    "enabled": false,
    "mode": "transport_only",
    "server": null,
    "notes": "Enable after endpoint + controls validation"
  },
  "locks": [],
  "entries": {}
}
```


## Machine Validation

- Canonical schema file: `manifest.schema.json`
- Automation updater: `.github/scripts/update_manifest.py`
- CI/workflow jobs should validate manifest shape before commit.

## `entries` Object (Per-file Coordination Unit)

Each key is a repository-relative file path. Example:

```json
"entries": {
  "INBOX/ingest-2026-03-25T120501Z.md": {
    "content_hash": "sha256:...",
    "last_writer": "agent:codex",
    "last_write_at": "2026-03-25T12:05:01Z",
    "last_read_at": "2026-03-25T12:05:10Z",
    "status": "active",
    "lock_id": null,
    "version": 3
  }
}
```

## Soft-Lock Protocol (v1)

Soft-locks are advisory but required by protocol.

1. Agent proposes a write target.
2. Agent appends lock record to `locks`:
   - `lock_id`
   - `file_path`
   - `agent_id`
   - `created_at`
   - `expires_at`
   - `state` (`active`/`released`/`expired`)
3. Agent re-reads manifest before write.
4. If another `active` lock exists for the same file path and is not expired:
   - do not write
   - raise `FLAG` with conflict summary
5. On successful write:
   - update `entries[file_path]`
   - mark lock `released`
6. If run aborts, lock expires naturally at `expires_at`.

### Lock TTL

- Default lock TTL: **15 minutes**
- Long-running jobs must renew lock before expiry.

## Conflict Rule

When lock contention exists, no parallel writes to same `file_path` are allowed.

Winner priority:
1. Existing active lock holder
2. If simultaneous creation, lexicographic lowest `lock_id`

All losers must `FLAG` and stop the write attempt.

## MCP Adoption Gate

Set `mcp.enabled` to `true` only after all checks pass:

- Obsidian MCP Tools plugin installed and reachable
- endpoint/tool enumeration captured
- successful MCP write test to controlled path
- permission boundaries verified

Until then, operate in filesystem baseline mode.

## Ingest Filename Rule (Cross-platform)

All ingest artifacts must use:

- `ingest-YYYY-MM-DDTHHMMSSZ.md`

Disallowed:

- any `:` in filename
- local-time ambiguous suffixes

Example valid filename:

- `ingest-2026-03-25T120501Z.md`
