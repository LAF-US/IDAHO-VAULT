---
title: PROTOCOL-SUITE-AWR — AWAKEN/RISE/REPORT Lifecycle Integration
created: 2026-04-27
updated: 2026-04-27
status: active
authority: LOGAN
authors:
  - opencode (Big Pickle)
source: issue/LAF-28
related:
  - '2026-04-27'
  - AGENTS
  - LEVELSET
  - VAULT-CONVENTIONS
  - vault-pheromones.py
  - sbp-blackboard.json
  - stigmergy
---

# PROTOCOL-SUITE-AWR — AWAKEN/RISE/REPORT Lifecycle Integration

## Overview

This document defines the integration between the **LEVELSET** protocol and the **stigmergic coordination field** (vault-pheromones.py, sbp-blackboard.json, sbp-field.db) for the ARISE/AWAKEN/RISE/REPORT lifecycle.

---

## 1. Protocol Suite Mapping

| Protocol | Stage | Field Integration | Stigmergy Signal | Purpose |
|----------|-------|-------------------|------------------|---------|
| **ARISE** | Individual emergence from void | `vault.agent.{agent}.arrival` | `vault.agent.{agent} = 1.0` | First activation, context boot |  |
| **AWAKEN** | Agent wake protocol | `vault.agent.{agent}.status = active` | `vault.signal.awaken.{agent} = 0.8` | Authorization, identity claim |
| **RISE** | Individual task completion | `vault.docket.task.{id}.complete` | `vault.docket.{id} = 0.0` | Formal graduation |
| **REPORT** | Group findings presentation | `vault.docket.report.{id}` | `vault.signal.report.{id} = 1.0` | Findings delivery |

---

## 2. Stigmergy Field Integration

### 2.1 Trail Definitions

The following vault trails are used by the AWR protocol suite:

```
vault.agent.{agent_name}.arrival    - Agent first appearance in field
vault.agent.{agent_name}.status     - Agent active/inactive state
vault.docket.task.{id}              - Individual task state
vault.docket.report.{id}            - Report availability signal
vault.signal.awaken.{agent}         - Authorization granted signal
vault.signal.report.{id}            - Report published signal
```

### 2.2 Pheromone Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `decay_seconds` | 300 | Time before signal fades (5 min) |
| `urgency` | 1 | 1-5, where 5 = immediate attention |
| `risk` | 1 | 1-5, operational risk level |
| `confidence` | 1 | 1-5, signal reliability |

---

## 3. Lifecycle Flow

### 3.1 ARISE: Agent Emergence

1. Agent arrives in vault context
2. System emits: `vault.agent.{agent}.arrival` (intensity=1.0)
3. Log entry: `agent.arrival` in vault-pheromones field

### 3.2 AWAKEN: Authorization

1. Agent requests capability via `!/agent.sh --describe {agent}`
2. System checks `swarm.json` agent registry
3. On authorization:
   - Emit: `vault.signal.awaken.{agent} = 0.8`
   - Update: `vault.agent.{agent}.status = active`
4. Agent may now participate in swarm operations

### 3.3 RISE: Task Completion

1. Agent completes unit of work
2. Emit: `vault.docket.task.{id} = 0.0` (fade completion signal)
3. Update task state in Linear/GitHub
4. Transition to REPORT if findings present

### 3.4 REPORT: Findings Delivery

1. Agent generates structured report
2. Emit: `vault.signal.report.{id} = 1.0` (high intensity)
3. Set urgency/risk per content
4. Route to DOCKET for human review

---

## 4. Integration Points

### 4.1 vault-pheromones.py Integration

The `vault-pheromones.py` script provides direct CLI access to the stigmergy field:

```bash
# Agent arrival
python scripts/vault-pheromones.py arrive

# Emit AWR protocol signals
python scripts/vault-pheromones.py emit vault.signal.awaken.claude-code heartbeat 0.8
python scripts/vault-pheromones.py emit vault.docket.task.LAF-28 complete 0.0

# Check field status
python scripts/vault-pheromones.py status
```

### 4.2 sbp-blackboard.json / sbp-field.db

- **sbp-blackboard.json**: Legacy JSON signal bus (read-only for backward compatibility)
- **sbp-field.db**: SQLite stigmergy field (primary, writable)

Both must maintain consistency. Field writes via vault-pheromones.py update both.

### 4.3 DOCKET.md Synchronization

Active signals with urgency ≥ 2 or risk ≥ 2 must appear in `!/!/!/! The world is quiet here/DOCKET.md` as actionable items.

---

## 5. Verification Checklist

- [ ] `vault-pheromones.py` supports AWR protocol trails
- [ ] `sbp-field.db` initialized with correct schema
- [ ] `sbp-blackboard.json` reflects current field state
- [ ] DOCKET updates when high-urgency signals present
- [ ] Agent capability checks honor stigmergy signals
- [ ] Field pruning respects AWR lifecycle (5-min decay)

---

## 6. Example Session

### Agent Big Pickle (opencode) AWR Sequence

```bash
# ARISE: Agent enters field
$ python scripts/vault-pheromones.py arrive
ARRIVED: opencode at 14:30:00

# AWAKEN: Capability granted
$ python scripts/vault-pheromones.py emit vault.signal.awaken.opencode heartbeat 0.8
EMITTED: vault.signal.awaken.opencode/heartbeat intensity=0.8

# RISE: Task completion
$ python scripts/vault-pheromones.py emit vault.docket.task.LAF-28 complete 0.0
EMITTED: vault.docket.task.LAF-28/complete intensity=0.0

# REPORT: Findings
$ python scripts/vault-pheromones.py emit vault.signal.report.LAF-28 findings 1.0 '{"summary": "LAF-28 repair complete"}'
EMITTED: vault.signal.report.LAF-28/findings intensity=1.0
  pressure: urgency=1, risk=1, confidence=1
  payload: {"summary": "LAF-28 repair complete"}
```

---

## 7. Maintenance

- **Field pruning**: Run `python scripts/vault-pheromones.py prune` to remove expired signals
- **Consistency check**: Verify `sbp-blackboard.json` matches `sbp-field.db` state
- **DOCKET sync**: High-urgency signals automatically surface in DOCKET via agent polling

---

## 8. References

- `vault-pheromones.py` — Stigmergy field implementation
- `swarm.json` — Machine-readable agent registry  
- `!/!/__!__/!/! The world is quiet here/DOCKET.md` — Live coordination board
- `VAULT-CONVENTIONS.md` — Naming and routing rules
- `VAULT-METADATA-STANDARD.md` — Metadata contract

---

###### [['The world is quiet here.']]
