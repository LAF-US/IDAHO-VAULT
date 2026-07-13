thread_id: 019f1e3c-a163-7293-97ed-8197a4c2079c
updated_at: 2026-07-07T04:33:41+00:00
rollout_path: /Users/logan/.codex/sessions/2026/07/01/rollout-2026-07-01T09-11-57-019f1e3c-a163-7293-97ed-8197a4c2079c.jsonl
cwd: /Users/logan

# The rollout established that IDAHO-VAULT’s `.codex` and governance surfaces are intentionally repo-local, then shifted into PR triage and a focused CI hotfix investigation.

Rollout context: The user first asked to compare `~/.codex` with `~/IDAHO-VAULT/.codex`, then asked conceptual questions about Codex/dotdirs/Obsidian/vault semantics, then asked for a broad look at open PRs, and finally asked to inspect/fix the failing PR #788 and remember the ABCD framing. The session ran from `/Users/logan`, with the vault at `/Users/logan/IDAHO-VAULT` and the live Codex state at `/Users/logan/.codex`.

## Task 1: Compare `~/.codex` vs `IDAHO-VAULT/.codex`

Outcome: success

Preference signals:
- The user asked to check divergence between the home Codex directory and the vault-local one, then later clarified that from the vault, the task was specifically to inspect the `.codex` folder. That suggests future work in the vault should stay tightly scoped to the target dotdir and not wander into unrelated vault content.

Key steps:
- Located the vault at `/Users/logan/IDAHO-VAULT` rather than the alternative `Library/Application Support/IDAHO-VAULT` path.
- Compared file lists and diffs for `config.toml`, `rules/default.rules`, and `skills/`.
- Found `~/.codex` to be much larger and runtime-heavy (`236M`, `9513` files) versus the vault `.codex` (`508K`, `49` files).
- Verified the vault `.codex` had no pending git changes under `.codex`.

Failures and how to do differently:
- A broad `find /Users/logan -type d -name IDAHO-VAULT` touched macOS-protected folders and had to be cut short. Future similar searches should be narrowed earlier.
- A full-tree `find` on `~/.codex` was extremely noisy because of caches/plugins/db state; better to compare focused subtrees first.

Reusable knowledge:
- `~/.codex` is live agent state: auth, logs, DBs, caches, memories, plugins, history.
- `IDAHO-VAULT/.codex` is a small repo-scoped config/rules/skills surface, not a full home-state clone.
- In this vault, `config.toml`, `rules/default.rules`, and `skills/` are the meaningful overlap points for divergence checks.

References:
- `ls -la /Users/logan/.codex`
- `find /Users/logan/IDAHO-VAULT/.codex -type f -print`
- `find /Users/logan/.codex -maxdepth 2 -type f -print`
- `diff -u /Users/logan/.codex/config.toml /Users/logan/IDAHO-VAULT/.codex/config.toml`
- `diff -u /Users/logan/.codex/rules/default.rules /Users/logan/IDAHO-VAULT/.codex/rules/default.rules`
- `diff -rq /Users/logan/.codex/skills /Users/logan/IDAHO-VAULT/.codex/skills`

## Task 2: Explain Codex/dotdirs/Obsidian/vault semantics

Outcome: success

Preference signals:
- The user pushed on the distinction between “running from `~/.codex`” versus the shell cwd and then framed `~/.codex` as part of “you.” That suggests future explanations should separate workspace root, tool state directory, and model identity layer explicitly.
- The user characterized the vault as a Git repo plus an Obsidian vault, saying the “magic lives in the middle where those two circles overlap.” That is now a durable framing for future vault work.
- The user emphasized that `~/.codex` and other dotdirs are “local state files” and asked for reflection plus online research on filename conventions regarding the `.` character.

Key steps:
- Used the web to confirm Obsidian’s file-native, local-first, plugin-heavy PKM positioning.
- Used the web to ground the meaning of leading-dot filenames/directories as hidden/config/state surfaces rather than mere decoration.
- Mapped the vault to a “governed knowledge substrate” model: Obsidian for navigation, Git for history/accountability, dotdirs for control/state, and agents as bounded labor over the substrate.

Reusable knowledge:
- Dotdirs are not just “hidden”; they are usually control/state surfaces.
- In this vault, `.codex`, `.obsidian`, `.github`, and similar folders should be treated as operational layers, not content.
- The user’s operating model for the vault is explicitly the overlap of Obsidian semantics, Git semantics, and vault-specific law.

References:
- Obsidian official site and help pages were consulted for vault/file-native/Markdown-flavor positioning.
- GNU coreutils `ls` docs, Python `pathlib` docs, and freedesktop XDG base directory docs were consulted for dotfile / filename semantics.

## Task 3: Open PR triage and backlog shaping

Outcome: success

Preference signals:
- The user said “most agents work off of main - I have been working off this branch more frequently,” which means `logan/obsidian` is a real working surface and not just a temporary side branch.
- When discussing PR lifecycle, the user corrected the meaning of “superseded”: it “needs a pointer to an explicit and specific heir.” That is a strong durable rule for future status labels.
- The user also gave the ABCD mnemonic and later reinforced “just start at #788 and remember ABCD,” which should be preserved as a task lens for future brownfield, adversarial, collaboration, dogfood work.
- The user cautioned that not every green PR should be merged immediately because some risk overwriting daily notes, zettels, etc. That is a durable distinction: green checkmarks are not sufficient for canonization in this vault.

Key steps:
- Queried open PRs via `gh pr list` after local network calls failed.
- Found 45 open PRs total, with 42 targeting `main`, 2 targeting `logan/obsidian`, and 1 targeting `mistral/vibe-research`.
- Summarized the backlog into mergeable vs conflicting vs draft, and identified the large review backlog / generated PR / lifecycle PR clusters.
- Noted that PR #788 was the key hotfix because it was likely unblocking the review machinery itself.

Failures and how to do differently:
- Plain `gh` calls initially failed because GitHub auth/network was unavailable in the sandbox; re-ran the same calls with escalated network permission.
- `gh auth status` reported the stored default token invalid, so future agents should expect `gh auth` to be brittle here even if some networked PR calls work.

Reusable knowledge:
- The PR garden is not one queue; it’s several ecosystems: infrastructure hotfixes, automation hygiene, generated recurring artifacts, content/zettel changes, and historical/litigation PRs.
- `green` means the machinery didn’t object, not that the PR should be merged into canon.
- PRs with `review/threads-open` and `review/suggestions-ready` can be backlog pressure rather than immediate merge candidates.

References:
- `gh pr list --repo LAF-US/IDAHO-VAULT --state open --limit 100 ...`
- Summary counts: 45 open PRs; 42 `main`, 2 `logan/obsidian`, 1 `mistral/vibe-research`; 34 mergeable, 11 conflicting, 2 drafts, 23 `review/threads-open`, 9 `review/suggestions-ready`, 9 `risk/high`.
- Large/open examples inspected: #789, #788, #787, #785, #784, #782, #781, #780, #777, #769, #767, #766, #746/742/741/720/687 etc. (see raw rollout for the full list and statuses).

## Task 4: Inspect and validate PR #788 hotfix

Outcome: success

Preference signals:
- The user’s “start at #788” instruction established the immediate priority.
- The user’s ABCD framing and the vault’s brownfield/adversarial context indicate failing automation should be treated as evidence, not as authority.

Key steps:
- Loaded the GitHub CI-fix skill, then inspected PR #788 metadata and patch.
- Confirmed it is a one-file hotfix in `.github/scripts/gh_cli.py` that keeps the `gh` allow-list and NUL-byte rejection, while removing newline/CR rejection.
- Pulled failing GitHub Actions job logs for `sync-review-state` and `sweep-review-threads`.
- The logs showed both jobs checked out `main` at `27bc24b5` and died inside `review_feedback_loop.py -> pr_github.py -> gh_cli.py` with `ValueError: Command arguments contain disallowed control characters`.
- Created a temporary detached worktree at the PR commit and validated the fix there.
- Verified the direct guard behavior: multiline argv accepted, non-`gh` rejected, NUL rejected.
- Verified `python3 -m unittest tests/test_review_feedback_loop.py` in the temp worktree: 109 tests passed.
- `uv run pytest` failed for an environment reason (`lancedb==0.30.0` wheel gap on macOS x86_64), not because of the PR.
- Cleaned up the temporary worktree afterward.

Failures and how to do differently:
- `gh auth status` showed an invalid default token, but networked PR reads still worked; future agents should not assume `gh auth status` is a hard gate for all GH calls here.
- The bundled `inspect_pr_checks.py` helper assumed `python`; on this machine `python3` had to be used.
- `python3 -m pytest` was unavailable in the temp environment; `unittest` succeeded and was enough to validate the targeted suite.
- `uv run` hit a known dependency/platform issue unrelated to the patch; future similar local validation should be ready to fall back from `uv` to stdlib tests when wheel availability is a blocker.

Reusable knowledge:
- The failing review-loop jobs were self-referential: they crashed before doing useful work because the PR fixed the exact validation that blocked multiline GH arguments.
- For this repo, multiline PR bodies/comments are normal and should not be rejected simply because they contain `\n` or `\r`.
- The minimal safe validation in `gh_cli._validate_cmd` is: allow only `gh`, require string args, reject NUL bytes.

References:
- PR #788: `Hotfix: revert newline/CR rejection in gh_cli._validate_cmd (breaks every multi-line PR comment)`
- Commit under review: `fa59ae990b5e91ffcc7dfb30b1e6b2d846db39f3`
- Failing logs showed `review_feedback_loop.py failed: Command arguments contain disallowed control characters`
- Validation commands: `python3 -m unittest tests/test_review_feedback_loop.py`, `python3 -m py_compile .github/scripts/gh_cli.py .github/scripts/review_feedback_loop.py .github/scripts/pr_github.py`
- Key log line: `sync-review-state` and `sweep-review-threads` both failed inside `gh_cli._validate_cmd`

## Task 5: Persist vault-side observations and PR context

Outcome: success

Preference signals:
- The user’s branch comment about working off `logan/obsidian` more frequently suggests branch-local observations are part of the durable working surface, not throwaway chatter.
- The user’s correction about superseded needing an explicit heir suggests future status notes should be precise and lineage-aware.

Key steps:
- Recorded a first witness note for the `!/WAKEUP.md` path-drift issue, then another broader inventory note for dangling pointers across governance paths and flattened `src/idaho_vault/...` package assumptions.
- Confirmed that the second witness note was committed locally on `logan/obsidian` and that the branch remained ahead of origin after the PR triage.
- Preserved the notion that `superseded` is not a trash status; it implies a named heir.

Reusable knowledge:
- The vault has a real path-drift / flattened-surface problem across `!/` routing, generated bootstrap surfaces, and Python package layout.
- There are two distinct debt classes: routing pointers (`!/WAKEUP.md`, `!/AGENTS.md`, `!/agents.json`) and executable package topology (`src/idaho_vault/...` vs flattened `src-idaho_vault-...`).

References:
- The rollout created `WITNESS-CODEX-DANGLING-POINTERS-2026-07-06.md` and earlier `WITNESS-CODEX-WAKEUP-PATH-DRIFT-2026-07-06.md`.
- The repo state at the end of the rollout was `logan/obsidian` ahead of origin by 5 commits.
