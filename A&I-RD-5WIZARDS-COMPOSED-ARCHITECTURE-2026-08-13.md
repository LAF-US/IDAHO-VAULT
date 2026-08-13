---
title: "A&I R&D — 5Wizards as a Composed Inquiry Architecture"
date: 2026-08-13
author: Manus AI
authority: pending Logan review
from: Manus AI
to: Vault Architecture & Infrastructure ; Research & Development
doc_class: research-and-development-note
status: draft
subject: Reassessment of 5Wizards as a bounded inquiry chamber composed from CrewAI, LangGraph, AutoGen, deterministic validators, and vault-native records
related:
  - .crewai/5WIZARDS-DRAFT.md
  - .crewai/MANIFEST.md
  - !/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md
  - !/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-V2-2026-04-17.md
  - 2026-agentic-AI-landscape-general-theory-2026-05-19.md
  - INBOX/THE-MUSIC-BOX-MODEL-2026-05-30.md
  - CONSTITUTION.md
tags: [A&I, R&D, 5Wizards, CrewAI, LangGraph, AutoGen, inquiry, governance, architecture]
---

# A&I R&D — 5Wizards as a Composed Inquiry Architecture
## 2026-08-13 | Draft for Architect Review

> **Status statement:** This is an R&D synthesis, not a topology declaration. It does not alter `.crewai/MANIFEST.md`, register a crew, grant a role, authorize a runtime, or promote any artifact. It records a design interpretation for review.

## 1. Question under review

The question is not whether **CrewAI**, **LangGraph**, or **AutoGen** should replace one another. The question is whether the `5Wizards` concept becomes stronger when each framework has a bounded, inspectable responsibility inside one lawful inquiry system.

The proposed answer is **yes**. The core unit is not a permanent agent government or a six-question checklist. It is a **bounded inquiry run**: an externally opened review of a named source set that returns a structured account of what is established, probable, disputed, missing, or out of scope.

The House remains the durable context. A run is an event within the House. It does not create a new authority centre merely because it contains multiple agents, a council, or a conversation.

## 2. Evidence posture and date discipline

This note relies on several materials with distinct dates, authorities, and statuses. They should not be flattened into one undifferentiated specification.

| Source | Date / status stated by source | What it contributes | What it does **not** establish |
|---|---|---|---|
| `.crewai/MANIFEST.md` | Created 2026-04-04; updated 2026-08-13; `status: retired` | The record of the CrewAI dependency-removal decision: no CrewAI runtime, crew, or runner remains registered. | That the six-question concept, Familiar roles, LangGraph, AutoGen, or human-feedback training has been rejected as future design work. |
| `.crewai/5WIZARDS-DRAFT.md` | 2026-04-15; `status: draft`; `phase: concept-refinement` | The most detailed 5Wizards design: six inquiry lanes, paired Wizard/Familiar roles, atomic claims, validation gates, a Council, and staged outputs. | Live topology, registered agents, or an approved implementation plan. |
| `!/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md` | 2026-04-16; recommendation note | A caution that CrewAI should be an adapter around a proven core, not the sole location of system truth; it names LangGraph as a possible later graph-runtime fit. | A requirement that no additional framework can ever be used. |
| `!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-V2-2026-04-17.md` | 2026-04-17; draft map | A narrow routing rule: one driver lane per individual step, chosen for live status, reviewability, low hidden state, and lack of duplicate authority. | A rule that the entire House must use only one framework. |
| `2026-agentic-AI-landscape-general-theory-2026-05-19.md` | 2026-05-19; theory documentation; non-prescriptive | A concise framework distinction: CrewAI for role-based teams, LangGraph for stateful graphs, AutoGen for layered conversations and rapid iteration. | A vault-specific production topology. |
| `INBOX/THE-MUSIC-BOX-MODEL-2026-05-30.md` | 2026-05-30; explicitly offered as a lens rather than canon | A model of external authorization, pinned scope, governor restraint, finite execution, and silence between runs. | A complete framework or implementation specification. |

The direct instruction of the Architect remains controlling. Where these sources conflict or leave an issue undecided, this note records the tension rather than resolving it by assertion.

## 3. Restated design thesis

`5Wizards` should be a **truth-first, multi-lane inquiry chamber**. It is designed to handle a source packet—documents, repository files, transcripts, code, or other named materials—under a bounded mandate.

The six inquiry lanes are the journalistic questions:

| Lane | Question | Wizard function | Familiar function | Primary product |
|---|---|---|---|---|
| `WHO` | Who is involved? | Synthesizes identities, roles, standing, and relationships. | Tests identity claims, aliases, attribution, and standing assumptions. | Identity ledger. |
| `WHAT` | What exists or happened? | Synthesizes events, artifacts, changes, and assertions. | Tests existence, artifact integrity, and claim boundaries. | Artifact/event ledger. |
| `WHEN` | When did it occur? | Synthesizes chronology and sequence. | Tests timestamps, version order, recency, and temporal precision. | Timeline. |
| `WHERE` | Where is it situated? | Synthesizes location, jurisdiction, path, or system placement. | Tests scope, path, environment, and location ambiguity. | Location/jurisdiction map. |
| `WHY` | Why should a claim be believed or matter? | Synthesizes stated rationale and evidence-based significance. | Tests causal overreach, unsupported motive, and interpretive leaps. | Rationale ledger. |
| `HOW` | How does it work or unfold? | Synthesizes mechanisms, procedures, and transitions. | Tests reproducibility, omitted steps, and mechanism claims. | Process model. |

The Wizard and Familiar are not merely role-playing wrappers around the same prompt. Their jobs should create useful tension: **propose versus challenge**, **resolve versus preserve dissent**, and **synthesize versus test grounding**.

## 4. Composed architecture

The frameworks are compatible because they answer different architectural questions.

| Layer / instrument | Proposed responsibility | Bounded interface | Must not become |
|---|---|---|---|
| **Vault record** | Holds source dossiers, run charters, cited evidence, reports, decisions, and durable artifacts. | File paths, commit identifiers, source hashes, and explicit frontmatter. | A background agent memory that alters itself without review. |
| **LangGraph** | Holds the run’s explicit state, parallelism, conditional transitions, human pauses, revision caps, and resumability. | Typed `InquiryRunState` and named transitions. | A constitutional authority, self-scheduler, or automatic promoter. |
| **CrewAI** | Instantiates the role-and-task composition of a specific run: Wizards, Familiars, research tasks, tool permissions, and bounded synthesis assignments. | Agents, tasks, crews/flows, structured task output. | The only definition of the 5Wizards system or an unbounded manager. |
| **AutoGen** | Supplies optional, bounded conversational hearings where dialogue itself is evidence-producing: cross-examination, challenge, clarification, or negotiated wording. | A fixed participant set, purpose, turn budget, and transcript artifact. | An unbounded group chat that determines state by consensus or persistence. |
| **Deterministic Python** | Enforces schemas, provenance checks, citation presence, state transitions, budget limits, and serialization. | Validators operating on structured artifacts. | A faux-agent system that substitutes pre-written answers for inquiry. |
| **Human review** | Opens the run, defines or approves its scope, answers blocked questions, and decides whether a staged result has further standing. | Signed or recorded run charter and explicit review decision. | A post-hoc ritual after agents have already self-authorized. |

## 5. The run state is the principal control surface

The important design object is a typed, inspectable `InquiryRunState`, not a prompt transcript and not a manager agent’s private memory.

```text
InquiryRunState
├── run_id
├── charter
│   ├── question
│   ├── authorized_source_set
│   ├── permitted_tools
│   ├── output_scope
│   └── authority_reference
├── lane_packets[WHO|WHAT|WHEN|WHERE|WHY|HOW]
│   ├── probe_brief
│   ├── claim_ledger
│   ├── evidence_ledger
│   ├── objections
│   ├── resolution
│   └── lane_status
├── council_packet
│   ├── cross_lane_conflicts
│   ├── unresolved_questions
│   └── synthesis_recommendation
├── governor
│   ├── turn_budget
│   ├── tool_budget
│   ├── revision_budget
│   └── stop_reason
└── disposition
    ├── staged
    ├── incomplete
    ├── blocked
    └── reviewed
```

The state makes it possible to determine what happened without accepting any agent’s summary of its own behavior as sufficient evidence.

## 6. Proposed run lifecycle

```text
1. WIND / OPEN
   Human creates a charter: question, source set, tools, and output boundary.

2. FRAME
   LangGraph initializes a finite run state.
   CrewAI assigns the applicable Wizard/Familiar roles.

3. PROBE
   Each active lane states what it is trying to establish and what evidence would count.

4. INVESTIGATE
   Wizard and Familiar produce claims, evidence references, and objections.

5. HEARING — OPTIONAL
   AutoGen-style dialogue is invoked only for a named dispute that benefits from
   attributable exchange. It is capped, recorded, and cannot promote itself.

6. VALIDATE
   Deterministic validators check atomic-claim structure, evidence references,
   fatal objections, contradictions, and run budgets.

7. COUNCIL
   LangGraph collects the lane packets. A synthesis task may identify cross-lane
   contradictions, shared evidence, or missing links. It does not erase dissent.

8. DISPOSITION
   The run ends as a staged grounded account, a qualified/disputed account, or
   an incomplete/blocking report. Human review decides any later use.
```

This is a sequence of **bounded state changes**, not a self-perpetuating workflow. The music-box lens is useful here: a run is externally opened, plays only its authorized tune, is governed by explicit brakes, and ends honestly when its budget or scope is exhausted.

## 7. Validation and the place of conversation

Every candidate claim should be atomic enough to validate independently.

```json
{
  "claim_id": "when-004",
  "lane": "WHEN",
  "text": "The configuration was changed after the initial report.",
  "evidence_refs": ["path/to/file.md#L20-L31", "commit:abc123"],
  "source_scope": "authorized",
  "confidence": "probable",
  "status": "disputed",
  "objections": ["timestamp source and commit chronology disagree"]
}
```

A claim should not qualify as grounded merely because a Wizard wrote it eloquently or a Familiar agreed. At minimum, it needs a lane, a concrete evidence reference, a scope-valid source, and no unresolved fatal objection. The system can enforce **evidence discipline for an identified corpus**; it cannot guarantee metaphysical truth.

AutoGen-style conversation is therefore optional and specific. It belongs where structured ledgers reveal a genuine conflict that needs direct exchange. It is not the default execution substrate for all six lanes.

## 8. Council without self-sovereignty

The Council should not be an agent legislature that votes itself authority. Its proper technical function is cross-domain editorial review:

- identify contradictions between lane packets;
- identify where one claim has been treated as different evidence by different lanes;
- identify missing causal, temporal, identity, or procedural links;
- preserve dissent and unresolved objections;
- recommend a disposition for the run.

The Council may produce a `council_matrix` and a `synthesis_recommendation`. It should not autonomously declare output canonical, broaden the source scope, schedule its own next run, or appoint agents to new offices.

## 9. Smallest credible pilot

The first credible prototype should prove a real inquiry mechanic without simulating a full pantheon.

| Element | Pilot constraint |
|---|---|
| Scope | One human-authorized source dossier and one concrete question. |
| Roles | One Wizard/Familiar pair, beginning with `WHAT` unless the docket makes another lane more appropriate. |
| Orchestration | A short LangGraph path with a finite revision cap. |
| Dialogue | At most one bounded hearing, only if a defined objection requires it. |
| Artifacts | Charter, claim ledger, evidence ledger, objections, resolution, and disposition. |
| Outcome | A grounded finding, qualified finding, or explicit non-finding—never a fabricated clean answer. |
| Promotion | No automatic promotion; output remains staged pending human review. |

The correct success criterion is not “all agents spoke.” It is that an outside reviewer can inspect the packet and understand **what was asked, what sources were allowed, what claims were made, what evidence supports them, what was challenged, and why the run stopped where it did**.

## 10. Decisions that remain open

The following are design decisions for Logan rather than assumptions for an implementation:

1. Is the Council always a complete six-lane body, or can a docket convene only the offices materially implicated?
2. In which situations should a Familiar be an independent model/agent, a deterministic critique routine, or a human seat?
3. What real docket should test the first pilot: vault archaeology, source reporting, repository change review, or another identified use case?
4. What source classes are eligible for a run, and how are external sources admitted?
5. When do disputed runs produce a partial account, and when should they return only an unresolved-question or Mirage report?
6. Should a dedicated synthesis office exist, or should final voice vary by docket and be decided only after evidence practice is stable?
7. Which artifacts belong in a staging location versus the repository root under the current placement rule?

## 11. Non-claims

This note does **not** claim that:

- any CrewAI 5Wizards topology is currently registered or runnable;
- current Python code accurately implements Familiar roles, LangGraph state, AutoGen hearings, or all deterministic validation described here;
- LangGraph or AutoGen is installed, configured, approved, or required;
- metaphorical offices alone create permissions;
- the Council has authority to promote, legislate, appoint, or continue itself;
- the House / Keys framework is exhausted by this technical mapping.

## 12. Bottom line

The strongest 5Wizards design is a composed system with one clear purpose: **bounded, inspectable inquiry**.

- CrewAI can provide role-and-task composition.
- LangGraph can provide explicit state and controlled transitions.
- AutoGen can provide a bounded hearing when dialogue is genuinely useful.
- Deterministic code can enforce artifact contracts and stopping conditions.
- The vault can preserve the record.
- Human review can retain the decision to open, interpret, and promote work.

That division permits rich, MUD/MUSH-like social and narrative expression without confusing conversation for authorization, persistence for standing, or a runtime for the House itself.

---

### Source references

1. `.crewai/MANIFEST.md` — created 2026-04-04; updated 2026-08-13; `status: active`.
2. `.crewai/5WIZARDS-DRAFT.md` — created/updated 2026-04-15; `status: draft`; `phase: concept-refinement`.
3. `!/SENIOR-GAME-DEV-NOTE-CONNECTOR-POSTURE-2026-04-16.md` — 2026-04-16.
4. `!/DRAFT-MAP-TOOL-LANES-FOR-ONE-LIVE-LOOP-V2-2026-04-17.md` — 2026-04-17; draft.
5. `2026-agentic-AI-landscape-general-theory-2026-05-19.md` — 2026-05-19; non-prescriptive theory documentation.
6. `INBOX/THE-MUSIC-BOX-MODEL-2026-05-30.md` — 2026-05-30; model explicitly stated as a lens rather than canon.

*Prepared by Manus AI for Architect review. The prior experimental CrewAI implementation was removed after dependency review; no implementation, registration, or promotion follows from this note without further instruction.*
