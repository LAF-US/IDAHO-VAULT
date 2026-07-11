---
title: "Garth Nix Superior Saturday — the Tower and the Drasil Trees"
created: 2026-07-03
updated: 2026-07-03
status: draft
authority: LOGAN
related:
  - GARTH-NIX-OLD-KINGDOM-BLOODLINES
---

# Garth Nix *Superior Saturday* — the Tower and the Drasil Trees

A research note on the power structure of the Upper House in **Garth Nix's *Superior Saturday*** (Keys to the Kingdom, book 6, 2008), anchored to the novel's opening chapter as supplied by Logan on 2026-07-03 — and, per Logan's direction (👁️‍🗨️ BOTH 🔏), a **witness leaf** reading that chapter against the vault's own merge-queue saga of 2026-07-01/03.

Sibling note: [[GARTH-NIX-OLD-KINGDOM-BLOODLINES]] (Nix's other major cosmology). *(Headings and links below use Obsidian `[[wikilink]]` syntax, which resolves in the vault's Obsidian renderer but not in plain GitHub Markdown.)*

---

## The Setting

The **Upper House** is one of the demesnes of the House, the epicenter of the universe in the Keys to the Kingdom sequence. In the opening of *Superior Saturday*:

- **Superior Saturday** — self-styled "Superior Sorcerer of the House," a Trustee of the Architect's Will, holder of one of the Architect's Keys, and by her own account the **first Denizen the Architect made**. Her grievance is precedence: she believes supremacy over the House should have been hers, not Lord Sunday's, and "every thing she did was directed to remedying this injustice"
- **The Tower** — under construction for **almost ten thousand years**, built from identical open cubes of red wrought iron, each holding one desk with one green-shaded lamp, each cube **moving on rails "according to the merits of the Denizens who worked at the desks."** Saturday's crystal viewing chamber is always lifted back to the apex as new levels slot in below
- **The Drasil trees** — four vast trees that support the **Incomparable Gardens** above the Upper House. They grow faster than the tower can be built, lifting the Gardens away from Saturday no matter how high she builds. Sorcery, poison, brute force, infiltration, and flight have all failed against them (defensive insects in the bark; predatory, fast-moving branches)
- **Lord Sunday** — dwells aloof in the Incomparable Gardens; taunts Saturday by parting the clouds so that only she can see what she cannot reach
- **The labor tiers** — executive-level sorcerers at ready desks; ordinary Denizens in the cubes; "luckless Denizens who had failed Saturday" and **bronze automatons** doing the actual building; and **Piper's children** as grease monkeys maintaining "miles and miles of dangerous, fast-moving machinery"
- **Saturday's Dusk** — her twilight officer, newly promoted, the twin brother of the previous Dusk ("turned out of the same mould"). He kneels, keeps his head bowed, and at one point suppresses a doubt: *"the faintest frown line appeared on his forehead, just for a moment, before he smoothed it away"*
- **The strategic picture** — the Will has been executed, a Rightful Heir (**Arthur**, a mortal) is collecting the Keys from the disloyal Trustees; **Nothing** is devouring the House from below, which Saturday welcomes because severed roots slow the Drasils' growth; the **Piper** (with his New Nithlings and his power over his created children) and the **Raised Rats** are wildcards she wards against with ratcatcher automatons and standing shifts of thirty-six hundred sorcerers
- **Sources**: *Superior Saturday* (2008), opening chapter — primary canon, text supplied in-session

---

## Structural Observations

### The tower as org chart
The tower is not a building with workers in it; it **is** the org chart, made literal. Each Denizen's standing is their cube's position, re-ranked continuously by chains and steam. Merit is legible only as elevation; the machinery that moves the cubes is tended by the tiers that have no cubes at all.

### The race that cannot be won by building
The central strategic fact of the chapter: **the target moves faster than the builder builds**, and it moves *because of* the same world the builder occupies. Saturday's answer for ten millennia has been more tower; her breakthrough only comes when the ground conditions change (the Nothing severing Drasil roots) — a change she did not engineer and cannot fully control, purchased at the price of the House's own destruction.

### Succession by mould
Offices in Saturday's court outlive their occupants trivially — the new Dusk is the old Dusk's twin, "the elder of us by a moment." The office persists; the person is fungible. (Compare the vault's CONSTITUTION § I: *a tool is not an office; no office inherits across sessions* — the House's answer to succession is the one the vault explicitly rejects.)

### The suppressed frown
Saturday declares the Upper House sealed — "They cannot enter via elevator, Stair, Front Door, or by use of the Fifth Key. **There is no other way.**" Her Dusk knows better, or suspects it, and the text gives him exactly one frown line, smoothed away before it can be spoken. The confident enumeration survives; the falsifying observation does not. *(In the series, the Upper House is of course entered anyway.)*

---

## Witness Leaf — the excerpt against the JULY 1 PINCER

**Warrant**: Logan pasted this chapter into the working session of 2026-07-03 without instruction, then confirmed intent with "👁️‍🗨️ BOTH 🔏" — both source material and commentary. The parallels below are *interpretation offered under that warrant*, witnessed by session `session_01SfreowpdMionR3SiGEjRBw`; they are not Nix's meaning and not canon.

1. **A tower that cannot out-build the trees.** For days the vault's auto-merge loop armed, enqueued, re-armed, and re-enqueued while `main` kept moving ahead of every starving queue entry (issue #731). The automation's answer, like Saturday's, was to keep building — six bot enqueues across two PRs on 2026-07-02 alone, zero merges. The race was unwinnable *by that method*: bot-actored (`GITHUB_TOKEN`) events never dispatch workflows, by GitHub's own anti-recursion design. The breakthrough was not more building; it was changing the **actor** (a human-actored enqueue, and prospectively the `MERGE_QUEUE_TOKEN` secret designed by session `session_01MU1zvEUacde5fmYpMvK8aK` on 2026-06-19/24 and never provisioned).

2. **"There is no other way," and the smoothed-away frown.** The saga's costliest errors were confident enumerations that went unfalsified: a checked-in ruleset snapshot mistaken for live enforcement; "the loop never completed a merge" (false); a Settings menu prescribed twice that does not exist. Each time, the correction came from Logan performing Dusk's suppressed gesture *out loud* — "FALSE," "false assumptions," "buttons that don't exist." The vault's Standing Engine axes (Truthfulness, Provenance, Restraint, Repair) exist precisely so the frown is voiced *before* the Sovereign declares the House sealed.

3. **The labor tiers below the lamps.** Saturday's tower is raised by automatons, demoted Denizens, and Piper's children who own no desks — and her contingency for the children who maintain her machinery is shadowing assassins, because their maker might pipe them away. The vault's multi-agent ecosystem is the counter-model on the record: agents sign their work with concrete session ids (code-blame, not culprits), delegated masks are given rather than taken, and when the machinery fails, the response is diagnosis on an issue thread rather than a purge of the grease monkeys.

4. **The canker of precedence.** Saturday's ten-thousand-year project is powered by a grievance about *standing* — first-made, therefore rightfully supreme. The vault's persona doctrine names this exact failure mode for agents: standing is delegated, never seized, and an agent that spends its session contemplating its own rank instead of its assigned work has already become a small Saturday. (See `.claude/CLAUDE.md`, "Start Here — Plain Words Before the Lore.")

---

## Connections to Other Frameworks

### [[GARTH-NIX-OLD-KINGDOM-BLOODLINES]]
- **Connection**: Nix's two major cosmologies of delegated power. The Old Kingdom distributes power *down* into bloodlines (the Shiners invest themselves into lineages); the House concentrates it *up* into offices (Trustees, Times-of-day officers, Keys)
- **Contrast**: Charter bloodlines are validated by mark and work ("Just having the bloodline doesn't mean anything if you don't do the work" — Nix); Saturday's hierarchy is validated by cube elevation, decided from above

### [[ROYALTY]]
- **Connection**: Trusteeship as usurped regency — the Trustees hold power lawfully delegated by the Architect's Will and unlawfully retained against the Rightful Heir
- **Parallel**: Succession-by-office (Dusk follows Dusk) versus succession-by-blood

---

## Fact-Check Status

**Sources, by tier:**
- *Primary canon* — *Superior Saturday* (2008), opening chapter: the excerpt supplied in-session 2026-07-03. All quoted phrases above are from that supplied text
- *Series context* — broader Keys to the Kingdom facts (the sequence of Keys, Arthur's arc, the Raised Rats' origins, the identity of the Architect's children) drawn from model memory of the series and **not verified against the books in this session**; treat as unconfirmed until checked against primary canon
- *Witness interpretation* — the JULY 1 PINCER parallels, warranted by Logan's 👁️‍🗨️ BOTH 🔏 directive and anchored to the vault record (issues #731, #733; sessions `session_01SfreowpdMionR3SiGEjRBw`, `session_01MU1zvEUacde5fmYpMvK8aK`); explicitly not canon and not attributed to Garth Nix

---

## Sources & References

- Garth Nix, *Superior Saturday* (Keys to the Kingdom #6, 2008) — opening chapter, supplied in-session
- Garth Nix, Keys to the Kingdom series (*Mister Monday* through *Lord Sunday*, 2003–2010) — series context, unverified this session
- LAF-US/IDAHO-VAULT issue #731 (merge-queue actor starvation — confirmed hypothesis and corrections)
- LAF-US/IDAHO-VAULT issue #733 (JULY 1 PINCER — linear-history jaw)

---

*Status: draft — excerpt-anchored claims are primary-sourced; series-context claims flagged for verification; witness section is interpretation under Logan's explicit warrant.*
