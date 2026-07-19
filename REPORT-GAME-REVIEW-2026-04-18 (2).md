---
title: "Report - Game Review"
date created: 2026-04-18
authority: codex
doc_class: report
status: active
related:
  - "!/DEV-DESIGN-REPORT-CIVIC-FANTASY-SCAFFOLD-2026-04-17.md"
  - "!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md"
  - "!/HUB-WORLD-ROUTE-MAP-2026-04-17.md"
  - "!/CIVIC-LAW-AND-VAULTED-SYNTAX-2026-04-17.md"
  - "src/idaho_vault/civic_scaffold.py"
  - "src/idaho_vault/operator_context.py"
  - "src/idaho_vault/five_wizards/threshold_runner.py"
  - "src/idaho_vault/main.py"
  - "pyproject.toml"
  - "tests/test_civic_scaffold.py"
  - "tests/test_threshold_runner.py"
---

# Report - Game Review

## Scope

This is a game-design and playability review of the current `IDAHO-VAULT`
scaffold.

The standard here is not "is the lore interesting?"
The standard is:

- does the player have a real front door
- does the world respond to conduct
- do routes produce distinct actions and consequences
- does the current machine play, or only describe play

## Findings

### Finding 1

`[P1]` The hub-world scaffold is not currently reachable through a truthful live
front door.

`src/idaho_vault/civic_scaffold.py` already contains the closest thing the repo
has to a game map: districts, readiness, common loop, rank, and return logic.
But the package scripts exposed in `pyproject.toml` only surface bootstrap,
training/replay stubs, tests, trigger handling, and the threshold slice. There
is no operator-facing command that actually enters or renders the civic scaffold
for a player or designer. As a result, the core game frame exists in code but
not in the live command surface. From a game review perspective, that means the
hub exists as backstage structure rather than as a playable front door.

Primary surfaces:

- `src/idaho_vault/civic_scaffold.py:103`
- `src/idaho_vault/main.py:86`
- `pyproject.toml:12`

### Finding 2

`[P1]` The standing engine is still descriptive rather than operative.

The design packet correctly says the world should run on standing rather than a
generic morality meter, and it defines multiple standing axes, failure states,
and ranks. The executable scaffold does not implement that model. In code,
`StandingRank` only has `novice` and `witness`, and the current rank is derived
entirely from whether the operator front door resolves, not from conduct,
repair, restraint, provenance, or jurisdiction. That means consequence is still
repo-health based rather than behavior based. As a game, the world cannot yet
reward truthful handling or punish counterfeit authority procedurally, because
those transitions are not encoded.

Primary surfaces:

- `!/STANDING-ENGINE-AND-LAWFUL-ENDINGS-2026-04-17.md:35`
- `src/idaho_vault/civic_scaffold.py:25`
- `src/idaho_vault/civic_scaffold.py:287`
- `tests/test_civic_scaffold.py:71`

### Finding 3

`[P1]` The threshold slice is a staging proof, not yet a gameable trial.

The current threshold runner is honest about startup and staging, but almost all
of the content it produces is fixed text authored by `_lane_spec()`. Each lane
claim, note, warning, and summary is prewritten and then staged once the boot
chain, front door, and evidence references pass validation. That makes the
slice useful as a contract demonstration, but not yet as a game system. There
is no meaningful player choice, no route divergence, no changing world state,
and no uncertainty beyond file/surface validity. In game terms, the current
trial is mostly a deterministic recital of lawful posture, not a responsive
encounter.

Primary surfaces:

- `src/idaho_vault/five_wizards/threshold_runner.py:89`
- `src/idaho_vault/five_wizards/threshold_runner.py:203`
- `src/idaho_vault/five_wizards/threshold_runner.py:347`
- `tests/test_threshold_runner.py:43`

### Finding 4

`[P2]` The district map currently overstates breadth relative to implemented
interaction.

The civic scaffold lists a credible hub-world with Root Awakening, Orientation
Hall, Forge, Docket, Post Room, Scribe's Chamber, and Machinery Floor. But two
districts are explicitly only `declared`, and the scaffolded districts
themselves mostly expose surface summaries rather than action sets. The Docket
and Post Room are especially important because they imply live external traffic
and procedural consequence, yet the scaffold currently represents them as named
places with notes saying they are not locally executable. That is honest in one
sense, but as a game review finding it still means the map is ahead of the
verbs. The player can see the city plan before the streets are walkable.

Primary surfaces:

- `src/idaho_vault/civic_scaffold.py:32`
- `src/idaho_vault/civic_scaffold.py:188`
- `src/idaho_vault/civic_scaffold.py:236`
- `tests/test_civic_scaffold.py:89`

## Current Read

The project already has a strong genre identity.

It does *not* yet have a fully playable game loop.

What it has is:

- a strong constitutional and symbolic design language
- a truthful startup and routing philosophy
- a thin but real executable scaffold
- one deterministic threshold slice

That is enough to prove the design direction.
It is not yet enough to say the game properly plays.

## Best Read Of The Current Build

Right now the project is closest to:

- a playable design packet
- a scaffolded hub-world map
- a set of lawful operator rituals
- the first slices of a consequence machine

It is not yet:

- a robust standing simulator
- a route-divergent encounter game
- a system where district travel reliably changes future admissibility

## Next Material Gains

### 1. Expose the civic scaffold through one truthful player-facing command

The first game-review fix should be a real front door to the map that already
exists in code.

### 2. Encode standing transitions as state, not prose

The next game-critical machine is not wider lore.
It is rank movement, restriction, dormancy, and local admissibility driven by
conduct.

### 3. Give one district a real action grammar

The threshold slice should evolve from "lawful staging recital" into one
district with:

- an input
- a trial
- possible failure
- return
- changed standing or state

### 4. Keep declared districts out of the player's implied verb-space until they
can answer actions truthfully

A district can remain named while still clearly marked as not yet enterable.
What the current build should avoid is making the map feel broader than the
verbs really are.

## Bottom Line

As a game, `IDAHO-VAULT` is not vapour.
It has a real design center and the beginning of a machine.

But the current build still plays more like a truthful constitutional prototype
than like a fully responsive world.

The strongest next step is not more mythology.
It is one playable loop where standing changes because of what the player did.
