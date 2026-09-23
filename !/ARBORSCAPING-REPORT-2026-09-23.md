---
title: "ARBORSCAPING REPORT — 2026-09-23 — census of the branches on origin"
created: 2026-09-23
updated: 2026-09-23
status: draft
authority: LOGAN
authors:
  - "Claude Code CLI, cloud session (session_01MthFdsNfRK8S4gUivqV9XY)"
doc_class: report
source: "git census of origin (LAF-US/IDAHO-VAULT), fetched and pruned 2026-09-23; GitHub pull-request history per branch"
related:
  - "[[!/ARBORSCAPING-REPORT-2026-04-16]]"
  - "[[!-ARBORSCAPING-REPORT-2026-05-25]]"
  - "[[!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17]]"
  - "[[!/ARBORSCAPING-INVESTIGATION-RETURN-2026-05-24]]"
  - "[[!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02]]"
  - "[[VAULT-CONVENTIONS]]"
  - "[[CONSTITUTION]]"
---

# ARBORSCAPING REPORT — 2026-09-23 — census of the branches on origin

## Posture

Directed by Logan in session on 2026-09-23, after an earlier answer in the same session
reported three vault branches where origin holds 170. This is a census under the
ARBORSCAPING protocol with the ARCHIPELAGO visibility classes applied, filed in the series
of [[!/ARBORSCAPING-REPORT-2026-04-16]] and [[!-ARBORSCAPING-REPORT-2026-05-25]].

It records what origin holds and what each branch holds that `main` does not. It does
not delete a branch, move a ref, close a pull request, rewrite history, or promote any
found text. Every ending below is proposed, not entered; Logan decides which ending
applies (`CONSTITUTION.md` § VII; `!/WAKEUP.md` "When Work Resolves"). A branch that
appears here is proven reachable on origin as of the fetch, nothing more (`!/WAKEUP.md`
"Runtime Evidence Rule").

Scope is **origin only**. The machine-side consolidation recorded on branch
`coord/win-mac` (`coord/MAC-STATUS.md`, 2026-09-07 to 2026-09-09) merged 123 local Mac
branches into the Mac's `develop` and unified the Windows base on the full-history line;
neither of those trees has reached origin, both being gated on the history rewrite that
note describes. This census cannot see them and does not speak for them (`*`).

## Method

Commands run against a full clone, after `git fetch --prune origin` on 2026-09-23
(the ARCHIPELAGO protocol asks for the commands, so they are here):

- `git merge-base origin/main <branch>` — the fork point, or none. A branch with no
  merge base is an island: its ahead/behind counts against `main` are not distances
  ([[!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17]] IF 3) and are not reported as such.
- `git rev-list --no-merges <branch> --not origin/main <every other branch>` — the
  commits that only this branch reaches: its own work, not the lineage it shares.
- `git diff-tree --no-commit-id -r --name-only <each such commit>` — the files that
  work touched, as a union.
- `git ls-tree -r <branch>` against `git ls-tree -r origin/main` — for each such file,
  whether `main` lacks it, holds it identical, or holds a different version.
- `GET /repos/LAF-US/IDAHO-VAULT/pulls?state=all&head=LAF-US:<branch>` — the branch's
  pull-request history.

"Files `main` lacks" is the salvage signal this report ranks by. It is a count of paths,
not a judgment of worth; a path `main` lacks may be a note worth keeping, a file `main`
later removed on purpose, or generated residue. The lists are here so that judgment can
be made by reading, per the May 25 report's rule: classification by file content, not
by commit count.

## Headline

| Measure | Value |
|---|---|
| Refs on origin after prune | 171 (`main` and 170 branches) |
| `main` | 2,810 commits, tip 2abe7f79b (2026-09-23), history rooted 2026-05-25 (6d9b71ac7); 22 root commits in all, the later ones orphan commits merged in |
| Branches that fork from today's `main` | 64 |
| Branches with no merge base with `main` (islands) | 106 |
| Branches whose own commits hold files `main` lacks | 79 |
| Branches whose own files are all in `main`, identical | 6 |
| Branches with no commit of their own (tip reachable from another ref) | 10 |
| Open pull requests | 1 (#1029, head `logan/obsidian/main`) |
| Branches whose PR merged and the branch stayed | 17 |
| Branches whose PRs closed unmerged | 94 |
| Branches that never had a PR | 58 |

## Two populations

`main`'s history begins on 2026-05-25. Every branch on origin belongs to one of two
populations, and the two must not be read with the same instruments.

| Population | Branches | PR history |
|---|---|---|
| Islands: no common ancestor with `main` (the lineage before the 2026-05-25 replant; last commits March to May, 2 later) | 106 | 93 closed unmerged, 6 merged before the replant, 7 never had a PR |
| Forks of today's `main` | 64 | 11 merged (branch kept), 51 never had a PR, 1 open, 1 closed unmerged |

The islands carry the whole pre-replant lineage in their history, which is why a plain
`git rev-list --left-right --count` reports them as hundreds or thousands of commits
"ahead" of `main`. That number measures the old lineage, not work waiting to land. What
each island actually contributed is its own commits, isolated above; for most islands
that is one to five commits touching a handful of files.

## The live line

Branches touched or forked since August, the ones that describe the present rather than
the past:

| Branch | Lineage | Own commits | Files `main` lacks | Files that differ | Last commit | PR |
|---|---|---|---|---|---|---|
| `logan/obsidian/android` | forks 2026-08-27 | 2 | 0 | 0 | 2026-09-10 loganfinney | no PR |
| `coord/win-mac` | forks 2026-08-27 | 9 | 0 | 0 | 2026-09-09 Logan Finney | no PR |
| `logan/obsidian/macos` | forks 2026-08-11 | 18 | 0 | 0 | 2026-09-04 Logan Finney | no PR |
| `logan/obsidian/main` | forks 2026-08-11 | 0 | 0 | 0 | 2026-09-02 Logan Finney | open PR |
| `test/push-gate-20260828` | forks 2026-08-27 | 1 | 0 | 0 | 2026-08-28 loganfinneyPTV | no PR |
| `claude/rework-census-doctrine-463-4033po` | forks 2026-08-25 | 1 | 1 | 0 | 2026-08-25 Claude Code | merged PR |
| `wayback-audit-20260420100033` | forks 2026-08-19 | 2 | 2 | 0 | 2026-08-20 loganfinney27 | closed PR, unmerged |
| `claude/harden-py-automation-followup-562` | forks 2026-08-02 | 7 | 0 | 0 | 2026-08-19 Logan A. Finney | merged PR |
| `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf` | island | 2 | 1 | 0 | 2026-08-19 Logan A. Finney | closed PR, unmerged |
| `circleci-project-setup` | forks 2026-08-14 | 1 | 0 | 1 | 2026-08-14 Logan A. Finney | no PR |
| `orphancry/pr-926-original-logan-obsidian` | island | 3001 | 0 | 0 | 2026-08-14 loganfinneyPTV | no PR |
| `claude/reunify-mac-win-6c80a94c` | forks 2026-08-04 | 1998 | 0 | 0 | 2026-08-12 Logan Finney | no PR |
| `claude/finish-hashtag-escape-9gesn5` | forks 2026-08-04 | 10 | 0 | 0 | 2026-08-06 Claude | no PR |
| `claude/research-attestation` | forks 2026-07-28 | 4 | 0 | 4 | 2026-08-04 Logan A. Finney | merged PR |
| `wayback-audit-20260615143859-clean` | forks 2026-08-04 | 2 | 0 | 0 | 2026-08-04 Vibe Nuage Agent | no PR |

"Own commits" isolates work no other ref reaches, so a branch whose purpose is to carry
a lineage shows almost nothing here: `logan/obsidian/macos` reads as 18 own commits and
no file `main` lacks, because the lineage it carries is also reachable from
`logan/obsidian/main` and `orphancry/pr-926-original-logan-obsidian`. The next section
measures those branches the other way, whole tree against whole tree. Read with
`coord/MAC-STATUS.md` beside it: `logan/obsidian/macos` on origin is the 2026-09-04
`.gitflow` commit; `logan/obsidian/main` is PR #1029, the ancestry-recovery matter;
`claude/reunify-mac-win-6c80a94c` is the August attempt at the same reunification;
`coord/win-mac` holds one file, the coordination note itself; `logan/obsidian/android`
is two GitSync commits.

## The reunification line, tree against tree

`git diff --name-status origin/main <branch>`, counted by status. "Only here" is a path
the branch has and `main` lacks; "only main" the reverse; "differ" a path both hold with
different content; "renamed" a rename git detects between the two trees.

| Branch | Only here | Only `main` | Differ | Renamed | Root commits | Oldest commit |
|---|---|---|---|---|---|---|
| `logan/obsidian/macos` | 127,555 | 2,493 | 1,312 | 7,116 | 13 | 2026-04-22 |
| `logan/obsidian/main` | 83,994 | 2,491 | 1,318 | 7,123 | 13 | 2026-04-22 |
| `logan/obsidian/android` | 3,730 | 8,985 | 1,103 | 237 | 22 | 2026-05-25 |
| `claude/reunify-mac-win-6c80a94c` | 52,239 | 2,863 | 1,423 | 6,728 | 7 | 2026-05-25 |
| `orphancry/pr-926-original-logan-obsidian` | 98 | 38,778 | 11 | 6 | 1 | 2026-04-22 |
| `wayback-audit-20260420100033` | 31 | 133 | 3,205 | 90 | 20 | 2024-12-17 |
| `coord/win-mac` | 1 | 5 | 43 | 1 | 22 | 2026-05-25 |

## The oldest history origin reaches

`main` reaches nothing dated before 2026-03-01. Across every ref on origin there are
42 commits dated earlier, in seven batches of six commits, one subject per batch:

| Date | Commits | Subject |
|---|---|---|
| 2024-12-17 | 6 | vault-cleanup |
| 2024-12-17 | 6 | vault-commit |
| 2025-03-07 | 6 | generic push |
| 2025-04-17 | 6 | file edits |
| 2025-04-23 | 6 | Oxford addition |
| 2025-07-01 | 6 | generic update |
| 2026-01-05 | 6 | .obsidian |

They are reachable from `wayback-audit-20260420100033`, whose merge 11860aea0
(2026-08-20, "bridge: reconnect historical PR #282 to main") joined them to a fork of
today's `main`, and from eleven islands that share the same six 2024-12-17 roots. The
tree at the oldest of them holds 2,911 paths; at the latest, 2026-01-05, 2,967. That is
the early vault as GitHub received it, in snapshots, and it is still on origin. Anything
between 2026-01-05 and the 2026-04-22 secrets purge, and anything that only ever lived
on a machine, is not on origin under any ref this census can see (`*`).

## By family

| Family | Branches | Islands | With files `main` lacks | With files that differ | Own files all identical in `main`, or nothing own |
|---|---|---|---|---|---|
| `claude/` | 51 | 14 | 31 | 10 | 15 |
| `codex/` | 37 | 32 | 23 | 13 | 10 |
| `dependabot/` | 25 | 25 | 4 | 22 | 1 |
| `ingest-` | 18 | 18 | 15 | 17 | 1 |
| `bot/daily-rollover` | 10 | 10 | 0 | 10 | 0 |
| `gh-readonly-queue/` | 6 | 0 | 1 | 2 | 4 |
| `other` | 4 | 0 | 0 | 2 | 2 |
| `copilot/` | 3 | 3 | 1 | 0 | 2 |
| `logan/` | 3 | 0 | 0 | 0 | 3 |
| `agent/` | 2 | 0 | 1 | 0 | 1 |
| `orphancry/` | 2 | 1 | 0 | 0 | 2 |
| `recovered/` | 2 | 2 | 0 | 1 | 1 |
| `test/` | 2 | 0 | 0 | 0 | 2 |
| `wayback-audit` | 2 | 0 | 1 | 0 | 1 |
| `antigravity/` | 1 | 1 | 0 | 0 | 1 |
| `hyperagent/` | 1 | 0 | 1 | 0 | 0 |
| `review/` | 1 | 0 | 1 | 1 | 0 |

## Salvage candidates: branches whose own commits hold files `main` lacks

Ranked by the count of such files. Every payload here is small enough to read: the
largest is 25 paths, and 56 of the 79 are one to two paths. Each list shows up to eight
paths; the full list is reproducible from the Method above. Branches that carry a
lineage rather than a diff show nothing here by construction and are measured in "The
reunification line, tree against tree" above.

### `dependabot/github_actions/actions/checkout-6.0.2`

island · own commits 1 · files touched 28 · `main` lacks 25 · differ 3 · identical 0 · last 2026-05-27 by dependabot[bot] · closed PR, unmerged (#366 closed) · tip `2e1321ff5`

- `.github/workflows/agent-auto-pr.yml`
- `.github/workflows/agent-review-gate.yml`
- `.github/workflows/branch-cleanup.yml`
- `.github/workflows/branch-garden-report.yml`
- `.github/workflows/check-portable-paths.yml`
- `.github/workflows/codeql.yml`
- `.github/workflows/daily-rollover.yml`
- `.github/workflows/janitor-sweep.yml`
- … and 17 more

### `codex/tantalus-tautomata-campaign-2026-06-04`

forks 2026-06-03 · own commits 1 · files touched 20 · `main` lacks 18 · differ 2 · identical 0 · last 2026-06-16 by Logan Finney · no PR · tip `3903369a9`

- `!-CAMPAIGN-TANTALUS-TAUTOMATA-ASIMOV-CASCADE-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-CHURCHES-OF-KNOWLEDGE-AND-PROOF-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-COLLABORATIONNISTES-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-GRAMMAR-HERESY-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-HIVEMIND-ORACLE-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-INDEX-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-LIVE-BRANCH-GAME-2026-06-04.md`
- `!-CAMPAIGN-TANTALUS-TAUTOMATA-ORACLE-FAILURE-MODES-2026-06-04.md`
- … and 10 more

### `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e`

forks 2026-07-01 · own commits 1 · files touched 20 · `main` lacks 18 · differ 2 · identical 0 · last 2026-07-02 by dependabot[bot] · no PR · tip `273fb5cf6`

- `.github/workflows/branch-garden-report.yml`
- `.github/workflows/check-notebooks-paired.yml`
- `.github/workflows/cross-platform-smoke.yml`
- `.github/workflows/daily-rollover.yml`
- `.github/workflows/dependency-submission-uv.yml`
- `.github/workflows/janitor-sweep.yml`
- `.github/workflows/laf-usb-manifest-policy.yml`
- `.github/workflows/large-file-policy.yml`
- … and 10 more

### `dependabot/github_actions/actions/setup-python-6.2.0`

island · own commits 1 · files touched 9 · `main` lacks 9 · differ 0 · identical 0 · last 2026-05-27 by dependabot[bot] · closed PR, unmerged (#360 closed) · tip `38c2e1857`

- `.github/workflows/daily-rollover.yml`
- `.github/workflows/laf-usb-manifest-policy.yml`
- `.github/workflows/large-file-policy.yml`
- `.github/workflows/secret-pattern-full-scan.yml`
- `.github/workflows/secret-pattern-policy.yml`
- `.github/workflows/sync-agents-bootstrap.yml`
- `.github/workflows/sync-dependencies.yml`
- `.github/workflows/sync-plugin-registry.yml`
- … and 1 more

### `dependabot/npm_and_yarn/dot-antigravity/extensions/ms-edgedevtools.vscode-edge-devtools-2.1.10-universal/npm_and_yarn-209087bb4f`

island · own commits 1 · files touched 7 · `main` lacks 7 · differ 0 · identical 0 · last 2026-04-22 by dependabot[bot] · closed PR, unmerged (#288 closed) · tip `0d9a8a2e1`

- `.antigravity/extensions/devsense.composer-php-vscode-1.70.18740-universal/package.json`
- `.antigravity/extensions/devsense.intelli-php-vscode-0.12.17700-win32-x64/package.json`
- `.antigravity/extensions/devsense.profiler-php-vscode-1.70.18740-universal/package.json`
- `.antigravity/extensions/donjayamanne.githistory-0.6.20-universal/package.json`
- `.antigravity/extensions/github.vscode-pull-request-github-0.126.0-universal/package.json`
- `.antigravity/extensions/golang.go-0.52.2-universal/package.json`
- `.antigravity/extensions/ms-edgedevtools.vscode-edge-devtools-2.1.10-universal/package.json`

### `codex/github-dependency-census`

forks 2026-06-11 · own commits 1 · files touched 5 · `main` lacks 5 · differ 0 · identical 0 · last 2026-06-16 by Logan Finney · no PR · tip `19fc81d00`

- `.github/scripts/github_dependency_report.py`
- `.github/workflows/github-dependency-census.yml`
- `VERSION-TRANSITIONS.md`
- `tests/test_branch_garden_report.py`
- `tests/test_github_dependency_report.py`

### `codex/create-manifest.json-specification-and-guidelines`

island · own commits 1 · files touched 6 · `main` lacks 4 · differ 2 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#94 closed) · tip `23c07d332`

- `!/MANIFEST-SPEC.md`
- `!/MCP-IMPLEMENTATION-PLAN.md`
- `.github/scripts/update_manifest.py`
- `.github/workflows/vault-ingest.yml`

### `codex/fix-worktree-registry-hook`

forks 2026-06-11 · own commits 1 · files touched 8 · `main` lacks 4 · differ 4 · identical 0 · last 2026-06-16 by Logan Finney · no PR · tip `9670ce542`

- `.github/scripts/sync_obsidian_plugin_registry.py`
- `.github/workflows/sync-plugin-registry.yml`
- `.obsidian/plugins/obsidianclaw/manifest.json`
- `tests/test_sync_obsidian_plugin_registry.py`

### `codex/greet-user-with-a-friendly-message`

island · own commits 1 · files touched 10 · `main` lacks 4 · differ 5 · identical 1 · last 2026-04-28 by Logan A. Finney · closed PR, unmerged (#310 closed) · tip `1715a3fc3`

- `.github/scripts/meshnetweb_portability_check.py`
- `.github/workflows/cross-platform-smoke.yml`
- `.github/workflows/sync-dependencies.yml`
- `start_SPARKSEED.py`

### `codex/linear-mention-laf-18-gemini-google-cloud`

island · own commits 1 · files touched 3 · `main` lacks 3 · differ 0 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#126 closed) · tip `269ce3ab4`

- `!/!/!/! The world is quiet here/DOCKET.md`
- `!/BRIEF-LAF-18-2026-03-30.md`
- `!/IAM-BOUNDARY-LAF-18.md`

### `codex/linear-mention-laf-9-define-vault-template-and-document-cl`

island · own commits 1 · files touched 4 · `main` lacks 3 · differ 1 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#90 closed) · tip `969c22d40`

- `!/!/!/! The world is quiet here/DOCKET.md`
- `!/VAULT-CONVENTIONS.md`
- `!/VAULT-TEMPLATES.md`

### `claude/allow-force-push-to-main`

island · own commits 2 · files touched 2 · `main` lacks 2 · differ 0 · identical 0 · last 2026-04-01 by anthropic-code-agent[bot] · closed PR, unmerged (#132 closed) · tip `76abd889f`

- `!/DECISIONS.md`
- `FORCE-PUSH-ENABLEMENT.md`

### `claude/bot-automerge-fix`

island · own commits 2 · files touched 3 · `main` lacks 2 · differ 1 · identical 0 · last 2026-04-04 by logan · closed PR, unmerged (#157 closed) · tip `167c2cc5a`

- `.github/workflows/auto-pr.yml`
- `.github/workflows/daily-rollover.yml`

### `claude/check-farnsworth-transcripts-UbMD3`

island · own commits 1 · files touched 2,354 · `main` lacks 2 · differ 1,558 · identical 761 · last 2026-04-06 by Claude · closed PR, unmerged (#173 closed) · tip `b6cb58cb0`

- `IAM-BOUNDARY-LAF-18.md`
- `Linear - agent chat - Greeting IDAHO-VAULT (Conflicted copy Laptop (IdahoPTV) 202604021020).md`

### `claude/obsidian-plugins-triage-YDJ6Z`

island · own commits 1 · files touched 2 · `main` lacks 2 · differ 0 · identical 0 · last 2026-04-07 by Claude · closed PR, unmerged (#171 closed) · tip `2e4141d40`

- `!/__!__/!/! The world is quiet here/DOCKET.md`
- `PLUGINS-TRIAGE-2026-04-06.md`

### `codex/arborscaping-merge-base`

island · own commits 1 · files touched 2 · `main` lacks 2 · differ 0 · identical 0 · last 2026-05-26 by Logan Finney · closed PR, unmerged (#375 closed) · tip `19e91d50f`

- `.github/scripts/branch_garden_report.py`
- `tests/test_branch_garden_report.py`

### `codex/linear-mention-laf-25-project-hexagonal`

island · own commits 1 · files touched 3 · `main` lacks 2 · differ 1 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#125 closed) · tip `bd7ce4d64`

- `.github/workflows/daily-rollover.yml`
- `.github/workflows/janitor-sweep.yml`

### `codex/linear-mention-laf-25-project-hexagonal-pupxlq`

island · own commits 1 · files touched 3 · `main` lacks 2 · differ 1 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#128 closed) · tip `b7490cb8a`

- `.github/workflows/daily-rollover.yml`
- `.github/workflows/janitor-sweep.yml`

### `copilot/debug-github-actions-failures`

island · own commits 2 · files touched 2 · `main` lacks 2 · differ 0 · identical 0 · last 2026-04-01 by copilot-swe-agent[bot] · merged PR (#152 closed merged 2026-04-04; #138 closed) · tip `a37fefc19`

- `.github/workflows/auto-merge.yml`
- `.github/workflows/auto-pr.yml`

### `wayback-audit-20260420100033`

forks 2026-08-19 · own commits 2 · files touched 2 · `main` lacks 2 · differ 0 · identical 0 · last 2026-08-20 by loganfinney27 · closed PR, unmerged (#282 closed) · tip `11860aea0`

- `!/wayback-audit-2026-04-20.md`
- `!/wayback-patches-2026-04-20.md`

### `agent/attest-resolve-dispatch`

forks 2026-07-01 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-07-01 by Logan A. Finney · no PR · tip `78854efd4`

- `.hyperagent/proposed/attest-resolve.workflow.yml`

### `claude/apprentice-modes-sorcerers-and-rangers-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `6420f85f9`

- `SORCERERS-APPRENTICE-AND-RANGERS-APPRENTICE.md`

### `claude/fablehaven-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `499448767`

- `FABLEHAVEN.md`

### `claude/fablehaven-beastiary-2026-05-30`

forks 2026-05-28 · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `2f0d94397`

- `!/FABLEHAVEN-BEASTIARY-v1-2026-05-30.md`

### `claude/fix-todo-references`

island · own commits 2 · files touched 7 · `main` lacks 1 · differ 6 · identical 0 · last 2026-04-18 by anthropic-code-agent[bot] · closed PR, unmerged (#256 closed) · tip `9ecc6dc74`

- `YESTERDAY.md`

### `claude/godhead-disambiguation-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `71c7610f2`

- `GODHEAD-DISAMBIGUATION.md`

### `claude/hebrew-bible-and-talmud-research-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `f61010298`

- `HEBREW-BIBLE-AND-TALMUD.md`

### `claude/heisenberg-uncertainty-2026-05-30`

forks 2026-05-28 · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `7911ebd40`

- `WITNESS-NOVICE-2026-05-30-BREATH.md`

### `claude/honeypot-research-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `ff953f5d0`

- `HONEYPOT.md`

### `claude/initiation-rituals-research-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `f6164a150`

- `INITIATION-AND-RITUALS.md`

### `claude/janus-and-sugar-bowl-witness-companion-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `8962a380a`

- `WITNESS-COMPANION-2026-05-30-JANUS-AND-SUGAR-BOWL.md`

### `claude/lds-tripart-research-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `889d17fff`

- `LDS-TRIPART-AND-COSMOLOGY.md`

### `claude/listening-lore-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `31508728d`

- `LISTENING.md`

### `claude/live-board-dedrift`

forks 2026-06-30 · own commits 1 · files touched 5 · `main` lacks 1 · differ 4 · identical 0 · last 2026-06-30 by Claude · merged PR (#708 closed merged 2026-06-30) · tip `ccfeaab2f`

- `.github/copilot-instructions.md`

### `claude/masons-and-mormons-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `cbfaaafac`

- `MASONS-AND-MORMONS.md`

### `claude/metatron-research-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `5362c68b1`

- `METATRON.md`

### `claude/propose-suggestions-ready`

forks 2026-06-19 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-06-19 by Claude · merged PR (#577 closed merged 2026-06-19) · tip `2a53503cc`

- `tests/test_review_feedback_loop.py`

### `claude/ptolemy-research-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `62a802aba`

- `PTOLEMY.md`

### `claude/rework-census-doctrine-463-4033po`

forks 2026-08-25 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-08-25 by Claude Code · merged PR (#820 closed merged 2026-08-25) · tip `62c59e5c5`

- `.github/scripts/test_topology_census.py`

### `claude/serene-heisenberg-8ltqb5`

forks 2026-06-30 · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-06-30 by Claude · merged PR (#713 closed merged 2026-06-30) · tip `39e5cecd7`

- `tests/test_review_feedback_loop.py`

### `claude/socrates-journal-2026-05-31`

forks 2026-05-28 · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-31 by Claude · no PR · tip `224bf6388`

- `SOCRATES-JOURNAL-2026-05-31.md`

### `claude/socrates-research-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by Claude · no PR · tip `df637199a`

- `SOCRATES.md`

### `claude/the-binder-magicians-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `e7c1dcb93`

- `THE-BINDER-AND-BOOK-OF-THE-BINDER.md`

### `claude/to-will-and-to-halt-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `6c36f4e1b`

- `TO-WILL-AND-TO-HALT.md`

### `claude/witness-fire-brazen-head-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by github-actions[bot] · no PR · tip `d2386515f`

- `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-29-THE-FIRE-AND-THE-BRAZEN-HEAD.md`

### `claude/witness-novice-what-the-novice-does-not-know-2026-05-30`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by Claude · no PR · tip `a8c8c0265`

- `WITNESS-NOVICE-2026-05-30-WHAT-THE-NOVICE-DOES-NOT-KNOW.md`

### `claude/witness-the-hand-2026-05-29`

forks 2026-05-28 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-29 by github-actions[bot] · no PR · tip `30877ce19`

- `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-29-THE-HAND.md`

### `claude/witness-usurpers-triptych-2026-05-30`

forks 2026-05-28 · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-05-30 by github-actions[bot] · no PR · tip `46d271ec3`

- `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-30-THE-USURPERS-TRIPTYCH.md`

### `codex/codex-work-surface-guard`

forks 2026-06-18 · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-06-18 by Logan Finney · merged PR (#567 closed merged 2026-06-18; #564 closed merged 2026-06-18) · tip `5a08f736a`

- `!/PULLMAN-CLOUD-RUN-SNAPSHOT-BACKUP-2026-06-18.md`

### `codex/example-low-risk-pr-flow-2026-04-23`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-04-23 by Logan Finney · closed PR, unmerged (#299 closed) · tip `cf91deca3`

- `.github/swarm/automation-probe-low-risk-2026-04-23.md`

### `codex/github-mention-add-handoff-note-acknowledging-codex-mention`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-30 by logan · closed PR, unmerged (#113 closed) · tip `b5c947a3c`

- `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md`

### `codex/github-mention-add-handoff-note-acknowledging-codex-mention-0t7ech`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-30 by logan · closed PR, unmerged (#114 closed) · tip `8dee046c8`

- `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md`

### `codex/github-mention-add-handoff-note-acknowledging-codex-mention-16l2ya`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-30 by logan · closed PR, unmerged (#115 closed) · tip `f4b245b2a`

- `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md`

### `codex/linear-mention-laf-11-define-routing-rules-for-,-/,`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#91 closed) · tip `fea96bac3`

- `!/VAULT-ZONES.md`

### `codex/linear-mention-laf-12-break-out-the-courtroom-into-project`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#92 closed) · tip `8d5c28fec`

- `!/!/!/! The world is quiet here/DOCKET.md`

### `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf`

island · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-08-19 by Logan A. Finney · closed PR, unmerged (#85 closed) · tip `3cab31a6c`

- `.github/scripts/linear_pr_sync.py`

### `codex/linear-mention-laf-19-ping-emitted.-033026.0136]`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#123 closed) · tip `abe358161`

- `!/BRIEF-LAF-19-2026-04-01.md`

### `codex/linear-mention-laf-23-gemini-code-partner-report`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#124 closed) · tip `23a3c64c5`

- `.github/workflows/auto-pr.yml`

### `codex/linear-mention-laf-23-gemini-code-partner-report-t311rs`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-31 by logan · closed PR, unmerged (#127 closed) · tip `44628a60e`

- `.github/workflows/auto-pr.yml`

### `codex/linear-mention-laf-7-swarm-coordination-agent-assembly`

island · own commits 1 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#86 closed) · tip `0ba37e6f4`

- `!/!/!/! The world is quiet here/DOCKET.md`

### `codex/revise-persona-and-constitutional-files`

island · own commits 1 · files touched 3 · `main` lacks 1 · differ 2 · identical 0 · last 2026-03-28 by logan · closed PR, unmerged (#84 closed) · tip `892d28083`

- `!/CONSTITUTION.md`

### `dependabot/github_actions/actions/checkout-6`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-03-31 by dependabot[bot] · merged PR (#121 closed; #31 closed merged 2026-03-23) · tip `831f8b37f`

- `.github/workflows/pr-linear-sync.yml`

### `hyperagent/developer-0-esto-perpetua-provenance`

forks 2026-06-30 · own commits 2 · files touched 1 · `main` lacks 1 · differ 0 · identical 0 · last 2026-06-30 by Logan A. Finney · no PR · tip `e29196d19`

- `WITNESS-HYPERAGENT-DEVELOPER-0-VAULTED-SYNTAX-AND-CORRECTIONS-2026-06-30.md`

### `ingest-2026-04-09T100606Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-09 by github-actions[bot] · closed PR, unmerged (#194 closed) · tip `dffa7f7ef`

- `!/ingest-2026-04-09T100606Z.md`

### `ingest-2026-04-17T130149Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-17 by github-actions[bot] · closed PR, unmerged (#281 closed) · tip `4bf000811`

- `!/ingest-2026-04-17T130149Z.md`

### `ingest-2026-04-19T124314Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-19 by github-actions[bot] · closed PR, unmerged (#264 closed) · tip `a5b0ec909`

- `!/ingest-2026-04-19T124314Z.md`

### `ingest-2026-04-22T131021Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-22 by github-actions[bot] · closed PR, unmerged (#290 closed) · tip `49d8f8949`

- `!/ingest-2026-04-22T131021Z.md`

### `ingest-2026-04-26T124810Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-26 by github-actions[bot] · closed PR, unmerged (#306 closed) · tip `3cd97083e`

- `!/ingest-2026-04-26T124810Z.md`

### `ingest-2026-04-27T132259Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-04-27 by github-actions[bot] · closed PR, unmerged (#308 closed) · tip `cbf97b924`

- `!/ingest-2026-04-27T132259Z.md`

### `ingest-2026-05-09T125235Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-09 by github-actions[bot] · closed PR, unmerged (#319 closed) · tip `16c689b9b`

- `!/ingest-2026-05-09T125235Z.md`

### `ingest-2026-05-10T125330Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-10 by github-actions[bot] · closed PR, unmerged (#320 closed) · tip `5c94a4843`

- `!/ingest-2026-05-10T125330Z.md`

### `ingest-2026-05-11T142514Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-11 by github-actions[bot] · closed PR, unmerged (#323 closed) · tip `b9f91e7f2`

- `!/ingest-2026-05-11T142514Z.md`

### `ingest-2026-05-12T135222Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-12 by github-actions[bot] · closed PR, unmerged (#325 closed) · tip `4c83f4dfe`

- `!/ingest-2026-05-12T135222Z.md`

### `ingest-2026-05-13T140457Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-13 by github-actions[bot] · closed PR, unmerged (#326 closed) · tip `95b51d2bd`

- `!/ingest-2026-05-13T140457Z.md`

### `ingest-2026-05-14T132834Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-14 by github-actions[bot] · closed PR, unmerged (#337 closed) · tip `c13ff4d9f`

- `!/ingest-2026-05-14T132834Z.md`

### `ingest-2026-05-15T132754Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-15 by github-actions[bot] · closed PR, unmerged (#338 closed) · tip `7d4c04437`

- `!/ingest-2026-05-15T132754Z.md`

### `ingest-2026-05-16T125701Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-16 by github-actions[bot] · closed PR, unmerged (#339 closed) · tip `17b3217fa`

- `!/ingest-2026-05-16T125701Z.md`

### `ingest-2026-05-17T125448Z`

island · own commits 1 · files touched 2 · `main` lacks 1 · differ 1 · identical 0 · last 2026-05-17 by github-actions[bot] · closed PR, unmerged (#340 closed) · tip `1d9bed906`

- `!/ingest-2026-05-17T125448Z.md`

### `review/pr-471-agent-swarm-signing`

forks 2026-06-04 · own commits 1 · files touched 4 · `main` lacks 1 · differ 3 · identical 0 · last 2026-06-16 by Logan Finney · no PR · tip `e16a4aa0f`

- `VERSION-TRANSITIONS.md`

## Branches whose own files are all in `main`, identical

Nothing to salvage by content. Under ARBORSCAPE these are PRUNE candidates once Logan
says so; nothing is pruned by this report. `logan/obsidian/android` appears on the
count alone and is not a candidate: per `coord/MAC-STATUS.md` (2026-09-09) the
`logan/obsidian/*` branches are Logan's own Obsidian working branches under git-flow,
outside branch gardening.

- `agent/mcp-probe` — forks 2026-07-01, own commits 2, files 1, last 2026-07-02, no PR
- `claude/docket-posture-transclusion` — forks 2026-06-30, own commits 2, files 1, last 2026-06-30, merged PR
- `claude/update-claude-files-PRWCJ` — island, own commits 2, files 1, last 2026-05-22, closed PR, unmerged
- `codex/example-high-risk-pr-flow-2026-04-23` — island, own commits 1, files 1, last 2026-04-23, closed PR, unmerged
- `logan/obsidian/android` — forks 2026-08-27, own commits 2, files 7, last 2026-09-10, no PR
- `wayback-audit-20260615143859-clean` — forks 2026-08-04, own commits 2, files 1, last 2026-08-04, no PR

## Branches with no commit of their own

The tip of each is reachable from another ref, so the branch name adds nothing to what
origin already holds elsewhere.

- `claude/resolve-pr-conflicts` — island, last 2026-03-30, merged PR
- `codex/research-import-batch-2026-04-16` — island, last 2026-04-17, closed PR, unmerged
- `dependabot/uv/uv-aa7cb66ac2` — island, last 2026-04-16, closed PR, unmerged
- `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` — forks 2026-07-01, last 2026-07-01, no PR
- `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` — forks 2026-07-01, last 2026-07-02, no PR
- `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` — forks 2026-07-01, last 2026-07-02, no PR
- `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` — forks 2026-07-01, last 2026-07-02, no PR
- `logan/obsidian/main` — forks 2026-08-11, last 2026-09-02, open PR
- `orphancry/pr-388-original-automation-sync-dependencies` — forks 2026-06-23, last 2026-06-23, no PR
- `recovered/pr-353` — island, last 2026-05-22, no PR

## Merge-queue leftovers

`gh-readonly-queue/main/pr-*` refs are the temporary branches GitHub's merge queue builds
each candidate on and normally deletes. Six remain from 2026-07-01 and 2026-07-02.

- `gh-readonly-queue/main/pr-475-497da14475f83833feed873fdea5e24769d010e0` — own commits 1, files `main` lacks 0, differ 1
- `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` — own commits 0, files `main` lacks 0, differ 0
- `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e` — own commits 1, files `main` lacks 18, differ 2
- `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` — own commits 0, files `main` lacks 0, differ 0
- `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` — own commits 0, files `main` lacks 0, differ 0
- `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` — own commits 0, files `main` lacks 0, differ 0

## Against the May 25 report

[[!-ARBORSCAPING-REPORT-2026-05-25]] classified seven local branches. On origin today:

- `bot/daily-rollover-2026-04-24` — still on origin; own commits 1, files `main` lacks 0, differ 1, identical 0; closed PR, unmerged
- `bot/daily-rollover-2026-04-25` — still on origin; own commits 1, files `main` lacks 0, differ 1, identical 0; closed PR, unmerged
- `codex/example-high-risk-pr-flow-2026-04-23` — still on origin; own commits 1, files `main` lacks 0, differ 0, identical 1; closed PR, unmerged
- `codex/example-low-risk-pr-flow-2026-04-23` — still on origin; own commits 1, files `main` lacks 1, differ 0, identical 0; closed PR, unmerged
- `ingest-2026-04-24T130510Z` — still on origin; own commits 1, files `main` lacks 0, differ 1, identical 1; closed PR, unmerged
- `ingest-2026-04-25T124501Z` — still on origin; own commits 1, files `main` lacks 0, differ 1, identical 1; closed PR, unmerged
- `copilot/filter-secret-scanning-alerts` — no longer on origin; [[!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17]] records its deletion after salvage

The May 25 PRUNE candidates whose payload it found in trunk now show that payload as
*differing* from `main`, not identical: the daily notes and probe stubs were edited on
`main` after the census. That is consistent with the earlier finding, not a reversal.

## Finding: the frontmatter of `VAULT-CONVENTIONS.md` is tooling residue

Raised by Logan in the same session. The block at the top of `VAULT-CONVENTIONS.md` on
`main` carries `authority: LOGAN`, then a `related:` list of sixty tokens ("THE", "Act",
"DOS", "emoji", "syntax", "Yes"-class words alongside real note names), then
`date created: Sunday, April 12th 2026, 4:02:32 am` and a matching `date modified`.
`VAULT-METADATA-STANDARD.md` asks for `title`, `updated`, `status` and `authority`, with
`created` and `related` as optional fields "used only when useful; avoid metadata bloat".

- `git blame -L 1,67` attributes the whole block to one commit, db2e4c05e (2026-06-30,
  "fix(pr-680)"), which is one of `main`'s 22 root commits: the block arrived wholesale
  from a machine-side tree, not from an edit in a pull request.
- The same two shapes appear vault-wide: 12,739 tracked notes carry a `related:` list
  and 634 carry the weekday-spelled `date created`/`date modified` pair. `DECISIONS.md`,
  `VAULT-TEMPLATES.md`, `!README.md` and `!/WAKEUP.md` carry one or both.
- No script in the repository writes `related:`. `scripts_scripts/metadata_survey.py`
  counts it; `scripts_scripts/laf_usb_manifest.py` validates it; `daily_rollover.py`
  writes `date created`/`date modified` for daily notes only. The generator is on the
  Obsidian side, and plugin settings are gitignored by design (`VAULT-CONVENTIONS.md`
  § "Obsidian Sync / Git Boundary"), so this census cannot name the plugin: `*`.
- Not done here: rewriting that block on `main`. It would be regenerated at the next
  machine-side pass while the generator runs, and `coord/MAC-STATUS.md` (2026-09-09)
  records a pared, scar-cleaned `VAULT-CONVENTIONS.md` on the Mac's `develop` that has
  not reached origin; an edit here would collide with it. Disposition is Logan's: switch
  the generator off on the devices, or accept the fields and let the standard say so.

## Proposed next actions

All pending Logan; verbs per the ARCHIPELAGO protocol.

1. **read** — the salvage candidates with fewer than fifty files `main` lacks, by
   `git show <branch>:<path>`, to sort note from residue. The 27 research and witness
   branches of 2026-05-28 to 05-31 under `claude/` are the largest coherent group: one
   note each, never a PR.
2. **route to ARBORSCAPE** — the islands whose closed PRs and closed matters are
   already recorded, once their own files are read; the House rule leaves their PR
   numbers as they are.
3. **ignore with evidence** — the six merge-queue leftovers and the ten branches with no
   commit of their own, once Logan confirms the evidence above.
4. **ask Logan** — the reunification line (`logan/obsidian/*`,
   `claude/reunify-mac-win-6c80a94c`, `orphancry/pr-926-original-logan-obsidian`,
   `wayback-audit-20260420100033`): these are the matter of #1029 and of the
   machine-side consolidation, not of branch gardening.
5. **preserve** — nothing here needs a new preserved ref; every branch is still on origin.

No branch is deleted by this report, and none should be until Logan enters the endings.

## Full census

One row per branch on origin. "Own commits" are commits no other ref reaches. Islands
have no fork point. Visibility class per the ARCHIPELAGO protocol; risk class likewise.

| Branch | Lineage | Own commits | Files touched | `main` lacks | Differ | Identical | Last commit | Author | PR history | Visibility | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `add-garth-nix-old-kingdom-2026-06-02` | forks 2026-05-28 | 1 | 1 | 0 | 1 | 0 | 2026-06-01 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `agent/attest-resolve-dispatch` | forks 2026-07-01 | 1 | 1 | 1 | 0 | 0 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `agent/mcp-probe` | forks 2026-07-01 | 2 | 1 | 0 | 0 | 0 | 2026-07-02 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `antigravity/pullman-oidc-pipeline` | island | 3 | 0 | 0 | 0 | 0 | 2026-04-12 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `bot/daily-rollover-2026-04-03` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-03 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-04` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-04 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-05` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-05 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-13` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-13 | github-actions[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-18` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-18 | github-actions[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-20` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-20 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-22` | island | 1 | 2 | 0 | 2 | 0 | 2026-04-22 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-24` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-24 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-25` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-25 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-26` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-26 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `circleci-project-setup` | forks 2026-08-14 | 1 | 1 | 0 | 1 | 0 | 2026-08-14 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/add-legal-references` | island | 1 | 0 | 0 | 0 | 0 | 2026-04-09 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/agent-representation-etymology-2026-05-29` | forks 2026-05-28 | 3 | 0 | 0 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/allow-force-push-to-main` | island | 2 | 2 | 2 | 0 | 0 | 2026-04-01 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/anchors-lesson-and-hermes-trismegistus-2026-05-29` | forks 2026-05-28 | 5 | 0 | 0 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/apprentice-modes-sorcerers-and-rangers-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/bind-frankenstein-persona-2026-05-30` | forks 2026-05-28 | 3 | 0 | 0 | 0 | 0 | 2026-05-30 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/bot-automerge-fix` | island | 2 | 3 | 2 | 1 | 0 | 2026-04-04 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/check-farnsworth-transcripts-UbMD3` | island | 1 | 2,354 | 2 | 1,558 | 761 | 2026-04-06 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/docket-posture-transclusion` | forks 2026-06-30 | 2 | 1 | 0 | 0 | 1 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fablehaven-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fablehaven-beastiary-2026-05-30` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/finish-hashtag-escape-9gesn5` | forks 2026-08-04 | 10 | 0 | 0 | 0 | 0 | 2026-08-06 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fix-todo-references` | island | 2 | 7 | 1 | 6 | 0 | 2026-04-18 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/geminiaeus-live-board-witness` | forks 2026-06-30 | 1 | 1 | 0 | 1 | 0 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/godhead-disambiguation-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/harden-py-automation-followup-562` | forks 2026-08-02 | 7 | 0 | 0 | 0 | 0 | 2026-08-19 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/hebrew-bible-and-talmud-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/heisenberg-uncertainty-2026-05-30` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/honeypot-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/initiation-rituals-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/janus-and-sugar-bowl-witness-companion-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/lds-tripart-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/levelset-refresh-2026-03-29` | island | 4 | 0 | 0 | 0 | 0 | 2026-03-30 | Logan Finney | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/listening-lore-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/live-board-dedrift` | forks 2026-06-30 | 1 | 5 | 1 | 4 | 0 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/masons-and-mormons-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/metatron-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/obsidian-plugins-triage-YDJ6Z` | island | 1 | 2 | 2 | 0 | 0 | 2026-04-07 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/preserve/codex-github-automation-hardening-2026-05-22` | island | 2 | 1 | 0 | 1 | 0 | 2026-05-22 | Logan Finney | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/preserve/codex-swarm-mvp-github-intake` | island | 3 | 0 | 0 | 0 | 0 | 2026-05-22 | Logan Finney | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/propose-suggestions-ready` | forks 2026-06-19 | 1 | 1 | 1 | 0 | 0 | 2026-06-19 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/provision-socrates-chamber-2026-05-29` | forks 2026-05-28 | 4 | 0 | 0 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/ptolemy-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/repo-size-compliance-5accf9` | island | 1 | 139 | 0 | 2 | 0 | 2026-04-01 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/research-abhorsen-old-kingdom` | island | 5 | 0 | 0 | 0 | 0 | 2026-05-28 | github-actions[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/research-attestation` | forks 2026-07-28 | 4 | 5 | 0 | 4 | 0 | 2026-08-04 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/resolve-pr-conflicts` | island | 0 | 0 | 0 | 0 | 0 | 2026-03-30 | logan | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/reunify-mac-win-6c80a94c` | forks 2026-08-04 | 1998 | 0 | 0 | 0 | 0 | 2026-08-12 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/rework-census-doctrine-463-4033po` | forks 2026-08-25 | 1 | 1 | 1 | 0 | 0 | 2026-08-25 | Claude Code | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/serene-heisenberg-8ltqb5` | forks 2026-06-30 | 1 | 2 | 1 | 1 | 0 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/socrates-journal-2026-05-31` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 2026-05-31 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/socrates-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/sugar-bowl-witness-2026-05-28` | island | 2 | 1 | 0 | 1 | 0 | 2026-05-28 | github-actions[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/sweep-enqueue-unstable-prs` | forks 2026-06-24 | 1 | 0 | 0 | 0 | 0 | 2026-06-24 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/the-binder-magicians-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/to-will-and-to-halt-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/update-claude-files-PRWCJ` | island | 2 | 1 | 0 | 0 | 1 | 2026-05-22 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/witness-fire-brazen-head-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-novice-what-the-novice-does-not-know-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-the-hand-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 2026-05-29 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-usurpers-triptych-2026-05-30` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 2026-05-30 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/add-legal-references` | island | 2 | 1 | 0 | 1 | 0 | 2026-04-09 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/arborscaping-merge-base` | island | 1 | 2 | 2 | 0 | 0 | 2026-05-26 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/audit-swarm-liveness-semantics-2026-06-10` | forks 2026-06-11 | 1 | 13 | 0 | 2 | 0 | 2026-06-16 | Logan Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/background-rhythm` | island | 5 | 0 | 0 | 0 | 0 | 2026-04-07 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/codex-work-surface-guard` | forks 2026-06-18 | 1 | 1 | 1 | 0 | 0 | 2026-06-18 | Logan Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/create-manifest.json-specification-and-guidelines` | island | 1 | 6 | 4 | 2 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/example-high-risk-pr-flow-2026-04-23` | island | 1 | 1 | 0 | 0 | 1 | 2026-04-23 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/example-low-risk-pr-flow-2026-04-23` | island | 1 | 1 | 1 | 0 | 0 | 2026-04-23 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/fix-high-priority-bug-in-pr-#34` | island | 3 | 0 | 0 | 0 | 0 | 2026-03-23 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/fix-worktree-registry-hook` | forks 2026-06-11 | 1 | 8 | 4 | 4 | 0 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/get-pr-in-merge-passable-state` | island | 6 | 1 | 0 | 1 | 0 | 2026-04-18 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-automation-hardening-2026-05-22` | island | 2 | 1 | 0 | 1 | 0 | 2026-05-22 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-dependency-census` | forks 2026-06-11 | 1 | 5 | 5 | 0 | 0 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-0t7ech` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-16l2ya` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/greet-user-with-a-friendly-message` | island | 1 | 10 | 4 | 5 | 1 | 2026-04-28 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-11-define-routing-rules-for-,-/,` | island | 1 | 2 | 1 | 1 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-12-break-out-the-courtroom-into-project` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf` | island | 2 | 1 | 1 | 0 | 0 | 2026-08-19 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-18-gemini-google-cloud` | island | 1 | 3 | 3 | 0 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-19-ping-emitted.-033026.0136]` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-23-gemini-code-partner-report` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-23-gemini-code-partner-report-t311rs` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-25-project-hexagonal` | island | 1 | 3 | 2 | 1 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-25-project-hexagonal-pupxlq` | island | 1 | 3 | 2 | 1 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-7-swarm-coordination-agent-assembly` | island | 1 | 1 | 1 | 0 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-9-define-vault-template-and-document-cl` | island | 1 | 4 | 3 | 1 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/live-state-snapshot` | island | 3 | 0 | 0 | 0 | 0 | 2026-04-12 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/research-import-batch-2026-04-16` | island | 0 | 0 | 0 | 0 | 0 | 2026-04-17 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/revise-persona-and-constitutional-files` | island | 1 | 3 | 1 | 2 | 0 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/swarm-mvp-github-intake` | island | 3 | 0 | 0 | 0 | 0 | 2026-05-22 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/tantalus-tautomata-campaign-2026-06-04` | forks 2026-06-03 | 1 | 20 | 18 | 2 | 0 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/touchstone-corpus-repair-clean` | island | 4 | 0 | 0 | 0 | 0 | 2026-04-10 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/update-branch-protection-rules` | island | 1 | 0 | 0 | 0 | 0 | 2026-04-01 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/version-drift-ledger` | island | 3 | 0 | 0 | 0 | 0 | 2026-05-26 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/worm-watch-hardening` | island | 3 | 0 | 0 | 0 | 0 | 2026-05-17 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `coord/win-mac` | forks 2026-08-27 | 9 | 0 | 0 | 0 | 0 | 2026-09-09 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `copilot/coordinating-hexagonal-hub` | island | 1 | 0 | 0 | 0 | 0 | 2026-04-01 | copilot-swe-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `copilot/debug-github-actions-failures` | island | 2 | 2 | 2 | 0 | 0 | 2026-04-01 | copilot-swe-agent[bot] | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `copilot/help-logan-overwhelmed` | island | 4 | 0 | 0 | 0 | 0 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `dependabot/github_actions/actions/checkout-6` | island | 1 | 2 | 1 | 1 | 0 | 2026-03-31 | dependabot[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/github_actions/actions/checkout-6.0.2` | island | 1 | 28 | 25 | 3 | 0 | 2026-05-27 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/github_actions/actions/setup-python-6.2.0` | island | 1 | 9 | 9 | 0 | 0 | 2026-05-27 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/npm_and_yarn/dot-antigravity/extensions/ms-edgedevtools.vscode-edge-devtools-2.1.10-universal/npm_and_yarn-209087bb4f` | island | 1 | 7 | 7 | 0 | 0 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/click-8.4.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/cryptography-48.0.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/google-cloud-pubsub-2.36.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-08 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/lancedb-0.30.2` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/lxml-gte-6.1.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/mcp-1.27.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-api-1.41.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-exporter-otlp-proto-common-1.42.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-exporter-otlp-proto-grpc-1.41.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/pdfminer-six-20260107` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/portalocker-3.2.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/posthog-7.15.4` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/propcache-0.5.2` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/protobuf-7.35.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-25 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/rich-15.0.0` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/typer-0.25.1` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-2fce4a7a35` | island | 1 | 1 | 0 | 1 | 0 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-aa7cb66ac2` | island | 0 | 0 | 0 | 0 | 0 | 2026-04-16 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-b06552e8ac` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-c30c77f42d` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-f81bb61997` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-21 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `fix/record-vaulted-abhorsens-first-2026-05-31-clean` | forks 2026-06-07 | 4 | 0 | 0 | 0 | 0 | 2026-06-07 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `gh-readonly-queue/main/pr-475-497da14475f83833feed873fdea5e24769d010e0` | forks 2026-07-01 | 1 | 1 | 0 | 1 | 0 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e` | forks 2026-07-01 | 1 | 20 | 18 | 2 | 0 | 2026-07-02 | dependabot[bot] | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 2026-07-02 | dependabot[bot] | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 2026-07-02 | Claude | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 2026-07-02 | Claude | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `hyperagent/developer-0-esto-perpetua-provenance` | forks 2026-06-30 | 2 | 1 | 1 | 0 | 0 | 2026-06-30 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `ingest-2026-04-09T100606Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-09T130617Z` | island | 7 | 0 | 0 | 0 | 0 | 2026-04-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-17T130149Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-17 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-19T124314Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-19 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-22T131021Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-22 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-24T130510Z` | island | 1 | 2 | 0 | 1 | 1 | 2026-04-24 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-25T124501Z` | island | 1 | 2 | 0 | 1 | 1 | 2026-04-25 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-26T124810Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-26 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-27T132259Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-04-27 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-09T125235Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-10T125330Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-10 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-11T142514Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-11 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-12T135222Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-12 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-13T140457Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-13 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-14T132834Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-14 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-15T132754Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-15 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-16T125701Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-16 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-17T125448Z` | island | 1 | 2 | 1 | 1 | 0 | 2026-05-17 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `logan/obsidian/android` | forks 2026-08-27 | 2 | 7 | 0 | 0 | 0 | 2026-09-10 | loganfinney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `logan/obsidian/macos` | forks 2026-08-11 | 18 | 0 | 0 | 0 | 0 | 2026-09-04 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `logan/obsidian/main` | forks 2026-08-11 | 0 | 0 | 0 | 0 | 0 | 2026-09-02 | Logan Finney | open PR | BRANCH-ONLY | LIVING-WORK |
| `orphancry/pr-388-original-automation-sync-dependencies` | forks 2026-06-23 | 0 | 0 | 0 | 0 | 0 | 2026-06-23 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `orphancry/pr-926-original-logan-obsidian` | island | 3001 | 0 | 0 | 0 | 0 | 2026-08-14 | loganfinneyPTV | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `recovered/pr-324` | island | 1 | 1 | 0 | 1 | 0 | 2026-05-13 | dependabot[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `recovered/pr-353` | island | 0 | 0 | 0 | 0 | 0 | 2026-05-22 | Claude | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `review/pr-471-agent-swarm-signing` | forks 2026-06-04 | 1 | 4 | 1 | 3 | 0 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `test/push-gate-20260828` | forks 2026-08-27 | 1 | 0 | 0 | 0 | 0 | 2026-08-28 | loganfinneyPTV | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `test/tier2-signing-2026-05-29` | forks 2026-05-28 | 1 | 0 | 0 | 0 | 0 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `wayback-audit-20260420100033` | forks 2026-08-19 | 2 | 2 | 2 | 0 | 0 | 2026-08-20 | loganfinney27 | closed PR, unmerged | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `wayback-audit-20260615143859-clean` | forks 2026-08-04 | 2 | 1 | 0 | 0 | 1 | 2026-08-04 | Vibe Nuage Agent | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |

## Reservation

No ref was created, moved or deleted, no pull request touched, no history rewritten.
Historical censuses remain evidence of what they recorded when filed. The counts above
are reproducible from the Method with the same clone; the readings of file content that
the salvage decisions need have not been made here and are not implied.

---

## DOCUMENT METADATA

- **Created:** 2026-09-23
- **Last Updated:** 2026-09-23
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI, cloud session (session_01MthFdsNfRK8S4gUivqV9XY)
- **Change Note:** First filing: census of the 170 branches on origin, salvage and prune candidates, the frontmatter finding on `VAULT-CONVENTIONS.md`.
