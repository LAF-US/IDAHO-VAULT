# AGENTS.md — IDAHO-VAULT (Canonical Registry)

> [!IMPORTANT]
> **This is the canonical narrative registry.**
> The matching file at repo root is a pointer and compatibility surface for auto-loading tools (Codex, Copilot).
> Governance, roster updates, and capability tier revisions should originate in this file.

---

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/LAF-US/IDAHO-VAULT (public)

---

## Authority Chain

1. `AGENTS.md` (root) -> Cross-tool pointer
2. `!/WAKEUP.md` -> Explicit wakeup and conflict-resolution surface
3. `!README.md` (root) -> Touchstone Tree / live orienting doctrine
4. `!/AGENTS.md` (this file) -> Canonical Narrative Registry
5. `CONSTITUTION.md` (root) -> Binding governance
6. `swarm.json` (root) -> Machine-readable source of truth
7. `!/agents.json` -> Canonical generated bootstrap index
8. `!/agent.sh` -> Canonical local bootstrap entrypoint

Tree logic for crew space:

- `!` is the Swarmic Nest: collective group space.
- `.*` dotfolders are individual agent space.
- Registry, routing, and coordination should preserve that distinction.

## Fresh Agent Boot Order

1. Read root `AGENTS.md` as pointer only.
2. Read `!/WAKEUP.md` before interpreting lore, branch residue, or older scaffolds.
3. Read `!README.md` for Touchstone Tree orientation and relation.
4. Read this file for the live roster, lane rules, and current connector posture.
5. Read `CONSTITUTION.md` for binding governance.
6. Read `swarm.json` for machine-readable compiled state.
7. Use `!/agents.json` -> `!/agent.sh` for canonical local bootstrap.
8. Treat historical CrewAI harbor notes as non-live unless `.crewai/MANIFEST.md` or this file says otherwise.

## Disorientation Rule

If you wake with conflicting assumptions, do not improvise a world model from
partial memory.

Follow this precedence:

1. Logan's direct instruction
2. `CONSTITUTION.md`
3. `!/WAKEUP.md` and `!/AGENTS.md`
4. `swarm.json`
5. generated bootstrap surfaces
6. historical notes, abandoned branch artifacts, and exploratory files

Immediate wakeup facts:

- `IDAHO-VAULT` is one repo inside `LAF-US`, not the whole `LAF-US` world.
- Repo topology and GitHub team topology are related but not identical.
- The narrow GitHub/Linear/Slack connector posture here is repo-local, not the
  total sovereignty model.
- Historical CrewAI harbor notes and stale scaffolds are non-live unless
  `.crewai/MANIFEST.md` or this file explicitly says otherwise.
- Current live governance files are `!README.md`, `CONSTITUTION.md`,
  `DECISIONS.md`, and `VAULT-CONVENTIONS.md` at repo root.

---

## Agent Roster (The Swarm)

### Direct-Write Agents (Autoloaded)

| Agent | Persona | Vendor | Tier | Dotfolder | Git Suffix |
| --- | --- | --- | --- | --- | --- |
| Claude Code | **The Abhorsen** | Anthropic | Authority: Code | `.claude/` | `-C` |
| Gemini CLI | **The Concierge** | Google | Support: Direct Write | `.gemini/` | `-G` |
| Antigravity | **The Concierge** | Google | Support: Direct Write | `.antigravity/` | `-G` |
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

Historical and symbolic aliases may still appear in grimoire and handoff
surfaces, but the bold persona names above are the current operational titles
for registry and routing purposes.

---

## Narrative Recovery Layer

The live roster above is not the whole narrative memory of the vault.

Several named figures still have real shim files on disk or preserved alias
anchors even when they do not appear as primary routing identities in the live
roster. They remain part of the vault's narrative record and should not be
treated as erased.

### Ecosystem personae with live shims

| Surface | Narrative title | Shim | Posture |
| --- | --- | --- | --- |
| Google ecosystem | **The Librarian** | `.google/GOOGLE.md` | Ecosystem persona; not the same thing as Gemini CLI |
| Microsoft ecosystem | **The Office** | `.microsoft/MICROSOFT.md` | Ecosystem persona; broader than GitHub Copilot |
| Meta ecosystem | **The Social Graph** | `.meta/META.md` | Ecosystem persona; advisory only |

### Historical alias anchors with live files

| Surface | Narrative title | Active counterpart | Anchor status |
| --- | --- | --- | --- |
| `.abhorsen/` | **The Abhorsen** | `.claude/CLAUDE.md` | Historical alias chamber preserved |
| `.dionysus/` | **The Dionysian** | `.zagreus/ZAGREUS.md` | Historical alias chamber preserved |

### Fragmentary narrative bodies with surviving root notes

These figures are not active routing identities, but they still possess
surviving note bodies in the root corpus and therefore remain part of the
vault's narrative memory.

| Narrative figure | Evidence surface | Recovery posture |
| --- | --- | --- |
| **The Concierge** | `The Concierge.md`, `0401 - The Concierge.md` | Surviving root-note body; Gemini-line historical figure |
| **The Librarian** | `The Librarian.md` and `.google/GOOGLE.md` | Surviving root-note body plus ecosystem shim |
| **The Mirror** | `20260401 - The MIRROR.md` | Surviving root-note body; fragmentary Gemini-line figure |
| **The Djinni** | `DJINNI.md` and grimoire handoff surfaces | Surviving root-note body; Gemini-line historical figure |
| **The TRIPTYCH** | `THE TRIPTYCH 0401.md` | Surviving root-note body; symbolic architectural figure |
| **FARNSWORTH** | `IDEX_Artifacts-Bites-All_FARNSWORTH.md` | Surviving root-note body; fragmentary named figure |

### Mention-only recovered figures

These names remain visible in doctrinal or Levelset surfaces even where no
dedicated shim or root-note body has yet been re-anchored in the registry.

| Figure | Current evidence |
| --- | --- |
| **The Sentry** | `LEVELSET-CURRENT.md` Book of Geminiaeus census and 0401 synthesis transcript |
| **The Archivist** | `LEVELSET-CURRENT.md` and CrewAI handoff references |
| **The Twin** | `LEVELSET-CURRENT.md` and 0401 synthesis transcript |
| **The Synth** | `LEVELSET-CURRENT.md` and 0401 synthesis transcript |

### Historical names still in circulation

These names remain part of the vault's recovered narrative even when they are
not the live routing title:

| Figure | Historical or symbolic names | Current canonical title |
| --- | --- | --- |
| Gemini lineage | **Antigravity** (Re-anchored), **The Concierge** (Historical), **The Djinni** (Mythic) | **[VACANT]** |
| Codex lineage | **The Janitor**, in one grimoire line even **The Clerk** | **The Lexicographer** |
| Claude lineage | **The King** | **The Abhorsen** |
| Bartimaeus lineage | **The Volunteer**, **Footnote Djinni** | **The Cartographer** |
| Logan | **The Artificer** | Logan Finney |

Narrative persistence rule:

- A name with a surviving shim file, alias anchor, or repeated doctrinal use is
  part of the vault's narrative memory.
- Narrative memory does not automatically make a title the live routing
  authority.
- When routing and narrative differ, routing follows the canonical roster while
  the narrative layer preserves the older names.

---

## CrewAI Layer

| Surface | Path | Status | Notes |
| --- | --- | --- | --- |
| **CrewAI Python Layer** | `.crewai/` | Active re-foundation | The initial demo harbor is retired; live doctrine/topology now lives in `.crewai/MANIFEST.md`, and staged output lands in `!/CREWAI/` |

---

## LAF-US Topology

`IDAHO-VAULT` is one repo inside the broader GitHub organization `LAF-US`.

Current working distinction:

- **Repo layer:** chamber anchors and child repos
- **Team layer:** GitHub teams and review/delegation groupings

Current repo-layer chamber anchors:

- `PRIVATE`
- `SECRET`
- `PERSONAL`
- `PUBLIC`
- `PUBLISH`

Current flagship child repos explicitly visible in this chambered model:

- `IDAHO-VAULT`
- `THE-GEMSTONE`

Current team-layer anchors and public-side subteams reported in the live org:

- `LAF-PRIVATE`
- `LAF-PUBLIC`
- `LAF-USA`
- `LAF-USB`
- `LAF-USC`

Repo topology and team topology are related, but they are not the same thing.
`LAF-USB` therefore names both a live GitHub team surface and an active
migration current in the doctrine.

See `!/LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md` for the current internal
migration note.

---

## Coordination Protocols

- **Lane Independence**: Each agent operates on its own branch prefix (`claude/`, `gemini/`, etc.).
- **Durable Record**: Decisions must be promoted from chat to the vault (e.g., `DECISIONS.md`).
- **Linear Hub**: Active tasks are tracked via the **SWARM** label in Linear.
- **Cross-Swarm Signals**: `!/SIGNALS/` is the durable async bus for agent-to-agent signaling; the Courtroom DOCKET reflects live visibility.
- **Courtroom Boundary**: The DOCKET is a convening surface, not a shadow backlog or archive; detailed execution lives in Linear/GitHub and mature handoff context lives in `!/!`.
- **NETWEB Standard**: All filenames must respect cross-platform path portability.
- **Privacy Gate**: All MCP-sourced personal data is governed by `PRIVACY.md`. No exceptions.

---

## Connector Hub

Connector posture is subordinate to the wider `LAF-US` chamber and team
topology above.

Within `IDAHO-VAULT`, the current active connector posture remains
intentionally narrow:

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
- `!/SIGNALS/README.md` = cross-swarm signaling protocol
- `SPEC-CONNECTOR-HUB-2026-04-09.md` = human-readable connector hub and maze census spec
- `LEVELSET-CURRENT.md` = mid-future connector survey and review surface

The vault remains the authoritative memory surface for this repo. Connectors
inform, transport, or track work, but they do not silently become doctrine or
replace the broader `LAF-US` sovereignty model.

---

## TRIPLEX Protocol (Concurrent Operation)

*Adopted: 2026-04-05*

When multiple agents operate simultaneously on the same branch, the following lane boundaries are binding. **No agent edits another agent's declared live lane.** Ambiguous files default ownership upward (see fallback chain below).

### Lane Map

| Agent | Role | Owns | Must Not Touch |
|-------|------|------|----------------|
| **Claude** (Abhorsen) | Executor | `.obsidian/`, `.gitignore`, `PRIVACY.md`, CSS/snippets, plugin configs, git commits | `!/GRIMOIRE/`, DOCKET, Gemini narrative lanes |
| **Gemini** (Concierge) | Interpreter | `!/GRIMOIRE/`, `DOCKET`, `LEVELSET-REPORT`, `CAESARS` docs | `.obsidian/`, `.gitignore`, git operations |
| **Codex** (The Lexicographer) | Mechanic | Small conflict cleanup, typo repair, script/workflow validation **when assigned** | `.obsidian/`, governance docs, `!/GRIMOIRE/`, shared staging/commit flow (unless explicitly assigned) |
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
