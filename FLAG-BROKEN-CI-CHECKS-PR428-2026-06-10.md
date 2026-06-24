---
title: "Flag — Broken CI Checks (auth) on PR #428"
updated: 2026-06-10
created: 2026-06-10
authority: LOGAN
doc_class: flag-record
status: archived
matter: "Two CI checks on PR #428 failed on GitHub-API authentication, independent of PR content — RESOLVED by a base-branch update"
flagged-by: "Claude Code (imported software; Direct-Write implementer) — flag raised at the Architect's command to flag broken checks in a commit"
adjudication: "RESOLVED 2026-06-10 — both checks passed after the base update (head 1413f97); no workflow was edited. Retained for the record."
related:
  - "[[DISAMBIGUATION-NEEDED-LINK-TARGETS-2026-06-09]]"
  - "[[!/AGENTS]]"
---

# Flag — Broken CI Checks (auth) on PR #428

> Raised at the Architect's command to **flag the broken checks in a commit**. Two checks on `LAF-US/IDAHO-VAULT` PR #428 (head `bff5439`) fail, and both fail for the **same reason: a GitHub-API authentication error in the Actions environment** — *not* because of anything in the branch's content. This node records the breakage and holds the fix for the Architect. It **decides nothing and edits no workflow.**
>
> **Provenance.** Conclusions read **verbatim from the failing job logs** on head `bff5439`, pulled 2026-06-10. Tier: **[fact]** for the log excerpts and the pass/fail inventory; **[reading]** for the "not content-related" attribution (grounded in: the branch diff is 100% Markdown, and a parallel CodeQL job on the same languages passed).

## Update — 2026-06-10: resolved by a base-branch update

Both checks now **pass.** After the Architect updated the base branch (`main` merged into the PR branch; head advanced from `bff5439` → `1413f97`), CI re-ran clean: **`auto-merge-maintainer` → success** and **both `Analyze (python)` (CodeQL) → success**, alongside every other gate. The earlier `401` / `Requires authentication` failures were transient environment/token conditions, not branch content — confirmed, since nothing in the branch's `.py` or workflow surface changed between `bff5439` and `1413f97` except the base merge. **This session edited no workflow.** The flag is **closed and retained for the record**; the original (failing) findings are preserved below as the historical entry.

## The two failing checks (historical — as of `bff5439`)

| Check | Conclusion | Root cause (from logs) |
|---|---|---|
| `Analyze (python)` (CodeQL) | failure | `codeql-action/init` aborted: `HttpError: Requires authentication` while determining feature enablement. A **parallel** `Analyze (python)` and `Analyze (actions)` on the same commit **passed** — so this is one workflow's credential issue, not a code defect. |
| `auto-merge-maintainer` | failure | `gh pr merge --auto` returned **`401 Unauthorized` — "Requires authentication."** The auto-merge automation's token lacks merge permission. |

Both errors are **token/permissions** problems in the CI environment. The branch diff is entirely Markdown (research/concept notes); CodeQL scans `.py`, which this branch never touches.

## What is green (for contrast)

All content and quality gates on `bff5439` pass: the six `smoke` matrix jobs; `check-paths`, `check-dotfolder-anchors`, `check-date-placeholders`, `check-secret-patterns`, `check-large-files`, `check-version-transitions`; Aikido, GitGuardian, CodeQL `Analyze (actions)` and the **passing** `Analyze (python)`; `submit-pypi`; GitBook; and CodeRabbit ("Review completed"). The **required** status checks that gate `main` — `check-secret-patterns`, `check-large-files`, `check-paths`, `check-dotfolder-anchors` — are all green.

## Why this is flagged, not fixed

The fix lives in `.github/workflows/*` (CI token scopes / permissions) — a **protected path**. The repo's own `auto-merge-maintainer` logic marks `.github/workflows/*` as "manual review required," and CI secrets/permissions are an Architect/maintainer concern, not an implementer's Direct-Write surface. So this session **does not touch the workflows**; it records the breakage and the evidence, and holds the decision.

## Disposition

**Status: RESOLVED (2026-06-10).** Both checks passed on the base-updated head `1413f97` (see the Update section above) — confirming the breakage was environmental, not branch content. Originally flagged OPEN for the Architect / maintainer while both checks were failing on `bff5439`. This flag promoted nothing and changed no automation; it stands as the record that the failures were transient and pre-dated this branch's content.

---

## DOCUMENT METADATA

- **Created:** 2026-06-10
- **Last Updated:** 2026-06-10
- **Status:** Archived (resolved)
- **Authority:** LOGAN
- **Authors:** Claude Code (imported software; Direct-Write implementer)
- **Change Note:** Flagged the two auth-failing CI checks (CodeQL `Analyze (python)`, `auto-merge-maintainer`) on PR #428 head `bff5439`; evidence from job logs; no workflow edited. Updated 2026-06-10: both checks passed after a base-branch update (head `1413f97`); flag closed and retained.
