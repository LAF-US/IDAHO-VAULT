# AGENTS.md — IDAHO-VAULT

> **This is a cross-tool pointer.** The canonical agent registry lives at `!/AGENTS.md`.
> This file exists at repo root because OpenAI Codex CLI, GitHub Copilot, and Qodo auto-load `AGENTS.md` from the repository root.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)

---

## Canonical Registry

See `!/AGENTS.md` for the full agent registry: capability tiers, boundary rules, and agent roster.

---

## Agent Dotfolders (quick reference)

| Agent | Dotfolder | Governance shim | Auto-loaded? | Notes |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/` | `.claude/CLAUDE.md` | Yes | Official path |
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

All agents are governed by `!/CONSTITUTION.md`. All agents share conventions in `!/VAULT-CONVENTIONS.md`. Logan is human; agents are software. Logan directs; agents execute.
