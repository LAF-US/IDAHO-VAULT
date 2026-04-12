# 1Password CLI & SSH Agent Setup

**Scope:** Local developer machine + GitHub Actions integration  
**Status:** Template with desktop reality notes from 2026-04-12  
**Updated:** 2026-04-12

---

## Part 1: Local Installation (Developer Machine)

### Prerequisites

- Windows 11 Pro
- Git Bash installed (`C:\Program Files\Git\bin\bash.exe`)
- 1Password desktop app installed
- Administrative access on machine

### Step 1: Install 1Password CLI

**Option A: Scoop**

```bash
scoop install 1password
op --version
```

**Option B: Homebrew**

```bash
brew install 1password-cli
```

**Option C: Manual download**

Download from the 1Password CLI release page and add it to `PATH`.

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

If an account already exists and just needs re-auth:

```bash
op signin --account my.1password.com
```

Verification sequence:

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

```bash
op item get "GitHub SSH Key" --fields private_key --format json | jq -r '.value' > /tmp/gh_key
ssh-keygen -l -f /tmp/gh_key
rm /tmp/gh_key
```

Enable SSH agent in the 1Password desktop app:

- Open 1Password
- Settings
- Developer
- Toggle `SSH Agent` on

Configure `~/.ssh/config`:

```text
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
git config --global gpg.ssh.program "ssh-keyscan"
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

Create a password item:

- Name: `GitHub Actions Service Account`
- Password: generated token or existing `OP_SERVICE_ACCOUNT_TOKEN`

Retrieve token:

```bash
op item get "GitHub Actions Service Account" --fields password
```

### Step 2: Add Secret to GitHub

Add `OP_SERVICE_ACCOUNT_TOKEN` to GitHub repo secrets.

### Step 3: Update Workflow to Fetch Secrets

```yaml
- name: Authenticate 1Password
  run: |
    echo "${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}" | op signin --raw

- name: Fetch secret from 1Password
  run: |
    SECRET=$(op item get "GitHub Personal Access Token" --fields password)
    echo "::add-mask::$SECRET"
```

---

## Part 3: Vault Secret Inventory

Create these items in the appropriate visible vault from `op vault list`:

| Item Name | Type | Usage | Status |
|---|---|---|---|
| `GitHub Personal Access Token` | Password | GitHub API calls | Create or migrate |
| `GitHub SSH Key` | SSH Key | Git commits and pushes | Create or import |
| `Linear API Key` | Password | Linear workspace sync | Migrate |
| `Idaho Legislature API Key` | Password | Scraper auth | Create if needed |
| `Email SMTP Credentials` | Password | Budget tracker email | Create if needed |
| `what3words` | API Key | what3words desktop / CLI lookup | Verified live item in vault `Vault` |

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
|---|---|
| `op: command not found` | Add 1Password CLI to `PATH` |
| `Access is denied` from the desktop pipe | Re-test outside the sandbox or isolated shell before assuming local 1Password is broken |
| `op whoami` says not signed in | Check `op account list` and `op vault list`; the live desktop path may still have usable vault access |
| Vault not found | Run `op vault list` and use the real visible vault name instead of assuming `IDAHO-VAULT` |
| Secret item not found | Verify the item title and vault in the desktop app, then mirror that exact path in CLI commands |

---

## References

- 1Password CLI docs
- 1Password SSH agent docs
- GitHub SSH signing docs

---

**Next:** verify the exact secret path you need with `op item get`, then test the dependent external API from the same live desktop context.
