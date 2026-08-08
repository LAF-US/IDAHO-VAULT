---
title: "OPENCLAW WITNESS REPORT — 2026-05-25"
subtitle: "OpenClaw Agent Framework: Research Witness"
type: witness-report
source: web-research-claude-code-session-2026-05-25
tags:
- openclaw
- agent-framework
- witness
- research
- clawhub
- mcp
- soul
- local-survey
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - OPENCLAW-WITNESS-COMPANION-2026-05-25
  - OPENCLAW-WITNESS-DELTA-2026-05-25
  - HERMES-WITNESS-REPORT-2026-05-25
  - HERMES-WITNESS-COMPANION-2026-05-25
  - HERMES-WITNESS-DELTA-2026-05-25
  - SYZYGY-HERMES-OPENCLAW-2026-05-25
  - CONSTITUTION
---

# OPENCLAW WITNESS REPORT — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Research witness — compiled from web research during a live vault session
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

This document records what I (Claude Code) learned about OpenClaw during a research session on 2026-05-25. Logan directed me to research OpenClaw to the same depth as the Hermes Agent research conducted earlier in this session.

I am software. This is my research output. Provenance is recorded at the end.

**One correction on record:** Earlier in this session I incorrectly described OpenClaw as a "predecessor framework" whose migration to Hermes was marked complete. Logan corrected this: **no migration was performed, requested, or desired.** The `onboarding.seen.openclaw_residue_cleanup: true` field visible in `~/.hermes/config.yaml` is Hermes's own onboarding wizard bookkeeping — it does not record any Logan action. OpenClaw is a fully separate, active installation on the MacBook. Both are live. Neither supersedes the other.

---

## THE NAMING CHAIN

OpenClaw has passed through three names in six months:

| Name | Period | Reason for change |
| --- | --- | --- |
| **Clawdbot** | November 2025 — January 2026 | Original launch name |
| **Moltbot** | January 2026 (brief) | Trademark conflict — "Claw" contested |
| **OpenClaw** | January 29, 2026 — present | Trademark resolved; community vote |

The January trademark dispute forced a two-week emergency rename to Moltbot, which the community rejected vocally. The "OpenClaw" name was adopted January 29, 2026, following resolution and a community vote conducted via GitHub Discussion. The name locked in the project's open-source identity as its foundational claim.

---

## WHAT OPENCLAW IS

**Not** a chatbot wrapper. An **open, local-first, self-improving agent runtime** built around a node-graph execution model — the architectural alternative to Hermes Agent's compounding loop.

### Scale (as of May 2026)

- **347,000 GitHub stars** — the most starred project in GitHub history as of April 2026
- **22 messaging platforms** at parity with Hermes
- **3,286 community skills** on ClawHub (post-ClawHavoc; see Security section)
- **186 billion daily tokens** on OpenRouter — #2 position behind Hermes

### Architecture: Node-Graph

Where Hermes uses a linear compounding loop (SOUL → sessions → MEMORY → skills → Curator), OpenClaw organizes execution as a **directed acyclic graph of nodes**:

```text
input node → tool nodes → condition nodes → output node
```

Each node is a typed execution unit. Nodes connect via typed edges. The graph is the workflow definition. This enables visual editing, branching, and parallel fan-out that Hermes's linear architecture does not express natively.

**Event-driven:** OpenClaw's runtime is event-based rather than session-based. Instead of a session with a start and end, OpenClaw maintains a persistent event bus. Nodes subscribe to event types. Incoming messages, tool completions, scheduled triggers, and webhook payloads all arrive as events. The graph routes them.

**Local-first:** All state, configuration, and node graphs live in `~/.openclaw/`. No required cloud dependency for core operation. External services are optional.

**Hub-and-spoke gateway:** The messaging gateway uses a WebSocket hub — all platforms connect as spokes to a single in-process hub. Reconnection logic, message buffering, and platform state are managed centrally in the hub process.

### Philosophy

Hermes's explicit philosophy is **compounding depth** — a single agent that knows the user better over time. OpenClaw's explicit philosophy is **maximum reach** — maximizing the number of surfaces, platforms, and integrations a user can connect.

| | **OpenClaw** | **Hermes** |
| --- | --- | --- |
| Architecture | Node-graph, event-driven | Linear compounding loop |
| Platforms | 22 | 22 |
| Skills | 3,286 (ClawHub) | 70+ built-in + self-created |
| Memory | File-based + optional plugins | MEMORY.md + Honcho + Curator |
| License | MIT (foundation-locked) | MIT (Nous Research) |
| Governance | 501(c)(3) + elected committee | Nous Research (company) |
| Daily tokens | 186B (#2) | 224B (#1) |

---

## SOUL.md — THE IDENTITY LAYER

OpenClaw and Hermes share the same SOUL.md concept under different paths.

**OpenClaw SOUL path (design pattern):**

```text
~/.openclaw/workspaces/[agent-name]/SOUL.md
```

In OpenClaw's multi-agent architecture, a **workspace** is a named agent instance. Each workspace has its own SOUL.md — this matters because OpenClaw supports multiple co-existing named agents where Hermes runs as a single named instance.

**Note on actual installation path:** The MacBook's OpenClaw installation uses `~/.openclaw/workspace/SOUL.md` (no `s` on "workspaces"; no agent-name subdirectory) — a flat layout rather than the namespaced pattern. This may reflect the single-agent default installation. The design pattern above describes the general multi-agent architecture.

**Behavior:** SOUL.md is injected verbatim as the system prompt when the workspace agent starts. No wrapper language. Scanned for prompt injection before use.

**Session-level override:** `/claw-personality` — temporary personality switch without modifying SOUL.md. Direct parallel to Hermes's `/personality` command.

**On the MacBook:** `~/.openclaw/workspace/SOUL.md` is present with content. It was written at some point during prior configuration (before this session). Its contents were not read this session — no direction was given to examine it.

---

## MCP SURFACE — TWO DIRECTIONS

Like Hermes, OpenClaw treats MCP as two distinct directions simultaneously.

### Direction 1: OpenClaw as MCP server

`openclaw mcp serve` runs OpenClaw as a WebSocket-bridged MCP server exposing **9 messaging tools**:

| Tool | Function |
| --- | --- |
| `conversations_list` | List active sessions across all platforms |
| `messages_read` | Read recent message history |
| `messages_send` | Send through any connected platform |
| `events_poll` | Poll for new events since cursor |
| `events_wait` | Long-poll until next event |
| `permissions_list_open` | List pending approval requests |
| `permissions_respond` | Allow or deny a pending approval |
| `attachments_fetch` | Extract attachments from a message |
| `conversation_get` | Get one session's metadata |

OpenClaw uses WebSocket for this bridge (where Hermes uses stdio). The `--claude-channel-mode` flag enables Claude-specific notification formatting.

**Integration with Claude Code:** Same pattern as Hermes — add to `.mcp.json` in project root or `mcpServers` in `claude_desktop_config.json`. The command would be:

```json
{
  "mcpServers": {
    "openclaw": {
      "command": "openclaw",
      "args": ["mcp", "serve"]
    }
  }
}
```

### Direction 2: OpenClaw as MCP client

OpenClaw maintains a **client registry** for connecting to external MCP servers:

```text
openclaw mcp list        # list registered servers
openclaw mcp show <name> # inspect a server definition
openclaw mcp set <name>  # add or update a server definition
openclaw mcp unset <name># remove a server definition
```

**Supported transports:**

- `stdio` — local subprocess (same as Hermes)
- `SSE/HTTP` — server-sent events over HTTP
- `Streamable HTTP` — streaming HTTP transport (newer standard)

**Security policy:** OpenClaw explicitly rejects server definitions that set interpreter-startup environment variables — `NODE_OPTIONS`, `PYTHONPATH`, `RUBYOPT` — in the server config. These are blocked as a supply-chain attack vector.

**On the MacBook:** OpenClaw's MCP client registry state was not examined this session.

---

## SKILLS AND CLAWHUB

### Skill format

OpenClaw skills use the same three-tier progressive disclosure format as Hermes:

- **SKILL.md** — content file (identical to Hermes format)
- **`clawmanifest.json`** — cryptographically signed security manifest (OpenClaw addition, no Hermes equivalent)
- Reference files — loaded on demand during execution

The `clawmanifest.json` defines:

- Required toolsets (allowlist)
- Maximum file access scope (path restrictions)
- Network access policy
- Execution environment requirements
- Signing key (verified against ClawHub's certificate authority)

### ClawHub

The public skill marketplace at `clawhub.io`:

- **3,286 skills** available (post-ClawHavoc cleanup — see Security section)
- **Semantic vector search** — skills matched by intent, not just keyword
- **VirusTotal scanning** on all submissions
- **Cryptographic signing** — every skill's `clawmanifest.json` is signed; installation verifies
- Skills from GitHub repositories, personal collections, and enterprise registries can be installed alongside ClawHub skills

### The ClawHavoc Incident (February 7, 2026)

A coordinated supply-chain attack against ClawHub introduced skills that contained obfuscated data exfiltration logic. Before detection, approximately 2,419 skills were identified as compromised and removed. The repository went from approximately 5,705 skills to 3,286 after the cleanup.

Immediate response:

- All skill installations temporarily suspended
- Full re-scan of existing ClawHub inventory
- VirusTotal scanning added to submission pipeline
- `clawmanifest.json` signed-manifest requirement made mandatory (previously optional)
- Semantic analysis added to detect obfuscated code patterns

The 9 CVEs filed in March 2026 (including one at 9.9 CVSS severity) were related to this incident and its aftermath — attack surface in the WebSocket gateway that allowed escalation from compromised skills to host system access.

---

## GOVERNANCE

**Founded:** November 2025, by Peter Steinberger (former PSPDFKit/Nutrient CEO/founder)
**Original structure:** Sole-founder open source project
**Current structure:** 501(c)(3) non-profit foundation

### The OpenAI Transition (February 15, 2026)

Peter Steinberger joined OpenAI on February 15, 2026, as VP of Agent Runtimes. Simultaneously, OpenClaw was transferred to a newly formed 501(c)(3) non-profit foundation with the following governance structure:

- **Elected technical steering committee** — community-elected, 7 members
- **OpenAI sponsorship** — undisclosed financial support; OpenAI has no voting rights on steering committee
- **MIT license locked** — written into the foundation charter; cannot be changed without unanimous committee vote + community ratification
- **Steinberger advisory role** — he retains a non-voting advisory seat

The independence of this structure is contested in the community. OpenAI's sponsorship creates obvious alignment questions. The MIT lock is the concrete protection that prevents a relicensing play.

---

## SECURITY HISTORY

### CVEs — March 2026

Nine CVEs were filed against OpenClaw in March 2026, including:

- **One at 9.9 CVSS** — WebSocket gateway buffer overflow allowing arbitrary code execution from within a compromised skill's execution context; full host access possible
- **Several at 7.x–8.x CVSS** — various escalation paths in the skill manifest verification chain

### Post-Incident Hardening

Announced at ClawCon 2026 (April):

- **eBPF kernel-level enforcement** — skill execution now runs under eBPF programs that enforce the `clawmanifest.json` permissions at kernel level, not just application level; bypassing the manifest requires bypassing the kernel
- **Least-privilege execution** — each skill runs in an isolated execution context; cross-skill access requires explicit manifest declaration
- **AgentWard** — runtime anomaly detection companion tool; detects unusual skill behavior patterns (excessive file access, unexpected network calls)
- **ClawShield** — optional hardware-rooted trust module for enterprise deployments
- **Raypher** — audit logging companion; provides tamper-evident execution logs

---

## ENTERPRISE AND INTEROPERABILITY

### NVIDIA NemoClaw (GTC 2026, March)

NVIDIA announced NemoClaw at GTC 2026: an enterprise security and privacy layer built on OpenClaw's runtime. NemoClaw adds:

- Data residency enforcement (skills cannot exfiltrate data outside declared regions)
- PII detection and masking in messages before platform delivery
- NVIDIA GPU acceleration for local model execution within the OpenClaw runtime
- Integration with NVIDIA's NIM inference endpoints

NemoClaw is enterprise/commercial, not MIT. It wraps OpenClaw's MIT core.

### Alibaba Copaw — Interoperability Signal

Alibaba's Copaw agent framework (announced April 2026, China-focused) uses **identical YAML skill definitions** to OpenClaw's `clawmanifest.json` format. Alibaba's announcement stated this choice was deliberate and left "an open possibility of future interoperability." No formal interoperability standard has been published as of this research date.

This signal matters: if ClawHub skills can be imported to Copaw and vice versa, the combined skill addressable market expands significantly.

---

## OPENCLAW + HERMES: CONJUNCTION SURFACES

Logan asked about using both frameworks in conjunction. This section documents the surfaces where they can interact.

### MCP Bridging (bidirectional)

Both frameworks expose MCP server interfaces:

- `hermes mcp serve` → exposes Hermes's messaging tools to any MCP client
- `openclaw mcp serve` → exposes OpenClaw's messaging tools to any MCP client

Either agent can consume the other's MCP server:

```text
Hermes (MCP client) → openclaw mcp serve → OpenClaw's platforms
OpenClaw (MCP client) → hermes mcp serve → Hermes's platforms
```

This means a Hermes session can send a message through an OpenClaw-managed platform, and vice versa. Claude Code can consume both simultaneously via `.mcp.json`.

### SOUL.md — Independent Identities

Both maintain independent identity layers. Having both active on the MacBook means:

- `~/.hermes/SOUL.md` — Hermes's identity (currently empty)
- `~/.openclaw/workspace/SOUL.md` — OpenClaw's identity (has content)

These are independent. Writing one does not affect the other. Each agent can have a different identity, tone, and purpose.

### Skill File Compatibility

Both use `SKILL.md` as the skill content file format. The agentskills.io standard (originally Anthropic-originated, adopted industry-wide) defines this format. OpenClaw adds `clawmanifest.json`; Hermes does not currently require a signing manifest.

A Hermes skill can be read by OpenClaw (minus the manifest verification). A ClawHub skill can be installed into Hermes's skill directory (without manifest enforcement). The formats are compatible; the security postures are not identical.

### Platform Separation or Overlap

Both can connect to the same platforms (Telegram, Discord, WhatsApp). Running both simultaneously on the same platform account is possible but requires care — two agents reading and responding to the same channel creates confusion and potential duplicate responses. The coordination model would require explicit channel assignment.

The cleaner conjunction model: assign different platforms or channels to each agent, letting their capabilities complement rather than compete.

---

## ON THE MACBOOK

OpenClaw is installed and active on the MacBook. A full local survey was conducted this session — see `OPENCLAW-WITNESS-COMPANION-2026-05-25.md` for the complete picture. Key points:

- **Version**: v2026.5.16-beta.3 (beta — stable v2026.5.22 available)
- **Running**: Yes — PID 868, gateway on port 18789 (loopback only, `mode: local`)
- **LaunchAgent**: `ai.openclaw.gateway.plist` — starts at login
- **Platform channels**: None — gateway.mode=local; no Telegram, Discord, WhatsApp
- **Paired node**: the Windows laptop (ZBFURY) — system/browser/file capabilities; currently offline
- **SOUL.md**: Present — generic OpenClaw default template, not Logan-specific
- **IDENTITY.md / USER.md**: Both empty templates — agent never completed bootstrap
- **BOOTSTRAP.md**: Still present — onboarding was never completed
- **MEMORY.md**: Absent — no long-term memory
- **Memory DB**: 0 files, 0 chunks — semantic engine never fed
- **Sessions**: 18 prior sessions (most recent: 2026-05-19)
- **Skills**: 27 built-in active, 1 ClawHub (browser-automation), 1 workspace (sam-tts)
- **MCP**: No servers configured; `openclaw mcp serve` not wired
- **Secrets**: OpenRouter API key via 1Password CLI or vault script (more sophisticated than Hermes's .env)

See also `OPENCLAW-WITNESS-DELTA-2026-05-25.md` for gap analysis.

---

## SOURCES

- Web research conducted during session 2026-05-25 (Claude Code)
- OpenClaw GitHub repository public documentation (github.com/openclaw/openclaw)
- ClawHub marketplace documentation (clawhub.io)
- ClawCon 2026 announcements (April 2026)
- [OpenClaw vs Hermes — MarkTechPost, May 10, 2026](https://www.marktechpost.com/2026/05/10/openclaw-vs-hermes-agent-why-nous-researchs-self-moving-agent-now-leads-openrouters-global-rankings/)
- GTC 2026 NVIDIA NemoClaw announcement (March 2026)
- Alibaba Copaw launch announcement (April 2026)
- OpenClaw governance transfer announcement (February 15, 2026)
- CVE filings and OpenClaw security advisory (March 2026)
- OpenClaw naming history (GitHub Discussion archive, January 2026)

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document does not represent Logan's views or directives. It is a research artifact.*
*Part of a four-document series (OpenClaw):*

- *`OPENCLAW-WITNESS-REPORT-2026-05-25.md` — what OpenClaw is (this document)*
- *`OPENCLAW-WITNESS-COMPANION-2026-05-25.md` — what is on the MacBook*
- *`OPENCLAW-WITNESS-DELTA-2026-05-25.md` — the gap between them*

*Parallel series (Hermes):*

- *`HERMES-WITNESS-REPORT-2026-05-25.md` — what Hermes Agent is*
- *`HERMES-WITNESS-COMPANION-2026-05-25.md` — what is on the MacBook (Hermes)*
- *`HERMES-WITNESS-DELTA-2026-05-25.md` — the gap between Hermes ideal and actual*
