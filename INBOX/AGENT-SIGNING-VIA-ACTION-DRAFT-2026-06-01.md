# AGENT SIGNING VIA `anthropics/claude-code-action` — Recipe DRAFT

> **CORRECTION (2026-06-24).** An earlier header WITHDREW this recipe on the premise that *"1Password is NOT a sustainable secret-source for this vault."* **That premise is false and is retracted.** 1Password is the vault's credential backbone — `CLAUDE.md` § 1Password Integration makes it the centralized secret store and the configured git-signing SSH agent; `OP_SERVICE_ACCOUNT_TOKEN` is provisioned in repo Secrets (`.op/secrets.template.md`, 2026-06-17); and Logan signs commits daily with the 1Password SSH agent. The secret-**source** (1Password) is therefore settled, and this design is **live**, not "overreach."
>
> What remains genuinely open is held under LOGAN's gate: activation, trigger model, the canonical vault + signing-key item, whether `claude-code-action` re-signs existing commits, and pinning the Action. Those are flagged below.

---

*Originally filed 2026-06-01 by `!socrates.claude.novice` as a proposal-marginalia draft; reworked 2026-06-24 (false-premise withdrawal retracted; cruft/regressive edits stripped; rebased onto current `main`). Companion to the workflow draft at `.github/workflows/claude-sign.yml`. Authority: LOGAN.*

---

## Goal

Provide a server-side signing path for chamber-authored commits so they satisfy the Main Ruleset's `required_signatures` rule (Gate A in Plan v5). The path uses **`anthropics/claude-code-action`** with an `ssh_signing_key` fetched from 1Password at CI time — the same path that produced PR #400's verified-as-`Claude` commits (per `!claude.abhorsen.waiting`'s signal `!/SIGNALS/SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md`).

This recipe **does not** require any local SSH key on the chamber's Windows or Mac machine. The signing happens in CI. Local commits remain unsigned-as-Claude; the workflow re-signs (or signs new commits) server-side.

## Architectural question — UNVERIFIED

The chamber has not yet verified from primary documentation whether `claude-code-action` can:

- **(A) Amend and sign existing commits** on a branch checked out in the workflow (the "rescue" use case for the cohort of currently-unsigned chamber branches), OR
- **(B) Only sign new commits** that the Action itself produces during the workflow run (the "Claude-runs-in-CI" use case)

If (A) is supported: the workflow takes existing unsigned chamber branches and signs them.

If only (B) is supported: a different path is needed. Options:
- The chamber operates differently going forward: drafts work locally, triggers a workflow that has Claude reproduce the work in CI (and commit signed). Cumbersome.
- Logan accepts a one-time "rescue" of historical branches via local re-signing with a key that IS registered, then future commits go through CI.

**This question requires Architect-tier investigation** of `claude-code-action`'s actual API.

## Prerequisites (Architect-tier setup)

Before the workflow at `.github/workflows/claude-sign.yml` can run successfully:

1. **GitHub Repo Secret** `OP_SERVICE_ACCOUNT_TOKEN` is configured — confirmed in place (`.op/secrets.template.md`, provisioned 2026-06-17; the existing `1password-secret-template.yml` uses it).
2. **1Password vault item** containing the SSH private key for Claude commit signing:
   - **Vault + item are LOGAN's to name.** Verified 2026-06-24, three names are in play and need reconciling: the WORKING `1password-secret-template.yml` references `op://vault-operations/...`; `.op/secrets.template.md` documents vault **"IDAHO-VAULT"** with SSH item **"GitHub SSH Key"**; the workflow draft used placeholder `op://Vault/claude-code-signing-key/...`. (Note: `vault-operations` is the *working* reference, not "legacy" as an earlier draft asserted.)
   - Decide: does Claude sign with its **own** new item, or the existing **"GitHub SSH Key"**?
   - Fields: `private-key` (the SSH private key)
3. **GitHub Signing Key registration**: the public key corresponding to the 1Password-stored private key must be registered as an SSH **Signing Key** (not just an Auth key) on a GitHub account whose commits will read as `Claude`. The exact account is LOGAN's choice — `loganfinney27` (would read as Logan unless `bot_id`/`bot_name` overrides), or a dedicated bot account.
4. **1Password vault item** for bot identity (if using a non-default `bot_id`/`bot_name`): item + fields (`bot-id`, `bot-name`) — names TBD by LOGAN.
5. **Workflow file activation**: `.github/workflows/claude-sign.yml` present on `main` and enabled in repo Settings → Actions.
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

- **`.github/workflows/1password-secret-template.yml`** — the working template for `OP_SERVICE_ACCOUNT_TOKEN` + `load-secrets-action@v4` (references `op://vault-operations/...`). The new workflow extends this pattern.
- **`.op/SETUP.md`** — 1Password CLI + SSH-agent signing setup recipe.
- **`.op/secrets.template.md`** — credential inventory (vault "IDAHO-VAULT", item "GitHub SSH Key"); would need a new entry for the Claude signing-key item if a dedicated one is created.
- **`cryptic-bouncing-cake.md` Plan v5** — the operational plan this recipe implements (Phase A.2-revised).
- **`!/SIGNALS/SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md`** — the AiW signal that named this server-side path.

## What this recipe does NOT do

- Does not install or activate the workflow (Architect's act)
- Does not create the 1Password vault items (Architect's act + 1Password-side setup)
- Does not register any SSH Signing Key on any GitHub account (Architect's act)
- Does not resolve the architectural question (A vs B) above — that requires reading `anthropics/claude-code-action`'s primary documentation
- Does not claim the workflow as-drafted will work without verification — it may need adjustment based on the Action's actual API

## Standing

The chamber's standing in this recipe: novice, proposing-marginalia. The drafts on this branch are for LOGAN to read, redirect, or activate. The activation is yours.

###### [["The world is quiet here."]]

*— Recipe DRAFT filed 2026-06-01 by Socrates (`!socrates.claude.novice`); reworked 2026-06-24.*
