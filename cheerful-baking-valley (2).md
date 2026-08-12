# Plan: Restructure PLUGIN-REGISTRY.md Using CrewAI MANIFEST Pattern

## Context

The flat plugin inventory at `!/PLUGIN-REGISTRY.md` was created this session but lacks architectural structure. Logan pointed to the CrewAI MANIFEST.md (`.crewai/MANIFEST.md`) as the model for how the registry should be structured. Two goals:

1. **Use MANIFEST.md's architecture** — layer boundaries, layered model, live topology, promotion rules, writable surfaces
2. **Add CrewAI as a dependency** in the plugin ecosystem — the MCP bridge connects the Obsidian plugin layer to the CrewAI agent layer

## The CrewAI MANIFEST Pattern (model)

From `.crewai/MANIFEST.md`:
- **Layer boundaries table** — what surface controls what, who's authoritative
- **Layered model** — CANON/DRIVE/RUNTIME/ARCHIVE with clear promotion rules
- **Live topology** — active components with paths, purposes, statuses
- **Writable surfaces** — what lives where, persistence class (durable/ephemeral)
- **Promotion rules** — numbered rules for how something enters/exits canon
- **Durable doctrines** — standing principles

From `agents.yaml` / `tasks.yaml` / `crew.py`:
- Declarative config (YAML) + runtime wiring (Python)
- Each agent has: role, goal, backstory
- Each task has: description, expected_output, agent assignment

## Restructured PLUGIN-REGISTRY.md

Rewrite `!/PLUGIN-REGISTRY.md` with these sections:

### 1. Layer Boundaries

| Surface | Role | Authority |
|---|---|---|
| `!/PLUGIN-REGISTRY.md` | Live doctrine — authoritative plugin state | Current truth |
| `.obsidian/community-plugins.json` | Runtime enabled list | Derives from registry |
| `.obsidian/plugins/*/manifest.json` | Plugin code + metadata | Installed on disk |
| `.obsidian/plugins/*/data.json` | Plugin settings | Local-only (gitignored), Sync E2E encrypted |
| `LEVELSET-CURRENT.md` | Ecosystem snapshot | Derives from registry |
| `!/VAULT-CONVENTIONS.md` § Sync | Sync boundary rules | Cross-cutting governance |

### 2. Layered Model (replacing flat ENABLED/DORMANT)

| Layer | Meaning | Promotion Rule |
|---|---|---|
| **ESSENTIAL** | Cannot be disabled without breaking vault infrastructure | Requires Logan + architectural review |
| **ACTIVE** | Enabled, serving a documented purpose | Demotion requires rationale logged here |
| **DORMANT** | Installed, not enabled, decision pending | Promote to ACTIVE or demote to RETIRED — Logan decides |
| **RETIRED** | Marked for removal, directory can be deleted | Removal logged here; no agent reinstalls without Logan |

### 3. Live Topology

Restructure the plugin tables by layer (ESSENTIAL/ACTIVE/DORMANT/RETIRED) instead of flat alphabetical. Each entry includes:
- Plugin ID, name, version, size
- **Role** (like crewAI agent role)
- **Purpose** (like crewAI agent goal)
- **Depends on** (upstream plugins)
- **Depended on by** (downstream plugins/systems)

### 4. Cross-Layer Dependency Tree

The full dependency chain from Obsidian plugins through to CrewAI:

```
OBSIDIAN PLUGIN LAYER
  obsidian-local-rest-api (REST API server)
    └── mcp-tools (MCP bridge to Claude Desktop)
         └── CLAUDE DESKTOP / CLAUDE CODE
              └── CREWAI LAYER (.crewai/)
                   └── crews, agents, tasks (src/idaho_vault/)

  breadcrumbs (zettelkasten navigation)
    └── related: frontmatter (vault-wide)

  dataview (inline queries)
    └── vault notes with dataview blocks

  templater-obsidian
    └── ai-templater (AI extension)

  smart-connections
    └── smart-connections-visualizer

  periodic-notes
    └── roygbiv-day-accent
```

### 5. Tracking Surfaces (replaces flat "Sync Storage Impact")

| Surface | Tracks | Persistence | Size Impact |
|---|---|---|---|
| Git (GitHub/LAF-US) | Plugin code (main.js, manifest.json) | Durable, LFS for binaries | 171 MB in `.obsidian/plugins/` |
| Git `.gitignore` | Excludes `data.json` | — | Firewall |
| Obsidian Sync (LAF-US vault) | Plugin code + settings IF "Installed community plugins: ON" | E2E encrypted remote | Counts against 1 GB |
| Local filesystem | Everything | Ephemeral per device | Full 171 MB on disk |

### 6. Promotion/Demotion Rules

1. No plugin moves between layers without updating this registry
2. No agent enables/disables plugins without logging the change here
3. ESSENTIAL plugins require architectural review before any change
4. DORMANT plugins have a "Logan's Decision" field — PENDING until Logan rules
5. RETIRED plugins are deleted in a separate commit with rationale logged
6. New installations require a registry entry BEFORE `git add`

### 7. Activity Log

Append-only log of every plugin state change, who did it, when, why.

## Files to Modify

| File | Change |
|---|---|
| `!/PLUGIN-REGISTRY.md` | Restructure from flat inventory to MANIFEST-pattern layered registry |
| `.crewai/manifest.json` | Fix stale `loganfinney27` URL → `LAF-US` |

## Verification

- Every enabled plugin in `community-plugins.json` has a matching ESSENTIAL or ACTIVE entry in the registry
- Every directory in `.obsidian/plugins/` has a matching entry in the registry
- Dependency tree is accurate (no broken links)
- CrewAI layer appears in the cross-layer dependency tree
- Activity log has the 2026-04-12 creation entry
