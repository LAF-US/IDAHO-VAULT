---
title: "Fleet Report — The Party & the Center: Working Set and Swap Point"
date created: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Slot under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
---

# Fleet Report — The Party & the Center: Working Set and Swap Point

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

Anchor, from POKEMON-GAME-MECHANICS-MAP-2026-05-03.md: "Pokemon Party | Active session context | Small, curated working set; 6-slot pressure maps to token/window limits." / "Pokemon Center terminal | Session start / retrieval moment | The point where context is loaded from storage into the active party." / "Party is volatile and narrow."

## The Mechanic (as it actually works)

- A **party** is a group of up to six Pokémon a Trainer carries; the limit is six in every core-series generation from Generation I (1996) onward. [verified] https://bulbapedia.bulbagarden.net/wiki/Party
- Pokémon beyond six are held in a separate **Pokémon Storage System**: numbered **Boxes**, accessed via a **PC** — most commonly the PC found inside a **Pokémon Center**, but also in Day Cares, player bedrooms, and battle facilities. **Deposit** moves a party Pokémon into a box slot; **withdraw** moves a box Pokémon into an open party slot. [verified] https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System
- Box capacity grew per generation (Gen I: 12 boxes x 20 = 240; Gen IV: 18 x 30 = 540; Gen VI+: up to 930-1200), but the six-slot party ceiling never changed. [verified] https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System
- Access changed structurally in Gen VIII: the **Pokémon Box Link**, a key item, lets the player deposit/withdraw from the party menu without physically reaching a PC (extended in GO and Let's Go as the sole storage interface). This removed the "must return to a Center" travel cost that every prior generation enforced. [verified] https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Box_Link
- The party, not the box, is where mechanical state accrues: only party Pokémon gain **experience points** and stat experience (EVs) from battle; a boxed Pokémon earns nothing even via Exp. Share, which only redistributes XP among non-fainted party members. [verified] https://bulbapedia.bulbagarden.net/wiki/Experience , https://bulbapedia.bulbagarden.net/wiki/Exp._Share
- Only party Pokémon gain friendship (every 256 steps), can hold and use items in the field, can have out-of-battle Abilities trigger, and can carry/hatch an **Egg** (max 5 Eggs at once, since Eggs can't battle and count toward the 6 slots); Eggs only progress toward hatching while in the party. [verified] https://bulbapedia.bulbagarden.net/wiki/Party , https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Egg
- In Generation I only, depositing into the box did not restore HP or status on withdrawal. Setting aside those parity issues, the general rule from Gen II forward is that status conditions are effectively cleared on deposit because the box only stores a reduced data structure (Gen III: 80 of 100 bytes) — level, HP, etc. are recalculated on withdraw. [verified] https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_III)
- **You cannot deposit your last party Pokémon.** The game blocks it and displays "That's your last Pokémon!" — the party may never reach zero. [verified] https://bulbapedia.bulbagarden.net/wiki/Glitzer_Popping
- Full-party catch handling changed materially across generations: Gen I-II, you cannot even throw a Poké Ball if both the party and the current box are full. Gen III added box-overflow routing (send to next open box). Gen IV onward lets you throw regardless, but the catch is auto-released if there's truly nowhere to put it. [verified] https://bulbapedia.bulbagarden.net/wiki/PC , https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System

## The Problem It Solved

Designers needed a bound on how much a player actively manages at once (battle order, held items, XP allocation) while still letting a player accumulate hundreds of Pokémon over a playthrough. The party/box split answers this by making "active and load-bearing" (party) structurally smaller and different in kind from "possessed but dormant" (box): the box is bulk-storage with reduced data and no progression; the party is the only place mechanics (XP, friendship, hatching, held-item effects) actually fire. The Center/PC is the sole named swap point between the two states, historically forcing a deliberate trip (a session boundary) to change what's active — a cost Gen VIII's Box Link later chose to remove.

## Constraints & Failure Modes

- Hard floor of 1: the party can shrink to six minus stored, but never to zero; the deposit UI itself refuses the action. [verified] https://bulbapedia.bulbagarden.net/wiki/Glitzer_Popping
- Full-party + full-current-box is a real soft-lock in Gen I-II (can't throw a ball at all); later generations degrade this to silent loss (auto-release) rather than a hard block, trading a blocked action for a silent one. [verified] https://bulbapedia.bulbagarden.net/wiki/PC
- Story-critical legendary encounters (Reshiram/Zekrom, Latios/Latias, Solgaleo/Lunala, Zacian/Zamazenta) can strand progress if party and storage are both full at the trigger point; some games (Gen V) let a player accidentally full-lock themselves out of a mandatory catch by over-filling both pools before the encounter. [verified] https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System
- **Bad Eggs**: a corrupted Egg state that behaves like a real Egg (can't battle, can't be released, can't be deposited into Bank/HOME) but never resolves — it permanently occupies a slot until a new save file. This is a genuine, documented data-integrity failure mode, not folklore. [verified] https://bulbapedia.bulbagarden.net/wiki/Bad_Egg
- **Glitzer Popping / Pomeg glitch** (Gen III): deliberately depositing the last Pokémon via a specific exploit sequence causes the party-count pointer to underflow, letting the game read PC box memory, Day Care data, and other save regions as if they were party slots — real, reproducible memory corruption stemming from the "never zero" invariant being circumvented. [verified] https://bulbapedia.bulbagarden.net/wiki/Glitzer_Popping
- **MissingNo.** (Gen I): encountering/battling this out-of-bounds species can scramble sprites and corrupt Hall of Fame save data due to an undersized sprite-decompression buffer sitting near save memory; the mechanism is documented and real. The broader mythology around it ("it eats your save," "guaranteed box wipes every time") is largely amplified folklore layered on top of a narrower, real bug. [lore, mechanism itself verified] https://bulbapedia.bulbagarden.net/wiki/MissingNo.

## What the Swarm Analogue Requires

Requirements a swarm's working-set mechanism must satisfy to earn the party/box analogue. Mapping is [inferred] from the mechanic above, not prescribed by it.

- [inferred] The active set must have a small, fixed, non-negotiable ceiling (the "6") — pressure at that ceiling is the point, not a bug to engineer away.
- [inferred] The active set must never be permitted to reach zero-context (the "last Pokémon" floor) — a swap-out action that would leave nothing active must be refused at the point of attempt, not detected after.
- [inferred] Progression signals (the swarm's analogue to XP/EVs/friendship) must accrue only to items in the active set; dormant/stored items must be inert with respect to those signals, and re-activation must not fabricate progression that didn't happen while dormant.
- [inferred] There must be exactly one named, explicit operation for moving an item between dormant and active state (deposit/withdraw), and it must be auditable as a discrete event, not an ambient side effect.
- [inferred] The swap point (Center/PC analogue) may be loosened toward on-demand access (as Gen VIII did with Box Link) only as an explicit design change, and that change should record what cost it removes (here: the travel/session-boundary cost) — not silently.
- [inferred] Full-and-full contention (active set full, dormant store also full or otherwise blocked) must degrade predictably: either the action is refused outright, or the newly-arriving item is deterministically discarded/rejected — never silently corrupting an existing active-set member.
- [inferred] Malformed or unresolvable items (the Bad Egg analogue) must be prevented from entering the active set in the first place, or the design must accept that such an item can permanently consume a slot until a hard reset — this tradeoff should be a conscious decision, not an emergent one.
- [inferred] Any mechanism that reads or writes active-set membership by direct memory/state manipulation, bypassing the deposit/withdraw operation, is the attack surface that produced Glitzer Popping and MissingNo. corruption; the analogue's implementation must not expose an equivalent raw-pointer path around its own accounting.

## Sources

- https://bulbapedia.bulbagarden.net/wiki/Party
- https://bulbapedia.bulbagarden.net/wiki/PC
- https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Storage_System
- https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Box_Link
- https://bulbapedia.bulbagarden.net/wiki/Experience
- https://bulbapedia.bulbagarden.net/wiki/Exp._Share
- https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_Egg
- https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_structure_(Generation_III)
- https://bulbapedia.bulbagarden.net/wiki/Bad_Egg
- https://bulbapedia.bulbagarden.net/wiki/Glitzer_Popping
- https://bulbapedia.bulbagarden.net/wiki/MissingNo.

###### [["The world is quiet here."]]
