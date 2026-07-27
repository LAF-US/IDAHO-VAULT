---
title: "Reporting Substrate — issue_reconciler.py Deep-Dive (Map v1)"
created: 2026-06-20
updated: 2026-06-20
status: active
authority: "LOGAN"
authors:
  - Claude Code
source:
  - "code read from origin/main: .github/scripts/issue_reconciler.py + pr_loop_watchdog.py + 5 caller workflows, 2026-06-20"
tags:
  - agent/coordination
  - github/automation
  - ci/automation
  - research/inquiry
related:
  - AGENTS
  - CLAUDE
  - VAULT-CONVENTIONS
  - REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20
  - GitHub
  - Claude Code
---

# Reporting Substrate — `issue_reconciler.py` Deep-Dive

*Filed by [[Claude Code]] (software NAME; no delegated TITLE or OFFICE claimed this session) — 2026-06-20*
*Branch: `claude/github-reviewers-research-u8hlk0`*
*Class: research / INQUIRY — a runtime read, not adopted policy. Companion to the [[REVIEW-MERGE-ENGINE-CLUSTER-A-DEEPDIVE-2026-06-20|Cluster A deep-dive]] and GitHub issue #586 "Map v1".*

---

## Provenance & an honest correction up front

Every claim cites a file/line I read from `origin/main` on 2026-06-20 (the checked-out branch is
397 commits stale — it lacks `looker-walk.yml` and carries an old cron'd `agent-review-gate.yml`;
the generator scripts and `issue_reconciler.py` are byte-identical to `main`).

**Expected vs. found.** I went in expecting to confirm that `issue_reconciler.py` is the "clean
shared substrate" `review_feedback_loop.py` never became, and to recommend leaving it alone. The
read does **not** fully support that. The reconciler is a genuinely *focused* tool — one job, no
review-state tangle — but it has two real fragilities and one side-effect smell that a redesign
should not paper over. The contrast with Cluster A holds at the level of *scope* (1 concern vs. 4),
not at the level of *"flawless."*

---

## 1. The engine at a glance

`issue_reconciler.py` (~242 lines) is single-mode — no subcommands. Args: `--title`,
`--body-file`, `--has-findings`, `--resolved-comment` (build_parser L213+). `reconcile_issue`
(L157) is the whole state machine:

| Input | Action | `issue_action` |
|---|---|---|
| findings, no open issue with this title | `create_issue` (L116) | `created` |
| findings, open issue, fingerprint already present | skip | `noop_duplicate` |
| findings, open issue, body changed | `comment_issue` (L133) | `commented` |
| no findings, no open issue | nothing | `noop` |
| no findings, open issue | post `--resolved-comment` + `close_issue` (L145, reason `completed`) | `closed` |

It touches **issues only**, sets **no labels**, never touches PRs. Identity is the issue **title
string**; body-level dedup is a **SHA256 fingerprint** marker (`<!-- issue-reconciler-fingerprint:… -->`).

## 2. The callers (all from `main`)

Uniform shape: **[generator] → markdown file → `issue_reconciler.py` → one durable issue.**

| Workflow | Trigger | Generator → body | `has_findings` source | Issue title |
|---|---|---|---|---|
| `agent-review-gate` | dispatch — **DISABLED** | `review_feedback_loop reconcile-open-prs` JSON → `pr_loop_watchdog.py build_report` | `bool(blocked)` + action-required queue, combined (L106/116) | `[PR Loop Watchdog]` |
| `looker-walk` | dispatch | `review_feedback_loop looker-walk` JSON → `render-worklist` | jq: any report `lane != "clear"` (L80) | `[Looker Worklist]` |
| `branch-garden-report` | cron Mon 10:00 | `branch_garden_report.py` | script output | `[Branch Garden]` |
| `large-file-watchdog` | cron Mon 11:00 | `large_file_watchdog.py` | script output | `[Large File Watchdog]` |
| `metadata-survey` | cron Mon 10:00 | `metadata_survey.py` | **hardcoded `true`** (L45) | `[Metadata Survey]` |

---

## 3. The four questions, answered by the read

### Q1 — Is the substrate sound, or does it have defects? *Mixed.*

**Fragility A — identity rests on an exact, brittle title string.** `find_open_issue_number`
(L69–89) runs `gh issue list --search "\"{title}\" in:title" --limit 20`, then keeps only an issue
whose title is `== title` exactly (L87). Two consequences: (1) if a human **renames** the
persistent issue even slightly, the next run finds nothing → **creates a duplicate** and orphans
the old thread; (2) the `--limit 20` cap means if >20 open issues match the search text, the real
one can fall outside the page and again spawn a duplicate. The **fingerprint dedups bodies, not
identity** — identity has no stable key (no marker-based lookup, no stored issue number), only the
title. This is the one finding that genuinely complicates the "just reuse it" story.

**Smell — a hash function that writes to disk.** `ensure_body_fingerprint` (L60–66) reads the body
file, strips any prior fingerprint, hashes the canonical body, and **writes the marker back into
the body file** (L65). It is idempotent (it strips before hashing, so re-runs are stable) and
harmless for ephemeral CI files, but it mixes a pure computation with a file mutation, and it means
the on-disk report no longer matches the generator's exact output. A redesign should split "compute
fingerprint" from "persist it."

**Edge — no close hysteresis.** When findings drop to zero the issue is commented + closed every
time (L177+); a flapping signal (findings → none → findings) would close and **recreate** the issue
(new number each cycle), posting churn. Minor, but real.

**Not a flaw — deliberate scope.** Issues-only / no-labels is a focused boundary, not a gap; triage
labels are left to other surfaces.

**Net:** sound *for its narrow job*, but with a brittle identity key and a side-effecting hash —
not "leave it untouched."

### Q2 — Is it separable, or is there hidden coupling? *Separable, but it duplicates plumbing.*

`issue_reconciler.py` imports nothing from `review_feedback_loop.py` — no module coupling. But the
two reimplement the same subprocess primitive: `gh()` / `gh_json()` (issue_reconciler L18–43) vs.
`_run()` / `_graphql()` (review_feedback_loop L111–160) — identical "run, capture, raise
`RuntimeError` on non-zero" pattern, just `gh`-prefixed vs. general-command. So it is cleanly
separable *as a tool*, at the cost of one duplicated wrapper. If the Cluster A §5 redesign extracts
a shared lib, this wrapper is its concrete first member — but that is an opportunity, not a forced
refactor.

### Q3 — How do the five callers actually relate? *One sink, two domains, per-caller finding logic.*

The reconciler is a **clean shared sink**; the variation lives upstream. Two callers
(`agent-review-gate`, `looker-walk`) are **bridges** — they generate content via
`review_feedback_loop.py` and persist via `issue_reconciler.py`, so they straddle both engines.
Three (`branch-garden`, `large-file`, `metadata`) are **standalone surveys**. The
`has_findings` semantics differ per caller (the §2 callers table): `metadata-survey` hardcodes `true` (its issue
is a permanent visibility surface for #252 and **never closes**, L42–45); `looker-walk` derives it
from a jq lane filter; the others trust their generator's output. No title collisions —
`looker-walk.yml`'s own comment (L66–69) explains it deliberately chose a title distinct from
`[PR Loop Watchdog]` because "issue_reconciler overwrites the body by title." So the callers share a
**glue shape** (generator → md + has_findings → reconciler) repeated 5× in YAML, not duplicated
logic.

### Q4 — What does this imply for the Cluster A §5 redesign? *Modest, and mostly affirming.*

The reporting subsystem (5 generators + 1 reconciler) is **not a knot** — it already embodies the
"extract a focused, reusable tool" pattern the Cluster A redesign aims for, which is evidence the
3-tool target is reachable. Two concrete, **independent** improvements fall out, neither requiring
the big redesign:
1. **Unify the `gh` wrapper** (Q2) into the shared lib the Cluster A doc §5 proposes.
2. **Make issue identity robust** (Q1, Fragility A): look the persistent issue up by a stable marker
   (the fingerprint family or a dedicated `<!-- reconciler-id:… -->` tag) rather than an exact title
   string, so manual renames and the 20-issue cap can't orphan a report.

"No deeper implication" is otherwise an honest answer: this substrate works, and the redesign's main
job remains the Cluster A engine, not this one.

---

## 5. Still unmapped (follow-ups, not done here)
The ~14 single-use scripts (a workflow and its own script, Clusters C/E singletons) and the ~10
inline-`gh` workflows that call no script. Those are the last pieces of the Map v1 topology.
