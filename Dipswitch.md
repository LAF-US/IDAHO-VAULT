<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Dipswitch | config diver | Reconstruct IDAHO-VAULT from the root tooling/bot config files only (no .md/.txt); 8-field; read-only

I have enough to reconstruct this place fully. Let me compile the final report.

---

## RECONSTRUCTION REPORT: LAF-US/IDAHO-VAULT

---

### 1. PLACE-NAME

**IDAHO-VAULT** — a personal AI-governed knowledge vault and multi-agent operating environment owned and constitutionally controlled by Logan Finney (loganfinney27).

---

### 2. POSITION — Core Systems, Ranked

1. **Multi-agent swarm layer** — seven named AI agents (Claude, Codex, Gemini, Copilot, Grok, Perplexity, Antigravity) each with dotfolder, capability tier, and signed git identity; coordinated via `swarm.json` and `!-agents.json`
2. **GitHub Actions automation corridor** — ~35 workflows governing agent PR ingestion, merge-queue arming, secret scanning, LFS policy, content validation, and daily rollover
3. **Obsidian knowledge vault** — the primary human-facing note surface; `!/` root contains governance docs (CONSTITUTION, AGENTS, WAKEUP); published via GitBook from `./!`
4. **Credential and secrets plumbing** — 1Password CLI integration, `.op/` path, PowerShell sweep scripts, GitGuardian scanning, explicit `.gitignore` credential class rules
5. **Content integrity pipeline** — `classify_paths.py` (risk tiering), `check_large_files.py` (LFS enforcement), `check_secret_patterns.py`, `validate_content.py`, `check_portable_paths.py` (NETWEB/Windows validity)
6. **CrewAI and OpenClaw local mesh** — a multi-agent orchestration layer (`.crewai/`) in "refoundation" status; local Ollama-backed mesh network via `.openclaw-local-mesh.yml`
7. **Internet Archive preservation** — `wayback-preserve.yml` and `wayback_audit.py` submit vault URLs to the Wayback Machine and audit preservation state

---

### 3. CENTRAL CONCEIT

Git is treated not as a code repository but as a **durable public record and accountability ledger** for one person's life, thought, and AI-agent activity: every commit is on the record, all AI agents write to branches and pass through Logan as the irreducible merge gate, and the entire structure is simultaneously an Obsidian personal knowledge base, a multi-agent operating environment, and a public archive whose contents are submitted to the Internet Archive for permanent preservation.

---

### 4. HEADING (telos)

**(a)** This machinery exists in order to **externalize, govern, and permanently preserve one human's cognitive and operational record across a swarm of AI agents under a single constitutionally-enforced authority**.

**(b)** Single best verb: **preserve**.

**(c)** Primary beneficiary: **Logan Finney** (sole named human; sole CODEOWNERS reviewer; all precedence chains terminate at "Logan direct instruction").

---

### 5. ENFORCED RULES (actually enforced by code/config)

1. **Agent branches only (`claude/*`, `codex/*`, `gemini/*`, `copilot/*`, `perplexity/*`, `grok/*`, `serena/*`) trigger auto-PR creation** — any other branch name is silently skipped by `agent-auto-pr.yml`. The PR is labeled with a risk tier from `classify_paths.py`; governance paths require Logan's explicit review before merge per `CODEOWNERS`.

2. **Files over 100 MB without LFS attributes, or any file over the 2 GB GitHub ceiling, are blocked** — `.gitattributes` routes all binary/media types to Git LFS with case-folded patterns; `.github/scripts/check_large_files.py` is the case-agnostic backstop that blocks oversized files lacking LFS attributes entirely.

3. **Credentials and secrets are aggressively excluded from the record** — `.gitignore` maintains an explicit multi-class exclusion list covering `.env`, key material, tool auth files (`.claude/credentials.json`, `.codex/auth.json`, `.gemini/oauth_creds.json`, etc.), with `check_secret_patterns.py` and `secret-pattern-policy.yml` scanning every PR push for credential leakage patterns.

---

### 6. PERCEPTION LOG

**Exact paths opened (N = 22):**

1. `` (root directory listing)
2. `.coderabbit.yaml`
3. `.pr_agent.toml`
4. `.codiumai.toml`
5. `.gitbook.yaml`
6. `.editorconfig`
7. `.gitconfig`
8. `.gitignore`
9. `.gitattributes`
10. `.github/` (directory listing)
11. `.github/CODEOWNERS`
12. `.github/FUNDING.yml`
13. `.github/dependabot.yml`
14. `.github/workflows/` (directory listing)
15. `.github/workflows/agent-auto-pr.yml`
16. `.github/workflows/swarm-mvp-intake.yml`
17. `.github/workflows/batch-arm-merge-queue.yml`
18. `!-agents.json`
19. `.openclaw-local-mesh.yml`
20. `.github/scripts/` (directory listing)
21. `.idaho-vault-signing-gate-build-tools/` (directory listing)
22. Root listing file (parsed from saved tool-result)

**N = 22 distinct paths opened.**

**~M rough count of non-.md/.txt machinery files in root: ~78** (from the parsed listing: `.py`, `.ps1`, `.sh`, `.json`, `.yaml`, `.yml`, `.json`, `.csv`, `.cmd`, `.bat`, `.sig`, `.js`, `.ts`, `.jpeg`, `.pdf`, `.ics`, `.patch`, `.bak`, config dotfiles).

**Machinery seen but NOT opened** (significant files not read):

- `.github/scripts/review_feedback_loop.py` (94 KB — largest script)
- `.github/scripts/classify_paths.py` (15 KB — the risk-tier classifier)
- `.github/scripts/daily_rollover.py` (38 KB)
- `.github/scripts/topology_census.py` (32 KB)
- All ~35 individual workflow `.yml` files not read
- `.bash_profile`, `.bashrc`, `.zshrc`, `.python-version`
- `!-1password-policy.ps1`, `!-credential-sweep.ps1`, and the other PowerShell scripts
- All 331 dotfolder directories (`.claude/`, `.codex/`, `.gemini/`, `.obsidian/`, `.crewai/`, etc.)
- `!-REPO-PAYLOAD-AUDIT-2026-04-03.json`, `!-dotfolder-hashcache.json`
- `.test_payload.sig`, `.python_history`

---

### 7. THREE [read] ANCHORS

**Anchor 1: `!-agents.json`**
The machine-readable agent registry. Defines the `authority_chain` (narrative registry → machine registry → bootstrap index → entrypoint), `conflict_precedence` (Logan > CONSTITUTION > agents > generated surfaces), `wakeup_protocol` boot order, and seven named agents with vendor, capability tier, git identity suffix, and required context files. This is the operational skeleton of the entire swarm.

**Anchor 2: `.github/workflows/agent-auto-pr.yml`**
The swarm intake valve. When any agent creates a branch matching its namespace (`claude/*`, `codex/*`, etc.), this workflow auto-creates a PR, runs `classify_paths.py` to assign a risk tier (`low`/`high`), labels accordingly, and marks lifecycle state as `staged`. It enforces that agents work through PRs — they cannot directly merge to `main`.

**Anchor 3: `.gitignore`**
The vault's primary epistemological statement in machine form. Its opening comment — "the vault is the record" — is the governing principle. It explicitly preserves notes, scripts, source documents, media, and agent memory while shielding credentials, runtime state, caches, and machine churn. The document encodes what counts as "on the record" versus ephemeral, class by class, for every tool Logan uses.

---

### 8. THREE [*] MARKS (inferred/guessed)

**[*] The 300+ dotfolders named after mythological figures and human characters (.anubis/, .zeus/, .isis/, .gatsby/, .lemony/, etc.) are not separate AI agents — they are [*] Obsidian "chambers" or persona-namespaced memory/notes surfaces**, one per named entity in Logan's personal knowledge graph. The `.gitignore` phrase "imported_software persona chambers" and "runtime dotfolders" supports this, but the actual contents of these folders were not read.

**[*] This vault is the local instantiation of a larger "LAF-US" organization-level topology** that includes at least five "cores" (referenced in `!-agents.json`: "LAF-USB-FIVE-CORES-MIGRATION-2026-04-15"), and possibly other repositories and physical USB/network storage (the `.gitconfig` safe directories reference `Z:\` and a UNC path `//[internal-ip redacted]/IDEX_Artifacts/`, and a `laf_usb_manifest.py` script exists). The full LAF-US chamber topology was not read.

**[*] The vault functions as a live personal operating system that Logan runs his actual daily life through** — not merely a note-taking tool. Evidence: `phone_link_intake.py` ingests phone notes; `daily_rollover.py` (38 KB, the largest script) manages temporal transitions; `1750180525.ics` (a calendar file) lives at root; JPEG images with phone-epoch timestamps are at root; a `wayback-preserve.yml` submits vault URLs to the Internet Archive as a permanent record. The "Esto Perpetua" phrase in one filename is Idaho's state motto ("Let it be perpetual"), consistent with the repo name and the preservation imperative.

<!-- [redacted 2026-06-28 by *.hyperagent.tinkerer]: runtime residue removed (internal IP / sandbox / local-desktop paths). Originals were the vault's own config values quoted by the cold reader, except the tool-result path (this run's sandbox). See ../REDACTIONS.md. -->
