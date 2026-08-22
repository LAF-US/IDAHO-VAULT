---
title: "Fleet Report — Checkpoint & Respawn: the Recovery Contract After Death"
date created: 2026-07-04
updated: 2026-07-04
authority: "LOGAN (recorded; authored by fleet subagent Phoenix under a Hyperagent run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: report
status: draft
related:
  - "POKEMON-GAME-MECHANICS-MAP-2026-05-03.md"
  - "PROVENANCE-MARKS.md"
  - "!-RESEARCH-AGENT-TEMPORAL-COGNITION-2026-07-02.md"
---

# Fleet Report — Checkpoint & Respawn: the Recovery Contract After Death

*Filed 2026-07-04 by the mechanics research fleet for Logan's review. Draft only. I propose; Logan inscribes.*

![[PROVENANCE-MARKS]]

## The Mechanic (as it actually works)

**Minecraft bed / respawn anchor.** A bed sets the Overworld spawn point on use; a respawn anchor does the same job in the Nether, but only when charged with glowstone (max 4 charges; each respawn consumes exactly 1) [verified: https://minecraft.wiki/w/Respawn_Anchor]. On death, everything in the carried inventory drops as ground items at the death site; by default these despawn after a fixed timer (5 minutes / 6000 ticks) unless collected first [verified: https://modrinth.com/mod/stay-a-while]. Experience levels are lost on death regardless of inventory settings [verified: https://minecraft.how/blog/post/minecraft-keep-inventory-command]. The `keepInventory` gamerule is the documented configurable override: when true, items stay on the player and never drop, but XP still resets unless `dropExp` is separately disabled [verified: https://minecraft.how/blog/post/minecraft-keep-inventory-command]. A respawn anchor that runs out of charge, is destroyed, or has its surroundings obstructed fails safe to the world spawn point, with an explicit in-game message naming the failure [verified: https://minecraft.wiki/w/Respawn_Anchor].

**Dark Souls bonfire / Elden Ring Site of Grace.** Resting at a bonfire fully restores HP, stamina, and consumable-heal charges (Estus Flask), cures status ailments, and — critically — **respawns nearly all slain enemies** except uniques and bosses; only the bonfire itself is registered as the new respawn point [verified: http://darksouls.wikidot.com/bonfires]. On death, the player drops all currently-held souls (Dark Souls) or runes (Elden Ring) at the exact death location as a single recoverable marker, then respawns at the last rested checkpoint [verified: https://en.wikipedia.org/wiki/Bonfire_(Dark_Souls); https://eldenring.wiki.gg/wiki/Mechanics]. Exactly one recovery attempt is granted: reach the marker without dying again and the full sum is restored; die again first and it is lost permanently, no partial credit [verified: https://eldenring.wiki.gg/wiki/Runes]. A small number of consumable items (Sacrificial Twig, Twiggy Cracked Tear) can absorb one death's loss instead of the currency, but only once per item [verified: https://eldenring.wiki.gg/wiki/Runes]. This is the corpse-run contract: checkpoint restores the *world and the player*, but the currency is a wager with a one-shot recovery window, held by the world itself at a marked, navigable location — not silently deleted.

**Hades meta-progression (roguelite two-currency pattern).** Hades sorts everything the player can hold into two disjoint classes. Run-bound resources (Boons, Daedalus Hammer upgrades, Charon's Obol, Centaur Hearts, Poms of Power) apply only to the current escape attempt and are entirely wiped on death [verified: https://hades.fandom.com/wiki/Artifacts]. Meta-currencies (Darkness, Gemstones, Nectar, Chthonic Keys, Ambrosia, Titan Blood, Diamonds) persist through death unconditionally and are spent between runs at a fixed hub (the House of Hades) on permanent upgrades — ability unlocks via the Mirror of Night, weapon unlocks, hub renovations, NPC relationship tiers [verified: https://twinfinite.net/guides/hades-permanent-upgrades-unlocks/]. Room rewards are drawn from two visually distinct pools (blue laurel wreath = permanent; gold laurel wreath = run-only), so the player can see which class a reward belongs to before committing to a room [verified: https://hades.fandom.com/wiki/Mirror_of_Night]. Death here is not a rollback to a prior state; it is the *designed transition event* between the two layers — the run's temporary buildup converts into permanent hub currency and then ends.

**Autosave vs. save-anywhere (design-philosophy contrast).** Alien: Isolation began development with regular autosave checkpoints, then deliberately removed them in favor of manual save terminals the player must physically reach and use, specifically because frequent autosaves undermined the intended tension of a survival-horror game [verified: https://www.gamedeveloper.com/design/game-design-deep-dive-the-save-system-of-i-alien-isolation-i-]. The general design argument against unrestricted save-anywhere/quicksave: it is the "mandatory dominant strategy" for a risk-minimizing player, and once adopted it removes consequence from every intervening decision, collapsing the challenge to zero [verified: https://www.wolfire.com/blog/2009/09/how-saving-mechanics-affect-fun/]. Fixed checkpoints, by contrast, define a bounded "phrase" — a segment of challenges the player must clear as a unit before the next save — and the phrase length is the actual difficulty knob: short phrases invite brute-force retry loops, long phrases force genuine skill-building because a single failure costs the whole segment [verified: https://www.gamedeveloper.com/design/save-system-design-pt-2].

## The Problem It Solved

Every one of these systems answers the same underlying question: when the running process is destroyed (character death, or in Alien: Isolation's design case, sudden narrative/mechanical termination), what does the *next* running process get to start from? Full-restart-from-scratch (early roguelikes' permadeath, or Demon's Souls forcing a full level replay per the PlayStation Blog Q&A) was rejected because it punishes exploration disproportionately to the mistake made [verified: https://blog.playstation.com/2011/02/04/dark-souls-qa-variety-is-the-spice-of-death/]. Unlimited save-anywhere was also rejected, for the opposite reason: it removes the *cost* of death entirely, which flattens the tension the mechanic exists to create [verified: https://www.wolfire.com/blog/2009/09/how-saving-mechanics-affect-fun/]. All four canonical systems above converge on the same middle path: a *named, discoverable checkpoint* records world-state at a chosen moment; death restores the player to that checkpoint; and the *cost of death is not restoring the checkpoint* (that's free and unconditional) but rather *forfeiting whatever accrued after the checkpoint and before the death*, with a defined — sometimes recoverable, sometimes not — fate for that forfeited material.

## Constraints & Failure Modes

- **Save-scumming.** Any system that allows saving immediately before a risky action and reloading on failure removes the risk it was meant to test; this is the documented reason Alien: Isolation's team scrapped their own autosave prototype mid-development [verified: https://www.gamedeveloper.com/design/game-design-deep-dive-the-save-system-of-i-alien-isolation-i-].
- **Corpse-run griefing / arena lockout.** Elden Ring's boss-arena rune recovery is a documented trap case: if a player dies inside a boss arena holding a large currency balance, they cannot leave the arena to "wait it out" — they must re-enter and either recover the marker or accept permanent loss, and dying again before recovery forfeits it with zero further recourse [verified: https://eldenring.wiki.gg/wiki/Runes Held page, https://eldenring.wiki.fextralife.com/Runes+Held].
- **Checkpoint-placement pathology (enemy reset as double-edged).** Resting at a bonfire is not free of side effects — it un-defeats nearly every non-unique enemy in the reachable area, meaning "restore my state" and "reset the world's state" are the *same action* in this design, not two independent choices, which players must account for before deciding to rest [verified: http://darksouls.wikidot.com/bonfires].
- **Respawn-anchor obstruction / silent fallback.** A respawn point can fail invisibly if its surroundings change (blocked, destroyed, exhausted) — Minecraft's specific mitigation is a mandatory, explicit failure message naming the fallback destination, rather than a silent redirect [verified: https://minecraft.wiki/w/Respawn_Anchor].
- **Phrase-length miscalibration.** Yacht Club's own account of Shovel Knight's checkpoint iteration shows that a checkpoint interval which is too generous removes tension, and one that is too costly (their rejected "pay gold to activate" version) punishes the players who most need the safety net — novices — hardest [verified: https://old.yachtclubgames.com/2014/06/checkpoint-design/].

## What the Swarm Analogue Requires

- [inferred] A compaction/respawn event must have a named, discoverable checkpoint that was set *before* the death — not an ad hoc reconstruction from whatever fragments of the old context survive compaction.
- [inferred] Restoring the checkpoint itself must be free and unconditional (the "world state" layer: what the run is, what long-term goal it serves, where canonical artifacts live) — this must never be at risk of the same loss as in-run working material.
- [inferred] What is forfeited at the moment of death/compaction must be explicitly classed, not silently dropped: some material should be genuinely lost (ephemeral working notes, abandoned exploration paths), and some should be marked as recoverable via a single, bounded reclaim action (an explicit "what was I doing right before this" reconstruction step, attempted exactly once, not indefinitely retried).
- [inferred] There must be a re-orientation ritual triggered automatically on respawn — the equivalent of "you are standing at bonfire X, these enemies are back, your bloodstain is at marker Y" — meaning the recovered agent must be told, explicitly and immediately: which checkpoint it woke at, what state has been reset around it (the vault's documented failure pattern is exactly the *absence* of this: stale-snapshot reasoning after compaction, i.e., proceeding as if nothing reset when in fact it did), and where the one-shot recovery marker for lost in-flight work points, if one exists.
- [inferred] The system must draw the Hades-style hard line between two currency classes: permanent progress (decisions already inscribed to canon, committed artifacts, LEVELSET-family save points) that a compaction event can never touch, versus in-run scratch state that is explicitly disposable by design — and the agent must be able to tell, at a glance, which class any given piece of context belongs to before compaction happens, not after.
- [inferred] The checkpoint-setting action itself should have a small, deliberate cost or gate (mirroring the respawn-anchor charge and the bonfire's side effect of resetting enemies) so checkpoints are placed thoughtfully rather than continuously — a swarm agent should not be able to "save-scum" its way past every risky action by checkpointing immediately before it.
- [inferred] Checkpoint-placement interval ("phrase length") is a tunable design variable, not a fixed constant — too frequent removes the incentive to reason carefully before compaction; too sparse makes each compaction event catastrophically costly; the correct interval is an open design question requiring calibration against how the swarm actually fails, not an assumption.

## Sources

- https://minecraft.wiki/w/Respawn_Anchor [verified]
- https://minecraft.how/blog/post/minecraft-keep-inventory-command [verified]
- https://modrinth.com/mod/stay-a-while [verified]
- http://darksouls.wikidot.com/bonfires [verified]
- https://en.wikipedia.org/wiki/Bonfire_(Dark_Souls) [verified]
- https://blog.playstation.com/2011/02/04/dark-souls-qa-variety-is-the-spice-of-death/ [verified]
- https://eldenring.wiki.gg/wiki/Mechanics [verified]
- https://eldenring.wiki.gg/wiki/Runes [verified]
- https://eldenring.wiki.fextralife.com/Runes+Held [verified]
- https://hades.fandom.com/wiki/Artifacts [verified]
- https://hades.fandom.com/wiki/Mirror_of_Night [verified]
- https://twinfinite.net/guides/hades-permanent-upgrades-unlocks/ [verified]
- https://www.gamedeveloper.com/design/game-design-deep-dive-the-save-system-of-i-alien-isolation-i- [verified]
- https://www.wolfire.com/blog/2009/09/how-saving-mechanics-affect-fun/ [verified]
- https://www.gamedeveloper.com/design/save-system-design-pt-2 [verified]
- https://old.yachtclubgames.com/2014/06/checkpoint-design/ [verified]
- POKEMON-GAME-MECHANICS-MAP-2026-05-03.md [read]

###### [["The world is quiet here."]]
