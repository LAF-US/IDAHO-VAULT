<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Bosun | CrewAI diver | Reconstruct IDAHO-VAULT from .crewai code only (no .md/.txt); 8-field; read-only

I have enough to deliver a thorough reconstruction. Here is the full report:

---

## 1. PLACE-NAME

**IDAHO-VAULT** — Logan Finney's personal Obsidian knowledge vault, re-founded as a vault-contained, locally-runnable CrewAI Python project for a multi-agent swarm operating under a constitutional governance protocol.

---

## 2. POSITION

Seven core systems ranked by structural weight:

1. **Five Wizards Framework** — five-lane (WHO/WHAT/WHEN/WHERE/WHY) + one council (HOW) epistemological claim-validation engine with Pydantic models, objection/mirage categorization, and gated staging.
2. **CrewAI Bootstrap Shard** — `src/idaho_vault/crew.py` + mock LLM: a credential-free deployment-shape validator that proves packaging and execution boundaries without calling any real model.
3. **Swarm Registry (`swarm.json`)** — machine-readable roster of all agents (Claude Code, Gemini CLI, Codex CLI, GitHub Copilot, Grok, etc.) with dotfolders, autoload files, conflict-precedence hierarchy, and capability tiers.
4. **Bootstrap Contract Validator** — `bootstrap_contract.py`: deterministic ten-check suite (pyproject, lockfile, manifest.json, training doctrine, launcher, config surfaces, runtime, Python version, crew.py, MANIFEST.md) that gates threshold runs.
5. **Vault-Local Runtime Containment** — `runtime.py` + `Use-VaultAgentEnv.ps1`: redirects APPDATA/LOCALAPPDATA/HOME/TMPDIR into `.agent-home/<agent>/` so CrewAI (and all other agents) cannot pollute the real user profile.
6. **GitHub Workflow Automation Layer** — 35+ CI workflows: large-file policy, secret-pattern scans, daily rollover, auto-merge/enqueue rhythm, agent-auto-PR, CodeQL, metadata survey, wayback preservation, branch-garden.
7. **Operator Context Surface** — `operator_context.py`: live resolution of boot-chain surfaces (`AGENTS.md`, `!/WAKEUP.md`, `CONSTITUTION.md`, `swarm.json`) and daily Obsidian note path against git-tracked files, consumed by every agentic run.

---

## 3. CENTRAL CONCEIT

IDAHO-VAULT is an Obsidian knowledge vault that has been re-constituted as its own governance infrastructure: every AI agent session (CrewAI, Claude, Codex, Gemini, Grok) must pass a deterministic prereflight that checks packaging, runtime containment, doctrinal alignment, and evidence-ref existence before it may stage any output — and even then, staged output remains non-canonical until the principal (Logan Finney) explicitly promotes it, enforced via the "threshold" concept that bars self-promotion.

---

## 4. HEADING (TELOS)

**(a)** This machinery exists in order to **govern a personal AI-agent swarm so that no agent can mistake architectural access for sanctioned authority, and every claim remains evidence-anchored and human-promotable**.

**(b)** Single best verb: **constrain**.

**(c)** Primary beneficiary: **Logan Finney** (sole named principal in `swarm.json`).

---

## 5. ENFORCED RULES (gates/validators the code actually runs)

1. **Bootstrap Contract Gate** (`bootstrap_contract.py` + `threshold_runner.py::_require_threshold_contract`): Before a Five Wizards threshold run may execute, all ten contract checks must pass (pyproject tokens present, uv.lock references crewai, manifest.json registers the active bootstrap crew, training doctrine markers match, launcher routes through `Use-VaultAgentEnv.ps1`, Python 3.10–3.13 pinned, config surfaces have expected keys, runtime containment markers present). If any fail, `ThresholdContractError` is raised and the run halts.

2. **Pydantic Schema Validators** (`five_wizards/models.py`): Every `Claim`, `Objection`, `PersonalNote`, `CouncilReport`, `CouncilSession`, `GateReport`, and `ValidationVerdict` is validated by `@model_validator(mode="after")` that enforces exact entity/personality/familiar/anchor mappings against the lane-domain enums. Mismatches raise `ValueError` and the object cannot be constructed. `extra="forbid"` on `WizardBaseModel` blocks unknown fields.

3. **Large-File Policy CI** (`.github/workflows/large-file-policy.yml`): On every PR, push to main, and merge-group event, `check_large_files.py` (loaded from the trusted-main ref, not the PR head) is run against the changed file list. Oversized files block merge.

---

## 6. PERCEPTION LOG

**Exact paths opened (read):**

- `.crewai/` (dir listing)
- `.crewai/manifest.json`
- `.crewai/__init__.py`
- `.crewai/crews/__init__.py`
- `.crewai/tools/__init__.py`
- `src/idaho_vault/crew.py`
- `src/idaho_vault/bootstrap_contract.py`
- `src/idaho_vault/main.py`
- `src/idaho_vault/__init__.py` (dir listing)
- `src/idaho_vault/five_wizards/enums.py`
- `src/idaho_vault/five_wizards/models.py`
- `src/idaho_vault/five_wizards/threshold_runner.py`
- `src/idaho_vault/config/agents.yaml`
- `src/idaho_vault/config/tasks.yaml` (dir listing — confirmed file exists)
- `src/idaho_vault/operator_context.py`
- `src/idaho_vault/runtime.py`
- `pyproject.toml`
- `swarm.json` (via saved file + direct read)
- `scripts/` (dir listing)
- `scripts/Use-VaultAgentEnv.ps1`
- `.github/` (dir listing)
- `.github/workflows/` (dir listing)
- `.github/workflows/agent-review-gate.yml`
- `.github/workflows/large-file-policy.yml`

**N paths opened:** 24

**Rough count of non-.md/.txt machinery files visible but not opened:** ~60 (35+ workflow `.yml` files, 10+ `five_wizards/` Python files not fully read, `.github/scripts/` Python scripts, `.codex/config.toml`, `.github/CODEOWNERS`, `.github/dependabot.yml`, `scripts/*.py`, `scripts/*.ps1`, `src/idaho_vault/civic_scaffold.py`, etc.)

**Machinery seen but NOT opened:**

- `src/idaho_vault/civic_scaffold.py`
- `src/idaho_vault/five_wizards/lane_runner.py`, `pipelines.py`, `renderers.py`, `service.py`, `staging.py`, `validators.py`, `workflow.py`, `who_lane.py`, `what_lane.py`, `when_lane.py`, `where_lane.py`, `why_lane.py`
- `.github/scripts/` (entire directory: `daily_rollover.py`, `review_feedback_loop.py`, `pr_loop_watchdog.py`, `issue_reconciler.py`, `check_large_files.py`, `metadata_survey.py`, etc.)
- All 35 remaining workflow `.yml` files
- `.codex/config.toml`, `.github/CODEOWNERS`, `.github/dependabot.yml`, `uv.lock`, `.python-version`
- `scripts/chain_zettels.py`, `scripts/openrouter_runtime.py`, `scripts/render_flatten_attribution.py`, `scripts/Export-Dropbox.ps1`, `scripts/export-dropbox.sh`
- `src/idaho_vault/mock_llm.py`

---

## 7. THREE [read] ANCHORS

1. **`src/idaho_vault/bootstrap_contract.py`** — Deterministic prereflight engine: ten named checks against the repo filesystem (pyproject.toml tokens, uv.lock crewai presence, .crewai/manifest.json bootstrap crew registration, training doctrine text markers, PowerShell launcher routing, agents.yaml/tasks.yaml key presence, runtime containment markers, Python version regex, crew.py and MANIFEST.md existence). Produces a `ContractReport` that is passed as context to the CrewAI crew and gates the threshold runner. This is the enforcement spine of the entire system.

2. **`swarm.json`** — Structured registry of every registered AI agent: their vendor, dotfolder, autoload file, capability tier (Direct Write / Read-Analysis / Multi-Repo Admin), and explicit conflict-precedence hierarchy (Logan direct instruction > CONSTITUTION.md > !/WAKEUP.md > swarm.json > generated bootstrap surfaces > historical residue). The wakeup boot-order is listed as executable fact: `AGENTS.md → !/WAKEUP.md → CONSTITUTION.md → DECISIONS.md → VAULT-CONVENTIONS.md`.

3. **`src/idaho_vault/five_wizards/threshold_runner.py`** — The primary agentic execution surface: builds a `FiveWizardsWorkflowInput` with five lane specs (each encoding a fixed claim, evidence refs drawn from the live `OperatorContext`, wizard note, and familiar counter-note) then calls `_require_threshold_contract` (which re-runs the bootstrap contract and validates all evidence refs exist on disk) before staging to `!/CREWAI/`. The runner textually enforces "Logan approval is still required before anything staged becomes canon."

---

## 8. THREE [*] MARKS

1. **[*]** The "Five Wizards" framework (WHO/WHAT/WHEN/WHERE/WHY lanes + HOW council, with Wizard/Familiar pairs, PersonalNotes, Objections, MirageCategories, GateReports) appears to be a custom epistemological protocol designed by Logan for disciplining AI agent reasoning — the lane names, "familiar" concepts (THOU/THAT/THEN/THERE/THY), and "mirage" categories (FABRICATED_ENTITY, OVERREACH, TEMPORAL_IMPRECISION) suggest an elaborate anti-hallucination and anti-overreach doctrine, likely influenced by the personal/philosophical nature of the vault (Sebald references, "Abhorsen" role nomenclature, "Esto Perpetua" motto visible in file names).

2. **[*]** The `civic_scaffold.py` and the `run_civic_scaffold` CLI entrypoint (registered in `pyproject.toml`) likely render a human-readable status surface of the vault's "civic" health — boot chain, operator front door, backlog — for Logan's use as a daily orientation dashboard. The name and the `OperatorContext` dependency strongly suggest a synthesized view of "what is live and what needs attention today," analogous to an Obsidian dashboard that runs through Python rather than the plugin layer.

3. **[*]** The quantity and sophistication of the GitHub workflow automation (35+ workflows: auto-merge-enqueue, batch-arm-merge-queue, dependabot-rhythm, wayback-preserve, swarm-mvp-intake, review-feedback-loop, daily-rollover) relative to the apparently single-user ownership suggests this vault is functioning as a live laboratory for AI-assisted personal governance tooling — Logan is building, testing, and iterating on the infrastructure for agentic knowledge work itself, not merely using it.
