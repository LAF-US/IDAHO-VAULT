---
title: "Repo Payload Audit"
updated: 2026-04-03
status: active
authority: "[[LOGAN]]"
tags:
  - administration/repo
  - administration/git
  - administration/audit
  - swarm
---

# REPO PAYLOAD AUDIT - 2026-04-03

This brief records the first machine-readable classification pass for repo
slimming work in `IDAHO-VAULT`.

## Current Signal

- packed git history: `362.28 MiB`
- classified payload candidates: `122`
- linked-from-notes candidates: `88`

### Recommended Actions

- `purge_as_trash`: `2`
- `move_to_annex`: `45`
- `manual_review`: `75`

## Highest-Weight Immediate Trash Candidates

- `.codex/tmp/Antigravity-full.exe`
- `.codex/tmp/Antigravity.exe`

## Annex-Leaning Payloads

The audit currently leans annex-ward for note-linked or reference-style media,
including large images, PDFs, audio, and similar evidence/reference assets that
do not need to remain in the root control-plane repo forever.

## Manual Review Pool

The largest manual-review cluster is Obsidian plugin runtime payloads under
`.obsidian/plugins/`. Because Human-Obsidian is the primary interface, these
should not be treated as disposable trash. They need a later Logan review to
decide which belong in root history, which should remain local-only, and which
can leave GitHub while staying on machine.

## Files

- Machine-readable inventory: `!/REPO-PAYLOAD-AUDIT-2026-04-03.json`
- Standing protocol: `!/REPO-SLIMMING-PROTOCOL.md`

## Standing Constraint

This is classification and guardrail work only. History rewrite, annex move,
and force-push protocol remain a later deliberate phase.
