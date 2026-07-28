# Commit signing setup — gitsign (candidate path, PR #487)

> **Status: one candidate implementation, not yet the canonical decision.**
> Issue #398 ("stable cross-platform signed-commit solution") has at least
> three competing drafts in flight: this PR (gitsign/sigstore OIDC), #450
> (claude-code-action + 1Password server-side signing), and #499 (bundles
> a version of this approach with the review-softlock fix). Which one
> becomes the vault's standard signing path is Logan's call, not assumed
> here. This document only explains how to use *this PR's* configuration
> once/if it's the one that lands.

## What this PR configures

`.gitconfig` enables [gitsign](https://github.com/sigstore/gitsign) —
sigstore's keyless, OIDC-based commit signing — as the local Git signing
program:

```ini
[commit]
	gpgsign = true
[gpg]
	format = x509
[gpg "x509"]
	program = gitsign
```

Note: Git ignores the legacy `gpg.program` key once `gpg.format = x509`
is set — the format-specific `gpg.x509.program` (or `[gpg "x509"]
program`) key is required, or Git silently falls back to `gpgsm` instead
of `gitsign`. There is also no `[gitsign] signingkey` config key; gitsign
derives identity from the OIDC login flow, not a static signing key.

Unlike the existing 1Password-SSH-agent-based signing flow, gitsign does
not depend on a local desktop agent being unlocked — it signs against a
short-lived certificate obtained via OIDC (GitHub identity), which is why
it was proposed as the fix for the "1Password agent locks, breaking
signing" failure mode named in #398.

## Setup

1. Install gitsign — three options:

   - **Go**: `go install github.com/sigstore/gitsign@latest`
   - **Homebrew** (macOS/Linux): `brew install sigstore/tap/gitsign`
   - **Prebuilt binary** (Windows/Linux/macOS/FreeBSD, amd64/arm64):
     download from the [gitsign releases page](https://github.com/sigstore/gitsign/releases)
     and put it on `PATH`. gitsign's release build does target Windows
     (`.goreleaser.yaml`: `linux`, `darwin`, `freebsd`, `windows`) even
     though the project's own quick-install docs only call out Homebrew/Go
     — a Go toolchain or WSL is not required on Windows, just for the Go
     install path specifically.

2. Confirm `gitsign` is on `PATH`:

   ```bash
   gitsign --version
   ```

3. With this repo's `.gitconfig` applied (either as the repo-local config,
   or merged into your global config), make a commit. The first commit
   triggers an OIDC login flow in your browser (GitHub identity by
   default); subsequent commits reuse the short-lived certificate until
   it expires.

## CI / headless signing

The interactive browser login flow in step 3 only applies to local,
human-driven commits. For CI or other headless environments (e.g. a
GitHub Actions job making a commit), gitsign needs an OIDC token source
instead of a browser popup — typically `permissions: id-token: write` on
the calling workflow job, so gitsign can obtain a Sigstore-recognized
OIDC token from GitHub Actions' own identity provider without any
interactive step. Without that permission, signing will fail in CI with
no browser to fall back on. This repo's own CI-signing wiring (if/when
built) is out of scope for this PR — see the "Open questions" section
below.

## Verifying a signed commit

```bash
git log --show-signature -1
```

or via GitHub's UI — signed commits show a "Verified" badge tied to the
signing identity (`loganfinney27` / GitHub OIDC), the same badge style
used for the existing 1Password-SSH-agent-signed commits, so verified
history doesn't visibly change format if/when the vault switches paths.

## Open questions (not resolved by this PR)

Carried over from #450's unresolved list, since they apply to any signing
path, not just claude-code-action:

- Which path is canonical: gitsign (this PR), 1Password server-side
  signing (#450), or the combined approach in #499?
- Does CI-driven (agent/bot) commit signing need a *different* mechanism
  than interactive human signing, or can they share this config?
- Rollout: is this meant to replace the 1Password SSH agent flow
  entirely, or coexist as a fallback for platforms where the agent isn't
  available?

These are flagged here rather than answered, per the same restraint this
PR's description already asks for: "yours to set, not assumed here."
