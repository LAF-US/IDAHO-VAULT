# AGENTS.md — THE-GEMSTONE

**Cross-tool pointer.** Auto-loaded by Codex CLI, GitHub Copilot, and Qodo when working in this repository.

**Owner:** Logan Finney
**Repository:** github.com/loganfinney27/THE-GEMSTONE
**Purpose:** Anonymous independent publication about Idaho, built on Quartz v4

---

## Swarm Role

This repository is part of Logan's Unified Swarm (LAF-US / PROJECT HORIZON). It is a publishing repo — content and configuration only. Agents work here to maintain the Quartz site, update automation, and manage content structure under Logan's direction.

---

## Agent Registry

| Agent          | Branch prefix | Role                                             |
| -------------- | ------------- | ------------------------------------------------ |
| GitHub Copilot | `copilot/`    | Inline editing, YAML/frontmatter, config changes |
| Claude Code    | `claude/`     | Structural work, automation, build pipeline      |
| Codex          | `codex/`      | Code tasks, scripting                            |
| Gemini         | `gemini/`     | Research and content support                     |

---

## Coordination

- Logan assigns tasks via GitHub Issues with `agent:*` labels
- Each agent works on its own branch
- PRs are the deliverable — Logan reviews and merges
- Auto-PR workflow creates PRs automatically when agents push to agent branches

---

## Boundaries

- Do not merge without Logan's approval
- Do not alter content under `content/` without explicit direction
- Do not change `quartz.config.ts` `baseUrl` or `theme` without explicit instruction
- Governance authority for this repo rests with Logan

---

## See Also

- `.github/copilot-instructions.md` — GitHub Copilot instructions
- `.claude/CLAUDE.md` — Claude Code instructions
