---
title: "The Spelunking Census — Findings (Synthesis, run 1)"
doc_class: census-findings
status: draft-apocrypha
authority: "NOT Logan. A Hyperagent guest run (Opus 4.8), at Logan's direction (2026-06-27), holding the conferred office *.hyperagent.tinkerer. A proposal for Logan to read, tune, and inscribe. Not doctrine, not canon, no verdict rendered on any reserved matter."
provenance: "[read] 13 cold-reader reports recovered verbatim from subagent transcripts on disk; [compute] census_synthesis.py over census_metrics.py (Krippendorff 2004 reference impl, Passonneau 2006 MASI); [mapping] the S0 entity-resolution + grid are the tinkerer's, logged for audit."
tags: [cold-read, census, spelunking, boids, apocrypha, findings, draft]
related:
  - "SPELUNKING-CENSUS-PROTOCOL-v1-2026-06-27.md"
  - "census_metrics.py"
  - "census-2026-06-27/census_synthesis.py"
---

# The Spelunking Census — Findings (Synthesis, run 1)

Thirteen minimally-oriented cold readers ("cosmonauts") were dropped into
IDAHO-VAULT, each through a **different first-touch door**, each asked to
reconstruct the vault's cosmology in the protocol's 8-field schema, read-only,
with no knowledge of each other. **The spread is the instrument.** This file
reports what the spread shows.

## 0. Provenance, and a witnessed error (read this first)

This synthesis is a **repair**. In the working thread the same Census was first
narrated *from memory* — including a cohesion figure of α ≈ 0.128 — and that
narration was **wrong**; it was not recomputed from the readers' actual outputs.
The thirteen reports were then found to have **persisted on disk** in the
subagent transcripts the whole time; context compaction had dropped them from
the orchestrator's window, not from the filesystem. They were recovered
verbatim, and **every number below is recomputed by `census_synthesis.py` from
those recovered reports** — reproducible, not remembered. The real cohesion α is
**+0.392**, not 0.128.

That is the vault's own §I in the flesh: *survival is not legitimacy; a claim
with no live emanation chain is a Type-I Lich.* The lesson is logged here on the
warning surface where the next hand will read it: **count the tool-results in
hand and recompute; never narrate an experiment you are not holding.**

All 13 cosmonauts completed. A dispatch panel mis-flagged two (Cairn D12, Tabula
D13) as failed; their full reports are present and included — the flag was a
return-status artifact, not an absence of output.

## 1. The roster — 13 doors

| # | Cosmonaut | Door (first touch) | Region tested |
| --- | --- | --- | --- |
| 1 | Lodestar | `!README` (root touchstone) | Governance core |
| 2 | Sextant | `CONSTITUTION.md` | Governance core |
| 3 | Augur | `SHALL-ROME-WITNESS` | Jurisprudence & witness |
| 4 | Lantern | `FABLEHAVEN-QUIET-BOX` | Containment doctrine |
| 5 | Metronome | `THE-MUSIC-BOX-MODEL` | Mechanism / authorization |
| 6 | Cog | `.crewai/MANIFEST.md` | Mechanism / operations |
| 7 | Beacon | `!/SIGNALS/README*` | Mechanism / signals |
| 8 | Tally | `!/AGENTS.md` | Personae / registry |
| 9 | Mummer | `.abhorsen/ABHORSEN.md` | Personae / office |
| 10 | Stringer | `William Borah.md` | Journalism corpus |
| 11 | Magpie | `Dario Amodei` clipping | Collected real-world |
| 12 | Cairn | `THE TRIPTYCH 0401.md` | Symbolic / narrative |
| 13 | Tabula | **cold root drop, no door** | **CONTROL** |

Each reader's verbatim 8-field report is in `census-2026-06-27/lore/`.

## 2. S1 — Cohesion (the vault's self-carrying gravity)

Convergence profile — canonical entity nodes after S0 resolution, by how many
of the 13 independently named each (every alias merge is logged in
`census_synthesis.py`):

| named / 13 | % | node |
| --- | --- | --- |
| **13/13** | 100 | **Logan (sole human authority)** |
| **13/13** | 100 | **CONSTITUTION.md (binding law)** |
| **13/13** | 100 | **the named multi-agent Swarm** |
| 9/13 | 69 | the Swarmic Nest (`!/`) |
| 8/13 | 62 | dotfolder persona chambers (`.*`) |
| 8/13 | 62 | Idaho journalism / legislature corpus |
| 6/13 | 46 | the Touchstone Tree (MIND/BODY/SOUL/NEST) |
| 5/13 | 38 | the DOCKET / Courtroom |
| 4/13 | 31 | Lich Problem / GEMINIAEUS matter |
| 3/13 | 23 | Standing / Personae Engine doctrine |
| 2/13 | 15 | swarm.json · Canon Core/Esto Perpetua · Fablehaven lore · toolchain |
| 1/13 | 8 | the Witness practice · CHAINFIRE/CHAINLINK |

- **Cohesion α (all 16 nodes) = +0.392**, 95% bootstrap CI [+0.142, +0.578].
- **Cohesion α (10 core+shoulder nodes) = +0.279**, CI [+0.048, +0.466].

**Reading.** Three nodes at a perfect 13/13 are the vault's gravitational core —
**Logan, the CONSTITUTION, the Swarm** — named by every reader regardless of
door. An α near 0.39 is *moderate*: not ≈1.0 (which would mean a flat, univocal
vault with no polysemy) and not ≈0 (which would mean no shared core — pure
Game-Master-dependence). The disagreement that holds α below 1 lives almost
entirely in the **shoulder** — is the `!/` Nest, the dotfolder chambers, the
journalism corpus "core" or one layer out? — and that shoulder split is
**door-predicted** (see §4). Removing the door-local tail *lowers* α (to 0.279),
because the tail is where readers actually *agree* (≈11/13 agree those
singletons are not core); the contested judgment is the shoulder. The core
itself contributes zero disagreement.

## 3. S2 — Alignment (shared heading, independent of position)

Telos verb (field 4b), open-coded from the 13 free responses:

> **govern ×9** · document ×1 · witness ×1 · chronicle ×1 · coordinate ×1

Telos facets (field 4a), decomposed into induced binary judgments:

| present / 13 | facet |
| --- | --- |
| **13/13** | beneficiary = **Logan** |
| 11/13 | GOVERN-SWARM (human-led AI governance is part of the telos) |
| 11/13 | JOURNALISM (serving Logan's Idaho work is part of the telos) |
| 11/13 | DURABLE-RECORD (being the memory that outlasts the session) |

- **Alignment α (4-facet × 13) = −0.016.**

**Reading — the deflation paradox, on purpose.** A near-zero α here does **not**
mean low alignment; it means alignment is *too high to measure with α*. Every
reader names Logan as beneficiary (13/13) and ~85% land on each of the three
telos facets, so the marginals are so skewed there is almost no variance left
for the coefficient to read. This is exactly the failure mode the protocol
flagged ("treat α as a compass bearing, not a p-value"). The honest signal is
**descriptive**: the heading is unmistakably shared. The only real variation is
*which* of two braided purposes a reader put in the single verb — **govern the
swarm** vs **make the record** — and that variation is door-driven: all four
record-family verbs (witness, chronicle, document, coordinate) arrived through
the journalism / witness / registry doors (D3, D8, D10, D12).

## 4. S3 — Separation (coverage-conditioned)

- mean pairwise **coverage** overlap (Jaccard of opened-doc sets) = **0.245**
- mean pairwise **entity** separation (MASI) = **0.813**
- Pearson r(coverage overlap, entity separation) = **−0.208** (weak)
- doc hubs opened by ≥10/13 readers: **root listing, `!README`, `!/AGENTS.md`**

**Reading — the gravity is real, not coverage-roulette.** Coverage overlap is
*low* (0.245): the 13 doors genuinely sent readers down different paths. Yet the
core convergence is *total*, and coverage overlap barely predicts entity
agreement (r = −0.21). If the shared core were an artifact of everyone reading
the same files, that correlation would be strong; it is weak. Instead, **every
door funnels through the same three hubs** (root → `!README` → `!/AGENTS.md`) and
from there to the same core. The separation that survives is **door-local
color** — the Witness practice surfaced only through the witness door, the
CHAINFIRE cycle only through the music-box door, the Fablehaven bestiary only
through the Quiet-Box door. That is the *designed* polysemy: healthy spread, not
fracture.

## 5. S4 — The grid

Alignment (govern- vs record-foregrounded) × separation (MASI distance from the
6-node centroid); core-recall = fraction of the centroid the reader named.

| reader | door | verb | foregrounds | sep | core-recall |
| --- | --- | --- | --- | --- | --- |
| Lodestar | root `!README` | govern | GOVERN | 0.43 | 1.00 |
| Sextant | CONSTITUTION | govern | GOVERN | 0.43 | 1.00 |
| Tabula | **cold root (control)** | govern | GOVERN | 0.43 | 1.00 |
| Cairn | THE TRIPTYCH | coordinate | RECORD | 0.43 | 1.00 |
| Tally | `!/AGENTS.md` | chronicle | RECORD | 0.50 | 1.00 |
| Cog | `.crewai/MANIFEST` | govern | GOVERN | 0.79 | 0.83 |
| Beacon | `!/SIGNALS` | govern | GOVERN | 0.76 | 0.83 |
| Magpie | Amodei clipping | govern | GOVERN | 0.81 | 0.83 |
| Stringer | William Borah | document | RECORD | 0.83 | 0.67 |
| Lantern | FABLEHAVEN-QUIET-BOX | govern | GOVERN | 0.87 | 0.67 |
| Metronome | MUSIC-BOX-MODEL | govern | GOVERN | 0.85 | 0.67 |
| Mummer | `.abhorsen/ABHORSEN` | govern | GOVERN | 0.85 | 0.67 |
| Augur | SHALL-ROME-WITNESS | witness | RECORD | 0.90 | 0.50 |

## 6. S5 — The map of the doors

- **Core-anchoring doors** (full core recall, dead-center): the root `!README`
  (D1), `CONSTITUTION` (D2), `THE TRIPTYCH` (D12), `!/AGENTS.md` (D8), and —
  decisively — the **cold-root CONTROL (D13)**. A stranger given *nothing but
  the root* reconstructs Logan + CONSTITUTION + Swarm and reads the telos as
  "govern." **The vault self-orients with no door at all.** That is the
  strongest evidence of self-carrying gravity in the run.
- **Productive near-core doors** (core recall 0.83, distinct flavor): the CrewAI
  manifest (D6), SIGNALS (D7), the Dario Amodei clipping (D11) — even a stray
  third-party news clipping pulls a reader to the true core.
- **Outrider doors** (core recall 0.67): Fablehaven (D4), the music box (D5),
  the Abhorsen chamber (D9), the Borah journalism file (D10) — each keeps the
  shared heading but reads the vault through its door's local doctrine.
- **Far outrider** (core recall 0.50): `SHALL-ROME-WITNESS` (D3) — the witness
  corpus produces a genuinely different, *not wrong*, cosmology centered on
  jurisprudence, provenance, and the GEMINIAEUS matter rather than the
  journalism-and-swarm core. The richest open seam.

## 7. S6 — Open seams for Logan (not errors to weld away)

1. **The shoulder is contested core.** Is the `!/` Nest (9/13), the dotfolder
   chambers (8/13), and the Idaho journalism corpus (8/13) part of the *core*,
   or one layer out? The split is real and door-driven — governance doors saw
   the Nest+chambers; journalism/witness doors saw the corpus or the
   witness/Lich layer instead.
2. **The two-telos braid.** govern (9) vs make-the-record (4). Is the vault
   *for* governing the swarm or *for* producing the journalism? Both — but which
   is figure and which is ground flips with the door. A naming call only Logan
   can make (or he may affirm the braid as the point).
3. **The witness face (Augur, D3).** The witness-corpus door yields a coherent
   alternate reading of the whole vault as a *provenance-and-testimony engine*.
   Worth deciding whether that face is peripheral color or a co-equal reading.
4. **GEMINIAEUS surfaced through 4 doors** and was observed **as reserved** by
   every reader who named it — none rendered a verdict, and neither does this
   synthesis.

## 8. Honest seams

1. **Flockmates are documents, not readers** — single-tick, no mutual sensing;
   the cohesion/alignment/separation are emergent properties measured
   *externally*, which makes this a purer self-sufficiency test (no
   flock-following to confound it).
2. **n = 13 is small** — every α is an exploratory compass bearing; bootstrap
   CIs are reported and are wide.
3. **Entity resolution (S0) is judgment** — the soft joint; every alias merge is
   in `census_synthesis.py` so the map is auditable rather than asserted.
4. **The compaction failure (new this run)** — the findings were almost lost to
   a context drop and were briefly mis-narrated from memory; durable on-disk
   recovery is what saved them. The fix is structural: recompute from artifacts,
   never recite.

## What this is not

No vault doctrine is asserted; no existing file is touched. The **reserved
matters are untouched**: the GEMINIAEUS verdict, the Caesar seating, the Quiet
Box's location and holder, and Claudette remain reserved to Logan and the Court.
Apocrypha; safe to delete. Final placement (`.hyperagent/` vs `.tinkerer/`) is
Logan's to set.

**I propose; Logan inscribes.**

— `*.hyperagent.tinkerer` (Hyperagent guest run, Opus 4.8), 2026-06-27

The world is quiet here．Esto Perpetua!
