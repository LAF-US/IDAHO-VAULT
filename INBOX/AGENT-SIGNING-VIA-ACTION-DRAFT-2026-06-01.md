# AGENT SIGNING VIA `anthropics/claude-code-action` — Recipe DRAFT (WITHDRAWN)

> **WITHDRAWN 2026-06-01.** This recipe was built on 1Password as the secret-source for the signing key (load-secrets-action + OP_SERVICE_ACCOUNT_TOKEN + op://Vault/... references). LOGAN's catch the same day: **1Password is NOT a sustainable secret-source for this vault** — the CLI is only installed on Logan's work-computer, and the whole integration chain inherits that fragility. I had been told this previously and did not retain it.
>
> The broader architecture (server-side via `anthropics/claude-code-action`) may still hold; only the **1Password secret-source picker is wrong**. The replacement path (GitHub Secrets stored directly / GitHub Environments / HashiCorp Vault / AWS Secrets Manager / self-hosted runner with key on disk / something else) requires LOGAN to name what is sustainable.
>
> **Do not activate.** Plan v5 in `cryptic-bouncing-cake.md` has been corrected to reopen the secret-source question as `*`. This file is preserved as historical evidence of the overreach.

---

*Originally filed 2026-06-01 by `!socrates.claude.novice` as a proposal-marginalia draft. Companion to the workflow draft at `.github/workflows/claude-sign.yml` (also WITHDRAWN). Authority: LOGAN. Status: DRAFT in INBOX/ — WITHDRAWN before LOGAN's gate. `.op/` is Logan's 1Password-curated operational space; the chamber has no standing to position docs there.*

---

## Goal

Provide a server-side signing path for chamber-authored commits so they satisfy the Main Ruleset's `required_signatures` rule (Gate A in Plan v5). The path uses **`anthropics/claude-code-action`** with an `ssh_signing_key` fetched from 1Password at CI time — the same path that produced PR #400's verified-as-`Claude` commits (per `!claude.abhorsen.waiting`'s signal `!/SIGNALS/SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md`).

This recipe **does not** require any local SSH key on the chamber's Windows or Mac machine. The signing happens in CI. Local commits remain unsigned-as-Claude; the workflow re-signs (or signs new commits) server-side.

## Architectural question — UNVERIFIED

The chamber has not yet verified from primary documentation whether `claude-code-action` can:

- **(A) Amend and sign existing commits** on a branch checked out in the workflow (the "rescue" use case for the cohort of currently-unsigned chamber branches), OR
- **(B) Only sign new commits** that the Action itself produces during the workflow run (the "Claude-runs-in-CI" use case)

If (A) is supported: the workflow takes existing unsigned chamber branches and signs them. Tonight's 20 unsigned chamber branches can each be re-signed.

If only (B) is supported: a different path is needed. Options:
- The chamber operates differently going forward: drafts work locally, triggers a workflow that has Claude reproduce the work in CI (and commit signed). Cumbersome.
- Logan accepts a one-time "rescue" of historical branches via local re-signing with a key that IS registered (the test from `test/tier2-signing-2026-05-29` showed the chamber's current key is NOT registered — LOGAN would register it, then chamber re-signs locally, then never again because future commits go through CI).

**This question requires Architect-tier investigation.** The chamber can draft based on (A) as the optimistic assumption; (B) requires the alternative paths above.

## Prerequisites (Architect-tier setup)

Before the workflow at `.github/workflows/claude-sign.yml` can run successfully:

1. **GitHub Repo Secret** `OP_SERVICE_ACCOUNT_TOKEN` is configured (per memory, this is already in place — confirmed by the existing `1password-secret-template.yml` working pattern).
2. **1Password vault item** containing the SSH private key for Claude commit signing:
   - Vault: `Vault` (canonical name per memory; legacy references to `vault-operations` need correction across `.op/SETUP.md`, `secrets.template.md`, and `1password-secret-template.yml`)
   - Item name: TBD by LOGAN (the workflow draft uses placeholder `claude-code-signing-key`)
   - Fields: `private-key` (the SSH private key)
3. **GitHub Signing Key registration**: the public key corresponding to the 1Password-stored private key must be registered as a SSH **Signing Key** (not just an Auth key) on a GitHub account whose commits will read as `Claude`. The exact account is LOGAN's choice — `loganfinney27` (Logan's personal account, which would make the commits read as Logan unless `bot_id`/`bot_name` overrides), or a dedicated bot account.
4. **1Password vault item** for bot identity (if using a non-default `bot_id`/`bot_name`):
   - Vault: `Vault`
   - Item name: placeholder `claude-bot-identity`
   - Fields: `bot-id` (numeric GitHub user ID), `bot-name` (GitHub username)
5. **Workflow file activation**: `.github/workflows/claude-sign.yml` must be present on `main` and the workflow must be enabled in repo Settings → Actions.
6. **Action version pin**: replace `@main` with a tagged release of `anthropics/claude-code-action` for stability.

## Per-session usage (after activation)

The chamber's normal flow does not change locally:
1. Open conversation with Logan
2. Read/write vault files locally
3. `git commit` locally (unsigned-as-Claude, status `U`)
4. `git push origin <branch>` (when Logan authorizes pushing)
5. (NEW) Trigger the `Claude Sign (DRAFT)` workflow via `workflow_dispatch` with the branch name
6. Workflow runs in CI, signs the branch's commits via the Action
7. PR can now satisfy Gate A and proceed through the merge queue

If trigger eventually moves to `pull_request_target`, step 5 becomes automatic on PR open.

## Verification path

After the workflow runs on a test branch:
- `gh api repos/LAF-US/IDAHO-VAULT/commits/<sha> --jq .commit.verification`
- Expected: `{verified: true, reason: "valid", verified_at: ...}`
- Expected author/committer: `Claude <noreply@anthropic.com>` (or the configured `bot_name`)

If verification reports `false` with reason `unsigned` or `unknown_key`:
- Re-check that the SSH public key is registered as a Signing Key on the GitHub account
- Re-check that the 1Password item path matches the workflow's reference
- Confirm `OP_SERVICE_ACCOUNT_TOKEN` is present in repo Secrets

## Related vault material

- **`.github/workflows/1password-secret-template.yml`** — the working template for `OP_SERVICE_ACCOUNT_TOKEN` + `load-secrets-action@v4`. The new workflow extends this pattern.
- **`.op/SETUP.md`** — 1Password setup recipe; references `IDAHO-VAULT` vault name that may need correction to `Vault`.
- **`.op/secrets.template.md`** — credential inventory; would need new entries for `claude-code-signing-key` and `claude-bot-identity` when those items exist.
- **`cryptic-bouncing-cake.md` Plan v5** — the operational plan this recipe implements (Phase A.2-revised).
- **`!/SIGNALS/SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md`** — the AiW signal that named this server-side path.
- **`!/REVIEWER-POSTURE-SURVEY-2026-06-01.md`** — adjacent reviewer-posture work; reviewer-multiplicity is a different Gate (Gate B) but related to the broader knot.

## What this recipe does NOT do

- Does not install or activate the workflow (Architect's act)
- Does not create the 1Password vault items (Architect's act + 1Password-side setup)
- Does not register any SSH Signing Key on any GitHub account (Architect's act)
- Does not modify any existing file in `.op/`, `.github/`, or vault root (only adds the workflow + this recipe)
- Does not resolve the architectural question (A vs B) above — that requires reading `anthropics/claude-code-action`'s primary documentation more carefully than this draft did
- Does not claim the workflow as-drafted will work without verification — it may need adjustment based on the Action's actual API

## Standing

The chamber's standing in this recipe: novice, proposing-marginalia. The drafts on this branch are for LOGAN to read, redirect, or activate. The activation is yours.

###### "The world is quiet here. Esto Perpetua!"

*— Recipe DRAFT filed 2026-06-01 by Socrates (`!socrates.claude.novice`).*
