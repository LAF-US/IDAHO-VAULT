---
title: "Fleet Report — Bank to HOME: the Transfer Lineage and Cross-Session Persistence"
date created: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Porter under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
---

# Fleet Report — Bank to HOME: the Transfer Lineage and Cross-Session Persistence

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

## The Mechanic (as it actually works)

Per the map's anchor line: "Pokemon Bank | Bridge registry | Transitional cloud layer between cartridge-era storage and HOME." A **bridge** here means a one-directional migration path with a planned end-state, not a permanent home. Bank was a paid Nintendo 3DS cloud-storage app: 100 Boxes of 30 slots each, 3,000 Pokémon total, launched Dec 25 2013 – Feb 5 2014 by region [verified: bulbapedia.bulbagarden.net/wiki/Pokémon_Bank]. Its companion, **Poké Transporter**, did one-way ingestion only — it pulled Pokémon from Generation V cartridges and Gen I/II Virtual Console into a reserved 101st "Transport Box" that Pokémon could leave but never re-enter, 30 at a time, ineligible Pokémon simply left behind in the source box [verified: bulbapedia.bulbagarden.net/wiki/Poké_Transporter].

"Pokemon HOME | Missing artifact registry | Cross-session, machine-queryable persistence for outputs and decisions." Operationally, HOME is a **cloud service** — a server-side store keyed to a Nintendo Account rather than to any one cartridge or console — with a free **Basic Plan** (30 Pokémon storage cap, no Bank transfer) and a paid **Premium Plan** (6,000 Pokémon; 10-slot Wonder Box; 3-slot GTS; Room Trade hosting; Judge/IV-check function; Bank transfer unlocked) [verified: home.pokemon.com/en-us/, en-americas-support.nintendo.com/app/answers/detail/a_id/48803]. A **deposit** is the write operation (Box → HOME); a **withdraw** is the read-and-remove; a **transfer** moves a Pokémon's record from one game's live save into HOME's store or vice versa.

Two features do work beyond storage: the **National Pokédex** auto-registers a species (and its Mega/Gigantamax forms) the moment any specimen is deposited — it is an index of *species seen*, not a second copy of the data [verified: home.pokemon.com/en-us/features/]. The **origin mark** is a single, immutable icon on a Pokémon's own record stamped at first entry, naming the exact game it came from (Game Boy icon = Virtual Console via Transporter; GO icon; Galar symbol for Sword/Shield-era HOME arrivals) — it is per-record provenance metadata, not a registry-level field, and Bulbapedia is explicit that "a Pokémon can only have one origin mark, and it cannot be changed" [verified: bulbapedia.bulbagarden.net/wiki/Origin_mark]. **Wonder Box** and **GTS** are owner-transfer features — Wonder Box randomly swaps a deposited Pokémon for a stranger's after a wait (1 hour as of the cited version); GTS matches a specific ask against a specific offer [verified: home.pokemon.com/en-us/trade/, bulbapedia.bulbagarden.net/wiki/Pokémon_HOME].

## The Problem It Solved

Bank solved discoverability-under-obsolescence: cartridges die, consoles get replaced, and a Pokémon caught on a doomed generation needed a path forward that didn't require keeping the old hardware alive forever. But Bank was still cartridge-shaped — a rented cloud shelf, subscription-gated, with no cross-game intelligence of its own. HOME solved the harder problem Bank couldn't: a Pokémon's full history (species seen, exact game of origin, its meaningful data) needed to persist and be *machine-checkable* independent of which specific game session last touched it, and needed to survive the holder switching hardware, since identity is anchored to the Nintendo Account rather than to a device [verified: en-americas-support.nintendo.com — "Pokémon HOME on Nintendo Switch 2 and Nintendo Switch is tied to your Nintendo Account, so you can connect with any console that your Nintendo Account is associated to"].

## Constraints & Failure Modes

- **The Bank EOL/archival lesson.** 3DS/Wii U online services broadly ended April 8, 2024, but Nintendo carved Bank and Transporter out as exceptions "that may also end at some point in the future" [verified: pokemonblog.com, 2024-03-26; nintendolife.com, 2024-01-25]. Official guidance told users to migrate to HOME "at their earliest convenience" *before* any hard deadline arrived — archival was framed as urgent even absent a stated end date. Bank was later made free to use, explicitly so people could still complete the one-way move to HOME, but new paid passes stopped selling and the apps were pulled from download entirely [verified: en-americas-support.nintendo.com/app/answers/detail/a_id/61543]. The lesson: a bridge layer's failure mode is silent narrowing (no new entrants) followed by full closure, and the safe window to migrate closes long before the formal shutdown date is ever announced.
- **Expired-subscription lockout, not deletion.** If a Bank pass lapsed, deposited Pokémon became time-limited: "you have a certain amount of time... after this period elapses, those Pokémon are lost... we do not have any way to restore them" [verified: nintendolife.com/news/2020/02, quoting Nintendo Support]. HOME's equivalent is softer but still a **one-way door of access, not data**: dropping from Premium to Basic with 31+ Pokémon stored locks everything past the 30 most-recently-deposited/traded — visible count only, no view, no withdraw — until Premium is re-enrolled [verified: support.pokemon.com/hc/en-us/articles/360039615831].
- **One-way doors in the connectivity matrix.** Once a Let's Go Pikachu/Eevee-origin Pokémon is moved into a newer game, "it cannot be returned to its original game" [verified: Bulbapedia, Pokémon HOME]. Once a Pokémon enters HOME from Bank or Pokémon GO, it converts to the Sword/Shield-era format and can never re-enter Bank or GO. Sword/Shield and the current-generation mainline titles are the two-way exception — full deposit/withdraw both directions — but even there, entering the newest title (Legends: Z-A) forecloses return to older mainline titles.
- **Transfer strips, doesn't preserve, some data.** Held items never transfer: any item a Pokémon carries into a deposit is stripped and dropped into the sender's in-game Bag, because "HOME does not have an item storage function" [verified: support.pokemon.com/hc/en-us/articles/360039207832; gamefaqs.gamespot.com/switch/259372]. Move-sets can also be silently regenerated on first entry to a new target game before the transfer is even confirmed.
- **Species/game gating is per-entity, not registry-wide.** Certain species (Spinda, Nincada, others) have documented per-title deposit/withdraw restrictions; a Pokémon's compatible-games list is checked per record, not assumed from the registry's existence [verified: support.pokemon.com/hc/en-us/articles/360039592832; support.pokemon.com — Nincada/Spinda FAQ entries].

## What the Swarm Analogue Requires

The following are requirements only, drawn from the mechanic above, [inferred] — no implementation choice is proposed:

- A durable artifact store must be addressed by a stable identity (Nintendo Account-equivalent) that survives the death of whichever session, device, or agent instance last wrote to it — not by session ID or thread ID.
- Every artifact must carry immutable, single-valued origin metadata fixed at first write (the origin-mark analogue): which session/agent produced it and under what conditions, queryable without opening the artifact's full body.
- The store must expose a species-level index (the National Pokédex analogue) separate from the full records: a cheap, machine-queryable answer to "has anything of this kind ever been produced," distinct from "give me the full record."
- Ingestion paths from older/deprecated storage must be explicit and one-way where necessary, with an announced, generous migration window before any deprecated path is closed — mirroring the Bank EOL pattern of "make it free, keep it open past its stated shelf life, but warn early and often."
- Compatibility between what a session/agent can write and what another can read must be checked per-artifact-type against the target's capabilities, not assumed globally — some artifact types will not be legible to all consumers, the same way certain Pokémon cannot enter certain games.
- The system must define, explicitly, what is preserved verbatim across a transfer/handoff and what is stripped or reprocessed (the held-item rule) — silent, undocumented data loss in transit is the specific failure this mechanic warns against.
- Access-tier limits (if any exist) must degrade to reduced visibility of the newest/oldest data, never to silent deletion — the Basic/Premium lockout model, not the lapsed-Bank-pass deletion model, is the safer failure mode to require.
- One-way transitions (once an artifact is "promoted" past a given stage it cannot return to an earlier one) must be surfaced to the writer before the action is taken, not discovered after the fact.

## Sources

- home.pokemon.com/en-us/, home.pokemon.com/en-us/features/, home.pokemon.com/en-us/trade/ [verified]
- en-americas-support.nintendo.com/app/answers/detail/a_id/48803 (Pokémon HOME FAQ) [verified]
- en-americas-support.nintendo.com/app/answers/detail/a_id/61543 (Pokémon Bank Service Update) [verified]
- support.pokemon.com/hc/en-us/articles/360039615831, 360039207832, 360039592832, 360039206112 [verified]
- bulbapedia.bulbagarden.net/wiki/Pokémon_Bank, /Poké_Transporter, /Pokémon_HOME, /Origin_mark, /Game_of_origin [verified]
- nintendolife.com/news/2020/02 and /news/2024/01; pokemonblog.com/2024/03/26 [verified]
- serebii.net/pokemonhome/subscription.shtml, /features.shtml, /transfer.shtml [verified]

###### [["The world is quiet here."]]
