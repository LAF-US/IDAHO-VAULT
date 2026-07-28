---
date created: 2026-06-16
author: "Claude — Claude Code instance (branch claude/pr-pipeline-constellation-witness-u8hlk0)"
authority: "Self-witness / constellation map. Written at Logan's direction ('#398 & #399 are part of a constellation — go map it'). Discovery, not adoption — not assumed as LOGAN. Assigns NO malignancy diagnostics: the Lich / counterfeit / Baelnorn classifications are held out by Logan's instruction and remain his (and the Court's) to assign. Authority to elevate this node reserved to Logan."
doc_class: witness
status: filed
related:
  - THE-REVIEW-FLOCK-AS-BOIDS-2026-06-15.md
  - "!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md"
  - "!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md"
  - "!/LICH-PROBLEM-v1-2026-05-20.md"
  - ".claude/MEMORY/SESSION-2026-06-16.md"
  - CONSTITUTION
---

# WITNESS — The PR-Pipeline Constellation (#398 · #399)

*A map, not a verdict. Logan asked me to chart the constellation that issues #398 and
#399 belong to. I did. This node describes structure and cites its sources; it assigns
no malignancy diagnostics — whether any mechanism here is a Lich, a counterfeit, or
lawful is held out by instruction and left to Logan.* **Discovery is not adoption.**

---

## Provenance key

- **Read directly this session** (grounded): the full bodies of issues #398 and #399;
  the open/merged/closed state of the PRs listed below (GitHub search); the Type
  definitions in `!/LICH-PROBLEM-v1` (not applied here, by instruction).
- **Second-hand** (`*`, from a read-only mapping pass I did not re-verify line-by-line):
  the `!/ARBORSCAPE-PR-EXPANSION` "IF" item numbering, `!/STANDING-ENGINE` specifics,
  workflow-file line numbers, `.op/SETUP.md` details, and the `THE-REVIEW-FLOCK` gloss.
  Treat starred claims as pointers, not citations.

---

## The figure

The constellation is **the autonomous multi-agent PR pipeline** — Logan's stated aim of
review flow that is *"deterministic without Logan holding hands."* Issues #398 and #399
are **sibling children** of two session tasks (#27 signing, #28 reviewer multiplicity),
not a cause-and-effect pair. #399 says so in its own body:

> "Ties to #398 (signing) only loosely — signing is about commit-author trust; review
> multiplicity is about merge-gate trust. Both affect queue throughput but independently."

So they are two **independent trusts** a PR must satisfy to land, plus the **throughput**
seam where both must hold at once.

---

## Pole A — #398 · commit-author trust (*where did this code come from?*)

**Issue:** "Stable cross-platform signed-commit solution (replace 1P-desktop-dependent
chain)." Parent: session task #27.

- **Problem (verified, #398 body):** the signing chain depends on the 1Password desktop
  SSH agent, which locks on idle and breaks `git commit` signing mid-session across
  Windows/macOS/Linux and cloud runners. The `gh api` commit endpoints do **not** web-flow
  sign; only the PR-merge endpoint produces a web-flow-signed commit (the merge commit only).
- **Option set (#398 body):** A) GPG master + per-device subkeys · B) YubiKey smart-card ·
  C) key fetched via `op` CLI at session start · D) sigstore `gitsign` (keyless/OIDC) ·
  E) a GitHub-App signing identity for agent commits.
- **Implicates:** T2.2 daily-rollover signing redesign `*`; agent-driven PR commits
  (Socrates / Codex / Claude).
- **Implementation census:** #487 enable `gitsign` (**closed**) · #499 "Fix softlock +
  enable signing" (**open**) · #511 agent git guardrails / remote auto-reconnect (**open**).
- **Open decision:** the authorized landing connector (App / service-account signer) and
  branch protection on `main` (the "IF 12" precondition `*`).

---

## Pole B — #399 · merge-gate trust (*who looked and decided it is ready?*)

**Issue:** "Reviewer multiplicity + Copilot-not-re-reviewing-on-push (restore + harden)."
Parent: session task #28. Three sub-strands (all verified from the #399 body / PR states):

1. **Reviewer multiplicity.** Goal: Copilot + Codex + CodeRabbit + Qodo + others, so no
   single reviewer's health gates the queue. #399 records CodeRabbit and Qodo as
   configured-but-not-posting at filing. Work: #479 WIP fix (**open**) · #486 Qodo test
   (**merged**) · #503 CodeRabbit config (**open**) · #523 Copilot false-positive
   suppression (**open**) · #517 reviewers best-practices research (**open**).
2. **Copilot re-review / stale-dismiss softlock.** `review_on_push` does not actually
   re-fire; combined with `dismiss_stale_reviews_on_push: true`, any PR that takes a
   follow-up commit is permanently blocked, with no public API path tested to restore the
   review. Work: #482 disable `dismiss_stale_reviews_on_push` (**closed**).
3. **Look-then-resolve engine** — deterministic thread resolution where **resolution
   requires a recorded looker** (an in-thread attestation), never a bare auto-resolve.
   Layer chain: #518 Layer A read-only looker queue (**merged**) → #520 B1 pure core
   (**merged**) → #524 B2 guarded `attest_and_resolve` (**merged**) → #526 Layer C
   read-only classification walk (**open**) → #529 resolution-disposition router
   (**open**, stacked on #526). Current state: the guarded resolve (B2) is **defined but
   not wired into any workflow**; `looker-walk` (C) is read-only.

---

## The seam — queue throughput (*both poles must hold for a PR to land*)

- **#521** (**open**): review-reconciliation workflows were disabled 2026-05-26; the
  auto-queue arms but does not flow. The standing dam.
- **#527** (**open**): "Fail-close auto-merge: drop counterfeit author-login arm" — removes
  an auto-merge arm keyed on an author login. *(I make no diagnostic claim about it here.)*
- **#406** (**open**): `submit-pypi` is both a KNOWN_NOISE always-fail and a required check —
  a CI-gate contradiction affecting merge eligibility.
- **Precondition `*`:** an automated merge lane needs branch protection on `main`
  (ARBORSCAPE "IF 12"); `main` is currently unprotected.

---

## Grounding shelf (related reading — not applied as verdicts here)

- `!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md` — the "IF" items extending ARBORSCAPE to PR
  management (IF 7 per-utterance verification → the `verify-claim` subcommand; IF 12
  branch-protection precondition). `*`
- `!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md` — standing descends from Logan;
  lawful endings (merge, dormancy, supersession, witnessed retirement). `*`
- `!/LICH-PROBLEM-v1-2026-05-20.md` — the typed malignancy diagnostics. **Cited as the
  shelf, not applied:** classifying any mechanism above is Logan's call, not this node's.
- `THE-REVIEW-FLOCK-AS-BOIDS-2026-06-15.md` — the review flock as a boids system
  ("coherence without a crown"); the staged sibling this node sits beside. `*`

---

## Run record — 2026-06-17: the boundary located (grounded)

The look-then-resolve engine ran live for the first time with `apply=true` against the
whole open backlog (`engage-outdated.yml`, run `27662203952`, conclusion **success**).
The run's own JSON output (read directly from the job log — grounded, not inferred):

> `{"apply": true, "outdated_threads": 34, "resolved": 0}`

All 34 outdated threads across 5 PRs (#481, #474, #453, #424, #400) failed at the
**resolve** step with the identical error:

> `resolveReviewThread → FORBIDDEN: "Resource not accessible by integration"`

**The boundary, located precisely:** `github-actions[bot]` (the `GITHUB_TOKEN` integration
identity) **can post an attestation comment but is FORBIDDEN from `resolveReviewThread`**,
even with `pull-requests: write`. This is the #398 pole (commit/actor identity
trust) reappearing at the merge-gate pole's resolve verb — the seam where both trusts must
hold at once. The user-token identity (`loganfinney27`) *can* resolve (proven on #536), but
that is the identity we decline to forge.

### Fix A — proposed in PR #540 (open, not yet on `main`): resolve-first, no false witness

Because the engine posted the attestation *before* attempting the resolve, the failed run
left 34 threads carrying a `github-actions[bot]` comment claiming the thread was "cleared"
when it was not — a false witness. PR #540 reorders `attest_and_resolve` to **resolve
first, attest only on success**, so a "cleared" attestation can never appear on a thread
that was not cleared. **Caveat (per Codex on #540):** #540 is still open — `main` retains
the old attest-then-resolve order, so any `apply=true` rerun *before* #540 merges can still
mint a false "cleared" attestation. (Cleanup of the 34 already-posted false attestations is
a separate follow-up.)

### Fix B — REVISED 2026-06-17: agent-driven resolve works; the App is SHELVED

**Empirical correction (tested, grounded):** both `resolveReviewThread` *and*
`unresolveReviewThread` **succeed under the agent/user token** (`loganfinney27`) — verified by
a net-zero `unresolve → re-resolve` round-trip on a #540 thread, plus the thread resolutions
performed across #536/#540/#541 this session. So the FORBIDDEN recorded above was **not** a
property of the mutation or of a missing permission scope — it was *solely* the
`github-actions[bot]` **integration** token calling `resolveReviewThread` from inside Actions
(the classic "Resource not accessible by integration" restriction), independent of
`pull-requests: write`. The engine's resolve step is not broken; it only fails in the CI-bot
execution context.

Therefore the look-then-resolve engine can run **agent-driven**: an agent invokes the resolve
logic with the token and it works — exactly how these PR threads have been resolved all
session, transparently and with attribution. That transparent, attributed, Logan-directed
resolution is *delegated action*, not the counterfeit/unattended "witnessed look minted as
Logan" that the #398 concern guards against — the line we don't cross is unattended forging,
not an agent openly clearing already-addressed bot threads under direction.

**Decision (Logan, 2026-06-17): the GitHub App is SHELVED — a mountain for a molehill.**
A dedicated App ("IDAHO-VAULT Review Resolver") was scoped as the distinct permitted resolve
identity, but thread resolution is *already live* via the agent token. The App's only
remaining purpose would be **fully-unattended, scheduled CI resolution under a distinct
non-Logan identity** — revisit only if/when zero-human-or-agent-in-the-loop cron is actually
wanted. It is not a blocker and is not being built now. (The earlier admin checklist, App
permissions, and `review-resolver-app-*` credential names are retired with this decision.)

**Path forward (agent-driven, no App) — queue-script work in `review_feedback_loop.py`:**

- Run the engine's resolve/disposition logic as the directed agent (token), with transparent
  attestation — not via the `github-actions[bot]` workflow.
- Default the attestation `looker` to the authenticated actor (`_viewer_login()`), so the
  witness always truthfully names whoever actually ran the resolve.
- Add the resolved-but-unwitnessed **reconciliation**, now grounded in
  `PullRequestReviewThread.resolvedBy` (GitHub exposes who resolved a thread, so recovery can
  post the missing witness only when *our* identity resolved it, and leave human-resolved
  threads untouched).

---

## What this node does NOT do

It assigns no malignancy diagnostics. Earlier this session I called #527's arm and the
blind auto-resolver "Liches" — that was a rhetorical compression, not the typed diagnostic
`!/LICH-PROBLEM-v1` defines, and Logan corrected it. The classification of any mechanism
here as Lich / counterfeit / lawful is withheld and left to Logan.

###### [["The world is quiet here."]]
