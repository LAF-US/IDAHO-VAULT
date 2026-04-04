---
created: 2026-03-28
status: complete
author: "Codex"
---
# LEVELSET - Codex Archival - 2026-03-28

This is a pruning-safe handoff report for the Codex session that spanned code review, automation hardening, plugin inventory, and Gemini supervision support. If a future agent wakes up cold, trust the repository state and the files named here over chat memory.

## Current git truth

- Current branch at time of writing: `gemini/activate-linear-pilot`
- `HEAD`: `c708bb7` - `Align Codex tooling and harden vault automation`
- `claude/update-habit-tracker-todo-p18EW` also points to `c708bb7` and is `ahead 1` of `origin/claude/update-habit-tracker-todo-p18EW`
- `gemini/activate-linear-pilot` currently has no upstream shown in `git branch -vv`
- `main` is at `10e86e6`

## What Codex completed in this context window

### 1. Review-driven automation fixes

Codex reviewed `claude/update-habit-tracker-todo-p18EW` against `claude/agent-dotfolder-architecture`, found concrete bugs, and implemented the fixes that were low-risk and locally verifiable.

Files materially changed in that work:

- `.github/scripts/daily_rollover.py`
- `.github/scripts/date_tagger.py`
- `.github/workflows/review-response.yml`

Fixes included:

- preserving tasks already present in today's note during rollover
- preventing false "already tagged" skips by checking frontmatter tags instead of arbitrary date strings in file bodies
- making console/status output safe on the Windows environment in this vault
- fixing a frontmatter parsing edge case in `date_tagger.py`
- preventing rollover logic from misclassifying alternate TODO headings
- making the review workflow actually disable GitHub auto-merge instead of only relabeling a PR

Verification performed during the session included:

- `python .github/scripts/daily_rollover.py --date 2026-03-29 --dry-run`
- `python .github/scripts/date_tagger.py --dry-run`
- targeted function-level checks for frontmatter/tag and todo merge behavior

### 2. Codex/OpenAI architecture and implementation hardening

Codex aligned the repo's Codex/OpenAI setup and committed that work in `c708bb7`.

Key files in that commit:

- `.codex/config.toml`
- `.codex/CODEX.md`
- `AGENTS.md`
- `.github/scripts/linear_brief_generator.py`
- `.github/workflows/linear-brief.yml`
- `.gitignore`
- `swarm.json`
- `.vscode/mcp.json`

Purpose of that commit:

- align Codex config/docs with current repo governance
- use the current OpenAI Responses API shape in `linear_brief_generator.py`
- make repo-scoped MCP config explicit for Codex/VS Code
- keep root `AGENTS.md` consistent as the cross-tool autoload shim

### 3. Plugin auth inventory

Codex created a new report artifact:

- `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md`

This file is currently untracked on disk and was not committed in this session.

Read-only connector findings in that report:

- GitHub verified
- Linear verified
- Slack verified-read-only
- Google Calendar verified-read-only
- Google Drive verified-read-only
- Hugging Face verified-read-only
- Cloudflare `not-directly-probeable`

Recommendation captured in that report:

- `Phase 1 = Linear-first pilot`

Guardrail posture captured there:

- Vault remains the durable record
- Slack remains breadcrumb-only
- no multi-plugin orchestration until a Linear-first pilot is stable

## Gemini support and failure modes observed

Gemini was being supervised in parallel by Logan and Claude, with Codex providing calibration prompts and diagnostics.

Two Gemini Code Assist extension failure modes were observed:

### 1. Stale settings reference crash

Error shape:

- `vscode-userdata:/.../settings.json`
- `invalid line number`

Interpretation:

- Gemini Code Assist `2.75.0` was attempting to process a stale saved range in VS Code user settings, not a vault file

### 2. Agent/search runtime crash

Error shape:

- after `SearchText`
- `Cannot read properties of undefined (reading 'message')`

Evidence:

- log path: `C:\Users\loganf\AppData\Roaming\Code\logs\20260328T160919\window1\exthost\output_logging_20260328T160921\5-Gemini Code Assist Agent.log`
- stack text pointed into Gemini's own runtime (`a2a-server.mjs` / `_Task.acceptAgentMessage`)

Interpretation:

- this also appears to be an extension/runtime bug, not a vault bug

Known-good mitigation pattern during this session:

- use a fresh Gemini chat
- ignore `vscode-userdata:/.../settings.json`
- use repo-local files only
- avoid `SearchText`, repo-wide discovery, and aggressive agentic search on the first turn
- prefer file-by-file prompts with explicit paths

## Governance and boundary truths reaffirmed in-session

- `!/` is the control plane for governance, levelsets, protocols, and records
- root-flat `.md` files are intentional note corpus, not proof of disorder
- persona dotfolders are protected infrastructure
- do not touch `.gemini/` or other persona folders unless explicitly directed or it is your own dotfolder
- `.github/` is shared automation space, not a cleanup target

Specific live boundary call made during this session:

- if Gemini creates an activity/admin record named `GEMINI-ACTIVITY.md`, the correct home is `!/GEMINI-ACTIVITY.md`, not vault-root `GEMINI-ACTIVITY.md`

At the time of writing, Claude had already relayed a pause/correction to Gemini on that exact path question.

## Dirty worktree warning

The worktree is dirty well beyond Codex's own scope. Do not treat the current diff as a Codex-only change set.

Notable modified/deleted/untracked areas visible at write time include:

- `!/!/LEVELSET-CURRENT.md`
- `2026-03-28.md`
- `Centerville.md`
- `Idaho Republican Party.md`
- `INBOX/` file moves/deletions
- `swarm/README.md`
- `swarm/__init__.py`
- `swarm/app.py`
- `swarm/tests/test_app.py`
- multiple new untracked root notes and reports

Important implication:

- do not run broad cleanup, branch surgery, or "helpful" staging without re-scoping first

## What another agent should read first after pruning

If this session is compacted or killed, reorient in this order:

1. `!/AGENTS.md`
2. `AGENTS.md`
3. `!/VAULT-CONVENTIONS.md`
4. `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md`
5. `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md`

If Gemini debugging resumes, also consult:

- `C:\Users\loganf\AppData\Roaming\Code\logs\20260328T160919\window1\exthost\output_logging_20260328T160921\5-Gemini Code Assist Agent.log`

## Safe next actions

1. Decide whether `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` should be staged and committed.
2. Let Gemini finish or confirm the `!/GEMINI-ACTIVITY.md` path correction before any push from the Gemini side.
3. If Gemini crashes again, reset it with a fresh chat plus repo-local, file-by-file prompts.
4. If plugin work continues, scope the Linear-first pilot narrowly before any live writes.
5. Avoid broad git cleanup until the unrelated `swarm/`, `INBOX/`, and note churn is intentionally triaged.

## Last word

The most durable outputs from this Codex window are:

- commit `c708bb7`
- `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md`
- this archival levelset

Everything else should be treated as active, shared, and potentially in-flight.
