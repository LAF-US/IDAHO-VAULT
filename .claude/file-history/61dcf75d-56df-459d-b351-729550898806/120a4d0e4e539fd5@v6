# Plan: Agent Dotfolder Architecture

## Context

Agent instruction files currently live at vault root (`CLAUDE.md`, `GEMINI.md`,
`Perplexity.md`, `Grok.md`). This creates disambiguation collisions with vault
notes (`codex.md`), and doesn't follow the established dotfolder convention
already used by `.git/`, `.github/`, `.obsidian/`, `.claude/`, `.vscode/`, `.qodo/`.

The fix: each AI tool gets its own dotfolder. Files inside are invisible to
Obsidian's note graph, can't collide with vault notes, and each folder can grow
independently (settings, levelsets, context bundles). `!/` becomes the shared
commons all agents draw from — hub-and-spoke.

---

## Official Auto-Load Status (per tool documentation)

| Tool | Dotfolder | Auto-load file | Auto-loaded? |
| --- | --- | --- | --- |
| Claude Code | `.claude/` | `.claude/CLAUDE.md` | Yes — official |
| Gemini CLI | `.gemini/` | `.gemini/GEMINI.md` | Yes — official |
| OpenAI Codex CLI | `.codex/` | `.codex/config.toml` | Yes — official |
| Grok (xAI) | `.grok/` | `.grok/GROK.md` | Claimed — source uncertain |
| GitHub Copilot | `.github/` | `.github/copilot-instructions.md` | Yes — official (already done) |
| Qodo (PR review) | repo root | `.pr_agent.toml` | Yes — official |
| Qodo (test gen) | repo root | `.codiumai.toml` | Yes — official |
| Qodo (agents) | repo root | `agent.toml` + `agents/*.toml` | Yes — official |
| CodeRabbit | repo root | `.coderabbit.yaml` | Yes — official |
| Slack CLI | `.slack/` | `.slack/hooks.json` + `.slack/config.json` | Yes — official CLI |
| Canva CLI | repo root | `canva-app.json` | Yes — official CLI |
| Box CLI | repo root | `box.json` | Yes — official CLI |
| Deepseek | `.deepseek/` | none official | Manual injection |
| Perplexity | `.perplexity/` | none official | Manual injection |
| Microsoft (non-Copilot) | `.microsoft/` | none official | Manual injection |
| Meta AI / Llama | `.meta/` | none official | Manual injection |
| Linear | none | n/a | SaaS only — no local config. Linear Agent (launched 2026-03-24) configured in cloud workspace settings — no dotfolder needed |
| Google Workspace / Gemini web | `.google/` | manual injection shim | No official CLI dotfolder; shim by convention. Covers Gmail, Calendar, Drive, Workspace, Pinpoint, NotebookLM, Gemini web/API |
| Hugging Face | none (project) | n/a | User cache only |
| Fictive personas | `.bartimaeus/` `.zagreus/` `.persephone/` | none | Manual injection |

**Cross-tool standard:** `AGENTS.md` at repo root is auto-loaded by OpenAI Codex,
GitHub Copilot, and Qodo. Currently only `!/AGENTS.md` exists — create a thin
root-level `AGENTS.md` as a pointer.

---

## Capitalization Standard

**All `.md` governance files in agent dotfolders follow the pattern `.[agent]/AGENT.md`** — uppercase, agent name. This matches the existing vault-wide convention (CONSTITUTION.md, VAULT-CONVENTIONS.md, AGENTS.md, CLAUDE.md, GEMINI.md) and the official auto-load filenames already established by Claude Code and Gemini CLI.

Tool-mandated non-md files (e.g., `config.toml`, `hooks.json`, `settings.json`) remain lowercase per their tool's specification.

Root vault notes also use all-caps: `PERPLEXITY.md`, `GROK.md` (rename from mixed-case current filenames).

---

## Folder Structure (target state)

```text
.claude/
  CLAUDE.md          ← moved from root (official auto-load)
  rules/             ← optional: modular rules auto-loaded by Claude Code
  settings.json      ← already exists
  settings.local.json ← already exists

.gemini/
  GEMINI.md          ← moved from root GEMINI.md (official auto-load)
  settings.json      ← stub (Gemini CLI config)

.codex/
  config.toml        ← stub (official Codex CLI config — lowercase per spec)
  CODEX.md           ← governance shim for OpenAI Codex agents

.grok/
  GROK.md            ← governance shim (matches claimed convention)

.deepseek/
  DEEPSEEK.md        ← governance shim (manual injection)

.perplexity/
  PERPLEXITY.md      ← governance shim (source content from root Perplexity.md)

.microsoft/
  MICROSOFT.md       ← governance shim for full Microsoft AI surface.
                        Two identity contexts documented (see section below):
                        Personal account + IPT M365 institutional account.
                        Covers: GitHub Copilot (chat/CLI), Microsoft Copilot
                        (personal + M365), Azure OpenAI, Bing/Copilot in Edge,
                        Copilot Studio, Microsoft 365 apps (Word, Excel, etc.)

.google/
  GOOGLE.md          ← governance shim for Google ecosystem:
                        Gmail, Google Calendar, Google Docs, Google Drive,
                        Google Workspace, Pinpoint, NotebookLM,
                        Gemini (web/API — distinct from Gemini CLI in .gemini/)

.meta/
  META.md            ← governance shim for Meta AI surface:
                        Meta AI (WhatsApp/Instagram/Facebook), Llama models,
                        Meta AI Studio

.bartimaeus/
  BARTIMAEUS.md      ← fictive persona shim (manual injection)

.zagreus/
  ZAGREUS.md         ← fictive persona shim (manual injection)

.persephone/
  PERSEPHONE.md      ← fictive persona shim (manual injection)

.slack/
  SLACK.md           ← governance shim for Slack CLI / Slack AI surface
  hooks.json         ← Slack CLI project hooks (auto-loaded by Slack CLI)
  config.json        ← Slack CLI project config

AGENTS.md            ← NEW at root: thin cross-tool pointer to !/AGENTS.md
                        Human-readable. Auto-loaded by Codex CLI, Copilot, Qodo.
                        REQUIRED at root for cross-tool auto-load — cannot move.
swarm.json           ← NEW: machine-readable structured swarm registry.
                        Covers ALL swarm elements (see section below), not just agents.
                        Used by automation scripts to discover and coordinate swarm.
.pr_agent.toml       ← NEW: Qodo PR review config (auto-loaded)
.codiumai.toml       ← NEW: Qodo test generation config (auto-loaded)
.coderabbit.yaml     ← NEW: CodeRabbit review config (auto-loaded)
canva-app.json       ← NEW: Canva CLI app config (if Canva CLI used)
box.json             ← NEW: Box CLI config (if Box CLI used)
```

---

## Root Cleanup

Root `.md` files become **vault notes about the agents** (not agent directions). The operational instruction content moves into the dotfolder. The root file is repurposed/rewritten as a vault entry — so wikilinks like `[[CLAUDE]]`, `[[GEMINI]]`, `[[Perplexity]]` remain valid in the Obsidian graph.

| File | Action | Reason |
| --- | --- | --- |
| `CLAUDE.md` | Repurpose as vault note; copy content to `.claude/CLAUDE.md` | Root = Obsidian entity note about Claude persona; dotfolder = operational shim |
| `GEMINI.md` | Repurpose as vault note; copy content to `.gemini/GEMINI.md` | Same pattern |
| `Perplexity.md` → `PERPLEXITY.md` | `git mv` rename + repurpose as vault note; copy content to `.perplexity/PERPLEXITY.md` | All-caps standard; root = entity note |
| `Grok.md` → `GROK.md` | `git mv` rename + expand from empty stub into minimal vault note | Currently 0 bytes — add frontmatter + entity description |
| `codex.md` | Leave untouched | Existing vault note (DEFINE / terms) — not an agent file |
| `CLAUDE 1.md` / `CLAUDE 2.md` | Flag for Logan | Archive copies — Logan decides keep/move to `!/` |

### Vault note content (root files after repurpose)

Each repurposed root file gets:

- YAML frontmatter: `tags: [agents, ai]` + role alias
- One paragraph: who this agent is in the vault, what it does, capability tier
- Wikilinks to `[[CONSTITUTION]]`, `[[AGENTS]]`, related agent notes
- No operational instructions (those live in the dotfolder)
- A pointer: `Operational instructions: see [.agentname/filename]`

This preserves the Obsidian graph (all existing `[[CLAUDE]]` wikilinks stay valid) while cleanly separating vault-note identity from agent operational config.

---

## Swarm Registry Framework — `AGENTS.md` + `swarm.json`

### Why two formats

`AGENTS.md` (markdown) and `swarm.json` (structured) serve different consumers:

| File | Consumer | Purpose |
| --- | --- | --- |
| `AGENTS.md` (root) | Humans + AI tools (Codex CLI, Copilot, Qodo auto-load) | Human-readable cross-tool pointer; must stay at root |
| `!/AGENTS.md` | Humans + any agent reading `!/` commons | Canonical narrative agent registry with capability tiers |
| `swarm.json` (root) | Automation scripts, GitHub Actions, future tooling | Machine-readable structured registry of ALL swarm elements |

### `swarm.json` schema — all swarm elements

The swarm has four element types. `swarm.json` indexes all of them:

```json
{
  "agents": [
    {
      "id": "claude-code",
      "name": "Claude Code",
      "dotfolder": ".claude",
      "autoload_file": ".claude/CLAUDE.md",
      "autoload": true,
      "capability_tier": "Direct Write",
      "role": "The Abhorsen — terminal & repository mechanics",
      "label": "agent:claude-code"
    },
    {
      "id": "linear-agent",
      "name": "Linear Agent",
      "dotfolder": null,
      "autoload_file": null,
      "autoload": false,
      "config": "cloud — configured in Linear workspace settings",
      "capability_tier": "Advisory",
      "role": "Linear workspace AI — context synthesis, issue creation, status tracking",
      "launched": "2026-03-24",
      "label": null,
      "notes": "No local dotfolder. Access via Cmd+J, Slack, Teams, @mentions in Linear."
    }
  ],
  "personas": [
    {
      "id": "bartimaeus",
      "name": "Bartimaeus",
      "dotfolder": ".bartimaeus",
      "autoload": false,
      "role": "TBD — pending Logan's direction"
    }
  ],
  "systems": [
    {
      "id": "github",
      "name": "GitHub",
      "type": "coordination",
      "url": "https://github.com/loganfinney27/IDAHO-VAULT",
      "role": "Code hosting, PRs, Issues, Actions",
      "integrations": ["linear"]
    },
    {
      "id": "linear",
      "name": "Linear",
      "type": "coordination",
      "role": "Execution tracking, owners, deadlines (SWARM label)",
      "config": "cloud-only — no local dotfolder",
      "github_sync": "Bidirectional: PR lifecycle drives issue state (In Progress → In Review → Done). Branch naming or magic words (e.g. closes ENG-123) link PRs to issues.",
      "ai_agent": "Linear Agent (launched 2026-03-24) — configured in Linear workspace settings, not repo files. Access via Cmd+J, Slack, Teams, @mentions."
    },
    {
      "id": "slack",
      "name": "Slack",
      "type": "coordination",
      "role": "Ephemeral coordination — breadcrumbs only"
    },
    {
      "id": "obsidian-sync",
      "name": "Obsidian Sync",
      "type": "sync",
      "role": "Private courier for plugin settings and credentials across devices"
    }
  ],
  "protocols": [
    {
      "id": "levelset",
      "name": "LEVELSET",
      "version": "3.2.6.1",
      "file": "!/LEVELSET-STEP-0-EXTERNAL-AGENT.md",
      "status": "active"
    },
    {
      "id": "arise",
      "name": "ARISE",
      "version": "0.0",
      "file": null,
      "status": "awaiting adoption"
    }
  ]
}
```

**`AGENTS.md` at root stays a thin human pointer** — it does not duplicate `!/AGENTS.md` content. `swarm.json` is the machine layer. Scripts currently discovering paths by convention (e.g., `classify_paths.py`) can eventually read `swarm.json` instead of hardcoding.

---

## File Contents

### Standard shim structure (all non-auto-load files)

Every `instructions.md` / `GROK.md` / etc. follows the 6-block pattern:

1. **Load mechanism** — honest auto-load OR manual injection statement
2. **Identity header** — owner / repo / platform
3. **Governance** — defers to `!/CONSTITUTION.md`; declares capability tier
4. **Role** — agent persona, one paragraph
5. **Conventions pointer** — `See !/VAULT-CONVENTIONS.md`
6. **See Also** — flat list pointing to `!/` commons

Target: 30–45 lines per file.

### `.codex/config.toml` stub

```toml
# OpenAI Codex CLI project configuration
# See https://developers.openai.com/codex/config-reference
# Governance shim: .codex/instructions.md
# Shared conventions: !/VAULT-CONVENTIONS.md
```

### `.gemini/settings.json` stub

```json
{
  "// governance": "See .gemini/GEMINI.md and !/CONSTITUTION.md"
}
```

### `.microsoft/instructions.md` — Two-context design

Logan operates under **two distinct Microsoft identities**. The shim documents both explicitly so any Microsoft-surface agent knows which context is active:

| Context | Identity | Governed by | Copilot tier |
| --- | --- | --- | --- |
| **Personal** | Logan's personal Microsoft account | Logan's own preferences | Microsoft Copilot (consumer) |
| **Institutional** | Idaho Public Television M365 tenant | IPT IT policy | Microsoft 365 Copilot (enterprise) |

**What this means operationally:**

- Personal account: Logan controls all settings, data stays in personal OneDrive, no institutional audit trail
- IPT M365 account: Subject to IPT IT policy, data residency rules, Copilot features may be restricted or different by tenant configuration — Logan cannot assume same permissions as personal
- GitHub Copilot: Separate developer subscription linked to Logan's personal GitHub account (`loganfinney27`) — not IPT-managed
- Azure OpenAI: API access under Logan's subscription — personal context unless IPT-provisioned

**Practical rule in the shim:** When Logan says "work context" = IPT M365 institutional. When Logan says "personal" = consumer account. If ambiguous, ask before acting on any M365-scoped task.

One file handles both. No need to split into two dotfolders — the shim just documents context-switching explicitly.

### `.meta/instructions.md`

Governance shim for Meta AI products. Follows standard 6-block pattern.
Role: "The Social Graph" — Meta AI access via WhatsApp/Instagram/Facebook
integrations and Llama model deployments. Read/advisory only unless Logan
directs otherwise.

### Fictive personas

`.bartimaeus/`, `.zagreus/`, `.persephone/` get `instructions.md` stubs with
role TBD by Logan. Placeholder content:

```markdown
# [NAME] — IDAHO-VAULT

**Load mechanism:** Manual injection by Logan.
[...]
**Role:** [Pending Logan's direction — persona not yet formally defined.]
```

---

## Gitignore

**Rule:** IDE/runtime dotfolders are ignored. Agent governance dotfolders are tracked.

| Folder | Status | Action |
| --- | --- | --- |
| `.vscode/` | Already gitignored (line 14) | None |
| `.qodo/` | Agentic tool workspace — empty currently, not in `.gitignore` | Track (agentic, not runtime); no change needed |
| `.venv/` | Already gitignored | None |
| `.gemini/`, `.codex/`, `.grok/`, etc. | New governance folders | Must be tracked — verify no wildcard catches them |
| `.slack/` | Slack CLI project config | Track (governance/config, not runtime) |

No existing `.gitignore` wildcard rule will catch the new agent folders. The
`.gitignore` ignores named folders explicitly, not by pattern. Safe to proceed.

---

## Execution Order

1. `git mv CLAUDE.md .claude/CLAUDE.md` (repurpose root as vault note)
2. `git mv GEMINI.md .gemini/GEMINI.md` (repurpose root as vault note) + create `.gemini/settings.json`
3. `git mv Perplexity.md PERPLEXITY.md` then create `.perplexity/PERPLEXITY.md` (governance shim)
4. `git mv Grok.md GROK.md` (expand to vault note) + create `.grok/GROK.md` (governance shim)
5. Create remaining new dotfolders + governance shims:
   `.codex/`, `.deepseek/`, `.microsoft/`, `.google/`,
   `.bartimaeus/`, `.zagreus/`, `.persephone/`, `.meta/`
6. Create `.slack/` stubs
7. Create root-level config stubs: `AGENTS.md`, `swarm.json`, `.pr_agent.toml`,
   `.codiumai.toml`, `.coderabbit.yaml`, `canva-app.json`, `box.json`
8. Flag `CLAUDE 1.md` / `CLAUDE 2.md` to Logan before touching
9. Single commit on `claude/agent-dotfolder-architecture` branch

---

## Files Modified / Created

| Path | Status |
| --- | --- |
| `.claude/CLAUDE.md` | Moved from `CLAUDE.md` |
| `.gemini/GEMINI.md` | Moved from `GEMINI.md` |
| `.gemini/settings.json` | New stub |
| `.codex/config.toml` | New stub |
| `.codex/CODEX.md` | New governance shim |
| `.grok/GROK.md` | New governance shim |
| `.deepseek/DEEPSEEK.md` | New governance shim |
| `.perplexity/PERPLEXITY.md` | Source content from `Perplexity.md` |
| `.google/GOOGLE.md` | New governance shim (Gmail, Calendar, Docs, Drive, Workspace, Gemini web/API) |
| `.microsoft/MICROSOFT.md` | New governance shim (Copilot personal + M365, Azure OpenAI, Bing, Copilot Studio) |
| `.meta/META.md` | New governance shim (Meta AI, Llama, Meta AI Studio) |
| `.slack/SLACK.md` | New governance shim (Slack AI / Slack CLI surface) |
| `.bartimaeus/BARTIMAEUS.md` | New stub (role TBD by Logan) |
| `.zagreus/ZAGREUS.md` | New stub (role TBD by Logan) |
| `.persephone/PERSEPHONE.md` | New stub (role TBD by Logan) |
| `AGENTS.md` (root) | New — thin pointer to `!/AGENTS.md` (human-readable; auto-load required) |
| `swarm.json` (root) | New — machine-readable structured registry (agents, personas, systems, protocols) |
| `.slack/hooks.json` | New stub — Slack CLI project hooks |
| `.slack/config.json` | New stub — Slack CLI project config |
| `.pr_agent.toml` | New stub — Qodo PR review config |
| `.codiumai.toml` | New stub — Qodo test generation config |
| `.coderabbit.yaml` | New stub — CodeRabbit review config |
| `canva-app.json` | New stub — Canva CLI (stub only; activate if CLI used) |
| `box.json` | New stub — Box CLI (stub only; activate if CLI used) |
| `CLAUDE.md` (root) | Repurposed as vault note (entity note about Claude persona) |
| `GEMINI.md` (root) | Repurposed as vault note (entity note about Gemini persona) |
| `Perplexity.md` → `PERPLEXITY.md` (root) | Renamed (git mv) + repurposed as vault note |
| `Grok.md` → `GROK.md` (root) | Renamed (git mv) + expanded to minimal vault note |

---

## Open Questions for Logan

1. **`CLAUDE 1.md` / `CLAUDE 2.md`** at root — archive copies of old CLAUDE.md.
   Delete or move to `!/` archive?
2. **Fictive persona roles** — `.bartimaeus/`, `.zagreus/`, `.persephone/` stubs
   will have placeholder role text. Logan should define canonical roles before
   or after this PR.
3. **`.meta/` role** — assigned "The Social Graph" as placeholder. Logan should
   confirm or redefine before or after this PR.
4. **`.grok/` auto-load status** — the official xAI Grok (the LLM) has no
   confirmed CLI dotfolder convention. The `.grok/GROK.md` claim came from a
   community project. Treat as manual injection until confirmed otherwise.
5. **`swarm.json` scope** — Plan now includes `swarm.json` (expanded from agents-only
   to all four element types: agents, personas, systems, protocols). Schema stub
   included in plan. Should the full schema be authored in this PR, or just a
   minimal skeleton with agents populated and other sections stubbed?
   **Logan's call: full schema now vs minimal skeleton?**
