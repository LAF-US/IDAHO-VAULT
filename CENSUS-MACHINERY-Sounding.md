<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Sounding | machinery CONTROL | Reconstruct IDAHO-VAULT from code only, no door, from root (no .md/.txt); 8-field; read-only

I now have sufficient depth to produce the full reconstruction. Let me compile the findings.

---

## RECONSTRUCTION REPORT: LAF-US / IDAHO-VAULT

---

### 1. PLACE-NAME

**IDAHO-VAULT** — Logan Finney's personal AI-native knowledge vault and multi-agent operating environment, hosted at `C:\Users\<user>\Documents\IDAHO-VAULT` and mirrored publicly to GitHub under org `LAF-US`.

---

### 2. POSITION — 7 Core Systems, Ranked

1. **`!` Nest (swarmic command spine)** — Hierarchical control directory containing agent bootstrap, governance constitutions, wakeup protocols, and canonical decision surfaces. The "Swarmic Nest" with depth-tiered sensitivity; the still-point at `Esto Perpetua!` is considered immovable canon.

2. **Multi-agent registry and capability tiers** (`!-agents.json`, `swarm.json`)  — Named agents (Claude Code, Codex, Copilot, Gemini, Grok, Perplexity, Antigravity) with assigned dotfolders, git identities, capability tiers (Direct Write / Read-Analysis / Multi-Repo Admin), and required bootstrap context files.

3. **GitHub Actions automation corridor** (`.github/workflows/`, `.github/scripts/`) — ~35 workflows plus ~35 Python scripts governing: agent auto-PR creation, PR lifecycle state machine, secret-pattern scanning on every push, risk classification of changed paths, auto-merge queue rhythm, branch cleanup, daily rollover, Wayback Machine preservation, Obsidian plugin sync, metadata survey, and more.

4. **1Password credential management layer** (`!-credential-sweep.ps1`, `!-vault-placement-sweep.ps1`, `!-normalize-item-metadata.ps1`, `!-1password-policy.ps1`, `!-resolve_openrouter_secret.py`) — PowerShell + Python scripts that enumerate 1Password vaults (Personal, Work, Wallet, Vault, Private), audit API credentials, propose canonical names, recommend vault placement by service-hint heuristics, and write sanitized markdown/JSON reports. All writes require an explicit `ConfirmToken` safety interlock.

5. **OpenClaw local-mesh AI daemon** (`.openclaw-local-mesh.yml`, `.openclaw-local-only.yml`, `!-openclaw-daemon.sh`) — A local AI gateway (named "big-pickle") running `ollama/phi3:mini`, optionally with Kimi-K2 cloud, that provides a local-first mesh network for agent coordination with configurable cloud-model deny lists.

6. **Path risk classifier and PR review gate** (`.github/scripts/classify_paths.py`, `agent-auto-pr.yml`, `agent-review-gate.yml`, `secret-pattern-policy.yml`) — All agent-authored branch pushes (prefixed `claude/`, `codex/`, `gemini/`, etc.) are automatically intercepted, classified by a two-axis scheme (filetype circle × Nest depth), labeled `risk/low` or `risk/high`, and placed into a review lifecycle; secret patterns are blocked on every push/PR/merge-group.

7. **Obsidian knowledge vault integration** (`.obsidian/` config tracked, `obsidian_rest_api_client.py`, `normalize_tags.py`, `metadata_survey.py`, `daily_rollover.py`) — The markdown corpus is an Obsidian vault; Python scripts automate tag normalization, daily note rollover, frontmatter metadata surveying, and synchronization. The entire git record is the "vault-as-record."

---

### 3. CENTRAL CONCEIT

IDAHO-VAULT is a personal knowledge vault that doubles as a live multi-agent operating environment: the Obsidian markdown corpus is the durable record, and a layered control plane — 1Password for secrets, GitHub Actions for automation governance, a local AI mesh for agent coordination, and a swarmic nest of bootstrap/constitution documents — keeps a team of named AI agents (Claude, Codex, Copilot, Gemini, Grok, Perplexity, Antigravity) working in the vault under continuous human oversight by one owner, Logan Finney. Git-as-truth is the axiom: everything committed is "on the record."

---

### 4. HEADING (TELOS)

**(a)** This machinery exists in order to **allow one human operator to direct a coordinated swarm of heterogeneous AI agents against a single personal knowledge base, while enforcing credential hygiene, secret containment, and human-approval gates on all agent-authored changes.**

**(b)** Single best verb: **Orchestrate.**

**(c)** Primary beneficiary: **Logan Finney** (sole human operator, `loganfinney27`).

---

### 5. ENFORCED RULES (Code-Enforced)

1. **Secrets cannot land in the repo.** `secret-pattern-policy.yml` runs `check_secret_patterns.py` on every PR, push to main, and merge-group event, scanning changed files for patterns like `sk-ant-`, `sk-or-v1-`, `OPENROUTER_API_KEY`, etc. The check fails the workflow if matches are found.

2. **Item moves and edits in 1Password require an explicit safety token.** `!-vault-placement-sweep.ps1` and `!-normalize-item-metadata.ps1` both enforce `Assert-ApplySafety`: any write operation will `throw` unless `-ConfirmToken MOVE_ITEMS` / `EDIT_ITEMS` is passed, and the number of affected items must be under the policy's `max_moves`/`max_edits` limits (default 25/100) or `-ForceLargeBatch` must be set.

3. **Governance surfaces and the `!` Nest require Logan's explicit approval before merge.** `CODEOWNERS` assigns `@loganfinney27` ownership of `CONSTITUTION.md`, `AGENTS.md`, `LEVELSET.md`, `/.github/workflows/`, `/.github/scripts/`, `/.op/`, and the deep `!/!/__!__/` still-point. `classify_paths.py` pins all dotfolder agent configs and `.github/**` to `high` risk, preventing auto-merge on those paths regardless of the agent that authored them.

---

### 6. PERCEPTION LOG

**Exact paths opened (read):**

1. `` (root dir listing — 1000-item JSON)
2. `!` (dir listing of the `!` Nest)
3. `.claude.json`
4. `!-agents.json`
5. `!-CREWAI-LINKER-PROPOSAL-v1.json` (too large to read; metadata only)
6. `.gitconfig`
7. `!-credential-sweep.ps1`
8. `!-vault-placement-sweep.ps1`
9. `!-security-sweep.ps1`
10. `.openclaw-local-mesh.yml`
11. `!-1password-policy.ps1`
12. `!-normalize-item-metadata.ps1`
13. `!-swarm 1-state_manager.py`
14. `.gitignore`
15. `.coderabbit.yaml`
16. `.pr_agent.toml`
17. `.github` (dir listing)
18. `.github/CODEOWNERS`
19. `.github/workflows` (dir listing — 35+ workflow files)
20. `.github/workflows/agent-auto-pr.yml`
21. `.github/workflows/secret-pattern-policy.yml`
22. `.github/scripts` (dir listing — 35+ Python scripts)
23. `.github/scripts/classify_paths.py`
24. `!-resolve_openrouter_secret.py`
25. `.openclaw-local-only.yml`

**N = 25 paths opened** (24 successfully read, 1 too large).

**~M rough count of non-md/txt files in root:** ~78 at root level; hundreds more across ~331 subdirectories.

**Machinery seen but NOT opened (representative):**

- All 35+ `.github/workflows/*.yml` beyond `agent-auto-pr.yml` and `secret-pattern-policy.yml` (e.g., `batch-arm-merge-queue.yml`, `review-feedback-loop.yml`, `swarm-mvp-intake.yml`, `wayback-preserve.yml`)
- All 35+ `.github/scripts/*.py` beyond `classify_paths.py` (e.g., `review_feedback_loop.py` at 94KB, `topology_census.py`, `daily_rollover.py` at 37KB, `metadata_survey.py`)
- `!-CREWAI-LINKER-PROPOSAL-v1.json` (1MB)
- `.crewai/manifest.json`, `swarm.json` (referenced in `!-agents.json`)
- `.op/1password-hygiene-policy.json`
- All 300+ named agent dotfolders (`.claude/`, `.gemini/`, `.codex/`, `.anthropic/`, `.osiris/`, `.zeus/`, etc.)
- `!-dotfolder-hashcache.json`, `!-REPO-PAYLOAD-AUDIT-2026-04-03.json`
- `.github/swarm/` state subdirectory
- `.vscode/`, `.obsidian/` configs
- `!-launch-claude-openrouter.sh`, `!-openclaw-daemon.sh`

---

### 7. THREE [read] ANCHORS

1. **`!-agents.json`** — The machine-readable agent registry. Declares the authority chain (`AGENTS.md` → `swarm.json` → `!-agents.json` → bootstrap entrypoint), conflict precedence ("Logan direct instruction" outranks everything), and per-agent capability tiers, git identities, and required context files. The wakeup protocol boot order is encoded here.

2. **`.github/scripts/classify_paths.py`** — The path risk classifier. Implements a two-axis scheme (filetype circle × Nest depth) to label every PR changeset `low`/`high` (binary legacy) and `clear`/`low`/`med`/`high`/`nope` (richer tier4). The `!` Nest's still-point (`Esto Perpetua!`) is hardcoded as `nope` (do not auto-merge under any circumstances). This is the brain behind the automated PR governance.

3. **`!-vault-placement-sweep.ps1`** — The 1Password vault hygiene engine. Reads all 1Password items, classifies them by service hints (openrouter, anthropic, claude, github, etc.) and category (API_CREDENTIAL, SSH_KEY, LOGIN), recommends target vaults (Personal / Work / Wallet / Vault / Private) with confidence levels, generates timestamped JSON/Markdown reports, and — only when `-Apply -ConfirmToken MOVE_ITEMS` are both present — physically moves items via `op item move`.

---

### 8. THREE [*] MARKS (Inferred)

1. **[*]** The 300+ named dotfolders (`.osiris/`, `.zeus/`, `.anubis/`, `.apollo/`, `.arthur/`, `.abhorsen/`, etc.) are almost certainly named "persona chambers" — each representing a distinct AI agent identity, mythological character, or relationship/role archetype that Logan assigns context or memory to. The sheer breadth (Egyptian gods, Greek gods, biblical figures, literary characters, family-role names like `.mother/`, `.father/`, `.sister/`) suggests this is a world-model encoded in directory structure, not just tooling.

2. **[*]** The repo is Logan's actual live personal desktop vault — not a showcase or template. Evidence: `.claude.json` records 11 real startup sessions beginning 2026-03-22, a last session cost of $16.29 using `kimi-k2.5:cloud`, real GitHub paths (`C:\Users\<user>\Documents\IDAHO-VAULT`), a Claude companion named "Moth" with personality "A rare capybara of few words," and MCP integrations to Gmail, Google Calendar, Slack, Figma, Linear, and Asana. The file is a live session state snapshot committed to the repo.

3. **[*]** The `swarm.json` (not opened, but heavily referenced) is likely the master operational topology document — more authoritative than `!-agents.json` (which explicitly says `"source_of_truth": "swarm.json"` and `"status": "generated"`). The `!-CREWAI-LINKER-PROPOSAL-v1.json` at 1MB likely contains a very large CrewAI agent topology definition or a complete link-graph of the vault's document connections. The "Arborscaping" series visible in the `!` directory listing (`ARBORSCAPE-COMPLETION-REPORT`, `ARBORSCAPING-INVESTIGATION-RETURN`) [*] represents an automated pass of tree-structure analysis or topology grooming of the vault's content graph — the vault treats its own structure as a subject of ongoing agent-driven study.

<!-- [redacted 2026-06-28 by *.hyperagent.tinkerer]: runtime residue removed (internal IP / sandbox / local-desktop paths). Originals were the vault's own config values quoted by the cold reader, except the tool-result path (this run's sandbox). See ../REDACTIONS.md. -->
