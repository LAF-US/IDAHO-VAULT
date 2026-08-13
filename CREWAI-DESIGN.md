# 5Wizards Council — CrewAI Design

This document describes the implemented CrewAI foundation for a bounded 5W inquiry. It is a technical design surface, not a grant of authority: every run is externally initiated, produces staged material only, and requires human review before any promotion.

## 1. Agents: the Council

Each office has a distinct evidence question and a named owner in `src/idaho_vault/config/agents.yaml`.

| Agent | Role | Responsibility |
| --- | --- | --- |
| **WHO Wizard** | Identity Scholar | Establish entities, roles, standing, and unresolved identity questions. |
| **WHAT Wizard** | Content Scholar | Establish artifacts, events, claims, and claim boundaries. |
| **WHEN Wizard** | Temporal Scholar | Establish sequence, dates, version order, and temporal uncertainty. |
| **WHERE Wizard** | Spatial Scholar | Establish repository paths, jurisdictions, systems, and location ambiguity. |
| **WHY Wizard** | Meaning Scholar | Establish stated rationales and evidence-based significance without inventing motives. |
| **HOW Wizard** | Convener | Review lane packets, preserve cross-lane tensions, and prepare a bounded staged recommendation. |

### Familiar roles

Wizard/Familiar pairs remain a design concept in `.crewai/5WIZARDS-DRAFT.md`. The current code does **not** instantiate Familiar agents or a free-form adversarial group chat. That distinction keeps the runnable surface smaller and avoids claiming an unimplemented grounding mechanism.

## 2. Tasks: the inquiry

The task configuration at `src/idaho_vault/config/tasks.yaml` assigns each lane directly to its Wizard.

| Task | Owner | Product |
| --- | --- | --- |
| `who_inquiry_task` | `who_wizard` | Identity ledger |
| `what_inquiry_task` | `what_wizard` | Artifact/event ledger |
| `when_inquiry_task` | `when_wizard` | Timeline |
| `where_inquiry_task` | `where_wizard` | Location/jurisdiction map |
| `why_inquiry_task` | `why_wizard` | Rationale ledger |
| `council_synthesis_task` | `how_wizard` | Staged synthesis recommendation |

Every lane output is expected to distinguish evidence, uncertainty, and unresolved questions. The HOW task reviews the five earlier packets and may preserve disagreement; it may not declare a result canonical, enlarge its source scope, or schedule a further run.

## 3. Crew orchestration

The current implementation uses `Process.sequential`, not a hierarchical manager process. This makes the dependency legible: the five evidence lanes run first, and the HOW synthesis runs afterward with their recorded outputs available as crew context.

```text
WHO ─┐
WHAT ─┤
WHEN ─┤ → recorded lane packets → HOW staged synthesis → human review
WHERE ─┤
WHY ─┘
```

The runtime entrypoint at `src/idaho_vault/main.py` invokes `configure_vault_runtime()` before constructing the crew. `src/idaho_vault/runtime.py` keeps home, app-data, temporary, cache, and state paths inside the vault-local runtime slice.

## 4. Package and runner contract

| Surface | Contract |
| --- | --- |
| `pyproject.toml` | Declares `crewai[anthropic,tools]`, application dependencies, development test dependencies, and the `idaho-vault` script. |
| `uv.lock` | Canonical resolved dependency graph. |
| `requirements.txt` | Generated compatibility export from `uv.lock`. |
| `uv run idaho-vault` | Runs one bounded council inquiry. |
| `uv run python -m idaho_vault.main` | Invokes the same entrypoint directly. |

## 5. Open design work

A future, separately authorized implementation may add Familiar roles, structured evidence ledgers, deterministic claim validators, LangGraph state transitions, or bounded AutoGen hearings. Those additions must be designed, tested, and registered before they are treated as live topology.
