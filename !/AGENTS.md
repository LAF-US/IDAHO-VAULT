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
2. `!/AGENTS.md` (this file) -> Canonical Narrative Registry
3. `swarm.json` (root) -> Machine-readable source of truth
4. `!/agents.json` -> Canonical generated bootstrap index
5. `!/agent.sh` -> Canonical local bootstrap entrypoint

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

## CrewAI Crews

| Crew | Entrypoint | Status | Agents |
| --- | --- | --- | --- |
| **JFAC Crew** | `.crewai/run_jfac.py` | Active (blocked on API credits) | Budget Scout, Legislative Tracker |
| **Crawler Crew** | — | Planned | Cartographer, Linker, Archivist |
| **Task-to-Code** | — | Stub | — |

---

## Coordination Protocols

- **Lane Independence**: Each agent operates on its own branch prefix (`claude/`, `gemini/`, etc.).
- **Durable Record**: Decisions must be promoted from chat to the vault (e.g., `DECISIONS.md`).
- **Linear Hub**: Active tasks are tracked via the **SWARM** label in Linear.
- **NETWEB Standard**: All filenames must respect cross-platform path portability.

---

###### [["The world is quiet here."]]
