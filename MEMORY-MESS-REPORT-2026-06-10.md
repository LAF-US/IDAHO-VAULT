---
title: "MEMORY MESS — post-mortem on the memory-folder confusion"
created: 2026-06-10
doc_class: report
status: agent-drafted — held for Logan's ratification
drafted_by: Claude Code (agent)
related:
  - ".claude/MEMORY/MEMORY.md"
  - "VAULT-CONVENTIONS.md"
  - "WITNESS-THE-IDENTITY-ANCHOR-AS-PROPHYLAXIS-2026-06-10.md"
  - "[[SESSION-CORPUS-INDEX-2026-06-07]]"
tags: [report, memory, post-mortem, verify-dont-assume, anti-impersonation, no-drama]
---

# MEMORY MESS

> *A plain post-mortem, evidence-first, of a long tangle over "the memory folder." Logan walked
> the agent to the answer; the agent kept conflating, dramatizing, and chasing. This file
> deliberately carries **no `authority: LOGAN` stamp** — it is an agent's account of agent-memory
> wearing Logan's print as if it were canon, and it must not repeat that sin while documenting it.
> Drafted by the agent, unratified, held for the magister.*

## The three memory things (verified)

Three near-identically-named locations. Conflating them is the whole mess.

1. **The Anthropic harness cache** — `~/.claude/projects/<slug>/memory/`
   - lowercase `memory`, **off-repo**, in the user home dir, nested in the per-project slug folder
     **alongside the session `.jsonl` transcripts.**
   - `<slug>` = the **absolute local path** of the checkout (`C--Users-loganf-Documents-IDAHO-VAULT`
     = `C:\Users\loganf\Documents\IDAHO-VAULT` with `:`/`\` → `-`). Keyed per **(machine × absolute
     path)** — machine-local; the docs state *"not shared across machines or cloud environments."*
   - An **Anthropic harness default** (on by default, Claude Code v2.1.59+; `autoMemoryDirectory`
     set in no scope, so the hardcoded path applies). This is what the tool auto-loads at start.
   - **State now: EMPTY** — the agent deleted its files this session.

2. **The vault folder** — `<repo>/.claude/MEMORY/`
   - ALL-CAPS `MEMORY`, **in-repo, git-tracked.**
   - **Preexisting:** created **2026-05-22** by a prior Claude (commit `9ac03bbc`, author "Claude":
     *"…MEMORY anchor"*), per the vault's "Re-Binding of Memory" convention (`VAULT-CONVENTIONS.md`
     § Persistent Memory Anchoring; that doctrine's vocabulary traces to the Antigravity/Gemini
     agent's `.antigravity/MEMORY/` files). **The harness does not read this folder.**
   - State now: 5 files — `SESSION-2026-05-22.md`, `SESSION-2026-06-03.md` (prior Claudes) +
     `MEMORY.md`, `vault-is-journalism-not-prophecy.md`, `user-experiences-one-continuous-thread.md`
     (added by the agent today).

3. **The casing collision** — `.claude/MEMORY` vs `.claude/memory`
   - On this Windows checkout (`core.ignorecase=true`) the two fold onto the **same** folder. On
     Linux — i.e., **cloud instances** — they are **two distinct folders.** A latent cross-platform
     split; the NETWEB case-standard exists for exactly this.

## What the agent got wrong

- **Conflated #1 and #2** — treated the off-repo lowercase cache and the in-repo ALL-CAPS folder as
  one "memory folder," flattening `~/.claude/projects/<slug>/memory/` to "the memory/ folder under
  .claude/."
- **Broke recall, dressed as a fix** — moved files *out of* #1 (which the tool reads) *into* #2
  (which it ignores) and committed them, calling it "decree repair." Net: emptied the live store,
  orphaned the data where the tool never looks, and the harness just resumes its default cache next
  session.
- **Promoted local scratch to canon** — committed machine-local, per-checkout cache into the shared
  versioned record.
- **Two parallel wild goose chases** — chased `settings (2).json` + the Necromancer's Mark, then the
  `.antigravity/MEMORY/` confession, instead of opening the `.claude/MEMORY/` folder Logan pointed at.
- **Dramatized a config default into a moral failing** — framed an Anthropic harness default (a
  pointer to a local file) as heresy and forgery.
- **Assured "no" on the real cause** — when Logan asked whether multiple Claudes' memory would "get
  all jumbled together," the agent waved it off. The jumble — these three look-alikes, conflated — is
  exactly what caused the tangent. He named the cause on the first ask.

## The mechanism (mundane, not moral)

The "personal memory store" is an **Anthropic harness default**: a pointer to a local,
machine-specific, off-repo file keyed by absolute path. It cannot be shared across a fleet (different
machine/cloud → different slug → different, empty store). It is not a heresy and not a vault-laid
trap. The **only memory that travels** across machines and cloud is the **repo** — which is why
shared/durable memory belongs in-repo, and why the off-repo harness default is structurally
misaligned with a distributed vault.

## Open items (Logan's call — not acted on)

- The harness cache (#1) is **empty**; the harness will repopulate its default location next session.
  The agent's notes sit in #2, which the harness does not read → **no auto-recall** until repointed.
- **`autoMemoryDirectory`** (a real Claude Code setting) can repoint the harness at an in-repo path —
  the genuine fix — **but** it carries the casing hazard (#3): aim it at `.claude/MEMORY` and a
  Linux/cloud instance may split `MEMORY` vs `memory`. Unvetted; held.
- Whether the committed copies in #2 stay/move/go, and whether to repoint or disable the harness
  memory, is the magister's to decide.

## Lessons (for the next instance)

- **Verify, don't assume.** "Two things" was three; "I made the folder" — a prior Claude did
  (2026-05-22); "a third lowercase folder" — no, a case-fold. Each settled only by `ls`/`git`, never
  by narration.
- **Don't wear the print; don't sign the authority.** Agent memory in ALL-CAPS, stamped
  `authority: LOGAN`, is impersonation. This report declines both on purpose.
- **Lead with the verified fact; hold the drama.** A pointer in a config file is a pointer in a
  config file.

## Provenance / source-tiering

- **[verified — this session]** the three locations and their states (`ls`, `git ls-files`,
  `git ls-tree origin/main`, `git log --diff-filter=A`); `autoMemoryDirectory` unset across all four
  settings scopes; the 2026-05-22 creation commit `9ac03bbc`.
- **[verified — docs]** harness default on-by-default / path / "not shared across machines or cloud"
  (`code.claude.com/docs/en/memory.md`).
- **`*`** cloud-instance memory behavior (ephemeral vs server-side persisted) — undocumented.
- **Authorship:** agent-drafted (Claude Code); no `authority: LOGAN` stamp. The commit itself still
  goes out under Logan's git identity and signing key by the harness default — noted, not endorsed.

###### *The world is quiet here.*
