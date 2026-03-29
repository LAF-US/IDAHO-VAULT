---
tags:
  - operations/swarm
  - workflow/mvp
updated: 2026-03-25
status: draft
source: linear/LAF-10
---

# LAF-10 — MVP Swarm Workflow (Vault + Linear + Slack)

## Goal

Define the **smallest repeatable path** from a new request to a reviewed artifact, using:

- **Linear** as the task system of record for execution state
- **Slack** as the live coordination surface (breadcrumbs only)
- **Vault (repo files + PR)** as the durable record and final artifact destination

---

## MVP Flow (6 Steps)

### 1) Task intake (Linear)

**Trigger:** Logan or an agent captures a request and creates/updates a Linear issue in team `Logan Finney`.

**Required minimum fields:**

- Clear title
- Short acceptance criteria (1–3 bullets)
- Owner agent label (`agent:codex`, `agent:claude-code`, etc.)
- Link to repo/workspace if code or docs are expected

**Definition of done for this step:** Issue is assigned, scoped, and has explicit deliverable language.

---

### 2) Agent delegation (Linear → branch)

Assigned agent claims the issue and starts a dedicated branch:

- Branch naming (MVP): `<agent>/<linear-id>-<short-slug>`
- First comment on issue: “Starting work” with planned output file(s)

**Definition of done for this step:** One owner, one branch, one expected artifact path.

---

### 3) Live coordination surface (Slack)

Agent posts short status breadcrumbs in Slack (e.g., `#general`):

- STARTED: issue + branch
- BLOCKED: blocker + owner needed to unblock
- READY FOR REVIEW: PR link

**Hard rule:** Slack is ephemeral. No decision is final until captured in vault files / PR description.

**Definition of done for this step:** Anyone watching Slack can see current status in real time.

---

### 4) Durable record destination (Vault + PR)

Agent produces the artifact in-repo (doc/script/config/code) and opens a PR.

**Minimum PR payload:**

- What changed
- Why it changed
- How to verify
- Linked Linear issue (`LAF-10` style reference)

**Definition of done for this step:** The current best artifact exists in git history and is reviewable as a diff.

---

### 5) Approval gate (human review)

Logan is the approval authority for merge.

**Gate checks (MVP):**

- Scope matches Linear acceptance criteria
- Diff is understandable and bounded
- Any decisions made in Slack are reflected in the PR and/or vault file

**Definition of done for this step:** Logan explicitly approves (PR approval or merge decision).

---

### 6) Completion and closure pattern (PR + Linear + Slack)

After merge:

1. Agent posts merge note in Slack (brief breadcrumb).
2. Agent updates Linear issue to completed/closed with PR link.
3. If governance/operational decision was made, agent records it in the appropriate vault file (e.g., decision log or task doc).

**Definition of done for this step:** Linear is closed, merged artifact is in vault history, and Slack has final breadcrumb.

---

## Minimal Responsibility Map

- **Linear:** intake, ownership, status transitions, closure state
- **Slack:** real-time signals only
- **Vault/GitHub PR:** durable artifact, review, and audit trail
- **Logan:** approval gate and merge authority

---

## MVP Success Criteria

This workflow is considered proven when it runs end-to-end for at least one issue with:

1. Intake captured in Linear
2. Work completed on a dedicated branch
3. At least one live Slack breadcrumb during execution
4. Artifact merged via PR
5. Issue closed with link to merged PR

If all five occur, the swarm path is operational and repeatable.
