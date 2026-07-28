<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Tappet | workflows diver | Reconstruct IDAHO-VAULT from .github/workflows + code only (no .md/.txt); 8-field; read-only

I now have a thorough picture of this repository. Let me compile the full report.

---

## Report: LAF-US/IDAHO-VAULT

---

### 1. PLACE-NAME

**IDAHO-VAULT** — A personal AI-multi-agent knowledge vault for Logan (LAF-US), built on Obsidian as the interface layer, GitHub as the execution transport, and a heavily automated CI/CD control plane that governs how a swarm of AI agents (Claude, Codex, Gemini, Copilot, Grok, Perplexity, Serena, Mistral, DeepSeek) read from and write to the vault.

---

### 2. POSITION — Seven Core Systems, Ranked

1. **Agent swarm governance layer** — multi-AI write-permission registry with tiered capability (Direct Write / Advisory / Read-only) per agent, coordinated via `agents.json` and `swarm.json`
2. **CI risk-classification engine** — `classify_paths.py` two-axis (filetype × Nest-depth) tier scheme gates every PR with `risk/low` or `risk/high` labels
3. **Automated PR pipeline** — agent branches (`claude/*`, `codex/*`, `gemini/*`, etc.) get auto-PRs created, lifecycle-tagged (`staged`), and swept into a merge queue
4. **Secret and content guard** — pre-commit hook + CI workflow scan changed files for credential patterns, dangerous HTML, and oversized payloads before commit/merge
5. **`manifest.json` soft-lock system** — two-phase acquire/release UUID lock protocol tracking every file written by any agent, with SHA-256 hashing, versioning, and Obsidian template inventory
6. **Daily-note / rollover automation** — `daily_rollover.py` (38 KB, largest script) manages recurring task carryforward, date-placeholder resolution, and TO-DO-LIST maintenance
7. **NETWEB path-portability enforcement** — CI validator blocks cross-platform path violations (illegal chars `<>:"|?*`, Windows-copy suffixes, etc.) from entering the tree

---

### 3. CENTRAL CONCEIT

This is a governed, multi-agent personal knowledge operating system in which a single human owner (Logan) is the sole merge authority, and a swarm of AI coding agents are permitted to write to the vault only through a structured PR pipeline — every write is classified by risk, scanned for secrets, validated for content safety, registered in a manifest, and held in a staged lifecycle state until the human explicitly merges it. The vault is simultaneously an Obsidian notebook and a self-policing software repository that treats AI-generated content with the same CI discipline as production code.

---

### 4. HEADING (telos)

**(a)** "This machinery exists in order to **let multiple AI agents contribute to a single human's personal knowledge vault without any agent being able to bypass the owner's review**."

**(b)** Primary verb: **governs**

**(c)** Primary beneficiary: Logan (the human owner, LAF-US), who retains sole merge authority over every AI-authored change

---

### 5. ENFORCED RULES (what the code actually makes true)

**Rule 1 — Secret exclusion at commit and PR boundary.**
`check_secret_patterns.py` runs at pre-commit (`.githooks/pre-commit`) AND in the `secret-pattern-policy.yml` CI check on every PR, push to main, and merge-group event. It matches regex patterns for GitHub tokens, OpenAI/Anthropic keys, private-key PEM blocks, credential JSON filenames, SSH key filenames, and `.env` paths. Violations exit non-zero; no matched text is printed (path + line + rule name only). The `generic_secret_assignment` rule can be bypassed inline with `# secret-pattern: allow` but dedicated token rules cannot.

**Rule 2 — All agent-authored files must be registered in `manifest.json` under a soft-lock before commit.**
`update_manifest.py` enforces a two-phase acquire/release lock protocol keyed on `(file_path, agent_id)`. A conflicting active lock from a different agent raises `RuntimeError`. Every entry records SHA-256 hash, writer, timestamp, and version counter. The `swarm-mvp-intake.yml` workflow verifies that only the expected two files (`INBOX/SWARM-MVP/...md` and `manifest.json`) are changed; any deviation exits 1. Deletions of `PROTECTED_LIVE_FILES` (AGENTS.md, CONSTITUTION.md, etc.) from an automated lane are rejected by `validate_content.py`.

**Rule 3 — PR branches from agent namespaces (`claude/*`, `codex/*`, `gemini/*`, `copilot/*`, `perplexity/*`, `grok/*`, `serena/*`) receive a `risk/low` or `risk/high` label determined by the path classifier, and the swarm-intake PR is always draft-only with "Logan remains the merge gate" written in the PR body.**
`agent-auto-pr.yml` gates on branch name prefix, calls `classify_paths.py` to compute the binary `tier`, stamps `--label risk/$RISK_TIER`, and marks lifecycle state as `staged`. Low-risk PRs additionally receive `review/pending`. The `swarm-mvp-intake.yml` hard-codes `--draft` and the PR body reads: "This PR is draft-only. Logan remains the merge gate."

---

### 6. PERCEPTION LOG

**Exact paths opened (N = 18):**
- `.github/workflows/` (directory listing)
- `.github/workflows/agent-auto-pr.yml`
- `.github/workflows/batch-arm-merge-queue.yml`
- `.github/workflows/secret-pattern-policy.yml`
- `.github/workflows/swarm-mvp-intake.yml`
- `.github/workflows/agent-review-gate.yml`
- `.github/workflows/large-file-policy.yml`
- `.github/workflows/validate-daily-notes.yml`
- `.github/workflows/check-portable-paths.yml`
- `.github/scripts/` (directory listing)
- `.github/scripts/classify_paths.py`
- `.github/scripts/check_secret_patterns.py`
- `.github/scripts/validate_content.py`
- `.github/scripts/update_manifest.py`
- `.githooks/pre-commit`
- `agents.json`
- root directory listing (via large tool-result file)
- code search for `manifest.json` (returned 119 hits, partial read)

**N opened: 18 distinct file reads**

**~M non-md/text files visible: approximately 75+** (38 yml workflows, 35+ Python scripts in `.github/scripts`, several `.json` config/data files at root, `.githooks/pre-commit`, `pyproject.toml`, `uv.lock`, `.obsidian/` config JSONs, `.crewai/` files)

**Notable machinery seen but NOT opened:**
- `daily_rollover.py` (37 KB — largest script; manages daily note carryforward cycle)
- `review_feedback_loop.py` (94 KB — largest file in the repo by far; the full PR review state machine)
- `topology_census.py` (31 KB — vault structure surveyor)
- `swarm.json` (root — the machine-readable agent registry and promotion rules)
- `manifest.json` (root — the live execution-state coordination document)
- `pyproject.toml` / `uv.lock` (Python package config; CrewAI dependency referenced)
- `.obsidian/` config JSONs (daily-notes.json, templates.json, community-plugins.json)
- `.crewai/manifest.json` (CrewAI layer registry at `status: refoundation`)
- `src/idaho_vault/bootstrap_contract.py` (vault bootstrap contract checker)
- `codeql.yml`, `cloud-run-deploy.yml`, `wayback-preserve.yml`, `looker-walk.yml` (additional workflow machinery)
- `obsidian_rest_api_client.py` (Obsidian REST API integration script)

---

### 7. THREE [read] ANCHORS

**Anchor 1 — `.github/scripts/classify_paths.py`**
The path-risk classifier: implements a two-axis (filetype: `clear/low/med` × Nest-depth: `high/nope`) scheme. Files in the `!` Swarmic Nest are classified by depth; maze (non-Nest) files by extension against three "blessed language circles" (Natural Language → clear, Machine Documentation → low, Computer Code → med). The `!` prefix and `Esto Perpetua!` path segment are structural markers of the vault's internal hierarchy. Outputs a JSON blob with binary `tier` (low|high) for the live `risk/<tier>` label contract, plus richer `tier4` field for future routing.

**Anchor 2 — `agents.json`**
The agent discovery index: registers 10 AI agents (Claude Code, Codex CLI, Gemini CLI, GitHub Copilot, Grok, Perplexity, DeepSeek, Mistral, Serena, Antigravity) with vendor, dotfolder, capability tier, instructions file, autoload flag, and required/optional context files. Defines a conflict-precedence stack: Logan direct instruction > CONSTITUTION.md > WAKEUP.md / AGENTS.md > swarm.json > generated bootstrap > historical notes. GitHub = execution transport; Linear = execution state; Slack = ephemeral breadcrumbs.

**Anchor 3 — `.githooks/pre-commit`**
The local commit gate: runs 5 checks in sequence — sync Obsidian plugin registry + stage manifest/swarm, verify registry consistency, validate LAF-USB object manifests, scan staged files for secrets, check for oversized files, and (if jupytext is available) sync any paired `.ipynb` notebooks with their plaintext twins. This is the first enforcement layer before CI; a failure on any check aborts the commit.

---

### 8. THREE [*] MARKS (inferred / guessed)

**[*] Mark 1 — The vault is primarily a journalism/civic-data workspace focused on Idaho state government.**
`validate_content.py` contains `SCOPE_ALLOWED_DIRS` with explicit paths like `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/`, `GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/`, `GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO HOUSE/`, and `GOVERNMENTS/IDAHO - LEGISLATIVE/IDAHO SENATE/`. The `check_secret_patterns.py` explicitly exempts `.op/1password-hygiene-policy.json` (1Password governance doc). The name "IDAHO-VAULT" and LAF-US (likely a journalistic/civic organization) combined with Idaho legislative directory structure strongly imply this is a personal knowledge base for covering Idaho politics/legislation — "the journalism vault" language appears in a search result fragment.

**[*] Mark 2 — Logan (the owner) is a solo operator managing a significant AI-agent overhead that has at times grown unwieldy, and the entire CI machinery is a retrospective control layer built to regain governance over what the agents were doing.**
Evidence: the inline comments in `batch-arm-merge-queue.yml` document specific past failures by PR number (PR #484, #485, #549, #588, #663), field notes dated 2026-06-19 and 2026-06-20, and a `batch-arm-merge-queue.yml` comment noting "armed=73 while ZERO PRs entered the queue." The `agent-review-gate.yml` disabled its own cron ("disabled_manually 2026-05-26 — failing/noisy") and explicitly warns a prior PR wrongly re-wired it. This pattern — escalating workflow complexity, numbered post-mortems, explicit notes to future agents ("NEXT AGENT — the one fact that prevents breakage") — suggests the repo grew faster than its governance and the control machinery is being built incrementally to catch up.

**[*] Mark 3 — The `!` Swarmic Nest (`!/`) is a nested "inner sanctum" of the vault with its own governance hierarchy (seven "Levels" or "Demesnes," with `Esto Perpetua!` as the inviolable still-point), and `classify_paths.py`'s "maze vs. labyrinth" metaphor is part of a deliberate, idiosyncratic personal cosmology Logan applies to the vault's information architecture.**
Evidence: `classify_paths.py` uses the terms "maze" (filetype axis), "labyrinth" (depth axis), "Swarmic Nest," "Sierpinski spine," "Esto Perpetua!" (Latin: "let it be perpetual"), "blessed language circles," and references "VAULT-CONVENTIONS § File Types" and "the Architect's three blessed language circles." The `validate_content.py` script references "PROTECTED_LIVE_FILES" including `!/WAKEUP.md` and `!/AGENTS.md`. The `agents.json` boot order and the file `LEVELSET.md` in required context all point to an elaborate self-designed ontology. This cosmology is not incidental — it is load-bearing: the classifier's `NEST_PREFIX = "!"` and `STILL_POINT_SEGMENT = "Esto Perpetua!"` are active code.
