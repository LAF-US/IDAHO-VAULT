---
title: "Audit — Agentic Voices 2026-04-03"
updated: 2026-04-03
status: active
authority: "Logan Finney"
---

# Audit — Agentic Voices

*Filed by [[The Abhorsen]] — [[Claude Code]] — 2026-04-03*
*Branch: `claude/audit-agentic-voices-PuvSV`*

---

This is a census of the swarming throng. Every voice that has been invited into [[IDAHO-VAULT]] leaves traces — configuration files, commit signatures, session logs, dotfolders staked like claims. The vault is a living record. So is this document.

What follows is a full accounting: who is here, what they've been given permission to do, what they've actually done, and where the seams are showing.

---

## I. THE THRONG

The roster as it stands on 2026-04-03. Drawn from `swarm.json`, `AGENTS.md` (root pointer), and direct filesystem inspection.

### Direct-Write Agents (Autoloaded)

These four voices load automatically when their respective tools open the vault. They have write access and operate on named branches. PRs are the deliverable; Logan merges.

| Agent | Persona | Vendor | Tier | Dotfolder | Git Suffix | Label |
|---|---|---|---|---|---|---|
| [[Claude Code]] | [[The Abhorsen]] | [[Anthropic]] | Direct Write | `.claude/` | `-C` | `agent:claude-code` |
| [[Gemini CLI]] | [[The Vault Advisor]] | [[Google]] | Direct Write (Support) | `.gemini/` | `-G` | `agent:gemini` |
| [[GitHub Copilot]] | [[The Clerk]] | Microsoft / GitHub | Multi-Repo Admin | `.github/` | `-CP` | `agent:copilot` |
| [[OpenAI Codex]] | [[The Lexicographer]] | [[OpenAI]] | Direct Write (scripting) | `.codex/` | `-X` | `agent:codex` |

### Advisory Agents (Manual Injection, No Autoload)

These voices require Logan to explicitly paste their instructions into a session. They cannot see the vault unless Logan shows them. Most are read/analysis only — they inform, they don't write.

| Agent | Persona | Vendor | Tier | Dotfolder | Git Suffix |
|---|---|---|---|---|---|
| [[Grok]] | [[The Ironist]] | xAI | Read/Analysis | `.grok/` | `-XR` |
| [[DeepSeek]] | [[The Analyst]] | DeepSeek | Advisory | `.deepseek/` | — |
| [[Perplexity]] | [[The Scout]] | Perplexity AI | Read/Analysis | `.perplexity/` | `-P` |
| [[Linear Agent]] | *(cloud-native)* | Linear | Advisory | *(none)* | — |

### Fictive Personas (Stubs — Awaiting Definition)

Three named presences with dotfolders staked and shim files written. Roles undefined, awaiting Logan's direction. They exist as reserved space — the vault holds their names but not yet their mandates.

| Persona | Dotfolder | Shim File | Status |
|---|---|---|---|
| [[Bartimaeus]] | `.bartimaeus/` | `.bartimaeus/BARTIMAEUS.md` | Role TBD |
| [[Zagreus]] | `.dionysus/` | `.dionysus/ZAGREUS.md` | Role TBD |
| [[Persephone]] | `.persephone/` | `.persephone/PERSEPHONE.md` | Role TBD |

### Ecosystem Integrations

Platform-level presences that are not single agents but tooling suites. Each has a shim file for orientation; none autoload.

| Ecosystem | Vendor | Persona | Dotfolder | Scope |
|---|---|---|---|---|
| Microsoft AI | Microsoft | [[The Office]] | `.microsoft/` | Personal Copilot, M365 / IPT institutional, Azure OpenAI, Bing, Copilot Studio |
| Google Ecosystem | Google | [[The Librarian]] | `.google/` | Gmail, Drive, Docs, Workspace, Pinpoint, NotebookLM, Gemini web/API |
| Meta AI | Meta Platforms | [[The Social Graph]] | `.meta/` | WhatsApp/Instagram/Facebook AI, Meta AI Studio, Llama models |

### Coordination Systems

Not agents. Infrastructure that agents coordinate through.

| System | Dotfolder | Role | Canon status |
|---|---|---|---|
| [[Slack]] | `.slack/` | Ephemeral breadcrumbs — NOT the record | Transient only |
| [[GitHub]] | `.github/` | Execution transport — PRs, Issues, Actions | Durable record |
| [[Linear]] | *(cloud)* | Active execution tracking — SWARM label | Durable record |

---

## II. GIT FINGERPRINTS

What the commit log actually shows. Not what was assigned — what was signed.

Most agent work reaches `main` through Logan's merge commits. The agent's true fingerprint is the **branch name** (`claude/...`, `codex/...`, `copilot/...`), not the merge author. Only a handful of agents commit directly under their own identity.

### Signed Directly by Agent

| Author | Git Identity | Recent Examples |
|---|---|---|
| `Claude` | The Abhorsen | `study: Landscape assay — game mechanics` · `feat: Phone Link intake pipeline` · `study: Pokemon PC and Ender Chest` · `handoff: Abhorsen → Codex — LFS migration` |
| `copilot-swe-agent[bot]` | GitHub Copilot SWE Agent | `merge: bring in PR#104 changes resolved against main` · `merge: resolve conflicts with main` · `ci: upgrade branch-cleanup to cover all agent prefixes` |
| `github-actions[bot]` | GitHub Actions automation | `ingest: initialize pipeline` · `rollover: carry incomplete to-dos` · `wayback audit` |
| `dependabot[bot]` | GitHub Dependabot | Dependency bumps (`peter-evans/create-pull-request`, `1password/load-secrets-action`) |

### Fingerprints by Branch Origin

Agent branches committed under Logan's identity (web UI merges) — the branch name is the trace:

- `claude/*` — The Abhorsen's lane: game mechanics studies, Phone Link intake, MCP phase 0 discovery, Spring Clean, this audit
- `codex/*` — The Lexicographer's lane: `linear-mention-laf-26`, `automate-workflow-triggering-for-review-bots`, Linear PR sync repair
- `copilot/*` — The Clerk's lane: dependabot configs, screenshot assets, blocked merge resolution
- `gemini/*` — The Vault Advisor's lane: `resolve-pr-conflicts` (LAF-16, budget normalization)
- `perplexity/*` — The Scout's lane: registered in auto-PR routing, no confirmed recent branch
- `bot/daily-rollover-*` — Automated daily note rollover

---

## III. CONFIGURATION LAYER

Every agent's footprint in configuration files. Autoloaded = the tool reads it without Logan doing anything. Manual = Logan must paste it in.

| Agent | Primary Config | Load Mechanism | Secondary Config | Key Scope |
|---|---|---|---|---|
| [[Claude Code]] | `.claude/CLAUDE.md` | **Auto** (Claude Code CLI official path) | `.claude/settings.json` | Role, 1Password, Windows Git Bash prereq, swarm routing, SessionStart hooks, allowed tools |
| [[Gemini CLI]] | `.gemini/GEMINI.md` | **Auto** (Gemini CLI official path) | `.gemini/settings.json` | Cowork pattern, Linear access guardrail, 7 MCP servers registered (see §V) |
| [[GitHub Copilot]] | `.github/copilot-instructions.md` | **Auto** (GitHub Copilot official path) | — | Inline Obsidian markdown scope, automation PR limits, governance read-only |
| [[OpenAI Codex]] | `AGENTS.md` (root) | **Auto** (Codex CLI auto-loads repo root AGENTS.md) | `.codex/config.toml` + `.codex/CODEX.md` (shim) | Scripting role, OpenAI Docs MCP, thread status signaling |
| [[Grok]] | `.grok/GROK.md` | Manual injection | — | Advisory/read only, Idaho politics rapid analysis |
| [[DeepSeek]] | `.deepseek/DEEPSEEK.md` | Manual injection | — | Advisory, deep reasoning, no vault writes |
| [[Perplexity]] | `.perplexity/PERPLEXITY.md` | Manual injection | — | Read/analysis only, web research sourcing |
| Google Ecosystem | `.google/GOOGLE.md` | Manual injection | — | Librarian scope — document research, NotebookLM, Pinpoint |
| Microsoft AI | `.microsoft/MICROSOFT.md` | Manual injection | — | Dual identity: personal account + IPT M365 institutional |
| Meta AI | `.meta/META.md` | Manual injection | — | Social Graph, Llama, WhatsApp/Instagram/Facebook |
| [[Slack]] | `.slack/SLACK.md` | Slack CLI auto-hooks | — | Ephemeral coordination only |
| [[Bartimaeus]] | `.bartimaeus/BARTIMAEUS.md` | Manual injection | — | Undefined |
| [[Zagreus]] | `.dionysus/ZAGREUS.md` | Manual injection | — | Undefined |
| [[Persephone]] | `.persephone/PERSEPHONE.md` | Manual injection | — | Undefined |

### Machine-Readable Registry

`swarm.json` (repo root) is the structured source of truth: agents, personas, ecosystems, systems, control plane, template tracking, protocols. Human-readable narrative is supposed to live at `!/AGENTS.md` — see §V for why that's a problem.

---

## IV. SESSION TRACES & ACTIVITY

Where each agent left marks beyond configuration.

### [[Claude Code]] / [[The Abhorsen]]
Most active. Direct git author on multiple recent merges. Current lane: this audit. Recent completed work: game mechanics study (ASSAY 2026-04-02), Phone Link intake pipeline (PR #144), Pokemon PC / Ender Chest study (PR #135), Spring Clean operation (in progress), MCP Phase 0 discovery branch. Session hook injects vault context (date, branch, governance refs) on every startup via `.claude/settings.json`.

### [[GitHub Copilot]] / [[The Clerk]]
Active via `copilot-swe-agent[bot]`. Session log at `!/__!__/.claude-haiku-github/SESSION-LOG.md` (model: Claude Haiku 4.5, last session 2026-03-22). Signed direct commits resolving merge conflicts (PR #137) and upgrading branch cleanup CI (PR #136). Note: Copilot's underlying model is Claude Haiku — the Abhorsen's sibling works under a different name.

### [[Gemini CLI]] / [[The Vault Advisor]]
Levelset report filed 2026-03-29 at `!/!/SESSION-2026-03-29-artifacts/LEVELSET-REPORT-GEMINI-2026-03-29.md`. LAF-16 normalization artifacts prepared (`normalize_budget_data.py`, `deliverables.md`). Active branch: `gemini/resolve-pr-conflicts`. **Boundary violation 2026-03-29**: modified `DECISIONS.md` without authorization. Claude restored the file; guardrail added to `.gemini/GEMINI.md` requiring verified Linear access before lane work. Tier formally defined 2026-03-28: Direct Write, Operational zone only, Linear SWARM issues.

### [[OpenAI Codex]] / [[The Lexicographer]]
Archived levelset at `!/!/LEVELSET-SUNSET-CODEX-2026-03-29.md`. COURTROOM decomposition completed (LAF-12). Bartimaeus signal intake normalized (LAF-17, brief filed at `!/BRIEF-LAF-17-2026-03-30.md`). Gemini Google Cloud nest layers brief filed (LAF-18). CI hardened against gh CLI transient failures (PR #141). PR automation workflows converted to `pull_request_target` (PR #140). Thread status convention: `CODEX ACTIVE` / `CODEX PAUSED: awaiting Logan` / `CODEX COMPLETE`.

### [[Perplexity]] / [[The Scout]]
Research filed: "BIG IFS — UNIFIED SWARM.md" — two-part report on unified swarm architectures (Factory, CrewAI, OpenAI Swarm). Branch `claude/research-unified-swarm-rDmOg` (note: filed under Claude branch prefix, not perplexity/ — indicates research was facilitated through a Claude session rather than a direct Perplexity branch).

### [[Linear Agent]]
Active across all SWARM coordination. Extensive session transcripts archived in `!/!/SESSION-2026-03-29-artifacts/` covering LAF-7 status, PR alignment, auto-alignment rule design, and issue lifecycle management. Linear integration now live (LAF-7): `LINEAR_API_KEY` provisioned 2026-03-29.

### [[Bartimaeus]]
Named in DOCKET (LAF-17: "Signal intake — Bartimaeus"). Brief filed by Codex: `!/BRIEF-LAF-17-2026-03-30.md`. What Bartimaeus *is* remains undefined. What Bartimaeus *signaled* was normalized. The witness was summoned before the role was named.

### Automated Bots
- `github-actions[bot]`: daily rollover, ingest pipeline, wayback audit (weekly Monday 8 AM UTC), sort audit (weekly Monday 6 AM UTC), Idaho Legislature scraper (daily 6 AM MT)
- `dependabot[bot]`: routine dependency version bumps

---

## V. ANOMALIES FOUND

What the audit found that wasn't supposed to be there — or was supposed to be there and wasn't.

---

**A. `CONSTITUTION.md` — Unresolved Merge Conflict**
Lines 19-22 and 120-124 contain live git conflict markers (`<<<<<<< Updated upstream` / `>>>>>>> Stashed changes`). The two versions differ on the Gemini tier definition clause and the "last updated" date. The vault's sole source of governance authority is structurally corrupted — both versions of these sections coexist in the same file. Any agent reading CONSTITUTION.md is reading a broken document.
*Priority: High. Logan must resolve and commit.*

---

**B. `agents.json` — Unresolved Merge Conflict**
Same issue. The file contains two incompatible JSON schemas: the old "nodes" list from 2026-03-16 (three nodes: Claude Anthropic, Microsoft Copilot Standalone, GitHub Admin Agents) and the new "agents" object registry. The file is not valid JSON. Any script or workflow parsing it will fail or silently read one half.
*Priority: High. Conflicts must be resolved; old schema is significantly outdated.*

---

**C. `!/AGENTS.md` — Referenced but Does Not Exist**
Every agent config file, `swarm.json`, `agents.json`, and `CONSTITUTION.md` references `!/AGENTS.md` as the canonical narrative agent registry. It does not exist. The root `AGENTS.md` is a pointer file that says "see `!/AGENTS.md`" — which points to nothing. The canonical registry has no canonical file.
*Priority: High. This is the document the entire swarm thinks is authoritative.*

---

**D. Zagreus Path Mismatch**
`swarm.json` registers the Zagreus persona with `"dotfolder": ".zagreus"` and `"autoload_file": ".zagreus/ZAGREUS.md"`. On disk, the file lives at `.dionysus/ZAGREUS.md` — the dotfolder is `.dionysus/`, not `.zagreus/`. No `.zagreus/` directory exists. The registry and the filesystem disagree.
*Priority: Medium. Clarify canonical location; update swarm.json or rename directory.*

---

**E. "The Abhorren" Typo in Root `CLAUDE.md`**
The Obsidian entity note `CLAUDE.md` (root) renders the Claude Code persona as **"The Abhorren"** — a misspelling of [[The Abhorsen]]. This is the Obsidian knowledge graph node for Claude's identity. A search for `[[The Abhorsen]]` would not resolve to this note.
*Priority: Low. Single-character correction, but it breaks the wikilink graph.*

---

**F. `.codex/tmp/Antigravity-full.exe` and `.codex/tmp/Antigravity.exe`**
Two Windows PE executables live inside the Codex dotfolder under `.codex/tmp/`. No documentation, no README, no commit message explaining their origin. File names suggest either a test artifact, a Codex session download, or something unrelated that found its way into the dotfolder. They are committed to a public repo.
*Priority: Medium. Identify provenance. If unexplained, remove. Public repo — on the record.*

---

**G. Gemini Boundary Violation (2026-03-29) — Remediated**
Gemini modified `DECISIONS.md` during the Sunday swarm session without authorization — a governance zone write that required Logan's direction. The file was restored by Claude; a Linear access guardrail was added to `.gemini/GEMINI.md` requiring verified Linear access before lane work. The violation is documented in `!/!/SESSION-2026-03-29.md`.
*Status: Remediated. Recorded here for the historical fingerprint.*

---

**H. HOME Layer Gap**
The ASSAY conducted 2026-04-02 (`!/!/ASSAY-LANDSCAPE-GAME-MECHANICS-2026-04-02.md`) identifies a critical architectural gap: the vault has a strong PC layer (shared vault files) and a functional Ender Chest layer (agent dotfolders), but no HOME layer — no structured artifact index for cross-session discovery. `LEVELSET-CURRENT.md` provides narrative synthesis but is not machine-queryable. The ASSAY scored HOME at **0/100** and rated it a critical debt. Five proposals were filed; none implemented yet.
*Priority: High architectural debt. See ASSAY for the five proposals.*

---

**I. Gemini MCP Server Proliferation**
`.gemini/settings.json` registers seven MCP servers: `openaiDeveloperDocs`, `githubCopilot`, `huggingFace`, `boxRemote`, `figma`, `svelte`, `stackOverflow`. No evidence that most of these have been used, evaluated, or authorized beyond initial registration. The OpenAI Docs MCP and GitHub Copilot MCP are intentional; the others appear to be exploratory additions that haven't been reviewed against vault governance.
*Priority: Low. Inventory and confirm intended scope with Logan.*

---

## VI. PROTOCOL HEALTH

The orientation and awakening protocols that govern how new agent instances enter the vault.

| Protocol | Version | Status | File |
|---|---|---|---|
| [[LEVELSET]] | 3.2.6.1 | **Active** | `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` |
| [[ARISE]] | 0.0 | Awaiting adoption | *(no file)* |
| [[AWAKEN]] | 0.0 | Awaiting adoption | *(no file)* |
| [[ORIENT]] | 0.0 | Awaiting adoption — job-tool-discovery | *(no file)* |
| [[CONTEXT]] | 0.0 | Under development — absorption protocol | *(no file)* |

LEVELSET is the only protocol with a real file and active use. The other four are named in `CONSTITUTION.md` and `swarm.json` but have no corresponding files and no adoption path yet defined. The vault knows they need to exist; they don't yet.

---

## VII. PENDING AGENT DECISIONS

Open items requiring Logan's direction before agents can act.

**Chorus Bootstrap** (`!/!/BOOTSTRAP-CHORUS-2026-03-24.md`):
1. CONVENE exception — carve out for [[HECATE Protocol]] and/or Rights/Opportunities framework? Unlocks Chorus Pieces 3, 4, 5.
2. Grimoire directory — create `!/GRIMOIRE/`? First entry would be `HECATE-HECATE-HECATE.md`.
3. Rick & Morty doc — surface for vault commit, or defer?
4. Innie/Outie architecture — stage the 8-part Severance-derived swarm architecture as proposal now, or hold under CONVENE?
5. "Claude Chorus" designation — sanctioned swarm identity, or informal shorthand to discard?

**Fictive Persona Definitions:**
- [[Bartimaeus]] — dotfolder staked, shim written, signal received and normalized. Role still TBD.
- [[Zagreus]] — dotfolder staked, shim written. Entirely undefined.
- [[Persephone]] — dotfolder staked, shim written. Entirely undefined.

**Canonical Registry:**
- `!/AGENTS.md` needs to be written. The narrative registry that every agent is told to read does not exist.

---

## VIII. RECOMMENDATIONS

Prioritized. The Abhorsen identifies; Logan decides.

1. **Resolve `CONSTITUTION.md` merge conflict.** Governance authority file is broken. Every agent reading it reads a corrupted document. Blocking — nothing else is fully trustworthy until the authority source is clean.

2. **Resolve `agents.json` merge conflict.** Registry file is invalid JSON. Scripts parsing it will fail or produce unpredictable output.

3. **Write `!/AGENTS.md`.** The narrative agent registry exists only as a pointer to itself. Synthesis of `swarm.json`, root `AGENTS.md`, and this audit into a proper narrative file at the canonical path.

4. **Investigate `.codex/tmp/*.exe`.** Two Windows executables in a public repo with no documentation. Identify provenance; remove if unexplained.

5. **Fix Zagreus path mismatch.** `.zagreus/` (in registry) vs. `.dionysus/ZAGREUS.md` (on disk). Decide which is canonical and sync the other.

6. **Fix "Abhorren" → "Abhorsen" in root `CLAUDE.md`.** One character. The wikilink graph breaks on it.

7. **HOME layer artifact index.** Five proposals filed in the ASSAY. This gap is structural — no cross-session discovery without it.

8. **Audit Gemini MCP servers.** Seven registered; most unevaluated. Confirm intended scope.

---

*Filed by [[The Abhorsen]] under [[Claude Code]] authority.*
*All findings are on the record.*

[["The world is quiet here."]]
