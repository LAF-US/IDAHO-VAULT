---
name: 1Password Secrets Reference
description: Template for secrets managed via 1Password vault
type: reference
---

# 1Password Secrets Inventory

**Vault:** IDAHO-VAULT (or suitable 1Password team vault)  
**Management:** All secrets centralized in 1Password; GitHub Actions synced via `OP_SERVICE_ACCOUNT_TOKEN`  
**Updated:** 2026-03-30

---

## Secrets Currently in Use

| Secret Name | Type | Used By | Current Status | Next Action |
|---|---|---|---|---|
| `GitHub Personal Access Token` | Personal Access Token | GitHub API (Linear sync, scraper) | ❌ Not created | Create in 1Password + migrate from GitHub Secrets |
| `GitHub SSH Key` | SSH Key (Ed25519) | Git commits, pushes, SSH auth | ❌ Not created | Generate or import + register in 1Password |
| `Linear API Key` | API Key | Linear workspace sync (GitHub Actions) | ⚠️ In GitHub Secrets | Migrate from GitHub Secrets → 1Password |
| `Idaho Legislature API Key` | API Key | Scraper authentication | ❌ Not created | Create if legislator.idaho.gov requires auth |
| `Email SMTP Credentials` | Username + Password | Budget tracker email delivery | ❌ Not created | Create if using SMTP service |
| `Todoist API Token` | API Token | Todoist probe + future bridge (`.github/workflows/todoist-probe.yml`) | ❌ Not created | Create in 1Password as `todoist-api-token`, field `credential` |
| `OP_SERVICE_ACCOUNT_TOKEN` | Service Token | GitHub Actions → 1Password auth | ⚠️ In GitHub Secrets | Sync from 1Password via manual provisioning |

---

## Credential Rotation Schedule

| Secret | Rotation Frequency | Last Rotated | Next Due |
|---|---|---|---|
| GitHub PAT | 90 days | — | — |
| SSH Key | Annual or on compromise | — | — |
| Linear API Key | 180 days | — | — |
| SMTP credentials | 180 days | — | — |
| Service account token | 90 days | — | — |

---

## Access Control

- **1Password vault:** Team vault "IDAHO-VAULT" (if org account) or Personal vault (individual account)
- **GitHub Actions:** Only `OP_SERVICE_ACCOUNT_TOKEN` exposed; all other secrets fetched at runtime via `op item get`
- **Local developer:** Full access via `op` CLI after authentication
- **Emergency access:** Backup codes stored in secure location (not repo)

---

## Deprecation / Cleanup

| Item | Status | Date Marked | Cleanup Date |
|---|---|---|---|
| *(none currently)* | — | — | — |

---

## How to Add a New Secret

1. **In 1Password desktop app:**
   - Vault → "IDAHO-VAULT"
   - Create new item (Password, SSH Key, or appropriate type)
   - Title: `[Service] [Credential Type]` (e.g., `Slack Bot Token`)
   - Save

2. **In GitHub Actions workflow:**
   ```yaml
   - name: Fetch Secret from 1Password
     run: |
       SECRET=$(op item get "[Service] [Credential Type]" --fields password)
       echo "::add-mask::$SECRET"
       echo "SECRET_NAME=$SECRET" >> $GITHUB_ENV
   ```

3. **In this file:**
   - Add row to "Secrets Currently in Use" table

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

### If a Secret is Compromised

1. **Immediately revoke** in source system (GitHub, Linear, service provider)
2. **Generate replacement** 
3. **Update in 1Password**
4. **Rotate in all dependent systems**
5. **Audit logs** — check for unauthorized access in GitHub Actions, Linear, etc.
6. **Notify team** (if applicable)

### If 1Password Account is Compromised

1. **Change 1Password account password**
2. **Revoke all service tokens** in 1Password vault
3. **Generate new `OP_SERVICE_ACCOUNT_TOKEN`**
4. **Update GitHub Secrets** with new token
5. **Rotate all secrets** that may have been exposed
6. **Contact 1Password support** if account unauthorized access detected

### Access Denied After Setup

```bash
# Re-authenticate
op signin

# Check current session
op whoami

# List available vaults
op vault list

# Check vault permissions
op vault get IDAHO-VAULT
```

---

## Testing

**Local test (after setup):**
```bash
op item get "GitHub Personal Access Token" --fields password
# Should return the token without errors
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

- `.op/SETUP.md` — Installation and configuration steps
- `!/VAULT-CONVENTIONS.md` — Vault secret management section
- `.claude/CLAUDE.md` — Claude Code operational context
