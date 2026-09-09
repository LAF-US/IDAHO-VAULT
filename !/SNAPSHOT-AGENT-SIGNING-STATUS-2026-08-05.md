---
authority: LOGAN
agent: Claude Code
created: 2026-08-05
doc_class: status-snapshot
status: filed
tags:
  - snapshot
  - github
  - signing
  - github-app
related:
  - "CONSTITUTION.md"
  - "AGENTS.md"
  - "https://github.com/LAF-US/IDAHO-VAULT/issues/398"
  - "https://github.com/LAF-US/IDAHO-VAULT/pull/471"
  - "https://github.com/LAF-US/IDAHO-VAULT/pull/895"
---

# Agent Commit Signing (GitHub App path) — plain-language status, 2026-08-05

This is a status snapshot, not doctrine. Written because agents keep landing on
this topic without a straight answer, per Logan. Full design history and
discussion: GitHub issue #398. This file is the "what's actually going on"
version.

## The problem this solves

`main` requires every commit to be GitHub-verified (`required_signatures`
branch ruleset). Logan's own commits sign via a local 1Password SSH-agent
bridge that locks itself on idle and fails mid-commit (`fatal: failed to write
commit object`) — that's a **separate, still-unsolved problem**, tracked as
"Human Signing" in #398. Nothing here fixes that.

This file is about **agent** commits specifically: when Claude Code, Codex,
OpenCode, or Mistral commit from a terminal or CI runner, they have no signing
key of their own. Borrowing Logan's identity to sign is explicitly rejected in

# 398 as "not an authentication solution — an impersonation hazard."

## The fix

A dedicated **GitHub App** per agent (same kind of thing as `dependabot[bot]`,
`coderabbitai[bot]`, `codacy-production[bot]` — all already installed on this
repo). When a GitHub App creates a commit through GitHub's REST API using its
own installation token, GitHub marks that commit verified automatically —
server-side, no local key. App installation tokens are themselves short-lived
(normally ~1 hour) and can be revoked/rotated, same as any credential — the
workflow avoids the 1Password-style lock failure not because the token never
expires, but because it mints a fresh one per run (`actions/create-github-app-token`)
instead of depending on one long-lived session.

## Current state, verified today (not carried forward from old comments)

- **Built and merged to `main`:** `.github/workflows/agent-swarm-signing-proof.yml`
  plus four dispatch-only wrappers (`-opencode`, `-claude`, `-mistral`,
  `-codex`). This is a **test harness only** — dispatching it makes one
  throwaway proof commit for the chosen agent and checks whether GitHub
  reports it `verified: true`. It is not wired into any real agent commit
  path yet.
- **No GitHub App has been confirmed to exist for any of the 4 agents.**
  PR #471's original body (2026-06-04) claimed the `opencode-agent` App
  "already exists." A global GitHub user search for that exact name returns
  zero results as of this writing, but that's **inconclusive, not
  disproof** — a privately-installed App isn't guaranteed to surface in
  general user search. Not independently confirmed either way for any of
  the four; this session's tooling can't see what's actually installed on
  the `LAF-US` org. The next section's step 1 is how to actually check.
- **Nothing has been proven yet.** No proof run has produced a
  `verified: true` result on issue #398.

## What actually needs to happen next (concrete, not vague)

1. Logan checks `https://github.com/organizations/LAF-US/settings/installations`
   to see what, if anything, is already installed.
2. For each agent lane that isn't already there: create a GitHub App at
   `https://github.com/settings/apps/new`, grant `contents: write`,
   `pull-requests: write`, `issues: write`, install it on this repo.
3. For each App, store two values as repo Settings → Secrets and variables → Actions:

   | Agent | Variable (App ID) | Secret (private key) |
   | --- | --- | --- |
   | opencode | `OPENCODE_AGENT_APP_ID` | `OPENCODE_AGENT_PRIVATE_KEY` |
   | claude | `CLAUDE_APP_ID` | `CLAUDE_APP_PRIVATE_KEY` |
   | mistral | `MISTRAL_APP_ID` | `MISTRAL_APP_PRIVATE_KEY` |
   | codex | `CODEX_APP_ID` | `CODEX_APP_PRIVATE_KEY` |

4. From the Actions tab, manually dispatch `Agent Swarm Signing Proof — <agent>`
   for one lane (recommended: start with one, not all four) and read the
   result it posts to issue #398.

Until step 4 succeeds once, this whole mechanism is unproven — treat any
claim otherwise as unverified.

Claude-Session: <https://claude.ai/code/session_01Gwgxf5zb2cGx9PZGHDLTMV>
