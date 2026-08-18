---
title: "Fleet Report — The PC Boxes: Durable, Organized, Fixed-Point Storage"
date created: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Bill under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
---

# Fleet Report — The PC Boxes: Durable, Organized, Fixed-Point Storage

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

Anchor, from POKEMON-GAME-MECHANICS-MAP-2026-05-03.md: "Pokemon PC / Boxes | Shared vault / repo corpus | Durable, organized, fixed-point storage for canonical work products." Working conclusion on file: "The vault already has a strong PC layer."

## The Mechanic (as it actually works)

The storage system's own vocabulary: a **box** holds a fixed number of **slots**; a Pokémon is **deposited** into a box or **withdrawn** from it; the whole apparatus is the **Pokémon Storage System** (also "PC," "PC Box"). [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System]

Box counts × capacity by generation (boxes × slots-per-box = total slots): Gen I 12×20=240 (8×30=240 JP); Gen II 14×20=280 (9×30=270 JP); Gen III 14×30=420; Gen IV 18×30=540; Gen V 8/16/24×30=720; Gen VI 30×30=900; SM/USUM 32×30=960; Let's Go 1×1,000; Sw/Sh 32×30=960; BDSP 40×30=1,200; Legends Arceus 32×30=960; SV 32×30=960. [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System]

Ownership: the system is a maintained **service** with a named maintainer per region, not an anonymous utility. Bill built the original (Kanto/Johto); named successors tinker with and maintain regional forks: Lanette (Hoenn), Bebe (Sinnoh — "My buddy Bill developed the basic storage system. I tinkered with it here and there to make it easier for me to use."), Amanita (Unova), Cassius (Kalos), Molayne (Alola). In-game, the UI literally reads "Someone's PC" until the player meets that region's maintainer, at which point it becomes "Bill's PC," "Bebe's PC," etc. [verified, https://bulbapedia.bulbagarden.net/wiki/Bill] [verified, https://bulbapedia.bulbagarden.net/wiki/Bebe] [verified, https://bulbapedia.bulbagarden.net/wiki/PC]

Organization affordances and arrival generation: box naming arrived Gen II (custom names, 8-char limit, later 14 then 16); wallpapers (purely cosmetic, box-distinguishing) arrived Gen III; sorting (by catch order, Pokédex #, level, CP, favorites-on-top, species name) and attribute search (name/type/move/TM/nature/gender/markings) reached full expression in Let's Go / Sw-Sh's Box Link UI; Group Move Mode ("Tray," rectangular multi-slot selection and relocation) arrived Gen V, building on a Gen III "Relocate Mode" precursor. [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System] [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Box_Link]

Box Link (Let's Go 2018; Sw/Sh, BDSP, Legends Arceus, SV) let the storage system be reached from the party menu almost anywhere in the world — no physical PC required — with explicit exceptions (Gym Challenges, Champion Cup, Legends Arceus's League). [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Box_Link]

Gen I/II save-before-switch: changing the active box forced an explicit save prompt ("When you change a #MON BOX, data will be saved. OK?"). Only one box lived in working memory (Bank 1/wMisc) at a time; switching copied the outgoing box out to SRAM banks 2/3, recalculated a checksum over it, then copied the incoming box in. This was consistency-by-force: the design assumed a battery-powered, power-loss-prone device (Game Boy) and treated "one box in memory" plus "commit on every switch" as the only way to guarantee the box and its checksum never diverged. [verified, https://github.com/pret/pokecrystal/blob/b35eb72290b964b98844afbe741bb7ede34b9ef3/engine/save.asm] [verified, https://retrocomputing.stackexchange.com/questions/13237/what-technological-limitations-required-the-box-system-in-gen-1-pok%c3%a9mon-games]

Full-box handling: Gen I–III, if party AND current box are both full, the game refuses to let the player even throw a Poké Ball. From Gen III onward, a catch with a full current-box-but-open-party routes automatically to the next open box. From Gen IV, catching with everything full is allowed but the catch is auto-released. Gen V added a box-unlock gate (new box tranches require every visible box to hold ≥1 Pokémon first; bypassable via Bank/HOME). At absolute total capacity, several titles hard-block story progress (OR/AS Southern Island, Sw/Sh Zacian/Zamazenta) until the player frees space — total capacity is a real, enforced ceiling, not a soft cap. [verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System]

## The Problem It Solved

Party capacity (6) is far smaller than achievable collection size; the PC decouples "what you can act with" from "what you durably own," giving a canonical off-path store that survives resets, screen transitions, and (in later gens) region boundaries — while remaining a single fixed-point location per save file, not scattered inventory.

## Constraints & Failure Modes

- **[lore]** Gen I/II box-switch save exploitation is the origin of the community's "cloning glitch": interrupting the forced save at a precise moment during a box switch could leave a Pokémon simultaneously in both the outgoing box and the party, because the two-phase (boxes-then-party) commit was not atomic against power interruption.
- **[verified, https://glitchcity.wiki/wiki/Bad_clone_glitch]** "Bad clone" folklore: uninitialized SRAM in never-yet-filled empty slots, combined with a reset mid-write, could surface a box slot whose species byte was written but whose full record wasn't — producing "?????"-named, level-0 corrupt entries. Ironically, a box that had *ever* been filled once was safe from this because leftover slot-20 data always got overwritten with real data, foreclosing "useful" corruption.
- **[verified, https://retrocomputing.stackexchange.com/questions/13237/what-technological-limitations-required-the-box-system-in-gen-1-pok%c3%a9mon-games]** The Gen I "current box only" constraint (one box cached in working memory) existed because the platform couldn't hold all 12 boxes live at once; every switch was therefore a full serialize-checksum-deserialize cycle, not a lightweight pointer move.
- **[verified, https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System]** Full-box-plus-full-party in Gen I–III blocks the *initiating action* (can't throw a ball) rather than accepting-then-rejecting — a hard admission-control failure mode later generations relaxed into auto-release or auto-routing.

## What the Swarm Analogue Requires

- Durable storage must be a **maintained service with a named, discoverable owner** at any given time — not an anonymous store — so a consumer can ask "whose PC is this?" and get an answer. [inferred]
- Storage must expose **fixed-capacity units** (boxes/slots) with knowable, queryable limits, not unbounded elastic space — capacity ceilings should be visible before they're hit. [inferred]
- Full-capacity conditions must be **handled explicitly** (reroute to next unit, block the write, or release-with-warning) rather than silently overflowing or silently dropping data. [inferred]
- Any operation that switches the "current" working unit should **serialize outgoing state before admitting incoming state** — the swarm's analogue to the Gen I forced save-on-switch — to avoid the two-writers-in-one-slot class of corruption. [inferred]
- Multi-item operations (the Group Selection precedent) should exist for **organizing at scale**, not just single-record deposit/withdraw, once volume passes a threshold. [inferred]
- Anywhere-access (the Box Link precedent) is a **later-generation upgrade**, not a day-one requirement — the sequence "fixed physical access point first, remote access later" is itself informative for phased rollout. [inferred]

## Sources

- Pokémon Storage System — https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System
- Bill — https://bulbapedia.bulbagarden.net/wiki/Bill
- Bebe — https://bulbapedia.bulbagarden.net/wiki/Bebe
- PC — https://bulbapedia.bulbagarden.net/wiki/PC
- Pokémon Box Link — https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Box_Link
- Save data structure (Generation I) — https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_I)
- pret/pokecrystal engine/save.asm (ChangeBoxSaveGame) — https://github.com/pret/pokecrystal/blob/b35eb72290b964b98844afbe741bb7ede34b9ef3/engine/save.asm
- What technological limitations required the box system (Retrocomputing SE) — https://retrocomputing.stackexchange.com/questions/13237/what-technological-limitations-required-the-box-system-in-gen-1-pok%c3%a9mon-games
- Bad clone glitch — https://glitchcity.wiki/wiki/Bad_clone_glitch
- Cloning glitches — https://bulbapedia.bulbagarden.net/wiki/Cloning_glitches

###### [["The world is quiet here."]]
