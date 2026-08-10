---
name: idaho-vault-action-pinning
description: "IDAHO-VAULT currently pins GitHub Actions to commit SHA with version comment. Logan is reconsidering whether universal SHA pinning is worth the maintenance cost vs. major-version tags for low-risk read-only setup actions. Keep matching the surrounding file's style until policy is settled."
metadata:
  node_type: memory
  type: project
  originSessionId: c6d318fa-b7e2-4d26-8bc8-139b94952b9f
---

**Current state (2026-05-26):** IDAHO-VAULT workflows pin every action by commit SHA with a trailing `# vN` comment:

```yaml
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4
- uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
```

An earlier agent installed this discipline. **The policy is under review** — Logan flagged that universal SHA pinning may create more conflict vectors than it prevents, especially for read-only setup actions whose threat surface is small but whose maintenance burden (Node-runtime deprecation, manual bump cadence) is real.

**Trade-off Logan is weighing:**

| Action type | Threat | Reasonable pin style |
|---|---|---|
| Has secrets, posts comments, pushes commits | High — can exfiltrate/impersonate | SHA pin |
| Read-only setup (setup-python, setup-uv, setup-node) | Low — no token escalation on its own | Major-version tag fine |
| Custom/unmaintained actions | High — author may abandon | SHA pin + audit before bump |

**What to do meanwhile:**
- When adding an action to an existing workflow, **match the surrounding file's style** to avoid creating an inconsistent pin pattern that pre-empts Logan's broader decision.
- Don't propose mass-converting existing pins until Logan has settled the policy.
- If a Node runtime is actually deprecated and breaks a pin, the fix is bumping the pin (not abandoning pinning); but until that happens, no pre-emptive sweeps.

**How to pin to SHA when adding (still the default for now):**
1. `gh api repos/<org>/<action>/releases/latest --jq '.tag_name'` → latest tag
2. `gh api repos/<org>/<action>/git/ref/tags/<tag> --jq '.object.sha'` → commit SHA
3. `gh api repos/<org>/<action>/contents/action.yml --jq .content | base64 -d | grep "using:"` → confirm runtime (prefer `node24`)
4. Write as `uses: <org>/<action>@<sha> # <tag>`

Related: [[idaho_vault_dep_drift_pattern]] (same "fix the underlying thing" discipline, different layer)
