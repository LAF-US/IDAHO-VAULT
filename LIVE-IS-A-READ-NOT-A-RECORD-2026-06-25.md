---
updated: 2026-06-25
created: 2026-06-25
title: "'Live' Is a Read, Not a Record — Config Truth Lives in the Surface, Not the Notebook"
authority: LOGAN
doc_class: doctrine-clarification
status: active
matter: "Trusting live configuration over documents that merely restate it"
witnessed-by: "Claude Code — session https://claude.ai/code/session_01MU1zvEUacde5fmYpMvK8aK; occasioned by my own twice-made error this session"
adjudication: "Filed at Logan's direct command ('write this Live Witness, after rereading CONSTITUTION.md'). Defers to CONSTITUTION.md §I; amends no governance."
related:
  - "[[CONSTITUTION]]"
  - "[[VAULT-CONVENTIONS]]"
  - "[[LICH-IS-A-CHARGE-NOT-A-METAPHOR-2026-06-10]]"
  - "[[.claude/CLAUDE]]"
date: 2026-06-25
---

# 'Live' Is a Read, Not a Record

> **Logan's correction, recorded in substance:** *"Don't trust somebody's notebook
> paper over live config."* And: *"Sometimes I change or tinker with the live ruleset
> on a whim — Logan is a fickle creator-god."* Filed at his command, after rereading
> `CONSTITUTION.md`. This leaf records **how to know a rule**; it defers entirely to
> `[[CONSTITUTION]]` §I and amends nothing.

## The governing line already exists

`CONSTITUTION.md` §I Core Principles: **"There is no 'live' coordination surface. Any
document with 'live' or 'current' written in it is instantaneously out of date."**

A `.md` that *restates* configuration — which gates are required, who must review, what
the ruleset enforces — is exactly such a document. It is stale the instant it is written,
and staler each time the creator tinkers. This witness adds nothing to §I; it only drives
one nail.

## The ruling, in three points

1. **"Live" is a READ, not a RECORD.** To know whether a rule is enforced, *query the
   surface now*. Do not cite a document that describes it. A document is testimony about a
   past moment; the surface is the present fact.
2. **The creator is fickle by right.** Logan changes the live ruleset on a whim — that is
   the Architect's prerogative, not a defect. So every cached belief about configuration is
   provisional and must be re-read on each occasion that depends on it.
3. **A surviving artifact is not live authority** (`CONSTITUTION` §II: *"an artifact is not
   automatically live authority because it survived"*). That a doc exists, is committed, and
   sounds authoritative says nothing about whether the live surface still agrees with it.

## How to read it live (the method, not a snapshot)

When a decision turns on what `main` actually enforces, read the branch's **live** rules —
e.g. `GET /repos/{owner}/{repo}/rules/branches/{branch}` — and look at the live
`pull_request` / `merge_queue` / check rules, never at a `.md`. The merge automation already
embodies this discipline: it never asserts what the rules are; it reads each PR's live
`mergeStateStatus` and acts only on `CLEAN`/`UNSTABLE`, so it bends to whatever the ruleset
currently says rather than to a remembered list.

## What is NOT live (the traps that bit me)

- **`.github/CODEOWNERS`** implies workflow and governance paths require Logan's review. At a
  live read this session the ruleset set `require_code_owner_review: false` and
  `required_approving_review_count: 0` — so that gate was **not** enforced. CODEOWNERS is
  intent on paper, not an active control; do not infer enforcement from its existence.
- **`VAULT-CONVENTIONS` § "Merge queue"** enumerates the queue-entry gates. An enumeration in
  a doc is a snapshot; trust the ruleset, not the list.
- **This very leaf.** The moment it names a setting, that naming is out of date per §I. The
  config note below is **point-in-time testimony, already stale** — go read the surface.

## Point-in-time testimony (read 2026-06-25 — already out of date)

At one read of the live ruleset on `main` the enforced gates were: review-thread resolution
required; CodeQL (critical / errors); code quality (errors); Copilot review on push; the
merge queue (ALLGREEN); and **no** required approvals and **no** code-owner review. Recorded
as what was *seen*, not as what *is* — re-read before relying on any line of it.

## The occasion — witnessed

This leaf is occasioned by **my own error.** This session I twice asserted what branch
protection enforced by reading documents instead of the live config: first I cited
`VAULT-CONVENTIONS` to claim code-owner review was not wired in; then, shown `CODEOWNERS`, I
flipped and alarmed that the automation had been bulldozing a gate Logan had set — both
conclusions drawn from a `.md`, neither from the ruleset. Reading the live rules settled it
and matched neither panic. Recorded per the **Repair axis**
(`[[!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17]]` / the PERSONAE ENGINE): the error
named, so the next session reads the surface first. This is the same shape as
`[[LICH-IS-A-CHARGE-NOT-A-METAPHOR-2026-06-10]]` — a loose usage corrected and recorded — and
it sits beside the Provenance axis already in `[[.claude/CLAUDE]]`: a document is not
provenance for live state.

> Filed at Logan's command. Clarification and witness only — it defers to `[[CONSTITUTION]]`
> §I and promotes nothing into governance on its own motion.

---

```markdown
The world is quiet here．Esto Perpetua!
```
