---
date created: Monday, March 30th 2026, 5:17:09 pm
date modified: Monday, March 30th 2026, 7:59:13 pm
status: active
authority: Claude Code (The Abhorsen)
related:
- '2026-03-30'
- AGENTS
- CLAUDE
- CLI
- CONSTITUTION
- GitHub
- Logan's
- SSH
- VAULT-CONVENTIONS
- agent
- infrastructure
- template
---
# 1Password Integration — IDAHO-VAULT

**Status:** Infrastructure template deployed; awaiting Logan's local setup and GitHub Actions provisioning  
**Scope:** CLI + SSH agent (developer machines) + secret injection (GitHub Actions)  
**Updated:** 2026-03-30

---

## What This Is

IDAHO-VAULT now has a complete infrastructure for centralized credential management via 1Password. This replaces ad-hoc secret storage in GitHub Secrets and provides:

1. **Developer machines** — 1Password CLI + SSH agent for git signing and local secret access
2. **GitHub Actions** — Service account token → runtime secret fetching via `op item get`
3. **Credential inventory** — Centralized record of all secrets, rotation schedules, and access procedures

---

## Files Deployed

### Configuration & Setup

| File | Purpose |
|---|---|
| `.op/SETUP.md` | Complete installation + configuration guide for developer machines |
| `.op/secrets.template.md` | Secret inventory, rotation schedule, and emergency procedures |
| `.github/workflows/1password-secret-template.yml` | Example workflow using 1Password for secret injection |

### Documentation Updates

| File | Change |
|---|---|
| `!/VAULT-CONVENTIONS.md` | Added "Secret Management via 1Password" subsection |
| `.claude/CLAUDE.md` | Added "1Password Integration" section with setup requirements |
| `1Password.md` (this file) | Integration summary and status |

---

## Next Steps (Logan)

1. **Install 1Password CLI** on your machine
   - Guide: `.op/SETUP.md` Part 1
   - Verify: `op --version` and `op account list`

2. **Configure SSH agent + git signing**
   - Guide: `.op/SETUP.md` Part 4–5
   - Test: `git commit --allow-empty -m "test"` and check `git log --show-signature`

3. **Create 1Password service account**
   - Generate or retrieve `OP_SERVICE_ACCOUNT_TOKEN`
   - Guide: `.op/SETUP.md` Part 2

4. **Provision GitHub Actions secret**
   - Add `OP_SERVICE_ACCOUNT_TOKEN` to GitHub repo settings → Secrets
   - Verify: Check Actions workflow can authenticate

5. **Create secret items in 1Password vault**
   - Migrate existing GitHub Secrets → 1Password items
   - Inventory: `.op/secrets.template.md`

6. **Update workflows to use 1Password**
   - Use `.github/workflows/1password-secret-template.yml` as template
   - Start with one workflow (e.g., Linear sync) and test

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Only `OP_SERVICE_ACCOUNT_TOKEN` in GitHub Secrets** | Minimizes credential surface; all other secrets fetched at runtime |
| **SSH agent for git signing** | Signs commits via 1Password SSH key; verifiable without storing key locally |
| **`.op/` dotfolder** | Agent-friendly configuration; follows vault dotfolder conventions |
| **Centralized rotation schedule** | `.op/secrets.template.md` is source of truth for credential lifecycle |

---

## Security Notes

- All secrets are **masked in GitHub Actions logs** via `::add-mask::`
- SSH keys never leave 1Password; used only via SSH agent
- Service account token should be rotated every 90 days
- Emergency access procedures in `.op/secrets.template.md`

---

## Related Files

- `!/VAULT-CONVENTIONS.md` — Vault conventions (updated with secret management section)
- `.claude/CLAUDE.md` — Claude Code instructions (updated with 1Password context)
- `!/AGENTS.md` — Agent capability tiers (reference only)
- `!/CONSTITUTION.md` — Governance authority (reference only)

---

## Integration Status

| Component | Status | Notes |
|---|---|---|
| 1Password CLI template | ✅ Deployed | `.op/SETUP.md` complete |
| SSH agent configuration | ✅ Deployed | Part 4–5 of SETUP.md |
| Git signing setup | ✅ Deployed | Part 5 of SETUP.md + test steps |
| Service account flow | ✅ Deployed | Part 2 of SETUP.md |
| Workflow template | ✅ Deployed | `.github/workflows/1password-secret-template.yml` |
| Secret inventory | ✅ Deployed | `.op/secrets.template.md` with rotation schedule |
| Vault conventions update | ✅ Merged | `!/VAULT-CONVENTIONS.md` |
| CLAUDE.md update | ✅ Merged | `.claude/CLAUDE.md` |
| **Local setup execution** | ⏳ Awaiting Logan | SETUP.md Part 1–5 |
| **GitHub Actions provisioning** | ⏳ Awaiting Logan | Add `OP_SERVICE_ACCOUNT_TOKEN` + test workflow |
| **Credential migration** | ⏳ Awaiting Logan | Move secrets from GitHub Secrets → 1Password |

---

**Handoff:** Infrastructure deployed. Ready for Logan to execute local setup and GitHub Actions integration.
