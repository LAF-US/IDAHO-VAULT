# Vaulted Syntax: research brief for a universal handoff protocol

**The core design problem is solved.** The prior art converges on a clear answer: a universal handoff protocol for IDAHO-VAULT should adopt USB's device-descriptor pattern (agents self-describe in a standard format), layer MCP (tool connectivity) under A2A-style agent cards (agent identity and capability advertisement), and borrow ATProto's Lexicon pattern for a typed operational vocabulary. The "USB for agents" analogy is not merely metaphorical — USB's actual architectural decisions map with surprising precision onto the multi-agent handoff problem, and the 2024–2026 protocol landscape has independently converged on the same patterns USB established in 1996.

---

## 1. The USB convergence pattern

### The design problem USB solved

Before USB (circa 1994), a typical PC back panel had **8–10 physically distinct connector types**: two DE-9 serial ports, one DB-25 parallel port, two PS/2 mini-DIN ports, one DA-15 game port, one HD-15 VGA port, plus potentially SCSI, DIN-5 keyboard, and audio jacks. Each peripheral type required its own port, its own driver, its own IRQ assignment, and its own configuration ritual. The IBM PC architecture provided only **16 IRQ lines**, of which roughly 5–6 were pre-allocated. Users manually set IRQ, DMA, and I/O addresses via jumpers or DIP switches. Adding a third serial device required an expansion card — and another scarce IRQ. Nothing was hot-pluggable. Every device needed its own power supply.

This is the exact structural analog of a multi-agent swarm where each surface (Linear, Slack, Gmail, Drive, Obsidian, GitHub) and each agent (Claude, Gemini, Copilot, Codex) uses its own format, its own assumptions, and its own handoff conventions. The pre-USB PC had no universal bus. IDAHO-VAULT currently has no universal protocol.

### How convergence happened

**Ajay Bhatt**, a senior staff architect at Intel, initiated USB development around 1990–1994, motivated by the simple frustration of connecting a printer. Intel hosted a founding meeting at its Jones Farm Campus in Hillsboro, Oregon, bringing together six other companies. The **USB Implementers Forum** was formally established December 5, 1995, with seven founding members: **Intel, Compaq, Microsoft, DEC, IBM, NEC, and Nortel**. USB 1.0 shipped January 1996.

The convergence was driven by **aligned incentives across different roles**: Intel wanted to simplify chipset design, Microsoft wanted to deliver on the Plug-and-Play promise of Windows 95, PC OEMs wanted fewer SKUs on back panels, and peripheral makers wanted a larger addressable market. Intel made USB **open and royalty-free** — deliberately forgoing licensing revenue to maximize adoption. Bhatt: "I don't do these things for money. I did this to bring about change."

### The five design decisions that made USB universal

**Decision 1: Host-controller architecture.** One host, many devices. The host initiates all transactions, schedules all bandwidth, manages enumeration, controls power. Devices cannot communicate directly with each other. This was a **deliberate simplification** — Bhatt stated they needed to "build an interface that would work with devices that had 25-cent silicon." Complexity lives in the host; devices stay cheap and dumb.

**Decision 2: Standardized physical connector with enforced directionality.** Type-A (host-side) and Type-B (device-side) prevent accidentally connecting two hosts. Data pins are recessed behind power pins so power establishes before data connects.

**Decision 3: The enumeration protocol.** When a device connects, the host automatically detects it (voltage change on D+/D- lines), issues a bus reset, requests the device descriptor at default address 0, assigns a unique address (1–127), reads the full descriptor hierarchy, matches it to a driver, and activates a configuration. The entire process is automatic. No IRQs, no jumpers, no reboots.

**Decision 4: The device descriptor — the critical design pattern.** Every USB device must provide an **18-byte fixed-structure self-identification record** containing: USB spec version (bcdUSB), device class/subclass/protocol, vendor ID, product ID, device version, max packet size, number of configurations, and string descriptor indices. Below this sits a hierarchy: Configuration → Interface → Endpoint descriptors. The host traverses this tree top-down. **The device declares what it is, what it needs, and how to communicate with it. The host never needs to know the device's internals.** This inversion — from "the user tells the system what's connected" to "the device tells the system what it is" — is the fundamental architectural insight.

**Decision 5: Class-based polymorphism.** USB device classes (HID, Mass Storage, Audio, CDC, Video) enable generic drivers. A keyboard from any manufacturer works with the same HID class driver. The host doesn't need vendor-specific knowledge — only the class code.

### What USB deliberately excluded

USB did not attempt peer-to-peer communication (unlike FireWire), guaranteed real-time performance, long-distance connectivity (5m max), networking/multi-host, or reversible connectors. Each exclusion was a **scope decision** that kept the standard achievable. USB 1.0 at 12 Mbit/s was slower than SCSI and the forthcoming FireWire 400 — critics called it "Useless Serial Bus." Adoption was sluggish until Apple's iMac G3 (August 1998) shipped USB-only, forcing the peripheral ecosystem to comply.

### The analogy mapping for multi-agent protocol design

| USB concept | Multi-agent analog |
|---|---|
| Device Descriptor (18 bytes) | Agent Card / Agent Descriptor — self-identifying manifest published on connection |
| idVendor + idProduct | Agent identity — unique identifier for provider and agent type |
| bcdUSB | Protocol version — which version of the handoff protocol the agent supports |
| bDeviceClass/SubClass | Agent capability class — general category of work (text-generation, code-execution, retrieval) |
| Configuration Descriptor | Agent configuration profiles — different modes the agent can operate in |
| Interface Descriptor | Functional interfaces — specific capabilities/APIs the agent exposes |
| Endpoint Descriptor | Communication endpoints — channels with defined transfer types, directions, rate limits |
| bMaxPacketSize | Max message/token size — payload constraints per transaction |
| bMaxPower | Resource consumption declaration — compute/memory/cost budget |
| Enumeration | Agent registration/discovery — orchestrator discovers agents, reads descriptors, assigns identifiers |
| SET_CONFIGURATION | Agent activation — orchestrator selects which mode to activate |
| Host-controller model | Orchestrator pattern — central coordinator that schedules all communication |
| Class drivers | Generic agent adapters — standard interfaces that work with any agent of a given class |

**The core lesson:** USB succeeded because it required every device to **self-describe in a standardized format before communication begins.** This decouples the host from device internals, enables hot-plugging (agents joining/leaving dynamically), and allows a single orchestrator to manage a heterogeneous ecosystem.

---

## 2. Prior art survey

### 2A. Model Context Protocol (MCP) — highest priority

**Status:** Announced November 25, 2024 by Anthropic; donated to the **Agentic AI Foundation (AAIF)** under the Linux Foundation on December 9, 2025. Co-founded by Anthropic, Block, and OpenAI; platinum members include AWS, Bloomberg, Cloudflare, Google, Microsoft. Current spec version: **2025-11-25**. Licensed MIT (spec) and Apache 2.0 (SDKs/servers). **97M+ monthly SDK downloads**, 10,000+ published servers, 58 maintainers.

**What it is:** MCP solves the N×M integration problem — previously, integrating N tools with M AI front-ends required N×M custom connectors. MCP reduces this to N+M. It is inspired by Microsoft's Language Server Protocol (LSP) and has been called "the USB-C for AI." It is fundamentally a **model-to-tool protocol**, not an agent-to-agent protocol.

**Architecture:** Three roles — **Host** (the LLM application, acts as security broker), **Client** (connector within the host maintaining a 1:1 stateful connection with a server), **Server** (lightweight service exposing tools, resources, and prompts). All communication uses **JSON-RPC 2.0** over three transport options: stdio (local subprocess), Streamable HTTP (recommended for remote), or legacy HTTP+SSE. Initialization follows a strict three-phase lifecycle: capability negotiation → initialized notification → operation.

**Three primitives:**
- **Tools** (model-controlled): executable functions with JSON Schema inputs. The AI model decides when to call them.
- **Resources** (application-controlled): read-only data sources identified by URIs, with subscription support.
- **Prompts** (user-controlled): reusable parameterized message templates.

**Capability negotiation** happens at initialization: client and server each declare what features they support (tools, resources, prompts, sampling, logging, roots). If a client doesn't advertise a capability, the server must not use it.

**Authentication:** OAuth 2.1 for HTTP transports (added in the 2025-06-18 spec). Servers classified as OAuth Resource Servers. For stdio transport, relies on OS-level process permissions. Client ID Metadata Documents (added 2025-11-25) simplify registration.

**What MCP does not do:** MCP has **no agent discovery mechanism** (no equivalent of Agent Cards), **no peer-to-peer communication** (fixed client-server asymmetry), **no multi-party negotiation**, **no agent identity standard**, and **no structured handoff primitive**. Session state is transient and in-memory — if the connection dies, state is lost. MCP is point-to-point, not mesh.

**Security concerns are significant.** Documented vulnerabilities include prompt injection via tool metadata, tool poisoning (5.5% of public servers affected), rug-pull attacks (tools silently changing behavior post-installation), and cross-server interception. The spec uses SHOULD (not MUST) for human-in-the-loop requirements.

**The 2025-11-25 spec additions are relevant:** Tasks (experimental abstraction for tracking long-running server work with states: working, input_required, completed, failed, cancelled) and Sampling-with-Tools (servers can run their own agentic loops using the client's LLM, enabling server-side sub-agents).

### 2B. Agent-to-Agent Protocol (A2A)

**Status:** Announced April 9, 2025 by Google; donated to the Linux Foundation June 23, 2025. **150+ supporting organizations** including AWS, Microsoft, Salesforce, SAP, Atlassian, Adobe. Current version: **v1.0** (stable, as of March 2026). Licensed Apache 2.0. **22,000+ GitHub stars**. Five production SDKs (Python, JavaScript, Java, Go, .NET). Production deployments in supply chain, financial services, and IT operations. Microsoft integrated A2A into Azure AI Foundry and Copilot Studio; AWS added support through Amazon Bedrock AgentCore.

**What it is:** A2A standardizes **agent-to-agent communication** — how agents from different frameworks discover each other, delegate tasks, report status, and pass artifacts. Where MCP is vertical (agent-to-tool), A2A is horizontal (agent-to-agent). The official documentation states: "Use MCP for tools and A2A for agents."

**The Agent Card — the USB device descriptor analog.** Every A2A agent publishes an **Agent Card** at `/.well-known/agent-card.json` — a JSON document containing: name, version, description, capabilities (streaming, push notifications, state history, extended card), skills (each with id, name, description, tags, examples, input/output MIME types), supported interfaces (JSON-RPC, gRPC, REST with URLs), security schemes, provider info, and optional cryptographic signatures. Extended Agent Cards (authenticated versions) expose additional private capabilities. **This is the closest existing implementation of the USB device descriptor pattern for agents.**

**Task lifecycle:** Tasks progress through defined states: `submitted → working → input-required → completed | failed | canceled | rejected`. The `input-required` state enables multi-turn interaction — the agent can pause and ask the client for more information. Status updates delivered via polling, SSE streaming, or webhook push notifications.

**Artifacts** are tangible outputs (documents, images, structured data) composed of typed Parts: TextPart, FilePart, DataPart, FormPart, IFramePart, VideoPart, AudioPart, ActionPart. Artifacts can be streamed incrementally.

**Three-layer spec architecture:** Layer 1 is a canonical data model in Protocol Buffers (`spec/a2a.proto`); Layer 2 defines abstract operations; Layer 3 maps to concrete protocol bindings (JSON-RPC, gRPC, REST). Agents declare supported bindings in their Agent Card's `supportedInterfaces`.

**Authentication:** Declared in Agent Cards via `securitySchemes` (aligned with OpenAPI). Supports API Key, HTTP Auth, OAuth 2.0, OpenID Connect, Mutual TLS. Agent Card Signing (v1.0) uses JWS per RFC 8785 for identity verification.

**Limitations for a single-operator system:** Network overhead (HTTP/gRPC even for local agents), no centralized registry standardized yet, no shared memory by design (agents are opaque), and authentication overhead unnecessary in a trusted single-operator deployment. A2A is primarily designed for enterprise/multi-party scenarios but can work for personal systems — it may be over-engineered for a trusted local environment.

### 2C. AT Protocol (ATProto)

**Focus areas: DID identity, Lexicon schemas, Relay model.**

**DID-based identity.** ATProto uses W3C Decentralized Identifiers as persistent, primary account identifiers. Two supported methods: **did:plc** (custom method; identifier derived from `base32(sha256(signedGenesisOp)).slice(0,24)`; resolved via PLC directory at `plc.directory`) and **did:web** (DID document served at `/.well-known/did.json`). A resolved DID document contains: the DID itself, `alsoKnownAs` (handle aliases), `verificationMethod` (signing key as Multikey type), and `service` (PDS endpoint URL). The routing flow is: **DID → resolve DID document → extract service endpoint → route request**. Handle resolution works bidirectionally: DNS TXT at `_atproto.{handle}` maps handle→DID, and DID document's `alsoKnownAs` maps DID→handle. Both directions must validate.

**Lexicon schema system.** Lexicon is ATProto's schema definition language for repository record types, HTTP API endpoints, WebSocket event streams, and OAuth scopes. Schemas are identified by **NSIDs** (Namespaced Identifiers) in reverse-DNS format (e.g., `app.bsky.feed.post`). Primary definition types: `record` (stored data), `query` (GET endpoint), `procedure` (POST endpoint), `subscription` (WebSocket stream). The type system includes concrete types (boolean, integer, string with format constraints like `did`, `handle`, `datetime`), containers (array, object), and meta types (`ref` for reuse, `union` for discriminated unions with `$type` field, `unknown`, `token` for symbolic values). **Open unions** default to accepting new variants without breaking old implementations. Unexpected fields are ignored, not rejected — enabling forward-compatible schema evolution. Backward-compatible evolution rules: new fields must be optional, non-optional fields cannot be removed, types cannot change, breaking changes require a new NSID.

**The Relay model.** A Relay aggregates event streams from multiple Personal Data Servers (PDS) into a single unified firehose — a real-time WebSocket stream of all data changes. Event types: `#commit` (record create/update/delete with signed commit and Merkle tree proof), `#identity` (DID/handle changes), `#account` (status changes). Architecture: PDS → Relay → AppView. Relays are content-agnostic (don't parse records), permissionless, and replaceable. Cursor-based replay allows consumers to reconnect and catch up from where they left off.

**Service-to-service authentication** uses short-lived JWTs signed by the account's signing key, with `iss` (sender DID), `aud` (receiver DID + service fragment), `lxm` (bound to specific method), and 60-second expiration. Verification: receiving service resolves sender's DID, extracts public key, verifies signature.

**What transfers to agent protocol design:** DID as agent identity (stable, resolvable, key-rotation-capable); DID document as routing table (agent DID → resolve → service endpoint); Lexicon as operational vocabulary (define agent operations as typed schemas under a namespace like `ai.swarm.task.handoff`); Relay as event bus (aggregate agent events, enable cursor-based replay for crash recovery); service auth JWTs for lightweight inter-agent authentication.

**What does not transfer:** ATProto's scale assumptions (millions of accounts vs. 3–20 agents), public data model (agent communication needs privacy), did:plc centralization (PLC directory is a single server), MST/repo structure (overengineered for small agent state), DNS-based handle resolution (adds latency), and the 72-hour recovery window (designed for human account theft, not agent key management).

### 2D. ActivityPub

ActivityPub (W3C Recommendation, January 2018) uses the Actor model with inbox/outbox message passing and JSON-LD-serialized Activities. It is designed for **federation between independent, mutually untrusted servers** — a problem IDAHO-VAULT does not have. The Actor model abstraction and typed activity vocabulary have conceptual merit, but the federation machinery (server discovery, HTTP Signatures, content delivery fan-out) is unnecessary for a single-operator swarm. **Verdict: not worth deeper investigation.** The relevant patterns from ActivityPub already appear in purpose-built agent protocols.

### 2E. JSON-LD and Schema.org

JSON-LD adds semantic meaning to JSON through `@context`, `@type`, and `@id`. It enables self-describing data and semantic interoperability. Schema.org provides a shared vocabulary. **ANP (Agent Network Protocol) already uses JSON-LD as its primary data format**, and LMOS (Eclipse Foundation) uses it for agent capability descriptions. For IDAHO-VAULT, plain JSON with a well-defined schema is likely more practical than full JSON-LD, unless cross-framework interoperability becomes a requirement. The complexity and verbosity of JSON-LD are costs without clear benefit in a single-operator context.

### 2F. Emerging protocols and standards (2025–2026)

The landscape has consolidated around a **"dual-stack" pattern**: MCP for agent-to-tool (vertical) and A2A for agent-to-agent (horizontal). Several additional protocols merit attention:

**Agent Communication Protocol (ACP)** — IBM BeeAI, now Linux Foundation. Lightweight REST-native agent messaging. Standard HTTP verbs, multipart messages, capability-based security tokens. Simpler than A2A but less capable.

**Agent Network Protocol (ANP)** — Most ambitious identity model. Uses **W3C DIDs for agent identity**, JSON-LD for data, and a three-layer stack (identity/encryption, meta-protocol negotiation, application protocol). Has an MCP-to-ANP bridge. White paper published July 2025; drove the creation of the **W3C AI Agent Protocol Community Group** (first meeting June 2025). Specifications expected 2026–2027.

**NLIP (Natural Language Interaction Protocol)** — Ecma International TC56. **Five standards approved December 10, 2025** (ECMA-430 through ECMA-434). Universal envelope protocol using natural language instead of shared ontologies. Uses CBOR/JSON over WebSocket. Unique approach: generative AI translates between local ontologies, enabling "hot-extensibility" without requiring all agents to share a schema.

**Anthropic Agent Skills** — Open standard (December 18, 2025). Standardized format for packaging procedural knowledge as SKILL.md folders. Complements MCP (MCP = connectivity; Skills = operating manual). **Already adopted by OpenAI, Microsoft, Atlassian, Figma, Cursor, GitHub.** Donated to AAIF.

**AGENTS.md** — OpenAI (August 2025). Lightweight markdown convention for giving AI coding agents project-specific guidance. **60,000+ open-source projects.** Donated to AAIF.

**OASF (Open Agentic Schema Framework)** — AGNTCY/Cisco. Standardized schema for defining agent capabilities using attribute-based taxonomies. Content-addressable, OCI-compatible. Agent Directory for discovery. Supports A2A agents, MCP servers, Copilot manifests.

**OpenAI Agents SDK** — Introduced the **Handoff** pattern: agents explicitly transfer control to each other, carrying conversation context. Not a wire protocol; in-process orchestration. Uses MCP for tool connectivity.

**Governance has consolidated** around the Linux Foundation: AAIF (MCP, AGENTS.md, Goose), A2A Project, AGNTCY (OASF, ACP). The W3C AI Agent Protocol Community Group is pursuing longer-term standardization (2026–2027).

**FIPA** (Foundation for Intelligent Physical Agents, 1996) is **effectively dormant**. Its concepts (performatives, directory facilitators, agent management systems) have been absorbed into modern protocols. Not actively relevant.

---

## 3. Compatibility notes

This section maps each external protocol against the existing IDAHO-VAULT internal conventions, noting where they align and where they conflict. Per the project constraints, internal conventions are referenced only as a compatibility surface — no details about their implementation are fabricated or inferred.

### Agent-to-agent signal protocol (status, threading, naming)

- **A2A aligns strongly.** A2A's task lifecycle states (`submitted → working → input-required → completed → failed → canceled → rejected`) provide a formalized version of agent status signaling. A2A's `contextId` groups related tasks, which maps to threading. A2A Agent Cards include `name`, `version`, and `description` fields that could align with naming conventions.
- **MCP partially aligns.** MCP's experimental Tasks feature (2025-11-25 spec) introduces states (`working`, `input_required`, `completed`, `failed`, `cancelled`). However, MCP has no threading or naming conventions for agents — only for servers and tools.
- **ATProto aligns for naming and identity.** DID handles provide a resolution-verified naming system. DID documents provide a structured identity format. Lexicon tokens (`ai.swarm.status#idle`, `ai.swarm.status#working`) could formalize status signaling as a typed vocabulary.
- **Potential conflict:** A2A task states are a fixed enum. If IDAHO-VAULT's internal signal protocol uses custom states not in A2A's set, the mapping would need an extension mechanism or a compatibility layer.

### Layer model (CANON / DRIVE / RUNTIME / ARCHIVE)

- **No external protocol directly maps to a four-layer architecture.** MCP's primitives (Tools, Resources, Prompts) are functional categories, not architectural layers. A2A operates entirely at what would likely be the RUNTIME layer. ATProto's PDS → Relay → AppView is a three-tier data flow, not an architectural layer model.
- **ATProto's architecture is the closest structural analog:** PDS (origin data) → Relay (aggregation/routing) → AppView (materialized views) could map loosely to CANON (source of truth) → RUNTIME (active processing) → DRIVE (working state), with ARCHIVE as a distinct persistence layer ATProto doesn't address.
- **Implication:** The layer model is an internal architectural decision that external protocols would plug into, not replace. MCP servers would operate at the RUNTIME layer. Agent Cards would be published from CANON. Archived handoff records would live in ARCHIVE. The protocol itself should be layer-aware (e.g., handoff packets could include a `layer` field indicating which layer they originate from or target), but no external protocol provides this.

### Agent training sequence and volunteer assignment table

- **A2A's Agent Card skills field is the closest analog.** Skills with `id`, `description`, `tags`, and `examples` could encode training status or assignment eligibility. However, A2A has no concept of training sequence or progressive capability unlock.
- **Agent Skills (Anthropic) aligns for capability packaging.** SKILL.md files with progressive disclosure (summary → full instructions) mirror a training sequence where agents progressively load capability.
- **No external protocol models assignment tables.** Volunteer assignment (which agent handles which task type) is an orchestration-layer concern. A2A's capability-based routing (match skills to tasks) provides the mechanism, but the assignment policy is internal.

### Machine-readable agent registry (swarm.json)

- **A2A Agent Cards are the most direct external equivalent** of entries in a swarm.json. Each Agent Card is a JSON document describing a single agent's identity, capabilities, and endpoint. A swarm.json could be implemented as a local index of Agent Cards, or as a directory service that returns Agent Cards for registered agents.
- **MCP has no agent registry concept** — only server-level identification.
- **OASF (Open Agentic Schema Framework)** provides an Agent Directory that could serve as a more formal registry, supporting A2A agents, MCP servers, and other agent types.
- **ATProto's DID resolution** provides a decentralized registry pattern (DID → DID document → service endpoint), but is overengineered for a local registry.
- **Potential compatibility pattern:** swarm.json entries could adopt A2A Agent Card schema for each agent, making the registry externally interoperable without changing the internal file structure.

### Capability tiers and lane rules

- **A2A Agent Cards partially support this.** Skills can be tagged and categorized, and Extended Agent Cards (authenticated) can expose different capability levels to different requestors. However, A2A has no concept of capability tiers (graduated permission levels) or lane rules (constraints on which agents can perform which operations).
- **MCP's Roots** provide a boundary mechanism (servers can only access defined filesystem scopes), which is a form of lane rule.
- **OAuth scopes** (used by both MCP and A2A) could encode capability tiers as scope hierarchies.
- **ATProto's Lexicon permission-sets** define OAuth scope bundles, which could model capability tiers as graduated scope sets.
- **Conflict:** No external protocol models the concept of "lanes" — constraints that an agent of tier X can only operate on certain task types or surfaces. This is an orchestration-level policy that would need to be implemented in the Vaulted Syntax protocol itself, not adopted from external standards.

### Naming, frontmatter, sourcing, and path conventions

- **ATProto's NSID system aligns with path conventions.** Reverse-DNS namespaced identifiers (e.g., `ai.swarm.task.handoff`) provide a structured naming system that could complement internal path conventions.
- **Agent Skills' SKILL.md metadata** is a form of frontmatter — structured metadata at the top of capability files.
- **AGENTS.md** is a frontmatter-like convention for project-level agent guidance.
- **MCP tool schemas** (name, description, input JSON Schema) provide structured metadata for capabilities, analogous to frontmatter for tools.
- **Potential conflict:** If internal naming conventions use a different format than NSID or Agent Card naming, a mapping layer would be needed. ATProto NSIDs use dots as separators and reverse-DNS authority; if IDAHO-VAULT uses slashes or different authority patterns, the conventions would need reconciliation.

---

## 4. Design implications for Vaulted Syntax

### The protocol should have three layers, not one

The prior art converges on a clear separation of concerns:

1. **Identity and descriptor layer** — how agents self-describe and discover each other. Adopt the A2A Agent Card pattern. Each agent in IDAHO-VAULT publishes a machine-readable descriptor containing: agent ID, protocol version, capability class, supported interfaces, skills/capabilities, input/output formats, resource requirements, and human-readable metadata. This maps directly to swarm.json entries. The descriptor is the "USB device descriptor" — it is the first thing an orchestrator reads when an agent connects.

2. **Tool and context layer** — how agents access tools and pass context. This is MCP. The system already uses MCP. No change needed at this layer, but Vaulted Syntax should define how MCP tool results are packaged into handoff packets.

3. **Handoff and coordination layer** — how agents delegate tasks, report status, and transfer context to each other. This is the gap. Neither MCP nor A2A fully solves this for a single-operator personal swarm. A2A's task lifecycle provides the state machine; OpenAI's Handoff pattern provides the transfer-of-control concept; ATProto's Lexicon provides the typed vocabulary.

### The device descriptor is the highest-leverage design element

USB's success was built on the device descriptor. The Agent Card is the proven implementation of this pattern for agents. **Vaulted Syntax should define an Agent Descriptor format** that:

- Is compatible with A2A Agent Card schema (for potential external interoperability)
- Extends it with IDAHO-VAULT-specific fields: capability tier, lane assignments, layer affinity (CANON/DRIVE/RUNTIME/ARCHIVE), training status, and surface bindings (which external services the agent can access)
- Is the canonical representation in swarm.json
- Is the first thing the orchestrator reads when an agent connects or is invoked
- Contains enough information for the orchestrator to route, authorize, and configure the agent without knowing its internals

### Lexicon-style typed vocabulary should define the operational language

ATProto's Lexicon system provides the best model for defining a **shared operational vocabulary** for Vaulted Syntax. Define operations as Lexicon-style schemas under a custom namespace:

- `vault.handoff.transfer` — procedure: transfer task between agents
- `vault.signal.status` — record: agent status update
- `vault.context.share` — procedure: share context blob
- `vault.task.assign` — procedure: assign task to agent

Each schema strictly defines input/output types, required/optional fields, and validation rules. Open unions allow adding new operation types without breaking existing agents. The NSID system provides natural namespacing. This vocabulary becomes the "USB protocol" — the shared language that all agents speak regardless of their internals.

### The host-controller model is correct for a single-operator system

USB's deliberate decision to use a host-controller model (one host, many devices, no peer-to-peer) maps precisely to a single-operator swarm. **The journalist is the host. Agents are devices.** Peer-to-peer agent communication (A2A's design target) adds complexity without benefit when a single operator controls all agents. The orchestrator should initiate all handoffs, schedule all work, and manage all state — just as the USB host controller initiates all transactions.

This means A2A's full peer-to-peer model is **overengineered** for IDAHO-VAULT, but its Agent Card format and task lifecycle are directly adoptable. MCP's client-server model already enforces the correct topology.

### The handoff packet is the missing primitive

No existing protocol defines a complete **handoff packet** — the structured artifact that transfers everything a receiving agent needs to continue a task. Based on the prior art, a Vaulted Syntax handoff packet should contain:

- **Task descriptor:** what needs to be done (typed per Lexicon schema)
- **Context payload:** conversation history, intermediate results, relevant documents (structured as MCP Resources)
- **Provenance chain:** which agents have touched this task, what they did, and what they produced (analogous to ATProto's signed commit chain)
- **Capability requirements:** what the receiving agent needs to be able to do (matchable against Agent Descriptor skills)
- **Layer and path metadata:** which CANON/DRIVE/RUNTIME/ARCHIVE layer this task operates at, and relevant path conventions
- **Status and threading:** current status, thread ID, parent task reference (compatible with the internal signal protocol)

### What to exclude from scope

Following USB's example of deliberate exclusion, Vaulted Syntax should **not** attempt to:

- Replace MCP for tool connectivity (MCP already works; layer on top of it)
- Implement federation or multi-operator trust (single operator; no need for DID resolution infrastructure, OAuth between agents, or signed Agent Cards)
- Define transport (use existing transports — stdio for local, HTTP for remote)
- Standardize agent internals (the whole point is that agents are opaque; only the descriptor and handoff protocol are standardized)
- Handle billing, payments, or resource accounting (the Agent Payments Protocol exists but is irrelevant here)

### The NLIP insight deserves attention

NLIP's approach — using natural language instead of shared ontologies, with generative AI translating between local vocabularies — is worth watching. For a system where agents include LLMs with different capabilities and contexts, the assumption that all agents will perfectly adhere to a typed schema may be brittle. A Vaulted Syntax handoff packet could include both a **structured typed payload** (for machine parsing) and a **natural language summary** (for LLM-based agents that can interpret intent even if the schema doesn't perfectly match). This dual-format approach provides schema-enforced reliability with natural-language fallback.

### Recommended next steps

The prior art is sufficient to begin protocol design. The three immediate design tasks are: **(1)** define the Agent Descriptor schema, extending A2A Agent Card format with IDAHO-VAULT-specific fields; **(2)** define the handoff packet schema, using Lexicon-style typed definitions under a `vault.*` namespace; **(3)** define the state machine for handoff lifecycle, adopting A2A's task states and extending with any internal signal protocol states that don't map to the A2A set. Everything else — transport, authentication, tool access — already exists and should be reused, not reinvented.