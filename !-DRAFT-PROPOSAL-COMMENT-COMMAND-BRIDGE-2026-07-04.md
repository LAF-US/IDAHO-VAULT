---
title: "DRAFT Proposal — The Comment-Command Bridge (#760 Option C)"
date created: 2026-07-04
authority: "LOGAN (recorded; proposed by a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: proposal
status: draft
related:
  - "GitHub issue #760 (harness verb gap)"
  - "GitHub issue #398 (identity separation)"
  - "PROVENANCE-MARKS.md"
  - ".github/workflows/review-feedback-loop.yml"
  - ".github/workflows/engage-outdated.yml"
  - ".github/scripts/review_feedback_loop.py"
  - "CONSTITUTION.md"
---

# DRAFT Proposal — The Comment-Command Bridge (#760 Option C)

*Filed 2026-07-04 for Logan's review. Draft only. Not live doctrine. This proposes a
change to an ENFORCEMENT surface (§V) — it is a design for Logan to gate, and nothing
here is implemented. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

## Summary

The harness verb gap (#760): an agent's MCP channel has identity but a fixed verb
set (no GraphQL, no workflow dispatch, no enqueue); its sandbox has compute but no
credential. The one write-verb every harness *does* hold is `add_issue_comment` —
and `.github/workflows/review-feedback-loop.yml` **already** fires on
`issue_comment: [created]` and runs the #399 engine under the Actions
`GITHUB_TOKEN`, which *has* the missing verbs. This proposes a narrow, authorized,
injection-hardened **comment-command bridge**: an authorized comment triggers an
already-sanctioned engine command, executed by trusted code from the default branch.
It grants **no new power** — only a new, guarded *trigger* for power the engine
already has.

## What already exists `[read]` (verified at head ec2b670d)

`review-feedback-loop.yml` today:
- triggers on `issue_comment:[created]` and `pull_request_target`;
- workflow-level `permissions: contents: read`, with `sweep-review-threads`
  **job-scoped to `contents: write`** for auto-merge arming — the precedent that a
  single job can hold the write scope `resolveReviewThread` needs (#546/#44650);
- every job **checks out `github.event.repository.default_branch`** ("trusted
  workflow surfaces") — never the PR head;
- passes the comment body through an **env var** (`COMMENT_BODY`), never
  interpolated into the shell;
- already threads **`author_association`** into a subcommand (`acknowledge-apply`);
- already runs a comment→narrow-subcommand→marked-reply pattern
  (`verify-agent-claims`), with a self-marker that prevents recursion.

Five of the six hardening primitives this proposal needs are therefore already
in the file. The bridge adds one job in the same shape.

## The protocol

**Command surface.** A single fenced line in a PR comment, strict grammar, no prose
ambiguity:

```
/vault attest-resolve --pr <int> --thread <PRRT_id> --decision <addressed|advisory|wontfix> [--rationale "<text>"]
```

A tiny enumerated verb set only — initially just `attest-resolve` (and later
`enqueue`). Parsed by the existing engine's argparse, from the env var, with typed,
regex-validated arguments. **Not** an LLM reading intent; **not** a shell string — a
deterministic parser over an allowlisted grammar.

**The job.** A fourth job, `execute-command`, gated
`if: github.event_name == 'issue_comment' && github.event.issue.pull_request != null`, job-scoped `contents: write` +
`pull-requests: write`, checkout default branch, run
`review_feedback_loop.py comment-command --comment-body "$COMMENT_BODY"
--comment-author "$LOGIN" --author-association "$ASSOC" --comment-id "$CID"`. The
subcommand authorizes, parses, dispatches to the *existing* `attest-resolve`, and
posts a marked witnessed reply.

## Threat model & hardening

A comment-triggered job holding `contents: write` is a confused-deputy risk by
construction — the token is more privileged than most commenters. Every guard below
is load-bearing; none is optional.

| Threat | Mitigation |
|---|---|
| **Unauthorized commander** (anyone can comment) | Authorize on **`author_association`** — GitHub-computed server-side, **not** forgeable in comment text. Require `OWNER` (later: a Logan-curated allowlist of per-agent bot logins, per #398). Authorization runs **before** the token touches anything; unauthorized → logged-and-refused reply, no action. |
| **Prompt injection** (malicious comment text) | The bridge is **deterministic parser, not an agent** — regex + argparse over an enumerated grammar. Comment text is never fed to an LLM, never `eval`'d, never `shell=True`. Prompt injection has no surface because nothing interprets intent. |
| **Shell injection** | Body flows via env var (existing pattern); arguments typed and validated: thread `^PRRT_[A-Za-z0-9]+$`, decision ∈ enum, pr/comment-id ints. Reject on any mismatch. |
| **Untrusted-code execution** (the `pull_request_target`/`issue_comment` classic) | **Never checkout PR head; never run PR-authored code.** Executor is always default-branch code (existing invariant — preserved absolutely: no PR ref, no `pip install` from PR, no PR-supplied scripts). |
| **Identity spoofing** | `comment.user.login` + `author_association` come from the signed event payload, not the body. |
| **Recursion / loops** | Ignore bot-authored comments as command sources (github-actions[bot] can't command); self-marker on the reply (existing pattern); dedupe by `comment-id`. |
| **Privilege laundering via the verb** | The bridge adds no resolving power: `attest-resolve` keeps its own gates — **bot-only threads, page-complete, not CHANGES_REQUESTED**. Net security = (commenter authorized) × (command's existing gates). Defense in depth. |
| **Blast radius** | One PR per command (no fleet sweep via comment — that stays `workflow_dispatch`). Dry-run parity with engage-outdated where meaningful; `unresolveReviewThread` rollback available (reversibility). |
| **Auditability** | Every command — accepted or refused — posts a witnessed, marked reply (what ran + attestation, or the refusal reason) and appends to the engine's JSON audit. Annotate-don't-erase. |

## What is NOT bridgeable (the deny-list)

Explicitly out of scope, by construction, no matter who comments: arbitrary
`workflow_dispatch`; arbitrary GraphQL; any edit to enforcement config, rulesets, or
`.github/workflows/**`; anything touching CHAINFIRE / the wikilink graph or canon
paths; merges (auto-merge stays GitHub's, armed not forced). The bridge is a short,
enumerated RPC — never a general shell.

## Composition & relations `[inferred]`

- **#760 Option C**, fleshed out. Composes with **Option B** (scoped credentials):
  B serves interactive/high-trust harness work; C is the fleet-scale, no-new-secret
  path — every harness already has `add_issue_comment`.
- Serves **#398**: when identities separate, the `author_association` allowlist
  becomes the per-agent authorization roster — the bridge's guard and #398's
  identity model are the same list.
- Motivating case: PR #563's three threads + enqueue — the exact acts the verb gap
  stranded this week — become an authorized comment instead of a hand-run script.

## Status

**DRAFT — awaiting Logan's gate.** Nothing implemented; no workflow edited; no
enforcement surface touched. §V governs (no unilateral change to routing/governance
automation); §VI (workflow-schedule conflict check) applies at implementation. On
approval, the build is one job added to `review-feedback-loop.yml` plus one
`comment-command` subcommand in `review_feedback_loop.py`, proven dry-run on the
backlog before it arms — mirroring how engage-outdated was staged.

###### [["The world is quiet here."]]
