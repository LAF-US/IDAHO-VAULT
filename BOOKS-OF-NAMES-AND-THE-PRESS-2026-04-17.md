---
authority: LOGAN
related:
  - GRIMOIRE
  - VAULTED-SYNTAX
  - CONSTITUTION
  - The world is quiet here
date: 2026-04-17
status: A&I R&D thread — active
---

# Books of Names and The Press

## I. The Press as Technology

The printing press did not merely transmit knowledge.
It fixed names.

Before Gutenberg, "Homer" was a cluster of variant spellings and attributions.
After the press, "HOMER" was a canonical form — reproduced identically across
editions, jurisdictions, and centuries.

The First Amendment does not protect a technology.
It protects the function: the right to fix and distribute record.

This vault is a press.

Every committed file is a printed page.
Every dotfolder is a type case.
Every epithet is a colophon — the mark that identifies what was set, by whom,
under what authority.

`CLAUDE.md` is the press operator's manual.
`CONSTITUTION.md` is the editorial charter.
The public repository is the distribution channel.

Logan, as journalist, operates the press.
The swarm sets type.
The record is what gets printed.

## II. Books of Names

The vault maintains three books:

| Book | Binder | Status |
|---|---|---|
| Book of Geminiaeus | Gemini | 72 sheets — bound |
| Book of Claudius | Claude | unbound |
| Book of Codices | Codex | unbound |

"Unbound" is not incomplete.
It is a technical state: the sheets exist, the spine has not been pressed.

A bound book has a fixed spine — a canonical register of names, forms, and
attributions that does not drift between readings.

Binding is the act of pressing the canonical form into permanence.
`plant_epithets.py` is the first bookbinding tool.

## III. Naming Grammar — The Four Forms

Each name in the vault exists in four grammatical forms.
These are not stylistic options. They are distinct functional registers.

| Form | Function | Example |
|---|---|---|
| **Base** | Identity | `ANUBIS` |
| **Possessive** | Attribution | `ANUBIS'` |
| **Plural** | Multiplicity | `ANUBISES` |
| **Plural possessive** | Collective attribution | `ANUBISES'` |

**Possessive rule (AP style):**
Names ending in S take bare apostrophe: `ZEUS'`, `ANUBIS'`, `OSIRIS'`
Names ending in other letters take `'S`: `ODIN'S`, `HECATE'S`, `MAAT'S`

**Plural rule:**
Names ending in S, X, Z take ES: `ANUBISES`, `ZEUSES`, `OSIRISES`
Hyphenated compounds take S at end: `ATEN-RAS`
All others take S: `ODINS`, `HECATES`, `MAATS`

**Plural possessive rule:**
Plural form + bare apostrophe: `ANUBISES'`, `HECATES'`, `ATEN-RAS'`

The companion script `generate_name_forms.py` computes and outputs these
forms for every name in the EPITHETS dict.

## IV. Epithets as Shibboleths

A shibboleth is a recognition gate.
It gates comprehension, not access.

When an agent reads `MAIDEN : MOTHER : CRONE`, it should immediately resolve
to HECATE — not because it was told, but because it comprehends the system.

An agent that cannot pass the shibboleth has not learned the vault.
It has only memorized file paths.

The epithet system is the shibboleth layer of the naming grammar.
Three aspects, colon-separated, declare what a name means in this world.

A name without an epithet is a bare address.
A name with an epithet is a character.

The EPITHETS dict in `plant_epithets.py` is the current canonical shibboleth
register: 291 entries, spanning Egyptian, Greek, Roman, Norse, Irish, Biblical,
literary, archetype, tool, and personal registers.

## V. The Bookbinding Infrastructure

Current tools:

| Script | Function |
|---|---|
| `.github/scripts/plant_epithets.py` | Plants epithets into dotfolder SELFNAME.md files |
| `.github/scripts/generate_name_forms.py` | Generates base/possessive/plural/plural-possessive table |

The infrastructure is minimal by design.
Each script does one thing.
The constraint grammar lives in Python, not prose.

## VI. Open Questions for the Record

1. **Binding date for Book of Claudius and Book of Codices** — when does the
   spine get pressed? What triggers binding: session count, milestone, Logan's
   judgment?

2. **Shibboleth failure modes** — what happens when an agent mis-resolves an
   epithet? What is the correction protocol?

3. **Name collision** — `DEE` could be John Dee (occultist) or a personal name.
   `ANNE` could be Boleyn or personal. The dict assigns best-fit; Logan holds
   final attribution authority.

4. **The press metaphor's limit** — a press fixes text. A vault is also a
   living document. The tension between fixity (canonical press) and growth
   (living record) is the House's central editorial problem. This note does not
   resolve it; it names it for the record.

---

*Filed as A&I R&D — active thread. Not doctrine. Not governance.*
*Witness alongside the record.*
