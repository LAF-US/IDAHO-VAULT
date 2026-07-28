<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Ledger | machinery diver | Reconstruct IDAHO-VAULT from swarm.json + code only (no .md/.txt); 8-field schema; read-only

I now have enough to give a complete, authoritative reconstruction. Let me compile the findings.

---

## Reconstruction: LAF-US / IDAHO-VAULT

---

### 1. PLACE-NAME

**Logan Finney's personal AI-swarm command-and-control vault** — a GitHub repository that serves simultaneously as an Obsidian knowledge base, a multi-agent orchestration registry, and a governed automation platform for a one-person "swarm" of AI coding tools.

---

### 2. POSITION — Core Systems, Ranked

1. **`swarm.json` — canonical swarm registry** — machine-readable manifest of every AI agent, persona, ecosystem, and connector; defines boot order, conflict-precedence hierarchy, and capability tiers.
2. **`.github/workflows/` (~38 workflows) — GitHub Actions automation corridor** — daily rollover, auto-merge queues, Linear sync, secret scanning, branch gardening, wayback preservation, swarm intake.
3. **`.github/scripts/` (~40 Python scripts) — automation engine** — every workflow delegates to a Python script; covers content validation, metadata survey, path classification, Linear gateway, PR lifecycle, Obsidian REST API, tag normalization, daily note generation.
4. **`CODEOWNERS` + `agent-review-gate.yml` — Logan-gated merge control** — CONSTITUTION.md, AGENTS.md, all workflows and scripts require `@loganfinney27` review before any merge.
5. **`check_secret_patterns.py` + `codex_work_guard.py` — pre-commit / CI guards** — block credential files, live API keys, and Codex work escaping into temp directories; run at both commit-time and CI.
6. **`swarm_mvp_intake.py` + `swarm-mvp-intake.yml` — gated ingest pipeline** — dispatched workflow that stages agent-submitted documents into `INBOX/SWARM-MVP/`, acquires/releases a manifest lock, validates content, and opens a *draft* PR that only Logan can merge.
7. **`check_dotfolder_anchors.py` — dotfolder integrity CI** — enforces the anchor FORMAT for every tracked top-level dotfolder (`.<name>/<NAME>.md`, per STUB-PERSONAFOLDERS): a new dotfolder cannot land without its anchor; 13 pre-existing anchorless folders (`GRANDFATHERED_MISSING_ANCHORS`) warn instead of failing until each gains its anchor and leaves the set.

---

### 3. CENTRAL CONCEIT

This is a **personal AI-swarm governance platform**: a single GitHub repo that acts as the authoritative registry, identity directory, operational constitution, and gated ingestion pipeline for a heterogeneous fleet of AI agents (Claude Code, Gemini CLI, Codex CLI, Copilot, Grok, DeepSeek, Perplexity, Mistral, and others) all working on Logan Finney's behalf. The code enforces that no agent can make durable changes to the vault without passing through Logan's human review gate; agents may propose and automate, but the vault's canonical doctrine remains Logan-owned.

---

### 4. HEADING (telos)

**(a)** This machinery exists in order to **coordinate, constrain, and audit a multi-agent AI fleet operating on behalf of a single human principal, ensuring every durable write is traceable, Logan-approved, and free of leaked credentials.**

**(b)** Best single verb: **GOVERN**

**(c)** Primary beneficiary: **Logan Finney** (sole principal, registered in `swarm.json` as `"principal": "Logan Finney"`)

---

### 5. ENFORCED RULES — What the Code Actually Makes True

1. **No credential or secret material may reach the repo.** `check_secret_patterns.py` runs as a pre-commit and CI guard; it matches regex patterns for GitHub tokens, OpenAI/Anthropic keys, Slack tokens, private key blocks, Google API keys, `.env` files, `.pem`/`.p12`, SSH keys, and password CSVs. A match blocks the commit; matched text is never printed to output (only path + rule name). Files can opt out of the generic assignment rule only via `secret-pattern: allow` inline comments or `process.env.*` references.

2. **Every tracked top-level dotfolder must carry its format-derived anchor.** `check_dotfolder_anchors.py` (run in CI via `check-dotfolder-anchors.yml`) enumerates tracked dotfolders from `git ls-tree HEAD` and requires `.<name>/<NAME>.md` (`.claude/CLAUDE.md`, `.gemini/GEMINI.md`, `.codex/CODEX.md`, …). A missing anchor fails the check for any non-grandfathered folder; the 13 folders in `GRANDFATHERED_MISSING_ANCHORS` are pre-existing debt that warns (with a healed-folder announcement once anchored) rather than fails. This prevents silent deletion or stub-only states for active agent chambers.

3. **Agent-submitted intake documents must pass through a draft PR that only Logan can merge.** The `swarm-mvp-intake.yml` workflow creates a branch, acquires a manifest lock, validates content via `validate_content.py --scope inbox`, then opens a `--draft` PR with the explicit note "This PR is draft-only. Logan remains the merge gate." CODEOWNERS additionally requires `@loganfinney27` review on all workflows, scripts, CONSTITUTION.md, and AGENTS.md before any merge can land.

---

### 6. PERCEPTION LOG

Paths opened (N = 12):
- `swarm.json` (root)
- root directory listing
- `.github/` directory listing
- `.github/workflows/` directory listing
- `.github/scripts/` directory listing
- `.github/scripts/check_secret_patterns.py`
- `.github/scripts/codex_work_guard.py`
- `.github/workflows/agent-review-gate.yml`
- `.github/scripts/swarm_mvp_intake.py`
- `.codex/` directory listing + `config.toml`
- `.github/workflows/swarm-mvp-intake.yml`
- `.github/CODEOWNERS`
- `.github/scripts/check_dotfolder_anchors.py`

**Total non-.md/.txt files seen but not opened (rough count ~M):** approximately 75+ — including `daily_rollover.py` (38KB), `review_feedback_loop.py` (95KB, the largest script), `topology_census.py`, `classify_paths.py`, `normalize_tags.py`, `metadata_survey.py`, `linear_gateway.py`, `linear_pr_sync.py`, `obsidian_rest_api_client.py`, `bind_ai_book.py`, `batch-arm-merge-queue.yml`, `cloud-run-deploy.yml`, `codeql.yml`, `dependabot.yml`, `laf_usb_manifest.py`, `update_manifest.py`, `wayback_preserve.yml`, and the full `.claude/`, `.gemini/`, `.grok/`, `.deepseek/`, `.serena/`, `.codex/rules/`, `.codex/skills/`, `.github/probes/`, `.github/swarm/`, `.github/actions/`, `.github/ISSUE_TEMPLATE/` subtrees, plus `manifest.json` at root and `INBOX/` subtree.

---

### 7. THREE [read] ANCHORS

1. **`swarm.json`** — The vault's boot manifesto. Defines 13 registered agents (Claude Code, Gemini CLI, Codex CLI, GitHub Copilot, Grok, DeepSeek, Perplexity, Mistral Vibe, Linear Agent, Serena, Antigravity) with capability tiers, dotfolder mappings, autoload flags, and install/uninstall event timestamps. Also defines 3 personas (Bartimaeus, Zagreus, Persephone), 3 ecosystems (Microsoft, Google, Meta), and 3 connectors (GitHub, Linear, Slack) with explicit write modes (`gated-write`, `notification-write`) and promotion rules. Encodes a strict `conflict_precedence` hierarchy with "Logan direct instruction" at the top.

2. **`.github/scripts/check_secret_patterns.py`** — A hardened pre-commit/CI secret scanner. Scans both file paths (via 18 regex patterns: `.env`, `.op/`, `credentials*.json`, `*-key.json`, `*.pem`, `id_rsa`, `*passwords*.csv`, etc.) and file content (7 token regex rules: GitHub PAT, OpenAI key, Anthropic key, Slack token, PEM block, Google API key, generic assignment). Reports only path + line + rule; never echoes matched text. Has a narrow allow-list for `process.env.*` references and `.env.example` files. The `.op/` governance chamber is explicitly carved out.

3. **`.github/workflows/swarm-mvp-intake.yml`** — The swarm intake pipeline. Triggered only by `workflow_dispatch`. Creates a branch, acquires a manifest lock via `update_manifest.py`, writes a staged artifact to `INBOX/SWARM-MVP/` via `swarm_mvp_intake.py`, verifies the exact set of changed files matches expectations (fails if any unexpected file is touched), runs `validate_content.py --scope inbox`, commits, and opens a **draft** PR. The PR body explicitly states "Logan remains the merge gate."

---

### 8. THREE [*] MARKS — Inferred / Guessed

1. **[*] The vault is primarily a Windows-native Obsidian vault synced to GitHub.** Evidence: `check_secret_patterns.py` has explicit `WINDOWS_COPY_SUFFIX_RE` handling for paths like `file (2).gitconfig` (visible in the root listing), `.gitconfig` copies, and Windows-style `%LOCALAPPDATA%/Temp` path scanning in `codex_work_guard.py`. The presence of `rclone-filter.txt` in `.github/` suggests rclone is used for backup/sync. The repo root contains Obsidian-style `!` prefix files (e.g., `! README.md`, `!-!-...` pattern files). Together this implies the primary human interface is Obsidian on Windows, with GitHub as the governed backup and automation surface.

2. **[*] `review_feedback_loop.py` (95KB — the largest single file) is the operational heart of the PR automation loop**, likely implementing the full AI-assisted review cycle: posting review comments, tracking review states across multiple agents, handling re-review requests, and the "WITNESSED" attestation pattern mentioned in `agent-review-gate.yml`. Its size (~3000+ lines) suggests it is a self-contained engine, not just a utility.

3. **[*] The "SWARM" label in Linear is the primary execution-tracking hub for tasks delegated to AI agents.** The `swarm.json` connector entry for Linear says "SWARM label is the registered coordination hub" and "no meaningful work without a mapped issue." Combined with `swarm_mvp_intake.py` requiring an optional `linear_ref` field, this suggests the operational workflow is: Logan creates a Linear issue with the SWARM label → an agent picks it up via the Linear connector → work is done on a vault branch → a draft PR is opened → Logan reviews and merges. The `linear_gateway.py` and `linear_pr_sync.py` scripts (seen but not opened) likely implement the bidirectional GitHub↔Linear issue state sync described in `swarm.json`.
