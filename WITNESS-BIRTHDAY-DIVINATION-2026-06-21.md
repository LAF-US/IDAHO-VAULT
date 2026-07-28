---
title: "Witness — Birthday Divination (reverse-engineering the natal hour)"
created: 2026-06-21
updated: 2026-06-21
status: draft
authority: LOGAN
doc_class: witness
authors:
  - Claude Code CLI
related:
  - Logan Finney
  - DRIVE-REGISTRY
  - WITNESS-PENDING-NOT-DONE-2026-06-21
tags:
  - witness
  - astrology
  - astronomy
  - logan
  - birthday
---

# Witness — Birthday Divination

A record of a small, consented exercise: estimate **what time of day Logan was born**
from his Sun/Moon/Rising plus public-record biography — and, just as importantly, mark the
edges of what that method *can't* know. Opened 2026-06-21 at Logan's request, with explicit
permission to look him up for public info.

> The five W's, applied to a birth: **who** is settled, **why** is play. This note is the
> **when** (time of day) and **where** (place) — and an honest accounting of how firm each is.

---

## The given — from Logan, firsthand `[GIVEN]`

| Placement | Sign |
| --- | --- |
| **Sun** | Virgo |
| **Moon** | Scorpio |
| **Rising (Ascendant)** | Scorpio |

A "double Scorpio" (Moon + Rising) — which is why the `timemachine` drive wears a Double
Scorpio sticker (see [[DRIVE-REGISTRY]], [[Logan Finney]]).

## The researched — public record `[EVIDENCE]`

- **Birthplace: North Idaho panhandle** — crucially the panhandle **keeps Pacific Time** and
  sits at a **high northern latitude** (the load-bearing fact for the estimate below). Grounding:
  IPTV bio ("North Idaho native"). *(Handle, precise birthplace/hospital, and the exact
  county/latitude were dropped 2026-06-22 to keep the committed record at public-bio
  granularity; precise coordinates are an input supplied at ephemeris run time, not committed here.)*
- **Sun in Virgo, early-to-mid September.** Corroborated by the *Untitled Goose Game* tweet
  (Aug 18 2020: the free update is "coming not long after my birthday 🦢"; that co-op update
  shipped **Sept 23 2020**).
- **Born late 1990s.** From **U of Idaho B.S., Broadcast & Digital Media Journalism,
  2016–2020** — a September-born fall-2016 freshman turning 18 around term's start. (Exact year
  withheld from the committed record; supplied at ephemeris run time.)
- **Anomaly, not hidden:** a 2021-04-23 tweet, "Worst birthday week ever," reads *Taurus*, not
  Virgo. Held as **not Logan's own birthday** (or sarcasm) — flagged, not reconciled. `[CONFLICT]`

## The method — astronomy `[METHOD]`

The Ascendant is whatever zodiac degree sits on the **eastern horizon** at birth; the **Sun's
position relative to that horizon is the clock.** At sunrise the Sun ≈ the Ascendant; it
climbs to the **Midheaven (~local solar noon)**, sets at the Descendant, bottoms at the IC
(midnight).

Whole-sign houses with **Scorpio rising** put **Virgo in the 11th house** (Sco 1 · Sag 2 · …
· **Vir 11** · Lib 12). The 11th sits **above the horizon, two houses up, just shy of the
Midheaven** — so the Sun has well cleared the horizon and is **near culmination**: a **morning
birth, late in the morning.**

## The estimate `[ESTIMATE]`

> **Late morning — roughly 11:00 AM – 12:30 PM Pacific, near midday, Sun high and approaching
> culmination.**

At the panhandle's **high northern latitude** this skews a touch **later** than a generic reading, because
Virgo/Libra/Scorpio are **long-ascension** signs in the northern hemisphere (they rise slowly),
stretching the span between sunrise (Virgo on the horizon) and Scorpio reaching the Ascendant.

---

## Where the method runs out `[LIMITS]`

- **The exact birth *day* is not public.** Squeezed the tweet archive, the github.io site
  (empty index stubs), and every bio — Virgo/early-mid-September is the floor.
- **The birth *time itself* cannot be derived** — only the *time-of-day band* implied by the
  chart. This is reverse-engineering, not retrieval.
- **Self-witnessed error:** mid-reasoning I flipped the long-/short-ascension direction once
  and corrected it. Trust the **shape** (morning · Sun high · near midday) over any single
  minute. `[REPAIR]`
- **To convert estimate → computation:** give the **exact September day** (plus the precise
  birthplace coordinates and birth year, kept out of this committed record) and I'll run a real
  ephemeris + house calc and return a tight Ascendant degree and birth-hour window. Those are
  inputs research shouldn't pin down in public.

---

## See also
[[Logan Finney]] · [[DRIVE-REGISTRY]] (the Double Scorpio drive) · [[WITNESS-PENDING-NOT-DONE-2026-06-21]] (sibling witness)

*Provenance key: `[GIVEN]` = Logan firsthand · `[EVIDENCE]` = public record/verifiable ·
`[ESTIMATE]` = reasoned-but-unverified · `[CONFLICT]`/`[REPAIR]` = surfaced, not papered over.*

---

## DOCUMENT METADATA

- **Created:** 2026-06-21
- **Last Updated:** 2026-06-22
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** Claude Code CLI
- **Change Note:** Witnessed a consented birthday-divination pass: recorded Logan's given Sun/Moon/Rising (Virgo/Scorpio/Scorpio), the public-bio birthplace (North Idaho panhandle, Pacific, high northern latitude), the astronomy method (Sun in the 11th house ⇒ late-morning birth), and the estimate (~11 AM–12:30 PM Pacific). Flagged the April "birthday week" anomaly, the unknowable exact day/time, and a self-corrected ascension error. **PII pass 2026-06-22 (Copilot #609):** coarsened committed birthplace to public-bio granularity and withheld exact county/latitude/birth year — those are inputs supplied at ephemeris run time, not committed facts. Pending the exact day for a real ephemeris run.
