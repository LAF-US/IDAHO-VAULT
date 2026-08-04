<!-- [cold-read apocrypha] recovered subagent report; raw, verbatim; not canon. -->

# Dredge | journalism-automation diver | Reconstruct IDAHO-VAULT from the Idaho-government scraping/budget code only (no .md/.txt); 8-field; read-only

I now have a thorough picture of this repository's machinery. Here is the full reconstruction:

---

## 1. PLACE-NAME

**IDAHO-VAULT** — the personal knowledge and journalism vault of Logan Finney (Idaho reporter, handle `@lfinneytweets`), run by the LAF-US GitHub organization.

---

## 2. POSITION — 7 Core Systems, Ranked

1. **Obsidian knowledge vault** — massive flat-file Markdown knowledge base, structured by a canonical taxonomy (GOVERNMENTS / ORGANIZATIONS / PEOPLE / PLACES / SOURCES / TOPICS), tracking Idaho legislative, judicial, and executive entities, sourced articles, hearing notes, and people.

2. **GitHub Actions automation layer** — ~30+ workflows enforcing vault hygiene, managing PRs, running daily rollover, auditing sort order, syncing Wayback Machine preservation, checking file sizes and secret patterns.

3. **Daily rollover engine** (`daily_rollover.py`) — scheduled Action that carries incomplete to-do tasks forward from yesterday's daily note into today's, syncing against a persistent `TO DO LIST.md` active backlog.

4. **Multi-agent AI swarm** (`!-agents.json`, `.github/swarm/`, `swarm.json`) — registered roster of AI agents (Claude Code, Codex, Copilot, Gemini, Grok, Perplexity, Antigravity) each with dotfolder configs, git identities, and a precedence chain; governed by a `CONSTITUTION.md` and `WAKEUP` protocol.

5. **Twitter/X archive importer** (`!-twitter-extract.py`) — converts Logan's Twitter export (`tweets.js`) into individual YAML-fronted Markdown notes in `tweets/YYYY/`, deduplicated by tweet ID.

6. **Wayback Machine preservation pipeline** (`wayback-preserve.yml`, `wayback_audit.py`) — on every push to `SOURCES/`, `GOVERNMENTS/`, `TOPICS/`, extracts `URL:` fields from changed notes and submits them to Save Page Now (archive.org), logging results back into the vault.

7. **Sort/metadata audit infrastructure** (`sort_audit.py`, `metadata_survey.py`, `normalize_tags.py`, `classify_paths.py`) — walks the vault tree, flags misplaced files against a defined taxonomy, enforces naming conventions (e.g. `YYYY-MM-DD - Outlet - Title.md` for news articles), and reports anomalies via GitHub Actions step summaries.

---

## 3. CENTRAL CONCEIT

IDAHO-VAULT is a journalist's beat database — an Obsidian vault committed to GitHub where Idaho government reporting (legislature, JFAC, budget, courts, agencies) is the content, and a multi-agent AI swarm plus GitHub Actions are the custodians, enforcing taxonomy, preserving sources, and carrying work forward daily. The vault is simultaneously a personal knowledge graph, a sourcing and citation archive, and a CI-governed information system that will not let secrets, oversized binaries, or misclassified notes slip through.

---

## 4. HEADING (Telos)

(a) This machinery exists in order to **maintain a permanently organized, tamper-resistant, AI-assisted record of Idaho government activity for investigative journalism**.

(b) Single best verb: **chronicle**.

(c) Primary beneficiary: **Logan Finney** (Idaho Reports journalist and sole owner, `LAF-US`).

---

## 5. ENFORCED RULES — 3 the Code Actually Enforces

1. **Files over 100 MB must be Git LFS-tracked; files over 2 GB cannot be committed at all** — enforced on every PR, push, and merge-group event by `check_large_files.py` / `large-file-policy.yml`, which inspects `.gitattributes` for the `filter=lfs` attribute and fails the check with a non-zero exit code.

2. **No secret material may be committed** — `check_secret_patterns.py` / `secret-pattern-policy.yml` scans changed files for path patterns (`.env`, `credentials.json`, `id_rsa`, etc.) and content patterns (GitHub tokens `ghp_*`, OpenAI keys `sk-*`, Anthropic keys `sk-ant-*`, private key blocks, Google API keys, generic `api_key=…` assignments) and fails the build if any match fires, without printing the matched text.

3. **News media files in `SOURCES/NEWS MEDIA/` must follow the `YYYY-MM-DD - Outlet - Title.md` naming convention** — `sort_audit.py` flags any file in that folder that does not match the `NEWS_MEDIA_PATTERN` regex and emits a violation in its CI-generated audit report.

---

## 6. PERCEPTION LOG

Exact paths opened (read):

- `""` (root directory listing — truncated, ~1000 items)
- `sort_audit.py`
- `.github/` (directory listing)
- `.github/workflows/` (directory listing)
- `.github/scripts/` (directory listing)
- `.github/scripts/daily_rollover.py`
- `.github/workflows/wayback-preserve.yml`
- `.github/workflows/large-file-policy.yml`
- `.github/scripts/check_large_files.py`
- `.github/scripts/check_secret_patterns.py`
- `!-agents.json`
- `!-twitter-extract.py`
- `!-swarm 1-state_manager.py`

**N = 13 paths read.**

**~M rough count of non-.md/.txt files seen but not read from the root listing alone:** approximately 80–100 machine files visible at the root (`.ps1`, `.py`, `.json`, `.sh`, `.yaml`, `.yml`, `.cfg`, `.csv`, `.sig`, `.bat`, `.cmd`, `.js`, `.ts`, `.toml`, `.ics`, `.xml`, `.pdf`, `.patch`, etc.) — plus hundreds more inside the `.github/` tree and the hundreds of `.dotfolder/` agent configuration directories.

Machinery seen but NOT opened:

- `.github/scripts/topology_census.py` (31 KB — vault graph analysis)
- `.github/scripts/review_feedback_loop.py` (94 KB — largest script, AI-driven PR review automation)
- `.github/scripts/metadata_survey.py`, `normalize_tags.py`, `classify_paths.py`
- `.github/workflows/agent-auto-pr.yml`, `batch-arm-merge-queue.yml`, `swarm-mvp-intake.yml`
- `.github/workflows/wayback-audit.yml`
- `!-agents.json` swarm's `swarm.json` (referenced but not opened)
- `.crewai/manifest.json`
- `.claude.json`, `.claude (2).json` (Claude Code config)
- `!-vault-placement-sweep.ps1`, `!-credential-sweep.ps1`, `!-normalize-item-metadata.ps1` (PowerShell hygiene scripts)
- `JFAC Panel Full.mp4.xml` (caption/subtitle file)
- `2026-03-10-Woodward-and-Cook.txt` (JFAC hearing transcript — excluded per .txt rule)
- All ~400+ agent dotfolders (`.claude/`, `.codex/`, `.gemini/`, `.horus/`, `.zeus/`, etc.) — each containing persona configs

---

## 7. THREE [read] ANCHORS

1. **`sort_audit.py`** — Defines the canonical vault ontology (a 100-entry `FOLDER_TAXONOMY` dict mapping path fragments to human labels), walks the entire vault tree, flags files that pattern-match as Idaho bills / hearings / news articles but are not in the correct folder, flags orphans sitting above their proper subfolder, and enforces the `YYYY-MM-DD - Outlet - Title.md` naming rule for news media; writes a dated audit report to `!ADMINISTRATION/`.

2. **`.github/scripts/daily_rollover.py`** — Full to-do carry-forward engine: reads yesterday's daily note for incomplete `- [ ]` tasks in the `[[TO DO LIST]]` section, merges them against the persistent `TO DO LIST.md` active backlog using a structured model (group-ordered, deduped by normalized task key that strips Obsidian Tasks plugin emoji annotations), writes the merged result into today's note with canonical YAML frontmatter, and updates the persistent list — runs every morning as a scheduled GitHub Action.

3. **`.github/workflows/wayback-preserve.yml`** — On every push to `main` touching `SOURCES/**`, `GOVERNMENTS/**`, or `TOPICS/**`: extracts `URL:` frontmatter fields from all changed `.md` files, submits each URL to `https://web.archive.org/save/{url}` via Save Page Now with a rate-limit delay, logs the archived snapshot URLs to a `!/wayback-preserve-YYYY-MM-DD.md` file, and opens a PR with the log.

---

## 8. THREE [*] MARKS

1. **[*]** The hundreds of dotfolders named after mythological figures (`.horus/`, `.zeus/`, `.osiris/`, `.isis/`, `.artemis/`, etc.) and also human names (`.logan/`, `.david/`, `.paul/`, etc.) appear to be Obsidian vault notes formatted as directory stubs or agent persona chambers — likely the Obsidian knowledge graph "people" and "concepts" nodes being stored as folders rather than files, which is unusual and may be an artifact of the vault structure (folders-as-entities pattern). The `.gitconfig`-style file at root suggests this vault originally grew from a home directory sync rather than a clean project repository.

2. **[*]** The `review_feedback_loop.py` (94 KB — the largest single script) almost certainly implements an automated AI-driven PR review cycle: given its name, its size, and the presence of `agent-auto-pr.yml`, `agent-review-gate.yml`, `review-response.yml`, and `review-feedback-loop.yml` workflows, it likely calls an LLM API to review vault PRs (checking content conventions, taxonomy placement, naming) and posts structured review comments — making the vault effectively self-reviewing.

3. **[*]** The JFAC investigation (JFAC Working Groups, open meetings challenge under Idaho Code §74-207, the March 2026 Capitol Correspondents Association letter, the `JFAC Investigation Master Brief 2026-03-12`) is an active live investigative reporting project being tracked in this vault — the `LEVELSET-SUNSET-jfac-open-meetings.md` file referencing a "JFAC agent" and a "LEVELSET" story sunset report strongly suggests Logan was running a dedicated AI agent specifically assigned to monitor and synthesize the JFAC open-meetings story, treating GitHub issues and vault notes as the agent's working memory.
