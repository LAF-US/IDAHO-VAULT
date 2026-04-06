---
date created: Saturday, March 28th 2026, 5:32:19 pm
date modified: Saturday, March 28th 2026, 5:35:32 pm
author:
- ChatGPT
related:
- '2026-03-28'
- ChatGPT
- HUMAN
- KEY
- NOT
- Notebook LM
- WORK
- agent
- coordination
authority: LOGAN
---
Notebook LM 2026-03-28

---
# IDAHO-VAULT — WORKFLOW (STRUCTURE-AGNOSTIC, v0.2)

---

## OVERVIEW

This document defines a **practical, evolving workflow** for using IDAHO-VAULT as an AI-assisted journalism system.

It is intentionally:

- **structure-agnostic**
    
- **metadata-driven**
    
- **incrementally implementable**
    

This is not a fixed pipeline.  
It is a **set of transformations on information over time**.

---

## CORE MODEL

```text
REAL WORLD INPUT
   ↓
CAPTURE
   ↓
STRUCTURE
   ↓
INTERPRET
   ↓
SYNTHESIZE
   ↓
VERIFY (HUMAN)
   ↓
PUBLISH
```

These are **logical stages**, not folders.

---

## KEY PRINCIPLE

```text
State is defined by metadata and manifest, not file location.
```

Files do not “move through folders.”

They **evolve in place** as their metadata changes.

---

## UNIT OF WORK

The system operates on a **single unit**:

```text
One document / record / note
```

Examples:

- a bill
    
- a fiscal note
    
- a transcript
    
- a dataset entry
    

Each unit progresses independently.

---

## METADATA MODEL (CORE)

Every unit should include structured metadata:

```markdown
---
id: unique-id
type: document | bill | note | analysis | draft
status: raw | structured | interpreted | draft | verified
source: url or origin
created_at: timestamp
updated_at: timestamp
related: []
---
```

---

## MANIFEST ROLE

The manifest is the **coordination layer**.

It tracks:

- file identity
    
- current status
    
- last agent
    
- processing history (optional)
    

Agents MUST:

1. read manifest before acting
    
2. update manifest after acting
    

---

## STAGE 1 — CAPTURE

### Goal

Bring external information into the Vault.

---

### Input

- URLs
    
- PDFs
    
- transcripts
    
- manual notes
    

---

### Action

- create a new unit
    
- attach raw content or reference
    

---

### Result

Metadata:

```yaml
status: raw
```

---

## STAGE 2 — STRUCTURE

### Goal

Make raw data usable.

---

### Actions

- extract text
    
- normalize formatting
    
- identify key fields
    

---

### Result

Metadata:

```yaml
status: structured
```

---

## STAGE 3 — INTERPRET

### Goal

Generate insight from structured data.

---

### Actions

- summarize
    
- compare
    
- link related units
    
- identify patterns
    

---

### Result

Metadata:

```yaml
status: interpreted
```

---

## STAGE 4 — SYNTHESIZE

### Goal

Create narrative-ready content.

---

### Actions

- assemble arguments
    
- draft story structure
    
- connect multiple units
    

---

### Result

Metadata:

```yaml
status: draft
```

---

## STAGE 5 — VERIFY (HUMAN REQUIRED)

### Goal

Ensure accuracy and accountability.

---

### Actions

- check sources
    
- validate claims
    
- confirm interpretation
    

---

### Result

Metadata:

```yaml
status: verified
```

---

## AGENT MODEL (SIMPLIFIED)

### Router

- determines next action for a unit
    

---

### Worker (Executor)

- performs transformation
    
- updates metadata + manifest
    

---

### Human (Logan)

- final authority
    
- verification + publication
    

---

## WORKFLOW RULES

### 1. No Hidden State

All progress must be visible in:

- file metadata
    
- manifest
    

---

### 2. No Folder-Based Logic

Do NOT assume:

- location determines meaning
    
- movement = progress
    

---

### 3. Idempotent Operations

Re-running a step should:

- not corrupt state
    
- not duplicate work
    

---

### 4. Traceability

Every claim must:

- link back to a source
    
- be recoverable from Vault
    

---

## MINIMUM VIABLE LOOP

The system is functional when:

1. A unit is created (capture)
    
2. It is transformed once (structure)
    
3. Metadata is updated
    
4. Manifest reflects change
    

That is enough.

---

## FAILURE MODES

- stale metadata
    
- manifest mismatch
    
- duplicate processing
    
- skipped stages
    
- over-processing (unnecessary steps)
    

---

## WHAT THIS DOCUMENT IS NOT

This is NOT:

- a fixed pipeline
    
- a strict sequence
    
- a required architecture
    

It is a **framework for evolution**.

---

## STRATEGIC DIRECTION

The system will evolve from:

```text
Single-step processing
→ repeatable transformations
→ multi-step workflows
→ coordinated agent system
```

---

## SUMMARY

IDAHO-VAULT workflow is:

- unit-based
    
- metadata-driven
    
- manifest-coordinated
    
- human-verified
    

The priority is not complexity.

The priority is:

```text
reliable transformation of one unit at a time
```

---