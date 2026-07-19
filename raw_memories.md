# Raw Memories

Merged stage-1 raw memories (stable ascending thread-id order):

## Thread `019ed800-3c94-7942-b81c-5bbfe3bc4bf4`
updated_at: 2026-07-04T04:17:12+00:00
cwd: /Users/logan
rollout_path: /Users/logan/.codex/sessions/2026/06/17/rollout-2026-06-17T17-52-34-019ed800-3c94-7942-b81c-5bbfe3bc4bf4.jsonl
rollout_summary_file: 2026-06-17T23-52-34-zymg-reorient_idaho_vault_local_mounted_github_status.md

---
description: Reoriented the IDAHO-VAULT local repo, mounted Vault worktree, and live GitHub refs; learned that the local repo is the working `logan/obsidian` branch area while the mounted Vault is intended as protected main, but mounted fetch/status were flaky due to LFS and network issues.
task: inspect/reorient IDAHO-VAULT local repo, mounted Vault, and GitHub refs
task_group: repository-orientation
task_outcome: partial
cwd: /Users/logan
keywords: git, gh, ls-remote, fetch, status, LFS, network, IDAHO-VAULT, logan/obsidian, main, origin/HEAD, mounted Vault
---

### Task 1: Reorient IDAHO-VAULT local repo, mounted Vault, and GitHub refs

task: inspect/reorient IDAHO-VAULT local repo, mounted Vault, and GitHub refs
task_group: repository-orientation
task_outcome: partial

Preference signals:
- when the user said "The local IDAHO-VAULT is the logan/obsidian working branch, while the mounted Vault drive is the main protected branch" -> future agents should treat `/Users/logan/IDAHO-VAULT` as the working area and not assume it is canonical main.
- when the user said "With those new orienting contexts in mind, go explore and reorient to the project status - the VAULT and GitHub" -> future agents should compare local repo, mounted Vault, and live GitHub, not just one surface.
- the user explicitly framed the mounted Vault as protected and the local repo as working -> future agents should avoid writing or force-syncing across that boundary without checking refs first.

Reusable knowledge:
- `/Users/logan/IDAHO-VAULT` is a Git repo with remote `https://github.com/LAF-US/IDAHO-VAULT.git`.
- `/Volumes/Vault` is also a Git worktree (`git rev-parse --show-toplevel` returned `/Volumes/Vault`), not merely a container directory.
- Both local and mounted worktrees were checked out to `logan/obsidian`; `origin/HEAD` points to `origin/main`.
- Live GitHub refs from `git ls-remote` were: `main bf51d924bca050907099ef33b2374670e3514c3e` and `logan/obsidian 1d68a56067de2bacfd40e768a3ec7d5d75ad0830`.
- `gh repo view` confirmed the repo is public and default branch is `main`.
- The local repo had `ahead 9` on `logan/obsidian` and three tracked modifications plus three untracked Markdown files at the time of the final status pass: `! README.md`, `!CROSSFRAMING-Project.md`, `ROAD.md`, `- CLI Reference.md`, `2026-02-01 - Ollama Models How to Pull, List, Update, and Manage Local LLMs.md`, `Python.md`.

Failures and how to do differently:
- `git pull --ff-only origin main` initially failed in the sandbox with `Could not resolve host: github.com`; rerun with network approval succeeded. Future similar pulls may need explicit network approval.
- Mounted-drive `git fetch origin` was flaky and at one point failed with `RPC failed; curl 56 Recv failure: Connection reset by peer` / `fatal: early EOF`; do not rely on mounted refs until a fetch fully completes.
- Mounted-drive `git status` hit a Git LFS clean-filter permission failure on `.obsidian/plugins/handwritten-notes/templates/blank.pdf`; future status checks on `/Volumes/Vault` may need LFS-neutral or escalated handling.
- Broad directory enumeration produced huge output and was not useful; use targeted branch/ref/status commands first.

References:
- `git -C /Users/logan/IDAHO-VAULT remote -v` -> `origin https://github.com/LAF-US/IDAHO-VAULT.git (fetch/push)`
- `git -C /Users/logan/IDAHO-VAULT status --short --branch` -> `## logan/obsidian...origin/logan/obsidian [ahead 9]`
- `git -C /Users/logan/IDAHO-VAULT rev-list --left-right --count main...origin/main` -> `1496 1522` in the stale local-ref view before live GitHub ref confirmation
- `git -C /Users/logan/IDAHO-VAULT rev-list --left-right --count logan/obsidian...origin/logan/obsidian` -> `9 0`
- `git -C /Volumes/Vault rev-parse --short main` -> `59a0742ce`
- `git -C /Volumes/Vault rev-parse --short logan/obsidian` -> `7342e4110`
- `git -C /Users/logan/IDAHO-VAULT rev-parse --short origin/main` -> `bf51d924b`
- `git -C /Users/logan/IDAHO-VAULT rev-parse --short origin/logan/obsidian` -> `1d68a5606`
- `git -C /Users/logan/IDAHO-VAULT log --oneline --decorate -9 origin/logan/obsidian..logan/obsidian` showed the working branch’s unpublished cleanup/quarantine commits, starting with `867984262 (HEAD -> logan/obsidian) docs: record Trash retrieval candidates`
- `gh repo view LAF-US/IDAHO-VAULT --json nameWithOwner,defaultBranchRef,pushedAt,isPrivate` -> `defaultBranchRef.name = main`, `pushedAt = 2026-07-04T03:20:55Z`
- `gh pr list --repo LAF-US/IDAHO-VAULT --state open --limit 10 ...` returned active PRs including `#748`, `#742`, `#741`, `#721`, `#720`, `#691`

## Thread `019f1e3c-a163-7293-97ed-8197a4c2079c`
updated_at: 2026-07-07T04:33:41+00:00
cwd: /Users/logan
rollout_path: /Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl
rollout_summary_file: 2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md

---
description: Compared home vs vault Codex state, mapped the vault as Obsidian+Git+local-state substrate, then triaged open PRs and validated PR #788 as the keystone hotfix for multiline GH command handling.
task: compare ~/.codex with vault .codex; explain Codex/dotdir/vault semantics; inspect open PRs; validate PR #788 hotfix
task_group: /Users/logan/IDAHO-VAULT and /Users/logan
task_outcome: success
cwd: /Users/logan
keywords: .codex, IDAHO-VAULT, Obsidian, GitHub PRs, gh pr list, gh pr checks, gh auth status, review_feedback_loop.py, gh_cli.py, lancedb wheel gap, worktree, multiline argv, NUL bytes, path drift, flattened src package, ABCD
---

### Task 1: Compare `~/.codex` and vault `.codex`

task: compare /Users/logan/.codex with /Users/logan/IDAHO-VAULT/.codex
task_group: local Codex state vs repo-scoped Codex config
task_outcome: success

Preference signals:
- The user asked to compare the home Codex folder with the vault-local Codex folder, then clarified that from the vault they meant the `.codex` folder specifically -> future scope should stay tightly on the target dotdir and not drift into unrelated vault content.

Reusable knowledge:
- `~/.codex` is the live agent state layer: auth, logs, DBs, caches, memories, plugins, history.
- `IDAHO-VAULT/.codex` is a much smaller repo-scoped config/rules/skills surface; the important overlap files are `config.toml`, `rules/default.rules`, and `skills/`.
- The vault-local `.codex` had no pending git changes under `.codex` when checked.

Failures and how to do differently:
- Broad `find /Users/logan -type d -name IDAHO-VAULT` touched protected macOS folders and had to be cut short; future searches should narrow earlier.
- Full-tree `find` on `~/.codex` was too noisy because of caches/plugins/DBs; compare focused subtrees first.

References:
- `ls -la /Users/logan/.codex`
- `find /Users/logan/IDAHO-VAULT/.codex -type f -print`
- `diff -u /Users/logan/.codex/config.toml /Users/logan/IDAHO-VAULT/.codex/config.toml`
- `diff -u /Users/logan/.codex/rules/default.rules /Users/logan/IDAHO-VAULT/.codex/rules/default.rules`
- `diff -rq /Users/logan/.codex/skills /Users/logan/IDAHO-VAULT/.codex/skills`

### Task 2: Explain Codex/dotdirs/vault semantics

task: explain Codex instance vs ~/.codex vs working directory; research dotfile conventions and Obsidian PKM
task_group: conceptual framing for the vault
task_outcome: success

Preference signals:
- The user pressed on the difference between “running from `/Users/logan`” and “running from `~/.codex`,” indicating they want a precise separation between workspace root, tool state, and model identity.
- The user framed the vault as a Git repo plus an Obsidian vault, with the “magic” in the overlap, which is now the durable mental model for future vault work.
- The user described `~/.codex` and other dotdirs as local state files and asked for reflection plus online research on `.` filename conventions.

Reusable knowledge:
- Dotdirs are usually control/state surfaces, not just hidden files.
- In this vault, `.codex`, `.obsidian`, `.github`, and similar dotdirs should be treated as operational layers, not authored content.
- Obsidian’s official positioning matches the user’s framing: file-native, local-first, Markdown-based, plugin-heavy PKM.

References:
- Web sources consulted: Obsidian official site/help, GNU `ls` docs, Python `pathlib`, freedesktop XDG base directory spec.

### Task 3: Open PR triage and backlog shaping

task: inspect the open PR garden in LAF-US/IDAHO-VAULT and identify what is actually stuck
task_group: GitHub PR triage
task_outcome: success

Preference signals:
- The user said most agents work off `main` but they have been working off `logan/obsidian` more frequently -> treat `logan/obsidian` as a real live working surface, not a throwaway branch.
- The user clarified that `superseded` needs a pointer to an explicit and specific heir -> future status labels should preserve lineage and named replacement.
- The user said not every green PR should be merged immediately because some can overwrite daily notes / content zettels -> green checks are not sufficient to canonize a PR in this vault.
- The user invoked the ABCD framing for the brownfield/adversarial/collaboration/dogfood mode and asked to remember it -> use that lens on future Vault/automation triage.

Reusable knowledge:
- In this repo, the PR garden breaks down into infrastructure hotfixes, automation hygiene, generated recurring artifacts, content/zettel changes, and historical/litigation PRs.
- “Green” means the machinery didn’t object, not that the PR should become canon.
- The open PR set at the time was 45 total: 42 targeting `main`, 2 targeting `logan/obsidian`, 1 targeting `mistral/vibe-research`; 34 mergeable, 11 conflicting, 2 drafts, 23 with `review/threads-open`, 9 with `review/suggestions-ready`, 9 `risk/high`.

Failures and how to do differently:
- Initial `gh` calls failed due to sandbox/network restrictions; reran with escalated network permission.
- `gh auth status` reported an invalid default token, so future agents should not assume auth status alone is reliable here even if some GH reads still succeed.

References:
- `gh pr list --repo LAF-US/IDAHO-VAULT --state open --limit 100 ...`
- Key counts: 45 open PRs; 42 `main`, 2 `logan/obsidian`, 1 `mistral/vibe-research`; 34 mergeable, 11 conflicting, 2 drafts, 23 review threads, 9 suggestion-ready, 9 high-risk.
- Highest-leverage PRs identified: #788 (hotfix), #789 (workflow formatting), #784/#785/#780/#782 (small mergeable items), #787 (still failing), and the large/conflicting backlog (#563/#562/#471/#499/#470/#463/#646 etc.).

### Task 4: Inspect and validate PR #788 hotfix

task: inspect PR #788, determine whether its red checks are self-inflicted, and validate the hotfix locally
task_group: GitHub CI debugging / brownfield hotfix
task_outcome: success

Preference signals:
- The user said to start at #788 and keep ABCD in mind -> this is the prioritized first cut.
- The user later clarified that `superseded` needs a named heir, so the broader PR garden should not be treated as garbage; it should be lineage-aware.

Reusable knowledge:
- PR #788 is a one-file hotfix in `.github/scripts/gh_cli.py` (+16/-3) that keeps the `gh` allow-list and NUL rejection while removing newline/CR rejection.
- The failing jobs (`sync-review-state` and `sweep-review-threads`) both checked out `main` at `27bc24b5` and failed inside `review_feedback_loop.py -> pr_github.py -> gh_cli.py` with `ValueError: Command arguments contain disallowed control characters`.
- The newline/CR rejection is wrong for this repo because GraphQL queries and PR/comment bodies are legitimately multiline, and `subprocess.run(..., shell=False)` means a newline inside one argv element is inert here.
- The direct guard should be: allow only `gh`, require string args, reject NUL bytes.

Failures and how to do differently:
- `gh auth status` still reported an invalid default token, but networked PR reads and check inspection worked; future agents should not overtrust auth status as a total blocker.
- The bundled `inspect_pr_checks.py` assumed `python`; use `python3` on this machine.
- `python3 -m pytest` was unavailable in the temp worktree; `python3 -m unittest tests/test_review_feedback_loop.py` was the successful targeted validation.
- `uv run` failed for an environment/dependency reason (`lancedb==0.30.0` wheel gap on macOS x86_64), which should be recognized as unrelated to the code change.
- The temp worktree creation initially tried to fetch a partial/blobless commit and hit DNS in the sandbox; retrying with network permission solved it.

References:
- PR #788: `Hotfix: revert newline/CR rejection in gh_cli._validate_cmd (breaks every multi-line PR comment)`
- Commit under review: `fa59ae990b5e91ffcc7dfb30b1e6b2d846db39f3`
- Failing logs: `review_feedback_loop.py failed: Command arguments contain disallowed control characters`
- Validation commands: `python3 -m unittest tests/test_review_feedback_loop.py`, `python3 -m py_compile .github/scripts/gh_cli.py .github/scripts/review_feedback_loop.py .github/scripts/pr_github.py`
- Temporary detached worktree was created at `/private/tmp/idaho-pr-788` and removed afterward.

### Task 5: Persist vault-side observations and PR context

task: record path-drift / dangling-pointer inventory and keep the branch/local state consistent
task_group: vault governance / local observability
task_outcome: success

Preference signals:
- The user’s branch-local work on `logan/obsidian` is real and ongoing, so branch-local witness notes are part of the live working surface.
- The user’s correction that `superseded` needs a specific heir implies future status docs should avoid vague archival labels.

Reusable knowledge:
- There are two distinct debt classes in the vault: routing pointers (`!/WAKEUP.md`, `!/AGENTS.md`, `!/agents.json`) and executable package topology (`src/idaho_vault/...` vs flattened `src-idaho_vault-...`).
- The vault has path-drift scars across governance docs, generated registries, and Python package layout; these are not the same problem and should be repaired separately.

References:
- Created/committed witness note: `WITNESS-CODEX-DANGLING-POINTERS-2026-07-06.md`
- Earlier witness note: `WITNESS-CODEX-WAKEUP-PATH-DRIFT-2026-07-06.md`
- End state: `logan/obsidian` remained clean and ahead of origin by 5 commits after the inspection/validation work.

## Thread `019f24fa-9b75-7863-bc6a-a48f831fd1ec`
updated_at: 2026-07-02T23:47:44+00:00
cwd: /Users/logan/IDAHO-VAULT
rollout_path: /Users/logan/.codex/sessions/2026/07/02/rollout-2026-07-02T16-37-11-019f24fa-9b75-7863-bc6a-a48f831fd1ec.jsonl
rollout_summary_file: 2026-07-02T22-37-11-SyEA-idaho_vault_secret_scrub_abcd_topology_exploration.md

---
description: Repaired a rewritten branch after a secret scrub, added a root ABCD doctrine note, then explored a vault topology split where docs/CI still reference !/ surfaces while the tree mostly contains root-flattened !- compatibility files; user prefers narrow changes, contradiction mapping, and treating the vault as a running machine rather than a static repo.
task: git history repair, root doctrine note, and vault topology reconnaissance
task_group: /Users/logan/IDAHO-VAULT
task_outcome: success
cwd: /Users/logan/IDAHO-VAULT
keywords: git force-with-lease, secret-pattern guard, meshnetweb portability, generate_agents_bootstrap, ABCD Method, !/WAKEUP.md, !/AGENTS.md, !-WAKEUP.md, !-AGENTS.md, swarm.json, Obsidian Git, running machine, tertium quid
---

### Task 1: secret-scrub git repair

task: repair rewritten git history after secret scrub and reconnect origin/logan/obsidian
task_group: git-repair / vault repo maintenance
task_outcome: success

Preference signals:
- when the repo had been manipulated to scrub a leaked secret, the user asked to “address” it -> future agents should repair the branch/remote state without flattening unrelated vault context.
- when unrelated local noise appeared, the user did not ask for cleanup -> leave unrelated working-tree changes alone unless explicitly requested.

Reusable knowledge:
- `git fetch --prune origin` can be blocked by sandbox writes to `.git/FETCH_HEAD`; rerun with escalated permissions if needed.
- `git push --force-with-lease --set-upstream origin logan/obsidian` successfully republished the scrubbed history and restored tracking.
- `.github/scripts/check_secret_patterns.py` is a repo-native secret guard that reports only file/rule and does not print secret values.
- `python` was not on PATH in this environment; use `python3` for local checks.

Failures and how to do differently:
- The initial fetch failed on sandbox write permissions; use escalation earlier when `.git` metadata needs updating.
- Concurrent Obsidian/Git plugin activity can move the branch during verification; re-fetch before final claims.

References:
- `git push --force-with-lease --set-upstream origin logan/obsidian`
- `python3 .github/scripts/check_secret_patterns.py --paths-from-stdin`
- `secret-pattern guard: OK`
- verified remote move: `a30c58b6e...ba28e7913`

### Task 2: ABCD method note

task: create root-level ABCD-METHOD.md note and commit it
task_group: documentation / doctrine note
task_outcome: success

Preference signals:
- when the user asked to “write a short note at the repo root (ABCD-METHOD.md) and commit it please,” that indicates a preference for small, narrowly scoped commits for simple note additions.

Reusable knowledge:
- New files need `git add` before `git diff --cached` will show the contents.
- The note was kept root-level and isolated from the existing repo noise.

Failures and how to do differently:
- Plain `git diff` showed nothing for the new file until staged; use `git diff --cached` for brand-new files.

References:
- file: `ABCD-METHOD.md`
- commit: `679d5a08c docs: add ABCD method note`

### Task 3: vault topology reconnaissance

task: explore contradictory vault path surfaces and CI/governance expectations
task_group: vault topology / governance reconciliation
task_outcome: success

Preference signals:
- when the user said “It’s as much a LOGIC PUZZLE as it is a CODE PROJECT - Go explore...,” they wanted contradiction mapping and discovery before cleanup.
- when the user said “tertium quid,” they wanted a third framing rather than choosing a binary side.
- when the user said “the VAULT is never static - it is a running machine,” they wanted the system modeled as live routing/interfaces/archives, not as a static repository.

Reusable knowledge:
- Current docs and CI still reference `!/WAKEUP.md`, `!/AGENTS.md`, and `!/agents.json`, while the tree mostly contains root-flattened `!-` counterparts and root compatibility files.
- The migration hinge is commit `68c266064` with message `cleanup: vacate !/ nest, move all files to ROOT with !- prefix`.
- `python3 .github/scripts/meshnetweb_portability_check.py --strict` fails because `!/WAKEUP.md` is missing.
- `python3 .github/scripts/generate_agents_bootstrap.py --check` also fails in the current tree.
- `swarm.json` names `Logan Finney` as principal and treats the registry as durable registration with no liveness inference.
- The safest abstraction for this vault is: keep expected ports open, route them to the right bodies, and distinguish route, archive, and authority.

Failures and how to do differently:
- Do not assume `!/AGENTS.md` or `!/WAKEUP.md` exist just because docs mention them; verify file presence first.
- A shell `test -f ...; test -f ...` chain can mislead if not all failures are aggregated; use a single probe when checking multiple required paths.
- Treat the split as a live interface-maintenance problem, not a cleanup task.

References:
- hinge commit: `68c266064 cleanup: vacate !/ nest, move all files to ROOT with !- prefix`
- failing checks: `missing required file not found: !/WAKEUP.md`, `generate_agents_bootstrap.py --check` exit 1
- compatibility files: `!-WAKEUP.md`, `!-AGENTS.md`, `!-agents.json`, root `WAKEUP.md`, root `AGENTS.md`, root `agents.json`
- concurrent local change: `.obsidian/community-plugins.json` added `smart-connections`

