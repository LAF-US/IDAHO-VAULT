---
title: NORMALIZATION — Character Conformity and Mojibake Sweeping
status: active
authority: LOGAN
date created: 2026-07-07
date landed: 2026-07-08
related:
  - VAULT-CONVENTIONS
  - CONSTITUTION
  - "!README.md"
---

# NORMALIZATION — Character Conformity and Mojibake Sweeping

## Where this stands (2026-07-08)

This program is built and live in this repo. Nothing below is waiting on a
decision.

- **A check now runs on every change** and rejects any tracked text file that
  is not valid UTF-8. It is on and passing.
- **The wrong-encoding files were fixed** — about 145 of them, converted to
  UTF-8, each conversion reversible byte-for-byte so nothing was invented.
- **Garbled text and look-alike characters were swept** wherever the repair
  could be proven correct; anything that could not be proven is left visibly
  flagged rather than guessed at.
- One damaged document, `PLUGIN-TRIAGE.md`, was recovered from a broken
  encoding; a single character on one row could not be recovered and is
  marked plainly in the file.

The rest of this document is the original program design and the record of the
norm answers, kept for reference.

---

*A general program, portable to any LAF-US surface. The norm decisions were
Logan's; he answered them on 2026-07-08 (N1 in chat, N2–N4 via the ask-user
tool, quoted verbatim below; N5 settled by his framing at creation).*

---

## What This Is

One declared character norm, a sweeping apparatus that detects and repairs
nonconforming bytes (wrong encodings, mojibake, homoglyphs), and loud-failing
enforcement so drift cannot silently re-accumulate.

This is the **content-byte sibling of NETWEB**: NETWEB (VAULT-CONVENTIONS §
"Portable Path Standard") governs what characters may appear in *paths*;
nothing yet governs what bytes may appear in *file contents*. The program is
framed per the #626 ordering: **norm → prescription → enforcement** — nothing
is prescribed here ahead of the norm being set.

## Evidence the Disorder Is Real

Grounded instances, all from `IDAHO-VAULT` (the program's first deployment
surface, not its boundary):

- **2026-07-07 — 166 tracked files are not valid UTF-8.** Found when the
  Codacy Security Scan crashed (`MalformedInputException`) on PR #793, a
  one-test PR that merely drew the short straw. The byte signature is
  systematic — one generator's fingerprint: every `.*/CHAMBER.md` persona
  anchor carries a cp1252 em-dash byte (`0x97`); every `.*/stub.txt` wildcard
  stub opens with latin-1 `0xbf` (`¿`). Written by a cp1252 writer, read for
  weeks by tolerant readers, exposed only when a strict reader touched them.
  (Reproduction and adjudication: PR #793, comment 4907500812.)
- **2026-06 — Cyrillic homoglyphs in Latin prose.** Two Cyrillic `е`
  homoglyphs found embedded in a lyric exhibit and normalized to Latin during
  the #638 review — the same disorder class at the *codepoint* level rather
  than the byte level.
- **Consequence class:** strict readers crash or mis-scan (Codacy, above; any
  future tool that assumes UTF-8); search and diff silently miss content — a
  UTF-8 `grep` never matches a cp1252 byte sequence; homoglyphs defeat search
  and deduplication entirely while looking identical on screen.

## The Three Layers of the Disorder

1. **Encoding nonconformity** — bytes that are not the declared encoding at
   all (cp1252/latin-1 files in a UTF-8 world). Detectable mechanically;
   repair is decode-with-correct-charset → re-encode, byte-reversible and
   verifiable.
2. **Mojibake** — text already garbled by a past wrong decode being written
   back: an em-dash `—` whose UTF-8 bytes `E2 80 94` were once re-read as
   cp1252 becomes a three-character artifact; `é`'s bytes `C3 A9` likewise
   become a two-character one. (Specimens are named by their bytes here
   deliberately, so this document never carries live artifacts that a
   layer-2 sweep would "repair" out of its own definitions.) Survives as
   *valid* UTF-8, so encoding checks alone never catch it; requires pattern
   sweeping with human-reviewable diffs, because repairs are interpretive.
3. **Homoglyph / codepoint nonconformity** — valid UTF-8, wrong characters:
   Cyrillic `е` in Latin text, non-breaking spaces posing as spaces,
   smart-quote or dash variants where the norm says otherwise. Pure policy
   territory: what the norm permits decides what the sweep flags.

## The Norm — Rulings and Open Points

Rulings N2–N4 were given by Logan on 2026-07-08 through the Claude Code
ask-user tool in the live session (`session_01Fipj4vEJ5ADPuunn9ed5Hd`), and
N1 in chat the same day; each answer is quoted verbatim. N5 was settled
earlier by his framing directive.

- **N1 — Declared encoding. RULED: BOM-aware UTF-8.** Logan's answer,
  given in chat on 2026-07-08: **"BOM-aware UTF-8"**. Operational reading
  (implementation's, marked as such): the declared encoding is UTF-8; a
  single leading byte-order mark is recognized as a BOM — not content, not
  an offense — and the apparatus never *adds* one; any byte sequence not
  decodable as UTF-8 is nonconforming. *Record of the road here: the two
  earlier ask-tool responses each consisted of a single FULLWIDTH FULL STOP
  (U+FF0E) — first `(．)`, then `．` — held as uninterpretable rather than
  guessed at, until Logan reproduced the same character deliberately in
  chat (a live layer-3 specimen: valid UTF-8, homoglyph of the period,
  invisible to any encoding gate) and then ruled N1 in words.*
- **N2 — Chamber sovereignty vs. conformity. RULED: override.** Logan's
  answer: **"Override (Recommended)"** — of the candidate postures
  (override / consent / exempt), the override posture governs: bytes are
  infrastructure, not voice; encoding conformity applies everywhere,
  including `.*/` dotfolder chambers, and chamber *content* is never
  altered — only its byte representation.
- **N3 — Codepoint policy (exhibits sub-question). RULED: normalize
  exhibits too.** Logan's answer: **"Normalize exhibits too"** — the #638
  precedent (Cyrillic homoglyphs normalized *inside* a lyric exhibit)
  generalizes: verbatim exhibits are normalized like any other prose, not
  preserved byte-exact. The remaining N3 body (whether homoglyphs are
  categorically nonconforming; whether typographic characters are welcome
  as UTF-8 codepoints with only their mis-encodings swept) follows the
  direction this ruling sets but has not been separately enumerated.
- **N4 — Mojibake repair authority. RULED: bounded heuristics.** Logan's
  answer: **"Bounded heuristics (Recommended)"** — heuristic repair is
  allowed within the stated limits: in-scope only the closed families of
  known double-decode artifacts (UTF-8 read as cp1252/latin-1 and re-saved —
  the `C3 A9`-for-`é` class), applied only where the repaired text
  round-trips back to the observed bytes; everything else — ambiguous
  sequences, anything that fails the round-trip proof — flagged for human
  eyes, never auto-repaired.
- **N5 — Portability. SETTLED by directive.** Logan's directive at the
  program's creation (2026-07-07): the program is *"general, not specific
  to this repo."* The apparatus is written repo-agnostic (a checker and a
  sweeper any LAF-US repo can adopt), with `IDAHO-VAULT` merely its first
  deployment.

## Prescription and Enforcement (falls out of the answers)

- A **conformity checker** in the established trusted-validator pattern: red
  on any tracked text file violating the declared norm — encoding first,
  codepoint rules per N3. Runs per-PR so new drift dies at the door.
  **Text/binary discrimination is part of the checker's contract, not left
  to chance:** a file is treated as text only if it passes all three gates —
  (1) not marked binary by `.gitattributes`, (2) extension on the declared
  text list (the NETWEB doc pattern: an explicit list, no heuristic
  grandfathering), (3) no NUL byte in the first 8 KiB. Files failing the
  gates are skipped as binary; files that are *ambiguous* (text-listed
  extension but NUL bytes, or vice versa) are flagged for a human — the
  checker never silently guesses.
- A **sweeper** for the existing debt: layer 1 mechanically (decode →
  re-encode, reversibility verified byte-for-byte), layers 2–3 per N4/N3,
  all on dedicated branches with reviewable diffs.
- **Done when (enforced, fails loud):** the checker exists and is red against
  today's state (the 166 known offenders prove detection), then green after
  the sweep lands, then guards permanently. An unenforced write-up of the
  rule is debris, per #626's definition of done.

## Anchors

- PR #793 — the detector event (Codacy crash) and its adjudication
- Issue #794 — tracking issue for this program
- `VAULT-CONVENTIONS.md` § "Portable Path Standard (NETWEB)" — the path-side
  sibling; § "Character Set & Notation"
- #638 record — the Cyrillic-homoglyph normalization precedent
- CONSTITUTION § I — dotfolder chamber handling (bears on N2)

---

*Recorded by Claude Code session `session_01Fipj4vEJ5ADPuunn9ed5Hd`
(<https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd>). The norms are
Logan's, answered 2026-07-08; the apparatus is built and enforcing.*
