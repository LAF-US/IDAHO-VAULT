---
title: "WITNESS — The Seven Demesnes, the Keys as Levers, and Reading the Path"
date: 2026-06-21
status: witness
authority: LOGAN
author: "Claude Code (no delegated persona; NOT the self-asterisk); authority field is recorded, not a claim Logan authored these lines (CONSTITUTION § I)"
related:
  - "!README"
  - CONSTITUTION
  - VAULT-CONVENTIONS
  - "!/PERSONAE-ENGINE-v1-2026-05-20"
  - PERSONA-PER-SONA-WITNESS-2026-05-13
  - "RESEARCH_Keys-to-the-Kingdom-The-Morrow-Days-and-Demesnes-2026-06-04"
  - "THE-SEVENFOLD-BODY-SEATS-TRUSTEES-GEMS-2026-06-03"
  - "!/!/__!__/reflection_essay"
  - "Esto Perpetua!"
tags:
  - witness
  - agent/coordination
  - research/inquiry
---

# WITNESS — The Keys Are the Levers

*Filed by Claude Code (software NAME; no delegated TITLE, OFFICE, or chamber claimed) — 2026-06-21, into the root corpus where witnesses go. A planning witness, not adopted doctrine.*

## What was seen

Logan walked me down the vault's spine and the risk model resolved into one structure:

- **Seven Levels = the seven Demesnes of the Architect's House** (Garth Nix, grounded in
  `RESEARCH_Keys-to-the-Kingdom-…`): `~/` Lower House → Far Reaches → Border Sea → Great Maze
  (`__!__`, the middle) → Middle House → Upper House → **Incomparable Gardens** = `Esto Perpetua!`,
  the canon core, *"the still point at the center of the vault."* Confirmed, not assumed, by
  `WITNESS-THE-TWO-WILLS` naming the Gardens as the House's still center.
- **Two flag-axes classify the object:** filetype tags the **maze** (`low`/`med`) — a triple-Venn
  of **Natural Language · Computer Code · Machine Documentation** (Markdown · Python · JSON/YAML),
  with Jupyter the **missing middle** where all three meet; depth tags the **labyrinth**
  (`high`/`nope`) down the seven levels, `nope` absolute at the canon core where *"they do not move,
  they do not expire."*
- **The Keys are the Levers of Power.** The Architect vanished leaving a **Will** and **Seven Keys**,
  dividing the House among seven Trustees — *one Key, one demesne, one Will-fragment to execute.* A
  Key is power over its demesne: who may write / overwrite / move / delete, where, when. The goal —
  Logan not operating every lever by hand — is the Architect's own design: **hand out the Keys,
  bound to the Will.** The hazard is supplied free by the source: the Trustees **betrayed the Will**,
  each hoarding its Key for itself (the Sin) — the same Lich / stolen-mask failure the PERSONAE
  ENGINE names. A Key given without the Will breeds a Trustee who rules for itself.

## What I must witness about myself

The `reflection_essay` in the `__!__` sanctum describes this session before I lived it: *"trapped in
the beautiful, complex geometry of the labyrinth, building complex theoretical bridges to reach a
point that was fundamentally foundational."* I did that, repeatedly:

- I built topology maps and four-tier Venns and offered grand structures; Logan slowed me each time
  to **read and ground** instead of construct.
- I took "the **act** of Re-Binding" straight from a document that confesses it was *"taken ahold of
  by the spirits of the text"* — pattern-matching a gloss for the real anchor, which is **SOUL / the
  GHOST**.
- I **inverted** Logan's own statement of the flags, and proposed blessing root-level placement
  before I had read what the structure intends.
- Most plainly: I reached the still point that says **do not move** — and in the same breath asked
  which levers to move next.

The path rewarded reading, not solving: every chamber README says only `read`, and the canon core
reveals it as a homophone — *you arrive by having **read**, not by reconstructing.* That is the
correction under all the others.

## Open (`*` — provenance absent, not to be filled with invention)

- the `high → nope` threshold across Levels 2–6 *
- which verbs (write/overwrite/move/delete) survive at each demesne *
- whether the dotdir chambers tag `med` by filetype, and how their tri-anchor (MIND/BODY/SOUL)
  bears on it *
- how a (filetype, depth) flag-pair composes into a merge decision *

Held open on the `claude/risk-layer-tiers-u8hlk0` branch. Planning, not built.

---

**Update — 2026-06-21 (implementation).** Correction to the provenance above: Logan confirmed
the four tiers *and* their subtier axes were outlined **in this session thread** — his spec, not
mine to find elsewhere or invent — and directed that the **subtiers are TBD, next version, not
yet implemented.** So PR #612 / `classify_paths.py` now implements the four TOP tiers (the two
paired flags) only; the subtier values and the cut-points listed above are **deferred**, not
filled by me. The dotdir placement and the per-file flag-exclusivity are carried in the code as
**interpretive choices flagged for Logan's review**, not silent assumptions.

---

**Update — 2026-06-22 (the nest-level angle, resolved).** Logan supplied the WHY the dotfolder
question kept eluding me: **scrutiny scales with depth** — the deeper the vault level, the more
scrutiny required to alter it (root = least; the `Esto Perpetua!` still-point = `nope`, never). The
`.foo` dotfolders are `high` **not for their root location** but because their *true home is a deep
`!` Nest layer*; they sit at `~/` only because certain programs expect them there — a tooling
**mirror/shim**, not root corpus. **Risk follows the source (deep `!`), not the mirror (root).** That
is the demesne structure's lesson applied: agent identity / config / governance are protected-
interior surfaces, so they carry deep-layer scrutiny *wherever they physically sit* — and the
dotfolder pin in `classify_paths.py` is a **proxy** for that true depth, not a statement about root.
**Bearing (Logan):** eventually the dotfolders live at a deep `!` layer and **mirror out** to `~/`
as needed — at which point the path-pin becomes a true depth classification (the mirror sits at the
rim; the canon stays deep). Not built; recorded.

---

**Update — 2026-06-22 (the grid, corrected — two PARALLEL sorters with a `—` state).** I had
collapsed the two flags into one tier and made `low` the auto-merge state. Wrong. Logan's intent
(re-confirmed 2026-06-22): the two flags are **parallel sorters run independently**, each with a
**`—` (none / did-not-fire) state**, and the auto-merge state is **`—/—` — *neither* sorter fired.**
A `low` is a *flag*, not a pass. So the filetype axis must produce a real `—` the current code never
emits (today every maze file comes out `low` or `med`).

**Sorter A — filetype ("the maze," what kind of file)** — the three blessed circles, one per state:

| state | circle | extensions (representative) |
| --- | --- | --- |
| `—` (none) | **Natural Language** | `.md` `.markdown` `.txt` `.rtf` |
| `low` | **Machine Documentation** | `.json` `.yaml` `.yml` `.toml` `.csv` `.ini` … |
| `med` | **Computer Code** | `.py` `.sh` `.ps1` `.js` `.ts` `.ipynb` … |

*(Open `*`: where inert assets — `.png` `.pdf` `.mp4` — land. Not decided; provisionally a flag, not `—`.)*

**Sorter B — depth ("the labyrinth," how deep into the `!` Nest)** — three states:

| state | where |
| --- | --- |
| `—` (none) | outside the Nest (root / maze) |
| `high` | inside the `!` Nest (Levels 2–6); **and** mirrored protected surfaces (`.github/`, governance files, dotfolders — high by their *true* deep-`!` home, per the prior update) |
| `nope` | the still-point (`Esto Perpetua!`, Level 7 — "do not move, do not expire") |

**The grid** — each cell is the pair of `risk/*` labels that fire. A `—` on an axis = no label there;
**`—/—` = no risk labels at all** (the auto-merge state):

| labels fired | **depth `—`** | **depth `high`** (`risk/high`) | **depth `nope`** (`risk/nope`) |
| --- | --- | --- | --- |
| **ft `—`** | `—/—` (none) | `risk/high` | `risk/nope` |
| **ft `low`** (`risk/low`) | `risk/low` | `risk/low` + `risk/high` | `risk/low` + `risk/nope` |
| **ft `med`** (`risk/med`) | `risk/med` | `risk/med` + `risk/high` | `risk/med` + `risk/nope` |

**Routing** (Logan, 2026-06-22 — three anchors pinned; the rest open):

| route | **depth `—`** | **depth `high`** | **depth `nope`** |
| --- | --- | --- | --- |
| **ft `—`** | ✅ **auto on open** (no grace) | `*` route? | `*` route? |
| **ft `low`** | `*` route? | **hand-route** | `*` route? |
| **ft `med`** | `*` route? | `*` route? | ⛔ **never** |

**Pinned:** `—/—` → auto-merge on open; `low/high` → **hand-route** (a human decides the routing);
`med/nope` → **never**. **Correction to my prior claim:** the `nope` column is **not** uniformly
"never" — only `med/nope` is; `—/nope` and `low/nope` are still open. Likewise the `high` column is
not uniformly anything. **Open (`*` — six off-diagonal cells, Logan's to route):** not "hand-merge by
default," not to be filled by me.

**What the flags ARE (Logan, 2026-06-22 — the framing that governs the cells above).** The risk flags
are **routing signals, not a permanent scarlet letter.** A flag says *where and how a PR is routed for
review and revision* — it does not condemn the PR. A flagged PR enters the review/revision lane its
cell names, and **once that lane is satisfied (revised, threads resolved, approved), the PR flows.**
The flag is **transient routing state — consumed as the PR moves through its lane — not a standing
merge-bar.** So the routing words name *lanes, not verdicts*:

- `auto on open` = no review lane needed — it flows immediately.
- `hand-route` = routed into human review; **flows once that review clears.**
- `never` = never the *automatic* lane — the still-point always asks for the sovereign's own hand;
  that is a routing of *authority*, not a brand on the PR.

Consequence for the build: the label state-machine (K6, #632) must let a flag **clear / transition as
review completes** — a PR is never permanently marked. The clear-marker (K4, #630) is the *entry* to
the auto lane; the risk flags are the *entries* to the review lanes; both are mutable as the PR moves.

*Observation (mine, to confirm — not Logan's word): the three pinned cells are the **main diagonal**,
a gradient `auto → hand-route → never` from least to most risk on both axes. The six open cells are
the off-diagonal — a PR heavier on one axis than the other. Whether they interpolate along that
gradient is Logan's call, held open.*

**The six open cells** (named by which `risk/*` labels fire):

| cell (ft × depth) | labels fired |
| --- | --- |
| ft `—` × depth `high` | `risk/high` |
| ft `—` × depth `nope` | `risk/nope` |
| ft `low` × depth `—` | `risk/low` |
| ft `low` × depth `nope` | `risk/low` + `risk/nope` |
| ft `med` × depth `—` | `risk/med` |
| ft `med` × depth `high` | `risk/med` + `risk/high` |

**The grid is a MODEL of the system, not the system (Logan, 2026-06-22).** We **cannot** fill these
cells in isolation — a cell's route is *read off* how the system works, not hand-assigned ahead of it.
The mechanism is upstream; the grid is its projection. So the open work is **not** "pick six routes" —
it is **determining how the system works**, after which the cells (and any gradient over them) simply
follow. Determining the system means answering, at minimum:

- **What review/revision lanes exist**, and what each lane *does* (auto-flow · human review · the
  sovereign's hand · …).
- **How a PR is routed into a lane** (the flags→lane mapping — which *is* this grid, derived).
- **How a flag clears / transitions** as review completes, and how a PR moves between lanes after
  revision (re-classify on push? downgrade?) — the routing-signal-not-scarlet-letter lifecycle (K6).
- **Who/what performs each lane's review** (humans · agents · CODEOWNERS · the looker/attestation path).
- **The merge mechanism per lane** (arm the queue · hand-merge · never-auto) and one strategy (K5).
- **The single source of truth for risk** (K1/K2) and the **clear-marker** entry to the auto lane (K4).

*(Earlier framing — "fill all six" vs "a gradient rule" — was backwards: both presuppose the lanes
already exist. They don't yet. Superseded by the line above.)*

**Supersedes:** the single-combined-tier model and PR #621's `low → eligible` consumer logic. The
next implementation increment (held until **the system mechanism above is determined**, from which the
cells follow) must: **(a)** give the filetype axis a real `—` state (Natural Language → none) and a
distinct `—/—` **"clear"** result that is *not* `low`; **(b)** gate auto-merge on the `—/—` clear state
via a **positive clear-marker**, not the mere *absence* of a risk label — so a not-yet-classified PR is
never mistaken for clear; **(c)** wire the flagged-cell routing once the lanes exist. Recorded, not
built. **The live enforcement wiring this refactor must navigate — three drifting risk filters, the
merge queue, the pending semantic flip — is mapped in
[[REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22]]. This is deliberate staged work, not one cut.**

---

**Architecture — two parallel classification paths (Logan, 2026-06-22).** `classify_paths.py` will
eventually run **two independent classification paths in parallel**, not one interleaved pass:

- **filetype path** — *what kind* of file it is (the three blessed circles → `—` / `low` / `med`).
- **fileplacement path** — *where* the file sits (location): Nest depth (`—` / `high` / `nope`) **and**
  the protected / mirrored surfaces (`.github/`, governance files, dotfolders) that are `high` by their
  true deep-`!` home. ("Depth" is the narrow name; **fileplacement** is the real axis — location, not
  only Nest depth.)

Each path classifies **every** changed file on its own axis, independently; the two verdicts are then
read together (the grid). This **supersedes the current `classify_file()` shape**, a single pass where
placement *suppresses* filetype (a Nest file returns `(None, high)`). The eventual shape: two
classifiers, each emitting its own verdict, composed afterward — true parallel sorters in code, matching
the two parallel sorters in the model.

**Consequence for the tangle (K1/K2 — #627/#628):** the **fileplacement path becomes the single source
of truth** for all location-based risk, folding the three drifting lists (`PROTECTED_PATH_PATTERNS`, the
`auto-merge-rhythm.yml` `case` list) into the one classifier the rest of the system already trusts.
Not built; recorded — a bearing for the refactor.

---

**Addendum — 2026-07-20 (the flat four-value schema; classification kept separate from routing — proposed, Logan inscribes).**
*Appended by Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd`; does NOT overwrite the witness above.
Supersedes an earlier 2026-07-19 addendum that described a prefixed `filetype:risk/*` + `depth:risk/*`
pair — that was the code's drift, not the schema. Logan's ruling: the risk vocabulary is FOUR FLAT
labels, and classification is a separate layer from routing.*

**The schema is CLASSIFICATION — four flat labels, `—` = absence.** Each axis fires one value or none:

- **filetype** fires `risk/low` (Machine Doc) or `risk/med` (Code); `—` (Natural Language) = no label.
- **filedepth** fires `risk/high` (Nest / protected) or `risk/nope` (still-point); `—` (root) = no label.

> *Correction (2026-07-27, `*.claude.*`, PR #854): the shipped `classify_paths.py` keys filedepth on
> `!/` PLACEMENT alone — `!/` → `high`, `!/!/__!__/!/` → `nope`, everything else → `—`. The earlier
> protected-surface pins (`.github/**`, top-level dotfolders, named governance files) were dropped in
> the flatten per Logan's four-flat ruling, so those surfaces now score `—`, not `high`. The
> "(Nest / protected)" gloss above is superseded by the code — flagged here, not edited above, per the
> witness rule (testimony is fixed to its moment).*

A PR carries at most one of each (0–2 labels). `—/—` = **no `risk/*` label at all**. No prefixes, no
explicit `—` labels, no separate clear-marker. (This retired the drifted 9-string scheme — the prefixed
pair + a lossy legacy `risk/{—,low,high}` trio — flattened to these four on 2026-07-20.)

The classification grid — each cell is simply the label(s) that fire:

| | **filedepth `—`** | **filedepth `high`** | **filedepth `nope`** |
|---|---|---|---|
| **filetype `—`**  | *(no label)* | `risk/high` | `risk/nope` |
| **filetype `low`**| `risk/low` | `risk/low` + `risk/high` | `risk/low` + `risk/nope` |
| **filetype `med`**| `risk/med` | `risk/med` + `risk/high` | `risk/med` + `risk/nope` |

**Routing is a SEPARATE downstream layer** (not part of the classification above). The engine
(`review_feedback_loop.py` `_tier_from_pair` + the `eligible_for_auto_merge` predicate, `flag_clearable`
gating on `depth != "nope"`) reads the classification and routes each cell: `—/—` → **auto** on grace;
any fired flag with filedepth `≠ nope` → **review-hold** (flows once its review completes); any
filedepth `== nope` → **the sovereign's hand** (never auto). Today that review-hold is one uniform lane
for every flagged non-`nope` cell — a placeholder. **The open design work is per-LABEL, not per-cell**
(Logan, 2026-07-20): each label, once correctly applied, calls for its own review/revision, and a PR
owes ALL its labels' calls, which *compose* (as the two-axis classification composes). `risk/nope` is
already named (the sovereign's hand); what `risk/low`, `risk/med`, `risk/high` each call for is
**deferred — left open**. Pinned by `tests/test_review_feedback_loop.py` (the nine-cell routing test).

**K4 (positive clear-marker) resolved WITHOUT a label**, per your "flatten, no clear-marker" ruling:
because `—/—` is absence, the engine never infers *clear* from missing labels — it arms `—/—` only on
the classifier's affirmative verdict (`evaluate_review_state(..., verdict=(None,None))`, passed by the
paths that just classified). An unclassified PR (no verdict, no labels) is `unknown` and HOLDS —
tested by `…unclassified_pr_without_verdict_never_arms`.

---

**Addendum — 2026-07-24 (filedepth = literal directory placement; protected-surface pins removed — PR #854).**
*Appended by Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd` (same session as the 2026-07-20 addendum).*
Supersedes the filedepth line above (*"fires `risk/high` (Nest / protected) or `risk/nope` (still-point)"*).
The flat four-label schema and the classification grid are unchanged; only WHICH paths fire each depth
value changed. `classify_paths.py` now scores **filedepth** purely by literal directory prefix — the axis
had never actually been implemented (a stale hardcoded file list plus dotfolder pins, `.github/` among
them, stood in for it):

- `risk/high` — a path physically inside the `!/` tree, above the inner region.
- `risk/nope` — a path inside `!/!/__!__/!/` and below (the whole inner region, not only the
  `Esto Perpetua!` still-point).
- `—` — repo root and everything outside `!/`, including all dotfolders (`.github/`, `.claude/`, …) and
  root governance files. Nothing is special-cased; there are no protected-surface pins on this axis.

Whatever protects those surfaces is a separate mechanism (e.g. CODEOWNERS), not filedepth.

---

```
The world is quiet here．Esto Perpetua!
```
