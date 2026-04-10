---
authority: LOGAN
related:
- API
- CLAUDE
- CLI
- CONSTITUTION
- ChatGPT
- Copilot
- CrewAI
- DECISIONS
- GEMINI
- Gemini CLI
- GitHub
- Idaho
- Idaho Public Television
- Idaho Reports
- LEVELSET
- Logan Finney
- MCP
- OpenAI
- SDK
- The world is quiet here
- VAULT-CONVENTIONS
- 'Yes'
- agent
- blocked
- chain
- codex
---

# AGENTS.md — IDAHO-VAULT

> [!IMPORTANT]
> **This is a cross-tool pointer.** The canonical narrative registry now lives at [!/AGENTS.md](!/AGENTS.md).
> This file exists at repo root because OpenAI Codex CLI, GitHub Copilot, and Qodo auto-load `AGENTS.md` from the repository root.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)

---

## Canonical Registry

Root `AGENTS.md` is the auto-loaded cross-tool entrypoint.
See [!/AGENTS.md](!/AGENTS.md) for the canonical narrative registry: capability tiers, boundary rules, bootstrap rules, and the master agent roster.

The machine-readable source of truth remains `swarm.json`.
The canonical local execution bootstrap chain is `swarm.json` -> `!/agents.json` -> `!/agent.sh`.

## Fresh Agent Boot Order

1. Read this root `AGENTS.md` as a pointer and compatibility surface only.
2. Read `!README.md` for the Touchstone Tree and orienting doctrine.
3. Read `!/AGENTS.md` for the live roster, lane rules, and current connector posture.
4. Read `CONSTITUTION.md` for binding governance.
5. Read `swarm.json` for machine-readable compiled state.
6. Use `swarm.json` -> `!/agents.json` -> `!/agent.sh` for canonical local execution bootstrap.
7. Treat historical CrewAI harbor notes as non-live unless `.crewai/MANIFEST.md` or `!/AGENTS.md` says otherwise.

The current active connector hub is:

- GitHub = execution and transport
- Linear = execution state
- Slack = tertiary paging and breadcrumbs

The full connector classification lives in `!/AGENTS.md`, `swarm.json`, and `SPEC-CONNECTOR-HUB-2026-04-09.md`.

---

## Agent Dotfolders (Quick Reference)

| Agent | Dotfolder | Governance shim | Auto-loaded? | Role |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/` | `.claude/CLAUDE.md` | Yes | **The Abhorsen** (Code Authority) |
| Gemini CLI | `.gemini/` | `.gemini/GEMINI.md` | Yes | **The Vault Advisor** (Support) |
| OpenAI Codex | `.codex/` | `.codex/CODEX.md` | Yes | **The Lexicographer** (Scripting) |
| GitHub Copilot | `.github/` | `.github/copilot-instructions.md` | Yes | **The Clerk** (Admin) |

*Full roster including **Grok**, **Perplexity**, **DeepSeek**, **Serena**, and the **Cartographer** available in the [!/AGENTS.md](!/AGENTS.md) ledger.*

---

## CrewAI Layer (Quick Reference)

| Surface | Path | Status | Notes |
| --- | --- | --- | --- |
| **CrewAI Python Layer** | `.crewai/` | Active re-foundation | Retired demo harbor remains historical; live doctrine/topology is in `.crewai/MANIFEST.md`, and staged output lands in `!/CREWAI/` |

---

## Codex Thread Status

For Codex threads, use status signals instead of prompt-driven archival.

- `CODEX ACTIVE` while work is in progress
- `CODEX PAUSED: awaiting Logan` when Logan action is required
- `CODEX COMPLETE: work finished, no further action pending in this thread. Ready for termination or archive.` when the thread is done

Thread archiving is a manual Logan action. See `.codex/CODEX.md` for the
Codex-specific completion guidance.

---

## OpenAI Docs MCP

Always use the OpenAI developer documentation MCP server if you need to work
with the OpenAI API, ChatGPT Apps SDK, Codex, or OpenAI tooling without Logan
having to explicitly ask.

Codex project config for this lives in `.codex/config.toml`. VS Code agent-mode
config lives in `.vscode/mcp.json`.

---

## Governance & Coordination

Root governance files remain authoritative: `CONSTITUTION.md`, `DECISIONS.md`, `LEVELSET.md`, and `VAULT-CONVENTIONS.md`.

**NETWEB Path Standard:** All filenames must respect cross-platform path portability. See `VAULT-CONVENTIONS.md` for reserved name rules.

---

###### [["The world is quiet here."]]
