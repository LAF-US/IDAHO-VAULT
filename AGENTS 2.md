---
title: AGENTS
updated: 2026-04-02
status: active
authority: LOGAN
date created: Thursday, April 2nd 2026, 10:26:08 pm
date modified: Thursday, April 2nd 2026, 11:44:55 pm
related:
- '2026-04-02'
- AGENTS
- Anthropic
- CLAUDE
- CLI
- CONSTITUTION
- Copilot
- DECISIONS
- GEMINI
- GROK
- Gemini CLI
- GitHub
- LEVELSET
- LOGAN
- OpenAI
- PERPLEXITY
- PERSEPHONE
- VAULT-CONVENTIONS
- ZAGREUS
- agent
- chain
- codex
- coordination
- doctrine
- index
- infrastructure
- persona
---
# AGENTS - IDAHO-VAULT

This is the canonical narrative registry for the vault's agent layer.
It explains the roster, the authority chain, and the local bootstrap model that other tools should follow.

## Authority Chain

1. Root `AGENTS.md` is the auto-loaded cross-tool pointer.
2. This file is the canonical narrative registry.
3. `swarm.json` is the machine-readable source of truth.
4. `!/agents.json` is the generated bootstrap index for local shell use.
5. `!/agent.sh` is the canonical local bootstrap entrypoint.
6. Root `agent.sh` and root `agents.json` are compatibility surfaces for one transition cycle.

## Governance Anchors

The doctrine layer remains at repo root:

- `CONSTITUTION.md`
- `DECISIONS.md`
- `LEVELSET.md`
- `VAULT-CONVENTIONS.md`

The matching `!/` files for those documents are routing shims so older references and bootstrap-required context paths stay stable.

## Bootstrap-Capable Agents

These agents have generated records in `!/agents.json` and can be addressed through `!/agent.sh`.

| Invoke as | Agent | Dotfolder | Capability tier | Instructions | Notes |
| --- | --- | --- | --- | --- | --- |
| `claude` | Claude Code | `.claude/` | Direct Write | `.claude/CLAUDE.md` | Official Anthropic terminal agent |
| `codex` | OpenAI Codex CLI | `.codex/` | Direct Write (scripting) | `.codex/CODEX.md` | Root `AGENTS.md` auto-loads; `.codex/CODEX.md` is the repo-specific reference shim |
| `copilot` | GitHub Copilot | `.github/` | Multi-Repo Admin | `.github/copilot-instructions.md` | Official GitHub path |
| `gemini` | Gemini CLI | `.gemini/` | Direct Write (Support) | `.gemini/GEMINI.md` | Tier 1 support lane; PR-mediated writes only |
| `grok` | Grok | `.grok/` | Read/Analysis | `.grok/GROK.md` | Manual injection surface |
| `perplexity` | Perplexity | `.perplexity/` | Read/Analysis | `.perplexity/PERPLEXITY.md` | Research-first sidecar |

## Manual Or Non-Bootstrap Surfaces

These surfaces remain part of the registry, but they are not currently in the local bootstrap chain:

- `.deepseek/DEEPSEEK.md`
- `.microsoft/MICROSOFT.md`
- `.google/GOOGLE.md`
- `.meta/META.md`
- `.slack/SLACK.md`
- `.bartimaeus/BARTIMAEUS.md`
- `.zagreus/ZAGREUS.md`
- `.persephone/PERSEPHONE.md`
- Linear cloud agent (workspace-native, no local dotfolder)

Use `swarm.json` for the full machine-readable roster, ecosystem blocks, and control-plane roles.

## Boundary Rules

- Persona-specific dotfolders are protected infrastructure. They are not cleanup targets.
- An agent should modify only its own persona dotfolder unless Logan explicitly directs otherwise.
- `.github/` is shared automation infrastructure. It is intentional, protected, and governed separately from persona folders.
- Root-flat notes are intentional. Do not mass-move them just because they are at repo root.
- Slack is breadcrumb-only. Durable coordination belongs in the vault, GitHub, and Linear.

## Thread Status Signals

For Codex threads, use status signals instead of prompt-driven archival:

- `CODEX ACTIVE` while work is in progress
- `CODEX PAUSED: awaiting Logan` when Logan action is required
- `CODEX COMPLETE: work finished, no further action pending in this thread. Ready for termination or archive.`

## Local Bootstrap Usage

Canonical entrypoint:

```bash
source !/agent.sh codex
source !/agent.sh --describe claude
source !/agent.sh --validate copilot
```

Compatibility entrypoint:

```bash
source ./agent.sh codex
source ./agent.sh --describe gemini
```

## Control-Plane Roles

- GitHub: execution transport
- Linear: active coordination
- Slack: breadcrumb only
- Hugging Face: research sidecar, read-only for this lane

The vault is the record. Logan decides. Agents execute inside these boundaries.
