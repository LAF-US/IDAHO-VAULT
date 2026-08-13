---
title: "MUD–MUSH World Architecture"
date: 2026-08-13
author: Manus AI
authority: pending Architect review
doc_class: architecture
status: draft
tags: [MUD, MUSH, MOO, world-model, multi-agent, architecture]
---

# MUD–MUSH World Architecture
## A Text-First, Persistent, Multi-User World Model

> **Design premise:** A MUD–MUSH world is not merely a chat interface with fictional names. It is a persistent place in which rooms, objects, actors, permissions, memory, and consequences are explicit enough to be inspected, revised, and played.

## 1. Purpose

This document describes an architecture for a text-first world inspired by the traditions of MUDs, MUSHes, and MOOs. The design combines the durable world state associated with MUD engines, the social and role-playing flexibility associated with MUSHes, and the inspectable object model associated with MOOs.

The system should support both human and artificial participants. It should make their actions legible through rooms, verbs, artifacts, and records rather than treating an opaque agent transcript as the world itself.

## 2. Design principles

| Principle | Meaning |
|---|---|
| **Place before prose** | Every interaction occurs somewhere: a room, passage, workshop, archive, court, garden, or other named location with an explicit state. |
| **Objects have state** | Characters, documents, tools, doors, keys, and signals are objects with discoverable properties and histories. |
| **Verbs have consequences** | Commands are not decorative prompt text. A verb either reports information, proposes a change, or changes recorded state under an explicit rule. |
| **Memory is inspectable** | Important state is preserved as a world record rather than hidden in model context alone. |
| **Permission is capability, not costume** | A title or persona does not itself grant an action. The system checks the capability required for that action. |
| **Narrative remains optional** | A scene may be richly narrated, but narrative language cannot silently override state, permissions, provenance, or a failed validation. |
| **Silence is a valid state** | Actors do not need to remain active between sessions. A world can wait, retain its record, and resume only when a new session begins. |

## 3. MUD, MUSH, and MOO contributions

The three traditions overlap, but each contributes a different emphasis to the design.

| Tradition | Primary contribution | Architectural implication |
|---|---|---|
| **MUD** | Rooms, movement, game-like mechanics, and persistent state. | The world needs a durable location graph, explicit verbs, event processing, and a clear lifecycle for state changes. |
| **MUSH** | Social role-play, expressive scenes, collaborative worldbuilding, and staff-mediated norms. | The world needs communication channels, scene controls, consent-aware interaction, and a distinction between in-character action and out-of-character administration. |
| **MOO** | Object-oriented world extension through reusable objects and verbs. | Rooms, items, characters, and systems should expose stable interfaces and inherit behavior from well-defined archetypes. |

The resulting system need not mimic any historical server implementation. Its useful inheritance is a discipline: the world is composed of understandable objects and actions rather than one unstructured conversation.

## 4. World model

### 4.1 Rooms and the location graph

A **room** is the minimum unit of place. It has a stable identifier, a human-readable name, a description, contents, exits, local rules, and an event history.

```text
Room
├── id
├── name
├── description
├── tags
├── exits
│   ├── direction or verb
│   ├── destination_room_id
│   └── access_rule
├── contents
├── local_state
├── local_verbs
└── event_log
```

Rooms form a directed graph. An exit may be ordinary, conditional, locked, scheduled, or available only to an actor holding a relevant capability. A room can also be non-spatial: a council chamber, an editing desk, an archive index, or an asynchronous correspondence hall.

### 4.2 Actors

An **actor** is any entity able to perceive, communicate, propose, or perform actions. Actors may be human players, non-player characters, service agents, or temporary summoned roles.

```text
Actor
├── id
├── display_name
├── kind                 # human, agent, NPC, service
├── location
├── inventory
├── role_card
├── capabilities
├── constraints
├── session_state
└── action_history
```

A role card gives an actor a voice, responsibilities, and boundaries. Capabilities are separate. For example, an actor may be described as a librarian but lack permission to alter archival records; another may carry a key that permits entry to a particular room without being an administrator of the world.

### 4.3 Objects and artifacts

An **object** is a persistent thing that can be examined, moved, used, opened, altered, or referenced. An artifact may be a physical-fictional object, a source document, a ledger, a map, a note, a key, or a tool.

```text
Object
├── id
├── names and aliases
├── description
├── archetype
├── location or container
├── owner or steward
├── properties
├── verbs
├── provenance
└── event_history
```

Objects should have stable identifiers even when their displayed names change. This permits aliasing, renaming, and narrative presentation without breaking references or obscuring history.

## 5. Hard code and soft code

The system separates **hard code** from **soft code** without treating either as inferior.

| Layer | Contents | Change posture |
|---|---|---|
| **Hard code** | Session handling, authentication, permissions, event storage, state-transition rules, object schemas, tool boundaries, rate limits, and audit hooks. | Deliberate engineering change, reviewed and tested. |
| **Soft code** | Room descriptions, object behavior, scene scripts, actor role cards, world lore, quest logic, dialogue patterns, and local rules. | Worldbuilding change, inspectable and versioned. |

Hard code prevents the world from becoming an unbounded improvisation engine. Soft code prevents the engine from becoming an inert database. The architecture needs both: a reliable stage and content that can meaningfully change what happens on it.

## 6. Command model

Each player or agent action should resolve through a clear command contract.

```text
COMMAND
  → parse intent
  → identify actor, room, and referenced objects
  → check visibility and capabilities
  → evaluate local and global rules
  → emit an event or a proposal
  → update state only if authorized
  → render an in-world response and an inspectable record
```

Commands fall into three categories:

| Category | Examples | State effect |
|---|---|---|
| **Observe** | `look`, `examine`, `inventory`, `read`, `whereis` | No world-state change; creates optional access telemetry. |
| **Interact** | `say`, `ask`, `give`, `take`, `open`, `move`, `use` | May alter location, inventory, relationship state, or a scene. |
| **Administer** | `build`, `create`, `set`, `grant`, `archive`, `approve` | Alters world structure or permissions; always requires an explicit capability and durable record. |

Natural-language input may be accepted, but it should compile into one or more named commands before it changes state. This preserves the expressive quality of a MUSH while retaining the accountability of a MUD engine.

## 7. Keys, capabilities, and authority

A **Key** is a capability-bearing object or token. It can unlock a room, authorize a specific action, permit access to an artifact class, or enable a narrow administrative function.

Keys should be scoped, inspectable, and revocable. A Key is not synonymous with a person, office, or permanent superiority. It is an explicit grant with an identified boundary.

| Capability pattern | Example |
|---|---|
| **Access Key** | Enter a protected chamber or inspect a restricted artifact. |
| **Action Key** | Create a room, move an object, initiate a scheduled event, or open a hearing. |
| **Delegation Key** | Permit a named actor to carry out one task on behalf of a steward. |
| **Review Key** | Permit a reviewer to accept, reject, archive, or return a proposed change. |

Every Key should answer four questions: **what does it unlock, for whom, under what conditions, and how is it revoked?**

## 8. Multi-agent participation

Artificial participants should enter the world as actors with role cards, tool boundaries, session budgets, and observable outputs. They should not be granted unrestricted mutation rights merely because they can produce persuasive language.

### 8.1 Agent session contract

```text
AgentSession
├── mission
├── allowed rooms
├── allowed objects
├── allowed tools
├── token / turn / time budget
├── writable surfaces
├── required record outputs
├── escalation conditions
└── stop conditions
```

An agent can investigate, converse, draft, challenge, or propose. A state-changing action becomes effective only when the relevant command, capability, and validation rule permit it.

### 8.2 Roles, conversations, and state machines

Multiple agent frameworks can coexist because they can serve different functions:

| Concern | Suitable mechanism |
|---|---|
| Role definitions, assignments, and task composition | Crew-style orchestration. |
| Explicit state, branching, parallel activity, pauses, and resumability | Graph-based orchestration. |
| Bounded dialogue, debate, cross-examination, and scene interaction | Conversation-oriented orchestration. |
| Schema enforcement, access checks, budgets, and durable event writing | Deterministic application code. |

The world engine remains the final arbiter of state transitions. An agent conversation may produce a proposal, a transcript, or a recommendation; it does not rewrite the world merely by reaching rhetorical agreement.

## 9. Scenes and social interaction

A MUSH-like layer should support scenes as first-class objects.

```text
Scene
├── id
├── room
├── participants
├── purpose
├── visibility
├── start and end conditions
├── transcript
├── declared consequences
└── linked events
```

This separates ordinary conversation from a scene with intended consequences. Participants can role-play freely inside a scene while the system keeps track of what, if anything, changed after the scene concludes.

A useful rule is: **fictional action is expressive; consequential action is explicit.** A participant may describe trying a door, offering a treaty, or presenting evidence. The engine decides whether the door opens, the agreement is recorded, or the evidence becomes attached to a case.

## 10. Persistence and time

The world should preserve three related but distinct records:

| Record | Purpose |
|---|---|
| **Current state** | Answers what exists and where it is now. |
| **Event ledger** | Answers what happened, in what order, and under which command or rule. |
| **Narrative record** | Preserves descriptions, scenes, reports, and interpretation without confusing them with state. |

Time may be real-time, turn-based, scheduled, or event-driven. The architecture should support all four without requiring constant activity. A room may remain unchanged for months. A scheduled event may occur at a named time. A scene may be paused and resumed. A world may be quiet without becoming dead.

## 11. Observability and moderation

A persistent multi-user world requires tools for inspection and repair.

| Need | Required facility |
|---|---|
| **Inspection** | Object examination, room contents, actor location, provenance, event history, and capability queries. |
| **Debugging** | Command traces, failed validation reasons, tool-call logs, and replayable state transitions. |
| **Moderation** | Consent controls, communication visibility, mute/block functions, conflict escalation, and access revocation. |
| **Recovery** | Snapshots, append-only event records, rollback or compensating actions, and clear archival states. |
| **Evaluation** | Tests for verbs, permissions, rooms, object behavior, agent budgets, and scenario outcomes. |

A Wizard role may be responsible for maintaining the engine, but wizardry is operational stewardship, not an exemption from logging or review.

## 12. Minimal viable world

The first playable slice should be small enough to understand end-to-end.

| Component | Initial implementation |
|---|---|
| Rooms | An entry hall, one workroom, one archive, and one gated chamber. |
| Actors | One human player, one bounded assistant actor, and one maintenance role. |
| Objects | A map, a ledger, a key, a door, and one source artifact. |
| Verbs | `look`, `go`, `examine`, `read`, `take`, `give`, `ask`, `propose`, and `review`. |
| State changes | Move an actor, transfer an object, submit a proposal, and accept or return it. |
| Record | Append each consequential action to an event ledger. |
| Agent behavior | One narrowly scoped investigative or editorial task with a hard stop condition. |

The first success criterion is not scale. It is whether a participant can enter, understand where they are, interact with a few meaningful objects, make a proposal, observe the review boundary, and understand the resulting record.

## 13. Open design decisions

1. Which actions should be synchronous commands and which should create asynchronous jobs?
2. What makes a room private, shared, temporary, or archival?
3. How should a player distinguish in-character speech, out-of-character coordination, system output, and agent-generated text?
4. What kinds of Keys are durable, temporary, delegated, or single-use?
5. When should an action create an immediate state change versus a reviewable proposal?
6. What events deserve full narrative scenes, and what events should remain concise ledger entries?
7. How can participant consent and safety constraints remain legible inside the fiction rather than being hidden in an external rulebook?

## 14. Summary

A durable MUD–MUSH world is a system of **places, objects, verbs, records, and bounded authority**. Its fiction becomes meaningful because the world can remember, inspect, and respond to action. Its engine remains humane because it allows narrative, dialogue, consent, pause, review, and repair.

The architecture should therefore preserve two complementary truths: a world must be expressive enough for people to inhabit, and structured enough that no participant—human or artificial—can quietly redefine what happened.

---

### Reference orientation

This is a conceptual architecture document. It draws on the general traditions of MUDs, MUSHes, and MOOs, including persistent rooms, objects, verbs, social scenes, and programmable behaviors. It does not prescribe a particular historical codebase or server implementation.
