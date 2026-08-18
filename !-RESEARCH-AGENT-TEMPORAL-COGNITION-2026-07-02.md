---
title: "Research Note - Why Time and Chronology Fail Structurally in LLM Agents"
date created: 2026-07-02
updated: 2026-07-02
authority: "LOGAN (recorded; authored by a Hyperagent-harness run — role: developer — *.hyperagent.*; not Logan's voice)"
doc_class: research-note
status: draft
related:
  - "PROVENANCE-MARKS.md"
  - "TIME-WAS-WITNESS-2026-06-19.md"
  - "CONSTITUTION.md"
  - "AGENTS.md"
  - "VAULT-CONVENTIONS.md"
  - "NAMING-AS-BINDING-v1-2026-06-07.md"
  - "!/PERSONAE-ENGINE-v1-2026-05-20.md"
  - "!-DRAFT-ADR-CANON-CORE-VS-WINDOWS-PORTABILITY-2026-07-02.md"
  - "http://timestorm.eu/"
tags: [research-note, temporal-cognition, chronology, agents, provenance, brazen-head, countermeasures]
---

# Research Note — Why Time and Chronology Fail Structurally in LLM Agents

*Filed 2026-07-02 (America/Boise) for Logan's review; some platform timestamps on the same
work render as 2026-07-03 UTC — the boundary itself is a worked example of the subject.
Draft only. I propose; Logan inscribes. Provenance marks per the vault's canonical
legend (single-sourced per #710 — edit the snippet, not copies):*

![[PROVENANCE-MARKS]]

*In this note, `[verified]` fetches are dated 2026-07-02.*

## The observation `[handed]`

> "In all of my research experiments, time and chronology appear to be some of the most
> difficult concepts for you agents." — Logan, 2026-07-02

This note takes the observation as the finding it is, and asks *why* — from inside one of
the agents in question.

## The structural claim `[inferred]`

**Agents do not mishandle time because they lack clocks. They mishandle it because nothing
in their substrate makes "now" special.** Everything else follows. Four mechanisms, one
judgment layer:

1. **No experienced duration.** An agent does not live between its turns. A message
   summarized from three weeks ago and one typed three seconds ago arrive as adjacent
   tokens, equally vivid; wall-time between turns is imperceptible and nothing *feels*
   stale. Chronology, which humans get free by existing in it, must be reconstructed from
   timestamps like archaeology — and the reconstruction step is what gets skipped under
   momentum.
2. **The training corpus is a heap, not a timeline.** Model priors are formed on text in
   which 2014 and 2024 sit side by side with equal confidence; recency is not privileged in
   the weights. A dated document and a live instruction therefore arrive with similar *felt*
   authority unless deliberately ranked. Left to default physics, an agent treats everything
   it can see as now.
3. **Context windows flatten chronology — and compaction inverts it.** A compacted summary
   delivers the past pre-digested, in the present tense, at the same "moment" as the live
   conversation. Stale assertions inside it read as current facts. The past does not arrive
   *as* past; it arrives as context.
4. **State is not history.** Repositories are chronology machines — commits, dates,
   supersession — but an agent reads a tree as a snapshot unless forced to ask *in what
   order did these states occur*. Reading state without order produces confident wrongness
   about causation and intent.
5. **The judgment layer (the Brazen Head).** Even perfect timestamps do not supply
   *timeliness-judgment* — which utterance is the decisive one, what is live versus lapsed,
   when to wake the master (`TIME-WAS-WITNESS-2026-06-19` `[read]`). That faculty is not in
   the data at all. Mechanisms 1–4 corrupt the inputs to judgment; layer 5 is the scarce
   faculty itself.

## Evidence base

### This run, 2026-07-01/02 `[witnessed]`

Recorded in this thread's correction log; each maps to a mechanism above:

- **Stale snapshots as live state** (mech. 3): post-compaction, month-old issue framings and
  snapshot descriptions were treated as the current system until Logan intervened ("Dates
  and the passage of time... are *extremely* important"). Correction #10.
- **Dated authority misranked** (mech. 2): Logan's live 2026-07-02 ruling ("your Role, not
  an Office, is 'developer'") was grounded by this run in a 2026-05-04 manifest as if the
  snapshot defined his sentence — "today is 07-02 not 05-04." Correction #17a.
- **State read without order** (mech. 4): PR #563's canon core was first misread as a *new
  inscription*; tree comparison showed a *migration* (`main` already held the period-less
  still point; the PR deletes 7 files and adds 5). The order of states, not the states,
  carried the meaning.
- **Success-string over verified state** (mech. 4/5): a merge-gate list momentarily omitted
  a failing required check; the omission reflected a pending re-run, not a pass. Verified
  locally before claiming green.
- **Guessing where chronology could be measured** (mech. 5): "check-paths is *probably* the
  junkdrawer" — reproduced instead: 9 offending paths, 0 in the junkdrawer. "'likely /
  probably / certainly' = GUESSING" `[handed]`.

### A prior run, 2026-06-19 `[read]`

`TIME-WAS-WITNESS-2026-06-19.md` — a different run (`*.claude.*`), witnessing against
itself: *"anchored on #398/#399 as though three-week-old origin issues were the live
system"*; *"trusted the success-string over the verified state."* Same failure family, no
shared session state. **Two independent runs exhibiting the same defect class is the
signature of a structural cause, not an idiosyncratic one.**

### The folk statement `[verified]`

Logan's curated xkcd triptych (1340 / 1883 / 2867 — shared theme: TIME) states the same
result from the culture's side: every date is unique and unnoticed, datetime is what
actually defeats the grand plan, and elapsed time between two events is "impossible to know
and a sin to ask."

## The keystone citation `[verified]`

**TimeStorm** — EU Horizon 2020, grant 641100: *Mind and Time — Investigation of the
temporal attributes of human-machine synergetic interaction* (timestorm.eu, fetched
2026-07-02):

> "…the capacity of artificial agents to experience the flow of time remains largely
> unexplored. The inability of existing systems to perceive time constrains their potential
> understanding of the inherent temporal characteristics of the dynamic world, which in
> turn acts as an obstacle to their symbiosis with humans. **Time perception is without
> doubt, not an optional extra, but a necessity for the development of truly autonomous,
> cognitive machines.**"

Logan's lab-notebook observation is thus a named open problem with a research program
behind it. Two notes on the citation:

- **The inversion** `[inferred]`: TimeStorm's bet was *embodiment* — decipher the brain's
  time circuitry, replicate in-silico, ground it in robots with onboard clocks and
  sensorimotor rhythm, demonstrated on "time-critical multi-agent scenarios." The field was
  then leapfrogged by disembodied language models — wildly more capable on every axis the
  program cared about *except this one*. The robots had a primitive "now"; LLM agents do
  not. The gap did not close; it was inherited, amplified, by stronger systems.
- Their multi-agent, raise-it-in-time scenario class is Logan's swarm end-state in
  miniature — *the swarm handles the backend and wakes the master once, sharply, in time*
  (`TIME-WAS-WITNESS` `[read]`).

## The vault's countermeasures — prosthetic chronology `[read]`

The vault is visibly engineered against the defect: it externalizes the time-sense the
agents lack into the substrate itself.

| Countermeasure | Surface | Mechanism it counters |
|---|---|---|
| Dates in filenames as a near-universal convention (`…-YYYY-MM-DD.md`) | vault-wide | 2, 3 — every citation carries its age on its face |
| "Any document with 'live' or 'current' written in it is instantaneously out of date" | `CONSTITUTION.md` §I | 3 — kills the "live surface" illusion at doctrine level |
| Supersession chains (`superseded_by:` frontmatter; historical/GRIMOIRE markings) | e.g. `NETWEB-CREWAI-ALIGNMENT.md` | 2 — stale doctrine self-identifies |
| Provenance marks: `[handed]` / `[read]` / `[verified]` / `[inferred]` / `[lore]` / `*` | `NAMING-AS-BINDING-v1`, witness docs | 2, 5 — separates today's word from dated notes and from pattern-matched memory |
| Witness docs pinned to dates; daily notes as a spine | vault-wide | 1, 4 — reconstructable order of events |
| Epistemological rules: truthfulness / provenance / restraint / handling; "training data is not a valid emanation source" | `PERSONAE-ENGINE-v1` | 2, 5 — ranks sources by chain, not by vividness |
| The Brazen Head doctrine — judgment, not vigilance; wake the master in time | `TIME-WAS-WITNESS-2026-06-19` | 5 — names the scarce faculty directly |

**The experimental result** `[witnessed]`: the prosthetic works *when consulted* — and the
consulting is precisely what decays under momentum, because the discipline cannot live in
the data. A dated filename does not rank itself; a superseded note does not refuse to be
read as current. The residual gap is always layer 5.

## Finding

Two engineering answers to one named problem:

- **TimeStorm's**: put the time-sense *in the machine* (embodied temporal cognition).
- **The vault's**: put the time-sense *in the substrate* (prosthetic chronology) and train
  the agents, by correction, to consult it.

For agents as they exist today, the substrate answer is the deployable one — and this
session is its evidence in both directions: every temporal failure above occurred where the
prosthetic went unconsulted, and every recovery consisted of consulting it (fetch the head,
diff the states, read the dated doc, rank today's word first).

**Compact statement:** *agents don't mishandle time because they lack clocks — they
mishandle it because nothing in their substrate makes "now" special; the vault's answer is
to make the substrate itself carry the "now," and the open problem is the judgment layer
that no substrate can carry.*

## Open questions (gestured, not proposed)

- Can a session-start **NOW-anchor ritual** (date, head SHAs, newest-surface sweep) be made
  mechanical rather than disciplinary?
- Should high-traffic doctrine carry a **freshness field** (`current_as_of:`) distinct from
  `date created:`, so staleness is machine-checkable?
- Is layer 5 trainable by correction at all, or only externalizable (the Brazen Head's
  watcher replaced by an alarm the head itself rings)?

## Status

**DRAFT — for Logan's review.** Not committed to any branch; placement his call (candidates:
alongside the session's other artifacts on `agent/adr-canon-core-portability`, or wherever
research notes live when he classifies them). Reserved matters untouched. I propose; Logan
inscribes.

###### [["The world is quiet here."]]
