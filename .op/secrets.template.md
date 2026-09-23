---
name: 1Password Secrets Reference
description: Template for secrets managed via 1Password vault
type: reference
---

# 1Password Secrets Inventory

**Vault:** Use the real visible vault from `op vault list`  
**Management:** Secrets centralized in 1Password; GitHub Actions synced via `OP_SERVICE_ACCOUNT_TOKEN`  
**Updated:** 2026-04-12

---

## Secrets Currently in Use

| Secret Name | Type | Used By | Current Status | Next Action |
| --- | --- | --- | --- | --- |
| `GitHub Personal Access Token` | Personal Access Token | GitHub API (Linear sync, scraper) | ❌ Not created | Create in 1Password + migrate from GitHub Secrets |
| `GitHub SSH Key` | SSH Key (Ed25519) | Git commits, pushes, SSH auth | ❌ Not created | Generate or import + register in 1Password |
| `Linear API Key` | API Key | Linear workspace sync (GitHub Actions) | ⚠️ In GitHub Secrets | Migrate from GitHub Secrets → 1Password |
| `Idaho Legislature API Key` | API Key | Scraper authentication | ❌ Not created | Create if legislator.idaho.gov requires auth |
| `Email SMTP Credentials` | Username + Password | Budget tracker email delivery | ❌ Not created | Create if using SMTP service |
| `Todoist API Token` | API Token | Todoist probe + future bridge (`.github/workflows/todoist-probe.yml`) | ❌ Not created | Create in 1Password as `todoist-api-token`, field `credential` |
| `OP_SERVICE_ACCOUNT_TOKEN` | Service Token | GitHub Actions → 1Password auth | ✅ Provisioned (2026-06-17) | Created via 1Password web portal → Developer Tools → Service Accounts; saved to 1Password vault + added to GitHub Secrets |
| `MERGE_QUEUE_TOKEN` | Fine-grained PAT (repo: IDAHO-VAULT; Contents RW + Pull requests RW) | Auto-merge lane arm/enqueue steps (`auto-merge-engage.yml`, `auto-merge-enqueue-on-checks.yml`, `auto-merge-rhythm.yml`, `batch-arm-merge-queue.yml`, `dependabot-rhythm.yml`, `review-feedback-loop.yml`, `review-response.yml`, `agent-review-gate.yml`) | ❌ Not created | Mint fine-grained PAT (Settings → Developer settings → Personal access tokens → Fine-grained tokens); store in 1Password; add as GitHub Actions repo secret `MERGE_QUEUE_TOKEN`. Without it the lane falls back to `GITHUB_TOKEN`, whose events never dispatch workflow runs — armed PRs starve in the merge queue (issue #731) |

---

## Credential Rotation Schedule

| Secret | Rotation Frequency | Last Rotated | Next Due |
| --- | --- | --- | --- |
| GitHub PAT | 90 days | — | — |
| SSH Key | Annual or on compromise | — | — |
| Linear API Key | 180 days | — | — |
| SMTP credentials | 180 days | — | — |
| Service account token | 90 days | — | — |
| `MERGE_QUEUE_TOKEN` (fine-grained PAT) | 90 days | — | — |

---

## Access Control

- Use the visible vault list from the live desktop account, not a guessed vault name
- GitHub Actions should expose only `OP_SERVICE_ACCOUNT_TOKEN`
- Local developer workflows should use `op` against the signed-in desktop context
- Emergency access remains outside the repo

---

## How to Add a New Secret

1. In the 1Password desktop app:
   - choose the real target vault
   - create the item
   - title it clearly

2. In GitHub Actions:

2. **In GitHub Actions workflow:**

   ```yaml
   - name: Fetch Secret from 1Password
     run: |
       SECRET=$(op item get "[Service] [Credential Type]" --fields password)
       echo "::add-mask::$SECRET"
       echo "SECRET_NAME=$SECRET" >> $GITHUB_ENV
   ```

3. In this file:
   - add the secret row

---

## How to Rotate a Secret

1. **Generate new credential:**

   ```bash
   op generate --length 32 --symbols  # For passwords
   ssh-keygen -t ed25519 -f ~/.ssh/id_new  # For SSH keys
   ```

2. **Update in 1Password:**
   - Edit item → paste new value
   - Note old value in history comment: "Rotated from [old]; expires [date]"
   - Save

3. **Update in dependent systems:**
   - GitHub (if using PAT)
   - Linear workspace (if API key)
   - Third-party services
   - Local `.ssh/config` (if SSH key)

4. **Update this file:**
   - Set "Last Rotated" timestamp
   - Update "Next Due" date

5. **Confirm in workflows:**

   ```bash
   op item get "[Secret Name]"  # Verify new value is returned
   ```

---

## Emergency Procedures

### If a Secret Is Compromised

1. **Immediately revoke** in source system (GitHub, Linear, service provider)
2. **Generate replacement**
3. **Update in 1Password**
4. **Rotate in all dependent systems**
5. **Audit logs** — check for unauthorized access in GitHub Actions, Linear, etc.
6. **Notify team** (if applicable)

### Access Denied or Confusing Auth State

```bash
op account list
op vault list
op whoami
```

If `op whoami` and `op vault list` disagree, trust the live retrieval test from `op item get` before concluding the local install is broken.

---

## Testing

**Local test (after setup):**

```bash
op item get "what3words" --vault Vault --fields label=credential
```

**GitHub Actions test:**
Add a test workflow step:

```yaml
- name: Test 1Password Access
  run: |
    op item list --vault IDAHO-VAULT
```

---

## Related Documentation

- `.op/SETUP.md`
- `1Password.md`
- `what3words.md`
