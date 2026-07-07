---
title: NORMALIZATION — Character Conformity and Mojibake Sweeping
status: proposed
authority: LOGAN
date created: 2026-07-07
related:
  - VAULT-CONVENTIONS
  - CONSTITUTION
  - "!README.md"
---

# NORMALIZATION — Character Conformity and Mojibake Sweeping

*A general program, portable to any LAF-US surface. This document proposes the
program's shape; the norm decisions inside it are reserved to Logan. Tracking
issue: #794.*

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
   back (`â€"` where `—` was meant; `Ã©` for `é`). Survives as *valid* UTF-8,
   so encoding checks alone never catch it; requires pattern sweeping
   (ftfy-class heuristics) with human-reviewable diffs, because repairs are
   interpretive.
3. **Homoglyph / codepoint nonconformity** — valid UTF-8, wrong characters:
   Cyrillic `е` in Latin text, non-breaking spaces posing as spaces,
   smart-quote or dash variants where the norm says otherwise. Pure policy
   territory: what the norm permits decides what the sweep flags.

## The Norm — Decision Points Reserved to Logan

- **N1 — Declared encoding.** UTF-8 without BOM everywhere? Any exempt
  surfaces beyond binary formats?
- **N2 — Chamber sovereignty vs. conformity.** Most current offenders are
  `.*/` dotfolder chambers — personal agent surfaces under CONSTITUTION § I
  handle-with-care. Candidate postures, one to be chosen: **(a) override** —
  bytes are infrastructure, not voice; encoding conformity applies everywhere
  and chamber *content* is never altered, only its byte representation;
  **(b) consent** — chambers are swept only after a per-chamber notice window
  (a flag file or issue mention) passes without objection; **(c) exempt** —
  chambers are excluded from the sweep and only warned on, accepting that
  strict readers will keep crashing on them.
- **N3 — Codepoint policy.** Are homoglyphs categorically nonconforming in
  prose? Are typographic characters (em-dash, curly quotes) welcome as
  *UTF-8 codepoints* — the vault's own style is em-dash-heavy — with only
  their *mis-encodings* swept? Sub-question: do **verbatim exhibits** (quoted
  lyrics, witnessed external text) get normalized or preserved byte-exact?
  Precedent cuts both ways — #638 normalized Cyrillic homoglyphs *inside* a
  lyric exhibit deliberately; a fidelity-first reading would have kept them
  and flagged instead.
- **N4 — Mojibake repair authority.** Layer-1 re-encoding is provably
  reversible; layer-2 mojibake repair is interpretive. Per-file human review,
  or a well-tested heuristic pass with the diff as the record? Candidate
  limits if heuristics are allowed: in-scope only the closed families of
  known double-decode artifacts (UTF-8 read as cp1252/latin-1 and re-saved —
  the `â€"`/`Ã©` class), applied only where the repaired text round-trips
  back to the observed bytes; everything else — ambiguous sequences,
  exhibits, anything that fails the round-trip proof — flagged for human
  eyes, never auto-repaired.
- **N5 — Portability.** The apparatus is written repo-agnostic (a checker and
  a sweeper any LAF-US repo can adopt), with `IDAHO-VAULT` merely its first
  deployment — confirm or narrow.

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
(https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd). Proposed, not
adopted; the norm is Logan's.*
