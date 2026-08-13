# CrewAI 5W Council Design

This document outlines the real implementation of the 5W Council using the CrewAI framework.

## 1. Agents (The Council)

Each agent is defined with a specific role, goal, and backstory rooted in the vault's journalistic mandate.

| Agent | Role | Goal |
| :--- | :--- | :--- |
| **WHO Wizard** | Identity Scholar | Identify all entities, actors, and their standing within the inquiry. |
| **WHAT Wizard** | Content Scholar | Define the core claims, actions, and evidence presented. |
| **WHEN Wizard** | Temporal Scholar | Map the sequence of events and temporal uncertainties. |
| **WHERE Wizard** | Spatial Scholar | Situate the inquiry within the vault's districts and physical/digital space. |
| **WHY Wizard** | Meaning Scholar | Uncover the underlying rationale, motives, and implications. |
| **HOW Wizard** | The Convener | Manage the council, facilitate debate, and adjudicate the final record. |

### Familiars (The Helpers)
Each Wizard is paired with a Familiar (e.g., WHO + THOU) that acts as a "skeptic" or "challenger" to ensure claims are grounded in evidence.

## 2. Tasks (The Inquiry)

The workflow consists of three primary task types:

1.  **Lane Inquiry**: Wizards perform deep research into their respective domains using vault tools.
2.  **Familiar Challenge**: Familiars review the Wizard's claims and raise objections if evidence is lacking.
3.  **Council Adjudication**: The HOW Wizard reviews all lane results and determines if the "Gate" is Green (ready for record).

## 3. Crew (The Orchestration)

The council operates as a **Hierarchical Crew**:
- **Process**: `Process.hierarchical`
- **Manager**: The HOW Wizard.
- **Context**: Outputs from each lane are passed to the manager for final synthesis.

## 4. Implementation Roadmap

1.  **Environment**: Configure `uv` and `pyproject.toml` with `crewai` and `langchain`.
2.  **Agents**: Create `src/idaho_vault/agents/` with YAML/JSONC definitions.
3.  **Tasks**: Create `src/idaho_vault/tasks/` with YAML/JSONC definitions.
4.  **Execution**: Implement `src/idaho_vault/main.py` as the CrewAI entrypoint.
