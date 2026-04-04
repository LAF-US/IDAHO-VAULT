---
updated: 2026-03-25
status: active
---
# MCP IMPLEMENTATION PLAN

This plan defines a staged rollout for MCP usage in IDAHO-VAULT operations.

## Objective

Adopt MCP safely by moving from observation to constrained execution to reliable operations, while preserving governance visibility and a clear rollback path.

## Global Guardrails (all phases)

- Supervisor-visible operation: all MCP actions, findings, and exceptions are logged to governance-visible notes.
- Least privilege first: start read-only, then narrow write scope, then expand only after criteria are met.
- Reversible by default: every phase must support immediate fallback to native protocol paths.
- No silent escalation: unmet criteria or repeated errors trigger explicit stop conditions.

---


## Coordination Prerequisite (Blocking)

Before expanding MCP usage beyond discovery, `manifest.json` must be active as the shared coordination state.

Required baseline:
- `manifest.json` present at repo root
- lock protocol enabled (soft-lock v1)
- file-level entry updates on each write/read cycle

Reference: MANIFEST-SPEC

## Phase 0 — Read-only discovery

### Scope

- Enumerate available MCP resources.
- Enumerate available MCP resource templates.
- Record observed capability gaps against required workflows.

### Entry criteria

- MCP server(s) configured and reachable from the execution environment.
- A baseline list of target workflows exists for comparison (what we need MCP to do).
- A governance-visible log file/location is defined for discovery outputs.

### Required activities

- Capture resource inventory (`list_mcp_resources`) with timestamp.
- Capture template inventory (`list_mcp_resource_templates`) with timestamp.
- Map each target workflow to current MCP support status:
  - Supported now
  - Partially supported
  - Not supported
- Log capability gaps with impact and provisional mitigation.

### Exit criteria

- Resource and template inventories completed and stored.
- Capability gap register created and reviewed.
- At least one candidate write target selected for Phase 1 (example: Linear SWARM).
- No unresolved critical unknowns about authentication, access boundaries, or auditability.

### Explicit stop conditions

- MCP resources/templates cannot be reliably enumerated.
- Access boundaries are unclear or violate governance constraints.
- Discovery reveals missing auditability for actions/results.
- Any contradiction between MCP behavior and repository governance rules remains unresolved.

---

## Phase 1 — Controlled writes

### Scope

- Enable writes for exactly one target system (example: Linear SWARM).
- Use idempotency keys on every write-capable operation.
- Dry-run mode is default for all workflows; live writes require explicit opt-in per execution.

### Entry criteria

- Phase 0 exit criteria satisfied.
- Single target system approved and documented.
- Idempotency key strategy defined (generation, storage, replay behavior).
- Dry-run behavior validated for each planned write operation.

### Required activities

- Implement write wrappers with:
  - Required idempotency keys
  - Structured request/response logging
  - Dry-run default and explicit live-write flag
- Validate repeated execution does not duplicate side effects.
- Run controlled pilot scenarios (success path + known failure path).
- Document operator checklist for enabling/disabling live writes.

### Exit criteria

- Pilot completes with no unbounded side effects.
- Idempotency verified across retries/replays.
- Dry-run parity confirmed (dry-run output accurately predicts live behavior).
- Operational logs demonstrate traceability from request to result.

### Explicit stop conditions

- Any duplicate or non-idempotent write is observed.
- Dry-run/live behavior diverges in decision-relevant ways.
- Writes occur without explicit live-write enablement.
- Audit trail is incomplete for any write attempt.

---

## Phase 2 — Operationalization

### Scope

- Harden reliability and incident response for MCP-integrated workflows.
- Add retries, error taxonomy, and alerting.
- Define and validate rollback/fallback behavior to native protocol path.

### Entry criteria

- Phase 1 exit criteria satisfied.
- Error classes identified from pilot data.
- Ownership established for alerts and incident handling.
- Native protocol fallback path documented and tested.

### Required activities

- Implement retry policy by error class (transient vs permanent).
- Establish error taxonomy with standard handling actions.
- Configure alerting thresholds and escalation routes.
- Run rollback drills and fallback drills to native protocol path.
- Define service-level expectations (latency, success rate, recovery time).

### Exit criteria

- Retry behavior proven to improve reliability without unsafe side effects.
- Error taxonomy used consistently in logs and runbooks.
- Alerts are actionable (low noise, clear routing, clear severity).
- Rollback/fallback to native protocol path succeeds in test scenarios.
- Go/no-go review completed with explicit operator sign-off.

### Explicit stop conditions

- Alerting fails to notify owners for critical incidents.
- Retry logic amplifies failures or causes cascading impact.
- Fallback path cannot be executed within defined recovery targets.
- Incident handling lacks clear owner or runbook for critical error classes.

---

## Governance checkpoints by phase gate

- Gate 0 -> 1: Discovery completeness and risk acceptance review.
- Gate 1 -> 2: Controlled-write safety review and idempotency sign-off.
- Gate 2 -> Operate: Reliability and rollback readiness review.

If any gate is not passed, status remains at current phase and the implementation defaults to native protocol execution.
