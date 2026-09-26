# 1Password CLI & SSH Agent Setup

**Scope:** Local developer machine + GitHub Actions integration  
**Status:** Template — requires Logan execution  
**Updated:** 2026-03-30

---

## Part 1: Local Installation (Developer Machine)

### Prerequisites
- Windows 11 Pro (confirmed)
- Git Bash installed (`C:\Program Files\Git\bin\bash.exe`)
- 1Password app (desktop) already signed in
- Administrative access on machine

### Step 1: Install 1Password CLI

**Option A: Scoop (recommended for this machine)**
```bash
scoop install 1password
op --version  # Verify
```

**Option B: Homebrew**
```bash
brew install 1password-cli
```

**Option C: Manual download**
Download from https://app-updates.agilebits.com/check/win/1password/latest — extract to `C:\Program Files\1Password CLI\` and add to `PATH`.

### Step 2: Configure Shell Integration

Add to `~/.bashrc` (or equivalent):

```bash
# 1Password CLI integration
export OP_CONFIG_DIR="$HOME/.op"

# SSH agent (1Password) — Unix socket simulation on Windows
if [ -z "$SSH_AUTH_SOCK" ]; then
  export SSH_AUTH_SOCK="$HOME/.ssh/1password-agent.sock"
fi

# Alias for signed commits
alias op-signin='eval $(op signin)'
```

Reload shell:
```bash
source ~/.bashrc
```

### Step 3: Authenticate `op` CLI

```bash
op account add
# Follow prompts: sign-in with 1Password account
```

Test:
```bash
op account list
op vault list
```

### Step 4: Register SSH Key in 1Password

Assumption: You have an SSH key in 1Password vault (e.g., "GitHub SSH Key" item).

**Retrieve key fingerprint:**
```bash
op item get "GitHub SSH Key" --fields private_key --format json | jq -r '.value' > /tmp/gh_key
ssh-keygen -l -f /tmp/gh_key
rm /tmp/gh_key
```

**Enable SSH agent in 1Password desktop app:**
- Open 1Password → Settings → Developer
- Toggle "SSH Agent" ON
- Authorize the SSH key

**Configure SSH to use 1Password agent:**

Create/edit `~/.ssh/config`:
```
Host github.com
  AddKeysToAgent yes
  IdentityAgent ~/.ssh/1password-agent.sock
  IdentityFile ~/.ssh/id_github
```

### Step 5: Configure Git Signing

Point git to 1Password SSH key:

```bash
git config --global gpg.format ssh
git config --global user.signingkey "ssh-ed25519 XXXXXXX..." # fingerprint from Step 4
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.ssh.program "ssh-keyscan"  # or custom wrapper below
```

**Optional: Create SSH wrapper for signing** (if needed)

Create `~/.ssh/sign-wrapper.sh`:
```bash
#!/bin/bash
# Wrapper for git to sign via 1Password SSH key
ssh-keyscan "$@"
```

Make executable:
```bash
chmod +x ~/.ssh/sign-wrapper.sh
```

### Step 6: Test Git Signing

```bash
cd /path/to/IDAHO-VAULT
echo "test" > /tmp/test.txt
git commit --allow-empty -m "Test signed commit"
git log --show-signature  # Verify signature
```

---

## Part 2: GitHub Actions Integration

### Step 1: Create Service Account in 1Password

In 1Password vault, create a new "Password" item:
- **Name:** `GitHub Actions Service Account`
- **Username:** (optional)
- **Password:** Generate a strong token or use existing `OP_SERVICE_ACCOUNT_TOKEN`

**Retrieve token:**
```bash
op item get "GitHub Actions Service Account" --fields password
```

### Step 2: Add Secret to GitHub

In GitHub repo settings (`github.com/loganfinney27/IDAHO-VAULT/settings/secrets/actions`):

**New secret:** `OP_SERVICE_ACCOUNT_TOKEN`  
**Value:** (paste token from Step 1)

### Step 3: Update Workflow to Fetch Secrets

Example workflow file (`.github/workflows/example-with-secrets.yml`):

```yaml
name: Example Job with 1Password

on: [push]

jobs:
  use-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Authenticate 1Password
      - name: Authenticate 1Password
        run: |
          echo "${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}" | op signin --raw
      
      # Fetch secret from 1Password vault
      - name: Fetch GitHub Token from 1Password
        run: |
          GITHUB_PAT=$(op item get "GitHub Personal Access Token" --fields password)
          echo "::add-mask::$GITHUB_PAT"
          echo "GITHUB_TOKEN=$GITHUB_PAT" >> $GITHUB_ENV
      
      # Use secret in subsequent steps
      - name: Use Secret
        run: |
          echo "Token is configured"
          # Don't echo it; use ${{ env.GITHUB_TOKEN }}
```

---

## Part 3: Vault Secret Inventory

### Secrets to Add to 1Password Vault

Create these items in 1Password (Vault: "IDAHO-VAULT" or suitable team vault):

| Item Name | Type | Usage | Status |
|---|---|---|---|
| `GitHub Personal Access Token` | Password | GitHub API calls, Linear sync | Create |
| `GitHub SSH Key` | SSH Key | Git commits, pushes | Create |
| `Linear API Key` | Password | Linear workspace sync | Migrate (currently in GitHub Secrets) |
| `Idaho Legislature API Key` | Password | Scraper authentication | Create |
| `Email SMTP Credentials` | Password | Budget tracker email | Create |

### How to Add a Secret

```bash
op item create --category=login \
  --title="Secret Name" \
  --vault="IDAHO-VAULT" \
  username=user@example.com \
  password="$(op generate --length 32)"
```

### How to Retrieve a Secret

```bash
op item get "Secret Name" --fields password
op item get "Secret Name" --fields label=username --format json
```

---

## Part 4: Troubleshooting

| Problem | Solution |
|---|---|
| `op: command not found` | Add 1Password to PATH; check `echo $PATH` |
| SSH agent socket error | Ensure 1Password desktop app running + SSH Agent enabled in settings |
| Git signing fails | Verify `git config gpg.format ssh` and key fingerprint matches |
| GitHub Actions auth fails | Check `OP_SERVICE_ACCOUNT_TOKEN` is set and valid |
| Vault not found | Run `op vault list` to see available vaults; use correct vault name in commands |

---

## References

- [1Password CLI Docs](https://developer.1password.com/docs/cli/)
- [1Password SSH Agent](https://developer.1password.com/docs/ssh/)
- [Git Signing with SSH](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

---

**Next:** After completing local setup, run `op item list` to verify vault access, then coordinate GitHub Actions integration with Claude Code.
