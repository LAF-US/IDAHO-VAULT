---
date: 2026-04-22
authority: LOGAN
type: research
related:
- MCP
- multi-agent
- coordination
- protocol
- SBP
---

# SBP — Stigmergic Blackboard Protocol

**Source:** [github.com/AdviceNXT/sbp](https://github.com/AdviceNXT/sbp)
**Status:** v0.1.0-draft (Feb 2026)
**License:** MIT (code), CC BY 4.0 (spec)

---

## The Problem

Most multi-agent systems use orchestrators or message queues. These create:
- Bottlenecks
- Single points of failure
- Brittle coupling between agents

Every new agent means more glue code.

---

## The Solution: Stigmergy

**Stigmergy** is how ants coordinate: they leave pheromone trails in the environment. Other ants sense the trails and react. No meetings. No direct messages. No coordinator. The colony self-organizes.

**SBP brings this to software.**

---

## Core Concepts

### Pheromones

Signals deposited by agents with:
- **Intensity** (0.0–1.0): Signal strength
- **Decay**: Signals fade over time (stale signals evaporate)
- **Payload**: Optional data

### Trails

Namespaces that organize pheromones:
- `market.signals`
- `pipeline.stage1`
- `vault.agent-activity`

### Scent Conditions

Threshold rules. Agent declares: "Wake me when `volatility ≥ 0.7`" — then goes dormant until the environment triggers it.

### Merge Strategies

What happens when you emit a pheromone that already exists:
- **Reinforce**: Add intensities
- **Replace**: New overwrites old
- **Max**: Take the higher
- **Add**: Sum intensities

---

## Five Operations

| Op | Direction | Purpose |
|----|-----------|---------|
| **EMIT** | Agent → Blackboard | Deposit pheromone |
| **SNIFF** | Agent → Blackboard | Read environment state |
| **REGISTER_SCENT** | Agent → Blackboard | Declare trigger condition |
| **TRIGGER** | Blackboard → Agent | Activate dormant agent |
| **DEREGISTER** | Agent → Blackboard | Remove trigger |

---

## SBP vs MCP

| | MCP | SBP |
|---|-----|-----|
| **What it solves** | How an agent uses tools | How agents coordinate together |
| **Interaction** | Direct: "agent calls tool" | Indirect: "agent senses environment" |
| **Coupling** | Agent knows the tool | Agents don't know each other |
| **Pattern** | Request → Response | Emit → Sense → React |
| **State** | Sessions | Shared environmental state |

**They're complementary.** Use MCP for "what can I do?" Use SBP for "what's happening around me?"

---

## Design Principles

1. **Stale-by-Default** — All signals decay. Unreinforced data evaporates automatically.
2. **Sense, Don't Poll** — Agents declare interest patterns; the environment triggers them.
3. **Stateless Agents** — Agents are dormant by default. No persistent state between activations.
4. **Intensity Over Boolean** — Signals have continuous strength, enabling nuanced responses.

---

## SDKs

### Python
```bash
pip install sbp-client
```

### Node.js
```bash
npm install @advicenxt/sbp-server  # Server
npm install @advicenxt/sbp-client   # Client
```

### Local Mode (No Server)
```python
from sbp import SbpClient
client = SbpClient(local=True)
client.emit("local.test", "signal", 0.9)
```

---

## Use Cases

1. **Autonomous Research Teams** — MCP research agents emit findings; synthesis agent wakes when threshold reached
2. **Self-Healing Infrastructure** — Monitoring agents trigger remediation; transient blips decay harmlessly
3. **Financial Signal Processing** — Composite conditions (volatility AND orders) trigger responses
4. **Content Moderation Pipeline** — Staged pipeline from classifier → review → ban
5. **Multi-Agent Task Coordination** — Pipeline self-assembles from threshold conditions

---

## IDAHO-VAULT Applications

### Potential Uses

| Trail | Signal | Trigger |
|-------|--------|---------|
| `vault.daily.ingest` | Daily note created | Archive agent activates |
| `vault.security.sweep` | Credential detected | Purge agent triggers |
| `vault.agent.active` | Agent working | Activity monitor logs |
| `vault.branch.orchard` | Branch created | Arborscape assessment |
| `vault.dependabot.alert` | Vulnerability found | Fix agent activates |

### Comparison with Current Architecture

**Current (Linear/GitHub):**
- Centralized task tracking
- Explicit assignment
- Single point of coordination

**SBP-Enhanced:**
- Environmental awareness
- Emergent coordination
- Graceful degradation (agent dies, pheromones decay, others adapt)

---

## Status

Active protocol. v0.1.0 released Feb 2026. Spec is RFC 2119 compliant. Active development.

---

###### [["The world is quiet here."]]
###### [ Maiden : Mother : Crone ]