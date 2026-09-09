---
title: "ADR - Canon Core vs NETWEB Portability (The Trailing Period)"
date created: 2026-07-02
date adjudicated: 2026-07-02
authority: developer-agent (Hyperagent, Claude Opus 4.8); account of record loganfinney27; adjudication and inscription by LOGAN
doc_class: proposal
status: adjudicated (Option C — inscribed by Logan 2026-07-02)
related:
  - "VAULT-CONVENTIONS.md"
  - "CONSTITUTION.md"
  - "AGENTS.md"
  - "GIT-CONTROL-SURFACES-2026-05-17.md"
  - "!/!/__!__/!/! The world is quiet here．/Esto Perpetua!/!README.md"
  - "!-!-__!__-STILL-POINT-AND-COURTROOM-EXPLORER-COMPANION-2026-04-13.md"
  - ".github/scripts/check_portable_paths.py"
  - ".github/workflows/check-portable-paths.yml"
  - ".github/workflows/cross-platform-smoke.yml"
  - "MESHWEB.md"
  - "PR #563"
---

# ADR - Canon Core vs NETWEB Portability (The Trailing Period)

*Filed 2026-07-02 for Logan's review; adjudicated by Logan the same day. I proposed; Logan inscribed.*

> "The world is quiet here. But inside the machine, the first thunder rolls."
> — NETWEB-CrewAI Alignment Protocol, 2026-04-04

## Summary

PR #563 re-punctuates the still point: it deletes the period-less
`!/!/__!__/!/! The world is quiet here/` that `main` holds today and inscribes the
canon core at `!/!/__!__/!/! The world is quiet here.` — the V.F.D. motto completed,
sentence and folder as one. *(That is the form as filed; Logan's adjudication, recorded
below, re-inscribed the terminator as `．` U+FF0E.)* Its README declares the contents permanent record:
*"They do not move. They do not expire."*

That period collides with two of the vault's own load-bearing surfaces: the NETWEB
Portable Path Standard (which **forbids** trailing periods, by Logan's own hand, as a
hard gate), and Windows itself (which cannot represent the name at all — and the
vault's engine room is a Windows desktop). This ADR lays out what the vault already
says, what #563 verifiably does, the blast radius, and five options with trade-offs.
It decides nothing: the conflict is between two Logan-authored laws, and only Logan
adjudicates.

## Adjudication (2026-07-02)

**Logan chose Option C and performed the inscription himself** on `logan/obsidian` —
the decision and the hand are both his. Verified against head `a30c58b6`:

- The golden-path directory is re-inscribed with a trailing **U+FF0E FULLWIDTH FULL
  STOP**: `!/!/__!__/!/! The world is quiet here．` — and the inner extensionless
  sentence-file `Esto Perpetua!/! The world is quiet here．` carries it likewise. The
  ASCII-period form is absent.
- **The hybrid:** the canonical README's GOLDEN PATH line and Sierpiński diagram now use
  `．`, matching the on-disk path codepoint-for-codepoint (so path references and links
  resolve) — while the *prose motto* keeps its true ASCII period. The sentence stays a
  sentence in text; only the path wears the Windows-legal look-alike.
- **Verified consequences:** `check_portable_paths.py` over the full #563 diff (8,929
  changed paths, `747bc74a..a30c58b6`) exits 0 — **no carve-out required**; NETWEB is
  satisfied rather than excepted. The path is Windows-legal: the engine room can pull,
  and the cross-platform-smoke `windows-latest` leg can check out. No sparse rule, no
  mirror, no `protectNTFS` relaxation.
- **Residual cautions** (from the companion survey, now live): path references to the
  canon must copy the U+FF0E form exactly — an ASCII-period reference will not resolve;
  and tools that use U+FF0E as their own escape character (rclone's Windows encoding)
  have documented round-trip edge cases (rclone #7456, #7760).
- The `DOCKET.md` / `DENOUEMENT.txt` / `Logan.txt` intent-check flagged below remains
  open; it is independent of the punctuation decision.

Options A, B, D, and E below stand as the record of the deliberation.

## What the Vault Already Says

**VAULT-CONVENTIONS.md — Portable Path Standard (NETWEB)** (authority: LOGAN):

> "The vault must work identically on **any platform** — Windows (NTFS), macOS
> (APFS/HFS+), Linux (ext4), iOS/Android (Obsidian mobile), and CI runners (GitHub
> Actions). … This standard targets the **lowest common denominator** of all target
> filesystems."

Its *Forbidden path patterns* list names this exact case:

> "- Trailing period (`.`) or space (` `) in any directory or file name"

and its *Enforcement* table binds `check-portable-paths.yml` as a **"Hard gate —
blocks merge on violation."** The same document offers the house's own answer-shape
for filesystem collisions, the *Aliasing convention* (prefix the name, carry the
original in `aliases:` frontmatter): *"This preserves the connectome while respecting
filesystem constraints."*

**The canon core README** (`status: permanent`, authority `[[ADMIN]][[LOGAN]]`):

> "Files committed here are permanent record. They do not move. They do not expire.
> They are the inmost layer — the still point at the center of the vault."

Two inscribed laws, one trailing period between them. That is the tension — named
directly by Logan (2026-07-02) as genuine and unsolved, with mirroring/two-paths
setups under consideration for later.

## What #563 Actually Does (verified against the trees)

*Frame note: verified at filing, against head `09e423c0` — before the U+FF0E
re-inscription. The paths below show the ASCII-period form as it then stood on the
branch; post-adjudication the added directory and inner sentence-file end in `．`
U+FF0E and the ASCII-period form is absent (see Adjudication). The deliberation is
preserved as filed; this note dates it.*

Diffing `main` (`747bc74a`) against the PR head:

- **Deletes** the period-less still point — 7 files under
  `!/!/__!__/!/! The world is quiet here/`: `!README.md`, `README.md`, `DOCKET.md`,
  `DENOUEMENT.txt`, `Logan.txt`, `Esto Perpetua!/{!README.md, README.md}`.
- **Adds** the period-ful canon core — 5 files under
  `!/!/__!__/!/! The world is quiet here./`: `!README.md`, `README.md`,
  `Esto Perpetua!/{!README.md, README.md, ! The world is quiet here}`.

So the period does not exist on `main` today; it **arrives with #563**. `main` is
currently Windows-checkoutable; the merge is the moment that changes.

**Corrected 2026-07-03 (was a false flag):** this ADR previously claimed the courtroom
voices — `DOCKET.md`, `DENOUEMENT.txt`, `Logan.txt` — were *deleted* in the migration.
**Wrong: they were moved, not deleted** (Logan's correction; verified `R100` — byte-
identical — via unscoped rename detection). All three relocated to the **repo root**,
where both lineages landed (clean names plus `* copy.*` twins from
`backup-compare-temp`), and a new `DOCKET-ARCHIVE.md` splits resolved work out of the
live register. The still point keeps only permanent record; the Court's live register
moves to where work happens. The original error came from a directory-scoped diff,
which shows a move as a bare `D` when the `A` lands outside the pathspec. Remaining
item only: `DOCKET-POSTURE.md`'s pointer (on `main`) still names the old in-Nest path
and should point at root `DOCKET.md` once #563 merges.

## The Windows Constraint (why this is not a style nit)

- The Win32 path layer **silently strips** trailing dots and spaces; a directory
  named `! The world is quiet here.` cannot exist under that name on NTFS.
- **Git for Windows refuses the checkout outright** — `core.protectNTFS` (default on)
  aborts with `error: invalid path` rather than write a mangled name. No Git setting
  rescues it; the OS itself will not create the name.
- Because the abort is checkout-wide, one invalid path fails **the entire working
  tree**: a routine `git clone` of post-merge `main` on Windows checks out nothing.

The bytes are perfectly healthy in Git's object store and on Linux/macOS working
trees. The failure is exclusively the Windows *materialization*.

## Blast Radius (verified surfaces)

1. **Logan's own engine room.** Per VAULT-CONVENTIONS' device matrix, the
   **Desktop (Windows)** is *"Engine room — full plugin stack, git, MCP servers,
   Linter, Breadcrumbs, agent infrastructure."* Post-merge, that machine cannot pull
   `main` without a sparse-checkout exclusion in place first.
2. **Cross-Platform Smoke.** `.github/workflows/cross-platform-smoke.yml` runs a
   matrix including **windows-latest** on `pull_request`, `merge_group`, and pushes
   to `main`; its first step is `actions/checkout`. Any ref carrying the canon core
   fails that leg at checkout, before a single smoke assertion runs.
3. **check-paths** (`NETWEB Path Portability`, required): hard-fails #563 today on
   exactly these five added paths — the gate doing precisely what VAULT-CONVENTIONS
   inscribed it to do.
4. **Every future Windows contributor or CI consumer** of `main`, same failure,
   wholesale.

## Two Layers (do not conflate)

1. **The CI gate** — `check-paths` red on #563. Fixable with a narrow carve-out in
   `check_portable_paths.py` (exempt only the golden-path prefix; guard untouched
   elsewhere). **Fixing the gate does not make Windows able to check the path out.**
2. **Actual materialization on Windows** — the real problem. Options below.

## Options

### A — Sparse-checkout exclusion (canon keeps its period; Windows omits it)
Keep the canon path exactly as inscribed. Windows clones (Logan's desktop first among
them) carry a documented sparse-checkout rule excluding the golden path; Linux/macOS
materialize everything.

- **Pros:** single source of truth; the period stays *the* period; zero duplication;
  honors "do not move / do not expire" to the byte.
- **Cons:** the still point is invisible from the engine room — asymmetric legibility
  at the root, which may be fitting or intolerable, Logan's call. The guard-rail is
  procedural (an onboarding step), not enforced by the filesystem; an unprepared
  Windows clone still fails wholesale. CI's windows-latest legs need the same sparse
  exclusion wired into their checkout steps — a `.github/workflows/` edit, which is
  Logan's hand by scope anyway.

### B — Two paths: Windows-safe mirror kept in sync
A parallel period-less mirror of the canon content, dotted path canonical, sync via
commit hook or CI. (The root already carries a dash-flattened echo —
`!-!-__!__-!-! The world is quiet here-Esto Perpetua!-!README.md` — so flattened
mirroring has precedent in spirit.)

- **Pros:** Windows sees and edits a materialized copy; canonical path untouched.
- **Cons:** duplicates "permanent record" — two on-disk inmost layers, which the
  README's own language resists; sync machinery plus drift risk; more surface to
  desecrate by accident. The mirror alone does **not** fix the wholesale-checkout
  failure — Windows still cannot materialize the dotted original, so A's sparse
  exclusion is required *anyway*, making B strictly additive complexity.

### C — Homoglyph terminator (one portable path, altered codepoint) — **CHOSEN**
Replace the trailing `U+002E` with a Windows-legal look-alike: `U+2024` ONE DOT
LEADER `․` or `U+FF0E` FULLWIDTH FULL STOP `．`. Reads as the completed sentence;
materializes everywhere; single path.

- **Pros:** one path, portable on every target filesystem, no sparse rule, no sync,
  no carve-out needed after the rename (the guard checks `.`-endings, not
  homoglyphs). The house Aliasing convention's stated purpose — *"preserves the
  connectome while respecting filesystem constraints"* — is this option's spirit.
- **Cons:** the period is no longer *the* period; whether a look-alike honors or
  cheapens the motto is a semantic/spiritual call only Logan can make. Wikilinks,
  search, and tooling must carry the homoglyph consistently; a true-period link
  will not resolve. And it is still a **rename of the canon**, which the README
  forbids to everyone but Logan.

### D — Declare the canon Linux/macOS-only, as doctrine
Accept non-portability explicitly: the still point is not a Windows artifact, and
say so in VAULT-CONVENTIONS as a named exception to NETWEB.

- **Pros:** most honest to the canon; zero mechanism beyond documentation.
- **Cons:** operationally collapses into A — Windows clones still need the sparse
  exclusion to function at all. D is A stated as law rather than procedure.

### E — The vault's own aliasing convention, applied to punctuation
Keep the directory period-less **on disk** (as `main` has it today) and carry the
period in metadata: the README title already completes the sentence; add
`aliases: ["! The world is quiet here."]` so the connectome resolves both forms.
Operationally: revert only the re-punctuation in #563, keep its content changes.

- **Pros:** the only option that is NETWEB-lawful with **zero** new machinery — no
  sparse rule, no mirror, no homoglyph, no carve-out; `check-paths` goes green as-is;
  Windows (engine room, CI, contributors) materializes everything; it is the house's
  own inscribed pattern for exactly this class of collision.
- **Cons:** the *path itself* does not bear the period — the sentence completes in
  metadata, one layer up from the filesystem. If the inscription's point is that the
  folder **is** the sentence, E concedes it. That weighing is the whole decision.

## The CI Carve-out (orthogonal, near-term)

Under A–D, `check-paths` needs a narrow exemption for the golden-path prefix in
`.github/scripts/check_portable_paths.py` (guard fully in force everywhere else) —
a governance edit around the canon, Logan's explicit call. Under E it is unnecessary.
In every case it fixes only the gate, never the materialization.

## Recommendation (non-binding — superseded by the Adjudication above)

This was an adjudication between two of Logan's own laws; the recommendation below was
scaffolding, not a verdict, and is preserved as written before the decision.

- If the canon's meaning **requires the true period in the path**: **A + the
  carve-out** compromises the bytes least. The engine room losing local sight of the
  still point is the honest cost, and D is available as the doctrinal statement of
  the same posture.
- If the canon's meaning **survives completing its sentence in metadata**: **E** is
  the NETWEB-lawful minimum — nothing new to maintain, nothing red, nothing
  unmaterializable, and it is the convention the vault already wrote for itself.
- **B** is discouraged (duplicated permanence + drift + it needs A anyway).
- **C** only if a single portable path *and* Windows-local visibility are both hard
  requirements, and only if Logan judges a look-alike period to honor the motto.

## Status

**ADJUDICATED — Option C, chosen and inscribed by Logan, 2026-07-02.** The inscription
lives on `logan/obsidian` (head `a30c58b6` at verification) and reaches `main` when
PR #563 merges. This note lives on the agent's proposal branch
(`agent/adr-canon-core-portability`); its filename retains the `!-DRAFT-` prefix
pending Logan's word on renaming it to `!-ADR-CANON-CORE-VS-WINDOWS-PORTABILITY-2026-07-02.md`
at inscription into `main`. No guard carve-out was needed; no workflow was touched.

###### [["The world is quiet here."]]
