# Git Commit Signing via 1Password SSH Agent

**Scope:** Local developer machines (Windows + macOS) — companion to `.op/SETUP.md`
**Status:** Active — wired 2026-05-27 on the Windows host (loganf)
**Updated:** 2026-05-27
**Authority:** LOGAN

---

## Goal

Sign every git commit made from any of Logan's local machines with the SSH
key stored as the "GitHub" item in 1Password's "Vault" vault. This satisfies
the Main Ruleset's `required_signatures` rule without:

- Storing the private key in `~/.ssh/`
- Requiring per-machine GPG agent setup
- Needing to remember `-S` on every commit

The structural problem this addresses: prior to 2026-05-27, local commits
from cmd/Git-Bash on Windows produced unsigned commits ("N" in `git log
%G?`). The merge queue could not accept them because `required_signatures`
gated every commit in the PR. The only commits that satisfied the rule
were GitHub server-side `web-flow` merge commits produced by clicking
Merge in the web UI — which made everything a "click in the browser"
workflow. This setup makes file-editor and CLI commits sign automatically.

---

## Prerequisites

- 1Password app (desktop) installed and signed in
- The SSH signing key exists as a 1Password item titled `"GitHub"` in the
  `"Vault"` vault (or wherever Logan stores it; vault and item name are
  referenced from `agent.toml`)
- `op` CLI installed and signed in (see `.op/SETUP.md`)
- 1Password's built-in SSH Agent enabled in app settings
  (**Settings → Developer → Use the SSH Agent**)

No administrative access required for any step below.

---

## Per-machine recipe

### Step 1: tell the 1Password SSH agent which key to expose

By default the agent only exposes keys from the Personal/Private vault.
The "GitHub" key lives in the "Vault" vault, so the agent must be told to
include it.

Edit the agent's config file:

| OS | Path |
|---|---|
| Windows | `%LOCALAPPDATA%\1Password\config\ssh\agent.toml` |
| macOS | `~/.config/1Password/ssh/agent.toml` |

Append:

```toml
[[ssh-keys]]
item = "GitHub"
vault = "Vault"
```

Item-scoped (not vault-wide) keeps the surface narrow — only this one
key is offered to the agent, nothing else from the Vault vault.

**Restart 1Password app** (or toggle SSH Agent off/on in Settings →
Developer) so the new config is loaded.

Verify with the system OpenSSH client:

| OS | Command |
|---|---|
| Windows | `"C:\Windows\System32\OpenSSH\ssh-add.exe" -L` |
| macOS | `ssh-add -L` |

Should print the `ssh-ed25519 AAAA... GitHub` line. If not, the toml
wasn't picked up — re-verify the path and restart 1Password.

### Step 2: configure git (global, all repos)

```bash
git config --global gpg.format ssh
git config --global gpg.ssh.program "<absolute path to system OpenSSH ssh-keygen>"
git config --global user.signingkey "key::ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... GitHub"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

The `gpg.ssh.program` path is critical on Windows: Git Bash ships its
own `/usr/bin/ssh-keygen` that does NOT know how to talk to Windows's
named-pipe SSH agent. Only the system OpenSSH at
`C:\Windows\System32\OpenSSH\ssh-keygen.exe` does.

| OS | `gpg.ssh.program` value |
|---|---|
| Windows | `C:/Windows/System32/OpenSSH/ssh-keygen.exe` |
| macOS | `/usr/bin/ssh-keygen` (Apple-shipped) |

`user.signingkey` uses the `key::` prefix to embed the public key string
inline (so git knows to verify against it without needing a file path
that varies per machine). Fetch the value from 1Password:

```bash
op item get GitHub --fields "public key" --reveal
```

### Step 3: configure verification (so local `git log %G?` shows `G`)

Even with a valid signature, git won't show `G` (good) unless it has an
`allowedSignersFile` mapping the signature back to a known signer.

```bash
# Write the allowed-signers file (one line per signer/key)
echo "loganfinney27@gmail.com namespaces=\"git\" $(op item get GitHub --fields 'public key' --reveal)" \
  > ~/.ssh/allowed_signers
git config --global gpg.ssh.allowedSignersFile "<absolute path to ~/.ssh/allowed_signers>"
```

| OS | path value |
|---|---|
| Windows | `C:/Users/<user>/.ssh/allowed_signers` |
| macOS | `~/.ssh/allowed_signers` |

This file is local-verification only — GitHub does its own verification
server-side using its own registry of your signing keys (Step 4).

### Step 4: register the public key as a SIGNING KEY on GitHub

GitHub treats SSH **Authentication** keys and SSH **Signing** keys as
separate categories. Even if your key is already registered as an Auth
key (for git push), it must ALSO be registered as a Signing key for
commit-signature verification to succeed.

UI path: https://github.com/settings/ssh/new → set the **Key type**
dropdown to **Signing Key** before pasting and saving.

Or via `gh` CLI (one-time scope refresh, then add):

```bash
gh auth refresh -h github.com -s admin:ssh_signing_key
gh api user/ssh_signing_keys \
  -f title="1Password GitHub Signing Key" \
  -f key="$(op item get GitHub --fields 'public key' --reveal)"
```

Once registered, GitHub's API reports `signature.state: VALID` for new
commits (was `UNKNOWN_KEY` before the registration). The `required_signatures`
ruleset rule then passes.

---

## Verification end-to-end

```bash
cd <any repo with required_signatures rule>
git commit --allow-empty -m "test signing"
git log -1 --pretty=format:"%H %G? %GS"
# Expected: <sha> G loganfinney27@gmail.com
```

GitHub-side check after push:

```bash
gh api graphql -f query='{ repository(owner:"LAF-US",name:"<repo>"){ pullRequest(number:<n>){ commits(last:1){ nodes{ commit{ signature{ isValid state } } } } } } }'
# Expected: signature: {isValid: True, state: VALID}
```

---

## Troubleshooting recipes

### `gpg: skipped "...": No secret key`
Git is invoking GPG instead of SSH signing. Confirm `gpg.format=ssh` is
set at the active scope (`git config --get gpg.format`).

### `error: Couldn't get agent socket?`
Git is invoking the wrong `ssh-keygen` — typically the MSYS2 version
that ships with Git Bash. Confirm `gpg.ssh.program` points at the system
OpenSSH binary (see table in Step 2).

### `error: 1Password: failed to fill whole buffer`
`op-ssh-sign` IPC handshake with the 1Password agent failed. Usually
means the agent isn't running, the app is locked, or the `agent.toml`
edit wasn't picked up. Restart the 1Password app and retry.

### `1Password: failed to fill whole buffer` + `Make sure the SSH key is saved in your Personal or Private vault`
The `agent.toml` doesn't list the vault holding the key. Re-check Step 1.

### `signature.state: UNKNOWN_KEY` on GitHub
The signing key is registered as Authentication but not Signing on
GitHub. See Step 4.

### Commits sign but pre-existing unsigned commits in PR still block
Required-signatures rules apply to EVERY commit in the PR, not just the
HEAD. To re-sign a series of unsigned commits already on a branch:

```bash
git rebase -f origin/main
```

With `commit.gpgsign=true` globally, the rebase re-creates each commit
and each gets signed.

---

## What was wired tonight (2026-05-27, Windows host)

- `agent.toml` extended with `[[ssh-keys]] item = "GitHub" vault = "Vault"`
- Five global git config lines set per Step 2 above
- `allowed_signers` file at `C:/Users/loganf/.ssh/allowed_signers` per Step 3
- Public key registered as Signing Key on GitHub (Logan, manually via UI)

The setup unblocked PR #390 (merged 2026-05-28T05:31:58Z), which itself
landed the merge_group: trigger additions to the required-check
workflows — without which the merge queue could never have completed a
queue cycle, signing or no.

---

## See also

- `.op/SETUP.md` — base 1Password CLI + SSH Agent install
- `.op/secrets.template.md` — credential inventory
- `.github/workflows/codeql.yml` — companion CodeQL matrix discipline
  (see PR #390 commit messages for the matrix-vs-history alignment story)
- `CONSTITUTION.md` — Main Ruleset including `required_signatures`
