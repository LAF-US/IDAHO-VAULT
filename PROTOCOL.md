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

###### [["The world is quiet here."]]
