---
title: "MacBook Ground-Zero Observation"
date: 2026-05-15
status: active-observation
authority: LOGAN
type: addendum
related:
  - LOCAL-VAULT-REUNIFICATION-2026-05-08
  - VAULT-MEDIA-STORAGE
  - EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08
  - CROSS-DRIVE-OVERLAP-REPORT-2026-05-08
  - LAF-USB-PROTOCOL-FRAMEWORK
  - LAF-USB-OBJECT-MANIFEST-2026-05-08
  - "!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14"
  - "!-OPENCLAW-HERMES-STATUS-2026-05-14"
---

# MacBook Ground-Zero Observation - 2026-05-15

This note records the current MacBook surface for the Vault reunification work.
It is an addendum to the existing Vault plans, not a replacement plan, new sync
standard, or new operating model.

The governing direction remains:

- [[LOCAL-VAULT-REUNIFICATION-2026-05-08]]
- [[VAULT-MEDIA-STORAGE]]
- [[EXTERNAL-DRIVE-MIGRATION-PLAN-2026-05-08]]
- [[CROSS-DRIVE-OVERLAP-REPORT-2026-05-08]]
- [[LAF-USB-PROTOCOL-FRAMEWORK]]

Related current-machine support notes:

- [[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]]
- [[!-OPENCLAW-HERMES-STATUS-2026-05-14]]

## Alignment Rule

Do not create another standard to reconcile existing standards.

Use the current lanes already defined by the Vault:

| Existing lane | MacBook interpretation |
| --- | --- |
| Git lane | Durable index for notes, source, small records, manifests, guard scripts, and LFS pointers. |
| External object lane | Payloads too large or operationally heavy for Git/Git LFS. |
| Local storage lane | Role-based drive observations and local staging surfaces. |
| Tooling lane | OpenClaw, Hermes, Ollama, routing, diagnostics, and CI helpers. |

The requested redundancy model maps onto those lanes:

- Storage: Local storage lane plus External object lane.
- Network: LAF-USB carrier lanes such as `rsync`, `rclone`, SSH, or Tailscale when available and approved.
- Git: Git lane as durable index and manifest record.

This does not create a fifth lane.

## MacBook Observations

These are local observations from the MacBook. They are not durable identifiers
and should not be used as global truth without verification.

| Surface | Observation |
| --- | --- |
| Machine | MacBook, host observed as `Logans-MBP.ht.home`. |
| OS | macOS 12.7.6, Darwin `x86_64`. |
| Current Vault path | `/Users/logan/IDAHO-VAULT`. |
| Internal Data volume | About 932 GiB total, 817 GiB used, 96 GiB free. |
| External volume | `/Volumes/storage`, about 4.5 TiB total, 1.5 TiB used, 3.1 TiB free. |
| Time Machine volume | `/Volumes/timemachine`, about 931 GiB total, 849 GiB used, 82 GiB free. |
| Time Machine destination | Local destination named `timemachine`. |

Mac paths may be useful operator notes during discovery. They should not become
durable storage keys in manifests.

## Available Local Tooling

Observed MacBook tools:

- `git`
- `git-lfs`
- `rsync`
- `rclone`
- `op`
- `openclaw`
- `hermes`
- `ollama`
- `tailscale`
- `ssh`
- `python3`
- `uv`
- `node`
- `npm`
- `docker`
- `colima`

Observed carrier context:

- `rclone` remotes include personal and professional Google Drive surfaces,
  Dropbox, and OneDrive.
- Tailscale CLI is installed, but the local daemon was not running during the
  prior check.
- OpenClaw Gateway was observed running locally on port `18789`.
- Hermes Gateway was observed running as a LaunchAgent.

These tools support the Vault. They do not decide Vault contents or storage
policy.

## MacBook and Windows Relationship

The MacBook and Windows machine should be treated as peer observation surfaces.
Neither machine becomes the sole authority.

The prior Git/LFS restructure chokepoint was observed on Windows. Do not project
that state onto the MacBook unless the MacBook revalidates it.

The existing canonical external-drive roles remain:

| Canonical role | Prior Windows observation | Meaning |
| --- | --- | --- |
| Home Desk | `D:`, `LoganF` | Broad home-base archive and staging surface. |
| Work Desk | `E:`, `Expansion` | Professional Idaho/media archive and working surface. |
| Travel Bag | `F:`, `ExternalSSD` | Portable active-work SSD. |

The MacBook external volumes above are candidates for role mapping, not new
canonical roles.

## LAF-USB Boundary

Use [[LAF-USB-PROTOCOL-FRAMEWORK]] as the staged sync framework.

The stable manifest connector is the existing `laf-usb-object-manifest/v1`
shape validated by `.github/scripts/laf_usb_manifest.py`. Do not invent a
separate Mac/Windows peer-ledger schema.

The disabled Project Courier path remains disabled. Do not use
`.github/scripts/vault-courier-sync.sh` as a live sync route unless it is
explicitly reprovisioned and approved later.

## Python Transition Point

Python state is a live transition point.

Observed MacBook state:

- `python3` observed as Python 3.13.7.
- The Vault `.python-version` records 3.13.3.
- `uv run pytest` was blocked by the missing exact 3.13.3 runtime.
- Direct `python3 run_checks.py` reached Python syntax checks, then failed
  because `pytest` was not installed for the active Mac Python.

Do not resolve this by assumption. The Mac/Windows compatibility target should
be chosen explicitly before changing Python runtime policy.

## Tooling Preferences for Routing

Current Logan preferences affecting OpenClaw/Hermes routing:

- Local Ollama models are preferred for simple local calls.
- OpenRouter cloud models are preferred for complex calls.
- Preferred model families: Mistral, Claude, then ChatGPT.
- Disliked local/text model families: Phi, Qwen, Gemma.
- Gemini is not approved as a general text model family here.
- Gemini or Google Cloud project keys may still be appropriate for TTS or
  infrastructure-specific tasks when explicitly scoped that way.

OpenClaw requires a model that can perform tool calls. Avoid `phi3:mini` for
OpenClaw routing.

## Safe Next Work

1. Keep this MacBook note cross-linked to the existing Vault plans.
2. Revalidate MacBook guardrails without rewriting Vault files:
   - large-file guard
   - secret-pattern guard
   - LAF-USB manifest validator
3. Use `rsync` and `rclone` dry-runs before any transfer.
4. Use checksums before any duplicate retirement.
5. Keep OpenClaw/Hermes diagnostics in the Tooling lane.
6. Treat every uncertain state as a live LOGAN point until resolved.

## Guardrails

- No new Vault standard.
- No new lane.
- No new peer-ledger schema.
- No deletion without Logan approval.
- No duplicate retirement without checksum or equivalent evidence.
- No public file-level manifest for personal folders.
- No absolute local-only paths as durable manifest identifiers.
- No credential material, signed URLs, tokens, or local config in durable
  manifests.
