<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Sieve | scripts diver | Reconstruct IDAHO-VAULT from .github/scripts code only (no .md/.txt); 8-field; read-only

I now have sufficient depth. Let me compile the full picture.

---

## 1. PLACE-NAME

**IDAHO-VAULT** — A personal Obsidian knowledge vault belonging to "Logan" (user `LAF-US`), backed by Git/GitHub and governed by a dense CI/automation layer.

---

## 2. POSITION — 7 core systems, ranked

1. **Daily Rollover Engine** — automated carry-forward of incomplete tasks between Obsidian daily notes at 4 AM MT via scheduled GitHub Action (`daily_rollover.py`, 37 KB, the largest script)
2. **Security/Secret Guard** — pre-commit and CI gate blocking accidental commit of credentials, private keys, `.env` files, OAuth tokens, and API key patterns (`check_secret_patterns.py` + `secret-pattern-policy.yml`)
3. **Agent-Swarm PR Pipeline** — automated PR creation from AI-agent branches (`claude/`, `codex/`, `gemini/`, `copilot/`, `perplexity/`, `grok/`, `serena/`) with risk-tiered routing (`agent-auto-pr.yml` + `classify_paths.py`)
4. **Manifest / Soft-Lock Layer** — UUID-based file-write locking and content-hash versioning in `manifest.json` so multiple agents can't clobber the same vault file concurrently (`update_manifest.py`)
5. **Content Validation Gate** — per-scope guard (bills / admin / generated / inbox / all) that blocks XSS injections, malformed YAML frontmatter, unresolved date placeholders, and deletion of governed documents (`validate_content.py`)
6. **Topology Census** — read-only auditor that maps the vault's "Swarmic Nest" (`!/`), root folders, and dotfolders against canonical doctrine (`CONSTITUTION.md`, `VAULT-CONVENTIONS.md`) to inventory authority state (`topology_census.py`)
7. **Large-File & Portability Police** — dual guard: files >100 MB must use LFS, files >2 GB are banned outright; NETWEB path check blocks Windows-illegal chars and case-collision paths (`check_large_files.py` + `check_portable_paths.py`)

---

## 3. CENTRAL CONCEIT

This is a personal "second brain" Obsidian vault that treats its owner's life — tasks, Idaho government documents, research, and daily notes — as a governed knowledge corpus with an AI-agent swarm as its workforce. The vault is not primarily a software project; it is a personal intelligence system that borrows the full machinery of software-engineering CI (gated PRs, secrets scanning, merge queues, lint, lock files) to keep a human's knowledge base safe, internally consistent, and partially automated.

---

## 4. HEADING (telos)

**(a)** "This machinery exists in order to **maintain a single authoritative, tamper-resistant, multi-agent-writable personal knowledge vault whose daily operational tempo (tasks, notes, government research) is automatically advanced while its governance structure and secrets remain inviolate**."

**(b)** Single best verb: **steward**

**(c)** Primary beneficiary: **Logan** (the vault's sole human owner, the permanent merge gate for every automated PR)

---

## 5. ENFORCED RULES — what the code actually gates

**Rule 1 — No secrets land in the repo.** `check_secret_patterns.py` runs on every PR and push to `main`. It hard-fails (exit 1) if any changed path matches a filename pattern (`.env`, `*-key.json`, `id_rsa`, `recovery-codes*`, `*.pem`, etc.) or if file content matches regex patterns for GitHub tokens (`ghp_…`), OpenAI keys (`sk-…`), Anthropic keys (`sk-ant-…`), private key PEM blocks, or generic `api_key = <long_value>` assignments. The validator runs from a pinned copy of `main` (the "trusted validator" checkout pattern), so a malicious PR cannot subvert the checker by modifying it.

**Rule 2 — No unresolved date-placeholder tokens in daily notes or the to-do list.** `validate_content.py` searches for literal `[[YESTERDAY]]`, `[[TODAY]]`, or `[[TOMORROW]]` strings in any file whose name is `YYYY-MM-DD.md` or `TO DO LIST.md` and exits 1 if found. This prevents a template-expansion failure from silently propagating stale placeholders through rollover cycles.

**Rule 3 — File moves into the vault's controlled scopes must stay in-scope; governed documents cannot be deleted by automation.** `validate_content.py`'s `--scope` flag restricts which directories an automated workflow is allowed to touch (e.g., scope `bills` locks writes to `GOVERNMENTS/IDAHO - LEGISLATIVE/…`; scope `inbox` locks to `INBOX/`). Deletion of any path in `PROTECTED_LIVE_FILES` (`AGENTS.md`, `CONSTITUTION.md`, `DECISIONS.md`, etc.) from an automated lane is a hard failure: `"Deletion of governed content requires explicit human review"`.

---

## 6. PERCEPTION LOG

**Exact paths opened:**

| # | Path |
|---|------|
| 1 | `.github/scripts/` (directory listing) |
| 2 | `.github/workflows/` (directory listing) |
| 3 | `.github/scripts/daily_rollover.py` |
| 4 | `.github/scripts/check_secret_patterns.py` |
| 5 | `.github/scripts/validate_content.py` |
| 6 | `.github/scripts/check_large_files.py` |
| 7 | `.github/workflows/secret-pattern-policy.yml` |
| 8 | `.github/scripts/classify_paths.py` |
| 9 | `.github/scripts/topology_census.py` |
| 10 | `.github/workflows/daily-rollover.yml` |
| 11 | `.github/scripts/swarm_mvp_intake.py` |
| 12 | `.github/workflows/swarm-mvp-intake.yml` |
| 13 | `.github/workflows/agent-auto-pr.yml` |
| 14 | `.github/scripts/update_manifest.py` |
| 15 | `.github/scripts/check_portable_paths.py` |
| 16 | `.github/scripts/obsidian_rest_api_client.py` |

**N opened: 16**

**~M rough count of non-md/text files visible (scripts + workflows):** ~74 (37 scripts + ~37 workflow YAMLs)

**Machinery seen but NOT opened:**
`audit_repo_payloads.py`, `backfill_daily_notes.py`, `bind_ai_book.py`, `branch_garden_report.py`, `check_dotfolder_anchors.py`, `check_version_transitions.py`, `codex_work_guard.py`, `date_tagger.py`, `expand_date_aliases.py`, `generate_agents_bootstrap.py`, `generate_name_forms.py`, `issue_reconciler.py`, `janitor_sweep.py`, `jupytext_sync_paired.py`, `laf_usb_manifest.py`, `large_file_watchdog.py`, `meshnetweb_portability_check.py`, `metadata_survey.py`, `normalize_tags.py`, `phone_link_intake.py`, `pr_lifecycle.py`, `pr_loop_watchdog.py`, `review_feedback_loop.py` (94 KB — the largest besides rollover), `stale_bot_prs.py`, `sync_obsidian_plugin_registry.py`, `tag_stubs.py`, `test_classify_paths.py`, `uv_dependency_submission.py`, `wayback_audit.py`; also all 37 workflow YAMLs except the four opened.

> _Marginalia 2026-07-24: `audit_repo_payloads.py` (first listed) has since been deleted — PR #854._

---

## 7. THREE [read] ANCHORS

1. **`.github/scripts/daily_rollover.py`** — The heartbeat of the vault. Runs at 4 AM MT daily; reads `TO DO LIST.md` and yesterday's daily note (`YYYY-MM-DD.md`), strips completed tasks (including Obsidian Tasks plugin emoji annotations like `✅ 2026-05-20` to prevent resurrection), and merges the remaining open items into today's note. Builds canonical YAML frontmatter (weekday CSS class `roygbiv-{day}`, date aliases, yesterday/tomorrow nav links). Opens a PR to `main` for Logan to review and merge.

2. **`.github/scripts/check_secret_patterns.py`** — The vault's security perimeter. Runs from a pinned-SHA `trusted-main` checkout on all PRs and pushes to prevent the checker itself from being tampered with by the branch under test. Checks both filename patterns (SSH keys, service-account JSON, password CSV, `.npmrc`, etc.) and content patterns (GitHub/OpenAI/Anthropic/Slack tokens, private-key PEM blocks, generic long secret assignments). Reports only path + line number + rule name — never the matched secret text.

3. **`.github/scripts/classify_paths.py`** — The risk router for the AI-agent swarm pipeline. Implements a two-flag scheme: a `filetype` axis (Natural Language prose → `clear`/no flag; Machine Documentation + inert assets → `low`; Computer Code → `med`) and a `depth` axis (files inside the `!/` "Swarmic Nest" → `high`; files touching the `Esto Perpetua!` still-point → `nope`). Emits binary `low`/`high` for the live PR-label contract (`risk/low`, `risk/high`) plus a richer `tier4` field (`clear`/`low`/`med`/`high`/`nope`) for future routing. The docstring explicitly names "Logan" as the human holding routing decisions open.

---

## 8. THREE [*] MARKS — inferred / guessed

1. **[*] Logan is a researcher or advocate focused on Idaho state government.** `validate_content.py` explicitly defines an `IDAHO - LEGISLATIVE` scope covering `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/`, `/SESSIONS/`, `/IDAHO HOUSE/`, `/IDAHO SENATE/`. A dedicated `bills` scope, plus a `wayback_audit.py` script (Wayback Machine integration), suggests active collection and preservation of Idaho legislative records — likely a civic research or advocacy use case.

2. **[*] The vault runs a live Obsidian instance on a local desktop.** `obsidian_rest_api_client.py` targets `https://localhost:<redacted-port>` (the `obsidian-local-rest-api` community plugin's default endpoint), `update_manifest.py` models an `interface_system: obsidian` authority tier, and `.obsidian/` config files (daily-notes.json, templates.json, community-plugins.json) are referenced throughout. This is a live, actively-synced desktop Obsidian vault, not an archived corpus.

3. **[*] The "Swarm" of AI agents is growing and its governance is actively in flux.** `agent-auto-pr.yml` recognizes branches from `claude/`, `codex/`, `gemini/`, `copilot/`, `perplexity/`, `grok/`, and `serena/` — seven distinct AI agents or tools. `classify_paths.py`'s docstring references an open issue `#626` dated 2026-06-21 and a witness document `WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`, indicating the routing grid and agent governance model are under active design revision (likely in the days immediately before this reading).


<!-- [redacted 2026-06-28 by *.hyperagent.tinkerer]: runtime residue removed (internal IP / sandbox / local-desktop paths). Originals were the vault's own config values quoted by the cold reader, except the tool-result path (this run's sandbox). See ../REDACTIONS.md. -->
