---
name: idaho-vault-dep-drift-pattern
description: "Recurring problem in IDAHO-VAULT — Dependabot bumps individual transitive deps in requirements.txt that violate their consumers' pins (crewai, otel suite). submit-pypi correctly fails; ad-hoc closes/ignores accumulate. Structural fix needed."
metadata: 
  node_type: memory
  type: project
  originSessionId: c6d318fa-b7e2-4d26-8bc8-139b94952b9f
---

**The recurring pattern (recognized 2026-05-26):**

`pyproject.toml` declares only 6 top-level deps (crewai, flask, pydantic, huggingface-hub, requests-oauthlib, honcho-ai). `requirements.txt` is the fully-resolved transitive lockfile (~hundreds of lines, including click, mcp, opentelemetry-*, etc).

Dependabot is pointed at `requirements.txt` and bumps individual leaf entries. But many of those leaves are tightly pinned by their consumers:
- `crewai 1.14.5` pins `click~=8.1.7`, `mcp~=1.26.0` (latest crewai still does)
- `opentelemetry-exporter-otlp-proto-http==1.34.1` pins `opentelemetry-exporter-otlp-proto-common==1.34.1` (and the otel suite needs lockstep version moves)

Each Dependabot PR that bumps one of these leaves alone creates an unresolvable dep tree → `submit-pypi` correctly fails → PR sits or gets closed → next week's PR repeats the cycle. The `.github/dependabot.yml` has accumulated ad-hoc ignores (pydantic >=2.12, otel-grpc/proto >=1.35) — those are this pattern leaving scar tissue.

**CODEX's 2026-05-26 hardening did NOT fix this.** It added `dependabot-rhythm.yml` (gating *merges* of automation PRs) and the Containment ruleset (requiring `submit-pypi` to pass), but didn't address why submit-pypi keeps failing. Net effect: hardened the door on a wall that's still cracking.

**Why:** Why: Dependabot bumps a leaf, the consumer pin rejects it, submit-pypi fails, PR can't merge.

**How to apply:** Whenever a `submit-pypi` failure is in scope, check `requires_dist` of the consumer (crewai is the usual culprit) before proposing any bump. If the bump violates a consumer pin, the structural fix is one of:
1. **Scope Dependabot to pyproject.toml only** — remove requirements.txt from its purview; let `uv lock` regenerate transitives. Dependabot then only proposes top-level bumps; transitive moves come from `uv lock --upgrade` on a schedule.
2. **Define Dependabot `groups:`** in `.github/dependabot.yml` for known co-moving families (otel-* especially). Each group becomes one consistent PR.
3. **Both** — Option 1 is the root fix; Option 2 helps if you keep the lockfile-in-repo pattern.

Don't add another entry to the `ignore:` list unless it's a temporary fix tagged with a follow-up — that's how the scar tissue grows.

Related: [[idaho_vault_submit_pypi_noise]], [[idaho_vault_branch_protection_history]], [[feedback_no_demiurging]]
