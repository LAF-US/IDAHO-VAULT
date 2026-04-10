---
title: SPEC - Connector Hub and Connector Maze Census
updated: 2026-04-09
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

# SPEC - Connector Hub and Connector Maze Census

## Summary

This spec formalizes the connector model for IDAHO-VAULT in two phases:

- **V1 core hub:** GitHub + Linear + Slack
- **V2 maze census:** classify every available connector without promoting new authorities

The governing model does not change:

- **Vault** = durable record and doctrine
- **GitHub** = execution and transport
- **Linear** = execution state
- **Slack** = ephemeral paging and breadcrumbs

All other connectors remain read-first unless Logan explicitly promotes them later.

---

## V1 Core Hub

### Canonical roles

| Connector | Category | Write Mode | Canonical Role | Authoritative For |
|---|---|---|---|---|
| GitHub | `core` | `gated-write` | Issues, PRs, workflows, automation output, execution transport | execution transport |
| Linear | `core` | `gated-write` | Owners, status, planning, SWARM execution tracking | execution state |
| Slack | `core` | `notification-write` | Tertiary paging, quick coordination, breadcrumbs | nothing durable |

### Existing implementation anchors

- `.github/scripts/linear_gateway.py` remains the controlled Linear choke point
- `.github/scripts/linear_pr_sync.py` remains the GitHub-to-Linear lifecycle bridge
- Slack workflow reporting remains breadcrumb-only

### Core operating rule

1. A GitHub event, workflow event, issue change, or PR change occurs.
2. Linear mirrors owner, status, and planning state when appropriate.
3. Slack may notify or carry a breadcrumb.
4. Any durable outcome must be promoted into the vault and/or execution systems.

Slack never becomes a system of record through speed or repetition alone.

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
