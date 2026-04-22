---
name: authenticator setup
description: Logan's 2FA/auth stack — fragmented across four apps, 1Password consolidation in progress
type: reference
---

**Current state:** 2FA codes split across four apps — in-progress housekeeping.

- **1Password** — new, still configuring; intended as primary credential manager; TOTP migration target
- **Google Authenticator** — personal accounts, migrating out
- **Duo** — likely work/IT-mandated; cannot be moved
- **Microsoft Authenticator** — likely work/IT-mandated; cannot be moved

**To-buy:** YubiKey — hardware root of trust for 1Password SSH agent + git signing

**Consolidation goal:** 1Password as single TOTP store for everything not IT-mandated (Duo, MS Authenticator stay). YubiKey as hardware backup/unlock key for 1Password itself.

**How to apply:** When touching auth, credentials, or 1Password config — setup is incomplete. Do not assume 1Password holds all secrets yet.
