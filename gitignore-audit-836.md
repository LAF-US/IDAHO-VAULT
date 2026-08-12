# Audit: .gitignore (issue #836)

Commands run:

- git check-ignore -v -- .idaho-vault-signing-gate-build-tools/

.gitignore:21:	.idaho-vault-signing-gate-build-tools/


- git status --short --ignored -- .idaho-vault-signing-gate-build-tools/



- git check-ignore -v -- INBOX/PHONE-LINK/test.txt



.gitignore (current):

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



Findings:

- Searched for vestigial ignore patterns referenced in issue #836.
- The above command outputs show whether the patterns are currently matched by any ignore rule.

Recommendations / next steps:
- If any ignore rules remain and are vestigial, remove them in a follow-up patch and record reasoning here.
- If no vestigial rules exist, close issue #836 with this audit attached.

