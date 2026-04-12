---
authority: LOGAN
related:
- 1Password
- 2023-12-19 - GIAC meeting
- '2026-04-02'
- '218'
- '260'
- AGENTS
- API
- Act
- Ada County
- Boise
- Brad Little
- CLAUDE
- CLI
- CONSTITUTION
- Copilot
- DAILY NOTE
- DAILY NOTE TEMPLATE
- DECISIONS
- DOS
- GEMINI
- GitHub
- HFS
- Idaho
- Idaho Legislature
- Idaho Public Television
- Idaho Reports
- Idaho Statesman
- LEVELSET
- Logan Finney
- Logan's
- MCP
- OBSIDIAN DAILY NOTE
- Obsidian
- PROJECT
- PROTOCOL
- README
- SSH
- THE
- The world is quiet here
- UTC
- VAULT-METADATA-STANDARD
- VAULT-TEMPLATES
- VAULT-ZONES
- _AUX
- agent
- codex
- coordination
- doctrine
- election
- emoji
- format
- infrastructure
- legislative
- links
- meeting
- passwords
- persona
- syntax
- systems
- template
---

# VAULT-CONVENTIONS Ã¢â‚¬â€ Shared Reference for All Agents



This file contains the vault conventions shared by all AI agents working in IDAHO-VAULT. Individual agent instructions (`CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md`) reference this file for vault structure, naming, frontmatter, and protocol.



**Owner:** Logan Finney Ã¢â‚¬â€ journalist, producer/reporter, Idaho Reports / Idaho Public Television

**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)

**Platform:** Obsidian.md vault, version-controlled with git



---



## Vault Purpose



This is a personal journalism research vault. It contains notes on Idaho politics, government, legislation, people, organizations, and source documents. All committed content is **on the record** and should be treated as **publishable**.



---



## Authority Chain



This file is the shared delegation layer for day-to-day vault behavior. When rules overlap, use this precedence:

1. `!/README.md` for orientation and canonical path language
2. `VAULT-CONVENTIONS.md` for shared routing and write conventions
3. `VAULT-METADATA-STANDARD.md` for governed-note metadata and lifecycle rules
4. `VAULT-TEMPLATES.md` for class, filename, and template expectations
5. Live implementation wiring in `.obsidian/`, `.github/`, and `manifest.json` only insofar as it conforms to the documents above

`!/VAULT-CONVENTIONS.md` is a routing shim for bootstrap stability.
`VAULT-METADATA-STANDARD.md` outranks template guidance whenever metadata fields or lifecycle semantics overlap.


---



## Vault Structure



This vault is intentionally hybrid. Governance and automation live in dedicated

system folders, while a large share of the journalism corpus lives directly at

repo root. Do not assume that a root-heavy layout means the vault is

"unorganized," and do not use older taxonomy examples as permission to

restructure the current vault.



### Root Folder Semantics



| Path | Meaning | Agent rule |

| --- | --- | --- |

| `!/` | Stable routing, bootstrap aliases, shims, DOCKET, and control-plane breadcrumbs | Read first for stable system paths. Do not restructure, rename, or clean without Logan's explicit direction. |
| Repo root `.md` files | Primary note corpus and working knowledge base | Root-flat notes are intentional. Do not mass-move them into category folders without explicit authorization. |

| `INBOX/` | Intake and staging area | Use for intake only when directed. Do not auto-empty or normalize it. |

| `swarm/` | Swarm support artifacts and structured coordination data | Treat as infrastructure, not general note taxonomy. |

| `.github/` | Automation, workflows, scripts, and GitHub-specific instructions | Safe to modify only within assigned automation work and governance boundaries. |

| `.obsidian/` | Obsidian application configuration | Not note content. Respect sync and git boundaries before changing anything here. |

| Agent/persona dotfolders such as `.claude/`, `.codex/`, `.gemini/`, `.grok/`, `.deepseek/`, `.google/`, `.meta/`, `.microsoft/`, `.perplexity/`, `.persephone/`, `.zagreus/`, `.bartimaeus/` | Agent/persona shims, governance files, and local identity infrastructure | Protected. Do not delete, rename, consolidate, or "clean up" these folders unless it is your own dotfolder or Logan explicitly directs the change. |

| Tooling folders such as `.venv/`, `.vscode/`, `.qodo/` | Local environment or tool support | Do not infer that a hidden folder is disposable just because it is small, empty, or unfamiliar. |



### Folder Rules For Emerging Agents



- Treat `!/` as the vault control-plane routing layer.
- Treat root-flat notes as a deliberate operating choice, not a mistake to fix.

- Treat persona dotfolders as keystone infrastructure, even when they contain

  only a shim file or appear empty.

- If a folder's purpose is unclear, stop and ask Logan before proposing

  deletion, consolidation, or mass moves.

- Historical references to older folder trees are descriptive context, not

  standing authorization to reorganize the live vault.



---



## Naming Conventions



| Type           | Pattern                                | Example                                        |

| -------------- | -------------------------------------- | ---------------------------------------------- |

| Bills          | `(YYYY) Bill Type Number.md`           | `(2026) House Bill 24.md`                      |

| News articles  | `YYYY-MM-DD - Outlet - Title.md`       | `2024-01-15 - Idaho Statesman - Title here.md` |

| Hearings       | `YYYY-MM-DD - Committee or Meeting.md` | `2023-12-19 - GIAC meeting.md`                 |

| People         | `Full Name.md`                         | `Brad Little.md`                               |

| Other entities | Descriptive name, title case           | `Ada County.md`                                |



### Obsidian Filename Rule

In this vault, the filename is part of the note interface. Obsidian uses it in
the sidebar, quick switcher, wikilinks, backlinks, embeds, and everyday
retrieval.

Rules:

1. Optimize note filenames for Obsidian-visible identity and human retrieval,
   not just filesystem safety.
2. Keep filenames cross-platform safe, but preserve the natural note title when
   the platform allows it.
3. When filesystem constraints force a compromise, preserve the exact work name
   in frontmatter `title` and add `aliases` for likely link forms.
4. Do not replace a human-facing title with an arbitrary slug when the note is
   meant to be read, linked, and found by humans inside Obsidian.



---



## Document Classes and Templates



The canonical class/template system is defined in `!/VAULT-TEMPLATES.md`.



Rules:



1. Every new note should be created from a recognized document class first.

2. Required classes must use their canonical template and naming pattern.

3. Unknown/ambiguous notes are staged as `misc_reference` in place until they can be reclassified.

4. Class and template schema changes are governance changes, not ad-hoc formatting edits.



See `!/VAULT-TEMPLATES.md` for:



- class registry

- template IDs

- required frontmatter keys

- routing/maintenance workflow

- constitutional interaction model



### Daily Note Infrastructure



Daily notes currently use a specialized operational path instead of a full template-registry migration:



- active creation template: `DAILY NOTE TEMPLATE.md`

- active Obsidian wiring: `.obsidian/daily-notes.json`

- active normalization/carryforward scripts: `.github/scripts/daily_rollover.py`, `.github/scripts/tidy_daily_notes.py`, `.github/scripts/expand_date_aliases.py`



Do not treat `DAILY NOTE.md`, `OBSIDIAN DAILY NOTE.md`, or `template.md` as active daily-note infrastructure.



Concrete Markdown files named by tracked Obsidian client config as templates must also be mirrored into the machine-readable swarm tracking layer:



- `manifest.json` for execution/interface inventory

- `swarm.json` for the broader swarm and connector registry



If a plugin exposes only a template folder or keeps its settings private via Obsidian Sync, record that honestly as `folder_only` or `installed_untracked_config` rather than inventing concrete template files.



---



## Frontmatter Conventions



All Obsidian files use YAML frontmatter. The canonical header/footer policy is defined in `!/VAULT-METADATA-STANDARD.md` and should be treated as the source of truth for required fields, optional fields, lifecycle status, timestamp format, authorship, and authority.



### Baseline Required Fields (all governed markdown notes)



```yaml

title: "<document title>"

updated: YYYY-MM-DD

status: <draft|active|superseded|archived>

authority: "<decision authority>"

```



### Type-Specific Additions



Tags are stored in frontmatter only. Treat `tags:` as the canonical tag source for a note, use lowercase slash-path tags, and keep date/session/election tags as tags when they are part of the note taxonomy.



**People:**



```yaml

tags:

  - party/republican # or party/democratic

  - people/elected/legislative

residence: "Boise"

```



**News articles:**



```yaml

author: "Reporter Name"

outlet: "Outlet Name"

URL: https://...

tags:

  - media/articles

  - 2024/01/15

```



**Bills:**



```yaml

tags:

  - bills

  - 2026/session

aliases:

  - HB 24

cmte: ["Committee Name"]

sponsor: ["Sponsor Name"]

URL: https://legislature.idaho.gov/...

```



**Hearings:**



```yaml

cmte: "Committee Name"

tags:

  - 2023/12/19

```



---



## Wikilinks



Use `Full Name` for all internal links Ã¢â‚¬â€ people, places, organizations, bills, topics. This is how Obsidian builds the knowledge graph. Link densely in source documents.



---



## File Types



- **Markdown** = human product, attributable to Logan. Notes, stories, analysis.

- **Python** = machine/procedural product, attributable to AI agents. Scripts, scrapers, automation.

- **Administrative** = vault infrastructure. Instruction files, audit reports.



---



## Direct-Write Workflow



1. Determine whether the target artifact belongs to the control plane or the note corpus.

2. If it is governance or operational doctrine, prefer the root canonical files unless the artifact is specifically a routing shim, breadcrumb, DOCKET update, or bootstrap surface.
3. If it is corpus content, choose a document class first, then create the note at repo root using the canonical filename pattern and required metadata.
4. For Obsidian-facing notes, treat the filename as part of the user
   interface: choose a human-recognizable note name first, then use `title` and
   `aliases` to preserve exact forms when needed.

5. For daily notes, let Obsidian create the file from `DAILY NOTE TEMPLATE.md` and let the daily-note scripts maintain carryforward and normalization.

6. GitHub automation may write files and update transport artifacts, but those writes must conform to vault doctrine rather than redefine it.



---



## Authority and Coordination Model



- **Vault** is the canonical memory and doctrine layer.
- **GitHub** is the execution and transport layer for workflows, `manifest.json`, lock state, PRs, and automation output.

- **Linear** is execution-state support for ownership, status, and planning.

- **Chat/Slack** is transient coordination; durable decisions or context must be promoted into the vault and/or execution systems.

- **Core connector hub:** GitHub, Linear, and Slack form the active connector hub. GitHub executes, Linear tracks execution state, and Slack carries tertiary paging/breadcrumbs only.

- **Adjunct connectors:** Gmail, Google Calendar, Google Drive, and Box are read-first context lanes. They may inform work, but they do not become durable authorities until their outputs are explicitly promoted.

- **Deferred platform connectors:** Cloudflare and Hugging Face are classified in the connector registry but are not active operating authorities without a separate Logan-approved activation plan.

- **Registry surfaces:** `swarm.json` is the machine-readable connector registry. `SPEC-CONNECTOR-HUB-2026-04-09.md` is the human-readable bridge for the connector hub and maze census.

Root governance files hold doctrine. The `!/` layer keeps bootstrap paths and control-plane breadcrumbs stable across tools.


---



## Vault Ã¢â€ â€ Linear Operating Model Mapping



| Layer (purpose)            | Vault (canonical memory)                                                                                         | Linear (execution state)                                           | Chat/Slack (ephemeral)                                              |

| -------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |

| **Core / Mind**<br>governing doctrine | Constitution, Charter, Codex, decision logs, doctrine/guidance updates, LEVELSET snapshots                           | Work items to draft/revise doctrine; link PRs/issues to vault artifacts | Quick clarifications; capture any decision back into Vault/PR issue |

| **Periphery / Body**<br>operating mechanics | Protocols, procedures, preferences, templates/SOPs, stable checklists, automation docs                                   | Tasks/epics for doing the work, tracking status, ownership, deadlines | Live coordination, handoffs, Q&A; move outcomes to Linear/Vault     |

| **Ghost / Soul**<br>interpretive/cultural layer | Guidelines, grimoire/interpretive notes, guestbook/cultural norms, context vaults                                          | Action items emerging from interpretive work (e.g., follow-ups, retro tasks) | Brainstorms, vibes, drafts; memorialize decisions/insights in Vault |

| **`!` spaces**<br>operational infrastructure | System files, DOCKET, LEVELSET, agent routing, audit/log artifacts, workflow outputs that must persist                     | Incidents/infra tasks, runbooks in execution, workflow status, tickets | Real-time paging/alerts; record outcomes in Linear and Vault        |



**Decision Rule:** Vault holds doctrine and context that must persist. GitHub executes workflows and transport state. Linear tracks execution, owners, and current state. Chat/Slack is transient coordination Ã¢â‚¬â€ any decision or durable context must be promoted promptly into Vault and/or the execution systems.



---



## Automation



### Active Automation Scripts



| Script                 | Purpose                                     | Trigger                         |

| ---------------------- | ------------------------------------------- | ------------------------------- |

| `sort_audit.py`        | Audits vault structure for misplaced files  | Weekly Monday 6 AM UTC + manual |

| `idaho_leg_scraper.py` | Scrapes Idaho Legislature bill data         | Daily 6 AM MT + manual          |

| `post_digest.py`       | Posts bill activity to GitHub Issues digest | Called by scraper workflow      |

| `propose_moves.py`     | Proposes vault file reorganization          | Weekly Monday 7 AM UTC + manual |

| `wayback_audit.py`     | Audits URL preservation in Wayback Machine  | Weekly Monday 8 AM UTC + manual |

| `daily_rollover.py`    | Rolls over daily note tasks                 | Daily 4 AM MT                   |

| `linear_brief_generator.py` | Generates research briefs from Linear issues | Called by linear-brief workflow |

| `classify_paths.py`    | Classifies changed files by risk tier       | Called by auto-pr workflow      |

| `validate_content.py`  | Validates vault content structure           | Called by multiple workflows    |

| `post_levelset_closure.py` | Notifies when LEVELSET files ready for closure | Called by levelset-closure workflow |



### Utility Scripts (Manual Use Only)



These scripts are not called by automated workflows but are available for manual vault maintenance:



| Script                  | Purpose                                                      | Usage                               |

| ----------------------- | ------------------------------------------------------------ | ----------------------------------- |

| `expand_date_aliases.py` | One-off: expands date alias frontmatter in daily notes       | `python3 .github/scripts/expand_date_aliases.py [--dry-run]` |

| `normalize_tags.py`      | Normalizes Markdown note tags across vault                   | `python3 .github/scripts/normalize_tags.py [--write]` |

| `tidy_daily_notes.py`    | One-off: normalizes daily note frontmatter structure         | `python3 .github/scripts/tidy_daily_notes.py [--dry-run]` |

| `obsidian_rest_api_client.py` | REST API client for Obsidian Local REST API plugin    | Import/use in other scripts as needed |

| `mcp_guardrails.py`      | MCP protocol guardrails (reserved for future MCP integration) | Import/use in MCP-enabled scripts   |



Scripts live in `.github/scripts/`. Workflows live in `.github/workflows/`. Scripts that commit to the repo use `git config user.name "github-actions[bot]"`. Dependencies are tracked in `.github/scripts/requirements-scraper.txt`.



### Secret Management via 1Password



**Requirement:** All credentials (API keys, tokens, SSH keys, passwords) are managed centrally in 1Password. GitHub Actions uses `OP_SERVICE_ACCOUNT_TOKEN` plus runtime secret references to fetch secrets. No credentials are hardcoded in workflows or stored directly in GitHub Secrets (with the exception of the service account token itself).



**Scope:**

- Developer machines: 1Password CLI + SSH agent for local authentication and git signing

- GitHub Actions: service account token plus runtime secret references fetch secrets inside workflows

- All secrets are rotated on defined schedules (see `.op/secrets.template.md`)



**Key files:**

- `.op/SETUP.md` Ã¢â‚¬â€ Installation and configuration guide for developers

- `.op/secrets.template.md` Ã¢â‚¬â€ Secret inventory and rotation schedule

- `.github/workflows/1password-secret-template.yml` Ã¢â‚¬â€ Example workflow using 1Password



**Rules:**

1. Never commit credentials to the repo, even in `.env` files or example configs

2. All GitHub Actions secrets (except `OP_SERVICE_ACCOUNT_TOKEN`) are fetched from 1Password at runtime

3. Do not assume a developer machine's visible desktop vault names match CI secret-reference paths such as `op://vault-operations/...`

4. Use `::add-mask::` in workflows to prevent accidental credential leakage in logs

5. Rotate credentials on schedule; update `.op/secrets.template.md` with rotation date

6. SSH keys for git signing are managed via 1Password SSH agent on developer machines



**Implementation checklist:**

- [ ] Install 1Password CLI on developer machine

- [ ] Configure 1Password SSH agent and register git signing key

- [ ] Create 1Password service account and generate `OP_SERVICE_ACCOUNT_TOKEN`

- [ ] Add `OP_SERVICE_ACCOUNT_TOKEN` to GitHub Actions secrets

- [ ] Migrate existing secrets from GitHub Secrets Ã¢â€ â€™ 1Password vault

- [ ] Update workflows to fetch secrets via `op item get`



### MCP Action Logging Requirement (Mandatory)



Any automation in `.github/workflows/` or `.github/scripts/` that performs an MCP-mediated action **must** emit a structured log entry using the following reusable template.



#### Required MCP Action Log Template



```yaml

mcp_action_log:

  action_type: "<action type>"

  system_or_resource_id: "<system/resource id>"

  initiating_agent: "<initiating agent>"

  correlation_id: "<correlation id>"

  outcome: "<success|failure>"

  retry_count: <integer>

  related_ref: "<issue|pr|handoff file link>"

```



#### Field Definitions



- `action_type`: The MCP operation category (for example: `read_resource`, `write_resource`, `invoke_tool`).

- `system_or_resource_id`: The MCP server/system identifier or concrete resource identifier targeted by the action.

- `initiating_agent`: Agent identity that initiated the MCP action (for example: `agent:codex`, `agent:claude-code`, `github-actions[bot]`).

- `correlation_id`: Stable ID used to correlate retries and downstream events for the same logical action.

- `outcome`: Final attempt status. Must be exactly `success` or `failure`.

- `retry_count`: Number of retries attempted before final outcome (`0` for first-try success/failure).

- `related_ref`: URL or path to the related coordination artifact (GitHub Issue, PR, or `HANDOFF-*.md` file).



#### Enforcement Scope



- Applies to **all** MCP-mediated automation behavior implemented in:

  - `.github/workflows/**`

  - `.github/scripts/**`

- New MCP-capable workflow/script changes are non-compliant unless this template is logged for each MCP action attempt sequence.



---



## Sourcing Protocol



- **On the record:** Safe for public repo. All committed content is on the record.

- **On background:** Vault-safe but identity-protected. Use carefully Ã¢â‚¬â€ this is a public repo.

- **Off the record:** Ephemeral. Do not log, do not store, do not commit. If Logan says something is off the record, it does not go in files, code, comments, or commit messages.



When uncertain about sourcing category, **ask Logan**.



---



## Obsidian Sync / Git Boundary

Two systems share the vault. They have distinct, non-overlapping responsibilities.

| Layer | Obsidian Sync | Git / GitHub |
| --- | --- | --- |
| Vault content (`.md` files) | Syncs across devices | Tracked |
| Plugin code (`main.js`, `manifest.json`) | Desktop only (see below) | Tracked — public record |
| Plugin settings (`data.json`) | Desktop only, E2E encrypted | **Gitignored** — never reaches GitHub |
| `community-plugins.json` | Per-device (not synced) | Tracked — canonical desktop plugin list |
| Workspace state (`workspace.json`, `graph.json`) | Per-device | Gitignored — machine-local noise |

**Rule:** Obsidian Sync is the private courier for credentials and machine state. Git is the public record for vault content and plugin presence. The `.gitignore` wildcard `.obsidian/plugins/*/data.json` is the firewall — no `data.json` reaches GitHub without a deliberate `git add --force`.

### Device Roles

| Device | Role | Community Plugins |
| --- | --- | --- |
| **Desktop** (Windows) | Engine room — full plugin stack, git, MCP servers, Linter, Breadcrumbs, agent infrastructure | 26 (curated tier) |
| **Mobile** (Pixel) | Capture device — quick-jot notepad, read access | 0 (bare Obsidian) |

The phone writes `.md` files. The desktop processes them.

### Obsidian Sync Settings — Desktop

| Toggle | Setting |
| --- | --- |
| Core settings | ON |
| Appearance | ON |
| Hotkeys | ON |
| Active core plugins | ON |
| Active community plugins | ON |
| Installed community plugins | ON |

### Obsidian Sync Settings — Mobile (Pixel)

| Toggle | Setting |
| --- | --- |
| Core settings | ON |
| Appearance | ON |
| Hotkeys | ON |
| Active core plugins | OFF — phone does not need slides, audio-recorder, webviewer, etc. |
| Active community plugins | OFF — decouples plugin lists; desktop keeps 26, phone keeps 0 |
| Installed community plugins | OFF — phone does not need 140 plugin directories |

### Why Per-Device Plugin Lists

Obsidian Sync defaults to pushing the same plugin list to all devices. On a 20K-file vault, the desktop's 26-plugin stack (Dataview indexing, Omnisearch search index, Linter watching saves, MCP tools looking for a REST API server) overwhelms mobile. Disabling community plugin sync on the phone lets each device run its own appropriate stack while content (`.md` files), appearance, and hotkeys still flow both ways.

### Conflict Duplicates

When both devices edit the same config file between syncs, Obsidian creates a `(2)` copy (e.g., `app (2).json`). These are already gitignored via `.obsidian/**(2)*.json`. Delete them when found — Obsidian only reads the original filename.


## Git Practices



- Branch naming:

  - `claude/description-sessionId` for Claude Code branches

  - `copilot/description` for GitHub Copilot branches

  - `gemini/description` for Gemini agent branches

- Commit messages: Clear, descriptive, explain the "why"

- Never force-push without explicit permission

- Check in before anything irreversible

- The legislature scraper workflow commits directly to main for automated bill updates



---




## Character Set & Notation

Emojis are **first-class vault syntax** as of 2026-04-02 (Logan, superseding prior ASCII-only directive).

- Authority: [Unicode Consortium](https://unicode.org) â€” the canonical source for emoji definitions, codepoints, and names (see [full emoji list](https://unicode.org/emoji/charts/full-emoji-list.html))
- Emojis may appear in note titles, frontmatter, body text, DOCKET entries, and commit messages
- Use semantically â€” emojis carry meaning and should reinforce, not decorate

---
## Guiding Principles

- The five W's: who, what, when, where, why
- The four C's: collect, capture, catalogue, collate
- Public repo = on the record
- Markdown for human product. Python for machine/procedural product.
- Do not over-engineer. Keep it simple. Only build what's needed now.
- Check in before anything irreversible.
- **DISCOVERY BEFORE INVENTION:** Logan has made architectural decisions that live in the vault's structure, naming patterns, frontmatter fields, seed files, and file placement — not always in governance documents. Agents must READ existing conventions before proposing new ones. The vault is the record of decisions already made. Follow them; do not reinvent them. If you encounter a pattern you don't recognize, investigate before overwriting it.



---



## Conversation Taxonomy



Logan uses a naming convention for AI conversations:



| Prefix | Purpose |

| --- | --- |

| PERMANENT: | Central, non-deletable conversations |

| PERSISTENT: | Long-running, role-specific conversations |

| TASK: | Bounded, completable work items |

| STORY: | Journalism story development |

| PROJECT: | Multi-session projects |

| ISSUE: | Problem resolution |

| INQUIRY: | Research questions |



---



## Swarm Coordination



All agents coordinate through THE COURTROOM: `!/!/!/! The world is quiet here/DOCKET.md`



That file is the live status board. Read it to orient. Update it when you start or finish work.



Task assignment flows through GitHub Issues (with `agent:*` labels) and Linear (SWARM label). Slack carries breadcrumbs. The vault is the record.



---



## Vault Ã¢â€ â€ Linear Operating Model Mapping



Use this mapping to decide where work should live and what should remain ephemeral.



| Layer | Vault Role | Linear Role | Ephemeral Chat/Slack Role |

| --- | --- | --- | --- |

| **Core / Mind** (governing doctrine) | Canonical source of truth for doctrine and constraints (`CONSTITUTION.md`, `PROTOCOL.md`, `AGENTS.md`, `VAULT-CONVENTIONS.md`, `VAULT-ZONES.md`, `DECISIONS.md`) | Reference only in issue/project descriptions as links; do not duplicate doctrine text in Linear | Clarify intent in discussion, but final doctrine decisions must be written to vault governance files |

| **Periphery / Body** (operating mechanics) | Durable playbooks, runbooks, workflows, scripts, and system notes that define *how work is executed* | Active execution layer: projects, issues, milestones, priorities, assignees, and status tracking | Fast coordination, blockers, and quick decisions during execution; summarize durable outcomes back into vault or Linear |

| **Ghost / Soul** (interpretive/cultural layer) | Long-form narrative context, principles-in-practice, interpretive guidance, retrospectives that should persist | Lightweight pointers (issue comments/docs) to related vault narrative notes when relevant to work | Sensemaking, live interpretation, tone checks, brainstorming; keep ephemeral unless it becomes a durable principle |

| **`!` spaces** (operational infrastructure) | System control plane: DOCKET, handoffs, LEVELSETs, MCP plans, audits, routing files, and machine-operational records | Coordination mirror for assignment and accountability (SWARM-labeled issues) | Notifications/breadcrumbs only; do not treat Slack as system-of-record for infra state |



### Decision Rule



- **Vault:** Canonical memory and doctrine (what is true, why it is true, and durable operating knowledge).

- **Linear:** Work management and execution state (what is being done, by whom, and current status).

- **Chat/Slack:** Ephemeral coordination (what is being discussed right now).



If a decision must be recoverable in six months, store it in the vault. If it needs owner + due date + status, track it in Linear. If it is transient discussion, keep it in chat/Slack.



---



## Portable Path Standard (NETWEB)



The vault must work identically on **any platform** — Windows (NTFS), macOS (APFS/HFS+), Linux (ext4), iOS/Android (Obsidian mobile), and CI runners (GitHub Actions). Both NTFS and APFS are **case-insensitive**; only Linux is case-sensitive. This standard targets the **lowest common denominator** of all target filesystems.



### Forbidden filenames (any extension, any case)

`AUX`, `CON`, `NUL`, `PRN`, `COM0`–`COM9`, `LPT0`–`LPT9`

These are Windows reserved device names inherited from MS-DOS. They cannot exist as files on NTFS regardless of extension.



### Aliasing convention

When a stub or note would collide with a reserved name or a case-insensitive duplicate:

1. Prefix the filename with `_` (e.g., `AUX.md` becomes `_AUX.md`)
2. Add `aliases: [ORIGINAL]` to the YAML frontmatter so Obsidian wikilinks (`AUX`) still resolve

This preserves the connectome while respecting filesystem constraints.



### Case uniqueness

Filenames within any single directory **must be case-unique**. `Act.md` and `ACT.md` cannot coexist — NTFS and APFS silently overwrite one on checkout. When creating stubs or notes, check for existing files that differ only in case.



### Forbidden path patterns

- Trailing period (`.`) or space (` `) in any directory or file name
- Characters illegal on Windows: `< > : " | ? *`
- Colons (`:`) in filenames (illegal on macOS — internal path separator)
- Paths exceeding **218 characters** from repo root (NTFS MAX_PATH 260 minus typical local prefix)



### Enforcement

| Layer | Mechanism | Scope |
| --- | --- | --- |
| `.gitignore` | Case-insensitive patterns for reserved names | Advisory — prevents accidental `git add` |
| `check-portable-paths.yml` | CI workflow on every PR and push to `main` | **Hard gate** — blocks merge on violation |
| Agent discipline | All agents must check before creating files | Preventive |



### Reference

- [Microsoft: Naming Files, Paths, and Namespaces](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file)
- [Apple File System Guide](https://developer.apple.com/documentation/foundation/file_system)
