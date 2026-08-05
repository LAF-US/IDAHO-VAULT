---
authority: LOGAN
created: 2026-05-16
status: permanent
related:
  - CONSTITUTION
  - LAF-USB-PROTOCOL-FRAMEWORK
  - LOCAL-ARBORSCAPE-IDAHO-VAULT-SPLINTERS-2026-05-09
---
# VAULT SYNTHESIS CATALOGUE — 2026-05-16

**Operation:** Reconsolidation of 7 IDAHO-VAULT shards into one canonical repository.  
**Executed by:** The Abhorsen (Claude Code) under LOGAN's direct authority.  
**Result:** 7 directories → 1. `IDAHO-VAULT` is the sole surviving copy.

---

## Shard Inventory (pre-deletion)

| Directory | Type | Files | Disposition |
| --- | --- | --- | --- |
| `IDAHO-VAULT` | Git repo (restored from origin/main) | ~75,995 unique hashes | **CANONICAL — retained** |
| `IDAHO-VAULT-pushable` | Not a git repo | 40,940 | Superseded — deleted |
| `IDAHO-VAULT-agent-fix` | Not a git repo | 35,018 | Superseded — deleted |
| `IDAHO-VAULT-pr-high` | Not a git repo | ~35,017 | Superseded — deleted |
| `IDAHO-VAULT-pr-low` | Not a git repo | ~35,017 | Superseded — deleted |
| `IDAHO-VAULT-clean` | Git repo (clean clone of origin/main) | 16,514 | Superseded — deleted |
| `IDAHO-VAULT-history-rewrite.git` | Bare git repo (old `loganfinney27/IDAHO-VAULT`) | 812 | Archived — history preserved in vault, deleted |

---

## Content Analysis Summary

The restored vault (from `git reset --hard origin/main`) was already 95%+ complete.
The overwhelming majority of files flagged as "unique" in other shards were line-ending
divergences (CRLF vs LF) rather than missing content. Genuine gaps were small.

### Files confirmed as identical (different hash, same content)
All `.github/workflows/*.yml`, `.github/scripts/*.py`, `requirements.txt`, `uv.lock`,
`pyproject.toml`, most `.obsidian/` configs, and the bulk of vault notes — same content,
Windows CRLF in pushable/agent-fix vs LF in origin/main.

### Genuinely unique files copied into vault (commit f09f1037)

**From `IDAHO-VAULT-pushable`:**
- `LAF-USB.md` — LAF Universal Sync Bus concept note
- `USB.md` — USB framework alias note
- `Universal Sync Bus.md` — USB framework alias note
- `JUPYTER-NOTEBOOKS.md` — notebook infrastructure reference

**From `IDAHO-VAULT-agent-fix` / `IDAHO-VAULT-pr-high`:**
- `!/1password-preflight.ps1` — 1Password preflight check script
- `!/credential-sweep.ps1` — credential sweep utility
- `!/sbp-blackboard.json` — SBP blackboard state
- `!/security-sweep.ps1` — security sweep script
- `!/vault-placement-sweep.ps1` — vault placement sweep
- `!/launch-claude-openrouter.cmd` — OpenRouter launch stub
- `!/launch-codex-openrouter.cmd` — OpenRouter Codex launch stub
- `!/resolve-openrouter-secret.ps1` — OpenRouter secret resolution
- `!/branch-sweep-sha-pin-patch-2026-04-22.patch` — branch sweep patch
- `!/LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md` — Five Cores doctrine (nested under `!/`)
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-01-RFC.md`
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-02-DEAD-SEA-PARABLE.md`
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-03-STATEHOUSE-DISPATCH.md`
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-04-DIALOGUE-LUHMANN.md`
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-05-WATER-RIGHTS-BRIEF.md`
- `INBOX/AI-CAPTURES/NOTEBOOKLM-SOURCE-06-DEAD-LETTER.md`
- `archive/2026-04-21-control-surfaces/LEVELSET-CURRENT-depreciated-do-not-rely.md`
- `.obsidian/snippets/custom-admonitions.acaba3.css`

**Also available for review (not auto-merged):**
- `VAULT-CONVENTIONS.from-pushable-2026-05-08.md` — pushable version of VAULT-CONVENTIONS
  with aligned markdown table formatting. Content identical to current `VAULT-CONVENTIONS.md`;
  formatting is cleaner. Logan may wish to adopt and delete this file.

---

## Version Conflict Resolution

### `swarm.json`
- Vault (47,415 bytes, modified 2026-05-16): **AUTHORITATIVE** — most recent, largest,
  includes .yrael/ registration from this session's "Windows Claude" commit.
- Pushable (37,316 bytes, May 8): older local working copy — superseded.
- Agent-fix (29,120 bytes, April 23): oldest — superseded.

### `AGENTS.md`
- Vault and pushable: **byte-for-byte identical** (7,935 bytes each). No conflict.
- Agent-fix / pr-high (5,892 bytes, April 23): older, smaller — superseded.

### `VAULT-CONVENTIONS.md`
- Vault (33,765 bytes, from origin/main): authoritative committed version.
- Pushable (35,975 bytes, May 8): same content, aligned table formatting, more whitespace-clean.
  Preserved as `VAULT-CONVENTIONS.from-pushable-2026-05-08.md` for Logan's optional adoption.

---

## Historical Git Objects Preserved

**Source:** `IDAHO-VAULT-history-rewrite.git` (old `loganfinney27/IDAHO-VAULT` remote)  
**Method:** `git fetch` into `refs/preserved/history-rewrite/` namespace  
**All objects now accessible in the vault's git object store.**

### Preserved branches (28):

| Branch | Head commit | Notes |
| --- | --- | --- |
| `bot/daily-rollover-2026-04-03` | `3dc618d2` | GitHub Actions bot rollover |
| `claude/allow-force-push-to-main` | `1fa914cd` | Decision 23 documentation |
| `claude/repo-size-compliance-5accf9` | `c6c67280` | .gitignore hardening |
| `claude/resolve-pr-conflicts` | `f4ec04a0` | PR #117 merge |
| `claude/update-habit-tracker-todo-p18EW` | `56f86fc9` | Codex tooling alignment |
| `codex/create-manifest.json-specification-and-guidelines` | `6e775c87` | manifest.json spec |
| `codex/fix-high-priority-bug-in-vault-update` | `1f0708c5` | Local REST API secrets |
| `codex/fix-high-priority-bug-in-vault-update-25to8k` | `0867991c` | Local REST API secrets (variant) |
| `codex/github-mention-add-handoff-note-*` (×3) | `0ed9764f` | Codex handoff notes |
| `codex/linear-mention-laf-11-*` | `4f139df0` | LAF-11: routing grammar |
| `codex/linear-mention-laf-12-*` | `160c1436` | LAF-12: DOCKET refactor |
| `codex/linear-mention-laf-15-*` | `58515a9f` | LAF-15: Linear PR sync safeguards |
| `codex/linear-mention-laf-18-*` | `56502b37` | LAF-18: IAM boundary |
| `codex/linear-mention-laf-19-*` | `01edb8e3` | LAF-19: intake brief |
| `codex/linear-mention-laf-23-*` (×2) | `02f5118a` | LAF-23: Gemini partner report |
| `codex/linear-mention-laf-25-*` (×2) | `5b62817c` | LAF-25: Project Hexagonal |
| `codex/linear-mention-laf-7-*` | `9d2f9e46` | LAF-7: swarm coordination |
| `codex/linear-mention-laf-9-*` | `4adf57b2` | LAF-9: vault template system |
| `codex/revise-persona-and-constitutional-files` | `c77d596f` | Gemini persona revision |
| `codex/update-branch-protection-rules` | `6470face` | Branch protection |
| `copilot/debug-github-actions-failures` | `fc3fb8f5` | CI hardening (LAF-26) |
| `copilot/help-logan-overwhelmed` | `80637c7c` | Crisis session branch |
| `gemini/activate-linear-pilot` | `c642efc3` | Linear pilot activation |
| `main` | `cb7c1ab` | Old repo main (early April 2026) |
| `stashed` | `cae87e1` | Stash snapshot |
| `vault-moves-2026-03-30` | (various) | March 30 vault move operations |

**Also preserved:** PR refs `refs/preserved/history-rewrite/pull/1` through `pull/151`
(151 pull request references from `loganfinney27/IDAHO-VAULT`).

---

## Known Irrecoverable Content

**BOOK-OF-GEMINIAEUS source files** — `!/GRIMOIRE/BOOK-OF-GEMINIAEUS/Sheet*.md` (70+ files)
existed only as Smart Env embeddings (`.smart-env/multi/*.ajson`). The `.ajson` files store
vector embeddings only — no source text. These files were not found in any of the 7 shards.
Content is lost. This is documented here as the permanent record.

---

## Post-Reconsolidation Git State (2026-05-16)

```
* main 3b16a100 [origin/main: ahead 3] Merge remote-tracking branch 'origin/main'
```

Local main is 3 commits ahead of origin/main:
1. `309fe6e9` Windows Claude — .yrael/ anchor, session files
2. `f09f1037` fragmentation recovery pass partial — 23 unique files from shards
3. `3b16a100` Merge remote-tracking branch 'origin/main' — absorbed github-actions commits

**Push blocked** by LFS budget — pre-existing condition, not introduced by this operation.
Resolve via LAF-USB when transitioning to THE CITY (MacBook).
