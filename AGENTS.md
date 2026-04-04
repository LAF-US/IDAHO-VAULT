# AGENTS.md — IDAHO-VAULT

> **This is a cross-tool pointer.** The canonical agent registry lives at `!/AGENTS.md`.
> This file exists at repo root because OpenAI Codex CLI, GitHub Copilot, and Qodo auto-load `AGENTS.md` from the repository root.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)

---

## Canonical Registry

Root `AGENTS.md` is the auto-loaded cross-tool entrypoint.
See `!/AGENTS.md` for the canonical narrative registry: capability tiers, boundary rules, bootstrap rules, and agent roster.

The machine-readable source of truth remains `swarm.json`.
The canonical local bootstrap chain is `!/AGENTS.md` -> `swarm.json` -> `!/agents.json` -> `!/agent.sh`.
Root `agent.sh` and root `agents.json` remain temporary compatibility surfaces.

---

## Agent Dotfolders (quick reference)

| Agent | Dotfolder | Governance shim | Auto-loaded? | Notes |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/` | `.claude/CLAUDE.md` | Yes | Official path. On Windows, Claude Code requires Git Bash; if `bash.exe` is not on `PATH`, set `CLAUDE_CODE_GIT_BASH_PATH` to the installed `bash.exe`. |
| Gemini CLI | `.gemini/` | `.gemini/GEMINI.md` | Yes | Official path |
| OpenAI Codex CLI | `.codex/` | `.codex/CODEX.md` | Yes | Root `AGENTS.md` auto-loads; project config via `.codex/config.toml` |
| GitHub Copilot | `.github/` | `.github/copilot-instructions.md` | Yes | Official path |
| Grok (xAI) | `.grok/` | `.grok/GROK.md` | No | Manual injection |
| DeepSeek | `.deepseek/` | `.deepseek/DEEPSEEK.md` | No | Manual injection |
| Perplexity | `.perplexity/` | `.perplexity/PERPLEXITY.md` | No | Manual injection |
| Microsoft AI | `.microsoft/` | `.microsoft/MICROSOFT.md` | No | Manual injection |
| Google ecosystem | `.google/` | `.google/GOOGLE.md` | No | Manual injection |
| Meta AI / Llama | `.meta/` | `.meta/META.md` | No | Manual injection |
| Slack AI / Slack CLI | `.slack/` | `.slack/SLACK.md` | No | Via Slack CLI hooks |
| Bartimaeus (fictive) | `.bartimaeus/` | `.bartimaeus/BARTIMAEUS.md` | No | Manual injection |
| Zagreus (fictive) | `.zagreus/` | `.zagreus/ZAGREUS.md` | No | Manual injection |
| Persephone (fictive) | `.persephone/` | `.persephone/PERSEPHONE.md` | No | Manual injection |
| **Serena** | `.serena/` | `.serena/SERENA.md` | No | MCP server — semantic code intelligence; symbol nav, codebase analysis, refactoring; added 2026-04-04 |

## CrewAI Crews (quick reference)

| Crew | Entrypoint | Status | Agents | Notes |
| --- | --- | --- | --- | --- |
| **JFAC Crew** | `.crewai/run_jfac.py` | Active (blocked on API credits) | Budget Scout, Legislative Tracker, H911 Parser | MAP 3:5, ATT to 5Ws |
| **Crawler Crew** | — | Planned | Cartographer, Linker, Archivist | Post-CHAINFIRE vault mapping; Cartographer candidate: Bartimaeus |
| **Task-to-Code Bridge** | — | Stub | — | `.crewai/crews/task_to_code_crew.py` |
| **Vault Custodian** | — | Stub | — | `.crewai/crews/vault_custodian_crew.py` |
| **Sentinel Crew** | — | Stub | — | `.crewai/crews/sentinel_crew.py` |

Crew manifest: `.crewai/manifest.json`. Output staging: `!/CREWAI/`. Protocol: `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md`.

Persona-specific dotfolders in this table are protected infrastructure. They
are not implicit cleanup targets, even when they look empty or contain only a
shim file. An agent should modify only its own persona dotfolder unless Logan
explicitly directs otherwise. `.github/` is shared automation infrastructure:
also intentional, also not a cleanup target, but governed separately by the
canonical boundary rules in `!/AGENTS.md`.

For Codex specifically, the repo/root `AGENTS.md` is the primary auto-loaded
instruction source. `.codex/config.toml` provides project-scoped Codex config,
and `.codex/CODEX.md` is a Codex-specific reference shim rather than the
primary auto-loaded instructions file.

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

## Machine-Readable Registry

See `swarm.json` at repo root for the structured machine-readable registry (agents, personas, systems, protocols).

---

## Governance

Root governance files remain authoritative: `CONSTITUTION.md`, `DECISIONS.md`, `LEVELSET.md`, and `VAULT-CONVENTIONS.md`.
The matching `!/` files are stable routing shims for bootstrap and legacy references.
Logan is human; agents are software. Logan directs; agents execute.

**NETWEB Path Standard:** All agents creating files must respect cross-platform path portability. See `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)" for reserved filenames, case-uniqueness, and the `_PREFIX` aliasing convention. CI enforces this via `check-portable-paths.yml`.
