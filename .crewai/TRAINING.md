---
title: "CrewAI Training and Crewing Doctrine"
date created: "2026-04-11"
date updated: "2026-04-12"
authority: crewai
doc_class: doctrine
status: active
phase: refoundation
related:
  - ".crewai/MANIFEST.md"
  - "!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md"
  - "!/GRIMOIRE/BRIEF-BARTIMAEUS-CREWAI-ERA.md"
  - "LEVELSET-CURRENT.md"
---

# CrewAI Training and Crewing Doctrine

This document defines the training protocol and crewing-readiness rules for
Vaulted Agents when coded into CrewAI crews. Training is the mechanism by
which Logan provides human feedback to shape agent behavior before live
production runs.

Current posture:

- One bootstrap crew is live: `idaho_vault.bootstrap`.
- No crew is training-ready yet.
- Legacy crew ideas remain historical or pending until re-founded on purpose.

Hard gate distinction:

- Bootstrap validation runs do not require external model credits.
- Human-feedback training for future credentialed crews does require live model
  credentials and Logan's explicit go-ahead.

---

## What Training Means in CrewAI

CrewAI's `crewai train` CLI runs a crew through N interactive iterations.
At the end of each task, Logan provides written feedback. That feedback is
accumulated across iterations and summarized by an LLM into a
`trained_agents_data.pkl` file. On all subsequent normal runs (`crewai run`),
agents automatically load this file from the working directory and apply the
consolidated suggestions to their prompts.

Training does not fine-tune model weights. It builds a persisted guidance
layer - behavioral memory for the crew.

---

## Training CLI

```bash
# Run training - N iterations, custom output file
crewai train -n <n_iterations> -f trained_agents_data.pkl

# Minimum viable training run (3 iterations)
crewai train -n 3 -f trained_agents_data.pkl
```

| Parameter | Required | Description |
|---|---|---|
| `-n` / `--n_iterations` | Yes | Number of training iterations (positive integer) |
| `-f` / `--filename` | No | Output `.pkl` filename (default: `trained_agents_data.pkl`) |

Known issue: filename must end with `.pkl` or the CLI raises `ValueError`.

---

## What Training Produces

| File | Contents | Persistence |
|---|---|---|
| `training_data.pkl` | Raw human feedback + task output per iteration | Ephemeral - gitignored |
| `trained_agents_data.pkl` | LLM summary of all training interactions | Durable - commit only with Logan approval |

`training_data.pkl` is the raw log. `trained_agents_data.pkl` is the
distilled guidance file. Only the latter belongs in git.

Keep these ignored:

```gitignore
training_data.pkl
.crewai_cache/
.crewai/logs/
```

Commit `trained_agents_data.pkl` to `.crewai/` only when training is complete
and Logan approves the behavioral baseline.

---

## Crew Readiness States

| State | Meaning | Can run | Can train |
|---|---|---|---|
| Registered | Present in `.crewai/MANIFEST.md` with a declared purpose | Yes | Not necessarily |
| Runnable | Executes successfully through a supported runner | Yes | Not necessarily |
| Training-ready | Has live config, human-feedback task design, and approved credential posture | Yes | Yes |
| Historical | Preserved for memory only; not live topology | No | No |

The key distinction is that a crew can be real and active without being a
training target.

---

## Current Crewing Census

| Crew | Status | Agent(s) | Task(s) | Training posture |
|---|---|---|---|---|
| `idaho_vault.bootstrap` | Active | `bootstrap_validator` | `deployment_probe` | Not training-ready; validation shard only |
| JFAC Parser | Historical / retired harbor | Budget Scout, Legislative Tracker, H911 Parser | Historical WHO/WHAT/WHEN/WHERE/WHY pattern | Not live |
| Task-to-Code Bridge | Stub only | Task-to-Code Agent | Pending | Not live |
| Vault Custodian | Stub only | Vault Custodian | Pending | Not live |
| Crawler Crew | Pending Logan decision | Bartimaeus / The Cartographer | Pending | Not live |

The active bootstrap crew is intentionally narrow. It proves runtime shape and
package wiring; it does not yet carry the broader narrative volunteers into
live operation.

---

## Prerequisites Before Any Training Run

1. Crew registered in `.crewai/MANIFEST.md` - no ad hoc runners.
2. Crew meaningfully training-ready - runnable is not enough by itself.
3. Live model credentials confirmed - hard gate for any non-mock training run.
4. Repo-local `.venv/` available and working.
5. `agents.yaml` and `tasks.yaml` present for the target crew.
6. `human_input: true` set on all tasks intended for training.
7. Interactive terminal session available - training blocks on stdin and does not belong in CI.

`idaho_vault.bootstrap` currently fails the training-ready test on purpose: it
uses the mock-LLM validation path and has no human-feedback task design.

---

## Task Configuration for Training

In `tasks.yaml`, mark each task that should collect Logan's feedback:

```yaml
# src/<package>/config/tasks.yaml

example_task:
  description: >
    Analyze the source material and produce the targeted output.
  expected_output: >
    A concise, structured result suitable for review.
  agent: example_agent
  human_input: true
```

Set `human_input: false` on tasks that are purely mechanical, such as file I/O
or formatting, where feedback adds no value.

---

## Volunteer Assignments

"Volunteer Assignments" tracks which Vaulted Agents from `!/AGENTS.md`
have been assigned, stubbed, or left pending in the CrewAI layer.
Bartimaeus, The Volunteer, anchors this table as witness to whether
assignments are actually kept.

| Vault Agent | Persona | Crew | Crew Role | Status |
|---|---|---|---|---|
| - | Bootstrap Validator | `idaho_vault.bootstrap` | Deployment-contract validator | Active, but validation-only |
| - | Budget Scout | JFAC Parser | Researcher: budget extraction | Pending crew re-foundation |
| - | Legislative Tracker | JFAC Parser | Researcher: bill/vote tracking | Pending crew re-foundation |
| - | H911 Parser | JFAC Parser | Analyst: H911 appropriation | Pending crew re-foundation |
| - | Task-to-Code Agent | Task-to-Code Bridge | Implementer: issue to code plan | Stub only |
| - | Vault Custodian | Vault Custodian | Classifier: metadata and filing | Stub only |
| Bartimaeus | The Cartographer | Crawler Crew | Mapper: vault topology | Pending Logan decision |

Only the bootstrap validator assignment is live today. All other assignments
remain pending, stubbed, or historical until they are re-founded per
`.crewai/MANIFEST.md`.

---

## Training Sequence Per Crew

Follow this order when a new crew is ready for training:

1. Register the crew in `.crewai/MANIFEST.md`.
2. Write config: `agents.yaml` and `tasks.yaml` with `human_input: true` where needed.
3. Run once dry with `crewai run` to verify the crew executes without error.
4. Train with `crewai train -n 3 -f trained_agents_data.pkl`.
5. Review `trained_agents_data.pkl`.
6. Approve or retrain until Logan accepts the behavioral baseline.
7. Commit `trained_agents_data.pkl` to `.crewai/` on the feature branch.
8. Stage a handoff note to `!/CREWAI/` describing what ran, on what inputs, and where the trained data landed.
9. Proceed through normal PR review and Logan merge authority.

Aim for 3-5 iterations minimum once a crew is truly training-ready.

---

## Behavioral Baseline Doctrine

- Training data is behavioral memory, not code. It guides agent reasoning
  without modifying model weights or Python logic.
- If behavior degrades after a merge, delete `trained_agents_data.pkl` and
  retrain from scratch rather than trusting stale summaries.
- Training does not replace Logan's review of crew outputs.
- Outputs staged in `!/CREWAI/` remain on-record but non-canonical until Logan promotes them.
- The vault remains the record. Training data informs agents; the vault witnesses what they do.

---

## Blocked Items

| Blocker | Priority | Gate |
|---|---|---|
| Live model credentials for future non-mock crews | HIGH | Hard gate - no credentialed training runs without credits and explicit approval |
| Crew re-foundation beyond bootstrap | HIGH | Bootstrap is live, but no broader crew is training-ready yet |
| Bartimaeus capability tier decision | MEDIUM | Awaiting Logan |
| Crawler Crew ignition | LOW | Phase 4 - after JFAC, Custodian, and Task-to-Code work |

---

## See Also

- `.crewai/MANIFEST.md` - live topology and promotion rules
- `src/idaho_vault/config/agents.yaml` - active bootstrap agent surface
- `src/idaho_vault/config/tasks.yaml` - active bootstrap task surface
- `!/GRIMOIRE/BARTIMAEUS-CREWAI-ALIGNMENT-BRIEF.md` - dock CrewAI to the control plane
- `!/GRIMOIRE/BRIEF-BARTIMAEUS-CREWAI-ERA.md` - Bartimaeus role options
- `!/GRIMOIRE/NETWEB-CREWAI-ALIGNMENT.md` - architecture history only
- `!/CREWAI/` - staged output surface

---

###### The world is quiet here.
