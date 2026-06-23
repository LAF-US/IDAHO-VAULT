---
title: "Witness — required_signatures live-config probe (2026-06-23)"
created: 2026-06-23
updated: 2026-06-23
status: draft
authority: LOGAN
doc_class: witness
authors:
  - Claude Code CLI
related:
  - DRIVE-MANAGEMENT
  - WITNESS-PENDING-NOT-DONE-2026-06-21
  - CONSTITUTION
tags:
  - witness
  - git
  - branch-protection
  - signing
  - live-config
---

# Witness — required_signatures live-config probe

A deliberate, consented live-configuration test. The committed `main_ruleset.json` is a
**dated snapshot** (`updated_at: 2026-05-27`) that lists a `required_signatures` rule under
`enforcement: active`. Reading that file is not the same as observing live enforcement — the
recurring lesson this vault keeps teaching. One question could not be answered from the
snapshot or from commit history without a live flip:

> **Does `required_signatures`, with the merge queue's `MERGE` method, accept the queue's
> GitHub-signed merge commit while the underlying feature commits stay unsigned — or does it
> reject the unsigned author history?**

Every historical agent commit on `main` is `%G? = N` (unsigned); the merge-queue merge commits
are GitHub-signed (`E` — present, unverifiable locally for want of an `allowedSignersFile`).
That ambiguity is unresolvable by reading alone, because the merge queue signs the tip either
way.

## Method (this PR is the instrument)

- This note is committed **unsigned on purpose** (`--no-gpg-sign`) to replicate the normal
  agent state, not a signed special case.
- The PR opens as a **draft** so it cannot enter auto-merge or the merge queue *regardless of
  rule state* — only once it is explicitly marked ready does the `required_signatures` state
  become the operative gate.
- Logan flips `required_signatures` **on** (live), then the PR is marked ready and run through
  the queue.

## Reading the result

- **Merges clean** → `required_signatures` is satisfied passively by GitHub's merge-commit
  signature; agents never need to sign. The rule decouples from the author-signing roadmap
  (#398 / #399).
- **Blocks at merge** → the rule reaches the unsigned feature commits; signed-`main` is
  incompatible with the current unsigned-author workflow until author signing lands.

Either outcome is a real live-config datapoint, not a snapshot inference. After the read, the
rule is flipped back off and this branch is kept (if merged) or discarded (if blocked).

### The rule being toggled

The target is the repository ruleset **"Main Ruleset"** (id `16864823`), the `required_signatures`
rule — GitHub → repo **Settings → Rules → Rulesets**, or the `rulesets/16864823` API endpoint.
Per the **2026-05-27 snapshot** (`main_ruleset.json`) that ruleset carried **no bypass**
(`bypass_actors: []`, `current_user_can_bypass: never`). That is a *snapshot* value, not an
observed-live one — **confirm the live bypass settings in the UI/API before enabling**, because a
no-bypass rule left on silently blocks **unrelated** merges across the repo until it is reverted.

### Rollback (abort path)

If the probe **stalls, is abandoned, or fails for any reason**, flip `required_signatures` back
**off immediately** — before retrying or discarding the branch. Reverting the rule is the only
abort switch; nothing else overrides it. Then verify the revert actually took, live:

- [ ] `required_signatures` removed/disabled on **"Main Ruleset"** via the live UI/API (not read
      back from the committed snapshot).
- [ ] a normal **unsigned** agent PR can merge again — the gate is genuinely gone, not just
      edited in a file.

---

## DOCUMENT METADATA

- **Created:** 2026-06-23
- **Last Updated:** 2026-06-23
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** Throwaway probe artifact for a consented live test of the `main`
  `required_signatures` rule. Committed unsigned to mirror the real agent state; opened as a
  draft so the merge cannot fire under the rule-off state. Records the open question (does the
  merge queue's GitHub merge-signature satisfy `required_signatures` while feature commits stay
  unsigned?) and the pass/block reading. Companion to the live-vs-snapshot finding that
  `main_ruleset.json` is a 2026-05-27 export, not live enforcement.
