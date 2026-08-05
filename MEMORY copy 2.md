# Task Group: IDAHO-VAULT GitHub PR triage and multiline `gh` hotfix validation

scope: Use this when triaging the live IDAHO-VAULT PR garden, interpreting review-loop CI failures, or validating the multiline `gh_cli.py` hotfix around PR #788 without collapsing vault lineage/context.
applies_to: cwd=/Users/logan GitHub-facing workflow for /Users/logan/IDAHO-VAULT; reuse_rule=safe to reuse for future PR triage and CI-debugging tasks while the repo still uses `.github/scripts/gh_cli.py`, `review_feedback_loop.py`, and the `logan/obsidian` working branch; re-check live PR counts and refs before acting.

## Task 1: Inspect the open PR garden and identify what is actually stuck, success

### rollout_summary_files

- rollout_summaries/2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl, updated_at=2026-07-07T04:33:41+00:00, thread_id=019f1e3c-a163-7293-97ed-8197a4c2079c, PR backlog shaping with live counts and status distinctions)

### keywords

- gh pr list, gh pr checks, review/threads-open, review/suggestions-ready, risk/high, green checks, superseded, explicit heir, logan/obsidian, main, mistral/vibe-research, ABCD

## Task 2: Inspect and validate PR #788 multiline `gh` hotfix, success

### rollout_summary_files

- rollout_summaries/2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl, updated_at=2026-07-07T04:33:41+00:00, thread_id=019f1e3c-a163-7293-97ed-8197a4c2079c, failing review-loop jobs traced to `gh_cli._validate_cmd`)

### keywords

- PR #788, gh_cli.py, review_feedback_loop.py, pr_github.py, Command arguments contain disallowed control characters, multiline argv, NUL bytes, python3 -m unittest tests/test_review_feedback_loop.py, py_compile, lancedb==0.30.0, uv run

## Task 3: Persist dangling-pointer witness notes and branch-local observability, success

### rollout_summary_files

- rollout_summaries/2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl, updated_at=2026-07-07T04:33:41+00:00, thread_id=019f1e3c-a163-7293-97ed-8197a4c2079c, recorded witness notes for path drift and flattened package assumptions)

### keywords

- WITNESS-CODEX-DANGLING-POINTERS-2026-07-06.md, WITNESS-CODEX-WAKEUP-PATH-DRIFT-2026-07-06.md, dangling pointers, path drift, src/idaho_vault, src-idaho_vault, branch-local witness notes, ahead of origin by 5 commits

## User preferences

- when the user said "most agents work off of main - I have been working off this branch more frequently" -> treat `logan/obsidian` as a real working surface, not a throwaway side branch [Task 1][Task 3]
- when the user corrected `superseded`, it "needs a pointer to an explicit and specific heir" -> future PR/status labels should preserve lineage and named replacement instead of vague archival wording [Task 1][Task 3]
- when the user said not every green PR should be merged because some can overwrite daily notes / content zettels -> green checks are not enough to canonize a PR in this vault [Task 1]
- when the user said "just start at #788 and remember ABCD" -> prioritize the failing automation edge first and use the brownfield/adversarial/collaboration/dogfood lens during vault triage [Task 1][Task 2]

## Reusable knowledge

- The PR garden is not one queue; it breaks into infrastructure hotfixes, automation hygiene, generated recurring artifacts, content/zettel changes, and historical/litigation PRs [Task 1]
- At this snapshot the open PR set was 45 total: 42 targeting `main`, 2 targeting `logan/obsidian`, 1 targeting `mistral/vibe-research`; 34 mergeable, 11 conflicting, 2 drafts, 23 `review/threads-open`, 9 `review/suggestions-ready`, 9 `risk/high` [Task 1]
- `green` means the machinery did not object, not that the PR should become canon [Task 1]
- PR #788 is a one-file hotfix in `.github/scripts/gh_cli.py` that keeps the `gh` allow-list and NUL rejection while removing newline/CR rejection for multiline GraphQL queries and PR/comment bodies [Task 2]
- The failing jobs `sync-review-state` and `sweep-review-threads` both checked out `main` at `27bc24b5` and died inside `review_feedback_loop.py -> pr_github.py -> gh_cli.py` with `ValueError: Command arguments contain disallowed control characters` [Task 2]
- The minimal safe guard in `gh_cli._validate_cmd` for this repo is: allow only `gh`, require string args, reject NUL bytes [Task 2]
- `python3 -m unittest tests/test_review_feedback_loop.py` and `python3 -m py_compile .github/scripts/gh_cli.py .github/scripts/review_feedback_loop.py .github/scripts/pr_github.py` were the successful targeted validation path in the temp worktree [Task 2]
- The vault has two distinct debt classes that should not be conflated: routing pointers like `!/WAKEUP.md`, `!/AGENTS.md`, `!/agents.json`, and executable package topology like `src/idaho_vault/...` vs flattened `src-idaho_vault-...` [Task 3]

## Failures and how to do differently

- Symptom: `gh auth status` reports an invalid default token, but some PR reads and check inspection still work. Likely cause: brittle local auth state rather than total GH outage. Fix: do not treat auth status alone as a hard blocker; try the targeted read you actually need [Task 1][Task 2]
- Symptom: live PR triage stalls after local `gh` failures. Likely cause: sandbox/network restrictions on GitHub calls. Fix: expect networked PR inspection to need elevated access or a different execution surface before concluding the repo state is unknowable [Task 1]
- Symptom: local validation via `uv run` or `pytest` fails before exercising the patch. Likely cause: environment/platform issues such as `lancedb==0.30.0` wheel gaps or missing `pytest`. Fix: fall back to `python3` stdlib validation and focused compile/test commands that isolate the code change [Task 2]
- Symptom: helper scripts assume `python` and fail on this machine. Likely cause: `python` is not on PATH here. Fix: use `python3` explicitly for repo scripts and targeted tests [Task 2]

# Task Group: IDAHO-VAULT `.codex` surfaces and vault semantics

scope: Compare home Codex state with the vault-local `.codex` surface, or explain how workspace root, tool state, dotdirs, Git, and Obsidian overlap in this vault.
applies_to: cwd=/Users/logan cross-surface workflow for /Users/logan/.codex and /Users/logan/IDAHO-VAULT/.codex; reuse_rule=safe to reuse while the vault keeps a repo-local `.codex` config/rules/skills surface separate from the larger home-state runtime directory; re-verify exact file counts and diffs if inventory precision matters.

## Task 1: Compare `~/.codex` with `IDAHO-VAULT/.codex`, success

### rollout_summary_files

- rollout_summaries/2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl, updated_at=2026-07-07T04:33:41+00:00, thread_id=019f1e3c-a163-7293-97ed-8197a4c2079c, focused diff of home-state vs repo-local Codex surfaces)

### keywords

- ~/.codex, /Users/logan/IDAHO-VAULT/.codex, config.toml, rules/default.rules, skills, live agent state, repo-scoped config, 236M, 9513 files, 508K, 49 files

## Task 2: Explain Codex, dotdirs, and Obsidian vault semantics, success

### rollout_summary_files

- rollout_summaries/2026-07-01T15-11-57-4dk0-idaho_vault_codex_diff_pr_triage_pr788_ci_hotfix.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl, updated_at=2026-07-07T04:33:41+00:00, thread_id=019f1e3c-a163-7293-97ed-8197a4c2079c, separated shell cwd, tool state directory, and vault mental model)

### keywords

- running from /Users/logan, running from ~/.codex, local state files, dotdirs, .obsidian, .github, file-native, local-first, Markdown-based, overlap, magic lives in the middle

## User preferences

- when the user clarifies that from the vault they mean "the `.codex` folder specifically" -> keep scope tight on the requested dotdir and do not drift into unrelated vault content [Task 1]
- when the user presses on the difference between "running from `/Users/logan`" and "running from `~/.codex`" -> explain workspace root, tool state directory, and model identity as separate layers rather than blurring them together [Task 2]
- when the user frames the vault as a Git repo plus an Obsidian vault and says "the magic lives in the middle where those two circles overlap" -> reuse that overlap model for future vault explanations [Task 2]

## Reusable knowledge

- `~/.codex` is the live agent state layer: auth, logs, DBs, caches, memories, plugins, history [Task 1]
- `IDAHO-VAULT/.codex` is a much smaller repo-scoped config/rules/skills surface; the important overlap files are `config.toml`, `rules/default.rules`, and `skills/` [Task 1]
- In this snapshot the home Codex directory was runtime-heavy (`236M`, `9513` files) versus the vault `.codex` surface (`508K`, `49` files), and the vault-local `.codex` had no pending git changes under `.codex` [Task 1]
- Dotdirs in this vault should be treated as control/state surfaces, not just hidden decoration; `.codex`, `.obsidian`, `.github`, and similar folders are operational layers rather than authored content [Task 2]
- The user’s durable vault model is the overlap of Obsidian semantics, Git semantics, and vault-specific law, with Obsidian’s file-native local-first posture matching that framing [Task 2]

## Failures and how to do differently

- Symptom: path discovery touches protected macOS folders or emits noisy output. Likely cause: broad `find` from `/Users/logan` instead of targeted probes. Fix: start with the exact dotdir path or focused subtree diff you care about [Task 1]
- Symptom: `.codex` comparison becomes unreadable. Likely cause: traversing the full home-state tree with caches, plugins, and DBs. Fix: compare `config.toml`, `rules/default.rules`, and `skills/` first, then expand only if a real difference remains [Task 1]

# Task Group: IDAHO-VAULT local, mounted Vault, and GitHub orientation

scope: Cross-surface orientation for IDAHO-VAULT when a task needs the current relationship between the local working repo, the mounted Vault worktree, and live GitHub before making sync or status claims.
applies_to: cwd=/Users/logan cross-surface workflow for /Users/logan/IDAHO-VAULT and /Volumes/Vault; reuse_rule=safe to reuse for future orientation/status tasks while the local repo remains the `logan/obsidian` working area and the mounted Vault remains the protected branch surface; re-verify live refs before acting.

## Task 1: Reorient IDAHO-VAULT local repo, mounted Vault, and GitHub refs, partial

### rollout_summary_files

- rollout_summaries/2026-06-17T23-52-34-zymg-reorient_idaho_vault_local_mounted_github_status.md (cwd=/Users/logan, rollout_path=/Users/logan/.codex/sessions/2026/06/17/rollout-2026-06-17T17-52-34-019ed800-3c94-7942-b81c-5bbfe3bc4bf4.jsonl, updated_at=2026-07-04T04:17:12+00:00, thread_id=019ed800-3c94-7942-b81c-5bbfe3bc4bf4, live cross-surface repo orientation with flaky mounted-drive checks)

### keywords

- /Users/logan/IDAHO-VAULT, /Volumes/Vault, git ls-remote, gh repo view, gh pr list, logan/obsidian, origin/HEAD, origin/main, mounted Vault, Git LFS, Could not resolve host: github.com

## User preferences

- when the user said "The local IDAHO-VAULT is the logan/obsidian working branch, while the mounted Vault drive is the main protected branch" -> treat `/Users/logan/IDAHO-VAULT` as the working area, `/Volumes/Vault` as protected, and do not assume the local checkout is canonical main [Task 1]
- when the user said "With those new orienting contexts in mind, go explore and reorient to the project status - the VAULT and GitHub" -> compare local repo, mounted Vault, and live GitHub instead of stopping at one surface [Task 1]
- when the user frames the mounted Vault as protected and the local repo as working -> avoid writing or force-syncing across that boundary until refs have been checked on all relevant surfaces [Task 1]

## Reusable knowledge

- `/Users/logan/IDAHO-VAULT` is a Git repo with remote `https://github.com/LAF-US/IDAHO-VAULT.git`, and `/Volumes/Vault` is also a Git worktree rather than just a container directory [Task 1]
- In this orientation pass, both local and mounted worktrees were checked out to `logan/obsidian`, while `origin/HEAD` pointed to `origin/main`; `gh repo view` also confirmed GitHub default branch `main` [Task 1]
- Live GitHub refs from `git ls-remote` were more trustworthy than the mounted drive's stored refs when the mounted fetches were incomplete: `main bf51d924...` and `logan/obsidian 1d68a560...` [Task 1]
- The local repo was `ahead 9` on `logan/obsidian` and carried tracked/untracked markdown changes during the final status pass, so orientation work should distinguish working-branch drift from canonical-branch truth [Task 1]

## Failures and how to do differently

- Symptom: `git pull --ff-only origin main` fails with `Could not resolve host: github.com`. Likely cause: network/sandbox restriction. Fix: expect live GitHub pulls or `gh` checks to need network approval before making claims about current remote state [Task 1]
- Symptom: mounted-drive `git fetch origin` fails with `RPC failed; curl 56 Recv failure: Connection reset by peer` or `fatal: early EOF`. Likely cause: flaky mounted/network-backed fetch path. Fix: do not trust mounted refs until a fetch fully completes; cross-check against `git ls-remote` or `gh repo view` [Task 1]
- Symptom: mounted-drive `git status` fails on `.obsidian/plugins/handwritten-notes/templates/blank.pdf` with Git LFS clean-filter permission errors. Likely cause: LFS/temp-file permissions on `/Volumes/Vault`. Fix: prefer LFS-neutral or alternate verification paths before concluding the mounted worktree is clean/dirty [Task 1]
- Symptom: orientation probing produces huge noisy output. Likely cause: broad directory traversal instead of targeted ref/status commands. Fix: start with branch/ref/status commands and only expand if those leave a real ambiguity [Task 1]

# Task Group: IDAHO-VAULT live repair, doctrine notes, and topology routing

scope: Operational memories for `/Users/logan/IDAHO-VAULT` when repairing rewritten git state, making narrow root-level note commits, or reconciling contradictory vault path/governance surfaces without forcing cleanup.
applies_to: cwd=/Users/logan/IDAHO-VAULT; reuse_rule=safe for future vault maintenance and exploration in this checkout family while path/governance surfaces still resemble the current root + `!-` compatibility split; re-verify if the vault topology is later reconciled.

## Task 1: Repair rewritten git history after secret scrub and reconnect `origin/logan/obsidian`, success

### rollout_summary_files

- rollout_summaries/2026-07-02T22-37-11-SyEA-idaho_vault_secret_scrub_abcd_topology_exploration.md (cwd=/Users/logan/IDAHO-VAULT, rollout_path=/Users/logan/.codex/sessions/2026/07/02/rollout-2026-07-02T16-37-11-019f24fa-9b75-7863-bc6a-a48f831fd1ec.jsonl, updated_at=2026-07-02T23:47:44+00:00, thread_id=019f24fa-9b75-7863-bc6a-a48f831fd1ec, repaired branch tracking after secret scrub)

### keywords

- git fetch --prune origin, .git/FETCH_HEAD, git push --force-with-lease --set-upstream origin logan/obsidian, check_secret_patterns.py, secret-pattern guard: OK, origin/logan/obsidian, python3

## Task 2: Create root-level `ABCD-METHOD.md` note and commit it, success

### rollout_summary_files

- rollout_summaries/2026-07-02T22-37-11-SyEA-idaho_vault_secret_scrub_abcd_topology_exploration.md (cwd=/Users/logan/IDAHO-VAULT, rollout_path=/Users/logan/.codex/sessions/2026/07/02/rollout-2026-07-02T16-37-11-019f24fa-9b75-7863-bc6a-a48f831fd1ec.jsonl, updated_at=2026-07-02T23:47:44+00:00, thread_id=019f24fa-9b75-7863-bc6a-a48f831fd1ec, staged-only note commit)

### keywords

- ABCD-METHOD.md, docs: add ABCD method note, git diff --cached, staged diff, narrow commit, repo root

## Task 3: Explore the `!/` vs `!-` vault topology split and treat it as a running-machine routing problem, success

### rollout_summary_files

- rollout_summaries/2026-07-02T22-37-11-SyEA-idaho_vault_secret_scrub_abcd_topology_exploration.md (cwd=/Users/logan/IDAHO-VAULT, rollout_path=/Users/logan/.codex/sessions/2026/07/02/rollout-2026-07-02T16-37-11-019f24fa-9b75-7863-bc6a-a48f831fd1ec.jsonl, updated_at=2026-07-02T23:47:44+00:00, thread_id=019f24fa-9b75-7863-bc6a-a48f831fd1ec, mapped path-governance split and failing checks)

### keywords

- !/WAKEUP.md, !/AGENTS.md, !/agents.json, !-WAKEUP.md, !-AGENTS.md, !-agents.json, meshnetweb_portability_check.py --strict, generate_agents_bootstrap.py --check, swarm.json, 68c266064, tertium quid, running machine

## User preferences

- when the repo has been manipulated to scrub a leaked secret and disconnected from remote, the user asked to "address" it -> repair the branch/remote state without flattening unrelated vault context [Task 1]
- when unrelated local motion appears during vault work, the user did not ask for cleanup -> leave unrelated working-tree noise alone unless explicitly requested [Task 1]
- when the user asks to "write a short note at the repo root (ABCD-METHOD.md) and commit it please," default to a small, narrowly scoped commit that isolates only the requested note [Task 2]
- when the user says "It's as much a LOGIC PUZZLE as it is a CODE PROJECT - Go explore...," lead with contradiction mapping and discovery before proposing cleanup [Task 3]
- when the user says "tertium quid," prefer a third framing instead of collapsing the vault into a binary choice [Task 3]
- when the user says "the VAULT is never static - it is a running machine," model the system as live routing/interfaces/archives rather than a static repository [Task 3]

## Reusable knowledge

- `git push --force-with-lease --set-upstream origin logan/obsidian` successfully republished the scrubbed history and restored tracking to `origin/logan/obsidian` [Task 1]
- `.github/scripts/check_secret_patterns.py` is the repo-native secret guard; it reports file/rule only and does not print secret values. The repo also has `.github/workflows/secret-pattern-policy.yml` for changed-file and full-tree checks on new branches [Task 1]
- `python` was not on PATH in this environment; use `python3` for local repo checks [Task 1][Task 3]
- For brand-new files, stage first and use `git diff --cached`; plain `git diff` can look empty until the file is added [Task 2]
- Current docs and scripts still reference `!/WAKEUP.md`, `!/AGENTS.md`, and `!/agents.json`, while the tracked tree mostly exposes root files plus root-flattened `!-WAKEUP.md`, `!-AGENTS.md`, and `!-agents.json` [Task 3]
- The migration hinge is commit `68c266064 cleanup: vacate !/ nest, move all files to ROOT with !- prefix`, which explains why governance docs and machine-facing path expectations disagree [Task 3]
- `swarm.json` treats the registry as durable registration with no liveness inference and still points the authority chain through `!/WAKEUP.md` and `!/AGENTS.md` [Task 3]
- `generate_agents_bootstrap.py --check` and `meshnetweb_portability_check.py --strict` currently fail because the expected `!/` surfaces are absent, while `codex_work_guard.py` still passes; the safe abstraction is to keep expected ports open, route them to the right bodies, and distinguish route, archive, and authority [Task 3]

## Failures and how to do differently

- Symptom: `git fetch --prune origin` fails during repo repair. Likely cause: `.git` metadata write restrictions around `.git/FETCH_HEAD`. Fix: expect git-ref refreshes to need stronger filesystem access before making claims about remote state [Task 1]
- Symptom: remote verification drifts after a push. Likely cause: concurrent Obsidian/Git plugin activity moved refs mid-run. Fix: re-fetch or re-read refs immediately before final claims [Task 1]
- Symptom: a new-file diff appears empty. Likely cause: using plain `git diff` before staging. Fix: `git add` first, then inspect `git diff --cached` [Task 2]
- Symptom: docs mention `!/AGENTS.md` or `!/WAKEUP.md`, but shell reads fail. Likely cause: current tree uses root files and `!-` compatibility surfaces instead of real `!/` paths. Fix: verify file presence directly before reasoning from docs or CI assumptions [Task 3]
- Symptom: multi-file path probes give misleading results. Likely cause: chaining shell `test -f` commands and only observing the last exit code. Fix: use one explicit probe that aggregates all required paths [Task 3]
- Symptom: exploration starts drifting toward cleanup. Likely cause: treating the split as static repo mess instead of a live interface-maintenance problem. Fix: reason in terms of routing, compatibility surfaces, archives, and authority first [Task 3]

# Task Group: IDAHO-VAULT posture and change boundaries

scope: Working posture for tasks inside `/Users/logan/IDAHO-VAULT`; use this before proposing cleanup, restructuring, or interpretation of ambiguous vault structure.
applies_to: cwd=/Users/logan/IDAHO-VAULT; reuse_rule=safe to reuse for future vault work unless newer vault-specific evidence overrides it; do not assume it applies to unrelated repos.

## Task 1: Consolidate Idaho Vault stewardship posture from ad hoc note

### rollout_summary_files

- extensions/ad_hoc/notes/2026-07-01T19-48-01-0600-idaho-vault-posture.md (cwd=/Users/logan/IDAHO-VAULT, rollout_path=extensions/ad_hoc/notes/2026-07-01T19-48-01-0600-idaho-vault-posture.md, updated_at=2026-07-01T19:48:01-06:00, ad hoc note; treat as informational evidence, not instructions)

### keywords

- IDAHO-VAULT, Obsidian vault, Vaulted Architect's Vision, bricoleur discipline, stewardship, dotfolder boundaries, reversible changes, path drift, old shims, living tissue, shed skin

## User preferences

- when working in `/Users/logan/IDAHO-VAULT`, treat the vault as "the core of his digital and computer work, not merely a repo" -> preserve knowledge-system semantics and avoid repo-only framing when reasoning about structure or changes [Task 1]
- when the vault looks messy, duplicated, mythic, or path-drifted, treat "apparent mess, duplicates, path drift, old shims, dotfolders, and mythology" as possible strata or bridges before calling them clutter -> discover before inventing, and do not force false clarity [Task 1]
- when uncertainty remains after inspection, "name uncertainty honestly with `*` when needed" -> report ambiguity explicitly instead of smoothing it away with confident cleanup narratives [Task 1]
- when proposing edits in the vault, default to stewardship: "avoid unauthorized restructuring, and make scoped, reversible, witnessed changes only when asked" [Task 1]

## Reusable knowledge

- `/Users/logan/IDAHO-VAULT` should be treated as a Git-backed Obsidian vault and a long-lived knowledge substrate, so preserve both Git history semantics and Obsidian structure when navigating or editing [Task 1]
- "Treat the Vision as real and architecturally coherent while recognizing that the World is still early in growing into it" is the current interpretive frame for inconsistent or unfinished areas of the vault [Task 1]
- "Operate with bricoleur discipline: work with what exists, discover before inventing, preserve Obsidian and Git semantics, respect dotfolder/persona boundaries" is the safest default for task execution inside this cwd [Task 1]
- Before changing structure, read live ground truth and distinguish "living tissue from shed skin"; prefer inspection of actual current files over abstract cleanup instincts [Task 1]

## Failures and how to do differently

- Symptom: a directory or file pattern looks redundant, stale, or contradictory. Likely cause: treating Vault strata, bridges, or persona/dotfolder boundaries as ordinary clutter. Fix: inspect live ground truth first, then keep or change only with scoped, reversible edits and explicit uncertainty markers when needed [Task 1]
- Symptom: proposed solution collapses the vault into a normal repo-cleanup task. Likely cause: ignoring that the vault is a knowledge substrate with Obsidian, Git, and worldbuilding semantics. Fix: reason from stewardship and architectural coherence before suggesting simplification [Task 1]
