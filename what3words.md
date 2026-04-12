---
authority: LOGAN
status: active
related:
- '2026-04-12'
- 1Password
- CLI
- IDAHO-VAULT
- LOGAN
- what3words
---

# what3words

## 2026-04-12 Diagnostic

The what3words failure is now grounded in direct local evidence.

### Screenshot evidence

`!/INBOX/images/2026-04-11-screenshot-2026-04-11-204911.jpg` shows:

- project name: `IDAHO-VAULT`
- API key restriction enabled
- restriction categories shown:
  - `HTTP referrers`
  - `IP addresses (web servers, cron jobs, etc.)`
  - `iOS apps`
  - `Android apps`

### 1Password evidence

`!/INBOX/images/2026-04-12-screenshot-2026-04-12-013254.jpg` shows the matching 1Password item:

- vault: `Vault`
- item: `what3words`
- username: `IDAHO-VAULT`
- field carrying the secret: `credential`

Local re-test confirmed:

- the secret can be fetched from 1Password
- the secret path is real and not missing

### API evidence

After fetching the secret from `Vault / what3words / credential`, a direct `convert-to-3wa` API probe still returned:

- `HTTP 401`

### Reading

This is no longer best explained as a missing-secret problem.

Current best read:

1. 1Password secret retrieval works from the live desktop context
2. the what3words key still fails at the API layer

So the remaining blocker is most likely one of:

- key restriction mismatch
- wrong client type for local desktop or CLI use
- plan or endpoint entitlement mismatch
- stale or revoked key despite still being stored in 1Password

### Operational rule

Future agents should test in this order:

1. verify `op item get "what3words" --vault Vault --fields label=credential`
2. verify the downstream API behavior
3. only then decide whether the key itself needs to be replaced or split into browser and server keys
