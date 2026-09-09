---
title: "NOTE — The Risk Labeller, Batch Automation, and Arbiter Sortition, in the Context of the Wider Script Thicket"
updated: 2026-07-11
status: draft
authority: LOGAN
author: "Claude Code (no delegated persona, title, or office claimed this session)"
tags:
  - agent/coordination
  - ci/automation
  - github/merge
  - research/inquiry
related:
  - REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20
  - WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21
  - VAULT-CONVENTIONS
  - CONSTITUTION
---

# NOTE — The Risk Labeller, Batch Automation, and Arbiter Sortition, in the Context of the Wider Script Thicket

*Filed by Claude Code, 2026-07-11, session `claude/practical-cerf-l13ka2`. Deferred by Logan's own direction: "note for now," not act now. No redesign proposed here — just the sourced observation, so it doesn't have to be re-discovered later.*

## What Logan said

> "The 'batch' automations were intended to be a varied set of flowchart logic-gate sequenced tools to route PRs to the appropriate fix lanes... but unfortunately the contractor cobbled everything together into several misleadingly named monoscripts."
>
> "it's a 'note for now' along with two adjacent yet related systems, the risk labeller and the sortition arbiter"
>
> "classify_paths belongs in that file as well, prominently, then with a[nother], holistic perspective on the script thicket"

All three lines are Logan's own words, `[told]`, this session. Everything below is what I verified against the actual code today to ground that claim — not assumed from it.

## What I verified, per system

**1. Risk labeller (`classify_paths.py`) — the most architecturally mature of the three, and the one furthest from having its own output actually used.**
This is not a quick label-slapper; it's a genuinely careful two-axis model, and it says so about itself. Read in full (260 lines, `.github/scripts/classify_paths.py`):

- **Two independent analyses per file**, composed into a grid: `filetype_flag()` scores WHAT KIND of file it is — Natural Language (`.md`/`.txt`) → `—` (no flag), Machine Documentation (`.json`/`.yaml`) or inert assets → `low`, Computer Code (`.py`/`.sh`/`.ipynb`/...) → `med`, unrecognized → `med` (fail-safe). `placement_flag()` independently scores WHERE it sits — inside the `!` Nest, Levels 2–6 → `high`, the Level-7 "still point" (`Esto Perpetua!`) → `nope`, protected surfaces (`.github/**`, named root governance files, any top-level dotfolder like `.claude/`/`.codex/`) → `high` even outside the Nest, everything else → `—`.
- **One ordering primitive, `TIER_PRECEDENCE = ("nope", "high", "med", "low", "clear")`**, is the single source of truth both axes and their combination read — the module's own comment calls out that this is deliberate, to prevent the tier order from drifting out of sync between the aggregation and combine steps.
- **The output is an 8-field JSON object** (`tier`, `tier4`, `filetype`, `depth`, `subtier`, `by_file`, `high_risk_files`, `low_risk_files`) — a real 5-cell grid (`clear`/`low`/`med`/`high`/`nope`) with per-file detail and a `subtier` field already reserved for a *second* planned refinement (filetype subtiers = the three blessed circles + the Jupyter "missing middle"; depth subtiers = the seven Demesnes/Levels) that the file says is "unique unspecified" and deferred by Logan as of 2026-06-21.
- **Confirmed consumption: exactly 2 of 48 workflows call it** (`agent-auto-pr.yml`, `auto-merge-rhythm.yml`), and of the 8 fields it emits, **exactly 1** — the binary `tier` (`low`/`high`) — is read by anything, to stamp a single `risk/<tier>` label. `tier4`, `filetype`, `depth`, `subtier`, and both `by_file`/`*_risk_files` breakdowns are computed on every PR and then discarded. The file's own header names this precisely: *"the routing MECHANISM (lanes, flag lifecycle, grid-cell routes) is HELD for Logan — see issue #626 + `WITNESS-THE-KEYS-ARE-THE-LEVERS-2026-06-21.md`. The grid is a model, not code."* So this specific gap isn't new or hidden — a prior session already flagged it in writing, in the code itself, over three weeks before Logan raised it again today.

**2. Batch automation (`batch-arm-merge-queue.yml` + inline `gh` calls) — confirmed monoscript, no lane routing.**
Ran a live `dry_run: true` dispatch today (run `29162177905`) against all 32 open non-draft PRs. The script computes each PR's real `mergeStateStatus` (`CLEAN`/`UNSTABLE`/`BEHIND`/`BLOCKED`/`DIRTY`) but only branches on it into two buckets: `BEHIND` gets an actual branch-update, everything else not already `CLEAN`/`UNSTABLE` — whether it's `DIRTY` (a real merge conflict, 6 of 32 PRs today) or `BLOCKED` (failing checks or missing review, 23 of 32 PRs today) — gets the identical blind `gh pr merge --auto` no-op arm. There is no code path that distinguishes "needs conflict resolution" from "needs a check fixed" from "needs your review," despite the workflow's own header comments describing exactly that intended distinction ("DIRTY … is left for a human" — but the code arms it anyway, same as `BLOCKED`). It also never reads `classify_paths.py`'s output at all — a `depth:nope` PR touching the canon core and a `filetype:low` PR touching a single JSON file get identical treatment if both happen to be `BLOCKED`.

**3. Sortition arbiter (`arbiter_sortition.py` / `arbiter-sortition.yml`) — fixed draw, no risk input.**
`--arbiter-count 2` is a constant passed from the workflow file, not derived from a PR's risk labels. The reviewer pool (`ALL_REVIEWERS`) is a flat hardcoded set of 5 bots + Logan; there's no tier-based expansion (e.g., more/stricter arbiters for a `depth:high` PR touching `.github/**`) despite the risk classifier sitting right there, already labeling every PR before sortition runs.

## Holistic view of the script thicket

Logan asked for the wider view, not just these three, so here's the actual inventory rather than an impression of it. `.github/scripts/` holds **48 Python files, 13,505 lines total**, run by **48 workflow files** in `.github/workflows/`. Roughly, by function (my own grouping, not a file-declared taxonomy):

| Cluster | Scripts (rough count) | Examples |
| --- | --- | --- |
| Policy gates (fail-closed CI checks) | ~11 | `check_action_pins`, `check_large_files`, `check_portable_paths`, `check_redaction_damage`, `check_secret_patterns`, `check_python_version_pin`, `check_character_conformity`, `check_dotfolder_anchors`, `meshnetweb_portability_check`, `laf_usb_manifest`, `jupytext_sync_paired` |
| PR lifecycle / merge orchestration | ~10 | `review_feedback_loop` (2,343 lines — the single largest script in the repo, already deep-dived in `REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20.md` as one file covering 4 unrelated concerns across 14 subcommands), `pr_lifecycle`, `pr_loop_watchdog`, `pr_threads`, `pr_github`, `issue_reconciler`, `stale_bot_prs`, `codex_work_guard`, `arbiter_sortition`, `verify_arbiter_approvals` |
| Vault content maintenance | ~12 | `daily_rollover` (1,093 lines), `backfill_daily_notes`, `date_tagger`, `expand_date_aliases`, `normalize_tags`, `tag_stubs`, `generate_name_forms`, `metadata_survey`, `audit_repo_payloads`, `phone_link_intake`, `bind_ai_book`, `validate_content` |
| Registry / manifest sync | 3 | `generate_agents_bootstrap`, `sync_obsidian_plugin_registry`, `update_manifest` |
| Reporting (no gating effect) | ~6 | `branch_garden_report`, `topology_census` (906 lines), `wayback_audit`, `wayback_preserve`, `janitor_sweep`, `swarm_mvp_intake` |
| Classification | 2 | `classify_paths`, its own test file |
| Shared infra | 3 | `gh_cli`, `obsidian_rest_api_client`, `uv_dependency_submission` |

The pattern across all three systems above generalizes: this isn't three isolated gaps, it's the same shape recurring at every scale in this directory. `review_feedback_loop.py` is a *single file* that's internally the same story `classify_paths`/`batch-arm-merge-queue`/`arbiter_sortition` are *across files* — four genuinely distinct concerns (label substrate, review-state projection, claim verification, thread-attestation) sharing one 2,343-line module because nobody split them when the fourth concern got bolted on. The 48-script directory is the same fragmentation one level up: each script is usually well-built in isolation (today's read of `classify_paths.py` in particular is careful, self-documenting, deliberately single-sourced) but the *connections between them* — the wiring Logan describes as the intended "flowchart logic-gate sequenced" design — were never built, so 48 scripts run near each other on every PR mostly blind to each other's output.

## The connecting thread (the three, specifically)

All three named systems run on every PR, in sequence, and each one *could* read the risk classification the one before it produced — but none of them do except the single `tier` read in `agent-auto-pr.yml`. The intended flowchart (classify → route to a lane by risk+state → arbiter selection scaled to that lane) collapsed into three independent scripts that happen to run near each other on every PR, each blind to the others' output.

## Addendum, same day: the planned visible risk-label model (Logan's spec, verbatim)

After the 2026-07-11 label consolidation (4 orphan labels deleted, `merge/auto`/`auto-merge` descriptions corrected — GH PR #839), Logan added:

> "the `*:risk/*` labels are redundant too... the planned visible model is `risk/{—}NOR{{{low}OR{med}}+{{high}OR{nope}}}/{subtier}`"

That grammar is Logan's own line, `[told]`, this session, quoted exactly. My reading of it, offered as a parse and not as settled interpretation: **one composed `risk/...` label replaces the two per-axis labels** — the body is `—` when neither analysis fired (the NOR cell, matching today's live `risk/—`), otherwise a `+`-composition of the fired filetype flag (`low`|`med`) and the fired depth flag (`high`|`nope`), with a trailing `/{subtier}` segment. Under that model the six `filetype:risk/*` / `depth:risk/*` axis labels are redundant *as visible vocabulary* — the pair collapses into one label.

**Why they cannot simply be deleted today, verified against the engine (2026-07-11):** unlike the four orphans removed in #839's companion cleanup, the pair vocabulary is live-wired into `review_feedback_loop.py` at every layer — declared in `LABEL_SPECS` (so `ensure-labels` recreates them on every pass), read per-axis by `_axis_flag`/`_risk_pair_for_pr` (L935–980, with a fail-loud `RiskMarkerInvariantError` on per-axis double-labeling), restamped on every projection pass by the K6 apply step (L1037–1058, which also keeps the legacy sparse singles in sync), and consumed by the auto-merge eligibility chain itself (`is_clear`/`lane_complete`/`flag_clearable`, L1111–1125). Retiring them is an engine migration — the visible-projection layer of the K6 lane model — not an API cleanup.

**Open pins the grammar leaves (the `*` wildcard, not gaps I get to fill):**

1. **Single-axis-fired cells.** The 3×3 grid has four cells where exactly one axis fired (e.g. a maze `.py`: filetype `med`, depth `—`). The grammar's `+`-composition names the both-fired cells and `—` names the neither-fired cell; how a one-fired cell renders (`risk/med`? `risk/med+—`? something else) is not specified in the line as given.
2. **Subtier vocabulary.** `{subtier}` remains "unique unspecified" per `classify_paths.py`'s own docstring (filetype subtiers = the three blessed circles + the Jupyter missing-middle; depth subtiers = the seven Levels/Demesnes) — and which axis's subtier appears when both fired is likewise unspecified.
3. **Relation to the K6 two-label norm.** The engine's own comment records "K6/#632 (norm set by Logan, 2026-07-06): the lanes ARE the nine label pairs. Every PR carries exactly TWO axis labels." The composed model keeps the nine-cell lane grid but changes its visible projection from two labels to one — reading this as a refinement of K6's projection rather than a reversal of its model, but that characterization is mine, not Logan's.

## Aside, possibly useful later (not part of the deferred item)

`arbiter_sortition.py`'s own comment documents a CodeQL modeling fact directly relevant to the open alert I'm currently working on PR #562: *"CodeQL's command-line-injection sanitizer only recognizes comparisons against a literal constant, and a regex `.fullmatch()` does not register as one."* That's independent, prior-session confirmation of exactly what I was inferring today from `install-skill-from-github.py`'s persistent CodeQL alert surviving two rounds of regex-based validation (`_validate_ref`/`_validate_owner_repo`). Worth remembering if that alert (or ones like it) comes up again: CodeQL wants a literal-constant comparison, not a regex match, to recognize a barrier.

## Status

Deferred, per Logan. Not touching `.github/workflows/**` or `.github/scripts/**` for this — logged so the next pass (mine or anyone else's) doesn't have to re-derive it from scratch.
