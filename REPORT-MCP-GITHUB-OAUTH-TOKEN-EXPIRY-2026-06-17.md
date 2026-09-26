---
title: "MCP GitHub OAuth Token Expiry — Why the GitHub Tools Keep Dropping"
date: 2026-06-17
status: active
authority: LOGAN
doc_class: report
tags: [report, mcp, oauth, github, tooling, runtime, claude-code, auth, diagnosis]
related:
  - CLAUDE
  - "!/AGENTS.md"
  - REPORT-GH-AUTOMATION-TRIAGE-2026-05-25
---

# MCP GitHub OAuth Token Expiry — Why the GitHub Tools Keep Dropping

Diagnosis of a recurring symptom in Claude Code on the web (cloud sessions):
the `mcp__github__*` tools periodically fail with **`requires re-authorization
(token expired)`** while ordinary `git push`/`fetch` keeps working. Written
during PR #535; provenance is marked `[EVIDENCE]` (observed this session) vs.
`[CLAIM]` (corroborated by external sources) vs. `[INFERENCE]` (reasoning, not
verified).

## Symptom `[EVIDENCE]`

- The GitHub MCP tools returned, verbatim, `MCP server "github" requires
  re-authorization (token expired)` mid-session.
- At the same moment, `git push` / `git fetch` over the repo's `127.0.0.1`
  proxy remote **continued to work**.
- The condition recurs on long sessions; background system notices also show
  MCP servers repeatedly connecting/disconnecting.

## Mechanism (what's actually going on)

Two **distinct** things wear the same "tool unavailable" mask:

1. **OAuth access-token expiry — the GitHub drop.** `[CLAIM]` The MCP OAuth
   access token expires after roughly **one hour**. A refresh token is usually
   issued, but the MCP client frequently **fails to auto-refresh** it, so the
   connection dies at ~60 min with the exact `requires re-authorization (token
   expired)` string. This is a **recognized, open defect** in the client layer
   — not merely normal token-lifetime behavior — with a standing request to
   auto-refresh MCP OAuth tokens on expiry. (Sources below.)
2. **Connection churn of other MCP servers.** `[INFERENCE]` The constant
   connect/disconnect of unrelated connectors (Adobe, Lawve, MotherDuck, …) is
   transport cycling, separate from the credential expiry. The docs confirm
   cloud environments are **reclaimed after inactivity**, which is adjacent but
   does not, on its own, fully explain per-connector churn. Treat this half as
   unverified.

## Why `git` survives but the GitHub tools don't `[EVIDENCE → CLAIM]`

They use **different credential paths**. Per the docs: the git client uses "a
scoped credential inside the sandbox, which the proxy verifies and translates
to your actual GitHub authentication token," while the built-in GitHub tools
"authenticate through the GitHub proxy … so your token never enters the
container." Different lifecycles → `git` keeps working while the OAuth-backed
MCP tools lapse. This matched the observed behavior exactly.

## What the official docs do / don't say

- **Do:** token-based GitHub auth via a proxy; git uses a separate scoped
  sandbox credential; teleport/remote-control tokens are "short-lived" and
  refreshed via `/login`; cloud sessions/environments expire on inactivity.
- **Don't:** the page does **not** document the specific ~1-hour
  GitHub-MCP-token-no-refresh behavior. That came from the external issue
  reports, not the docs.

## Practical guidance

- The drop is **non-destructive**: `git` push/fetch is unaffected, and webhook
  events still wake the session — only *initiating* GitHub API reads is blocked
  while the token is lapsed.
- **Fix:** re-authorize the GitHub connection; that restores the tools for
  roughly the next token lifetime.
- **Workaround:** prefer `git` for time-sensitive repo actions; use the
  `mcp__github__*` tools opportunistically (right after a re-auth).
- **Expectation:** on a multi-hour session this **will recur** until the
  client-side auto-refresh fix lands; it is not a misconfiguration of this
  vault or repo.

## Provenance scorecard

| Claim | Standing |
| --- | --- |
| Exact error string; git unaffected; recurs on long sessions | `[EVIDENCE]` (this session) |
| ~1 h OAuth token, refresh not auto-firing, known open bug | `[CLAIM]` (multiple external reports) |
| git vs GitHub-tools use separate credential paths | `[CLAIM]` (official docs) |
| Inactivity-based environment reclamation | `[CLAIM]` (official docs) |
| Per-connector churn cause | `[INFERENCE]` (unverified) |

*Sourcing caveat: the issue-level specifics come from an aggregated web search
(US-only) over the reports below; the full threads were not each read end to
end. Treat as well-corroborated across several reports, not a single
authoritative spec.*

## Sources

- [Use Claude Code on the web — official docs](https://code.claude.com/docs/en/claude-code-on-the-web)
- [anthropics/claude-code #29718 — Auto-refresh MCP OAuth tokens on expiry](https://github.com/anthropics/claude-code/issues/29718)
- [anthropics/claude-code #28262 — MCP OAuth tokens not auto-refreshing despite valid refresh tokens](https://github.com/anthropics/claude-code/issues/28262)
- [anthropics/claude-code #25245 — "Token expired without refresh token" despite stored refresh token](https://github.com/anthropics/claude-code/issues/25245)
- [anthropics/claude-code #26281 — MCP OAuth tokens without expires_in/refresh_token silently expire](https://github.com/anthropics/claude-code/issues/26281)
- [astashov/liftosaur #560 — MCP OAuth access token expires after 1 hour with no auto-refresh](https://github.com/astashov/liftosaur/issues/560)
- [open-webui #19820 — MCP OAuth tokens not proactively refreshed, session loss after 1 hour](https://github.com/open-webui/open-webui/discussions/19820)

---

*Filed 2026-06-17 during PR #535. Symptom observed firsthand; mechanism
verified against the official docs and external issue reports (above), with the
one-hour/no-refresh framing corrected from "expected TTL" to "known client-side
refresh defect."*
