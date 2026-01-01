---
name: ssh-key-provenance-interim
description: All three SSH keys on the Mac are unapproved provenance; vaultlink provisionally authorized until Logan mints replacements
metadata: 
  node_type: memory
  type: project
  originSessionId: 5b93948e-edf3-4015-a8d6-73371cd51784
  modified: 2026-09-06T10:09:54.823Z
---

As of 2026-09-06, every SSH credential on the Mac (logans-mbp) is of agent or
unknown origin — none match the keys Logan kept in 1Password, and none were
approved by him:

- **Pair A** `.ssh/id_ed25519` (+.pub), May 23, comment `logan@Logans-MBP.ht.home`,
  SHA256:5mbheu2Eky5znb3gqSaLxImWQ3eHxVu8SoaQ1hFDEbw — referenced by `.ssh/config`, unproven.
- **Pair B** `.ssh/id_ed25519 copy` (+.pub copy), Aug 12, no comment,
  SHA256:S9oYMCdV3wEzLqg2eBa6yaipDzLmBiflDAA+TVueAWI — fully unattributed, no known dependency.
- **vaultlink** `vaultlink-zbfury-to-mac-20260830` in `.ssh/authorized_keys`
  (private half on zbfury), SHA256:B0HR6cbHxdFCjgYHhQRblCzc2WIRMXVhFtCqebx/+zU —
  agent-minted; "vaultlink" is NOT Logan-approved terminology. Functional (used
  for the .gitflow scp deliveries 2026-09-04).

**Standing decision (Logan, 2026-09-06):** the vaultlink key MAY be used for
zbfury↔Mac transfers *until* Logan mints his own keys (stored in 1Password),
installs them deliberately, and retires all three. Do not treat any of these as
permanent; do not enshrine their fingerprints in tracked vault files.

**Why:** functional-but-unapproved credentials need a deliberate ratify/retire
decision; Logan chose interim use with planned replacement.
**How to apply:** use vaultlink for cross-machine transfers when needed; expect
all three keys to disappear when Logan does the key reset; never add new keys or
authorized_keys entries without his explicit direction. See [[vault-repo-hazards]],
[[agent-failure-patterns]].
