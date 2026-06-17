---
authority: LOGAN-REVIEW-REQUIRED
status: staged
title: Version Transitions
updated: 2026-05-26
---

# Version Transitions

This is a proposed durable record for version changes made while solving
project needs. A version adjustment is not an isolated repair when another
runtime, package family, workflow, or local environment depends on it.

## Proposed Rule

- Do not change a governed version solely to make the current task pass.
- Before changing a governed version, name the requirement being served, the
  coupled dependencies or environments affected, and the verification result.
- Record the transition in the ledger below in the same pull request.
- Do not revert a governed version as a cleanup or conflict repair without a
  new record explaining the incompatibility being addressed.

Governed version surfaces include:

- `.python-version`
- dependency declarations and project/runtime versions in `pyproject.toml`
- manual or agent-authored pin changes in `requirements.txt`
- version fields in `.crewai/manifest.json`, `manifest.json`, `swarm.json`,
  and tracked Obsidian plugin manifests
- action pins and runtime version inputs in `.github/workflows/`,
  `.github/actions/`, and `.github/dependabot.yml`

## Automated Lock Exception

An authenticated `dependabot[bot]` pull request that changes only
`requirements.txt` may use the pull request metadata and the required
dependency-resolution check as its record. It is not permitted to bypass a
failed compatibility result, alter source constraints, or change a governed
workflow or registry without a ledger entry and manual review.

## Known Coupling Evidence

- `crewai==1.14.5` constrains `mcp~=1.26.0`; `mcp==1.27.1` failed dependency
  validation on PR #364.
- `crewai==1.14.5` constrains `click~=8.1.7`; `click==8.4.1` failed dependency
  validation on PR #363.
- OpenTelemetry package pins form a matching set; a single lift of
  `opentelemetry-exporter-otlp-proto-common` failed dependency validation on
  PR #359 while `opentelemetry-exporter-otlp-proto-http` remained at `1.34.1`.
- `.python-version`, `pyproject.toml`, and regenerated `requirements.txt`
  changed repeatedly on May 25-26, 2026 without a transition ledger.

## Ledger

| Date | Surface | Transition | Purpose / Compatibility Boundary | Verification | Authority |
| --- | --- | --- | --- | --- | --- |
| 2026-06-10 | `swarm.json` registry contract | `2026-05-22 (Logan Tool/Job Correction)` -> `2026-06-10 (durable registration, no liveness inference)` | Separate durable registration, dated observations, and appointment evidence from present agent liveness; consumers must use the renamed topology-census fields and must not infer runtime activity from registry metadata | Bootstrap generation check; topology and startup contract tests; JSON parse; legacy liveness-key scan; PR #510 required checks | Logan review required |
| 2026-05-26 | Version-governance control | unrecorded transition behavior -> staged guard | Prevent task-local version edits from breaking coupled runtime and dependency requirements; no package/runtime version changed by this entry | History review of `3cf73fab`, `0eab6bdf`, `bc19e3f1`, `d0fb10d5`; failures on PRs #359, #363, #364 | Logan review required |
| 2026-06-16 | `.github/workflows/looker-walk.yml` action pins | new workflow adopts the repo-standard `actions/checkout@de0fac2e… (v6.0.2)` pin — no version lifted | New read-only Layer-C census workflow (#526/#399) reuses the checkout pin already standardized across existing workflows; introduces no new or changed action version. The run step passes all `${{ }}` values via `env` (no template injection) and sets `persist-credentials: false` | YAML parse; zizmor template-injection + artipacked cleared; #526 required checks | Logan review required |
| 2026-06-17 | `.github/workflows/engage-outdated.yml` action pins | new workflow adopts the repo-standard `actions/checkout@de0fac2e… (v6.0.2)` pin — no version lifted | First "engage" workflow of the look-then-resolve engine (#399): attest-resolves only bot-only, GitHub-outdated review threads as `github-actions[bot]` (witnessed, never the blind reconciler); never merges. Reuses the standardized checkout pin; no new or changed action version. Dispatch input `apply` passed via `env` (no template injection); `persist-credentials: false`; `pull-requests: write` to resolve threads | YAML parse; `py_compile` + 65 tests; subcommand parse; required checks | Logan review required |
| 2026-06-17 | `.github/workflows/engage-outdated.yml` token scope | `permissions: contents: read` -> `contents: write` (keeps `pull-requests: write`) | Corrects the prior row's assumption that `pull-requests: write` suffices to resolve. The first live `apply=true` run (`27662203952`) resolved 0 of 34 outdated threads — every `resolveReviewThread` returned FORBIDDEN "Resource not accessible by integration". GitHub gates the review-thread resolve/unresolve GraphQL mutations on **Contents: Read & Write**, not pull-requests scope (community discussion #44650). This is the minimal scope lift to make the engine's resolve verb actually execute under the `GITHUB_TOKEN` integration identity; no action version changed | YAML parse; re-dispatch `apply=true` and confirm `resolved > 0` in the run JSON | Logan review required |
| 2026-06-17 | `.github/workflows/engage-outdated.yml` dispatch input | add optional `pr` workflow_dispatch input (string, default `''`) → `--pr` scope flag — no action version changed | Guinea-pig scoping: lets a dispatch target a single PR (#481, Logan's chosen first live case) instead of the whole backlog, to prove one engaged resolution clean before widening. New input passed via `env` (`$PR`) and appended as `--pr` only when non-empty (no template injection); checkout pin, `persist-credentials: false`, and `pull-requests: write` unchanged. `--pr` parsed by `_positive_int` (rejects 0/negative) and refused if the PR is not OPEN, holding the open-queue invariant the backlog walk already had (Sourcery/Copilot/Codex review on #536) | YAML parse; `py_compile` + 69 tests (incl. `--pr` scope, non-open refusal, non-positive rejection); subcommand `--pr` parse; required checks | Logan review required |
| 2026-06-17 | `.github/workflows/batch-arm-merge-queue.yml` query field | `gh pr list --json number,draft,labels` + `select(.draft == false)` -> `…,isDraft,…` + `select(.isDraft == false)` — no action version changed | Bugfix only: `draft` is not a valid `gh pr list` JSON field, so the "Get PRs" step crashed with `Unknown JSON field: "draft"` (dry-run `27701293257`), making the enqueue button-presser non-functional. `isDraft` is the correct field. No pin, runtime version, arming logic, or permission changed | Re-dispatch `dry_run=true`: "Get PRs" succeeds and emits `count=N` (no `Unknown JSON field`); required checks | Logan review required |
