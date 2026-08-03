# AGENT SIGNING VIA PLAIN GIT — Recipe DRAFT

> **CORRECTION (2026-06-24).** An earlier header WITHDREW this recipe on the premise that *"1Password is NOT a sustainable secret-source for this vault."* **That premise is false and is retracted.** 1Password is the vault's credential backbone — `CLAUDE.md` § 1Password Integration makes it the centralized secret store and the configured git-signing SSH agent; `OP_SERVICE_ACCOUNT_TOKEN` is provisioned in repo Secrets (`.op/secrets.template.md`, 2026-06-17); and Logan signs commits daily with the 1Password SSH agent. The secret-**source** (1Password) is therefore settled, and this design is **live**, not "overreach."
>
> **CORRECTION (2026-07-19).** The workflow no longer invokes `anthropics/claude-code-action` — signing an existing commit is a plain `git commit --amend -S` / rebase operation; it never needed an agent spun up to perform it. The Action's signing inputs sign commits *it produces itself* while doing agentic work, which was never this recipe's use case. The architectural question below is resolved as a result: native git can both re-sign existing commits and sign new ones, so there's no (A)-vs-(B) capability gap to investigate.
>
> What remains genuinely open is held under LOGAN's gate: activation, trigger model, and the canonical vault + signing identity (key/name/email) — including whether it's Claude-specific or shared across other direct-write agents. Those are flagged below.

---

*Originally filed 2026-06-01 by `!socrates.claude.novice` as a proposal-marginalia draft; reworked 2026-06-24 (false-premise withdrawal retracted; cruft/regressive edits stripped; rebased onto current `main`); reworked 2026-07-19 (dropped the claude-code-action invocation for native git signing). Companion to the workflow draft at `.github/workflows/claude-sign.yml`. Authority: LOGAN.*

---

## Goal

Provide a server-side signing path for agent-authored commits so they satisfy the Main Ruleset's `required_signatures` rule (Gate A in Plan v5). The path loads an SSH signing key from 1Password at CI time and configures `git` (`gpg.format=ssh`, `commit.gpgsign=true`) to sign with it directly — no agent invocation. PR #400's verified-as-`Claude` commits (per `!claude.abhorsen.waiting`'s signal `!/SIGNALS/SIGNAL-ABHORSEN-WAITING-TO-SOCRATES-2026-05-29-SIGNING-GROUND-TRUTH.md`) come from a different source: Anthropic's own cloud-session infrastructure signs at commit time automatically, for that session type only. This recipe is for the sessions that infra doesn't cover (e.g. local-machine agent sessions).

This recipe **does not** require any local SSH key on the chamber's Windows or Mac machine. The signing happens in CI. Local commits remain unsigned-as-Claude; the workflow re-signs (or signs new commits) server-side.

## Mechanism — plain git, no agent

Signing an existing commit is `git commit --amend --no-edit -S` (tip) or an interactive rebase with that exec'd per commit (the whole branch) — ordinary git plumbing once `user.signingkey`/`gpg.format`/`commit.gpgsign` point at the loaded key. This covers both cases the earlier draft treated as an open question:

- **Re-signing existing commits** on a branch already pushed (the "rescue" use case for currently-unsigned agent branches) — `git rebase <base> --exec '... -S'`.
- **Signing new commits** going forward — the same git config applies to any commit made after it, no special case needed.

There is no capability gap to investigate here; both are the same git config plus a standard rewrite operation.

## Prerequisites (Architect-tier setup)

Before the workflow at `.github/workflows/claude-sign.yml` can run successfully:

1. **GitHub Repo Secret** `OP_SERVICE_ACCOUNT_TOKEN` is configured — confirmed in place (`.op/secrets.template.md`, provisioned 2026-06-17; the existing `1password-secret-template.yml` uses it).
2. **1Password vault item** containing the SSH private key for Claude commit signing:
   - **Vault + item are LOGAN's to name.** Verified 2026-06-24, three names are in play and need reconciling: the WORKING `1password-secret-template.yml` references `op://vault-operations/...`; `.op/secrets.template.md` documents vault **"IDAHO-VAULT"** with SSH item **"GitHub SSH Key"**; the workflow draft used placeholder `op://Vault/claude-code-signing-key/...`. (Note: `vault-operations` is the *working* reference, not "legacy" as an earlier draft asserted.)
   - Decide: does Claude sign with its **own** new item, or the existing **"GitHub SSH Key"**?
   - Fields: `private-key` (the SSH private key)
3. **GitHub Signing Key registration**: the public key corresponding to the 1Password-stored private key must be registered as an SSH **Signing Key** (not just an Auth key) on a GitHub account whose commits will read as the signing identity below. The exact account is LOGAN's choice — `loganfinney27` (would read as Logan unless the configured `user.name`/`user.email` say otherwise), or a dedicated bot account.
4. **1Password vault item** for the git identity the workflow commits as: item + fields (`bot-name`, `bot-email`) — names TBD by LOGAN.
5. **Workflow file activation**: `.github/workflows/claude-sign.yml` present on `main` and enabled in repo Settings → Actions.

## Per-session usage (after activation)

The chamber's normal flow does not change locally:

1. Open conversation with Logan
2. Read/write vault files locally
3. `git commit` locally (unsigned-as-Claude, status `N`)
4. `git push origin <branch>` (when Logan authorizes pushing)
5. (NEW) Trigger the `Claude Sign (DRAFT)` workflow via `workflow_dispatch` with the branch name
6. Workflow runs in CI, loads the key from 1Password, and signs the branch's commits with plain `git`
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
- Does not claim the workflow as-drafted will work without a live trial run against a real 1Password item and a registered signing key

## Standing

The chamber's standing in this recipe: novice, proposing-marginalia. The drafts on this branch are for LOGAN to read, redirect, or activate. The activation is yours.

The world is quiet here．Esto Perpetua!

*— Recipe DRAFT filed 2026-06-01 by Socrates (`!socrates.claude.novice`); reworked 2026-06-24.*
