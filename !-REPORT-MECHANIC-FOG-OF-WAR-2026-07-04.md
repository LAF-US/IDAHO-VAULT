---
title: "Fleet Report — Fog of War: Explored Is Not Visible"
date created: 2026-07-04
updated: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Shroud under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
  - "!-RESEARCH-AGENT-TEMPORAL-COGNITION-2026-07-02.md"
---

# Fleet Report — Fog of War: Explored Is Not Visible

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

## The Mechanic (as it actually works)

The canonical model is **three states**, not two [verified: https://pudgycat.io/fog-of-war-in-video-games-explained/, https://liquipedia.net/starcraft2/Fog_of_War]:

1. **unexplored** — never seen by any vision source; rendered solid black; zero terrain data.
2. **shroud** (a.k.a. "explored/fog," greyed) — seen at some point, no vision source there now; terrain persists, but units/dynamic state render at **last-known state** — frozen at whatever was true the moment vision was lost.
3. **visible** — inside a current vision radius; fully live, including enemy units.

Per-game exact behavior [verified]:

- **StarCraft / StarCraft II**: buildings in shroud are drawn at last-known location and condition (being built, burning) but are **not selectable** — health, exact identity, and any change since last sighting are unknowable. Lifted or uprooted buildings are the explicit failure case: the shroud snapshot shows a building that is no longer there. Detector abilities (Scanner Sweep, Observers, sensor towers) are the engine-sanctioned re-scout tools. (liquipedia.net/starcraft2/Fog_of_War; starcraft.fandom.com/wiki/Fog_of_war)
- **Warcraft II** (the source of the vault's exact "shroud vs. fog" terminology): black = unexplored shroud; grey = explored fog. "The terrain that is there is still known, but any units in this Fog of War are not visible… When units re-enter grey areas, their knowledge of the terrain, as well as any units or buildings that inhabit that area, will be updated." Buildings retain last-known existence/condition until re-sighted. [verified: classic.battle.net/war2/basic/fog.shtml; ftp.war2.ru War2BNE manual]
- **Age of Empires**: terrain, once explored, persists permanently (never reverts to unexplored); units and dynamic objects vanish from shroud and only reappear on re-scout. A documented shared-vision bug — allied-scouted buildings disappearing from a player's own already-explored shroud — shows how fragile last-known-state bookkeeping is under multi-party vision. [verified: forums.ageofempires.com/t/bug-enemy-buildings-return-invisible-when-not-in-los]
- **Civilization**: map persists as last-explored; resources and tile improvements shown in shrouded territory can be **stale** — a rival's city, road, or improvement built after your last visit is not reflected until re-scouted. Community modding (a Civ "fog decay" modmod) exists specifically because base Civilization's shroud has *no* freshness decay at all — once explored, a tile's last-known snapshot persists indefinitely with no signal of its own age. [verified: forums.civfanatics.com/threads/map-fog-of-war-decay-modmod.699860]
- **League of Legends (vision-as-instrument variant)**: wards are a *deliberate, costed, decaying* freshness instrument layered onto the shroud/visible split. Vision Score explicitly penalizes a ward's information as it ages — 0% penalty at 60s, scaling to −50% by 120s of "staleness" (no interesting unit crossed it) — operationalizing "how fresh is this vision worth" as a first-class scored quantity. [verified: wiki.leagueoflegends.com/en-us/Vision_score]

## The Problem It Solved

Kriegsspiel (Reisswitz, Prussian Army, 1824) needed a way to represent that a commander's *belief* about enemy position and a battlefield's *actual* current state are different objects. The tabletop mechanic: an umpire placed blocks only for troops in mutual visual range and mentally tracked hidden troops, deploying blocks only when they entered view — i.e., a human-umpire implementation of exactly the unexplored/visible split, with the umpire's private knowledge standing in for "true state." [verified/lore: en.wikipedia.org/wiki/Kriegsspiel] Earlier tabletop wargames (Allgaier 1796, Reisswitz Sr. 1812) used physical setup screens to hide unit positions before play began — a cruder unexplored-only precursor. [verified: doi.org/10.1080/01916599.2017.1366928]

Origin-of-term note (mark carefully): the phrase "fog of war" is **popularly but incorrectly** attributed to Clausewitz. Clausewitz's *On War* never contains the German phrase *Nebel des Krieges*; his own term for battlefield uncertainty is **friction** (used 13+ times), with "fog" appearing only four times, twice literally meteorological. This is a well-documented misattribution, not folklore to repeat uncritically. [verified: clausewitz.com/bibl/Kiesling-OnFog.pdf; iasg.com/blog/2017/08/15/fog-war-no-one-gets-quote-right-concept-stands]

First videogame use: **Empire** (Walter Bright, 1977, PDP-10/FORTRAN, Caltech), inspired directly by Stratego and by real radar-detection history (Battle of Britain, Battle of Midway). Bright, interviewed directly: "the fog of war is impossible with the board game version of Empire, but with computers I knew I could make it work" — the first attested case of the mechanic moving from human-umpire-mediated (Kriegsspiel) to engine-enforced. [verified: madned.substack.com/p/a-talk-with-computer-gaming-pioneer; en.wikipedia.org/wiki/Empire_(1977_video_game)] The shroud-vs-fog *terminology split* used throughout this report is Warcraft II's (1995) explicit naming, distinguishing black "unexplored shroud" from grey "explored fog." [verified: classic.battle.net/war2/basic/fog.shtml]

## Constraints & Failure Modes

- **Map-hack cheating**: the entire game state is stored on every peer's machine in most RTS peer-to-peer architectures (no authoritative server); the "fog" is a *display filter*, not a data restriction. Tools like **Kartograph** passively read local memory to reveal the full map with zero network footprint — completely undetectable remotely. This is the load-bearing lesson: **fog of war enforced only by client-side rendering honor is not fog of war at all**; it must be enforced by restricting what data reaches the client, not by asking the client nicely not to show it. Proposed fixes (OpenConflict's state-partitioning, cryptographic Private-Set-Intersection schemes) exist precisely because "trust the renderer" fails. [verified: dl.acm.org/doi/10.1109/SP.2011.28 (OpenConflict); crypto.stanford.edu/~dabo/pubs/papers/onlinegames.pdf; esoteriic.com/enhancing-fog-of-war-in-multiplayer-games-with-cryptography]
- **Scouting economy (the cost of freshness)**: freshness is never free. StarCraft's Comsat scans cost 50 energy for 12 seconds of truth; League's Control Wards cost 75 gold and decay in value; both formalize "paying to know current state" as a resource-allocation decision, not a passive default. Missing a scout/scan is a documented, named failure: "A Terran player who did not scan with a Comsat could lose to a hidden Lurker rush." [verified: pudgycat.io/fog-of-war-in-video-games-explained; wiki.leagueoflegends.com/en-us/Vision_score]
- **Stale-intel misplays**: acting on a shroud's last-known-state as though it were current is the named pathology this whole mechanic exists to prevent, and it still happens — the AoE lifted-building case and the Civ resource-staleness case above are exactly this failure occurring *inside* correctly-implemented fog systems, because last-known-state rendering, if visually indistinguishable from live rendering, invites exactly the misread it was built to guard against.

## What the Swarm Analogue Requires

[inferred] — requirements only, no implementation:

- Agent memory must expose (at minimum) the three-state distinction, not a binary read/unread flag: **never-observed**, **last-known-state** (observed once, no current confirmation), **currently-confirmed**.
- Any rendering of previously-read state to an agent must be **visually/structurally distinguishable** from currently-confirmed state — the AoE and Civ failure modes above are exactly what happens when that distinction collapses.
- Last-known-state renderings must carry **their own last-observed timestamp** as a first-class, always-visible field — Civ's absence of any age signal on stale tiles is the anti-pattern to avoid.
- Freshness must have an explicit, named **acquisition cost** (a re-scout / re-read action), not be assumed ambient — mirroring Comsat energy and Control Ward gold.
- The system must define explicit **re-scout triggers**: conditions under which an agent is required (or strongly cued) to re-verify state before acting on it, rather than trusting an arbitrarily old last-known-state snapshot.
- Whatever marks state as "last-known" vs. "confirmed-live" must be enforced at a layer the agent cannot silently bypass or misreport — the map-hack lesson generalized: a staleness marker that can be spoofed or ignored client-side is not a staleness marker.
- The design should reserve room for a **decay/penalty signal** (per League's Vision Score staleness curve) so that trusting an increasingly old last-known-state carries a legible, scaling cost rather than a binary valid/invalid cliff.

## Sources

- Liquipedia, "Fog of War" (StarCraft II) — https://liquipedia.net/starcraft2/Fog_of_War
- StarCraft Wiki, "Fog of war" — https://starcraft.fandom.com/wiki/Fog_of_war
- Pudgy Cat, "Fog Of War In Video Games Explained" — https://pudgycat.io/fog-of-war-in-video-games-explained/
- Battle.net Classic, Warcraft II Strategy: Basic Overview — http://classic.battle.net/war2/basic/fog.shtml
- Warcraft Wiki, "Fog of War" — https://warcraft.wiki.gg/wiki/Fog_of_War
- Wikipedia, "Warcraft II: Tides of Darkness" — https://en.wikipedia.org/wiki/Warcraft_2
- Wikipedia, "Kriegsspiel" — https://en.wikipedia.org/wiki/Kriegsspiel
- Schuurman, "Models of war 1770–1830" — https://doi.org/10.1080/01916599.2017.1366928
- Kiesling, "On Fog" (Clausewitz misattribution) — https://www.clausewitz.com/bibl/Kiesling-OnFog.pdf
- IASG, "On the Fog of War — No One Gets this Quote Right" — https://www.iasg.com/blog/2017/08/15/fog-war-no-one-gets-quote-right-concept-stands
- Wikipedia, "Empire (1977 video game)" — https://en.wikipedia.org/wiki/Empire_(1977_video_game)
- Mad Ned Memo, "A Talk With Computer Gaming Pioneer Walter Bright About Empire" — https://madned.substack.com/p/a-talk-with-computer-gaming-pioneer
- Age of Empires Forums, buildings-return-invisible bug report — https://forums.ageofempires.com/t/bug-enemy-buildings-return-invisible-when-not-in-los/61807
- CivFanatics Forums, "Map Fog of War Decay Modmod" — https://forums.civfanatics.com/threads/map-fog-of-war-decay-modmod.699860/
- Bursztein, Hamburg, Lagarenne, Boneh, "OpenConflict: Preventing Real Time Map Hacks in Online Games" (IEEE S&P 2011) — https://dl.acm.org/doi/10.1109/SP.2011.28
- Esoteriic, "Enhancing Fog of War in Multiplayer Games with Cryptography" — https://esoteriic.com/enhancing-fog-of-war-in-multiplayer-games-with-cryptography/
- League of Legends Wiki, "Vision score" — https://wiki.leagueoflegends.com/en-us/Vision_score

###### [["The world is quiet here."]]
