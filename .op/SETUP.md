# 1Password CLI & SSH Agent Setup

**Scope:** Local developer machine + GitHub Actions integration  
**Status:** Template with desktop reality notes from 2026-04-12  
**Updated:** 2026-04-12

---

## Part 1: Local Installation (Developer Machine)

### Prerequisites

- Windows 11 Pro (confirmed)
- Git Bash installed (`C:\Program Files\Git\bin\bash.exe`)
- 1Password desktop app installed
- Administrative access on machine

### Step 1: Install 1Password CLI

**Option A: Scoop (recommended for this machine)**

```bash
scoop install 1password
op --version
```

**Option B: Homebrew**

```bash
brew install 1password-cli
```

**Option C: Manual download**
Download from <https://app-updates.agilebits.com/check/win/1password/latest> — extract to `C:\Program Files\1Password CLI\` and add to `PATH`.

### Step 2: Configure Shell Integration

Add to `~/.bashrc` or equivalent:

```bash
export OP_CONFIG_DIR="$HOME/.op"

if [ -z "$SSH_AUTH_SOCK" ]; then
  export SSH_AUTH_SOCK="$HOME/.ssh/1password-agent.sock"
fi

alias op-signin='eval $(op signin)'
```

Reload shell:

```bash
source ~/.bashrc
```

### Step 3: Authenticate `op` CLI

If no account is configured yet:

```bash
op account add
```

Test:

```bash
op account list
op vault list
op whoami
```

### Windows notes from the 2026-04-12 live re-test

- Logan's desktop already had a saved CLI account:
  - `my.1password.com`
  - `loganfinney27@gmail.com`
- The sandboxed shell produced a misleading pipe denial, but the live desktop context could still access vaults and items outside the sandbox.
- `op whoami` may still report `account is not signed in` even when `op vault list` and `op item get` succeed through the live desktop path.
- Do not assume the live vault is literally named `IDAHO-VAULT`; check `op vault list` and use the real visible vault name.

### Step 4: Register SSH Key in 1Password

Assumption: an SSH key item such as `GitHub SSH Key` exists in 1Password.

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

- Open 1Password
- Settings
- Developer
- Toggle `SSH Agent` on

Create/edit `~/.ssh/config`:

```
Host github.com
  AddKeysToAgent yes
  IdentityAgent ~/.ssh/1password-agent.sock
  IdentityFile ~/.ssh/id_github
```

### Step 5: Configure Git Signing

```bash
git config --global gpg.format ssh
git config --global user.signingkey "ssh-ed25519 XXXXXXX..."
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.ssh.program "ssh-keygen"
```

### Step 6: Test Git Signing

```bash
cd /path/to/IDAHO-VAULT
git commit --allow-empty -m "Test signed commit"
git log --show-signature
```

---

## Part 2: GitHub Actions Integration

### Step 1: Create Service Account in 1Password

A service account token is a distinct credential type — created in the 1Password web console under **Developer Tools**, not as a regular vault item. During creation, 1Password shows the token once and offers a **Save in 1Password** button that saves a copy of the token value into a vault item for later retrieval. This is a convenience backup, not the authoritative storage location; the service account itself lives in Developer Tools.

1. Go to `1password.com` → **Developer Tools** → **Service Accounts**
2. Click **New Service Account**, give it a name (e.g., `idaho-vault-github-actions`)
3. Grant it **Read** access to the relevant vault(s)
4. Click **Save in 1Password** — saves a copy of the token into your vault so you can retrieve it later
5. Copy the token value and add it to GitHub Secrets (Step 2 below)

### Step 2: Add Secret to GitHub

In GitHub repo settings (`github.com/loganfinney27/IDAHO-VAULT/settings/secrets/actions`):

**New secret:** `OP_SERVICE_ACCOUNT_TOKEN`  
**Value:** (paste token from Step 1 — or retrieve from 1Password if saved there)

### Step 3: Update Workflow to Fetch Secrets

```yaml
name: Example Job with 1Password

on: [push]

jobs:
  use-secrets:
    runs-on: ubuntu-latest
    # 1Password CLI v2 reads OP_SERVICE_ACCOUNT_TOKEN from the environment;
    # no explicit signin step needed.
    env:
      OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      
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

Create these items in the appropriate visible vault from `op vault list`:

| Item Name | Type | Usage | Status |
| --- | --- | --- | --- |
| `GitHub Personal Access Token` | Password | GitHub API calls, Linear sync | Create |
| `GitHub SSH Key` | SSH Key | Git commits, pushes | Create |
| `Linear API Key` | Password | Linear workspace sync | Migrate (currently in GitHub Secrets) |
| `Idaho Legislature API Key` | Password | Scraper authentication | Create |
| `Email SMTP Credentials` | Password | Budget tracker email | Create |

### How to Add a Secret

```bash
op item create --category=login \
  --title="Secret Name" \
  --vault="Visible Vault Name" \
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
| --- | --- |
| `op: command not found` | Add 1Password to PATH; check `echo $PATH` |
| SSH agent socket error | Ensure 1Password desktop app running + SSH Agent enabled in settings |
| Git signing fails | Verify `git config gpg.format ssh` and key fingerprint matches |
| GitHub Actions auth fails | Check `OP_SERVICE_ACCOUNT_TOKEN` is set and valid |
| Vault not found | Run `op vault list` to see available vaults; use correct vault name in commands |

---

## References

- 1Password CLI docs
- 1Password SSH agent docs
- GitHub SSH signing docs

---

**Next:** verify the exact secret path you need with `op item get`, then test the dependent external API from the same live desktop context.
