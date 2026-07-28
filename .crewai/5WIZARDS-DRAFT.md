---
title: "5Wizards - CrewAI Draft Architecture"
date created: "2026-04-15"
date updated: "2026-04-15"
authority: crewai
doc_class: architecture
status: draft
phase: concept-refinement
related:
  - ".crewai/MANIFEST.md"
  - ".crewai/TRAINING.md"
  - "!/CREWAI/README.md"
  - "!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md"
---

# 5Wizards

This document turns Logan's described idea into an implementation-oriented
CrewAI draft.

It is not live topology.

The current live CrewAI truth remains `.crewai/MANIFEST.md`.
Nothing in this document becomes operational until Logan approves it and the
relevant crews, tasks, and runners are registered on purpose.

---

## Why This Exists

The earlier generalist summary captured the ambition of the idea, but it
flattened several different things into one layer:

- metaphorical naming
- governance intent
- implementation detail
- live topology

This draft separates those layers so a coder can actually build the system
without pretending that concept art is already code.

---

## Control-Plane Constraints

Any implementation of the 5Wizards framework must remain true to the current
vault control plane:

- The vault is the durable record.
- GitHub remains execution and transport.
- Linear remains execution state.
- Slack remains breadcrumb-only.
- CrewAI is an orchestration layer, not a new sovereign source of truth.
- Durable CrewAI outputs stage to `!/CREWAI/` before any promotion.
- Promotion into canon remains Logan-gated.

This system must dock into the vault. It must not replace the vault.

---

## Naming Rule

This framework should be called `5Wizards`.

The name comes from Logan's use of the journalistic 5W frame, which in this
system includes `HOW` as part of the full inquiry set:

- `WHO`
- `WHAT`
- `WHEN`
- `WHERE`
- `WHY`
- `HOW`

That is the backbone of the architecture.

So the framework name remains `5Wizards`, but the implemented question lattice
contains six inquiry lanes.

---

## Journalistic Frame

5Wizards is a journalistic agentic tool.

It uses metaphor as a naming system and memory aid, not as entertainment and
not as a substitute for reporting discipline.

The practical meaning is:

- the `5W/H` questions define the reporting lanes
- Wizards draft and synthesize lane understanding
- Familiars challenge, verify, and force grounding
- Mirage is shorthand for unsupported reporting
- Council is shorthand for editorial cross-check and synthesis

The actual engine of the system is not lore. It is:

- source handling
- claim extraction
- evidence citation
- contradiction detection
- validation gates
- staged publication

---

## Design Intent

5Wizards is best understood as a truth-first inquiry harbor for
source material that Logan wants examined rigorously before claims are admitted
into the vault.

The design goal is disciplined journalistic claim handling:

- separate inquiry lanes by question type
- require grounded evidence
- preserve objections instead of smoothing them away
- block promotion when grounding fails
- synthesize only after domain-level review

The system should therefore be built as a multi-lane validation flow, not as a
single "smart agent."

---

## Vocabulary Mapping

Logan's metaphorical terms can be preserved, but they need stable technical
meanings.

| Metaphorical term | Technical meaning | Notes |
| --- | --- | --- |
| Wizard | Synthesis-oriented domain agent | Produces hypotheses, interpretation, and final lane resolution |
| Familiar | Named challenge-oriented companion for one lane | Tests claims, hunts contradictions, and presses for grounding |
| Mirage | Ungrounded or insufficiently evidenced claim | A failure state |
| Council | Cross-domain review stage | Aggregates resolved lane outputs and unresolved objections |
| Anchor | Domain-specific grounding requirement | Usually embodied by the lane's familiar name |

Recommended implementation rule:

- keep the metaphorical names in human-facing docs if Logan wants them
- use precise internal names in config and code

Example:

- `who_wizard` may exist as a human-readable alias
- `who_scholar` or `who_synthesist` is usually clearer in code

---

## Candidate Topology

The first serious implementation should not be a single monolith.
It should be a flow with six parallel domain lanes and one convergence layer.

### Lane model

Each inquiry domain owns one lane:

| Domain | Core question | Wizard function | Familiar | Familiar function |
| --- | --- | --- | --- | --- |
| WHO | Who is involved? | identity scholar | THOU | identity hunter |
| WHAT | What exists or happened? | content scholar | THAT | artifact hunter |
| WHEN | When did it happen? | temporal scholar | THEN | chronology hunter |
| WHERE | Where is it situated? | spatial scholar | THERE | location hunter |
| WHY | Why should the claim be believed? | meaning scholar | THY | causal hunter |
| HOW | How does it work or unfold? | process scholar | THE | procedure hunter |

The familiar names are canonical for the lane pairing.

They also function as anchor handles, but they should be implemented as
explicit validation categories rather than treated as self-justifying labels.

### Recommended execution structure

1. Intake
2. Six parallel `probe` tasks
3. Six parallel `investigate` tasks
4. Six parallel `validate` tasks
5. Six parallel `resolve` tasks
6. Governance gate
7. Council synthesis
8. Final authored output
9. Staged vault handoff

This suggests a Flow-style orchestrator or an explicit runner that manages task
dependencies, rather than a single CrewAI `Crew` with a long flat task list.

---

## Domain Pipeline

Each lane follows the same four-stage pattern, but with different evidence
types and failure tests.

### 1. Probe

Purpose:

- frame the question
- list preliminary hypotheses
- identify missing evidence
- declare what would count as grounding

Primary owner:

- synthesis role

Output:

- `probe_brief`

### 2. Investigate

Purpose:

- gather evidence
- challenge assumptions
- enumerate contradictions
- identify unsupported leaps

Primary owner:

- challenge role

Output:

- `evidence_ledger`

### 3. Validate

Purpose:

- compare hypotheses against evidence
- force explicit pass or fail decisions on atomic claims
- preserve unresolved objections

Primary owners:

- both roles

Output:

- `validation_verdict`

### 4. Resolve

Purpose:

- write the strongest grounded lane summary possible
- include surviving ambiguity instead of hiding it
- separate confirmed claims from probable claims and blocked claims

Primary owner:

- synthesis role

Output:

- `resolved_domain_brief`

---

## Recommended Artifact Contract

The architecture gets much easier to trust if every stage emits a bounded,
inspectable artifact.

| Stage | Artifact | Suggested format | Required use |
| --- | --- | --- | --- |
| Intake | source dossier | Markdown + frontmatter | Identify the source set and run scope |
| Probe | probe brief | Markdown or JSON | Record hypotheses and evidence plan |
| Investigate | evidence ledger | JSON or Markdown table | Capture cited evidence and counter-evidence |
| Validate | validation verdict | JSON | Encode pass, fail, blocked, and reasons |
| Resolve | resolved domain brief | Markdown | Human-readable lane output |
| Governance | gate report | JSON + Markdown summary | Record run-level go/no-go state |
| Council | council matrix | Markdown table or JSON | Compare lane outputs and contradictions |
| Final | synthesis note | Markdown | Staged artifact in `!/CREWAI/` |

Every durable artifact should include a `run_id` and a stable file path scheme.

---

## Atomic Claim Model

The core unit should not be "a paragraph." It should be an atomic claim.

Recommended minimum claim structure:

```json
{
  "claim_id": "who-003",
  "domain": "WHO",
  "text": "Agency X sponsored document Y.",
  "anchor_type": "Thou",
  "anchor_value": "Agency X",
  "evidence_refs": ["src-01#p3", "src-02#l18"],
  "confidence": "grounded",
  "status": "pass",
  "objections": []
}
```

Recommended validation statuses:

- `pass`
- `fail`
- `blocked`
- `disputed`

Recommended confidence labels:

- `grounded`
- `probable`
- `tentative`

No claim should be promoted as grounded without explicit evidence references.

---

## Validation Rules

The generalist assistant turned "truth enforcement" into a slogan. The
implementable version is narrower and more honest.

A claim may pass only if all of the following are true:

1. It has a domain.
2. It has an anchor type and anchor value.
3. It has at least one concrete evidence reference.
4. The challenge role has not left an unresolved fatal objection.
5. The claim does not contradict another passed claim without explanation.

Recommended verdict algorithm:

```python
def validate_claim(claim, objections):
    if not claim.anchor_value:
        return "fail", "missing_anchor"
    if not claim.evidence_refs:
        return "fail", "missing_evidence"
    if any(obj.severity == "fatal" for obj in objections):
        return "disputed", "fatal_objection"
    return "pass", "grounded_for_current_scope"
```

Important honesty rule:

This system cannot guarantee metaphysical truth.
It can only enforce evidence discipline for the run's available sources.

---

## Mirage Handling

Mirage should become a concrete run state.

Recommended Mirage categories:

- `missing-anchor`
- `missing-evidence`
- `contradictory-evidence`
- `overreach`
- `fabricated-entity`
- `fabricated-causation`
- `fabricated-process`
- `temporal-imprecision`
- `spatial-imprecision`

Recommended behavior:

- lane-level Mirage findings are recorded, not silently erased
- final synthesis is blocked from promotion when fatal Mirage findings remain
- the system emits a structured "mirage report" instead of pretending success

That means the right failure output is often not silence. It is a clear report
explaining why the run did not clear the gate.

---

## Governance Gate

The brainstorm suggested halting the entire system as soon as any lane fails.
That is emotionally satisfying but operationally weak.

Recommended policy:

- allow all started lanes to finish
- block final promoted synthesis if any lane ends in `fail` or `blocked`
- emit a run-level gate report summarizing what passed, failed, or remains disputed

This gives Logan a complete picture instead of a single early-stop error.

Recommended gate states:

- `green` - all lanes passed
- `yellow` - at least one lane is disputed but no fatal failures
- `red` - one or more lanes failed or were blocked

Only `green` runs should be eligible for a final integrated synthesis that is
framed as grounded.

---

## Council Synthesis

The Council is a structured cross-domain review pass.

Recommended Council responsibilities:

- identify contradictions across lanes
- identify duplicated evidence cited differently
- identify missing links between domains
- decide whether the six lane outputs can coexist as one coherent account
- preserve dissent notes instead of flattening disagreement

Recommended Council inputs:

- six resolved domain briefs
- six validation verdicts
- aggregated objection log
- gate report

Recommended Council outputs:

- `council_matrix`
- `cross_domain_objections`
- `synthesis_recommendation`

If the Council cannot reconcile contradictions, the run should end as a staged
failure report rather than a clean final narrative.

---

## Final Authoring

The earlier summary assigned final authorship automatically to the WHY lane.
That may or may not be right.

Recommendation for v1:

- do not hard-code WHY as the sovereign narrator yet
- use a dedicated synthesis step fed by the Council outputs
- allow Logan to decide later whether the WHY scholar should own that final pass

That keeps the architecture flexible while the inquiry model matures.

---

## CrewAI Mapping

If this system is built in CrewAI, the likely mapping looks like this:

| Design concern | CrewAI implementation candidate |
| --- | --- |
| Run orchestration | Flow or custom runner |
| Domain roles | Agents |
| Stage progression | Tasks or flow nodes |
| Evidence collection | Tools + structured artifacts |
| Validation | Python validators + task outputs |
| Governance gate | Python gate step |
| Council | Aggregation task or flow stage |
| Staged output | Markdown writer into `!/CREWAI/` |

Recommended implementation posture:

- keep core validation in Python, not only in prompt text
- use prompts to reason
- use code to enforce contracts

This matters because "no hallucinations" is not a prompt. It is a combination
of task design, artifact structure, and coded validation gates.

---

## Recommended Delivery Phases

### Phase 0 - Vocabulary and schema

Build:

- claim schema
- verdict schema
- gate states
- Mirage taxonomy

Do not build all 12 roles yet.

### Phase 1 - Single-lane pilot

Build one lane end-to-end first.

Recommended pilot lane:

- `WHAT`

Reason:

- artifact grounding is usually easier to verify than causation or intent

### Phase 2 - Multi-lane expansion

Add the remaining lanes once the artifact contract is stable.

### Phase 3 - Council layer

Add cross-domain synthesis and contradiction handling only after the lane
outputs are reliable.

### Phase 4 - Presentation polish

Layer in the richer human-facing Wizard/Familiar presentation only after the
underlying execution model is trustworthy.

The wrong order is branding first, contracts later.

---

## Non-Goals

This draft does not authorize any of the following:

- updating `.crewai/MANIFEST.md` as if this topology were live
- treating metaphorical language as executable truth
- replacing `swarm.json` with CrewAI internals
- bypassing GitHub or Linear coordination
- allowing CrewAI to write directly into canon without staging
- making unverifiable claims sound final

---

## Open Decisions Logan Still Owns

These are real design decisions, not implementation trivia:

1. Should the final narrator be a dedicated synthesis role or the WHY lane?
2. Should disputed runs emit a partial synthesis or only a Mirage report?
3. Should lane outputs be JSON-first, Markdown-first, or dual-format?
4. Which source classes are allowed in scope for a run?
5. Does every domain truly need a paired challenge role in v1?
6. Which first real-world use case should pilot this architecture?

Until those decisions are made, this remains a buildable draft rather than live
CrewAI doctrine.

---

## Implementation Recommendation

If Logan wants this pursued, the next coding step should be modest and real:

1. create explicit schemas for claims, verdicts, and run gates
2. implement one domain lane end-to-end
3. write staged outputs to `!/CREWAI/`
4. evaluate the pilot before multiplying agents

That path preserves Logan's 5Wizards idea without letting the architecture
outrun the evidence.

---

###### The world is quiet here.
