---
authority: LOGAN
agent: Codex #318
created: 2026-06-03
observed_at: 2026-06-03T00:00:15-06:00
doc_class: status-snapshot
status: filed
tags:
  - snapshot
  - github
  - git-config
  - signing
  - arborscape
  - codex-318
related:
  - "CONSTITUTION.md"
  - "AGENTS.md"
  - "!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md"
  - "!/ARBORSCAPING-INVESTIGATION-RETURN-2026-05-24.md"
  - "https://github.com/LAF-US/IDAHO-VAULT/issues/398"
---

# Snapshot - GitHub Config, Signing, and Arborscape Connector - Codex #318 - 2026-06-03

## Scope

This is a status snapshot, not doctrine and not a configuration change.

It records the local Git/GitHub configuration state observed after the signing
gate discussion, the Arborscape connector clarification, and Logan's correction
that `.op/AGENT-SIGNING-VIA-ACTION.md` was intentionally removed and any
remaining reference to it is stale.

No credentials are recorded here.

## Local Repository State

- Repository: `C:\Users\loganf\Documents\IDAHO-VAULT`
- Remote: `https://github.com/LAF-US/IDAHO-VAULT.git`
- Observed branch: `main`
- Observed HEAD: `64a28327`
- HEAD summary: `Merge pull request #394 from LAF-US/recover/374-version-transition-policy`
- Observed status before this snapshot file was written: clean, `main...origin/main`
- Observed diff before this snapshot file was written: none

Earlier in the session, the worktree had been observed on
`claude/draft-signing-via-action-2026-06-01` with an untracked
`.github/workflows/claude-sign.yml`. At this snapshot's observation time, the
worktree reported `main` and no such untracked file in `git status --short`.
That discrepancy is recorded as observed drift, not resolved by this snapshot.

## Local Git Identity State

Global Git identity is Logan:

- `user.name=Logan Finney`
- `user.email=loganfinney27@gmail.com`
- global signing is enabled
- global signing format is SSH
- global allowed signers file: `C:/Users/loganf/.ssh/allowed_signers`

Repo-local Git identity overrides Logan with Claude:

- `user.name=Claude`
- `user.email=noreply@anthropic.com`
- `user.signingkey=C:/Users/loganf/.ssh/claude_code_signing.pub`
- `commit.gpgsign=true`
- `gpg.format=ssh`
- `gpg.ssh.program=C:/Windows/System32/OpenSSH/ssh-keygen.exe`

No `.git/config.worktree` file was present when inspected.

Interpretation: this checkout is not identity-neutral. Any ordinary commit from
this repository will attempt to use the repo-local Claude identity unless the
acting process explicitly overrides it or a worktree-specific configuration is
introduced.

## Signing Principal State

The global `allowed_signers` file maps Logan's principal and key. The
repo-local signing key is the Claude Code public key:

- Claude key fingerprint observed:
  `SHA256:hzGO9NltwHgMhjSsL62F0AWfzBZfmSjOeA8rYujOaTI`
- Claude key label observed:
  `Claude Code (Windows / loganf)`

This explains the current class of failure:

- Git can create a cryptographic SSH signature.
- Local verification can still report no matching principal.
- GitHub `required_signatures` acceptance depends on GitHub-side verified
  provenance, not merely local `Good "git" signature` output.

## GitHub CLI State

GitHub CLI was observed logged in to `github.com` as `loganfinney27`.

- Git operations protocol: `https`
- Token storage: keyring
- Scopes observed without exposing token value: `repo`, `workflow`,
  `admin:ssh_signing_key`, `gist`, `read:org`

## GitHub Control Surface State

The `.github` control surface exists and includes:

- `.github/CODEOWNERS`
- `.github/workflows/`
- `.github/scripts/`
- `.github/actions/idempotent-pr-create/action.yml`
- `.github/workflows/branch-garden-report.yml`
- `.github/scripts/branch_garden_report.py`
- `.github/scripts/issue_reconciler.py`

`CODEOWNERS` marks `.github/workflows/` and `.github/scripts/` as requiring
Logan review when branch protection enforcement is active.

## Arborscape State

Existing Arborscape machinery already handles part of the intended automation:

- branch/PR census
- idempotent recurring issue publication
- classification into `SALVAGE`, `CHERRY-PICK`, `PRUNE`,
  `LIVING_WORKTREE`, `IDENTICAL`, and `FOREIGN_HISTORY`
- non-duplication pattern for PR lookup/creation

The current gap is not the absence of Arborscape. The current gap is the missing
authorized landing connector:

`branch_garden_report.py classification -> authorized App/API signer -> deterministic salvage PR/update -> protected main`

This point was added to GitHub issue #398:

- <https://github.com/LAF-US/IDAHO-VAULT/issues/398#issuecomment-4604766340>

## Stale Reference Correction

Earlier diagnosis treated `.op/AGENT-SIGNING-VIA-ACTION.md` as missing. Logan
corrected that interpretation:

- `.op/AGENT-SIGNING-VIA-ACTION.md` was removed intentionally.
- Any remaining reference to it is stale.

Corrected interpretation: a workflow or draft that cites that file contains
stale documentation residue. The removed file is not a missing required
dependency.

The signing-draft concern that remains is separate: any claim that an action can
re-sign existing branch commits still requires verification before being treated
as a working solution.

## Current Bottleneck

The bottleneck is landing provenance at branch-garden scale.

The Vault should preserve branch history as evidence while landing selected
payload through a GitHub-verified, ruleset-accepted signer. Rewriting every
historical branch is not the viable path. The viable path is deterministic
Arborscape salvage:

1. classify branch/PR payload;
2. preserve source branch and commit SHAs;
3. create or update a stable salvage branch/PR;
4. land through the authorized signing connector;
5. mark equivalent or superseded branches without duplicating work;
6. keep prune/delete gated by Logan unless already merged/closed and proven
   payload-free.

## Immediate Next Actions

1. Do not make Codex commits from this shared checkout under the repo-local
   Claude identity.
2. Introduce per-worktree identity isolation before any new agent-authored
   commits are made.
3. Treat `.github/workflows/claude-sign.yml` references to the removed `.op`
   recipe as stale if that draft reappears.
4. Evaluate Tier 2 signing by whether it can provide the Arborscape landing
   connector, not by whether it can produce a local signature.
5. Keep the smoke detectors active: do not relax required signatures, reviewer
   gates, or workflow checks as a substitute for fixing provenance.

## Filed Statement

Codex #318 records that the local configuration is capable of creating
signatures but is not currently a safe, identity-bound agent signing solution.
Arborscape is the intended automation surface for branch and PR convergence.
The missing part is the authorized, idempotent landing connector between that
surface and protected `main`.
