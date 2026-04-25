---
title: SPEC - Connector Hub and Connector Maze Census
updated: 2026-04-10
status: active
authority: LOGAN
type: spec
related:
  - GitHub
  - Linear
  - Slack
  - Gmail
  - Google Calendar
  - Google Drive
  - Box
  - Cloudflare
  - Hugging Face
  - swarm.json
  - LEVELSET
  - VAULT-CONVENTIONS
---

# SPEC - Connector Hub and GitHub Primacy

## Summary

This spec formalizes the connector model for IDAHO-VAULT with GitHub as the sole core authority.

- **V1 core hub:** GitHub only
- **V2 auxiliary:** Linear (execution state), Slack (ephemeral paging)

The governing model:

- **Vault** = durable record and doctrine
- **GitHub** = execution, transport, and coordination primacy
- **Linear** = execution state (mirrored from GitHub)
- **Slack** = tertiary paging and breadcrumbs only

All other connectors remain read-first unless Logan explicitly promotes them later.

---

## V1 Core Hub

### Canonical roles

| Connector | Category | Write Mode | Canonical Role | Authoritative For |
|---|---|---|---|---|
| GitHub | `core` | `gated-write` | Issues, PRs, workflows, automation, execution transport, coordination state | everything — single source of truth |
| Linear | `auxiliary` | `mirrored` | Mirrored from GitHub for human visibility | nothing authoritative |
| Slack | `auxiliary` | `notification-only` | Tertiary paging, breadcrumbs | nothing durable |

### Implementation anchors

- GitHub Issues and PRs are the system of record
- Linear mirrors owner, status, and planning state from GitHub for human convenience
- Slack workflow reporting remains breadcrumb-only

### Core operating rule

1. A GitHub event, issue, or PR change occurs.
2. That change is the authoritative record.
3. Linear and Slack may reflect or notify, but never replace GitHub.

---

## V2 Connector Maze Census

The maze census is a classification pass, not an activation pass.

It records the current shape of:

- GitHub
- Linear
- Slack
- Gmail
- Google Calendar
- Google Drive
- Box
- Cloudflare
- Hugging Face

For each connector, the census must capture:

- current availability in this environment
- current write posture
- doctrinal role
- repo integration points, if any
- auth dependency shape
- category: `core`, `adjunct`, `deferred`, or `experimental`
- allowed promotion path into vault, GitHub, or Linear
- human-only gates

V2 does **not** auto-enable new writes.

---

## Connector Categories

### Core

- GitHub
- Linear
- Slack

### Adjunct

- Gmail
- Google Calendar
- Google Drive
- Box

### Deferred

- Cloudflare
- Hugging Face

---

## Promotion Rules

- If it must be recoverable in six months, promote it into the vault.
- If it needs owner, due date, or active status tracking, promote it into Linear.
- If it is execution transport, workflow state, or PR state, keep it in GitHub and mirror only what matters.
- If it only exists in Slack, it is not durable yet.
- Gmail, Calendar, Drive, and Box may inform work, but they do not become authorities through use alone.
- Cloudflare and Hugging Face are deferred platform lanes until a separate activation plan exists.

---

## Registry Surfaces

- `swarm.json` is the machine-readable connector registry.
- `LEVELSET-CURRENT.md` carries the concise current-state connector maze matrix.
- `VAULT-CONVENTIONS.md` remains the higher doctrine for vault vs GitHub vs Linear vs Slack.

This spec is the human-readable bridge between those surfaces.

## DOCUMENT METADATA

- Created: 2026-04-09
- Last Updated: 2026-04-10
- Status: active
- Authority: LOGAN
