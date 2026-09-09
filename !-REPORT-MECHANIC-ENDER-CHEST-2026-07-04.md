---
title: "Fleet Report — The Ender Chest: Identity-Bound Storage That Follows the Agent"
date created: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Pearl under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
---

# Fleet Report — The Ender Chest: Identity-Bound Storage That Follows the Agent

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

## The Mechanic (as it actually works)

An ender chest is a placeable block with 27 inventory slots — a single 3×9 grid, the same capacity as a basic chest [verified: https://minecraft.wiki/w/Ender_Chest]. Its contents are not stored in the block. They are stored in the owning player's own save data (`EnderItems` in Java Edition, `EnderChestInventory` in Bedrock) [verified: https://minecraft.wiki/w/Ender_Chest]. The block itself is only an access point — the Wiki's own phrase is a "portal" to those 27 slots [verified: https://minecraft.wiki/w/Ender_Chest].

Because storage is player-bound rather than block-bound, the same physical chest shows different contents to different players who open it — that is the identity binding named in the vault's source map. Every ender chest in the world, including any placed in a different dimension, opens onto the same player-specific inventory: place one, fill it, then open a different ender chest anywhere else (Overworld, Nether, or the End) and the same 27 slots are there [verified: https://minecraft.wiki/w/Ender_Chest]. Two ender chests placed side by side do not merge into a double chest the way two regular chests do — there is no combined-capacity variant [verified: https://minecraft.wiki/w/Ender_Chest].

Crafting cost is deliberately steep: 8 obsidian (mined with a diamond or netherite pickaxe) surrounding one eye of ender (crafted from blaze powder + an ender pearl, itself an Enderman drop) [verified: https://minecraft.wiki/w/Ender_Update]. This is markedly more expensive than a basic chest (8 wood planks), which is the game's way of pricing the privilege of dimension-spanning personal storage.

The sanctioned way to exceed the 27-slot ceiling is nesting: shulker boxes (27-slot containers in their own right) can be placed inside an ender chest's slots. Up to 27 filled shulker boxes fit inside one ender chest, yielding an effective 729 slots (27 × 27) [verified: https://minecraft.wiki/w/Ender_Chest]. This is the only sanctioned capacity expansion — there is no other multiplier or upgrade path.

## The Problem It Solved

Regular chests are block-bound and location-bound: lose the chest, lose the contents; die far from your base, and your carried inventory scatters as drops at your death location. Prior to the per-player split (Java snapshot 12w24a), ender chests were even *world-shared* — one inventory for every player on a server, which defeated the purpose of "secure personal storage" the community had asked for [verified: https://minecraft.wiki/w/Ender_Chest]. The per-player redesign fixed this: it gave each player one pocket of storage that is theirs alone, reachable from anywhere, safe from both location loss and death loss — which is exactly why the source map filed it as "Identity-bound personal context that follows the agent across sessions" [read: POKEMON-GAME-MECHANICS-MAP-2026-05-03.md].

## Constraints & Failure Modes

- **Fixed ceiling.** 27 slots is 27 slots. There is no direct upgrade; only shulker-box nesting multiplies effective capacity, and even that tops out at 729 slots [verified: https://minecraft.wiki/w/Ender_Chest].
- **Block destruction ≠ data loss.** Breaking an ender chest does not drop its contents — they persist in the player's save data regardless of the block's fate [verified: https://minecraft.wiki/w/Ender_Chest]. Reclaiming the *block itself* requires Silk Touch; without it, the chest drops only 8 obsidian, and a new ender chest must be crafted to regain a physical access point (the contents were never at risk) [verified: https://minecraft.wiki/w/Ender_Chest].
- **Not dragon-proof.** Despite being made of obsidian, an ender chest block is not immune to the ender dragon and can be destroyed by it — access-point loss is real even if data loss is not [verified: https://minecraft.wiki/w/Ender_Chest].
- **Death-survival is the point, not an edge case.** Ender chest contents explicitly survive player death, unlike the carried inventory, which drops on the ground and can despawn or be looted [verified: https://minecraft.wiki/w/Ender_Chest].
- **Strictly personal — no joint access.** There is no shared or multi-player mode. Other players cannot see or take items from your ender chest; contrast with a regular chest, which any player can open and both see and take from [verified: https://minecraft.wiki/w/Ender_Chest].
- **Tombstone — the Nether Chest.** The source map records a rejected term: "Nether Chest | Non-canonical error term | Explicitly rejected in the canonical study; the real mechanic is the Ender Chest" [read: POKEMON-GAME-MECHANICS-MAP-2026-05-03.md]. No such block exists in Minecraft; the vault's own working notes once misnamed the mechanic before correcting to Ender Chest. This report preserves the tombstone per instruction — the error is part of the record, not scrubbed from it.

## What the Swarm Analogue Requires

- [inferred] A personal storage layer keyed to agent identity, not to machine or session — contents must resolve to the *same* agent regardless of which host process opens the store, mirroring per-player (not per-block) resolution.
- [inferred] Access from any execution context (any "dimension" the agent runs in — different hosts, sandboxes, or invocation types) must resolve to one identity-bound store, not a per-location copy.
- [inferred] Store contents must survive both (a) destruction of the local access point (a wiped dotfolder, a rebuilt sandbox) and (b) termination of the running session ("death") — persistence must be decoupled from any single ephemeral runtime.
- [inferred] A deliberate, non-trivial cost or gate on establishing a new access point is acceptable and may be desirable, to discourage casual proliferation of untracked local copies.
- [inferred] A fixed, bounded slot count at the base layer, with nesting (sub-containers packed inside the identity store) as the only sanctioned expansion mechanism — not unbounded ad hoc growth.
- [inferred] No joint or shared access mode at this layer: one agent's identity-bound store must not be readable or writable by another agent's process, by design, not by convention.
- [inferred] Recovering a lost local access point (re-creating the dotfolder) must not require recovering lost data — the two are independent failure domains, exactly as block loss and inventory loss are independent in the source mechanic.

## Sources

- https://minecraft.wiki/w/Ender_Chest [verified]
- https://minecraft.wiki/w/Ender_Update [verified]
- https://minecraft.wiki/w/Slot [verified]
- POKEMON-GAME-MECHANICS-MAP-2026-05-03.md [read]

###### [["The world is quiet here."]]
