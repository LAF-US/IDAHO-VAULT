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
|---|---|---|---|---|
| `GitHub Personal Access Token` | Personal Access Token | GitHub API | Not created | Create in 1Password or migrate |
| `GitHub SSH Key` | SSH Key | Git commits and pushes | Not created | Generate or import |
| `Linear API Key` | API Key | Linear sync | In GitHub Secrets | Migrate from GitHub Secrets to 1Password |
| `Idaho Legislature API Key` | API Key | Scraper auth | Not created | Create if needed |
| `Email SMTP Credentials` | Username + Password | Budget tracker email | Not created | Create if needed |
| `what3words API Key` | API Key | what3words desktop / CLI lookup | Live item verified | Use `Vault / what3words / credential`; investigate `HTTP 401` behavior |
| `OP_SERVICE_ACCOUNT_TOKEN` | Service Token | GitHub Actions to 1Password auth | In GitHub Secrets | Sync from 1Password via manual provisioning |

---

## Credential Rotation Schedule

| Secret | Rotation Frequency | Last Rotated | Next Due |
|---|---|---|---|
| GitHub PAT | 90 days | - | - |
| SSH Key | Annual or on compromise | - | - |
| Linear API Key | 180 days | - | - |
| what3words API Key | Provider policy | - | - |
| SMTP credentials | 180 days | - | - |
| Service account token | 90 days | - | - |

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

```yaml
- name: Fetch Secret from 1Password
  run: |
    SECRET=$(op item get "[Secret Name]" --fields password)
    echo "::add-mask::$SECRET"
```

3. In this file:
   - add the secret row

---

## How to Rotate a Secret

1. Generate the new credential
2. Update the 1Password item
3. Update dependent systems
4. Update this file
5. Confirm retrieval:

```bash
op item get "[Secret Name]"
```

---

## Emergency Procedures

### If a Secret Is Compromised

1. Revoke it in the source system
2. Generate a replacement
3. Update it in 1Password
4. Rotate all dependent systems
5. Audit logs

### Access Denied or Confusing Auth State

```bash
op account list
op vault list
op whoami
```

If `op whoami` and `op vault list` disagree, trust the live retrieval test from `op item get` before concluding the local install is broken.

---

## Testing

Local test:

```bash
op item get "what3words" --vault Vault --fields label=credential
```

Expected outcome on Logan's machine as of 2026-04-12:

- secret retrieval succeeds
- downstream what3words API probe still returns `HTTP 401`

That means the remaining blocker is now most likely the what3words key policy, restriction, or entitlement rather than a missing 1Password secret.

---

## Related Documentation

- `.op/SETUP.md`
- `1Password.md`
- `what3words.md`
