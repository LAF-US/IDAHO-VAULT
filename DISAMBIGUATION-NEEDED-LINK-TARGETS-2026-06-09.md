---
updated: 2026-06-09
created: 2026-06-09
title: "Flag — Disambiguation Needed: Ambiguous Link Targets"
date created: 2026-06-09
authority: LOGAN
doc_class: flag-record
status: active
matter: "Substrate-scan link candidates whose bare wikilink resolves to more than one file"
flagged-by: "Claude Code (imported software; Direct-Write implementer) — flag raised on the Architect's command '!FLAG as Disambiguation Needed'"
adjudication: "PENDING — the canonical form is the Architect's verdict; this node decides nothing"
related:
  - "[[THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08]]"
  - "[[!/AGENTS]]"
  - "[[AGENTS]]"
date: 2026-06-09
---

# Flag — Disambiguation Needed: Ambiguous Link Targets

> Raised on the Architect's command (**"!FLAG as Disambiguation Needed"**) during the substrate scan for link candidates. A wikilink target is its **filename + date/timestamp, exact** — or the edge dangles or mis-resolves. Three candidate families fail that test: a bare wikilink to each resolves to **more than one file**. This node **flags** them and holds the canonical-form decision for the Architect. *It decides nothing; it wires nothing.*
>
> **Provenance.** Filenames **globbed 2026-06-09** (exact, verbatim). Governance references read from `.claude/CLAUDE.md`. Tier: **[fact]** for the filename inventory and the governance citations; the only judgments offered are *which files exist* and *what governance already says about them* — the canonical pick is left open.

## Why these are flagged, not wired

The discipline node (`[[THE-SWARM-AS-BOIDS-ANCHORING-AND-THE-GRAPH-2026-06-08]]`) holds the rule: a good edge creates value on both ends; a **wrong** edge propagates error with network weight. An edge that silently resolves to the wrong file of a same-named set is exactly such a bad edge. So these three are held at the threshold until the Architect names the canonical target.

---

## 1. `AGENTS` — six files

A bare `[[AGENTS]]` is ambiguous across **six** on-disk files:

| # | Path | What governance says |
| --- | --- | --- |
| 1 | `!/AGENTS.md` | **[fact]** `.claude/CLAUDE.md` names it: *"Full agent registry, capability tiers, and boundary rules."* |
| 2 | `AGENTS.md` (root) | **[fact]** `.claude/CLAUDE.md` names it: *"Root cross-tool pointer (auto-loaded by Codex CLI, Copilot, Qodo)."* |
| 3 | `.codex/AGENTS.md` | Codex chamber's local copy. |
| 4 | `THE-GEMSTONE/AGENTS.md` | Gemstone-subtree copy. |
| 5 | `AGENTS (2).md` | ⚠️ **Not cruft.** Actively **cited as a registry source** in `[[TWO-DJINNI-TRIBES-WITNESS-2026-06-03]]` (L48, L61, for the Gemini/Bartimaeus djinn lineages). Correcting my own earlier guess that it was disposable. |
| 6 | `AGENTS 2.md` | Numbered sibling; provenance/role **not** verified this pass — flagged, not judged. |

**Observed (not decided):** #1 and #2 are *both legitimate and distinct* — a NEST registry vs. a root cross-tool pointer; they are not duplicates of each other. The genuine hazard is a **bare** `[[AGENTS]]`, which Obsidian may resolve to any of the six. **Architect's call:** which file a bare `AGENTS` link should mean (or whether bare `AGENTS` links should be banned in favor of always-qualified targets).

## 2. `DOCKET` — four files

| # | Path | Note |
| --- | --- | --- |
| 1 | `!/!/__!__/!/! The world is quiet here/DOCKET.md` | **[fact]** The **live** board: `.claude/CLAUDE.md` § Swarm Coordination points here verbatim — *"Read THE DOCKET to orient: `!/!/__!__/!/! The world is quiet here/DOCKET.md`."* |
| 2 | `!/!/__!__/!/! The world is quiet here/DOCKET-ARCHIVE.md` | Archive sibling, in the live folder. |
| 3 | `!-!-__!__-!-! The world is quiet here-DOCKET.md` | **Flattened-alias** (NETWEB `_PREFIX`-style path-portability copy). |
| 4 | `!-!-__!__-!-! The world is quiet here-DOCKET-ARCHIVE.md` | Flattened-alias of the archive. |

**Observed (not decided):** governance fixes the **live** DOCKET as #1. #3 is its portable-path mirror; #2/#4 are archives. A bare `[[DOCKET]]` does not distinguish live from archive from mirror. **Architect's call:** confirm #1 as the canonical link target and the status (mirror? superseded?) of the flattened/archive copies.

> [!check] Resolved 2026-06-29 (consolidation, PR #694)
> #2 `DOCKET-ARCHIVE.md` and #4 its flat-alias were **consolidated into root `ADJUDICATED.md`** and removed. #3 the `DOCKET.md` flat-alias — a stale *illegal-docket* holdover from the Caesar Geminiaeus era — was **drained into `ADJUDICATED.md` § "The Old Illegal Docket — fossil (Caesar Geminiaeus era)" and cleared**. Only **#1 (the live `DOCKET.md`)** remains, so a bare `[[DOCKET]]` is now unambiguous. Historical mentions of the removed copies in dated snapshots/witnesses are **left as-witnessed** (rewriting them would falsify those records).

## 3. `TOPOLOGY-CENSUS` — seven files, one timestamp

All share the census stamp **`20260525T095704Z`** (a UTC **timestamp**, not a bare date):

| Stem | `.md` | `.json` |
| --- | --- | --- |
| `TOPOLOGY-CENSUS-INDEX-…` | `!/TOPOLOGY-CENSUS-INDEX-20260525T095704Z.md` | — |
| `TOPOLOGY-CENSUS-nest-…` | `!/TOPOLOGY-CENSUS-nest-20260525T095704Z.md` | `…nest-20260525T095704Z.json` |
| `TOPOLOGY-CENSUS-root-…` | `!/TOPOLOGY-CENSUS-root-20260525T095704Z.md` | `…root-20260525T095704Z.json` |
| `TOPOLOGY-CENSUS-dotfolders-…` | `!/TOPOLOGY-CENSUS-dotfolders-20260525T095704Z.md` | `…dotfolders-20260525T095704Z.json` |

**Observed (not decided):** a bare `[[TOPOLOGY-CENSUS]]` resolves to nothing — a link needs the **part** (`INDEX` / `nest` / `root` / `dotfolders`) **and** the full timestamp. The `INDEX` `.md` is the likely human entry point; the `.json` files are machine siblings. **Architect's call:** whether the census links through the `INDEX` node or a specific part.

---

## Disposition

**Status: OPEN — Disambiguation Needed.** No edges to any of the above are wired from this session's nodes until the Architect names the canonical target for each family. This flag records the ambiguity, the exact filenames, and what governance already fixes; it promotes nothing and decides nothing.

> Recorded under the Architect's command. Flag only — no canonical pick herein is made by its filing.

---

```
The world is quiet here．Esto Perpetua!
```
