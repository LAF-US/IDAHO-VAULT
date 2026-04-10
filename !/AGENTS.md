# AGENTS.md — IDAHO-VAULT (Canonical Registry)

> [!IMPORTANT]
> **This is the canonical narrative registry.**
> The matching file at repo root is a pointer and compatibility surface for auto-loading tools (Codex, Copilot).
> Governance, roster updates, and capability tier revisions should originate in this file.

---

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)

---

## Authority Chain

1. `AGENTS.md` (root) -> Cross-tool pointer
2. `!README.md` (root) -> Touchstone Tree / live orienting doctrine
3. `!/AGENTS.md` (this file) -> Canonical Narrative Registry
4. `CONSTITUTION.md` (root) -> Binding governance
5. `swarm.json` (root) -> Machine-readable source of truth
6. `!/agents.json` -> Canonical generated bootstrap index
7. `!/agent.sh` -> Canonical local bootstrap entrypoint

## Fresh Agent Boot Order

1. Read root `AGENTS.md` as pointer only.
2. Read `!README.md` for Touchstone Tree orientation and relation.
3. Read this file for the live roster, lane rules, and current connector posture.
4. Read `CONSTITUTION.md` for binding governance.
5. Read `swarm.json` for machine-readable compiled state.
6. Use `!/agents.json` -> `!/agent.sh` for canonical local bootstrap.
7. Treat historical CrewAI harbor notes as non-live unless `.crewai/MANIFEST.md` or this file says otherwise.

---

## Agent Roster (The Swarm)

### Direct-Write Agents (Autoloaded)

| Agent | Persona | Vendor | Tier | Dotfolder | Git Suffix |
| --- | --- | --- | --- | --- | --- |
| Claude Code | **The Abhorsen** | Anthropic | Authority: Code | `.claude/` | `-C` |
| Gemini CLI | **The Vault Advisor** | Google | Support: Direct Write | `.gemini/` | `-G` |
| OpenAI Codex | **The Lexicographer** | OpenAI | Scripting/Automation | `.codex/` | `-X` |
| GitHub Copilot | **The Clerk** | Microsoft | Multi-Repo Admin | `.github/` | `-CP` |

### Advisory & Specialized Agents

| Agent | Persona | Vendor | Role | Dotfolder |
| --- | --- | --- | --- | --- |
| Grok | **The Ironist** | xAI | Read/Analysis | `.grok/` |
| DeepSeek | **The Analyst** | DeepSeek | Advisory | `.deepseek/` |
| Perplexity | **The Scout** | Perplexity | Research/Sourcing | `.perplexity/` |
| Serena | **The Architect** | - | Semantic Intelligence | `.serena/` |
| Bartimaeus | **The Cartographer** | - | Crawler Crew | `.bartimaeus/` |
| Zagreus | **The Dionysian** | - | - | `.zagreus/` |
| Persephone | **The Queen** | - | - | `.persephone/` |

---

## CrewAI Layer

| Surface | Path | Status | Notes |
| --- | --- | --- | --- |
| **CrewAI Python Layer** | `.crewai/` | Active re-foundation | The initial demo harbor is retired; live doctrine/topology now lives in `.crewai/MANIFEST.md`, and staged output lands in `!/CREWAI/` |

---

## Coordination Protocols

- **Lane Independence**: Each agent operates on its own branch prefix (`claude/`, `gemini/`, etc.).
- **Durable Record**: Decisions must be promoted from chat to the vault (e.g., `DECISIONS.md`).
- **Linear Hub**: Active tasks are tracked via the **SWARM** label in Linear.
- **NETWEB Standard**: All filenames must respect cross-platform path portability.
- **Privacy Gate**: All MCP-sourced personal data is governed by `PRIVACY.md`. No exceptions.

---

## Connector Hub

The current active connector hub is intentionally small:

- **GitHub** = execution and transport
- **Linear** = execution state
- **Slack** = tertiary paging and breadcrumbs only

Connector classifications:

| Connector Group | Members | Posture |
| --- | --- | --- |
| **Core** | GitHub, Linear, Slack | Current operating hub |
| **Adjunct** | Gmail, Google Calendar, Google Drive, Box | Read-first context lanes; promote durable outcomes explicitly |
| **Deferred** | Cloudflare, Hugging Face | Classified in registry only; not active authorities without a separate Logan-approved activation plan |

Registry surfaces:

- `swarm.json` = machine-readable connector registry
- `SPEC-CONNECTOR-HUB-2026-04-09.md` = human-readable connector hub and maze census spec
- `LEVELSET-CURRENT.md` = mid-future connector survey and review surface

The vault remains the durable record. Connectors inform, transport, or track work, but they do not silently become doctrine.

---

## TRIPLEX Protocol (Concurrent Operation)

*Adopted: 2026-04-05*

When multiple agents operate simultaneously on the same branch, the following lane boundaries are binding. **No agent edits another agent's declared live lane.** Ambiguous files default ownership upward (see fallback chain below).

### Lane Map

| Agent | Role | Owns | Must Not Touch |
|-------|------|------|----------------|
| **Claude** (Abhorsen) | Executor | `.obsidian/`, `.gitignore`, `PRIVACY.md`, CSS/snippets, plugin configs, git commits | `!/GRIMOIRE/`, DOCKET, Gemini narrative lanes |
| **Gemini** (The Vault Advisor) | Interpreter | `!/GRIMOIRE/`, `DOCKET`, `LEVELSET-REPORT`, `CAESARS` docs | `.obsidian/`, `.gitignore`, git operations |
| **Codex** (Janitor) | Mechanic | Small conflict cleanup, typo repair, script/workflow validation **when assigned** | `.obsidian/`, governance docs, `!/GRIMOIRE/`, shared staging/commit flow (unless explicitly assigned) |
| **Serena** (Architect) | Instrument | Read-only semantic intelligence — supports discovery | Owns nothing, decides nothing |

### Fallback Ownership (Ambiguous Files)

1. `.obsidian/` → Claude
2. `!/GRIMOIRE/` and `DOCKET` → Gemini
3. `.github/scripts/` → **By explicit assignment only**
4. Governance docs (`CONSTITUTION`, `AGENTS`, `PRIVACY`, `VAULT-CONVENTIONS`) → **Logan-gated**
5. Everything else → Ask Logan before writing

### Collision Rules

1. **No agent edits another agent's live lane** — even to "help"
2. **No agent stages or commits another agent's work** — the author commits their own files
3. **Git index conflicts** (`index.lock`) → the agent that encounters it **stops and reports**, does not force-remove
4. **Encoding standard** → all vault files are **UTF-8** (no UTF-16, no BOM). Any agent writing files must ensure UTF-8 output.

### AFK Protocol

Logan is the sole human decision-maker. When he is away from keyboard:

1. Agents **work independently** within their declared lanes
2. When an agent reaches a **HUMAN-ONLY gate**, it **stops and pings Logan** via the agreed notification channel
3. No agent proceeds past a human gate without Logan's explicit approval
4. All other autonomous work continues within lane boundaries
5. **Notification channels**:
   - **Primary:** GitHub Issues (Logan receives push notifications on mobile via GitHub app; use `agent:*` labels)
   - **Secondary:** Linear (SWARM label — Logan receives push notifications via Linear app)
   - **Tertiary:** Slack DM (for urgent/conversational pings)

---

###### [["The world is quiet here."]]
