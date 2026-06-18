---
authority: LOGAN-REVIEW-REQUIRED
status: staged
title: Version Transitions
updated: 2026-06-17
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
| 2026-06-17 | Python runtime | `3.13.3` -> `3.13.13` | Replace the Windows `tempfile` implementation that can retry permission failures up to `2,147,483,647` times; retain pytest cache checks and fail fast when cache storage is unavailable | Python 3.13.13 reports `TMP_MAX=20`; an unwritable-directory probe returns `PermissionError` in under 0.01 seconds; pytest cache-provider regression tests; cross-platform smoke remains on supported `3.10` and `3.13` lanes | Logan review required |
| 2026-05-26 | Version-governance control | unrecorded transition behavior -> staged guard | Prevent task-local version edits from breaking coupled runtime and dependency requirements; no package/runtime version changed by this entry | History review of `3cf73fab`, `0eab6bdf`, `bc19e3f1`, `d0fb10d5`; failures on PRs #359, #363, #364 | Logan review required |
