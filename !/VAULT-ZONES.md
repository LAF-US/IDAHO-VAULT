---
tags:
  - administration/governance
updated: 2026-03-25
status: draft
source: commit
---

# VAULT-ZONES — Governance Zone Definitions

This document partitions the vault into three governance zones by write-authority requirements. It formalizes the boundaries that already exist mechanically in `classify_paths.py` (two-tier risk classification) and `CODEOWNERS` (path-based review gates).

---

## Zone Definitions

| Zone | Paths | Write Authority | PR Merge Authority | Risk Tier |
|------|-------|----------------|-------------------|-----------|
| **Constitutional** | `!/` (all nested), root governance files (`CONSTITUTION.md`, `DECISIONS.md`, `AGENTS.md`, `PROTOCOL.md`, `VAULT-CONVENTIONS.md`, `VAULT-ZONES.md`, `CLAUDE.md`, `GEMINI.md`, `Ethics.md`, `Logan.md`) | Logan only. Agents propose via PR — no standing write window. | Logan only | High |
| **Operational** | `.github/workflows/`, `.github/scripts/`, `.github/actions/`, `.github/swarm/`, `!/swarm/` | Agents propose via PR. Logan reviews and merges. | Logan only | High |
| **Data** | `SOURCES/`, `TOPICS/`, `PEOPLE/`, `PLACES/`, `ORGANIZATIONS/`, `GOVERNMENTS/`, `ATTACHMENTS/`, `INBOX/`, `X LABELER/`, all other vault `.md` content | Agent-assignable via GitHub Issues. All writes via PR. | Logan (auto-merge eligible for low-risk per `auto-pr.yml`) | Low |

---

## Zone Details

### Constitutional Zone

Covers `!/` and its nested structure (`!/!/`, DOCKET, LEVELSET, DECISIONS copy, agent routing contexts), plus root-level governance `.md` files.

**Key constraint (CONSTITUTION.md Section V):** "Nothing modifies or destructively touches anything in `!/` without Logan's guiding hand."

**Access model:** No agent has a standing write window to Constitutional Zone files. All changes — including from CODE AUTHORITY — require:
1. A GitHub Issue or explicit Logan directive scoping the task
2. Work on a feature branch
3. PR submission for Logan's review
4. Logan's merge approval

This zone is protected by `CODEOWNERS` (`/!/` requires `@loganfinney27` review). Agent instruction files (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`) are Constitutional because they define agent behavior constraints.

### Operational Zone

Covers `.github/` subtrees and `!/swarm/` tooling. Both CODE AUTHORITY and Copilot can propose modifications to `.github/` per [[AGENTS]] Section 5 overlap rules.

**Access model:** Agents with GitHub repo access can submit PRs. Logan reviews and merges. No auto-merge — all Operational Zone changes are high-risk.

### Data Zone

Bulk vault content (3400+ files). Already classified as low-risk in `classify_paths.py`. Agents with write capability can be assigned Data Zone tasks via GitHub Issues with agent labels.

**Access model:** Auto-merge eligible per `auto-pr.yml` when `classify_paths.py` returns `low` tier. Logan can override.

---


## Exclamation-Space Routing Grammar

The `!` path family is a nested routing system with three distinct roles:

| Space | Operational role | What belongs here | Durability expectation |
|---|---|---|---|
| `!` | **Constitutional control plane** | Active governance files and canonical system rules (`CONSTITUTION`, `PROTOCOL`, `AGENTS`, `DECISIONS`, `VAULT-ZONES`, `VAULT-CONVENTIONS`, active protocol references) | Stable + durable (authoritative record) |
| `!/!` | **Routing workbench** | Time-scoped handoffs, levelsets, context packets, branch triage notes, protocol drafts, and in-flight coordination artifacts | Semi-stable: durable archive, but not canonical policy |
| `!/!/!` | **Live operations board** | The Courtroom and session-level coordination surface (`DOCKET.md`, immediate queue state, short operational status files) | Ephemeral exchange surface with periodic promotion |

### Stable routing vs ephemeral exchange

**Stable routing** means information is preserved as retrievable instruction or record-of-decision. In practice, this includes:
- governance decisions,
- durable operating rules,
- completed handoff bundles that future agents must be able to re-read.

**Ephemeral exchange** means transient coordination traffic that is useful now but not necessarily as-is later. In practice, this includes:
- session chatter,
- in-the-moment status signals,
- tentative notes before validation.

Rule of thumb:
- If another agent would need it later to avoid rework or ambiguity, route it to a stable file (`!` or archival content in `!/!`).
- If it only helps real-time coordination, keep it in `!/!/!` until resolved, then either discard or promote.

### Movement rules between `!` spaces

1. **Capture at point of action (`!/!/!`)**
   - Log active work state in the Courtroom/DOCKET layer while work is in progress.

2. **Package when context matures (`!/!`)**
   - When a thread becomes transferable (handoff, levelset, context bundle), move it into `!/!` as a dated artifact.
   - Use explicit filenames (`HANDOFF-*`, `LEVELSET-*`, `CONTEXT-*`, `SESSION-*`) so routing intent is obvious.

3. **Promote when policy crystallizes (`!`)**
   - If the artifact changes system behavior, agent boundaries, or durable protocol, extract the final rule into canonical governance files in `!`.
   - Canonical files should summarize decisions; `!/!` retains historical detail.

4. **Do not bypass promotion gates**
   - Decisions are not considered authoritative until represented in canonical governance docs under `!` and merged through normal PR review.

5. **Preserve traceability**
   - Canonical updates should reference the originating `!/!` artifact(s) so auditors can trace decision lineage.

## No Standing Write Windows

Per Logan's directive (2026-03-24): no agent — including CODE AUTHORITY — maintains a permanent open write window to any zone. All agent writes are:

- **Task-scoped:** tied to a specific GitHub Issue or explicit Logan directive
- **Branch-isolated:** work happens on feature branches, never direct to `main`
- **PR-gated:** all changes submitted as pull requests for review
- **Logan-merged:** Logan holds sole merge authority (with auto-merge exception for low-risk Data Zone changes)

This means CODE AUTHORITY's "Direct write" capability tier (per [[AGENTS]]) describes *mechanical ability*, not *standing authorization*. Each task requires fresh authorization.

---

## Exclamation-Space Routing Grammar

| Space | Purpose | Typical contents | Routing posture |
|-------|---------|------------------|-----------------|
| `!` | Constitutional anchor and pointer to the governance stack | `CONSTITUTION.md`, `DECISIONS.md`, `AGENTS.md`, `PROTOCOL.md`, `VAULT-CONVENTIONS.md`, `VAULT-ZONES.md`, `CLAUDE.md`, `GEMINI.md`, `Ethics.md`, `Logan.md`, `!/README.md` | **Stable only.** No scratch notes; use for canonical governance and orientation. |
| `!/!` | Routing spine for structured coordination and context packages | `LEVELSET-*`, `HANDOFF-*`, DOCKET/READY-STATE bundles, branch triage, MCP discovery, context passovers | **Stable routing.** Updates can churn but remain in-versioned artifacts. Promote final decisions to `!/DECISIONS.md` or other constitutional files. |
| `!/!/!` (`"The world is quiet here"`) | Live courtroom for active swarm coordination | `DOCKET.md`, live status updates, short-term instructions for in-flight sessions | **Hot but stable.** Use for real-time updates; roll durable outcomes into `!/!/` (handoffs/LEVELSET) or `!/` (DECISIONS/PROTOCOL) once settled. |

### Stable routing vs. ephemeral exchange

- **Stable routing** lives in the `!` family paths above. Anything written here is treated as canonical and must be committed.
- **Ephemeral exchange** happens in chats, Slack, GitHub comments, or temporary scratch files. These channels are coordination-only — not records of decision.

### Movement rules for agents

1. Capture outcomes from ephemeral channels into `!/!/!` (DOCKET) when work is active, or directly into `!/!/` handoffs/LEVELSET packages when handing over.
2. When a decision is confirmed, promote it to the appropriate constitutional file in `!/` (e.g., `DECISIONS.md`, `PROTOCOL.md`, `VAULT-CONVENTIONS.md`).
3. Do not park scratch content in `!` or `!/!`; either discard ephemeral notes or convert them into structured handoffs before committing.

---

## Alignment with Existing Systems

| System | What it does | Relationship to zones |
|--------|-------------|----------------------|
| `classify_paths.py` | Returns `high` or `low` risk tier per file path | Implements the Constitutional+Operational = high, Data = low split |
| `CODEOWNERS` | Requires `@loganfinney27` review for gated paths | Gates Constitutional Zone (`!/`) and Operational Zone (`.github/`) |
| `auto-pr.yml` | Auto-creates PRs from `claude/*` branches; auto-merges low-risk | Data Zone changes eligible for auto-merge |
| `branch-cleanup.yml` | Deletes merged `claude/*` branches | Applies to all zones equally |

**Note:** `classify_paths.py` still references old `!ADMIN/` paths in `HIGH_RISK_EXACT`. Follow-up recommended to update these to `!/` paths.

---

## Cross-References

- [[CONSTITUTION]] — Identity, constraints, working rules
- [[AGENTS]] — Agent registry, capability tiers, boundary rules
- [[DECISIONS]] — Confirmed Logan-approved decisions
- [[PROTOCOL]] — Operational vocabulary

---

## DOCUMENT METADATA

- **Created:** 2026-03-24
- **Author:** PERMANENT: AUTHORITY: CODE (draft)
- **Status:** Draft — awaiting [[LOGAN]]'s review
- **Authority:** [[LOGAN]]'s discretion
