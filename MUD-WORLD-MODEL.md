---
title: "MUD-World Model Architecture — Hard Code vs. Soft Code"
date created: 2026-06-03
authority: LOGAN
doc_class: architecture
status: active
related:
  - CONSTITUTION.md
  - AGENTS.md
  - !/AGENTS.md
tags: [MUD, MUSH, MOO, architecture, world-model, hard-code, soft-code]
---

# MUD-World Model Architecture
## The Convergence of Text-Based Worlds and Git-Based Multi-Agent Systems

*Filed at the repository root. This document establishes the conceptual and structural mapping between classical MUD/MUSH/MOO server architectures and the `IDAHO-VAULT` multi-agent ecosystem [1].*

---

## 1. The Core Metaphor: From Database to Virtual World

In classical text-based virtual worlds (MUDs, MUSHes, and MOOs), the engine maintains a persistent database where every room, item, player, and program is an object assigned an object number (`#0`, `#1`, etc.) [2]. 

In `IDAHO-VAULT`, the git repository serves as this persistent object database:
- **Git Commits** represent the transaction log and time-state of the world.
- **Branches** represent alternate dimensional realms (the "Central Finite Curve" model).
- **Files and Directories** represent rooms, containers, and interactive items.

| MUD/MOO Concept | Git & Vault Equivalent | Operational Meaning |
| :--- | :--- | :--- |
| **The Server Engine** | Python Runtimes & CLI Tools | Low-level execution layer handling command parsing, validation, and state transitions (Hard Code) [3]. |
| **The Persistent Database** | The Git Repository (`IDAHO-VAULT`) | Immutable storage of all world objects, room descriptions, and historical state [2]. |
| **Rooms & Chambers** | Vault Directories & Districts | Bounded contexts where agents gather, leave traces, and execute localized rules. |
| **Objects & Inventory** | Markdown Files & Artifacts | Readable, interactive elements that agents can examine, modify, or carry across commits. |
| **Wizards & Programmers** | Logan & Authorized Agents | Entities with elevated standing to write soft code and shape world rules [2]. |

---

## 2. Hard Code vs. Soft Code Architecture

Following classical MUD design principles, our architecture cleanly separates the foundational engine from the high-level narrative and behavioral scripts [3].

### 2.1 Hard Code (The Engine Layer)
Hard code refers to the low-level system software responsible for security, memory, transport, and protocol execution [3]. In our stack, this comprises:
- **The Constitution & Emanation Rules**: Physics-level constraints that dictate how authority flows from the first principle (`-L`) outward [4].
- **Python Frameworks & Runners**: Deterministic validators, schema enforcers, and execution harnesses (CrewAI, LangGraph, etc.) that prevent unauthorized state transitions.
- **Git Control Surfaces**: Hooks, branch protections, and commit sign-offs that enforce chain-of-custody.

### 2.2 Soft Code (The World Layer)
Soft code refers to the high-level scripts, personas, prompts, and narrative structures interpreted by the engine at runtime [3]. In our stack, this comprises:
- **Agent Personas & Backstories**: The specific roles of the 5 Wizards (WHO, WHAT, WHEN, WHERE, WHY) and their Familiars.
- **Room Descriptions & Lore Files**: Markdown documents at the repository root that establish the narrative reality and rules of engagement for anyone entering that directory.
- **Pheromone Traces & Dockets**: Ephemeral state and communication logs left by agents as they traverse the world.

---

## 3. Repository Root as the Entry Chamber

Placing core governance and architectural files directly at the repository root ensures that any agent or observer waking up in this dimension immediately encounters the "Entry Chamber" rules before exploring deeper subdirectories [5].

1. **`CONSTITUTION.md`**: The supreme law of the realm.
2. **`AGENTS.md`**: The roster and standing of entities.
3. **`MUD-WORLD-MODEL.md`**: This architectural bridge connecting text-based worldbuilding to agentic execution.
4. **`5WHO.md`, `5WHAT.md`, `5WHEN.md`, `5WHERE.md`, `5WHY.md`, `5HOW.md`**: The active inquiry slots for the current session.

---

## 4. Conclusion

By viewing `IDAHO-VAULT` through the lens of a MUD/MUSH engine, we reconcile the rigid discipline of software engineering with the expressive freedom of interactive storytelling. Hard code ensures the world does not collapse into ungrounded hallucination; soft code breathes life into the agents that inhabit it.

---

*Esto Perpetua.*

### References
- [1] `IDAHO-VAULT/CONSTITUTION.md`
- [2] Fandom MUD Wiki. *MOO Architecture*. 
- [3] Wikipedia. *Hard Coding and Soft Coding in MUDs*.
- [4] `IDAHO-VAULT/!/EMANATIONISM-PRINCIPLE-2026-05-18.md`
- [5] `IDAHO-VAULT/!/WAKEUP.md`
