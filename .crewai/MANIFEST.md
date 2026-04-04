---
title: "CrewAI Harbor Manifest"
date created: "2026-04-04"
authority: crewai
doc_class: manifest
---

# CrewAI Harbor Manifest

Machine-scannable, human-readable registry of all crews, agents, tasks, tools, and outputs.

**Upstream authority:** `swarm.json` (root) — the canonical machine-readable agent registry. This manifest does NOT replace it. CrewAI crews are instruments within the swarm, not a parallel registry.

**Architectural directive:** `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md`

---

## Runtime

| Key | Value |
|---|---|
| Package | `crewai[tools]>=1.12.0` |
| Python | 3.13+ |
| Environment | `.venv/` (repo-local) |
| Config | `.env` (API keys — gitignored) |
| Ephemeral | `.crewai_cache/`, `.crewai/logs/` (gitignored) |
| Output staging | `!/CREWAI/` |
| Runner | `.crewai/run_jfac.py` |

---

## Crews

### 1. JFAC Parser (Active)

**Purpose:** Structured extraction from Idaho JFAC budget / legislative artifacts.
**Status:** Active — built, awaiting first E2E run.
**Definition:** `.crewai/crews/jfac_crew.py`
**Runner:** `.crewai/run_jfac.py`

| Agent | Role | Tools | 5W |
|---|---|---|---|
| Budget Scout | Ingest minidata CSV, identify bills, agencies, scope | `minidata_reader` | WHO, WHAT |
| Legislative Tracker | Track bill progression, build timelines, check live status | `appropriations_timeline`, `bill_status_checker` | WHEN, WHERE |
| H911 Parser | Analyze bill text for policy intent (Phase 2 stub) | *(none yet)* | WHY |

| Task | Agent | Description |
|---|---|---|
| task_who | Budget Scout | Identify agencies, sponsors, committees per bill |
| task_what | Budget Scout | Analyze appropriation scope, funding type, amounts |
| task_when | Legislative Tracker | Build timeline from minidata snapshots |
| task_where | Legislative Tracker | Map current committee/chamber routing |
| task_why | H911 Parser | Preliminary intent analysis (full text Phase 2) |

**Input sources:**
- `minidata-*.csv` — dated JFAC minidata snapshots (vault root)
- `legislature.idaho.gov/sessioninfo/2026/legislation/minidata/` — live status

**Output:** `!/CREWAI/jfac-analysis-{run_id}.md`

---

### 2. Task-to-Code Bridge (Planned)

**Purpose:** Convert scoped work items (Linear issues, GitHub Issues) into implementation plans or code tasks.
**Status:** Stub — awaiting implementation.
**Definition:** `.crewai/crews/task_to_code_crew.py`

| Agent | Role | Tools |
|---|---|---|
| Task Analyst | Read work items, extract requirements and constraints | *(TBD)* |
| Plan Drafter | Generate implementation plan with files, steps, and verification | *(TBD)* |

**Input sources:** Linear issues (SWARM label), GitHub Issues (`agent:*` labels)
**Output:** `!/CREWAI/` implementation plans

---

### 3. Vault Custodian (Planned)

**Purpose:** Classify, normalize, and propose filing/metadata actions for vault materials.
**Status:** Stub — awaiting implementation.
**Definition:** `.crewai/crews/vault_custodian_crew.py`

| Agent | Role | Tools |
|---|---|---|
| Classifier | Scan vault files, propose doc_class and authority values | *(TBD)* |
| Normalizer | Check NETWEB compliance, flag path issues, propose renames | *(TBD)* |

**Input sources:** Vault filesystem scan
**Output:** `!/CREWAI/` filing proposals (Logan reviews before any moves)

---

## Tools

| Tool | File | Wraps | Used By |
|---|---|---|---|
| `minidata_reader` | `.crewai/tools/minidata_tool.py` | `normalize_budget_data.py` | JFAC Parser |
| `appropriations_timeline` | `.crewai/tools/timeline_tool.py` | `minidata_appropriations_timeline.py` | JFAC Parser |
| `bill_status_checker` | `.crewai/tools/scraper_tool.py` | `idaho_leg_scraper.py` (lightweight) | JFAC Parser |
| `address_space_writer` | `.crewai/tools/address_tool.py` | *(new)* | JFAC Parser |

---

## Evidence Trail

Every crew run must produce:
1. **Output file** in `!/CREWAI/` with vault frontmatter (title, date, authority, run_id)
2. **Console log** captured in `.crewai/logs/` (ephemeral, gitignored)
3. **Handoff record** — the output file itself documents inputs consumed and results produced

---

## See Also

- `swarm.json` — upstream machine registry (DO NOT MODIFY from CrewAI)
- `!/AGENTS.md` — human-readable agent narrative registry
- `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` — architectural directive
- `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md` — strategy document
- `!/CREWAI/HANDOFF-CREWAI-OPS.md` — operational handoff (how to run/inspect/extend)
