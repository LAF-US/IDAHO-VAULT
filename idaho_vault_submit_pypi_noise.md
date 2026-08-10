---
name: idaho-vault-submit-pypi-noise
description: "The submit-pypi check on IDAHO-VAULT comes from GitHub's Automatic Dependency Submission feature, not a `.github/workflows/` file. When it fails, it is correctly flagging a real dependency-resolution problem — fix the underlying conflict; do NOT propose disabling the feature."
metadata:
  node_type: memory
  type: project
  originSessionId: 4ebcc146-08af-4d98-8ba6-b8b3b366018d
---

The `submit-pypi` check that shows FAILURE on most IDAHO-VAULT PRs is GitHub's built-in "Automatic Dependency Submission (Python)" feature. It is **not** a workflow in `.github/workflows/`. The check fires from a dynamic source (`event: dynamic`, `path: dynamic/dependency-graph/auto-submission` in the workflow run metadata) and its job is named `submit-pypi` by GitHub.

The feature populates GitHub's dependency graph (which feeds Dependabot security alerts) by running Microsoft's component-detection engine against the repo's lockfile and posting the resolved tree via the Dependency Submission REST API.

**Why the check fails on this repo:** the dependency tree has a real unresolvable conflict. Codex identified the current case on 2026-05-22: `posthog==7.15.0` (from a recent Dependabot bump) vs. `chromadb` requiring `posthog<6.0.0`. The component-detection engine can't resolve the env, so submission fails. **The failing check is correct.** It is signaling a real broken state in the dependency graph.

**How to apply — and what NOT to do:**
- **DO** treat a failing `submit-pypi` check as a real signal pointing at a real dependency-resolution problem. Fix the underlying conflict; the check will then pass and Dependabot's transitive-dep coverage will work as intended.
- **DO NOT** propose disabling the feature in Settings → Code security as a "fix." Per Logan's standing discipline: turning off a failing check is not a fix — it is willfully ignoring something broken that is causing the check to fail. This applies to `submit-pypi` and to every other failing check.
- **DO NOT** propose editing branch protection to remove `submit-pypi` from a required-checks list — `main` is not branch-protected (HTTP 404 on `branches/main/protection`), so there is no required-checks list to clean up. That theory pattern-matches a sensible answer without grounding in evidence.
- **DO NOT** propose editing `.github/workflows/` to silence it — there's no workflow file producing it. The control is server-side (the dependency-graph submission feature), not in the repo.
- Diagnostic: `gh api repos/LAF-US/IDAHO-VAULT/actions/runs/<id>` — if `path` starts with `dynamic/`, the run is from a GitHub-managed feature, not a repo workflow. Then `gh api repos/LAF-US/IDAHO-VAULT/actions/runs/<id>/jobs` to confirm the job name.

**Historical correction (2026-05-24):** Earlier versions of this memory framed disabling the feature as "the durable fix if the failing check is becoming a distraction." That was wrong-shaped — it treated a real broken signal as noise to silence. Corrected to reflect Logan's discipline: a failing check is a signal that the thing it checks is broken; fix the broken thing, don't silence the signal.
