---
date created: Monday, March 30th 2026, 5:17:09 pm
date modified: Sunday, April 12th 2026, 1:35:00 am
status: active
authority: Claude Code (The Abhorsen)
related:
- '2026-03-30'
- '2026-04-12'
- AGENTS
- CLAUDE
- CLI
- CONSTITUTION
- GitHub
- Logan's
- SSH
- VAULT-CONVENTIONS
- what3words
- agent
- infrastructure
- template
---
# 1Password Integration - IDAHO-VAULT

**Status:** Infrastructure template deployed; local desktop reality now partially verified  
**Scope:** CLI + SSH agent (developer machines) + secret injection (GitHub Actions)  
**Updated:** 2026-04-12

---

## What This Is

IDAHO-VAULT has a documented 1Password integration layer for:

1. Developer machines - 1Password CLI + SSH agent for git signing and local secret access
2. GitHub Actions - service account token plus runtime secret fetching via `op item get`
3. Credential inventory - a durable record of secret expectations and rotation

---

## Files Deployed

| File | Purpose |
|---|---|
| `.op/SETUP.md` | Installation and configuration guide for developer machines |
| `.op/secrets.template.md` | Secret inventory, rotation schedule, and emergency procedures |
| `.github/workflows/1password-secret-template.yml` | Example workflow using 1Password for secret injection |
| `1Password.md` | Integration summary and current desktop findings |

---

## 2026-04-12 Desktop Verification

The local re-test from this machine established the following:

- `op` is installed and healthy:
  - version `2.33.1`
- A saved CLI account exists:
  - URL: `my.1password.com`
  - email: `loganfinney27@gmail.com`
  - user id: `X6OLMRVXDJAI3EGF7ITRFLFMDM`
- The sandboxed shell produced a false-looking first symptom:
  - `connecting to desktop app ... Access is denied`
- Re-running outside the sandbox clarified the real state:
  - `op account list` works
  - `op vault list` works
  - `op item get` works for at least one live secret
  - `op whoami` still reports `account is not signed in`

Visible vaults from the live desktop context:

- `Private`
- `Personal`
- `Vault`
- `Wallet`
- `Work`

Important correction:

- the live desktop account does **not** expose a vault literally named `IDAHO-VAULT`

That means the earlier documentation was too abstract. The local 1Password setup is not simply "broken," but the repo was assuming a vault name and sign-in state that do not match the current desktop context.

---

## what3words Secret Path

The local what3words credential was positively identified in 1Password:

- vault: `Vault`
- item: `what3words`
- field: `credential`
- username field value: `IDAHO-VAULT`

The secret can be fetched successfully from the live desktop context.

This matters because it rules out the earlier fear that 1Password could not supply the what3words key at all.

---

## Current Diagnostic Reading

The what3words failure is a two-layer story:

1. **1Password context**
   - local `op` access exists, but the CLI sign-in state is not cleanly represented by `op whoami`
   - the old assumption that the live vault is named `IDAHO-VAULT` is wrong

2. **what3words API behavior**
   - after fetching the live secret from 1Password, a direct API probe to `convert-to-3wa` returned `HTTP 401`
   - screenshot evidence in `!/INBOX/images/2026-04-11-screenshot-2026-04-11-204911.jpg` still shows the key is restriction-enabled

Operational rule:

- do not blame 1Password first if the sandbox is involved
- verify the real desktop `op` path and real vault/item name
- then test the external API

That sequence now shows:

- secret retrieval works
- API call still fails

So the remaining blocker is now best read as a what3words credential policy, restriction, or entitlement issue rather than a missing 1Password secret.

---

## Integration Status

| Component | Status | Notes |
|---|---|---|
| 1Password CLI template | complete | `.op/SETUP.md` exists |
| SSH agent configuration docs | complete | documented, not re-tested in this session |
| Git signing docs | complete | documented, not re-tested in this session |
| Service account flow | complete | template exists |
| Workflow template | complete | `.github/workflows/1password-secret-template.yml` |
| Secret inventory | complete | `.op/secrets.template.md` |
| Local CLI installation | verified | `op 2.33.1` present |
| Local account discovery | verified | `my.1password.com` / `loganfinney27@gmail.com` |
| Live vault naming assumption | corrected | no literal `IDAHO-VAULT` vault |
| what3words secret path | verified | `Vault / what3words / credential` |
| what3words API success | blocked | direct probe returned `HTTP 401` |

---

## Other OP Workflows Checked

The repo now shows three distinct 1Password workflow patterns:

1. `!/agent.sh`
   - local bootstrap path for agent sessions
   - previously treated `op whoami` as the only success condition
   - now adjusted to accept live `op vault list` access as a usable desktop-auth fallback when `op whoami` lies

2. `.github/workflows/linear-pr-sync.yml`
   - guarded correctly with `if: env.OP_SERVICE_ACCOUNT_TOKEN != ''`
   - already has a GitHub Secrets fallback for `LINEAR_API_KEY`

3. `.github/workflows/vault-courier.yml`
   - depends on `1password/load-secrets-action@v4` to fetch `op://vault-operations/idaho-vault-courier-key/credential`
   - did not previously guard the load step when `OP_SERVICE_ACCOUNT_TOKEN` was missing
   - now fails early with a direct message instead of letting the 1Password action fail opaquely

Important distinction:

- the local desktop path and the GitHub Actions service-account path are not the same thing
- local desktop testing exposed visible vaults like `Vault`, `Private`, and `Work`
- the workflows still intentionally reference `op://vault-operations/...` for CI
- that means a local mismatch in visible vault names does **not** automatically mean the GitHub Actions secret references are wrong

---

## Failing Process Signals

The live 1Password process and log check on `2026-04-12` showed:

- several old `1Password` and `1Password-BrowserSupport` processes still running from `2026-04-09` and `2026-04-10`
- fresh `1Password.exe` launches at approximately `2026-04-12 01:27:41` and `2026-04-12 01:32:33`
- repeated native-messaging `EndConnection` errors in `1Password_r00032.log`
- one `process tree is empty` SSH/session error
- repeated `BiometryUnavailable` warnings
- a fresh log line saying `1Password is already running, closing`

Current reading:

- there is evidence of noisy desktop-bridge churn
- there is evidence of duplicated or lingering 1Password processes
- there is **not** strong evidence here that the what3words secret path itself is failing
- the process noise helps explain why `op whoami` is not a reliable single probe on this machine

---

## Handoff

1Password is no longer the primary suspected blocker for what3words lookups on this machine.

The durable next question is the what3words key itself:

- restriction model
- allowed client type
- endpoint entitlement
- whether a separate server/CLI key should exist
