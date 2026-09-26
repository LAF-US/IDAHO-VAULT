# Plan: the 177 branches on GitHub first, then #1029's line

## Context

Logan: "177 first." Before anything on #1029, deal with every branch on GitHub. Read on 2026-09-25 with `git ls-remote` against main at a0143c75b (#1052's merge):

| Group | Count | What it is |
|---|---|---|
| main | 1 | |
| A. In main, no closed PR at the tip | 65 | Every commit already in main. Mostly finished `claude/*` and `codex/*` work, 6 leftover merge-queue branches. |
| B. In main, tip is a PR GitHub shows "closed", not "merged" | 96 | Content landed in main through #1045 and #1052. The PRs still read closed. |
| C. Not in main | 15 | #1029's line (5), the April 22 dump branches (4), open Dependabot PRs #1046–#1051 (6). |

This session's own branch is already gone; GitHub deleted it when #1052 merged.

The merge commit f09b1e73e for #1029 was built on a false picture (it ignores `logan/obsidian/macos` and `android`). It will not be pushed.

## Steps

1. **Group A: delete the 65 branches from GitHub.** Nothing is lost: re-check at run time that each tip is still an ancestor of main, and skip any that isn't. Each branch's commit is listed below, so any one can be put back with one push. The auto-mode classifier may refuse deletions; if it does, I stop and say so.
2. **Group B: test one repair before touching the rest.** Reopen #104 (`claude/resolve-pr-conflicts`, its commits all in main) and see whether GitHub records it as merged. Report what happened. The other 95 stay as they are until Logan decides: deleting their branches would block reopening, and reopening 95 PRs is noise he should choose.
3. **Group C:**
   - Dependabot #1046–#1051 through the merge queue in PR-number order, as with #1037–#1043. Fix only what a check or reviewer shows is wrong.
   - The four April 22 dump branches: untouched, Logan's call.
   - `logan/obsidian/android`: left for now, per Logan.
   - `logan/obsidian/main` (#1029), `macos`, `claude/reunify-mac-win-6c80a94c`, `orphancry/pr-926-original-logan-obsidian`: nothing until 1–3 are done; then back to Logan with the true state of that line.

Also noted, untouched: closed PRs #282, #287–#290, #889, #926, #980, #1023 and #1040 have no branch at their tip anymore.

## Status (2026-09-25, end of session)

- Step 1: not done. Logan allowed the deletions, but GitHub answered 403 to this session for the batch and for a single branch, before and after a reconnect. No workaround was tried. The deletion script went to Logan; the 65 branches are still on GitHub.
- Step 2: done. GitHub refused to reopen #104 ("state cannot be changed. These commits are already merged."). The 96 closed PRs cannot be reopened; their branches block nothing.
- Step 3, Dependabot: #1046–#1051 all merged. #1049 and #1051 each needed one signed `uv.lock` re-lock commit (b8d1dbbf1, eeec5a71d).
- #1029's line: another Claude session is working it (Logan). Not touched here. The merge commit f09b1e73e was never pushed.

## Not doing

- No `.claude/MEMORY/` writes. No force-push, no PR closes, no squash. No deletion of anything in groups B or C.

## Verification

- After step 1 (expected, not reached; step 1 did not run, see Status): `git ls-remote --heads origin` would show 106 branches (171 − 65), none of the 65 names.
- After step 2: #104's page shows merged or closed; reported either way.
- Dependabot PRs: each shows merged by the queue.

## Group A — the 65 (commit, branch)

```text
3996a3cc6f39 add-garth-nix-old-kingdom-2026-06-02
78854efd4edc agent/attest-resolve-dispatch
66048f470fc4 agent/mcp-probe
24ac1331d8d4 circleci-project-setup
5e930ca7ca93 claude/agent-representation-etymology-2026-05-29
4e632f2cdfc9 claude/anchors-lesson-and-hermes-trismegistus-2026-05-29
6420f85f986d claude/apprentice-modes-sorcerers-and-rangers-2026-05-30
0da389304f12 claude/bind-frankenstein-persona-2026-05-30
b44fe81af393 claude/docket-posture-transclusion
4994487671f7 claude/fablehaven-2026-05-30
2f0d9439702c claude/fablehaven-beastiary-2026-05-30
643227493497 claude/finish-hashtag-escape-9gesn5
2bc292698825 claude/geminiaeus-live-board-witness
71c7610f2e44 claude/godhead-disambiguation-2026-05-29
f1ecf7d1563d claude/harden-py-automation-followup-562
f61010298acf claude/hebrew-bible-and-talmud-research-2026-05-29
7911ebd40e17 claude/heisenberg-uncertainty-2026-05-30
ff953f5d0d61 claude/honeypot-research-2026-05-30
f6164a15028a claude/initiation-rituals-research-2026-05-30
8962a380a043 claude/janus-and-sugar-bowl-witness-companion-2026-05-30
889d17fff570 claude/lds-tripart-research-2026-05-29
31508728d269 claude/listening-lore-2026-05-30
ccfeaab2f3f7 claude/live-board-dedrift
cbfaaafacc36 claude/masons-and-mormons-2026-05-30
5362c68b1016 claude/metatron-research-2026-05-29
2942384a53cf claude/preserve/codex-github-automation-hardening-2026-05-22
b72a4165aeb5 claude/preserve/codex-swarm-mvp-github-intake
2a53503cc0b6 claude/propose-suggestions-ready
2793a4a2c901 claude/provision-socrates-chamber-2026-05-29
62a802aba65d claude/ptolemy-research-2026-05-29
4788e0100272 claude/research-abhorsen-old-kingdom
4934359d4354 claude/research-attestation
62c59e5c5f6d claude/rework-census-doctrine-463-4033po
39e5cecd7b41 claude/serene-heisenberg-8ltqb5
224bf638826d claude/socrates-journal-2026-05-31
df637199ac67 claude/socrates-research-2026-05-29
996bb9e65016 claude/sugar-bowl-witness-2026-05-28
d7ce06666712 claude/sweep-enqueue-unstable-prs
e7c1dcb9313d claude/the-binder-magicians-2026-05-30
6c36f4e1bd6e claude/to-will-and-to-halt-2026-05-30
d2386515f221 claude/witness-fire-brazen-head-2026-05-29
a8c8c0265bc6 claude/witness-novice-what-the-novice-does-not-know-2026-05-30
30877ce198dc claude/witness-the-hand-2026-05-29
46d271ec320a claude/witness-usurpers-triptych-2026-05-30
7ba4e58efdcf codex/audit-swarm-liveness-semantics-2026-06-10
5a08f736ad7b codex/codex-work-surface-guard
9670ce542cad codex/fix-worktree-registry-hook
19fc81d00b6f codex/github-dependency-census
3903369a9d68 codex/tantalus-tautomata-campaign-2026-06-04
59d6267e7424 coord/win-mac
73fb01141bcf fix/record-vaulted-abhorsens-first-2026-05-31-clean
a007059de9c4 gh-readonly-queue/main/pr-475-497da14475f83833feed873fdea5e24769d010e0
497da14475f8 gh-readonly-queue/main/pr-492-2022612309074c901a5f59287df0d99fbce3b8e7
273fb5cf63c4 gh-readonly-queue/main/pr-665-ab04530c6ddcb645577ad9b13e755b3cd4b5bf1e
ab04530c6ddc gh-readonly-queue/main/pr-723-00479ca927987bca0404a8193547e437a3c3701d
00479ca92798 gh-readonly-queue/main/pr-727-e8d6ab4cb6acc1e8c49f3d562218f7eb8b97ab4f
e8d6ab4cb6ac gh-readonly-queue/main/pr-728-747bc74aeb2b107b9cbb4cbcc5e2ee7c7bfe2669
e29196d19183 hyperagent/developer-0-esto-perpetua-provenance
7f6146cb337b orphancry/pr-388-original-automation-sync-dependencies
ca510775d14e recovered/pr-353
e16a4aa0f1d0 review/pr-471-agent-swarm-signing
db3e606050bf test/push-gate-20260828
8cd778585bb6 test/tier2-signing-2026-05-29
11860aea01b4 wayback-audit-20260420100033
0e6ab90739e7 wayback-audit-20260615143859-clean
```

## Group B — the 96, by kind (branch → closed PR)

- `bot/daily-rollover-*` (9): #151 #155 #159 #232 #257 #283 #301 #303 #305
- `ingest-*` (17): #194 #202 #264 #281 #302 #304 #306 #308 #319 #320 #323 #325 #326 #337 #338 #339 #340
- `dependabot/*` (23): #121 #176 #243 #295 #312–#316 #328 #330 #331 #333 #342 #352 #359 #360 #362–#366 #371
- `codex/*` (32 branches, 33 PRs; #190 and #191 share `codex/add-legal-references`): #43 #84–#86 #90–#92 #94 #113–#115 #123–#128 #133 #182 #190 #191 #214 #219 #245 #255 #299 #300 #310 #341 #355 #356 #374 #375
- `claude/*` (10 branches, 11 PRs; #353 and #354 share `claude/update-claude-files-PRWCJ`): #104 #118 #122 #132 #157 #171 #173 #188 #256 #353 #354
- `copilot/*` (3): #130 #138 #139
- `antigravity/pullman-oidc-pipeline` #227, `recovered/pr-324` #324

## Session record, 2026-09-25 (other LAF-US repos)

Logan: "All bot PRs, all repos", then fixes as asked. Everything below merged with merge commits.

- THE-GEMSTONE: bot PRs #32–#36, #38–#40, #60, #67, #80 and #85. #85 (27 npm updates) needed two fix commits, fe5ff54 and 74cfbdb, holding back TypeScript 7, Prettier 3.9, satori 0.33 and esbuild 0.27.7; it was merged without a human review, which was reported to Logan. CleanThat #73, then #87.
- IR-Court-Tracker: #16, #17.
- feed-generator: CleanThat #3; #4, the `tsconfig.json` trailing comma plus four clerical fixes; #5.
- VisionClaw: CleanThat #2; #3.

### CleanThat, corrected

The first trim (#73, feed-generator #3, VisionClaw #2) set `can_edit_not_protected_branches: false` on the belief that the bot would then only open PRs. CleanThat's source (solven-eu/cleanthat, d58eb81) declares that field and never reads it: the bot commits onto the head branch of every PR whose base is a protected branch. It did so on feed-generator #4. Repaired in THE-GEMSTONE #87, feed-generator #5 and VisionClaw #3 by adopting this vault's surface (`ANALYZER-CONFIGURATION-SURFACES.md`): syntax version only, no engine.

### pre-commit.ci

feed-generator and VisionClaw had no `.pre-commit-config.yaml`, so the installed app errored on every PR. Both now carry THE-GEMSTONE's read-only configuration (autofix off).

### Forks in LAF-US (as read 2026-09-25; all deleted by Logan by 2026-09-26)

| Repo | Forked from | Visibility | Logan's own commits since forking |
| --- | --- | --- | --- |
| feed-generator | bluesky-social/feed-generator | public | none; only his merges of Dependabot, CleanThat and this session's PRs |
| VisionClaw | Intent-Lab/VisionClaw | public | local build files only (`.idea/`, `workspace.xml`, `samples/`, a `Secrets.kt` backup) |
| AutoKeywordLinker | not visible to this session | public | none (last push predates the fork) |
| alfred-wordreference | not visible to this session | public | none (last push 2021) |

A fork of a public repo cannot be made private. None held work of Logan's worth keeping as a fork, and Logan deleted all four; an org search on 2026-09-26 lists 14 repos and no forks. Logan plans Bluesky feeds later: start those as a standalone repo from `bluesky-social/feed-generator`, not a fork.

### Open, for Logan

- The 65 Group A deletions (script delivered; GitHub 403 to this session).
- `!/LAF-USB-FIVE-CORES-MIGRATION-2026-04-15.md` predates loganfinney and foganlinney, and still lists feed-generator, which is now deleted; `quartz` and `loganfinney27.github.io` no longer resolve under those names.
- Logan (2026-09-26): repos he described as subtreed are being handled by the session on his MacBook. Which repos, and into what: `*`, not read here. Not touched by this session.

Session: https://claude.ai/code/session_01MthFdsNfRK8S4gUivqV9XY
