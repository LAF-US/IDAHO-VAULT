---
title: "Report - Cross-Framing the Tool-Lane Draft Family"
date created: 2026-04-17
authority: codex
doc_class: report
status: active
related:
  - "!/DRAFT-PROPOSAL-TOOL-USECASE-INTERSECTION-ANALYSIS-2026-04-17.md"
  - "!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-2026-04-17.md"
  - "!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-V2-2026-04-17.md"
  - "!/AGENTS.md"
  - "IDAHO-VAULT"
---

# Report - Cross-Framing the Tool-Lane Draft Family

## Documents Compared

- `!/DRAFT-PROPOSAL-TOOL-USECASE-INTERSECTION-ANALYSIS-2026-04-17.md`
- `!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-2026-04-17.md`
- `!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-V2-2026-04-17.md`

## Prior Dev Feedback, Reduced To Its Functional Spine

The dev team gave two rounds of useful correction.

First, on the original proposal:

- split the overloaded `authority axis` into two axes
- add a clearer decision rule
- test the framework against one real operator loop instead of a tasteful
  taxonomy

Second, on the first map:

- keep row values inside closed vocabularies
- stop naming multiple preferred lanes
- make one lane the driver and the others supporting

That feedback was coherent and cumulative. It did not overturn the direction.
It progressively forced the drafts from concept note toward decision
instrument.

## Comparative Read

### 1. The first draft is the problem frame

The first draft is still the best statement of why this analysis exists at all.

Its job is:

- define the problem
- name the analysis axes
- say what outputs are wanted
- establish that tool overlap is a standing problem, not just a clutter problem

It is not a usable routing instrument. It is a framing note.

### 2. The first map is the transition artifact

The first map is important even though it is no longer the best one.

Its job is:

- prove that the proposal can collapse into one concrete loop
- prove that `use case x lane` mapping produces real conclusions
- surface the exact places where ambiguity still remained

It is the bridge document between analysis concept and usable map.

### 3. The v2 map is the first operational shape

The v2 map is materially the strongest artifact of the three.

Its job is:

- use closed vocabularies
- separate driver from support
- constrain improvisation
- provide a reusable template for the next loop

It is the first one that can plausibly govern agent behavior instead of merely
advising it.

## Possible Cross-Framing

The three documents do not need to compete. They can be cross-framed as a
three-layer family.

### Frame A: Charter -> Prototype -> Template

This is the cleanest cross-framing.

- first draft = `charter`
- first map = `prototype`
- v2 map = `template`

This is probably the strongest interpretation because it preserves the
developmental logic instead of pretending the earlier drafts were mistakes.

### Frame B: Why -> Trial -> How

This is the most readable framing for humans.

- first draft = `why this analysis is needed`
- first map = `trial run on one live loop`
- v2 map = `how to map future loops`

This is useful if Logan wants to keep all three and make the family legible
quickly.

### Frame C: Doctrine-adjacent -> Draft instrument -> Reusable instrument

This is the most governance-friendly framing.

- first draft = `doctrine-adjacent rationale`
- first map = `draft instrument`
- v2 map = `reusable instrument`

This is a good framing if the concern is which note should remain explanatory
and which note should be treated as the seed of an actual operating method.

## Recommended Cross-Framing For The Vault

The best vault-specific framing is:

- first draft as the problem charter
- first map as the worked pilot
- v2 map as the canonical draft template

That gives each note a non-overlapping office.

It also means:

- the first draft should not be judged by whether it routes steps cleanly
- the first map should be preserved as the transitional pilot that exposed
  ambiguity
- the v2 map should be the one copied forward for additional loops

## What To Do With Each Document

### Keep

- first draft
  Reason: it still contains the broad problem statement and output model more
  explicitly than the maps do.
- v2 map
  Reason: this is the best foundation for actual repeated use.

### Keep, but demote in standing

- first map
  Reason: it is historically useful as the pilot and records the exact
  ambiguity the dev feedback corrected, but it should not be treated as the
  preferred reusable shape anymore.

That means the first map should be framed as:

- pilot
- trial
- transitional draft
- superseded by v2 for actual reuse

Not deleted, because it records the evolution of the instrument.

## What The Three Together Reveal

Taken together, the documents are already teaching a stable method:

1. state the standing problem clearly
2. narrow to one real loop
3. define closed vocabularies
4. assign one driver lane
5. let support lanes remain visible but secondary
6. widen one loop at a time

That is a legitimate house method now. Not doctrine yet, but more than random
drafting.

## Best Next Move

The next material gain is not another prose note about the method.

It is one more v2-style loop map.

Best candidates:

- source-note refinement
- companion-note writing
- GitHub review response
- inbox triage

Once there are two or three v2 maps, the first draft can be rewritten later
into a short overview that points at the family, instead of carrying so much
explanatory weight by itself.

## Bottom Line

The three documents are not three competing proposals.

They are three stages of one maturing instrument:

- the first names the problem
- the second proves the shape
- the third becomes the usable template

That is the most defensible cross-framing.
