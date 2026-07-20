# Plan: Pin GitHub Actions to Full Commit SHAs

## Context

The LAF-US org has a "Require actions to be pinned to full-length commit SHA" policy
available but not yet enabled. Before it can be enabled, all `uses:` references in
workflow files must be updated from tag-based pins (`@v4`) to commit SHA pins
(`@abc123... # v4`). All ten distinct action references have been resolved to their
current commit SHAs.

---

## SHA Map (resolved 2026-04-17)

| Reference | Commit SHA | Comment |
|---|---|---|
| `1password/load-secrets-action@v4` | `92467eb28f72e8255933372f1e0707c567ce2259` | `# v4` |
| `actions/checkout@v4` | `34e114876b0b11c390a56381ad16ebd13914f8d5` | `# v4` |
| `actions/setup-python@v5` | `a26af69be951a213d495a4c3e4e4022e16d87065` | `# v5` |
| `actions/setup-python@v6` | `a309ff8b426b58ec0e2a45f0f869d46889d02405` | `# v6` |
| `actions/upload-artifact@v7` | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | `# v7` |
| `dawidd6/action-send-mail@v16` | `d38f3f7cd391cdebfe0d38efc3998b935e951c4f` | `# v16` |
| `dependabot/fetch-metadata@v3` | `ffa630c65fa7e0ecfa0625b5ceda64399aea1b36` | `# v3` |
| `google-github-actions/auth@v3` | `7c6bc770dae815cd3e89ee6cdf493a5fab2cc093` | `# v3` |
| `google-github-actions/setup-gcloud@v3` | `aa5489c8933f4cc7a4f7d45035b3b1440c9c10db` | `# v3` |
| `peter-evans/create-pull-request@v8` | `5f6978faf089d4d20b00c7766989d076bb2fc7f1` | `# v8` |

---

## Files Modified

| File | Action references present |
|---|---|
| `.github/workflows/*.yml` (all 27) | `actions/checkout@v4`, `actions/setup-python@v6`, `peter-evans/create-pull-request@v8`, and others per file |
| `.github/actions/setup-vault/action.yml` | `actions/setup-python@v5` only |

---

## Implementation

Use `sed -i` global in-place replacements across all `.github/workflows/*.yml` and
`.github/actions/setup-vault/action.yml`. One sed expression per action. Execute all
in a single bash pass.

```bash
cd /path/to/repo
FILES=".github/workflows/*.yml .github/actions/setup-vault/action.yml"

sed -i \
  -e 's|1password/load-secrets-action@v4|1password/load-secrets-action@92467eb28f72e8255933372f1e0707c567ce2259 # v4|g' \
  -e 's|actions/checkout@v4|actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4|g' \
  -e 's|actions/setup-python@v5|actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5|g' \
  -e 's|actions/setup-python@v6|actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6|g' \
  -e 's|actions/upload-artifact@v7|actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7|g' \
  -e 's|dawidd6/action-send-mail@v16|dawidd6/action-send-mail@d38f3f7cd391cdebfe0d38efc3998b935e951c4f # v16|g' \
  -e 's|dependabot/fetch-metadata@v3|dependabot/fetch-metadata@ffa630c65fa7e0ecfa0625b5ceda64399aea1b36 # v3|g' \
  -e 's|google-github-actions/auth@v3|google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093 # v3|g' \
  -e 's|google-github-actions/setup-gcloud@v3|google-github-actions/setup-gcloud@aa5489c8933f4cc7a4f7d45035b3b1440c9c10db # v3|g' \
  -e 's|peter-evans/create-pull-request@v8|peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1 # v8|g' \
  $FILES
```

---

## Post-implementation

After files are updated and committed:
1. Enable "Require actions to be pinned to full-length commit SHA" in GitHub org Actions settings at `https://github.com/organizations/LAF-US/settings/actions`.
2. This requires org admin access — Logan handles this step.

---

## Verification

1. `grep -r "@v[0-9]" .github/` returns no matches (all tags replaced).
2. `grep -r "uses:" .github/workflows/ .github/actions/` shows only SHA-format pins.
3. Spot-check: `daily-rollover.yml` `actions/checkout` line reads `@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4`.
4. Commit goes to a branch; PR passes `check-paths` and `check-dotfolder-anchors` required checks.
