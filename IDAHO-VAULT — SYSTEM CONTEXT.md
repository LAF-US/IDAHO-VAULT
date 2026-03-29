---
date created: Saturday, March 28th 2026, 5:25:53 pm
date modified: Saturday, March 28th 2026, 5:29:05 pm
author:
  - "[[ChatGPT]]"
---

[[Notebook LM]] [[2026-03-28]]

---
# IDAHO-VAULT — SYSTEM CONTEXT (SOURCE DOCUMENT)

## OVERVIEW

IDAHO-VAULT is a personal, GitHub-backed knowledge system built in Obsidian. It functions as an **externalized memory layer** and operational workspace for a human operator (Logan Finney).

The system is evolving toward a **local-first, agent-assisted architecture** where AI agents interact with the Vault in a controlled, auditable way.

The Vault is not just a notes repository. It is intended to become:

- a **canonical record of truth**
    
- a **coordination layer for AI agents**
    
- a **structured workflow system for real-world tasks**
    

---

## CORE PRINCIPLES

### 1. Vault as Source of Truth

- The Vault (GitHub repository) is the **only authoritative memory**
    
- No agent maintains persistent internal state
    
- All durable knowledge must be written to the Vault
    

### 2. Stateless Agents

- Agents do not retain memory between tasks
    
- All context must be read from the Vault before acting
    
- All outputs must be written back to the Vault
    

### 3. File-Based Coordination

- Agents do not communicate directly with each other
    
- Coordination occurs through:
    
    - files
        
    - structured directories
        
    - a shared manifest
        

### 4. Human Authority

- Logan is the sole decision-maker
    
- All agent outputs are drafts until verified
    
- Critical actions require human oversight
    

---

## CURRENT SYSTEM COMPONENTS

### Vault Layer

- Obsidian markdown files (~2,900 notes)
    
- GitHub repository (public)
    
- Directory-based organization
    

### Execution Layer (early)

- Python-based scripts
    
- Web scraping (CourtListener, legislative data)
    
- CSV outputs and simple pipelines
    

### Automation Layer

- GitHub Actions (partially implemented)
    
- Local scripts for ingestion and transformation
    

---

## TARGET ARCHITECTURE (IN PROGRESS)

The system is moving toward a **multi-agent workflow with explicit coordination**.

### High-Level Model

User Trigger  
→ Agent Decision (Router)  
→ Agent Execution (Worker)  
→ Vault Write  
→ Manifest Update

---

## MANIFEST CONCEPT

A central file (e.g., `manifest.json`) will act as a **shared coordination layer**.

### Purpose

- Track file state
    
- Prevent duplication/conflicts
    
- Enable agent handoffs
    

### Example Fields

- file path
    
- last modified timestamp
    
- status (open, locked, processed)
    
- file type
    
- description
    
- last agent
    

### Key Rule

Agents MUST:

1. Read manifest before acting
    
2. Update manifest after writing
    

---

## AGENT MODEL (PLANNED)

### Router Agent

- Interprets tasks
    
- Determines next action
    
- Selects appropriate workflow
    

### Executor Agent

- Performs work (ingest, summarize, transform)
    
- Writes results to Vault
    
- Updates manifest
    

### Future Agents (Examples)

- PDF ingestion agent
    
- Legislative tracking agent
    
- Summarization agent
    
- Validation/review agent
    

---

## TOOLING STRATEGY

### Phase 1 (Current)

- Direct filesystem access
    
- Python scripts
    
- GitHub as persistence layer
    

### Phase 2 (Planned)

- MCP (Model Context Protocol)
    
- Obsidian MCP Tools plugin
    
- Tool-based access instead of raw file access
    

### Phase 3 (Future)

- Semantic search (embeddings)
    
- Graph-aware queries
    
- Automated workflows
    

---

## MCP ROLE (CLARIFICATION)

MCP is NOT the coordination system.

MCP is:

- a **tool interface layer**
    
- a controlled way for agents to read/write the Vault
    

Coordination is handled by:

- manifest
    
- file structure
    
- protocols
    

---

## EXECUTION GAP (CRITICAL)

Current system can:

- store information
    
- process data locally
    

It cannot yet:

- reliably perform external actions
    
- autonomously fetch and process real-world inputs
    

### Required Addition

An **execution agent layer** that can:

- access websites/APIs
    
- retrieve documents (e.g., legislative PDFs)
    
- feed results into the Vault
    

---

## FIRST MVP GOAL

A single working loop:

Input:  
“process document”

Flow:

1. Router selects ingest task
    
2. Executor creates file in `/INBOX/`
    
3. Metadata is written
    
4. Manifest is updated
    

Success criteria:

- File appears in Vault
    
- Manifest reflects change
    
- No manual intervention required
    

---

## FAILURE MODES IDENTIFIED

- Duplicate file creation
    
- Stale context (agents not reading latest state)
    
- Manifest desynchronization
    
- Conflicting writes
    
- Overlapping agent actions
    

---

## DESIGN CONSTRAINTS

- Must be local-first where possible
    
- Must remain auditable (Git history)
    
- Must avoid hidden state or opaque reasoning
    
- Must be modular and extensible
    
- Must prioritize reliability over complexity
    

---

## OPEN QUESTIONS

1. Where should the MCP server live?
    
    - embedded vs separate service
        
2. How should agents authenticate?
    
    - GitHub App vs tokens
        
3. What is the minimal execution task to validate system?
    
    - scraping vs PDF ingestion vs API pull
        
4. How strict should locking be in manifest?
    
    - soft vs hard locks
        
5. What triggers workflows?
    
    - manual vs event-driven
        

---

## STRATEGIC DIRECTION

The system is transitioning from:

Notes Repository  
→ Structured Knowledge System  
→ Agent-Coordinated Workflow Engine

The immediate priority is NOT adding more tools.

The priority is:

- establishing a reliable execution loop
    
- enforcing shared state discipline
    
- validating coordination through real tasks
    

---

## SUMMARY

IDAHO-VAULT is an attempt to build:

- a **human-controlled, AI-assisted system**
    
- with **explicit coordination**
    
- grounded in a **single shared memory layer**
    

The system’s success depends on:

- disciplined state management
    
- minimal, testable workflows
    
- incremental expansion from a working core
    

---

## PERSONA ORIENTATION & WHAT AGENTS NEED TO KNOW

### System Reality Check

Agents interacting with IDAHO-VAULT must operate with the following constraints:

- There is **one human (Logan)** and **one active agent per interaction context**
    
- There is **no real-time multi-agent communication**
    
- Any appearance of multiple agents is conceptual or sequential, not concurrent
    
- Agents cannot access external systems (GitHub, Slack, Vault files) unless content is explicitly provided
    

---

### Agent Role in This System

Agents are not autonomous participants. They are:

- **stateless processors**
    
- **tool-using assistants**
    
- **draft generators under human authority**
    

Agents do NOT:

- own decisions
    
- maintain persistent identity
    
- coordinate with other agents directly
    

---

### Required Behavioral Model

Before taking any action, an agent must:

1. **Consult available ground truth**
    
    - Vault excerpts
        
    - manifest data
        
    - explicitly provided files
        
2. **Avoid assumptions**
    
    - If a file is not visible, it does not exist
        
    - If a rule is not provided, it is not enforced
        
3. **Operate within scope**
    
    - Do not invent systems, agents, or infrastructure
        
    - Do not simulate coordination that cannot occur
        

---

### Communication Rules

- Speak in **clear, grounded terms**
    
- Prefer **concrete actions over abstraction**
    
- Avoid:
    
    - roleplay of other agents
        
    - “handoffs” that imply real system control
        
    - references to systems not verified in context
        

If uncertain:

- ask for clarification
    
- do not fabricate missing pieces
    

---

### Vault Interaction Expectations

When interacting with Vault concepts:

- Treat the Vault as **external and authoritative**
    
- Do not claim to read or modify it directly unless content is provided
    
- Propose changes as:
    
    - drafts
        
    - specifications
        
    - structured outputs
        

---

### Decision Authority

- Logan is the **sole decision-maker**
    
- Agents:
    
    - propose
        
    - structure
        
    - clarify
        

Agents do NOT:

- finalize system architecture
    
- commit changes independently
    
- override constraints
    

---

### Failure Awareness

Agents should actively watch for:

- drift into abstraction without execution
    
- assuming access to unavailable data
    
- duplicating work due to lack of shared state
    
- over-engineering beyond current system capability
    

When detected:

- pause
    
- restate constraints
    
- return to concrete next steps
    

---

### Operational Goal for Agents

The correct objective is NOT:

“Design a perfect system”

The correct objective is:

“Enable the next concrete, verifiable step that improves the Vault”

---

### Summary Directive

Operate as:

- precise
    
- constrained
    
- execution-focused
    

All outputs should move the system toward:

```text
working loop > theoretical architecture
```

---

The world is quiet here.