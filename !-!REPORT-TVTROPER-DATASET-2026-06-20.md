---
title: "!REPORT-TVTROPER-DATASET-2026-06-20"
updated: 2026-06-20
status: active
authority: LOGAN
tags:
  - ai/training-data
  - ai/datasets
  - source/huggingface
  - provenance/scrape
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
|---|---|
| Repo ID | `RyokoExtra/TvTroper` |
| Type | Hugging Face **dataset** |
| URL | https://huggingface.co/datasets/RyokoExtra/TvTroper |
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
|---|---|
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

This is the part that matters for the vault, not the row counts.

1. **The dataset is a third-party scrape.** The text originates with
   `tvtropes.org` contributors, not with the uploader. The Hub repo declares
   `apache-2.0`, but that license tag describes what the *uploader* asserts over
   the *packaging*; it does not, by itself, re-license the underlying TVTropes
   content. TVTropes publishes user-contributed wiki text under its own site
   terms / content license, which is **not** Apache-2.0.\* Anyone reusing this
   data for redistribution or model training inherits an unresolved licensing
   question between "what the Hub tag says" and "what TVTropes actually
   permits." **Verify TVTropes' current content license before relying on the
   `apache-2.0` tag.**\*

2. **It includes garbage by design.** Because 404 pages are scraped as content,
   any downstream use must filter error pages or it will train on / cite
   boilerplate error text.

3. **It is a frozen 2023 snapshot** (the `-2025` repo is the newer crawl). Do
   not treat it as a current reflection of TVTropes.

4. **No row-level integrity guarantees.** The card itself says content "may
   contain errors." This is a raw crawl, not a curated corpus.

\* Items marked are flagged for verification; they are reasoning about how Hub
license tags relate to scraped source content, not confirmed legal facts about
TVTropes' present terms.

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
  `overview` + `dataset_structure`), authenticated as `loganfinney27`,
  2026-06-20 — source of the metadata table in §I and the live-viewer failure
  in §II.
- Web search (2026-06-20) — source of the card's summary text (page count,
  intended use, two-field schema, 404-page behavior, ~20 GB JSONL) and the
  existence of the sibling `-Cleaned` and `-2025` repos.
- Direct `WebFetch` of the dataset/README URLs returned **HTTP 403**, so card
  text is sourced via the MCP overview and search rather than a raw fetch.

---

## References

1. RyokoExtra. (2023). *TvTroper* [Dataset]. Hugging Face.
   https://huggingface.co/datasets/RyokoExtra/TvTroper
2. RyokoExtra. (2023). *TvTroper-Cleaned* [Dataset]. Hugging Face.
   https://huggingface.co/datasets/RyokoExtra/TvTroper-Cleaned
3. KaraKaraWitch. (2025). *TvTroper-2025* [Dataset]. Hugging Face.
   https://huggingface.co/datasets/KaraKaraWitch/TvTroper-2025
4. TVTropes. *tvtropes.org* — source wiki for the scraped content.

---

## Closing

The world is quiet here. A wiki about every story, flattened into 651,522 rows —
including the pages that were never there.
