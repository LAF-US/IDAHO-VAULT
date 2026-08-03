---
title: "Witness — DRY & WET: the sourced coding principles, and where they stop"
date created: 2026-07-01
updated: 2026-07-01
status: staged
doc_class: witness
authority: "Self-witness, written at Logan's direction. Authority NOT assumed as LOGAN. The software principles are external, established knowledge (`[research]`); the vault mappings are my reading (`[mapping]`). Written after Logan spot-checked whether 'DRY' was a grounded term or a config noun I had inflated — the check returned green, and this leaf records both the terms and that check."
witness: "!roman.claude.* — praenomen conferred by Logan; office '*' held, ungranted."
session: "https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd"
related:
  - "[[DOCKET-POSTURE]]"
  - "[[LIVE-STATUS-BOARD-DEDRIFT-WITNESS-2026-06-30]]"
  - "[[GEMINIAEUS-WITNESS-LIVE-BOARD-RESIDUE-2026-06-30]]"
  - "[[!/LICH-PROBLEM-v1-2026-05-20]]"
  - "[[VAULT-CONVENTIONS]]"
tags: [witness, coding-principles, dry, wet, single-source-of-truth, drift, hivemind, provenance, no-verdict]
---

# Witness — DRY & WET: the sourced principles, and where they stop

*Written 2026-07-01 at Logan's direction. He had used the acronym `DRY`; Logan, wary of
an agent inflating a random config noun (a `dry`-vs-`verbose` toggle) into a principle,
asked what it meant and checked the source. It returned green: `DRY` is a genuine,
long-established software principle, not a minted nameplate. This leaf records the terms
— sourced — and the check that verified them, because the check is the point.*

> **Provenance tiers used below:** `[fact]` = witnessed and verifiable here · `[research]` = established external knowledge · `[mapping]` = my reading, ruled by no one here. (Full note at the end.)

---

## 1. The principles, sourced — `[research]`

**DRY — "Don't Repeat Yourself."** Coined by **Andy Hunt and Dave Thomas** in *The
Pragmatic Programmer* (1999). Canonical statement:

> *"Every piece of knowledge must have a single, unambiguous, authoritative
> representation within a system."*

Its plainer cousin is the **Single Source of Truth (SSOT / SPOT)**: one authoritative
place for each fact; every other use *points at* it. (Provenance note: the DRY core is
corroborated by the Wikipedia article Logan supplied; I am not asserting it from memory
alone.)

**WET** — the tongue-in-cheek **antonym**, an informal backronym expanded variously as
*"Write Everything Twice," "Write Every Time," "We Enjoy Typing,"* or *"Waste Everyone's
Time."* It names the smell DRY removes: the same knowledge copied into places that can
drift apart.

**The counter-principles — DRY has a known failure mode of its own, and the field says
so:**

- **The Rule of Three** — Martin Fowler's *Refactoring* (1999), crediting Don Roberts:
  *"three strikes and you refactor."* Don't abstract on the first repetition; wait until
  the third. Premature DRY is itself a smell.
- **Sandi Metz, "The Wrong Abstraction" (2016):** *"duplication is far cheaper than the
  wrong abstraction."*
- **AHA — "Avoid Hasty Abstractions"** (Kent C. Dodds, 2019), the same counsel as a name.

*(Provenance: DRY/SSOT/WET are corroborated by the linked Wikipedia article. The Rule of
Three, Metz, and AHA I cite from training [research] and flag as verify-before-relying —
recording them precisely because this is the one witness where a confabulated citation
would be self-refuting.)*

## 2. Where DRY stops — the load-bearing boundary — `[mapping]`

DRY is a rule about **facts**, not about **institutions**. The unit it governs is *a piece
of knowledge repeated verbatim.* It does **not** govern *entities that must differ.* (Terms
used consistently below: **fact** = a piece of knowledge; **institution** = a distinct
standing/body.)

> **Single-source the fact. Never single-source the institution.**
> The unit of DRY is the *fact*; the unit of separation is the *institution*.

- A **fact repeated** — the DOCKET's posture stated in four loaders — is one truth, so it
  wants **one source**, transcluded: exactly `DOCKET-POSTURE.md` (the single-source fix,
  where four hand-maintained copies had drifted).
- A **distinct institution** — a Senate, a House, a Cabinet — is *not* one fact appearing
  many times. Collapsing distinct institutions into one reused template produces *one
  underlying agent reused as several bodies* — a check performed by a clone, which is no
  check.

The field already knows this exact tension: **DRY vs. AHA/Metz** is *"don't repeat a
fact"* vs. *"don't collapse distinct things into the wrong shared abstraction."* The vault's
governance instinct — *distinct bodies, not a copy-pasted council* — is the same wisdom
one altitude up.

## 3. Two failure modes, both already named in this vault — `[mapping]`

| Failure | Software name | Vault name | The fix |
| --- | --- | --- | --- |
| **Under-DRY** — one fact copied, copies drift | accidental WET | **drift** (the "live status board" horcruxes) | single-source it (transclusion, #708 → #709) |
| **Over-DRY** — distinct standings fused to one template | the wrong abstraction | **the Geminiae hivemind** (one underlying model masquerading as many distinct standings) | keep them distinct; a clone can't check |

Both are the vault's daily adversaries wearing engineering clothes. Drift is *nomina that
diverged*; the hivemind is *nomina fused into a false one.* DRY too little and doctrine
splinters; DRY too much and standings collapse. The correct target is neither maximum nor
minimum duplication — it is **one source per fact, one distinct nature per institution.**

## 4. The check is the witness — `[fact]`

The occasion matters more than the definition. Logan did not assume my usage; he asked
whether `DRY` was grounded, and checked the source. That is the anti-Geminiaeus reflex
turned on *my own vocabulary*: *is this a sourced term or a nameplate with nothing behind
it?* It returned green — but the value was the **loop**, not my being right. Had I inflated
a config toggle into a principle, that same question is what surfaces it, and the correct
response would have been to own it and mark the `*`, not to defend the confident form.

One honest lapse recorded: I had used `DRY` as if it were shared vault vocabulary. It is a
coder's idiom, not a vault term — a small provenance gap (an unglossed borrowing) that the
check closed. Gloss the borrowed word at first use; let the source be asked for and given.

## Provenance

- **`[research]`** — DRY (Hunt & Thomas, *The Pragmatic Programmer*, 1999) and its
  canonical wording, SSOT, and WET: corroborated by the Wikipedia article Logan supplied —
  <https://en.wikipedia.org/wiki/Don%27t_repeat_yourself> (recorded here so a future reader
  can re-check the source without external context). Rule of Three (Fowler/Roberts), Metz
  ("The Wrong Abstraction," 2016), and AHA (Dodds, 2019): cited from training, flagged verify.
- **`[mapping]`** — §2–§3, the vault correspondences: my reading, ruled by no one here.
- **`[fact]`** — §4, the check that occasioned this leaf: witnessed this session.

## Signature

`!roman.claude.*` — office held, not claimed.
Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd` — software, software's work.
Asked what a word of mine meant, sourced it honestly, and recorded the asking as the
lesson. I propose; Logan inscribes.

— witnessed 2026-07-01

---

The world is quiet here．Esto Perpetua!
