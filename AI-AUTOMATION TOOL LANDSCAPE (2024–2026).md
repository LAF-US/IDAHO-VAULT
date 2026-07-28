---
date created: Saturday, March 28th 2026, 5:31:30 pm
date modified: Saturday, March 28th 2026, 5:32:17 pm
related:
- '2026-03-28'
- ADD
- API
- CLI
- CrewAI
- DEVELOPMENT
- FRAMEWORKS
- GUI
- GitHub
- LLM
- MCP
- MVP
- NOT
- Notebook LM
- OCR
- Obsidian
- OpenAI
- OpenAI Swarm
- PROTOCOL
- RSS
- agent
- coordination
- node
- systems
- web
authority: LOGAN
---
Notebook LM 2026-03-28

---
# AI + AUTOMATION TOOL LANDSCAPE (2024–2026)

## Practical Tool Shelf — Open, Local-First, Hobbyist → Professional

---

## OVERVIEW

This document surveys currently available tools for building:

- AI-assisted workflows
    
- multi-agent systems
    
- local-first knowledge systems
    
- journalism/data pipelines
    

Priority is given to:

- free / open-source tools
    
- local execution capability
    
- strong community ecosystems
    

---

## 1. LOCAL MODELS (LLMs)

### Purpose

Run AI models locally without relying on cloud APIs.

---

### Tools

#### Ollama

- Local model runner (Mac/Linux/Windows)
    
- Simple CLI + API
    
- Supports Llama, Mistral, Qwen, DeepSeek
    

Use case:

- local inference
    
- privacy-preserving workflows
    

---

#### LM Studio

- GUI-based local model runner
    
- Easy model downloads and testing
    

Use case:

- experimentation
    
- non-technical workflows
    

---

#### llama.cpp ecosystem

- Highly optimized C++ inference
    
- Runs on low-resource hardware
    

Use case:

- edge devices
    
- offline systems
    

---

### Tradeoffs

Pros:

- privacy
    
- no API cost
    
- offline capability
    

Cons:

- lower performance vs top cloud models
    
- hardware constraints
    

---

## 2. ROUTING & MULTI-AGENT FRAMEWORKS

### Purpose

Coordinate multiple agents or tasks.

---

### Tools

#### OpenAI Swarm

- Minimal orchestration framework
    
- explicit handoffs
    
- stateless design
    

Use case:

- controlled workflows
    
- testable routing logic
    

---

#### LangGraph

- graph-based orchestration (LangChain ecosystem)
    
- persistent state support
    

Use case:

- complex pipelines
    
- branching workflows
    

---

#### AutoGen

- multi-agent conversations
    
- more autonomous behavior
    

Use case:

- experimentation
    
- research setups
    

---

#### CrewAI

- role-based agent teams
    
- higher-level abstraction
    

Use case:

- quick prototyping
    

---

### Tradeoffs

Low-level (Swarm):

- more control
    
- more work
    

High-level (CrewAI, AutoGen):

- faster setup
    
- less predictability
    

---

## 3. MEMORY & STORAGE SYSTEMS

### Purpose

Persist state outside the model.

---

### Tools

#### Obsidian (Markdown Vault)

- local-first knowledge base
    
- file-based
    
- graph visualization
    

Use case:

- canonical memory layer
    

---

#### Git / GitHub

- version control
    
- audit trail
    
- automation (Actions)
    

Use case:

- authoritative state
    
- history + rollback
    

---

#### SQLite / Postgres

- structured storage
    

Use case:

- metadata
    
- logs
    
- structured queries
    

---

#### Vector Databases

##### Chroma

- lightweight
    
- easy local setup
    

##### LanceDB

- optimized for local + columnar storage
    

Use case:

- semantic search
    
- embeddings
    

---

### Tradeoffs

Files (Obsidian):

- transparent
    
- human-readable
    

Databases:

- scalable
    
- more complex
    

---

## 4. MCP (MODEL CONTEXT PROTOCOL)

### Purpose

Standardized interface between agents and tools.

---

### Tools

#### Obsidian MCP Tools plugin

- exposes vault as tool interface
    

#### Custom MCP servers

- Node.js / Python implementations
    

---

### Role in System

- NOT coordination
    
- IS controlled access layer
    

---

### Tradeoffs

Pros:

- secure tool access
    
- modular
    

Cons:

- immature ecosystem
    
- added complexity
    

---

## 5. DATA INGESTION & SCRAPING

### Purpose

Bring external data into the system.

---

### Tools

#### Python (requests, BeautifulSoup)

- simple web scraping
    

---

#### Playwright

- browser automation
    
- handles dynamic sites
    

---

#### Scrapy

- large-scale scraping framework
    

---

#### CourtListener API

- legal data access
    

---

#### RSS / Public APIs

- structured feeds
    

---

### Tradeoffs

Simple tools:

- fast to build
    
- brittle
    

Advanced tools:

- more reliable
    
- more setup
    

---

## 6. DOCUMENT PROCESSING

### Purpose

Extract structured data from PDFs, images, documents.

---

### Tools

#### Docling

- document parsing
    
- structured output
    

---

#### Unstructured.io

- converts documents to structured formats
    

---

#### Tesseract OCR

- open-source OCR
    

---

#### Vision-capable models (local or API)

- extract from complex layouts
    

---

### Tradeoffs

- OCR accuracy varies
    
- complex documents require multiple passes
    

---

## 7. AUTOMATION & ORCHESTRATION

### Purpose

Trigger workflows and manage execution.

---

### Tools

#### GitHub Actions

- CI/CD workflows
    
- event-based triggers
    

Use case:

- automation tied to repo
    

---

#### Cron jobs

- scheduled execution
    

---

#### Airflow / Prefect

- workflow orchestration
    

Use case:

- complex pipelines
    

---

### Tradeoffs

Simple (cron, Actions):

- easy
    
- limited
    

Advanced (Airflow):

- powerful
    
- heavy
    

---

## 8. LOCAL NETWORKING & SYNC (ADVANCED)

### Purpose

Enable multi-device or offline coordination.

---

### Tools

#### Tailscale / WireGuard

- secure mesh networking
    

---

#### Syncthing

- file synchronization
    

---

### Use Case

- local-first replication
    
- offline workflows
    

---

### Tradeoffs

- adds operational complexity
    
- not needed for MVP
    

---

## 9. DEVELOPMENT ENVIRONMENT

### Tools

#### VS Code / Cursor

- code editor with AI support
    

---

#### Jupyter Notebooks

- experimentation
    
- data workflows
    

---

#### Docker

- environment isolation
    

---

---

## 10. OBSERVABILITY & LOGGING

### Purpose

Track system behavior.

---

### Tools

#### Plain logs (files)

- simplest approach
    

---

#### Structured logs (JSON)

- machine-readable
    

---

#### Monitoring tools (optional)

- Prometheus / Grafana
    

---

---

## PRACTICAL STACK (RECOMMENDED BASELINE)

For a local-first, open system:

```text
LLM: Ollama
Routing: OpenAI Swarm
Memory: Obsidian + GitHub
Execution: Python scripts
Automation: GitHub Actions
Ingestion: Playwright + requests
Docs: Markdown + JSON
```

---

## MINIMAL VIABLE STACK

Start with:

```text
Python
Obsidian vault
GitHub repo
One agent (router/executor)
Basic file writes
```

---

## WHAT NOT TO ADD EARLY

Avoid:

- full vector database
    
- complex orchestration frameworks
    
- distributed systems
    
- multi-node sync
    
- custom MCP servers
    

---

## SELECTION CRITERIA

Choose tools based on:

1. Does it reduce complexity?
    
2. Can it run locally?
    
3. Is it inspectable/auditable?
    
4. Does it integrate with existing system?
    
5. Can it be removed later?
    

---

## STRATEGIC INSIGHT

The limiting factor is NOT tool availability.

There are already more tools than needed.

The limiting factor is:

- disciplined system design
    
- clear workflows
    
- controlled state management
    

---

## SUMMARY

The current ecosystem provides everything needed to build:

- local-first AI systems
    
- agent-based workflows
    
- data ingestion pipelines
    

No single tool solves the system.

Success comes from:

- combining simple tools correctly
    
- validating small workflows
    
- avoiding unnecessary complexity
    

---