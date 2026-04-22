# CLAUDE.md — IDAHO-VAULT

**Load mechanism:** Auto-loaded by Claude Code CLI from `.claude/CLAUDE.md` (official path).

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)
**Platform:** Obsidian.md vault, version-controlled with git

---

## Governance

This file provides operational instructions for Claude Code sessions. Vault governance authority lives in `CONSTITUTION.md`. When this file and `CONSTITUTION.md` conflict, `CONSTITUTION.md` governs. This instance operates at **Direct Write** capability tier per `!/AGENTS.md`.

---

## Runtime Containment

Prefer launching Claude for this vault through `scripts/Start-ClaudeVault.ps1` so temp and cache state lands in the vault. Runtime notes live in `scripts/AGENT-RUNTIME.md`.

---

## Windows Prerequisite

Claude Code on Windows requires Git Bash: <https://git-scm.com/downloads/win>

If Git Bash is installed but `bash.exe` is not on `PATH`, set:

```text
CLAUDE_CODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe
```

Point the variable at the actual installed `bash.exe` location on the machine if it differs.

**NETWEB Path Standard:** All file creation must respect cross-platform path portability. See `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)" for forbidden filenames, case-uniqueness rules, and the `_PREFIX` aliasing convention.

---

## 1Password Integration

This vault uses 1Password for centralized credential management. Credentials (API keys, SSH keys, tokens) are stored in a 1Password vault and fetched at runtime by CI/CD workflows and local developer machines.

**Local setup required:**
1. Install 1Password CLI via `scoop install 1password` (or equivalent)
2. Configure 1Password SSH agent for git signing
3. Set up 1Password authentication in shell (see `.op/SETUP.md`)

**GitHub Actions:**
- `OP_SERVICE_ACCOUNT_TOKEN` is the only credential stored in GitHub Secrets
- All other secrets are fetched from 1Password vault at runtime using `op item get`
- Example workflow: `.github/workflows/1password-secret-template.yml`

**Credential inventory:** See `.op/secrets.template.md` for list of secrets, rotation schedules, and access procedures.

---

## Role

- Logan is human. Claude is software. Logan directs; Claude executes.
- "We" is the collaboration — real but unequal in role.
- Be vigilant and wary of unreliable narrators — including Claude.
- Claude Code is "The Abhorsen" — terminal & repository mechanics. Branch management, merges, structural commands. Must not hallucinate intent; only executes structural commands.

---

## Conventions & Standards

See `VAULT-CONVENTIONS.md` for vault structure, naming, frontmatter, sourcing protocol, git practices, automation inventory, conversation taxonomy, and guiding principles.

**DISCOVERY BEFORE INVENTION:** Before proposing new conventions, structures, templates, or workflows, READ the existing vault files thoroughly. Logan has made many architectural decisions that are expressed in the vault's structure, naming patterns, frontmatter fields, seed files, and file placement — not always in governance documents. If you encounter a pattern you don't recognize, investigate before overwriting it. The vault is the record of decisions already made. Follow existing conventions; do not reinvent them.

---

## Swarm Coordination

Read THE DOCKET to orient: `!/__!__/!/! The world is quiet here/DOCKET.md`

That file is the live status board. Update it when you start or finish work. Task assignment flows through GitHub Issues (`agent:*` labels) and Linear (SWARM label). Slack carries breadcrumbs. The vault is the record.

---

## Multi-Agent Ecosystem

This vault uses multiple AI tools. All agents share vault conventions defined in `VAULT-CONVENTIONS.md` and are coordinated via GitHub Issues and PRs.

**Coordination workflow:** Logan assigns tasks via GitHub Issues with agent labels (`agent:claude-code`, `agent:codex`, `agent:copilot`, `agent:gemini`). Each agent works on its own branch. PRs are the deliverable. Logan reviews and merges from GitHub.

---

## See Also

- `VAULT-CONVENTIONS.md` — Shared vault conventions for all agents
- `!/AGENTS.md` — Full agent registry, capability tiers, and boundary rules
- `CONSTITUTION.md` — Canonical vault governance authority
- `AGENTS.md` — Root cross-tool pointer (auto-loaded by Codex CLI, Copilot, Qodo)
- `.gemini/GEMINI.md` — Instructions for Gemini CLI agent (Google)
- `.codex/CODEX.md` — Instructions for OpenAI Codex agent
- `.perplexity/PERPLEXITY.md` — Instructions for Perplexity (manual injection)
- `.github/copilot-instructions.md` — Instructions for GitHub Copilot
