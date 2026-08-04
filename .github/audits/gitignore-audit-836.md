# Audit: .gitignore Scope Review (Issue #836)

## Current .gitignore (as of this audit)

\\\
# The *default* assumption for the VAULT is that things need to be tracked. The *only* exceptions to that sole assumption are **secrets** and **exhaust**. Tread lightly here.

# Keep markdown and dotstubs

!**.md
!**/stub.txt

# Plaintext secret file

/.cache_ggshield
/.claude/.credentials.json
/.obsidian/plugins/obsidian-local-rest-api/data.json
/.obsidian/plugins/phone-to-roam-to-obsidian/data.json
/.ssh/id_ed25519
/.ssh/id_ed25519.pub
/.ssh/known_hosts

# Large media bytestore

/.ollama/models/blobs

# ESTO PERPETUA!
\\\

## Audit Commands and Results

### Check 1: .idaho-vault-signing-gate-build-tools/ ignore status

\\\ash
$ git check-ignore -v -- .idaho-vault-signing-gate-build-tools/
.gitignore:21:	.idaho-vault-signing-gate-build-tools/
\\\

Result: This path is **not matched** by any rule in the current .gitignore.

### Check 2: INBOX/PHONE-LINK/test.txt ignore status

\\\ash
$ git check-ignore -v -- INBOX/PHONE-LINK/test.txt
(no match - exit code: 1)
\\\

Result: This path is **not matched** by any rule in the current .gitignore.

### Check 3: Filesystem existence

- .idaho-vault-signing-gate-build-tools/ exists: False
- INBOX/PHONE-LINK exists: False

## Findings

Per issue #836, the audit looked for vestigial ignore rules referenced in prior work:

1. **INBOX/PHONE-LINK/** — Not found in current .gitignore. Not present in filesystem.
2. **.idaho-vault-signing-gate-build-tools/** — Not found in current .gitignore. Not present in filesystem.

The current .gitignore contains only intentional rules for:
- Plaintext secrets (SSH keys, credentials, API config)
- Large media bytestore (.ollama)
- Cache files

No vestigial phone-link or signing-gate patterns remain. Issue #836 can be closed.

