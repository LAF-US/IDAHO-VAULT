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
| OpenAI Codex CLI | `.codex/` | `.codex/CODEX.md` | Yes | Config via `.codex/config.toml` |
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

---

## Machine-Readable Registry

See `swarm.json` at repo root for the structured machine-readable registry (agents, personas, systems, protocols).

---

## Governance

All agents are governed by `!/CONSTITUTION.md`. All agents share conventions in `!/VAULT-CONVENTIONS.md`. Logan is human; agents are software. Logan directs; agents execute.
