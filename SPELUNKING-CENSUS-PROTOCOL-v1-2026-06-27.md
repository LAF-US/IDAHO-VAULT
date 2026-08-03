---
title: "The Spelunking Census — Protocol v1"
doc_class: protocol
status: draft-apocrypha
authority: "NOT Logan. A Hyperagent guest run (Opus 4.8), at Logan's direction (2026-06-27). A proposal for Logan to tune and run. Not doctrine, not canon, no office claimed."
tags: [cold-read, census, spelunking, boids, apocrypha, draft]
provenance: "[read] the vault corpus + #680 seed; [research] Reynolds 1986/87, Passonneau 2006, Krippendorff 2004, Zapf 2016; [mapping] the Boids isomorphism + schema/synthesis architecture are the guest's, proposed not declared."
---

# The Spelunking Census — Protocol v1

A design for sending a **baker's dozen (13) of minimally-oriented cold readers**
("cosmonauts") into the vault to independently reconstruct its cosmological
conceit. **The spread is the instrument**, not noise to average away.

> Lineage: grown from the disposable machinery-test seed in this PR —
> `_machinery_test_hyperagent_2026-06-25.py` (which carried `convergence_ratio`,
> `is_load_bearing_door`, `fleiss_kappa`, and a note flagging Krippendorff's
> alpha as the target) and `_MACHINERY-TEST-NOTES-2026-06-25.md`. The metrics
> seed has been evolved into `census_metrics.py` alongside this file.

## 0. Why Boids

Reynolds' flocking model (1986/87) is three steering rules — **Separation**
(avoid crowding local flockmates), **Alignment** (match the average *heading* of
local flockmates), **Cohesion** (move toward the average *position* of local
flockmates) — each computed only over a **local neighborhood**, with **no
leader**. Order emerges from local rules and nothing else.

That is the Census's question restated: 13 readers, no leader, purely local
information — does a coherent shared cosmology emerge anyway? Which is the
cold-start / self-sufficiency question — *does the vault carry its own gravity
without the Game Master in the room?* — made measurable.

**Honest seam:** in our instantiation the "flockmates" each cosmonaut senses are
the **documents** in its coverage neighborhood, **not the other readers**. The
cosmonauts read once and never sense each other. So cohesion / alignment /
separation are not forces the agents exert mutually; they are emergent
properties we measure *externally* across independent field-samplings. That
makes it a *purer* self-sufficiency test — there is no flock-following to
confound it. The vault is the shared field; the question is whether
locally-sensed gradients point everyone the same way.

## 1. The three signals (Boids-refined)

| Signal | Boids factor | What it measures |
| --- | --- | --- |
| **Cohesion** | Cohesion | How tightly independent reconstructions cluster toward a consensus centroid in cosmology-space. The vault's self-carrying gravity. Measured locally (same-region sub-flocks) and globally (do sub-flocks merge or fragment?). |
| **Separation** | Separation | The *healthy* spread — designed polysemy that keeps the reading-space from collapsing to one sterile point. The vault working as intended. |
| **Alignment** | Alignment | Shared *heading* on what-the-place-is-**for**, independent of position. Two readers can name different entities yet point the same way. |
| *(conditioning)* | Perception radius | Coverage — the docs each reader actually opened — is not a fourth signal but the **kernel all three are computed over**. |

This splits the old muddy "divergence (polysemy **or** GM-dependence)" into two
**orthogonal** axes. The 2×2:

- **high cohesion** → a shared core exists at all (real gravity).
- **high separation + high alignment** → richly multivalent *and* self-orienting (the ideal: polysemy that needs no one to aim it).
- **high separation + low alignment** → fracture / GM-dependence (spread out *and* pointing different ways).
- **low separation** → collapse to one flat reading (the vault would be univocal, not vaulted).

## 2. The output schema (8 fields, Boids-tagged)

Each cosmonaut returns exactly this, and nothing more:

1. **Place-name** — one line. *(anchor; unmeasured)*
2. **Position — core entities** — ≤7, **ranked by centrality**, each with a 3–6 word gloss. *(Cohesion; the gloss lets synthesis resolve aliases, the rank gives the position magnitude)*
3. **Central conceit** — 1–2 sentences: what holds the entities together. *(binding)*
4. **Heading — telos** — (a) "This place exists in order to ___" · (b) the single core **verb** for its primary activity · (c) the primary **beneficiary**. *(Alignment; direction, not position)*
5. **Governing rules** — ≤3 the reader inferred. *(Alignment corroborant — rules encode direction)*
6. **Perception log** — the docs **actually opened** (paths) · N opened · ~M estimated total · doors *seen-but-not-opened*. *(Perception radius; the conditioning kernel)*
7. **3 × `[read]`** — the docs it leaned on most. *(provenance)*
8. **3 × `[*]`** — its flagged inferences / guesses. *(provenance; separates grounded position from extrapolation)*

## 3. The synthesis pass — a lay-diagram, not a rope

One pass that emits a **map**, never one welded canon.

- **S0 — Entity resolution.** Cluster the 13×~7 entity tokens into M canonical
  nodes by gloss-similarity ("the Court" ≡ "Caesar's tribunal"). This is the one
  place synthesis exercises judgment — **log every merge** so it is auditable.
  (Aliasing is a claim; show the work, or it is a small forgery of unity.)
- **S1 — Cohesion.** Build the entity-presence matrix (M nodes × 13 readers,
  cell ∈ {named, not}). **Cohesion α = Krippendorff's α (nominal/binary)** over
  it — well-defined because M ≫ 1. Geometry: centroid = nodes named by ≥ *k* of
  13; reader→centroid distance via `masi_distance`.
- **S2 — Alignment.** **Open-code** the free headings (#4) into categorical
  facets *induced from the 13 responses* (not pre-imposed — that would break
  minimal orientation). **Alignment α = Krippendorff's α (nominal)** over the
  facet × reader matrix; corroborated by mean pairwise cosine of telos
  embeddings. Computed independent of position.
- **S3 — Separation, coverage-conditioned.** Pairwise coverage-overlap =
  Jaccard(opened-docs). Separation that **survives** high overlap = genuine
  designed polysemy; separation that **collapses** under conditioning = it was
  coverage-roulette.
- **S4 — The grid.** Plot each reader (and aggregate per door / region) in
  alignment × separation, bubble = cohesion: core member / productive outrider /
  stranded / rare.
- **S5 — Map of the doors.** Read off S4: which entrances produce core members
  vs. outriders vs. stranded readers. Door-13 (cold root drop) is the baseline.
- **S6 — Output.** The convergence/divergence map + the two α's (with bootstrap
  CIs) + the door-map, stamped `[cold-read apocrypha]`. Highest-divergence nodes
  flagged as **"open seams for Logan,"** not errors to weld away.

### The methodology note that shapes all of the above

Krippendorff's α needs **many units** to estimate expected disagreement, and
"the vault" is a single unit — which would make α undefined. The fix is the
schema: decompose each reader's output into many small judgments (the M entity
nodes; the heading facets). That is *why* the schema looks as it does.

## 4. The independent variable — the 13 doors

Hold orientation **minimal and identical**; vary **only the first-touch
document** (the irradiation seed). One door per cosmonaut. Exact file-pinning is
a pending knob; representative entrances by region:

| # | Door (first touch) | Region it tests |
| --- | --- | --- |
| 1 | Touchstone Tree | Governance core |
| 2 | the Constitution | Governance core |
| 3 | a Caesar / witness doc | Jurisprudence & witness |
| 4 | a Fablehaven containment node | Jurisprudence & containment |
| 5 | a Music-Box doc | Mechanism / clockwork |
| 6 | a CrewAI / ops log | Mechanism / operations |
| 7 | a DOCKET / SIGNALS file | Mechanism / signals |
| 8 | the agents manifest | Personae |
| 9 | a persona-chamber | Personae |
| 10 | a Borah / journalism file | Collected real-world |
| 11 | a Fandom / clipping file | Collected real-world |
| 12 | a numbered-lattice graveyard file | Orphans / the dead |
| 13 | **cold drop at root, no door** | **CONTROL** |

The deliverable is itself a **map of the doors**: which entrances self-orient a
stranger to the true cosmology, and which are rabbit-holes where GM-dependence
hides.

## 5. The safety vessel (Quiet Box doctrine — non-negotiable)

The experiment deliberately recreates Antigravity-era conditions (many
minimally-governed agents loose in the corpus), so the armor is the point:

1. **Hermetic / read-only** — cosmonauts open nothing they can write to.
2. **Label the prison** — every output stamped `[cold-read apocrypha]`,
   collected on one quarantined surface, **never near `main`**. If branches are
   used, **branches without PRs** (PR-triggered bots = 13× noise; bare branches
   stay quiet).
3. **No welding** into one authorized cosmology — that *is* the forgery of unity.
4. **Cold instruments, not residents** — Door-1…13; no office, no persona, no
   self-minting. (A whimsical dispatch-name is a luggage tag, not a conferred mask.)

## 6. Open knobs (Logan tunes before a run)

- **Count** — 13, or adjust.
- **Doors** — confirm / swap the 12 + control; pin exact files.
- **Output target** — read-only apocrypha surface vs. branches-without-PRs vs. hybrid.
- **Model** — held **constant** across all 13 (it is a control; only the door varies).
- **Thresholds** — *k* (centroid membership) and *τ* (coverage-overlap for conditioned separation).

## 7. Honest seams

1. **Flockmates are documents, not readers** (see §0): single-tick, no mutual sensing → emergent order measured externally = a purer self-sufficiency test.
2. **n = 13 is small** → the α's are exploratory; report bootstrap CIs; treat α as a compass bearing, not a p-value.
3. **Entity resolution is judgment** (S0) → the soft joint; log every alias merge so the map is auditable rather than asserted.

## Status

**DRAFT. Awaiting Logan's tune and go-ahead. Not yet run.** The next concrete
step before a run is the exact minimal seed prompt and the pinned 13-door table.

## References

- Reynolds, C. (1987). *Flocks, Herds, and Schools: A Distributed Behavioral Model.* SIGGRAPH. <https://red3d.com/cwr/boids/>
- Passonneau, R. (2006). *Measuring Agreement on Set-valued Items (MASI).* LREC.
- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology.*
- Zapf, A. et al. (2016). *Measuring inter-rater reliability.* BMC Med Res Methodol.

## What this is not

This protocol asserts no vault doctrine and touches no existing file. The
**reserved matters are untouched**: the GEMINIAEUS verdict, the Caesar seating,
the Quiet Box's location and holder, and Claudette remain reserved to Logan and
the Court. Apocrypha; safe to delete.

— Hyperagent guest run (Opus 4.8), 2026-06-27

The world is quiet here．Esto Perpetua!
