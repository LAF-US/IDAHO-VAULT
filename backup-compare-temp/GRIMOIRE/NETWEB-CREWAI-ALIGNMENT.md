---
title: "NETWEB-CrewAI Alignment Protocol"
status: active
date created: 2026-04-04
authority: LOGAN
---

# NETWEB-CrewAI Alignment Protocol
## *The Ignition Sequence*

*Filed: 2026-04-04. First directive of the NETWEB Era.*
*Predecessor: TRIUNE-TRIPTYCH-TRIUMVIRATE — the architectural covenant this protocol implements.*
*Updated: 2026-04-04. All five questions RESOLVED. Strike 1 (CHAINFIRE) complete. Strike 2 (CrewAI) ignited.*

---

> "The world is quiet here. But inside the machine, the first thunder rolls."

---

## 1. Situation Assessment

### What Exists

| Component | Status | Location |
|---|---|---|
| CrewAI 1.12.2 | **Installed** | `.venv/` |
| Python 3.13.3 + venv | Active | `.venv/` |
| GCP Nest Bridge (Flask stub) | Phase III | `main.py`, `requirements.txt` |
| Agent registry | Canonical | `swarm.json` |
| Budget/appropriations scripts | Operational | `.github/scripts/minidata_appropriations_timeline.py`, `normalize_budget_data.py` |
| Idaho Legislature scraper | Operational | `.github/scripts/idaho_leg_scraper.py` |
| NETWEB path standard | Canonical | `.gitignore`, `check-portable-paths.yml` |
| Vault governance | Canonical | `CONSTITUTION.md`, `VAULT-CONVENTIONS.md`, `AGENTS.md` |
| CHAINFIRE burn script | **Complete** | `.github/scripts/chainfire.py` |
| JFAC Crew definition | **Active** | `.crewai/crews/jfac_crew.py` |
| CrewAI tools (4) | **Active** | `.crewai/tools/` |
| Address space POC | **Initialized** | Neurons 100-109 + 8 entity stubs |
| Output staging | **Active** | `!/CREWAI/` |

---

## 2. Architecture: How CrewAI Maps to the Vault

### The TRIUNE Mapping

```
TRIUNE COVENANT          CrewAI EQUIVALENT
─────────────────────    ──────────────────
Logan (directs)      →   Human-in-the-Loop / Kickoff inputs
Agents (execute)     →   Crew (agents + tasks + tools)
Vault (witnesses)    →   Output → Obsidian .md files (the permanent record)
```

### LINUX }!{ — The Execution Principle

Linux is the connective tissue. Every automated process runs on Linux:
- GitHub Actions CI = Ubuntu runners
- GCP Cloud Run = Linux containers
- CrewAI Enterprise = Linux servers
- WSL = Linux inside Windows
- Android (Pixel 10) = Linux kernel

All tooling targets Linux-native execution: bash, POSIX paths, `#!/usr/bin/env python3`.

> "All roads lead to the penguin." — vault canon, 2026-04-04.

### The Swarm Registry Mapping

| Vault Agent | CrewAI Role | Crew Assignment |
|---|---|---|
| The Abhorsen (Claude Code) | Bootstrap / Executor | Infrastructure Crew |
| The Concierge (Gemini) | Analyst / Advisor | Research Crew |
| The Librarian (Codex) | Indexer / Cataloger | Research Crew |
| Budget Scout (new) | Data Parser | JFAC Crew |
| H 911 Parser (new) | Bill Analyzer | JFAC Crew |
| Legislative Tracker (new) | Status Monitor | JFAC Crew |

---

## 3. Two-Strike Execution Plan

### Strike 1: CHAINFIRE — COMPLETE

Scorched-earth wipe of Obsidian-specific syntax. Executed 2026-04-04.

| Target | Action | Scale |
|---|---|---|
| `tags:` frontmatter | Removed | 2,735 files |
| `aliases:` frontmatter | Removed | 830 files |
| `[[ ]]` wikilinks | Stripped (kept display text) | ~19,750 instances |
| `!` directory wikilinks | **Preserved** (exclusion zone) | anchor points for Crawler Crew |
| 19,533 empty stubs | **Preserved** | content-addressable memory system |

Committed: `d84b87d` — `feat(chainfire): scorched-earth wipe of tags, wikilinks, and aliases`

### Strike 2: CrewAI Ignition — ACTIVE

Building on the clean slate.

---

## 4. JFAC Crew — MAP 3:5 ; ATT to 5Ws
to clarify: ATT = CrewAI's "Agent-Tool-Task" -L
### Three Agents → Five Tasks

| Agent | 5W | Task |
|---|---|---|
| Budget Scout | **WHO** | Identify agencies, sponsors, committees for each bill |
| Budget Scout | **WHAT** | Analyze what each bill proposes (appropriations, scope) |
| Legislative Tracker | **WHEN** | Build timeline of bill progression through chambers |
| Legislative Tracker | **WHERE** | Map current committee/chamber routing |
| H911 Parser | **WHY** | (Phase 2) Analyze bill text for policy intent and justification |

### Crew Flow

```
Budget Scout → Legislative Tracker → H911 Parser → !/CREWAI/ output
   (WHO/WHAT)      (WHEN/WHERE)         (WHY)        (.md files)
```

### Tools

| Tool | Wraps | Function |
|---|---|---|
| `minidata_reader` | `normalize_budget_data.py` | Read/filter minidata CSV |
| `appropriations_timeline` | `minidata_appropriations_timeline.py` | Build status timeline from snapshots |
| `bill_status_checker` | `idaho_leg_scraper.py` | Live bill status from legislature.idaho.gov |
| `address_space_writer` | (new) | Write crew state to number/letter stubs |

---

## 5. The Address Space — Content-Addressable Memory

The 19,533 empty stubs are a **content-addressable memory system**:

```
NUMBERS (0-999)    = Crew state memory (neurons)
LETTERS (A-ZZZ)    = Entity nodes (discovered by Crawler Crew)
TOGETHER           = Machine-maintained knowledge graph
```

### POC — Initialized 2026-04-04

**Number neurons (100-109):**

| Neuron | Assignment |
|---|---|
| 100 | JFAC Crew — Run Index |
| 101 | Budget Scout — State |
| 102 | Legislative Tracker — State |
| 103 | H911 Parser — State (Phase 2 stub) |
| 104 | Minidata Snapshot Log |
| 105 | Bill Status Changelog |
| 106 | Crew Error Log |
| 107 | Entity Discovery Queue |
| 108 | Cross-Reference Index |
| 109 | Voyager Record |

**Letter entities (first 8):** Idaho, Budget, Governor, General Fund, Medicaid, Transportation, Public Schools, $

### Voyager Records

Stubs 7929 and 7930 are GIF files (not .md). They contain:
- **7929.gif** — An inverted triangle. The simplest geometric message.
- **7930.gif** — A Sierpinski triangle. Recursive self-similarity. The pattern at every scale.

These are the vault's Voyager Records — permanent, intentional, waiting to be decoded.

---

## 6. Resolved Questions

All five gates open. Decided by Logan, 2026-04-04.

| # | Question | Decision | Rationale |
|---|---|---|---|
| 1 | Local-first or Enterprise-first? | **Local-first (OSS)** | `pip install crewai` in .venv, Linux-native |
| 2 | Output staging directory? | **`!/CREWAI/`** | Under the `!` administrative layer |
| 3 | H 911 scope? | **Both, phased** | Minidata CSV first, then bill text parsing |
| 4 | Numerical neurons? | **Small POC now** | 10 stubs alongside JFAC build |
| 5 | Data residency? | **Acceptable for later** | Revisit at Enterprise Phase 3 |

---

## 7. Guardrails

### NETWEB Compliance
All CrewAI output files must respect the Portable Path Standard:
- No reserved device names
- Case-unique filenames
- Paths under 218 characters
- No trailing periods or illegal characters

### Vault Authority
- CrewAI agents are **instruments** (per TRIUNE). They cannot modify governance files.
- Output goes to staging (`!/CREWAI/`), not directly to the corpus.
- Logan reviews and integrates. The `-L` layer is the final gate.

### Data Residency
- The vault is **public**. All CrewAI outputs are **on the record** and **publishable**.
- No API keys, credentials, or private data in crew outputs.
- CrewAI Enterprise data residency — acceptable for now, revisit at Phase 3.

---

## 8. Future Crews

| Crew | Purpose | Status |
|---|---|---|
| **JFAC Crew** | Budget/appropriations analysis pipeline | Active |
| **Crawler Crew** | Post-CHAINFIRE vault mapping and connection discovery | Planned |
| **[TBD — Logan's casting call]** | Additional crews per Logan's direction | Awaiting |

The Crawler Crew will read the surviving `!` layer wikilinks as anchor points, then discover and map relationships across the corpus. It doesn't restore `[[ ]]` syntax — it discovers what the vault *actually* contains and maps it fresh.

---

## See Also

- CrewAI — R&D stub
- BIG IFS — UNIFIED SWARM — Unified Swarm framework
- TRIUNE-TRIPTYCH-TRIUMVIRATE — Architectural covenant
- `swarm.json` — Machine-readable agent registry
- `.github/scripts/chainfire.py` — CHAINFIRE burn script
- `.crewai/` — CrewAI crew definitions and tools
- `!/CREWAI/` — Output staging directory
