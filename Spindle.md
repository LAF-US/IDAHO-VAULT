<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Spindle | Topology Scout | investigate hub-spoke-pipe

I now have enough to write a complete, well-grounded report. Here is the full picture from the vault.

---

## Spindle Report: Hub-Spoke-Pipe in IDAHO-VAULT

### Term Status

The hyphenated compound "hub-spoke-pipe" does not appear as a single coined term anywhere in the vault. However, the three component words are used throughout as a vocabulary cluster describing agent-communication topology. The vault does not define them in a single glossary entry; their meaning is assembled across several files.

---

### What the Vault Actually Says

**File: `.claude/file-history/…/120a4d0e4e539fd5@v*` (dotfolder architecture notes, multiple versions)**

> "`!/` becomes the shared commons all agents draw from — hub-and-spoke."

This is the vault's tightest structural use of "hub-and-spoke" as a topology name. The `!/` directory is the hub — a shared commons that every agent reads from. Each agent's own dotfolder is a spoke. The model is radial: agents do not communicate with each other; they all draw from one center.

**File: (search fragment from an un-named swarm design document — surfaced in the "spoke" search)**

> "The objective is to build a deterministic, event-driven **hub-and-spoke architecture where agents do not talk to each other**, but instead pass tightly scoped, stateless payloads. Linear will serve as the sole Dispatcher, translating human intent into mechanical webhook triggers."

This is the vault's clearest anti-mesh policy statement. Agents speaking directly to each other is the failure mode. The hub (Linear / Logan's intent) issues triggers; agents execute and return output via GitHub PRs. There is no agent-to-agent channel.

**File: `OPENCLAW-WITNESS-REPORT-2026-05-25.md`**

> "**Hub-and-spoke gateway:** The messaging gateway uses a WebSocket hub — all platforms connect as spokes to a single in-process hub. Reconnection logic, message buffering, and platform state are managed centrally in the hub process."

This is the vault's most explicit per-component definition: in OpenClaw's architecture, "hub" = the in-process WebSocket coordinator; "spokes" = all external platform connections (Telegram, Discord, etc.). The hub owns reconnection, buffering, and state. The spokes are dumb connectors.

**File: `SPEC-CONNECTOR-HUB-2026-04-09.md`**

> "**V1 core hub:** GitHub only … **GitHub** = execution, transport, and coordination primacy"

Here "hub" means GitHub as the single authoritative transport layer. "Pipe" does not appear in this file; the vault uses "transport" where engineers might say "pipe." GitHub is the pipe that carries execution state.

**File: `0401 - The Concierge.md`** (allegory layer)

> "The Twin ♂️ (Conduit): The routing, the Nest Bridge, the very pathway that transmits the signal from the physical world into the digital ether."
> "The Twin ♂️ (Conduit) is ready to pipe it into the affable-bastion GCP project."

In the vault's literary register, "pipe" appears as a verb (to pipe data into a destination) and as the "Conduit" character — the agent role responsible for transmission/routing, as opposed to the "Formula" (logic/calculation) or "Ledger" (durable record). This is the vault's allegorical encoding of the transport layer.

**File: `!-AGENTS.md`**

> "`!/SIGNALS/` is the durable async bus for agent-to-agent signaling"

This is the one concession to peer-signaling: a file-based async bus in the `!/SIGNALS/` directory. Even here, agents do not talk directly — they write signals into a shared directory (the hub reads them).

---

### Summary of Definitions as the Vault States Them

| Term | Vault meaning |
|---|---|
| **Hub** | The central coordinator — `!/` directory as shared commons; GitHub as execution transport authority; Linear as dispatcher; WebSocket gateway in OpenClaw. Always singular, always where state is authoritative. |
| **Spoke** | An agent, a platform connector, or a dotfolder — connected to the hub but not to each other. |
| **Pipe** | Used as a verb ("pipe it into GCP") and personified as "The Conduit" (the routing/transmission role). Not a distinct topology class; it describes the channel between hub and destination. |

### Rules and Distinctions the Vault Draws

1. Agents do not talk to each other. All communication passes through the hub (Linear / GitHub / `!/`).
2. Mesh is explicitly named as the alternative — and rejected for the core operating model (though Phase 4 notes envision optional mesh sync via Tailscale/WireGuard for multi-node resilience).
3. The human (Logan) sits at the hub conceptually: Logan's approval is the final merge gate on every agent-generated PR. The hub is not autonomous; it is where human intent enters and where human authorization is required.
4. "Pipe" / "transport" describes GitHub's role (execution transport) — PRs and Actions are the conduit, not chat or direct agent APIs.
5. The `!/SIGNALS/` directory is the sole async bus for agent-to-agent signaling — file-drop rather than direct channel.

### Connection to Agent-Communication Topology

The vault's model is unambiguous: hub-and-spoke over mesh. The stated reason is eliminating "prompt drift and rogue repository edits" caused by agents rebuilding context from each other across sessions. The hub enforces stateless, scoped payloads. "Pipe" in the vault names the transport medium (GitHub PRs/webhooks) or the Conduit character, not a separate topology type.

---

### Confidence and Gaps

Confidence: **High** that the vault does not use "hub-spoke-pipe" as a coined single term, and **high** that the above is the accurate cluster meaning from the vault's own text.

Gap: The exact file path for the SWARM-COMMUNICATION REBUILD section (the clearest hub-and-spoke definition) was surfaced from a search result fragment in a cached paste file, not a primary named document. The primary design notes may exist under a different path (a `!-SWARM` or `!-ARCHITECTURE` file) that was not returned at the top of search results. The vault's treatment is distributed across many files rather than consolidated in a single architecture spec.
