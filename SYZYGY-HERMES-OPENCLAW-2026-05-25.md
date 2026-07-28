---
title: "SYZYGY: HERMES ∥ OPENCLAW — 2026-05-25"
subtitle: "Comparative and Conjunction Record: Two Agent Frameworks, One Machine"
type: syzygy
source: claude-code-session-2026-05-25
tags:
- syzygy
- hermes-agent
- openclaw
- comparative
- conjunction
- witness
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - HERMES-WITNESS-REPORT-2026-05-25
  - HERMES-WITNESS-COMPANION-2026-05-25
  - HERMES-WITNESS-DELTA-2026-05-25
  - OPENCLAW-WITNESS-REPORT-2026-05-25
  - OPENCLAW-WITNESS-COMPANION-2026-05-25
  - OPENCLAW-WITNESS-DELTA-2026-05-25
---

# SYZYGY: HERMES ∥ OPENCLAW — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Comparative and conjunction record
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

*Syzygy* (σῠζῠγῐ́ᾱ): the yoking-together of two bodies in alignment — astronomical conjunction, logical pairing, the moment two distinct things are seen in relation.

This document holds the relationship between Hermes Agent and OpenClaw. The six witness documents treat each framework independently — research, local survey, gap analysis. This document treats them together: what separates them, where they intersect, and what it means that both are live simultaneously on Logan's MacBook.

Neither framework supersedes the other. This document does not recommend one over the other. It records the conjunction.

---

## AT A GLANCE

| | **Hermes** | **OpenClaw** |
|---|---|---|
| **Philosophy** | Compounding depth | Maximum reach |
| **Architecture** | Linear compounding loop | Node-graph, event-driven |
| **Execution model** | Session-based | Event bus, persistent |
| **Platforms** | 22 | 22 |
| **Skills** | 70+ built-in + self-created (Curator) | 3,286 community (ClawHub, post-ClawHavoc) |
| **Memory** | MEMORY.md + Honcho + Curator | File-based + optional plugins |
| **Identity** | SOUL.md → `~/.hermes/SOUL.md` | SOUL.md → `~/.openclaw/workspace/SOUL.md` |
| **License** | MIT (Nous Research) | MIT (501(c)(3) foundation-locked) |
| **Governance** | Nous Research (company) | Elected committee + OpenAI sponsorship |
| **Daily tokens (OpenRouter)** | 224B (#1) | 186B (#2) |
| **Security posture** | Rapid patch cycle | Post-ClawHavoc hardening; eBPF enforcement |
| **Version on MacBook** | v0.14.0 | v2026.5.16-beta.3 |
| **Gateway state** | Live — Telegram, Discord, WhatsApp | Live — local mode only (no external platforms) |

---

## THE PHILOSOPHICAL DIVIDE

**Hermes** is a depth instrument. Its core loop — SOUL → sessions → MEMORY → skills → Curator — is designed to compound. The agent that ran yesterday is slightly better than the agent that ran the day before. The Curator refines passively. Memory accumulates. Skills self-generate from completed workflows. The primary investment is time: the longer Hermes runs in a specific context, the more it knows about that context.

**OpenClaw** is a reach instrument. Its node-graph model is designed for breadth — connecting the maximum number of surfaces, enabling visual workflow composition, supporting fan-out parallelism. The primary investment is configuration: the more nodes and connections a user defines, the more the system can do. The Windows laptop (ZBFURY) is already paired as a compute node — reach extending from the MacBook to a second machine.

These philosophies are not mutually exclusive. A setup can use Hermes for memory-intensive, context-accumulating work (the agent that knows Logan over time) and OpenClaw for surface-integration, workflow-routing work (the agent that reaches everywhere at once).

---

## ARCHITECTURE CONTRAST

### Session vs. Event

Hermes organizes work around **sessions**: a conversation begins, tools run, memory candidates are collected, the session ends. The SQLite session store is the record.

OpenClaw organizes work around **events**: an event bus runs continuously. Incoming messages, tool completions, scheduled triggers, and webhook payloads arrive as typed events. Nodes subscribe to event types. The graph routes them. There is no session boundary — only the event stream.

This difference matters for coordination: a Hermes session is a discrete unit that can be tracked and referenced; an OpenClaw event is an instantaneous point in a continuous flow.

### Loop vs. Graph

```
Hermes: SOUL → session → tools → MEMORY candidates → skill generation → Curator → richer MEMORY
```

```
OpenClaw: event → input node → [tool nodes ∥ condition nodes] → output node → event
```

Hermes's loop has no native parallel fan-out. OpenClaw's graph expresses parallelism natively — multiple tool nodes can run simultaneously from a single input node.

Hermes's loop accumulates toward the future. OpenClaw's graph executes the present.

---

## SHARED SUBSTRATE

Despite their architectural differences, both frameworks share significant common ground.

### SKILL.md Format

Both use `SKILL.md` as the skill content file format — the agentskills.io standard, originally developed by Anthropic (December 18, 2025), adopted by Microsoft, OpenAI, Atlassian, Figma, Cursor, GitHub, and others.

- A Hermes skill can be read by OpenClaw (without OpenClaw's `clawmanifest.json` signing).
- A ClawHub skill can be installed into Hermes's skill directory (without manifest enforcement).
- The formats are compatible. The security postures around them are not identical.

### SOUL.md Concept

Both use `SOUL.md` as the identity injection layer — verbatim, as slot #1 in every system prompt. The paths are different; the concept is the same. A SOUL.md written for one is not portable to the other (they serve different agents with different contexts) but the authoring discipline is the same.

### MCP — Dual Direction

Both implement MCP in two directions: as a server (exposing tools to other agents) and as a client (consuming external MCP servers). The tool sets they expose are parallel in structure, differing only in their transport protocol:

- Hermes: stdio transport
- OpenClaw: WebSocket transport with `--claude-channel-mode` flag

Both expose conversation list, read, send, and event poll operations.

---

## CONJUNCTION SURFACES

Where the two frameworks can actively interact.

### MCP Cross-Consumption

Both expose MCP server interfaces. Either can consume the other's:

```
Hermes (as MCP client) ──▶  openclaw mcp serve  ──▶  OpenClaw's local hub
OpenClaw (as MCP client) ──▶  hermes mcp serve  ──▶  Hermes's platform channels
```

This creates a bridge: a Hermes session can reach OpenClaw's local-mode capabilities (node graph, ZBFURY compute); an OpenClaw node can reach Hermes's external platform channels (Telegram, Discord, WhatsApp).

Claude Code can consume both simultaneously via `.mcp.json`:

```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"]
    },
    "openclaw": {
      "command": "openclaw",
      "args": ["mcp", "serve"]
    }
  }
}
```

Neither `.mcp.json` wire has been drawn as of this survey date.

### Platform Assignment

Both support the same 22 platforms. Running both on the same platform account simultaneously is possible but creates coordination risk — two agents reading and responding to the same channel produces confusion and potential duplicate responses.

The cleaner model: assign platforms or channels by agent. For example:
- Hermes: external messaging (Telegram, Discord, WhatsApp) — platforms it is already connected to
- OpenClaw: local hub and ZBFURY compute — its current `mode: local` configuration

This assigns the depth instrument to the persistent conversation surfaces and the reach instrument to local computation and node routing.

### Skill Directory Cross-Installation

Because SKILL.md format is shared, ClawHub skills can be manually placed in `~/.hermes/skills/` and Hermes skills can be placed in `~/.openclaw/workspace/skills/`. No manifest enforcement will run (OpenClaw's clawmanifest.json requirement applies to ClawHub-installed skills, not manually placed ones). The content loads; the security verification does not.

This is an interoperability surface, not a recommended workflow — it bypasses both frameworks' security posture.

---

## CURRENT STATE ON THE MACBOOK (2026-05-25)

Both are live. Neither knows the other is running.

| | **Hermes** | **OpenClaw** |
|---|---|---|
| **Process** | PID 62971 (gateway) + PID 63078 (WhatsApp bridge) | PID 868 (gateway) |
| **LaunchAgent** | `ai.hermes.gateway.plist` | `ai.openclaw.gateway.plist` |
| **SOUL.md** | Empty — template comment only | Generic default template |
| **Memory** | MEMORY.md wiped this morning (clean slate) | MEMORY.md absent; DB 0/0 |
| **Identity init** | Never written | BOOTSTRAP.md still present |
| **Active platforms** | Telegram ✅ Discord ✅ WhatsApp ✅ Signal ❌ | None — `mode: local` |
| **Paired nodes** | (self — MacBook) | MacBook (operator) + ZBFURY (offline) |
| **MCP server** | Not wired to any client | Not wired to any client |
| **Last session** | Active | 2026-05-19 (6 days ago) |

Neither agent has been given a standing in the vault — no SOUL.md appointment, no MEMORY.md anchoring their role in the LAF governance framework. Both are present. Both are capable. Both are unaddressed.

---

## THE UNOPENED WIRES

The conjunction surfaces identified above are all currently unwired:

| Surface | What's needed | State |
|---|---|---|
| Hermes → OpenClaw via MCP | `openclaw mcp serve` added to `~/.hermes/config.yaml` under `mcp_servers:` | ❌ not configured |
| OpenClaw → Hermes via MCP | `hermes mcp serve` registered in OpenClaw's MCP client registry | ❌ not configured |
| Claude Code → both | `.mcp.json` in vault root with both server entries | ❌ not configured |
| Platform channel assignment | Explicit platform-per-agent coordination policy | ❌ not defined |
| Skill cross-installation | Manual skill placement (with understood security tradeoff) | ❌ not performed |

These are observations, not directives. Logan directs.

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a comparative and conjunction record.*
*The individual witness series:*
- *Hermes: `HERMES-WITNESS-REPORT` · `HERMES-WITNESS-COMPANION` · `HERMES-WITNESS-DELTA`*
- *OpenClaw: `OPENCLAW-WITNESS-REPORT` · `OPENCLAW-WITNESS-COMPANION` · `OPENCLAW-WITNESS-DELTA`*
