---
title: "!REPORT-TVTROPER-DATASET-2026-06-20"
updated: 2026-06-22
status: active
authority: LOGAN
tags:
  - ai/training-data
  - ai/datasets
  - source/huggingface
  - provenance/scrape
  - licensing/creative-commons
related:
  - VAULT-CONVENTIONS
  - CLAUDE
  - "!-!REPORT-VISIONCLAW-RESEARCH-2026-06-17"
---

# REPORT ON `RyokoExtra/TvTroper` (Hugging Face dataset)

**Agent:** Claude Code (`agent:claude-code`)
**Date:** 2026-06-20
**Mode:** External research and classification of a Hugging Face dataset
**Status:** Reference note filed; no data ingested into the vault

---

## What This Note Is

The task surface was the bare string `RyokoExtra/TvTroper`. Logan confirmed
the intended reading: it is a **Hugging Face repo ID** (`owner/repo`), not a
vault persona. This note documents the dataset, its sibling datasets, and the
provenance/licensing questions a journalist should keep in view before relying
on it. Per the vault's epistemological rules, claims below are tied to their
source, and gaps are named with the `*` wildcard rather than filled with
invented certainty.

---

## I. Identification

| Field | Value |
| --- | --- |
| Repo ID | `RyokoExtra/TvTroper` |
| Type | Hugging Face **dataset** |
| URL | <https://huggingface.co/datasets/RyokoExtra/TvTroper> |
| Author (uploader) | `RyokoExtra` |
| Created | 28 Jun 2023 |
| Last updated | 29 Jun 2023 |
| Downloads | ~4.5K (as observed 2026-06-20) |
| Likes | 11 |
| Declared license | `apache-2.0` |
| Language | `en` |
| Declared task categories | `text-classification`, `text-generation` |
| Size category | `100K<n<1M` |
| Modality | text |

Source: Hugging Face Hub metadata for the repo, retrieved 2026-06-20 via the
Hugging Face MCP (`hub_repo_details`).

---

## II. What It Contains

- A **raw dataset dump** consisting of text from **at most 651,522 wiki pages**
  from `tvtropes.org`, excluding namespaces and date-grouped pages (per the
  dataset card's own "Dataset Summary").
- Per the dataset card, it is **primarily intended for unsupervised training of
  text-generation models**, though it tags itself for text-classification too.
- **Record schema:** two fields per row — the page **URL** and the
  **content retrieved**. The card warns that content "may contain errors, and
  if the page does not exist, the 404 error page is scraped" — i.e. error pages
  are present as data, not filtered out.
- **Distribution format:** the underlying files are JSONL, distributed as a
  single compressed archive on the order of ~20 GB.\*

\* The ~20 GB / JSONL / 404-page details come from the dataset card text as
surfaced through search of the card; treat exact archive size as approximate
until re-confirmed against the live file listing.

### Live-viewer caveat (verified this session)

As of 2026-06-20 the Hugging Face **Dataset Viewer fails** for this repo:
parquet auto-conversion did not produce exports ("Failed parquet jobs: 1"), and
the rows endpoint returns `500 Internal Server Error: The dataset generation
failed`. Practical effect: you cannot preview rows or stream it through the
standard `datasets` auto-parquet path; you would have to download and parse the
raw archive yourself.

---

## III. The TvTroper Family (related datasets)

The same underlying scrape exists in several forms. Confirmed to exist via
search/Hub on 2026-06-20:

| Repo | Note |
| --- | --- |
| `RyokoExtra/TvTroper` | Raw dump (this note). ≤651,522 pages. |
| `RyokoExtra/TvTroper-Cleaned` | A cleaned variant of the same ≤651,522-page corpus.\* |
| `KaraKaraWitch/TvTroper-2025` | Updated snapshot, **≈708,000 pages** (namespaces / date-grouped pages excluded).\* |

\* Cleaning specifics for `-Cleaned`, and the exact relationship between the
`RyokoExtra` and `KaraKaraWitch` accounts, are not fully verified in this
session. The 2023 scrape is attributed in the card text to **KaraKaraWitch**;
`RyokoExtra` appears to be the same maintainer or a closely linked alias, but I
have **not** independently confirmed that the two accounts are the same person.\*

Unrelated but easily confused (different authors, different intent):
`adorkin/tvtropes2imdb`, `MDGraff/tvtropes.self.demonstrating.character.pages`.

---

## IV. Provenance & Licensing — Why a Journalist Should Be Careful

This is the part that matters for the vault, not the row counts. The grey here
is not one ambiguity but a stack of them, and they compound.

### IV.1 The core mismatch

The Hub repo declares **`apache-2.0`** — a permissive license that allows
commercial use and relicensing. But the underlying TVTropes content is
**CC BY-NC-SA**: the site used CC BY-SA before July 2012, then switched to
**CC BY-NC-SA (NonCommercial–ShareAlike)** in July 2012 (verified via
Wikipedia's "TV Tropes" entry and contemporaneous reporting; see References).

Foundational rule: **you cannot grant rights you do not hold.** An uploader
applying `apache-2.0` to a scrape does not re-license the source text — the tag
only describes what the *uploader* claims over their *packaging*. The source
content's license travels with the words. So the Apache tag is, at best,
describing the wrong layer.

### IV.2 The three CC terms it collides with

CC BY-NC-SA imposes three obligations, and the dataset arguably breaks all
three:

- **NC (NonCommercial)** — The dataset is explicitly tagged for
  `text-generation` / `text-classification` training. Training a *commercial*
  model on it uses NonCommercial-licensed content commercially. Sharpest
  practical risk.
- **SA (ShareAlike)** — Derivatives must carry the same/compatible license.
  Apache-2.0 is **not** compatible with CC BY-NC-SA, so relabeling the corpus
  `apache-2.0` is itself a ShareAlike violation, independent of downstream use.
- **BY (Attribution)** — Requires crediting contributors. A bulk dump with a
  two-field schema (URL + raw content) carries no per-contributor attribution.

### IV.3 The deeper grey: the source license is itself contested

The 2012 relicensing was reportedly done **without the consent of many editors**
who had contributed under the older CC BY-SA terms, and the edit page carried no
licensing notice — so it is unclear whether TVTropes even held the right to
relicense a large portion of its *own* pre-2012 content to NC-SA. Provenance is
therefore broken at **two** levels: scraper → `apache-2.0` is almost certainly
wrong, and TVTropes → `CC BY-NC-SA` is itself disputed for older content. You
cannot cleanly answer "what license governs row N?"

### IV.4 Two layers that are not copyright at all

- **Terms-of-service / scraping.** Bulk scraping can breach a site's ToS
  regardless of the content license — a separate contract question from
  copyright.\*
- **The unsettled "is training fair use?" question.** Whether training a model
  on copyrighted text is infringement or fair use is actively litigated
  (2023–2026) and unresolved, so the NC restriction's *enforceability against
  model training specifically* is an open legal question, not a settled "no."\*

### IV.5 Data-quality caveats (not licensing, but bundled)

- **It includes garbage by design.** Because 404 pages are scraped as content,
  any downstream use must filter error pages or it will train on / cite
  boilerplate error text.
- **It is a frozen 2023 snapshot** (the `-2025` repo is the newer crawl). Do not
  treat it as a current reflection of TVTropes.
- **No row-level integrity guarantees.** The card itself says content "may
  contain errors." This is a raw crawl, not a curated corpus.

\* Items marked are genuinely open questions (ToS/contract exposure; whether
training on copyrighted text is fair use). They are flagged rather than resolved
— this note reasons about license *layers*, it does not render a legal opinion.

---

## V. Relevance to the Vault

- **Direct relevance:** low. This is a generic LLM pre-training scrape; nothing
  Idaho-, journalism-, or governance-specific.
- **Indirect relevance:** moderate, as a **case study in AI training-data
  provenance** — the exact tension Logan tracks elsewhere (where training
  corpora come from, how scraped third-party content gets re-licensed, and how
  "error-page-as-data" pollution enters models). Useful as a concrete example
  when writing or reasoning about dataset accountability.

**Recommendation:** keep as a reference note. Do **not** ingest the 20 GB corpus
into the vault — it has no on-record value here and carries the licensing
ambiguity above. If a future task needs TVTropes data, prefer the newer
`-2025` snapshot and resolve the source-license question first.

---

## VI. How These Facts Were Gathered (provenance)

- Hugging Face Hub metadata via the Hugging Face MCP (`hub_repo_details`,
  `overview` + `dataset_structure`), retrieved 2026-06-20 over the vault owner's
  authenticated Hugging Face session — source of the metadata table in §I and
  the live-viewer failure in §II.
- Web search (2026-06-20) — source of the card's summary text (page count,
  intended use, two-field schema, 404-page behavior, ~20 GB JSONL), the
  existence of the sibling `-Cleaned` and `-2025` repos, and the TVTropes
  content-license history in §IV (CC BY-SA → CC BY-NC-SA, July 2012; contested
  relicensing).
- Direct `WebFetch` of the dataset/README URLs returned **HTTP 403**, so card
  text is sourced via the MCP overview and search rather than a raw fetch.

---

## VII. Update — Acquisition Method & Access Surfaces (researched 2026-06-21)

A second pass — Hugging Face MCP re-pull plus web research — on the question
*"how was this scraped at all, when TVTropes has no API?"* The findings sharpen
§IV's provenance stack rather than change it.

### VII.1 There is no official TVTropes API — and that is load-bearing

- An API has been **requested for years and never delivered**; the stated blocker
  is the site's database architecture — *"every page is one giant text entry."*
  That same architecture is **why this dataset is raw page-text blobs** rather
  than structured fields.
- The operator's posture on bulk export is explicit and negative: *"absolutely
  not, under any circumstances, making available a public dump or torrent of the
  site's data."*

**Consequence:** the corpus could only have been obtained by **directly crawling
HTML pages.** The dataset card calls it a "raw dataset dump" but does **not**
state the method — so *crawl* is inference. It is corroborated, though, by the
dataset's own **404-page-as-content** behavior (§IV.5): an API or sanctioned
export would never hand back a 404 page as a record; a crawler hitting dead or
namespace-excluded URLs would.\*

### VII.2 This hardens the ToS/contract layer (§IV.4)

Because acquisition required crawling **against the operator's express no-dump
position**, the exposure flagged in §IV.4 is **concrete, not hypothetical** — and
independent of the copyright question. Three distinct layers:

- **ToS — the contract layer.** Bulk crawling against the site's stated terms is a
  contract question, separate from copyright; this is where the no-dump stance
  bites.
- **`robots.txt` — the access-control layer.** It governs *access*, not *usage*,
  and is not itself a contract — a breach is evidence, not a tort on its own.
- **Observed behavior.** TVTropes returned **HTTP 403** to this session's direct
  fetcher for `robots.txt` — an active anti-bot posture — so the verbatim crawl
  directives remain unconfirmed.\* (The **Hugging Face** dataset README likewise
  403'd a raw HTTP fetch; that is *Hugging Face's* anti-bot layer, a different
  host — its card content was reachable only via the Hugging Face MCP, not a raw
  pull.)

### VII.3 The closest "structured" access is itself a scrape

**DBTropes** is a Linked-Data wrapper (Kiesel & Grimnes, DFKI) that **parses
TVTropes pages into RDF / NTriples** — linking works (films, books, items) to the
tropes they feature — built on the **Skipforward / Skipinions** ontology and
published as monthly NTriples snapshots. It was offered *"as an alternative to web
scraping TVTropes directly"* — i.e. even the structured option exists **because
there is no API**, and is itself a parsing-scrape. Its last timestamped snapshot
is **2015-04-30** (≈20,000,000 RDF statements; ≈58,000 items; ≈27,000 feature
types; ≈3,550,000 feature instances) — so it is **stale by roughly a decade**, not
a live feed.

Notably, DBTropes **passes TVTropes' own per-page license through** to its
triples: the ontology declares *"Triples with the same subject are subject to the
designated license,"* using a CC license that permits derived works. That is a
sharp contrast with this dataset's blanket **`apache-2.0`** relabel of CC-licensed
source text (§IV.2) — the structured derivative preserved the source license; the
HTML scrape overwrote it.

### VII.4 Unverified — held with the `*`

A web-search summary referenced an *"unofficial `api.tvtropes.org`"* and an
*"official offline-mirror monthly SQLite dump."* Both **conflict with the explicit
no-dump stance** and could not be confirmed against primary sources — recorded
here as **unverified**, not asserted.\*

**The `*` flags in §VII mark three different kinds of uncertainty** — do not read
them as one:

- **[inference]** — reasoned from grounded evidence, not stated by the source:
  that acquisition was an HTML *crawl* (VII.1 — from no-API + 404-as-content).
- **[unfetched]** — a primary text that exists but could not be retrieved this
  session: `robots.txt`'s verbatim rules (VII.2 — HTTP 403).
- **[unverified]** — an external claim not corroborated against a primary source:
  the rumored `api.tvtropes.org` / SQLite mirror (VII.4). *(DBTropes' figures and
  2015-04-30 last snapshot in VII.3 are now grounded in the project's published
  stats, so they no longer carry this flag.)*

Grounded where stated; flagged — by kind — where not.

---

## References

1. RyokoExtra. (2023). *TvTroper* [Dataset]. Hugging Face.
   <https://huggingface.co/datasets/RyokoExtra/TvTroper>
2. RyokoExtra. (2023). *TvTroper-Cleaned* [Dataset]. Hugging Face.
   <https://huggingface.co/datasets/RyokoExtra/TvTroper-Cleaned>
3. KaraKaraWitch. (2025). *TvTroper-2025* [Dataset]. Hugging Face.
   <https://huggingface.co/datasets/KaraKaraWitch/TvTroper-2025>
4. TVTropes. *tvtropes.org* — source wiki for the scraped content.
   <https://tvtropes.org/>
5. Wikipedia. *TV Tropes* — license history (CC BY-SA → CC BY-NC-SA, July 2012)
   and relicensing controversy. <https://en.wikipedia.org/wiki/TV_Tropes>
6. SoylentNews. (2014, May 15). *TV Tropes Relicensed its Content - Without Permit.*
   <https://soylentnews.org/article.pl?sid=14/05/15/1938243>
7. Creative Commons. *Attribution-NonCommercial-ShareAlike 4.0 International
   (CC BY-NC-SA) — Legal Code.*
   <https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en>
8. TVTropes. *MediaNotes/ApplicationProgrammingInterface* — community page on the
   long-requested, never-shipped API.
   <https://tvtropes.org/pmwiki/pmwiki.php/MediaNotes/ApplicationProgrammingInterface>
9. DBTropes — Linked-Data (RDF/NTriples) wrapper for TVTropes (Kiesel & Grimnes,
   DFKI), built on the Skipforward/Skipinions ontology; the closest structured
   derivative, itself a parsing-scrape. Last timestamped snapshot 2015-04-30
   (≈20M statements, ≈58k items, ≈27k feature types, ≈3.55M feature instances);
   passes the source's per-page CC license through to its triples.
   Project: <http://skipforward.opendfki.de/wiki/DBTropes> — catalog entry:
   <http://linkeddatacatalog.dws.informatik.uni-mannheim.de/dataset/dbtropes>
10. Research provenance (2026-06-21): API-absence, the no-public-dump stance, and
    the DBTropes derivative surfaced via Hugging Face MCP re-pull + web search.
    A direct fetch of TVTropes `robots.txt` returned **HTTP 403** (TVTropes'
    anti-bot), so those crawl directives are unconfirmed and flagged `*` above; a
    raw fetch of the **Hugging Face** dataset README likewise returned **HTTP 403**
    (Hugging Face's anti-bot, a different host), so the card was read via the
    Hugging Face MCP rather than a raw pull.

---

## Closing

The world is quiet here. A wiki about every story, flattened into 651,522 rows —
including the pages that were never there.
