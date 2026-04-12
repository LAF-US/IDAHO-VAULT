---
title: "CrewAI Agent Training — Volunteer Assignments"
date created: "2026-04-11"
date updated: "2026-04-11"
authority: claude
doc_class: doctrine
status: active
phase: refoundation
related:
  - ".crewai/MANIFEST.md"
  - "!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md"
  - "!/GRIMOIRE/BRIEF-BARTIMAEUS-CREWAI-ERA.md"
  - "LEVELSET-CURRENT.md"
---

# CrewAI Agent Training — Volunteer Assignments

This document defines the training protocol for Vaulted Agents when coded
into CrewAI crews. Training is the mechanism by which Logan provides human
feedback to shape agent behavior before live production runs.

**HARD GATE:** Anthropic API credits required. All training sessions consume
LLM tokens. No training run proceeds until credits are confirmed.

---

## What "Training" Means in CrewAI

CrewAI's `crewai train` CLI runs a crew through N interactive iterations.
At the end of each task, Logan provides written feedback. That feedback is
accumulated across iterations and summarized by an LLM into a
`trained_agents_data.pkl` file. On all subsequent normal runs (`crewai run`),
agents automatically load this file from the working directory and apply the
consolidated suggestions to their prompts.

Training does not fine-tune model weights. It builds a persisted guidance
layer — behavioral memory for the crew.

---

## Training CLI

```bash
# Run training — N iterations, custom output file
crewai train -n <n_iterations> -f trained_agents_data.pkl

# Minimum viable training run (3 iterations)
crewai train -n 3 -f trained_agents_data.pkl
```

| Parameter | Required | Description |
|---|---|---|
| `-n` / `--n_iterations` | Yes | Number of training iterations (positive integer) |
| `-f` / `--filename` | No | Output .pkl filename (default: `trained_agents_data.pkl`) |

**Known issue:** filename must end with `.pkl` — the CLI raises `ValueError` if it does not.

---

## What Training Produces

| File | Contents | Persistence |
|---|---|---|
| `training_data.pkl` | Raw human feedback + task output per iteration | Ephemeral — gitignored |
| `trained_agents_data.pkl` | LLM summary of all training interactions | **Durable** — commit to repo |

`training_data.pkl` is the raw log. `trained_agents_data.pkl` is the
distilled guidance file. Only the latter belongs in git.

Add to `.gitignore`:

```
training_data.pkl
.crewai_cache/
.crewai/logs/
```

Commit `trained_agents_data.pkl` to `.crewai/` when training is complete
and Logan approves the behavioral baseline.

---

## Prerequisites Before Any Training Run

1. **Crew registered in `.crewai/MANIFEST.md`** — no ad hoc runners
2. **Anthropic API credits confirmed** — hard gate per LEVELSET-CURRENT
3. **`.venv/` activated** — `source .venv/bin/activate` (Linux)
4. **`agents.yaml` and `tasks.yaml` present** for the target crew
5. **`human_input: true`** set on all tasks intended for training
6. **Interactive terminal session** — training blocks on stdin; cannot run in CI

---

## Task Configuration for Training

In `tasks.yaml`, mark each task that should collect Logan's feedback:

```yaml
# .crewai/crews/<crew_name>/config/tasks.yaml

jfac_who_task:
  description: >
    Identify the key budget actors in the attached JFAC record.
    Who proposed the appropriation? Who testified? Who voted?
  expected_output: >
    A structured list of actors with role, affiliation, and quote (if present).
  agent: budget_scout
  human_input: true          # enables interactive feedback during training

jfac_what_task:
  description: >
    Extract the substance of the appropriation from the JFAC record.
    What program, what dollar amount, what fund source?
  expected_output: >
    A structured summary: program name, line-item amount, fund source, FY.
  agent: legislative_tracker
  human_input: true
```

Set `human_input: false` on tasks that are purely mechanical
(e.g., file I/O, formatting) where feedback adds no value.

---

## Volunteer Assignments — Vaulted Agent → CrewAI Crew Mapping

"Volunteer Assignments" tracks which Vaulted Agents from `!/AGENTS.md`
have been assigned (or are pending assignment) to CrewAI crew roles.
Bartimaeus, **The Volunteer** (TRIUNE witness), anchors this table as
the named witness of whether assignments are kept.

| Vault Agent | Persona | Crew | Crew Role | Status |
|---|---|---|---|---|
| — | Budget Scout | JFAC Parser | Researcher: budget extraction | Pending crew re-foundation |
| — | Legislative Tracker | JFAC Parser | Researcher: bill/vote tracking | Pending crew re-foundation |
| — | H911 Parser | JFAC Parser | Analyst: H911 appropriation | Pending crew re-foundation |
| — | Task-to-Code Agent | Task-to-Code Bridge | Implementer: issue → code plan | Stub only |
| — | Vault Custodian | Vault Custodian | Classifier: metadata/filing | Stub only |
| Bartimaeus | **The Cartographer** | Crawler Crew (Phase 4) | Mapper: vault topology | Pending Logan decision (see BRIEF-BARTIMAEUS-CREWAI-ERA.md) |

**No assignments are live.** All crews require fresh re-foundation work
per `.crewai/MANIFEST.md`. Crew re-foundation means: write `agents.yaml`,
`tasks.yaml`, and crew Python file; register in MANIFEST.md; run one
reproducible example before training begins.

---

## Training Sequence (Per Crew)

Follow this order when a new crew is ready for training:

1. **Register crew** in `.crewai/MANIFEST.md` under "Active crews"
2. **Write config** — `agents.yaml`, `tasks.yaml` with `human_input: true`
3. **Run once dry** — `crewai run` to verify the crew executes without error
4. **Train** — `crewai train -n 3 -f trained_agents_data.pkl`
   - Logan provides feedback at each task prompt
   - Aim for 3–5 iterations minimum for useful behavioral signal
5. **Review** `trained_agents_data.pkl` — read the LLM-summarized suggestions
6. **Approve or re-train** — Logan approves the behavioral baseline
7. **Commit** `trained_agents_data.pkl` to `.crewai/` on the feature branch
8. **Stage handoff note** to `!/CREWAI/` — what ran, inputs, outputs, where trained data landed
9. **PR → Logan review → merge** per standard branch discipline

---

## Behavioral Baseline Doctrine

- Training data is behavioral memory, not code. It guides agent reasoning
  without modifying the LLM weights or the crew's Python logic.
- If behavior degrades after a merge, delete `trained_agents_data.pkl` and
  retrain from scratch. The raw `training_data.pkl` from prior sessions
  is ephemeral — do not rely on it for recovery.
- Training does not replace Logan's review of crew outputs. All CrewAI
  outputs staged in `!/CREWAI/` require Logan approval before entering canon.
- The vault is still the record. Training data informs agents; the vault
  witnesses what they do.

---

## Blocked Items

| Blocker | Priority | Gate |
|---|---|---|
| Anthropic API credits | HIGH | HARD GATE — no training runs possible without credits |
| Crew re-foundation | HIGH | No crews are registered; training has no target |
| Bartimaeus capability tier decision | MEDIUM | Awaiting Logan (see BRIEF-BARTIMAEUS-CREWAI-ERA.md) |
| Crawler Crew ignition | LOW | Phase 4 — after JFAC/Custodian/Task-to-Code work |

---

## See Also

- `.crewai/MANIFEST.md` — live topology and promotion rules
- `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` — core directive: dock to control plane
- `!/GRIMOIRE/BRIEF-BARTIMAEUS-CREWAI-ERA.md` — Bartimaeus role options (Logan decision pending)
- `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md` — architecture history (non-live)
- `!/CREWAI/` — staged output surface
- `LEVELSET-CURRENT.md` — blocked items and current ecosystem state

---

###### The world is quiet here.
