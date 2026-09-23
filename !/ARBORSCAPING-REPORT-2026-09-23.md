---
title: "ARBORSCAPING REPORT — 2026-09-23 — census of the branches on origin"
created: 2026-09-23
updated: 2026-09-23
status: draft
authority: LOGAN
authors:
  - "Claude Code CLI, cloud session (session_01MthFdsNfRK8S4gUivqV9XY)"
doc_class: report
source: "`.github/scripts/branch_census.py` against origin (LAF-US/IDAHO-VAULT), fetched and pruned 2026-09-23; GitHub pull-request history per branch"
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
reported three vault branches where origin holds 170. Filed in the series of
[[!/ARBORSCAPING-REPORT-2026-04-16]] and [[!-ARBORSCAPING-REPORT-2026-05-25]], under the
ARBORSCAPING protocol with the ARCHIPELAGO visibility and risk classes.

A dated census is stale the moment a branch moves. So the census is a command,
`.github/scripts/branch_census.py`, and this note is one run of it plus the readings a
human still has to make on top. The block between the two marker comments below is
written by the script and refreshed by rerunning it; nothing in it is edited by hand.

The census records what origin holds and what each branch holds that `main` does not.
It does not delete a branch, move a ref, close a pull request, rewrite history, or
promote any found text. Every ending here is proposed, not entered; Logan decides which
applies (`CONSTITUTION.md` § VII; `!/WAKEUP.md` "When Work Resolves"). A branch that
appears here is proven reachable on origin as of the fetch, nothing more.

Scope is **origin only**. The machine-side consolidation recorded on `coord/win-mac`
(`coord/MAC-STATUS.md`, 2026-09-07 to 09-09) merged 123 local Mac branches into the
Mac's `develop` and unified the Windows base on the full-history line; neither tree has
reached origin, both gated on the history rewrite that note describes. This census
cannot see them and does not speak for them (`*`).

## How to regenerate

```text
gh api --paginate "repos/LAF-US/IDAHO-VAULT/pulls?state=all&per_page=100" \
  --jq '.[] | {head: .head.ref, number: .number, state: .state, merged: (.merged_at != null)}' \
  > prs.jsonl
python3 .github/scripts/branch_census.py --fetch --prs prs.jsonl --since 2026-08-01 \
  --history-before 2026-03-01 --update '!/ARBORSCAPING-REPORT-2026-09-23.md'
```

Per branch the script measures: the merge base with `main`, or none (an island: per the
ARCHIPELAGO protocol, not "ahead" or "behind"); own commits, `git rev-list --no-merges
<branch> --not origin/main <every other branch>`; the paths those commits touched and,
for each, whether `main` lacks it, holds it identical, or holds a different version; the
whole tree against `main`'s (`git diff --name-status`); root commits and oldest date;
last commit; pull-request history from the export; the ARCHIPELAGO classes. `--json`
writes every row with its full path lists. The script's docstring carries the rest.

## Correction to the first filing

The first filing of this note (commit 5a4b64782, earlier the same day) was produced from
scratch commands outside the vault. One of them handed several commits to a single
`git diff-tree` call; git reads the third argument onward as paths, so every branch with
more than one own commit came out with no paths at all. The salvage list read 79
branches; it is 107. The own-commit column also counted merge commits while the Method
said non-merge. Porting the generator into the vault surfaced both. The generated block
is the script's; the first filing's counts are superseded.

## Readings a human still has to make

### The oldest history origin reaches

`main`'s own history begins 2026-05-25; nothing it reaches is dated earlier. The islands
carry the lineage GitHub received from 2026-03-11 on. Before that lie 42 commits in seven
batches of six, 2024-12-17 to 2026-01-05 (subjects "vault-cleanup", "vault-commit",
"generic push", "file edits", "Oxford addition", "generic update", ".obsidian"), listed
in the generated block under "History older than anything `main` reaches". Origin holds
six root commits dated 2024-12-17, each carried by between 4 and 22 refs; the 2026-01-05
snapshot is carried by 17. `wayback-audit-20260420100033` reaches them through its merge
11860aea0 (2026-08-20, "bridge: reconnect historical PR #282 to main"), which joined
them to a fork of today's `main`. The tree at the oldest of them holds 2,904 paths; at
2026-01-05, 2,958. That is the early vault as GitHub received it, in snapshots, still on
origin. Anything between 2026-01-05 and the 2026-04-22 secrets purge, and anything that
only ever lived on a machine, is not on origin under any ref this census can see (`*`).

### The reunification line

Four forks hold a thousand or more paths `main` lacks, tree against tree:
`logan/obsidian/macos` (127,555), `logan/obsidian/main` (83,994),
`claude/reunify-mac-win-6c80a94c` (52,239) and `logan/obsidian/android` (3,730). Every
other fork sits near 555, the count of paths `main` has deleted since late May, which
says nothing about the branch. Read with `coord/MAC-STATUS.md`: `logan/obsidian/macos`
on origin is the 2026-09-04 `.gitflow` commit; `logan/obsidian/main` is PR #1029, the
ancestry-recovery matter; `claude/reunify-mac-win-6c80a94c` the August attempt at the
same reunification; `logan/obsidian/android` two GitSync commits; `coord/win-mac` one
file, the coordination note itself. Per that note the `logan/obsidian/*` branches are
Logan's own git-flow working branches, outside branch gardening. These are the matter of
#1029 and of the machine-side consolidation.

### The salvage list, read as a whole

107 branches hold paths `main` lacks. Three are the lineage carriers above (58,255,
44,075 and 3,967 paths by own commits) and are not read path by path.
`claude/finish-hashtag-escape-9gesn5` holds 148. The other 103 are small: 78 hold one or
two paths, 93 hold eight or fewer. The largest coherent group is 26 `claude/` research
and witness branches forked 2026-05-28 and last committed 05-29 to 05-31, one to five own
commits each, one to five paths `main` lacks, never a PR. Among the islands, 60 hold
paths `main` lacks; the largest payloads are `codex/live-state-snapshot` (106),
`orphancry/pr-926-original-logan-obsidian` (104), `antigravity/pullman-oidc-pipeline`
(28) and `dependabot/github_actions/actions/checkout-6.0.2` (25). "Paths `main` lacks"
counts paths, not worth: a path may be a note worth keeping, a file removed on purpose,
or generated residue. Classification is by reading, per the May 25 report's rule.

### Against the May 25 report

[[!-ARBORSCAPING-REPORT-2026-05-25]] classified seven local branches. On origin today
the two `bot/daily-rollover`, the two `ingest-` and the two `codex/example-*` branches
are still there, one own commit each, PRs closed unmerged. Five show their payload as
differing from `main` or identical to it, not lacking: the daily notes and probe stubs
were edited on `main` after that census. `codex/example-low-risk-pr-flow-2026-04-23`
holds one path `main` lacks. `copilot/filter-secret-scanning-alerts` is gone;
[[!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17]] records its deletion after salvage.
Consistent with the earlier finding, not a reversal.

### The frontmatter of `VAULT-CONVENTIONS.md` is tooling residue

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

1. **read** — the 103 small salvage payloads, by `git show <branch>:<path>`, to sort
   note from residue; the 26 research branches first, one note each.
2. **route to ARBORSCAPE** — the islands whose closed PRs are already recorded, once
   their own paths are read; the House rule leaves their PR numbers as they are.
3. **ignore with evidence** — the six merge-queue leftovers, the two branches whose own
   paths are all identical in `main`, and the eleven with no non-merge commit of their
   own, once Logan confirms the evidence in the block.
4. **ask Logan** — the reunification line: #1029 and the machine-side consolidation,
   not branch gardening.
5. **preserve** — nothing here needs a new preserved ref; every branch is still on origin.

No branch is deleted by this note, and none should be until Logan enters the endings.

## Census

<!-- branch-census:begin -->

Generated 2026-09-23 14:10 UTC by `.github/scripts/branch_census.py` from `origin`, base `origin/main` at `2abe7f79b` (2026-09-23). Do not edit between the markers; rerun instead:

```text
python3 .github/scripts/branch_census.py --prs prs.jsonl --since 2026-08-01 --history-before 2026-03-01 --update '!/ARBORSCAPING-REPORT-2026-09-23.md'
```

## Headline

| Measure | Value |
|---|---|
| Branches on `origin` besides `main` | 171 |
| `main` | 2,810 commits, tip `2abe7f79b` (2026-09-23), oldest commit 2026-05-25, 22 root commits, 38,796 paths |
| Forks of `main` (share a merge base) | 65 |
| Islands (no merge base with `main`) | 106 |
| Branches whose own commits hold paths `main` lacks | 107 |
| Branches whose own paths are all in `main`, identical | 2 |
| Branches with no non-merge commit of their own | 11 |
| Open pull requests | 1 — #1029 (head `logan/obsidian/main`) |
| Branches whose PR merged and the branch stayed | 17 |
| Branches whose PRs closed unmerged | 94 |
| Branches that never had a PR | 59 |

## Two populations

An island carries a whole lineage `main` does not share, so its ahead/behind count measures that lineage, not work waiting to land. What an island contributed is its own commits, isolated below.

| Population | Branches | Closed unmerged | Merged | Never a PR | Open |
|---|---|---|---|---|---|
| Islands | 106 | 93 | 6 | 7 | 0 |
| Forks | 65 | 1 | 11 | 52 | 1 |

## Recent: forked or committed since 2026-08-01

| Branch | Lineage | Own commits | `main` lacks | Differ | Last commit | PR |
|---|---|---|---|---|---|---|
| `claude/new-session-0riz1k` | forks 2026-09-23 | 1 | 2 | 1 | 2026-09-23 Claude | no PR |
| `logan/obsidian/android` | forks 2026-08-27 | 2 | 3,967 | 1,066 | 2026-09-10 loganfinney | no PR |
| `coord/win-mac` | forks 2026-08-27 | 9 | 1 | 0 | 2026-09-09 Logan Finney | no PR |
| `logan/obsidian/macos` | forks 2026-08-11 | 15 | 44,075 | 21 | 2026-09-04 Logan Finney | no PR |
| `logan/obsidian/main` | forks 2026-08-11 | 0 | 0 | 0 | 2026-09-02 Logan Finney | open PR |
| `test/push-gate-20260828` | forks 2026-08-27 | 1 | 0 | 0 | 2026-08-28 loganfinneyPTV | no PR |
| `claude/rework-census-doctrine-463-4033po` | forks 2026-08-25 | 1 | 1 | 0 | 2026-08-25 Claude Code | merged PR |
| `wayback-audit-20260420100033` | forks 2026-08-19 | 1 | 2 | 0 | 2026-08-20 loganfinney27 | closed PR, unmerged |
| `claude/harden-py-automation-followup-562` | forks 2026-08-02 | 6 | 5 | 1 | 2026-08-19 Logan A. Finney | merged PR |
| `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf` | island | 2 | 2 | 0 | 2026-08-19 Logan A. Finney | closed PR, unmerged |
| `circleci-project-setup` | forks 2026-08-14 | 1 | 0 | 1 | 2026-08-14 Logan A. Finney | no PR |
| `orphancry/pr-926-original-logan-obsidian` | island | 2528 | 104 | 7 | 2026-08-14 loganfinneyPTV | no PR |
| `claude/reunify-mac-win-6c80a94c` | forks 2026-08-04 | 1641 | 58,255 | 766 | 2026-08-12 Logan Finney | no PR |
| `claude/finish-hashtag-escape-9gesn5` | forks 2026-08-04 | 10 | 148 | 2,996 | 2026-08-06 Claude | no PR |
| `claude/research-attestation` | forks 2026-07-28 | 2 | 0 | 5 | 2026-08-04 Logan A. Finney | merged PR |
| `wayback-audit-20260615143859-clean` | forks 2026-08-04 | 2 | 0 | 2 | 2026-08-04 Vibe Nuage Agent | no PR |

## Forks whose whole tree holds 1,000 or more paths `main` lacks

A fork that carries a lineage rather than a diff shows few own commits above; this measures forks tree against tree. "Only here" is a path the branch has and `main` lacks; "only base" the reverse. Islands are left out: their whole tree predates the replant and differs wholesale. "Only here" also counts every path `main` has deleted since the fork point, so ordinary forks share a baseline below the threshold.

| Branch | Only here | Only base | Differ | Renamed | Root commits | Oldest commit |
|---|---|---|---|---|---|---|
| `logan/obsidian/macos` | 127,555 | 2,493 | 1,312 | 7,116 | 13 | 2026-04-22 |
| `logan/obsidian/main` | 83,994 | 2,491 | 1,318 | 7,123 | 13 | 2026-04-22 |
| `claude/reunify-mac-win-6c80a94c` | 52,239 | 2,863 | 1,423 | 6,728 | 7 | 2026-05-25 |
| `logan/obsidian/android` | 3,730 | 8,985 | 1,103 | 237 | 22 | 2026-05-25 |

## History older than anything `main` reaches

`main` reaches nothing dated before 2026-05-25. Across `origin` there are 5,702 commits dated earlier, by month:

| Month | Commits |
|---|---|
| 2024-12 | 12 |
| 2025-03 | 6 |
| 2025-04 | 12 |
| 2025-07 | 6 |
| 2026-01 | 6 |
| 2026-03 | 3,075 |
| 2026-04 | 1,286 |
| 2026-05 | 1,299 |

Dated before 2026-03-01 (`--history-before`), one row per date and subject, 42 commits:

| Date | Commits | Subject |
|---|---|---|
| 2024-12-17 | 6 | vault-cleanup |
| 2024-12-17 | 6 | vault-commit |
| 2025-03-07 | 6 | generic push |
| 2025-04-17 | 6 | file edits |
| 2025-04-23 | 6 | Oxford addition |
| 2025-07-01 | 6 | generic update |
| 2026-01-05 | 6 | .obsidian |

## By family

| Family | Branches | Islands | With paths `main` lacks | With paths that differ | Own paths all identical, or nothing own |
|---|---|---|---|---|---|
| `claude/` | 52 | 14 | 44 | 19 | 3 |
| `codex/` | 37 | 32 | 31 | 20 | 3 |
| `dependabot/` | 25 | 25 | 4 | 22 | 1 |
| `ingest-` | 18 | 18 | 16 | 18 | 0 |
| `bot/daily-rollover` | 10 | 10 | 0 | 10 | 0 |
| `gh-readonly-queue/` | 6 | 0 | 1 | 2 | 4 |
| `other` | 4 | 0 | 1 | 3 | 0 |
| `copilot/` | 3 | 3 | 2 | 0 | 1 |
| `logan/` | 3 | 0 | 2 | 2 | 1 |
| `agent/` | 2 | 0 | 1 | 0 | 1 |
| `orphancry/` | 2 | 1 | 1 | 1 | 1 |
| `recovered/` | 2 | 2 | 0 | 1 | 1 |
| `test/` | 2 | 0 | 0 | 0 | 2 |
| `wayback-audit` | 2 | 0 | 1 | 1 | 0 |
| `antigravity/` | 1 | 1 | 1 | 1 | 0 |
| `hyperagent/` | 1 | 0 | 1 | 0 | 0 |
| `review/` | 1 | 0 | 1 | 1 | 0 |

## Salvage candidates: own commits hold paths `main` lacks

Ranked by that count. It counts paths, not worth: a path the base lacks may be a note worth keeping, a file removed on purpose, or generated residue. Up to 3 paths are shown per branch; `--json` carries them all.

| Branch | Lineage | Own commits | `main` lacks | Differ | Last commit | PR | Paths `main` lacks |
|---|---|---|---|---|---|---|---|
| `claude/reunify-mac-win-6c80a94c` | forks 2026-08-04 | 1641 | 58,255 | 766 | 2026-08-12 Logan Finney | no PR | ` (2).bash_profile`<br>` (2).bashrc`<br>` (2).editorconfig`<br>… and 58,252 more |
| `logan/obsidian/macos` | forks 2026-08-11 | 15 | 44,075 | 21 | 2026-09-04 Logan Finney | no PR | ` (2).gitignore`<br>`! README (2).md`<br>`! The world is quiet here．.md`<br>… and 44,072 more |
| `logan/obsidian/android` | forks 2026-08-27 | 2 | 3,967 | 1,066 | 2026-09-10 loganfinney | no PR | ` (2).bash_profile`<br>` (2).bashrc`<br>` (2).editorconfig`<br>… and 3,964 more |
| `claude/finish-hashtag-escape-9gesn5` | forks 2026-08-04 | 10 | 148 | 2,996 | 2026-08-06 Claude | no PR | `!/__pycache__/resolve_openrouter_secret.cpython-311.pyc`<br>`.claude/skills/run-idaho-vault/__pycache__/driver.cpython-311.pyc`<br>`.codex/skills/.system/skill-installer/scripts/__pycache__/github_utils.cpython-311.pyc`<br>… and 145 more |
| `codex/live-state-snapshot` | island | 3 | 106 | 18 | 2026-04-12 Logan Finney | closed PR, unmerged (#214 closed) | `! PLAN - Large Media LFS Strategy.md`<br>`!/HECATE PROTOCOL.md`<br>`!/MANIFEST.json`<br>… and 103 more |
| `orphancry/pr-926-original-logan-obsidian` | island | 2528 | 104 | 7 | 2026-08-14 loganfinneyPTV | no PR | `'.' (3).md`<br>`.claude/settings.local.json`<br>`.codex/.personality_migration`<br>… and 101 more |
| `antigravity/pullman-oidc-pipeline` | island | 3 | 28 | 14 | 2026-04-12 Logan Finney | closed PR, unmerged (#227 closed) | `!/GRIMOIRE/AFFABLE-BASTION-OIDC-SETUP-2026-04-12.md`<br>`!/INBOX/images/2026-04-11-agent-to-janitor-white-dog.md`<br>`!/INBOX/images/2026-04-12-agent-to-janitor-lane-classification.md`<br>… and 25 more |
| `dependabot/github_actions/actions/checkout-6.0.2` | island | 1 | 25 | 3 | 2026-05-27 dependabot[bot] | closed PR, unmerged (#366 closed) | `.github/workflows/agent-auto-pr.yml`<br>`.github/workflows/agent-review-gate.yml`<br>`.github/workflows/branch-cleanup.yml`<br>… and 22 more |
| `codex/tantalus-tautomata-campaign-2026-06-04` | forks 2026-06-03 | 1 | 18 | 2 | 2026-06-16 Logan Finney | no PR | `!-CAMPAIGN-TANTALUS-TAUTOMATA-ASIMOV-CASCADE-2026-06-04.md`<br>`!-CAMPAIGN-TANTALUS-TAUTOMATA-CHURCHES-OF-KNOWLEDGE-AND-PROOF-2026-06-04.md`<br>`!-CAMPAIGN-TANTALUS-TAUTOMATA-COLLABORATIONNISTES-2026-06-04.md`<br>… and 15 more |
| `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e` | forks 2026-07-01 | 1 | 18 | 2 | 2026-07-02 dependabot[bot] | no PR | `.github/workflows/branch-garden-report.yml`<br>`.github/workflows/check-notebooks-paired.yml`<br>`.github/workflows/cross-platform-smoke.yml`<br>… and 15 more |
| `claude/preserve/codex-github-automation-hardening-2026-05-22` | island | 2 | 13 | 5 | 2026-05-22 Logan Finney | no PR | `.github/workflows/agent-auto-pr.yml`<br>`.github/workflows/branch-cleanup.yml`<br>`.github/workflows/check-portable-paths.yml`<br>… and 10 more |
| `codex/github-automation-hardening-2026-05-22` | island | 2 | 13 | 5 | 2026-05-22 Logan Finney | closed PR, unmerged (#355 closed) | `.github/workflows/agent-auto-pr.yml`<br>`.github/workflows/branch-cleanup.yml`<br>`.github/workflows/check-portable-paths.yml`<br>… and 10 more |
| `codex/background-rhythm` | island | 5 | 11 | 15 | 2026-04-07 Logan Finney | closed PR, unmerged (#182 closed) | `.github/scripts/branch_garden_report.py`<br>`.github/scripts/large_file_watchdog.py`<br>`.github/scripts/stale_bot_prs.py`<br>… and 8 more |
| `dependabot/github_actions/actions/setup-python-6.2.0` | island | 1 | 9 | 0 | 2026-05-27 dependabot[bot] | closed PR, unmerged (#360 closed) | `.github/workflows/daily-rollover.yml`<br>`.github/workflows/laf-usb-manifest-policy.yml`<br>`.github/workflows/large-file-policy.yml`<br>… and 6 more |
| `codex/version-drift-ledger` | island | 3 | 8 | 2 | 2026-05-26 Logan Finney | closed PR, unmerged (#374 closed) | `.github/scripts/check_version_transitions.py`<br>`.github/scripts/validate_content.py`<br>`.github/workflows/dependabot-rhythm.yml`<br>… and 5 more |
| `dependabot/npm_and_yarn/dot-antigravity/extensions/ms-edgedevtools.vscode-edge-devtools-2.1.10-universal/npm_and_yarn-209087bb4f` | island | 1 | 7 | 0 | 2026-04-22 dependabot[bot] | closed PR, unmerged (#288 closed) | `.antigravity/extensions/devsense.composer-php-vscode-1.70.18740-universal/package.json`<br>`.antigravity/extensions/devsense.intelli-php-vscode-0.12.17700-win32-x64/package.json`<br>`.antigravity/extensions/devsense.profiler-php-vscode-1.70.18740-universal/package.json`<br>… and 4 more |
| `claude/preserve/codex-swarm-mvp-github-intake` | island | 3 | 6 | 2 | 2026-05-22 Logan Finney | no PR | `.github/scripts/swarm_mvp_intake.py`<br>`.github/scripts/update_manifest.py`<br>`.github/scripts/validate_content.py`<br>… and 3 more |
| `codex/swarm-mvp-github-intake` | island | 3 | 6 | 2 | 2026-05-22 Logan Finney | closed PR, unmerged (#356 closed) | `.github/scripts/swarm_mvp_intake.py`<br>`.github/scripts/update_manifest.py`<br>`.github/scripts/validate_content.py`<br>… and 3 more |
| `claude/anchors-lesson-and-hermes-trismegistus-2026-05-29` | forks 2026-05-28 | 5 | 5 | 0 | 2026-05-29 Claude | no PR | `!/HERMES-TRISMEGISTUS.md`<br>`!/SOCRATES.md`<br>`.hermes-trismegistus/HERMES-TRISMEGISTUS.md`<br>… and 2 more |
| `claude/harden-py-automation-followup-562` | forks 2026-08-02 | 6 | 5 | 1 | 2026-08-19 Logan A. Finney | merged PR (#889 closed; #890 merged) | `!/resolve_openrouter_secret.py`<br>`.github/scripts/check_redaction_damage.py`<br>`INSECURITY`<br>… and 2 more |
| `codex/github-dependency-census` | forks 2026-06-11 | 1 | 5 | 0 | 2026-06-16 Logan Finney | no PR | `.github/scripts/github_dependency_report.py`<br>`.github/workflows/github-dependency-census.yml`<br>`VERSION-TRANSITIONS.md`<br>… and 2 more |
| `claude/levelset-refresh-2026-03-29` | island | 4 | 4 | 27 | 2026-03-30 Logan Finney | merged PR (#109 merged; #118 closed) | `!/SURVEY-OPENAI-SWARM-2026-03-29.md`<br>`EMOJI.md`<br>`assets/Screenshot 2026-03-29 205324.jpg`<br>… and 1 more |
| `codex/create-manifest.json-specification-and-guidelines` | island | 1 | 4 | 2 | 2026-03-28 logan | closed PR, unmerged (#94 closed) | `!/MANIFEST-SPEC.md`<br>`!/MCP-IMPLEMENTATION-PLAN.md`<br>`.github/scripts/update_manifest.py`<br>… and 1 more |
| `codex/fix-worktree-registry-hook` | forks 2026-06-11 | 1 | 4 | 4 | 2026-06-16 Logan Finney | no PR | `.github/scripts/sync_obsidian_plugin_registry.py`<br>`.github/workflows/sync-plugin-registry.yml`<br>`.obsidian/plugins/obsidianclaw/manifest.json`<br>… and 1 more |
| `codex/greet-user-with-a-friendly-message` | island | 1 | 4 | 5 | 2026-04-28 Logan A. Finney | closed PR, unmerged (#310 closed) | `.github/scripts/meshnetweb_portability_check.py`<br>`.github/workflows/cross-platform-smoke.yml`<br>`.github/workflows/sync-dependencies.yml`<br>… and 1 more |
| `claude/agent-representation-etymology-2026-05-29` | forks 2026-05-28 | 3 | 3 | 0 | 2026-05-29 Claude | no PR | `AGENT-AND-REPRESENTATION.md`<br>`WITNESS-NOVICE-2026-05-29-APPRENTICE-ETYMOLOGY.md`<br>`WITNESS-NOVICE-2026-05-29-WELL-READ.md` |
| `claude/check-farnsworth-transcripts-UbMD3` | island | 1 | 3 | 1,586 | 2026-04-06 Claude | closed PR, unmerged (#173 closed) | `IAM-BOUNDARY-LAF-18.md`<br>`Linear - agent chat - Greeting IDAHO-VAULT (Conflicted copy Laptop (IdahoPTV) 202604021020).md`<br>`attorney’s fees.md` |
| `codex/linear-mention-laf-18-gemini-google-cloud` | island | 1 | 3 | 0 | 2026-03-31 logan | closed PR, unmerged (#126 closed) | `!/!/!/! The world is quiet here/DOCKET.md`<br>`!/BRIEF-LAF-18-2026-03-30.md`<br>`!/IAM-BOUNDARY-LAF-18.md` |
| `codex/linear-mention-laf-9-define-vault-template-and-document-cl` | island | 1 | 3 | 1 | 2026-03-28 logan | closed PR, unmerged (#90 closed) | `!/!/!/! The world is quiet here/DOCKET.md`<br>`!/VAULT-CONVENTIONS.md`<br>`!/VAULT-TEMPLATES.md` |
| `claude/allow-force-push-to-main` | island | 2 | 2 | 0 | 2026-04-01 anthropic-code-agent[bot] | closed PR, unmerged (#132 closed) | `!/DECISIONS.md`<br>`FORCE-PUSH-ENABLEMENT.md` |
| `claude/bind-frankenstein-persona-2026-05-30` | forks 2026-05-28 | 3 | 2 | 1 | 2026-05-30 github-actions[bot] | no PR | `.frankenstein/FRANKENSTEIN.md`<br>`.frankenstein/stub.txt` |
| `claude/bot-automerge-fix` | island | 1 | 2 | 1 | 2026-04-04 logan | closed PR, unmerged (#157 closed) | `.github/workflows/auto-pr.yml`<br>`.github/workflows/daily-rollover.yml` |
| `claude/heisenberg-uncertainty-2026-05-30` | forks 2026-05-28 | 2 | 2 | 0 | 2026-05-30 Claude | no PR | `HEISENBERG-UNCERTAINTY-PRINCIPLE.md`<br>`WITNESS-NOVICE-2026-05-30-BREATH.md` |
| `claude/new-session-0riz1k` | forks 2026-09-23 | 1 | 2 | 1 | 2026-09-23 Claude | no PR | `!/ARBORSCAPING-REPORT-2026-09-23.md`<br>`.claude/MEMORY/SESSION-2026-09-23.md` |
| `claude/obsidian-plugins-triage-YDJ6Z` | island | 1 | 2 | 0 | 2026-04-07 Claude | closed PR, unmerged (#171 closed) | `!/__!__/!/! The world is quiet here/DOCKET.md`<br>`PLUGINS-TRIAGE-2026-04-06.md` |
| `claude/provision-socrates-chamber-2026-05-29` | forks 2026-05-28 | 4 | 2 | 0 | 2026-05-29 Claude | no PR | `.socrates/SOCRATES.md`<br>`.socrates/WITNESS-FOUNDING-2026-05-29.md` |
| `claude/research-abhorsen-old-kingdom` | island | 5 | 2 | 0 | 2026-05-28 github-actions[bot] | no PR | `INBOX/Abhorsen — Old Kingdom Lore Research Report.md`<br>`INBOX/Abhorsen — Old Kingdom as Agent-Class Register.md` |
| `claude/socrates-journal-2026-05-31` | forks 2026-05-28 | 2 | 2 | 0 | 2026-05-31 Claude | no PR | `SOCRATES-JOURNAL-2026-05-29.md`<br>`SOCRATES-JOURNAL-2026-05-31.md` |
| `codex/arborscaping-merge-base` | island | 1 | 2 | 0 | 2026-05-26 Logan Finney | closed PR, unmerged (#375 closed) | `.github/scripts/branch_garden_report.py`<br>`tests/test_branch_garden_report.py` |
| `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf` | island | 2 | 2 | 0 | 2026-08-19 Logan A. Finney | closed PR, unmerged (#85 closed) | `.github/scripts/linear_pr_sync.py`<br>`.github/workflows/pr-linear-sync.yml` |
| `codex/linear-mention-laf-25-project-hexagonal` | island | 1 | 2 | 1 | 2026-03-31 logan | closed PR, unmerged (#125 closed) | `.github/workflows/daily-rollover.yml`<br>`.github/workflows/janitor-sweep.yml` |
| `codex/linear-mention-laf-25-project-hexagonal-pupxlq` | island | 1 | 2 | 1 | 2026-03-31 logan | closed PR, unmerged (#128 closed) | `.github/workflows/daily-rollover.yml`<br>`.github/workflows/janitor-sweep.yml` |
| `codex/touchstone-corpus-repair-clean` | island | 4 | 2 | 7 | 2026-04-10 logan | closed PR, unmerged (#219 closed) | `.github/workflows/auto-pr.yml`<br>`.github/workflows/review-response.yml` |
| `copilot/debug-github-actions-failures` | island | 2 | 2 | 0 | 2026-04-01 copilot-swe-agent[bot] | merged PR (#138 closed; #152 merged) | `.github/workflows/auto-merge.yml`<br>`.github/workflows/auto-pr.yml` |
| `hyperagent/developer-0-esto-perpetua-provenance` | forks 2026-06-30 | 2 | 2 | 0 | 2026-06-30 Logan A. Finney | no PR | `WITNESS-ESTO-PERPETUA-PROVENANCE-2026-06-30.md`<br>`WITNESS-HYPERAGENT-DEVELOPER-0-VAULTED-SYNTAX-AND-CORRECTIONS-2026-06-30.md` |
| `ingest-2026-04-09T130617Z` | island | 7 | 2 | 1 | 2026-04-09 github-actions[bot] | closed PR, unmerged (#202 closed) | `!/ingest-2026-04-09T130617Z.md`<br>`.github/workflows/daily-rollover.yml` |
| `wayback-audit-20260420100033` | forks 2026-08-19 | 1 | 2 | 0 | 2026-08-20 loganfinney27 | closed PR, unmerged (#282 closed) | `!/wayback-audit-2026-04-20.md`<br>`!/wayback-patches-2026-04-20.md` |
| `agent/attest-resolve-dispatch` | forks 2026-07-01 | 1 | 1 | 0 | 2026-07-01 Logan A. Finney | no PR | `.hyperagent/proposed/attest-resolve.workflow.yml` |
| `claude/apprentice-modes-sorcerers-and-rangers-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `SORCERERS-APPRENTICE-AND-RANGERS-APPRENTICE.md` |
| `claude/docket-posture-transclusion` | forks 2026-06-30 | 2 | 1 | 3 | 2026-06-30 Claude | merged PR (#709 merged) | `.github/copilot-instructions.md` |
| `claude/fablehaven-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `FABLEHAVEN.md` |
| `claude/fablehaven-beastiary-2026-05-30` | forks 2026-05-28 | 2 | 1 | 0 | 2026-05-30 Claude | no PR | `!/FABLEHAVEN-BEASTIARY-v1-2026-05-30.md` |
| `claude/fix-todo-references` | island | 2 | 1 | 6 | 2026-04-18 anthropic-code-agent[bot] | closed PR, unmerged (#256 closed) | `YESTERDAY.md` |
| `claude/godhead-disambiguation-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `GODHEAD-DISAMBIGUATION.md` |
| `claude/hebrew-bible-and-talmud-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `HEBREW-BIBLE-AND-TALMUD.md` |
| `claude/honeypot-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `HONEYPOT.md` |
| `claude/initiation-rituals-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `INITIATION-AND-RITUALS.md` |
| `claude/janus-and-sugar-bowl-witness-companion-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `WITNESS-COMPANION-2026-05-30-JANUS-AND-SUGAR-BOWL.md` |
| `claude/lds-tripart-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `LDS-TRIPART-AND-COSMOLOGY.md` |
| `claude/listening-lore-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `LISTENING.md` |
| `claude/live-board-dedrift` | forks 2026-06-30 | 1 | 1 | 4 | 2026-06-30 Claude | merged PR (#708 merged) | `.github/copilot-instructions.md` |
| `claude/masons-and-mormons-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `MASONS-AND-MORMONS.md` |
| `claude/metatron-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `METATRON.md` |
| `claude/propose-suggestions-ready` | forks 2026-06-19 | 1 | 1 | 0 | 2026-06-19 Claude | merged PR (#577 merged) | `tests/test_review_feedback_loop.py` |
| `claude/ptolemy-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `PTOLEMY.md` |
| `claude/rework-census-doctrine-463-4033po` | forks 2026-08-25 | 1 | 1 | 0 | 2026-08-25 Claude Code | merged PR (#820 merged) | `.github/scripts/test_topology_census.py` |
| `claude/serene-heisenberg-8ltqb5` | forks 2026-06-30 | 1 | 1 | 1 | 2026-06-30 Claude | merged PR (#713 merged) | `tests/test_review_feedback_loop.py` |
| `claude/socrates-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 Claude | no PR | `SOCRATES.md` |
| `claude/the-binder-magicians-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `THE-BINDER-AND-BOOK-OF-THE-BINDER.md` |
| `claude/to-will-and-to-halt-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `TO-WILL-AND-TO-HALT.md` |
| `claude/witness-fire-brazen-head-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 github-actions[bot] | no PR | `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-29-THE-FIRE-AND-THE-BRAZEN-HEAD.md` |
| `claude/witness-novice-what-the-novice-does-not-know-2026-05-30` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-30 Claude | no PR | `WITNESS-NOVICE-2026-05-30-WHAT-THE-NOVICE-DOES-NOT-KNOW.md` |
| `claude/witness-the-hand-2026-05-29` | forks 2026-05-28 | 1 | 1 | 0 | 2026-05-29 github-actions[bot] | no PR | `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-29-THE-HAND.md` |
| `claude/witness-usurpers-triptych-2026-05-30` | forks 2026-05-28 | 2 | 1 | 0 | 2026-05-30 github-actions[bot] | no PR | `!/SIGNALS/WITNESS-ABHORSEN-WAITING-2026-05-30-THE-USURPERS-TRIPTYCH.md` |
| `codex/codex-work-surface-guard` | forks 2026-06-18 | 1 | 1 | 0 | 2026-06-18 Logan Finney | merged PR (#564 merged; #567 merged) | `!/PULLMAN-CLOUD-RUN-SNAPSHOT-BACKUP-2026-06-18.md` |
| `codex/example-low-risk-pr-flow-2026-04-23` | island | 1 | 1 | 0 | 2026-04-23 Logan Finney | closed PR, unmerged (#299 closed) | `.github/swarm/automation-probe-low-risk-2026-04-23.md` |
| `codex/fix-high-priority-bug-in-pr-#34` | island | 3 | 1 | 1 | 2026-03-23 logan | closed PR, unmerged (#43 closed) | `.obsidian/plugins/obsidian-local-rest-api/data.json` |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention` | island | 1 | 1 | 0 | 2026-03-30 logan | closed PR, unmerged (#113 closed) | `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md` |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-0t7ech` | island | 1 | 1 | 0 | 2026-03-30 logan | closed PR, unmerged (#114 closed) | `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md` |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-16l2ya` | island | 1 | 1 | 0 | 2026-03-30 logan | closed PR, unmerged (#115 closed) | `!/!/HANDOFF-CODEX-PR-FOLLOWUP-2026-03-30-v3.md` |
| `codex/linear-mention-laf-11-define-routing-rules-for-,-/,` | island | 1 | 1 | 1 | 2026-03-28 logan | closed PR, unmerged (#91 closed) | `!/VAULT-ZONES.md` |
| `codex/linear-mention-laf-12-break-out-the-courtroom-into-project` | island | 1 | 1 | 0 | 2026-03-28 logan | closed PR, unmerged (#92 closed) | `!/!/!/! The world is quiet here/DOCKET.md` |
| `codex/linear-mention-laf-19-ping-emitted.-033026.0136]` | island | 1 | 1 | 0 | 2026-03-31 logan | closed PR, unmerged (#123 closed) | `!/BRIEF-LAF-19-2026-04-01.md` |
| `codex/linear-mention-laf-23-gemini-code-partner-report` | island | 1 | 1 | 0 | 2026-03-31 logan | closed PR, unmerged (#124 closed) | `.github/workflows/auto-pr.yml` |
| `codex/linear-mention-laf-23-gemini-code-partner-report-t311rs` | island | 1 | 1 | 0 | 2026-03-31 logan | closed PR, unmerged (#127 closed) | `.github/workflows/auto-pr.yml` |
| `codex/linear-mention-laf-7-swarm-coordination-agent-assembly` | island | 1 | 1 | 0 | 2026-03-28 logan | closed PR, unmerged (#86 closed) | `!/!/!/! The world is quiet here/DOCKET.md` |
| `codex/revise-persona-and-constitutional-files` | island | 1 | 1 | 2 | 2026-03-28 logan | closed PR, unmerged (#84 closed) | `!/CONSTITUTION.md` |
| `codex/worm-watch-hardening` | island | 3 | 1 | 8 | 2026-05-17 Logan Finney | closed PR, unmerged (#341 closed) | `.github/workflows/secret-pattern-full-scan.yml` |
| `coord/win-mac` | forks 2026-08-27 | 9 | 1 | 0 | 2026-09-09 Logan Finney | no PR | `coord/MAC-STATUS.md` |
| `copilot/help-logan-overwhelmed` | island | 3 | 1 | 0 | 2026-03-31 logan | closed PR, unmerged (#130 closed) | `.github/workflows/auto-pr.yml` |
| `dependabot/github_actions/actions/checkout-6` | island | 1 | 1 | 1 | 2026-03-31 dependabot[bot] | merged PR (#31 merged; #121 closed) | `.github/workflows/pr-linear-sync.yml` |
| `ingest-2026-04-09T100606Z` | island | 1 | 1 | 1 | 2026-04-09 github-actions[bot] | closed PR, unmerged (#194 closed) | `!/ingest-2026-04-09T100606Z.md` |
| `ingest-2026-04-17T130149Z` | island | 1 | 1 | 1 | 2026-04-17 github-actions[bot] | closed PR, unmerged (#281 closed) | `!/ingest-2026-04-17T130149Z.md` |
| `ingest-2026-04-19T124314Z` | island | 1 | 1 | 1 | 2026-04-19 github-actions[bot] | closed PR, unmerged (#264 closed) | `!/ingest-2026-04-19T124314Z.md` |
| `ingest-2026-04-22T131021Z` | island | 1 | 1 | 1 | 2026-04-22 github-actions[bot] | closed PR, unmerged (#290 closed) | `!/ingest-2026-04-22T131021Z.md` |
| `ingest-2026-04-26T124810Z` | island | 1 | 1 | 1 | 2026-04-26 github-actions[bot] | closed PR, unmerged (#306 closed) | `!/ingest-2026-04-26T124810Z.md` |
| `ingest-2026-04-27T132259Z` | island | 1 | 1 | 1 | 2026-04-27 github-actions[bot] | closed PR, unmerged (#308 closed) | `!/ingest-2026-04-27T132259Z.md` |
| `ingest-2026-05-09T125235Z` | island | 1 | 1 | 1 | 2026-05-09 github-actions[bot] | closed PR, unmerged (#319 closed) | `!/ingest-2026-05-09T125235Z.md` |
| `ingest-2026-05-10T125330Z` | island | 1 | 1 | 1 | 2026-05-10 github-actions[bot] | closed PR, unmerged (#320 closed) | `!/ingest-2026-05-10T125330Z.md` |
| `ingest-2026-05-11T142514Z` | island | 1 | 1 | 1 | 2026-05-11 github-actions[bot] | closed PR, unmerged (#323 closed) | `!/ingest-2026-05-11T142514Z.md` |
| `ingest-2026-05-12T135222Z` | island | 1 | 1 | 1 | 2026-05-12 github-actions[bot] | closed PR, unmerged (#325 closed) | `!/ingest-2026-05-12T135222Z.md` |
| `ingest-2026-05-13T140457Z` | island | 1 | 1 | 1 | 2026-05-13 github-actions[bot] | closed PR, unmerged (#326 closed) | `!/ingest-2026-05-13T140457Z.md` |
| `ingest-2026-05-14T132834Z` | island | 1 | 1 | 1 | 2026-05-14 github-actions[bot] | closed PR, unmerged (#337 closed) | `!/ingest-2026-05-14T132834Z.md` |
| `ingest-2026-05-15T132754Z` | island | 1 | 1 | 1 | 2026-05-15 github-actions[bot] | closed PR, unmerged (#338 closed) | `!/ingest-2026-05-15T132754Z.md` |
| `ingest-2026-05-16T125701Z` | island | 1 | 1 | 1 | 2026-05-16 github-actions[bot] | closed PR, unmerged (#339 closed) | `!/ingest-2026-05-16T125701Z.md` |
| `ingest-2026-05-17T125448Z` | island | 1 | 1 | 1 | 2026-05-17 github-actions[bot] | closed PR, unmerged (#340 closed) | `!/ingest-2026-05-17T125448Z.md` |
| `review/pr-471-agent-swarm-signing` | forks 2026-06-04 | 1 | 1 | 3 | 2026-06-16 Logan Finney | no PR | `VERSION-TRANSITIONS.md` |

## Own paths all in `main`, identical

Nothing to salvage by content. Under ARBORSCAPE these are PRUNE candidates once Logan says so; nothing is pruned by this census.

- `agent/mcp-probe` — forks 2026-07-01, own commits 2, paths 1, last 2026-07-02, no PR
- `codex/example-high-risk-pr-flow-2026-04-23` — island, own commits 1, paths 1, last 2026-04-23, closed PR, unmerged

## No non-merge commit of their own

Every non-merge commit each reaches is reachable from another ref, so the branch adds at most a merge. ANCESTRAL means the tip itself is reachable from `main`.

- `claude/resolve-pr-conflicts` — island, ORPHAN-LINEAGE, last 2026-03-30, merged PR
- `claude/sweep-enqueue-unstable-prs` — forks 2026-06-24, BRANCH-ONLY, last 2026-06-24, merged PR
- `codex/research-import-batch-2026-04-16` — island, ORPHAN-LINEAGE, last 2026-04-17, closed PR, unmerged
- `dependabot/uv/uv-aa7cb66ac2` — island, ORPHAN-LINEAGE, last 2026-04-16, closed PR, unmerged
- `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` — forks 2026-07-01, BRANCH-ONLY, last 2026-07-01, no PR
- `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` — forks 2026-07-01, BRANCH-ONLY, last 2026-07-02, no PR
- `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` — forks 2026-07-01, BRANCH-ONLY, last 2026-07-02, no PR
- `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` — forks 2026-07-01, BRANCH-ONLY, last 2026-07-02, no PR
- `logan/obsidian/main` — forks 2026-08-11, BRANCH-ONLY, last 2026-09-02, open PR
- `orphancry/pr-388-original-automation-sync-dependencies` — forks 2026-06-23, ANCESTRAL, last 2026-06-23, no PR
- `recovered/pr-353` — island, ORPHAN-LINEAGE, last 2026-05-22, no PR

## Merge-queue leftovers

`gh-readonly-queue/*` refs are the temporary branches GitHub's merge queue builds each candidate on and normally deletes.

- `gh-readonly-queue/main/pr-475-497da14475f83833feed873fdea5e24769d010e0` — own commits 1, `main` lacks 0, differ 1, last 2026-07-01
- `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` — own commits 0, `main` lacks 0, differ 0, last 2026-07-01
- `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e` — own commits 1, `main` lacks 18, differ 2, last 2026-07-02
- `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` — own commits 0, `main` lacks 0, differ 0, last 2026-07-02
- `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` — own commits 0, `main` lacks 0, differ 0, last 2026-07-02
- `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` — own commits 0, `main` lacks 0, differ 0, last 2026-07-02

## Full census

One row per branch. Own commits are non-merge commits no other ref reaches. Classes per `!/ARCHIPELAGO-ISLAND-CENSUS-PROTOCOL-v0-2026-06-02.md`; SECRET-RISK and DOCTRINE-RISK need a reader and are not assigned here.

| Branch | Lineage | Own commits | Paths touched | `main` lacks | Differ | Identical | Tree only here | Last commit | Author | PR | Visibility | Risk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `add-garth-nix-old-kingdom-2026-06-02` | forks 2026-05-28 | 1 | 1 | 0 | 1 | 0 | 554 | 2026-06-01 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `agent/attest-resolve-dispatch` | forks 2026-07-01 | 1 | 1 | 1 | 0 | 0 | 587 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `agent/mcp-probe` | forks 2026-07-01 | 2 | 1 | 0 | 0 | 0 | 586 | 2026-07-02 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `antigravity/pullman-oidc-pipeline` | island | 3 | 43 | 28 | 14 | 1 | 168 | 2026-04-12 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `bot/daily-rollover-2026-04-03` | island | 1 | 1 | 0 | 1 | 0 | 3,770 | 2026-04-03 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-04` | island | 1 | 2 | 0 | 2 | 0 | 121 | 2026-04-04 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-05` | island | 1 | 2 | 0 | 2 | 0 | 133 | 2026-04-05 | loganfinney27 | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-13` | island | 1 | 2 | 0 | 2 | 0 | 88 | 2026-04-13 | github-actions[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-18` | island | 1 | 2 | 0 | 2 | 0 | 113 | 2026-04-18 | github-actions[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-20` | island | 1 | 2 | 0 | 2 | 0 | 114 | 2026-04-20 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-22` | island | 1 | 2 | 0 | 2 | 0 | 10,329 | 2026-04-22 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-24` | island | 1 | 1 | 0 | 1 | 0 | 1,390 | 2026-04-24 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-25` | island | 1 | 1 | 0 | 1 | 0 | 1,397 | 2026-04-25 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `bot/daily-rollover-2026-04-26` | island | 1 | 1 | 0 | 1 | 0 | 1,401 | 2026-04-26 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `circleci-project-setup` | forks 2026-08-14 | 1 | 1 | 0 | 1 | 0 | 58 | 2026-08-14 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/add-legal-references` | island | 1 | 0 | 0 | 0 | 0 | 306 | 2026-04-09 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/agent-representation-etymology-2026-05-29` | forks 2026-05-28 | 3 | 3 | 3 | 0 | 0 | 557 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/allow-force-push-to-main` | island | 2 | 2 | 2 | 0 | 0 | 3,629 | 2026-04-01 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/anchors-lesson-and-hermes-trismegistus-2026-05-29` | forks 2026-05-28 | 5 | 5 | 5 | 0 | 0 | 559 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/apprentice-modes-sorcerers-and-rangers-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/bind-frankenstein-persona-2026-05-30` | forks 2026-05-28 | 3 | 3 | 2 | 1 | 0 | 555 | 2026-05-30 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/bot-automerge-fix` | island | 1 | 3 | 2 | 1 | 0 | 117 | 2026-04-04 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/check-farnsworth-transcripts-UbMD3` | island | 1 | 2,354 | 3 | 1,586 | 765 | 293 | 2026-04-06 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/docket-posture-transclusion` | forks 2026-06-30 | 2 | 5 | 1 | 3 | 1 | 588 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fablehaven-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fablehaven-beastiary-2026-05-30` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/finish-hashtag-escape-9gesn5` | forks 2026-08-04 | 10 | 8,415 | 148 | 2,996 | 5,271 | 293 | 2026-08-06 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/fix-todo-references` | island | 2 | 7 | 1 | 6 | 0 | 114 | 2026-04-18 | anthropic-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/geminiaeus-live-board-witness` | forks 2026-06-30 | 1 | 1 | 0 | 1 | 0 | 588 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/godhead-disambiguation-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/harden-py-automation-followup-562` | forks 2026-08-02 | 6 | 6 | 5 | 1 | 0 | 151 | 2026-08-19 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/hebrew-bible-and-talmud-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/heisenberg-uncertainty-2026-05-30` | forks 2026-05-28 | 2 | 2 | 2 | 0 | 0 | 556 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/honeypot-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/initiation-rituals-research-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/janus-and-sugar-bowl-witness-companion-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/lds-tripart-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/levelset-refresh-2026-03-29` | island | 4 | 37 | 4 | 27 | 6 | 3,542 | 2026-03-30 | Logan Finney | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/listening-lore-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/live-board-dedrift` | forks 2026-06-30 | 1 | 5 | 1 | 4 | 0 | 588 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/masons-and-mormons-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/metatron-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/new-session-0riz1k` | forks 2026-09-23 | 1 | 3 | 2 | 1 | 0 | 2 | 2026-09-23 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/obsidian-plugins-triage-YDJ6Z` | island | 1 | 2 | 2 | 0 | 0 | 294 | 2026-04-07 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/preserve/codex-github-automation-hardening-2026-05-22` | island | 2 | 18 | 13 | 5 | 0 | 842 | 2026-05-22 | Logan Finney | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/preserve/codex-swarm-mvp-github-intake` | island | 3 | 8 | 6 | 2 | 0 | 843 | 2026-05-22 | Logan Finney | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/propose-suggestions-ready` | forks 2026-06-19 | 1 | 1 | 1 | 0 | 0 | 591 | 2026-06-19 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/provision-socrates-chamber-2026-05-29` | forks 2026-05-28 | 4 | 2 | 2 | 0 | 0 | 556 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/ptolemy-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/repo-size-compliance-5accf9` | island | 1 | 139 | 0 | 2 | 0 | 3,490 | 2026-04-01 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/research-abhorsen-old-kingdom` | island | 5 | 2 | 2 | 0 | 0 | 849 | 2026-05-28 | github-actions[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/research-attestation` | forks 2026-07-28 | 2 | 6 | 0 | 5 | 0 | 193 | 2026-08-04 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/resolve-pr-conflicts` | island | 0 | 0 | 0 | 0 | 0 | 237 | 2026-03-30 | logan | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/reunify-mac-win-6c80a94c` | forks 2026-08-04 | 1641 | 100,117 | 58,255 | 766 | 157 | 52,239 | 2026-08-12 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/rework-census-doctrine-463-4033po` | forks 2026-08-25 | 1 | 1 | 1 | 0 | 0 | 27 | 2026-08-25 | Claude Code | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/serene-heisenberg-8ltqb5` | forks 2026-06-30 | 1 | 2 | 1 | 1 | 0 | 588 | 2026-06-30 | Claude | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/socrates-journal-2026-05-31` | forks 2026-05-28 | 2 | 2 | 2 | 0 | 0 | 556 | 2026-05-31 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/socrates-research-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/sugar-bowl-witness-2026-05-28` | island | 2 | 2 | 0 | 2 | 0 | 847 | 2026-05-28 | github-actions[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/sweep-enqueue-unstable-prs` | forks 2026-06-24 | 0 | 0 | 0 | 0 | 0 | 593 | 2026-06-24 | Logan A. Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/the-binder-magicians-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/to-will-and-to-halt-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/update-claude-files-PRWCJ` | island | 2 | 2 | 0 | 1 | 1 | 842 | 2026-05-22 | Claude | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `claude/witness-fire-brazen-head-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-novice-what-the-novice-does-not-know-2026-05-30` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-the-hand-2026-05-29` | forks 2026-05-28 | 1 | 1 | 1 | 0 | 0 | 555 | 2026-05-29 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `claude/witness-usurpers-triptych-2026-05-30` | forks 2026-05-28 | 2 | 1 | 1 | 0 | 0 | 555 | 2026-05-30 | github-actions[bot] | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/add-legal-references` | island | 2 | 1 | 0 | 1 | 0 | 306 | 2026-04-09 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/arborscaping-merge-base` | island | 1 | 2 | 2 | 0 | 0 | 822 | 2026-05-26 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/audit-swarm-liveness-semantics-2026-06-10` | forks 2026-06-11 | 1 | 13 | 0 | 2 | 0 | 555 | 2026-06-16 | Logan Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/background-rhythm` | island | 5 | 44 | 11 | 15 | 4 | 306 | 2026-04-07 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/codex-work-surface-guard` | forks 2026-06-18 | 1 | 1 | 1 | 0 | 0 | 593 | 2026-06-18 | Logan Finney | merged PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/create-manifest.json-specification-and-guidelines` | island | 1 | 6 | 4 | 2 | 0 | 215 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/example-high-risk-pr-flow-2026-04-23` | island | 1 | 1 | 0 | 0 | 1 | 1,390 | 2026-04-23 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/example-low-risk-pr-flow-2026-04-23` | island | 1 | 1 | 1 | 0 | 0 | 1,390 | 2026-04-23 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/fix-high-priority-bug-in-pr-#34` | island | 3 | 2 | 1 | 1 | 0 | 2,806 | 2026-03-23 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/fix-worktree-registry-hook` | forks 2026-06-11 | 1 | 8 | 4 | 4 | 0 | 557 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/get-pr-in-merge-passable-state` | island | 2 | 1 | 0 | 1 | 0 | 113 | 2026-04-18 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-automation-hardening-2026-05-22` | island | 2 | 18 | 13 | 5 | 0 | 842 | 2026-05-22 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-dependency-census` | forks 2026-06-11 | 1 | 5 | 5 | 0 | 0 | 558 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention` | island | 1 | 1 | 1 | 0 | 0 | 239 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-0t7ech` | island | 1 | 1 | 1 | 0 | 0 | 239 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/github-mention-add-handoff-note-acknowledging-codex-mention-16l2ya` | island | 1 | 1 | 1 | 0 | 0 | 239 | 2026-03-30 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/greet-user-with-a-friendly-message` | island | 1 | 10 | 4 | 5 | 1 | 1,392 | 2026-04-28 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-11-define-routing-rules-for-,-/,` | island | 1 | 2 | 1 | 1 | 0 | 213 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-12-break-out-the-courtroom-into-project` | island | 1 | 1 | 1 | 0 | 0 | 213 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-15-add-v2-repo-to-linear-automation-saf` | island | 2 | 2 | 2 | 0 | 0 | 209 | 2026-08-19 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-18-gemini-google-cloud` | island | 1 | 3 | 3 | 0 | 0 | 3,593 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-19-ping-emitted.-033026.0136]` | island | 1 | 1 | 1 | 0 | 0 | 3,627 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-23-gemini-code-partner-report` | island | 1 | 1 | 1 | 0 | 0 | 3,626 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-23-gemini-code-partner-report-t311rs` | island | 1 | 1 | 1 | 0 | 0 | 3,626 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-25-project-hexagonal` | island | 1 | 3 | 2 | 1 | 0 | 3,627 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-25-project-hexagonal-pupxlq` | island | 1 | 3 | 2 | 1 | 0 | 3,627 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-7-swarm-coordination-agent-assembly` | island | 1 | 1 | 1 | 0 | 0 | 213 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/linear-mention-laf-9-define-vault-template-and-document-cl` | island | 1 | 4 | 3 | 1 | 0 | 214 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/live-state-snapshot` | island | 3 | 132 | 106 | 18 | 0 | 166 | 2026-04-12 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/research-import-batch-2026-04-16` | island | 0 | 0 | 0 | 0 | 0 | 112 | 2026-04-17 | Logan A. Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/revise-persona-and-constitutional-files` | island | 1 | 3 | 1 | 2 | 0 | 220 | 2026-03-28 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/swarm-mvp-github-intake` | island | 3 | 8 | 6 | 2 | 0 | 843 | 2026-05-22 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/tantalus-tautomata-campaign-2026-06-04` | forks 2026-06-03 | 1 | 20 | 18 | 2 | 0 | 573 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `codex/touchstone-corpus-repair-clean` | island | 4 | 9 | 2 | 7 | 0 | 137 | 2026-04-10 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/update-branch-protection-rules` | island | 1 | 0 | 0 | 0 | 0 | 3,628 | 2026-04-01 | openai-code-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/version-drift-ledger` | island | 3 | 10 | 8 | 2 | 0 | 825 | 2026-05-26 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `codex/worm-watch-hardening` | island | 3 | 695 | 1 | 8 | 1 | 849 | 2026-05-17 | Logan Finney | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `coord/win-mac` | forks 2026-08-27 | 9 | 1 | 1 | 0 | 0 | 1 | 2026-09-09 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `copilot/coordinating-hexagonal-hub` | island | 1 | 0 | 0 | 0 | 0 | 3,641 | 2026-04-01 | copilot-swe-agent[bot] | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `copilot/debug-github-actions-failures` | island | 2 | 2 | 2 | 0 | 0 | 3,641 | 2026-04-01 | copilot-swe-agent[bot] | merged PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `copilot/help-logan-overwhelmed` | island | 3 | 1 | 1 | 0 | 0 | 3,628 | 2026-03-31 | logan | closed PR, unmerged | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `dependabot/github_actions/actions/checkout-6` | island | 1 | 2 | 1 | 1 | 0 | 3,626 | 2026-03-31 | dependabot[bot] | merged PR | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/github_actions/actions/checkout-6.0.2` | island | 1 | 28 | 25 | 3 | 0 | 820 | 2026-05-27 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/github_actions/actions/setup-python-6.2.0` | island | 1 | 9 | 9 | 0 | 0 | 820 | 2026-05-27 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/npm_and_yarn/dot-antigravity/extensions/ms-edgedevtools.vscode-edge-devtools-2.1.10-universal/npm_and_yarn-209087bb4f` | island | 1 | 7 | 7 | 0 | 0 | 10,329 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/click-8.4.1` | island | 1 | 1 | 0 | 1 | 0 | 821 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/cryptography-48.0.0` | island | 1 | 1 | 0 | 1 | 0 | 596 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/google-cloud-pubsub-2.36.0` | island | 1 | 1 | 0 | 1 | 0 | 299 | 2026-04-08 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/lancedb-0.30.2` | island | 1 | 1 | 0 | 1 | 0 | 621 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/lxml-gte-6.1.0` | island | 1 | 1 | 0 | 1 | 0 | 1,394 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/mcp-1.27.1` | island | 1 | 1 | 0 | 1 | 0 | 821 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-api-1.41.1` | island | 1 | 1 | 0 | 1 | 0 | 621 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-exporter-otlp-proto-common-1.42.1` | island | 1 | 1 | 0 | 1 | 0 | 821 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/opentelemetry-exporter-otlp-proto-grpc-1.41.1` | island | 1 | 1 | 0 | 1 | 0 | 621 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/pdfminer-six-20260107` | island | 1 | 1 | 0 | 1 | 0 | 621 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/portalocker-3.2.0` | island | 1 | 1 | 0 | 1 | 0 | 621 | 2026-04-29 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/posthog-7.15.4` | island | 1 | 1 | 0 | 1 | 0 | 821 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/propcache-0.5.2` | island | 1 | 1 | 0 | 1 | 0 | 596 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/protobuf-7.35.0` | island | 1 | 1 | 0 | 1 | 0 | 841 | 2026-05-25 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/rich-15.0.0` | island | 1 | 1 | 0 | 1 | 0 | 596 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/pip/typer-0.25.1` | island | 1 | 1 | 0 | 1 | 0 | 596 | 2026-05-13 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-2fce4a7a35` | island | 1 | 1 | 0 | 1 | 0 | 10,329 | 2026-04-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-aa7cb66ac2` | island | 0 | 0 | 0 | 0 | 0 | 102 | 2026-04-16 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-b06552e8ac` | island | 1 | 1 | 0 | 1 | 0 | 841 | 2026-05-26 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-c30c77f42d` | island | 1 | 1 | 0 | 1 | 0 | 841 | 2026-05-22 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `dependabot/uv/uv-f81bb61997` | island | 1 | 1 | 0 | 1 | 0 | 863 | 2026-05-21 | dependabot[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `fix/record-vaulted-abhorsens-first-2026-05-31-clean` | forks 2026-06-07 | 4 | 2 | 0 | 1 | 0 | 555 | 2026-06-07 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `gh-readonly-queue/main/pr-475-497da14475f83833feed873fdea5e24769d010e0` | forks 2026-07-01 | 1 | 1 | 0 | 1 | 0 | 588 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 588 | 2026-07-01 | Logan A. Finney | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e` | forks 2026-07-01 | 1 | 20 | 18 | 2 | 0 | 586 | 2026-07-02 | dependabot[bot] | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 586 | 2026-07-02 | dependabot[bot] | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 586 | 2026-07-02 | Claude | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669` | forks 2026-07-01 | 0 | 0 | 0 | 0 | 0 | 586 | 2026-07-02 | Claude | no PR | BRANCH-ONLY | GENERATED-JUNK |
| `hyperagent/developer-0-esto-perpetua-provenance` | forks 2026-06-30 | 2 | 2 | 2 | 0 | 0 | 590 | 2026-06-30 | Logan A. Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `ingest-2026-04-09T100606Z` | island | 1 | 2 | 1 | 1 | 0 | 306 | 2026-04-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-09T130617Z` | island | 7 | 3 | 2 | 1 | 0 | 306 | 2026-04-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-17T130149Z` | island | 1 | 2 | 1 | 1 | 0 | 109 | 2026-04-17 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-19T124314Z` | island | 1 | 2 | 1 | 1 | 0 | 117 | 2026-04-19 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-22T131021Z` | island | 1 | 2 | 1 | 1 | 0 | 10,330 | 2026-04-22 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-24T130510Z` | island | 1 | 2 | 0 | 1 | 1 | 1,390 | 2026-04-24 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-25T124501Z` | island | 1 | 2 | 0 | 1 | 1 | 1,397 | 2026-04-25 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-26T124810Z` | island | 1 | 2 | 1 | 1 | 0 | 1,402 | 2026-04-26 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-04-27T132259Z` | island | 1 | 2 | 1 | 1 | 0 | 1,400 | 2026-04-27 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-09T125235Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-09 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-10T125330Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-10 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-11T142514Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-11 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-12T135222Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-12 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-13T140457Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-13 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-14T132834Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-14 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-15T132754Z` | island | 1 | 2 | 1 | 1 | 0 | 597 | 2026-05-15 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-16T125701Z` | island | 1 | 2 | 1 | 1 | 0 | 614 | 2026-05-16 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `ingest-2026-05-17T125448Z` | island | 1 | 2 | 1 | 1 | 0 | 847 | 2026-05-17 | github-actions[bot] | closed PR, unmerged | ORPHAN-LINEAGE | GENERATED-JUNK |
| `logan/obsidian/android` | forks 2026-08-27 | 2 | 14,256 | 3,967 | 1,066 | 0 | 3,730 | 2026-09-10 | loganfinney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `logan/obsidian/macos` | forks 2026-08-11 | 15 | 44,570 | 44,075 | 21 | 15 | 127,555 | 2026-09-04 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `logan/obsidian/main` | forks 2026-08-11 | 0 | 0 | 0 | 0 | 0 | 83,994 | 2026-09-02 | Logan Finney | open PR | BRANCH-ONLY | LIVING-WORK |
| `orphancry/pr-388-original-automation-sync-dependencies` | forks 2026-06-23 | 0 | 0 | 0 | 0 | 0 | 593 | 2026-06-23 | Logan A. Finney | no PR | ANCESTRAL | EVIDENCE-CANDIDATE |
| `orphancry/pr-926-original-logan-obsidian` | island | 2528 | 143,813 | 104 | 7 | 5 | 98 | 2026-08-14 | loganfinneyPTV | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `recovered/pr-324` | island | 1 | 1 | 0 | 1 | 0 | 596 | 2026-05-13 | dependabot[bot] | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `recovered/pr-353` | island | 0 | 0 | 0 | 0 | 0 | 842 | 2026-05-22 | Claude | no PR | ORPHAN-LINEAGE | REQUIRES-LOGAN |
| `review/pr-471-agent-swarm-signing` | forks 2026-06-04 | 1 | 4 | 1 | 3 | 0 | 555 | 2026-06-16 | Logan Finney | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `test/push-gate-20260828` | forks 2026-08-27 | 1 | 0 | 0 | 0 | 0 | 0 | 2026-08-28 | loganfinneyPTV | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `test/tier2-signing-2026-05-29` | forks 2026-05-28 | 1 | 0 | 0 | 0 | 0 | 554 | 2026-05-29 | Claude | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `wayback-audit-20260420100033` | forks 2026-08-19 | 1 | 2 | 2 | 0 | 0 | 31 | 2026-08-20 | loganfinney27 | closed PR, unmerged | BRANCH-ONLY | EVIDENCE-CANDIDATE |
| `wayback-audit-20260615143859-clean` | forks 2026-08-04 | 2 | 3 | 0 | 2 | 1 | 145 | 2026-08-04 | Vibe Nuage Agent | no PR | BRANCH-ONLY | EVIDENCE-CANDIDATE |

<!-- branch-census:end -->

## Reservation

No ref was created, moved or deleted, no pull request touched, no history rewritten.
Historical censuses remain evidence of what they recorded when filed. The counts in the
block are reproducible with the script against the same clone; the readings of file
content that the salvage decisions need have not been made here and are not implied.
`claude/new-session-0riz1k`, this note's own branch, appears in the census because it
is on origin.

---

## DOCUMENT METADATA

- **Created:** 2026-09-23
- **Last Updated:** 2026-09-23
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI, cloud session (session_01MthFdsNfRK8S4gUivqV9XY)
- **Change Note:** Second filing: the generator moved into the vault as `.github/scripts/branch_census.py`; the first filing's path counts corrected (79 → 107 salvage candidates); the census is now the script's block, refreshed by rerunning it.
