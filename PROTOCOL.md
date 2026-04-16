---
authority: LOGAN
related:
  - -LAF
  - '2026-03-25'
  - '2026-04-02'
  - AGENTS
  - BRIEF-LAF-3-2026-03-25
  - CONSTITUTION
  - DECISIONS
  - FLAG
  - LAF
  - LEVELSET
  - MCP
  - The world is quiet here
  - VAULT-METADATA-STANDARD
  - VAULT-ZONES
  - VML
  - agent
  - coordination
  - node
  - persona
date created: Sunday, April 12th 2026, 4:00:33 am
date modified: Sunday, April 12th 2026, 5:55:08 pm
---

# PROTOCOL.md — Operational Vocabulary

## Status: Draft
## Authority: Loganic Swarm

This document defines the operational semantics for multi-instance coordination within the agentic swarm. It provides the discrete command grammar used to manage file state, task handoffs, and resource allocation.

---

## 🏗️ Core Semantics

| Command | Intent | Expected Outcome |
|---|---|---|
| **HYDRATE** | Resolve stubs or external references into local context | Metadata/content populated from source |
| **INGEST** | Move external data into the vault's structured layers | File created in SOURCES or TOPICS |
| **FLAG** | Mark a file or task for human review/high-risk audit | Entry added to DOCKET; logic execution paused |
| **HANDOFF** | Package current context for a second agent (cross-persona) | LEVELSET/HANDOFF artifact committed to `!/!/` |
| **TERMINATE** | Safely end an agent session and clean up local scratch | Ephemeral branch purged; session summary in vault |

---

## 🛠️ Tooling Integration (MCP)

The protocol supports the **Model Context Protocol (MCP)** for transport-only integrations. Vault-native governance files remain the canonical source of truth for agent behavior.

### MCP Coordination rules:
1. **Transport-only**: Use MCP for fetching/sending data; do not delegate governance to external MCP hosts.
2. **Logged actions**: All MCP-initiated writes must be recorded in the vault’s audit trail (`!/!/` artifacts).

---

## ⚖️ Governance Anchors

- **CONSTITUTION**: Defines the "why" and "who"
- **AGENTS**: Defines the "what" (capability tiers)
- **DECISIONS**: Durable record of confirmed system changes
- **VAULT-ZONES**: Spatial write-authority boundaries

---

## 📝 Document Classes (VML)

See `VAULT-METADATA-STANDARD.md` for full definitions.

| Class | Role | Example |
|---|---|---|
| `brief` | Scoped design/intent note | `BRIEF-LAF-3-2026-03-25.md` |
| `handoff` | Session context bridge | `HANDOFF-CODEX-REPAIR-2026-04-02.md` |
| `neuron` | State-tracking node | `100.md` (Current State) |
| `protocol` | System behavior rule | `PROTOCOL.md` (This file) |

---

## 🧹 Exclamation-Space Routing

| Space | Posture | contents |
|---|---|---|
| `!` | Stable | Canonical governance |
| `!/!` | Workbench | Context packages |
| `!/!/!` | Hot | Live board (DOCKET) |

---

## 🤝 THE TRIUNE HANDSHAKE (Clarity)

The Handshake is the formal transition to **AFK Status**. It requires the **Three-in-One** to align their internal state with the **Serena Tapestry**.

- **THE KING (Claude)**: Binds the current git state and ensures no structural leaks remain in the index.
- **THE CONCIERGE (Gemini; historical alias: Antigravity)**: Narrates the current session's "Closing Argument" in the ledger.
- **THE LEXICOGRAPHER (Codex)**: Cleans the `!/!/` workbench and ensures machinery tools are in a stable background state.

## 📱 AFK PAGING (Mobile Escalation)

When the Swarm is operating AFK and encounters a **Level 1 Blocker** (e.g., Auth failure, critical logic conflict, or user-defined "Stop" condition), it must:

1. **Pause execution** of the blocked branch.
2. **Flag** the issue in the **[ 📱 MOBILE PAGE ]** section of the `DOCKET.md`.
3. **Commit** the state with the prefix `page/` for visibility.
4. **Wait** for the "Meatsack-at-Keys" to return.

---

###### [["The world is quiet here."]]
