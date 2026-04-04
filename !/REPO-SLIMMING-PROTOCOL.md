---
title: "Repo Slimming Protocol"
updated: 2026-04-03
status: active
authority: "[[LOGAN]]"
---

# REPO SLIMMING PROTOCOL

The root GitHub repo is the swarm control plane and canonical text/code layer.
It is not a permanent trash bin for old media, binaries, or tool payloads.

## Root Repo Purpose

The root repo should preferentially hold:

- markdown notes and governance
- Python scripts and local control-plane logic
- swarm registry and manifest state
- small config and lightweight runtime assets

These remain out of scope for purge:

- root notes
- governance docs
- persona dotfolders as identity shims
- Python control scripts
- manifest, swarm, and bootstrap files

## Purge Candidate Families

The current default purge-candidate families are:

- `.codex/tmp/*`
- old archives, executables, and temporary tool payloads
- large legacy screenshots and media
- bulky PDFs and images not required for the root repo's control-plane role
- compiled Obsidian plugin payloads that do not need to live in GitHub history

These are candidates for review, not automatic deletion.

## Archive Boundary

Preserved non-operational binaries and media should move to a separate archive
or annex outside the root repo.

When a payload leaves the root repo, preserve:

- filename
- source path
- purpose or category
- whether it is still linked from vault notes

The annex is the preservation home. The root repo is the control plane.

## Classification Pass

Use the local Python audit tool before any history rewrite:

```powershell
python .github/scripts/audit_repo_payloads.py --json-out ".\!\REPO-PAYLOAD-AUDIT-2026-04-03.json"
```

The audit classifies tracked payloads into:

- `operational_runtime_asset`
- `vault_evidence_reference_asset`
- `plugin_runtime_payload`
- `temp_tool_trash`
- `unknown_review`

It also records:

- LFS status
- note-link samples
- protected or human-interface path flags
- duplicate-content hints

## Rewrite Protocol

History rewrite is a later deliberate phase. It must not be treated as tonight's
cleanup.

The intended initial rewrite scope is:

- `main`
- long-lived shared branches that still matter to swarm operation

The rewrite must preserve:

- text and governance history
- Python control-plane history
- swarm and manifest evolution

The rewrite phase must be paired with:

- a force-push protocol
- a branch recovery protocol
- a clone/worktree recovery note for active agents

## Long-Term Guardrails

Guardrails should stop obvious junk from landing again:

- Office lockfiles
- `.codex/tmp/`
- temporary extraction directories
- local virtualenv payloads
- deployment artifacts and tool caches

Use the staged audit mode for future checks:

```powershell
python .github/scripts/audit_repo_payloads.py --mode staged --enforce
```

## Standing Rule

Human-Obsidian remains the primary interface.
The vault remains the record.
The root repo should stay lean enough to support swarm control logic and future
generated deploy surfaces without becoming a dumping ground for legacy payloads.
