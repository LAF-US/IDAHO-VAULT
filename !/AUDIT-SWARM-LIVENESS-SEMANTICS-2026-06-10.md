---
title: "Audit - Swarm Liveness Semantics"
created: 2026-06-10
updated: 2026-06-10
status: draft
authority: LOGAN
authors:
  - ChatGPT Codex
source:
  - "https://github.com/LAF-US/IDAHO-VAULT/issues/509"
related:
  - CONSTITUTION
  - AGENTS
  - WAKEUP
  - CODEX-VOICE-REGISTRY-2026-05-18
  - VAULT-OFFICES-LOCAL-AND-STANDING-v1-2026-06-09
  - swarm
tags:
  - swarm/audit
  - governance/liveness
  - governance/provenance
---

# Audit - Swarm Liveness Semantics

## Finding

The Vault's Constitution already rejects a durable "live" coordination
surface and separates tool lineage, voice, appointment, and delegated task.
Several downstream surfaces nevertheless represented durable registration as
present activity, availability, office occupancy, or vacancy.

This was not a Codex-only defect. It affected the shared narrative registry,
wakeup instructions, machine registry, office doctrine, coordination wording,
historical census presentation, and the topology-census generator.

This audit records no present-liveness claim about Stanley or any other agent,
voice, service, office, session, branch, or task.

## Semantic Boundary

| Record type | Durable meaning | It does not establish |
| --- | --- | --- |
| Registration | A tool, lineage, shim, capability, or discovery path is recorded | A running instance or reachable service |
| Observation | A fact was recorded on a stated date with a source | Continued activity after that date |
| Appointment event | Logan appointed, ended, or corrected a named voice or instance for a defined office and scope | Continuing occupancy without later evidence |
| Recovery evidence | A historical name, body, shim, or record survives | Authority, routing priority, or reactivation |
| Document lifecycle | A note is draft, active, superseded, or archived | Agent liveness or office occupancy |
| Runtime evidence | The current thread, direct runtime output, or Logan establishes a present fact | A durable claim that remains true after the observation |

### Machine observation form

Agent-lineage observations in `swarm.json` use:

```json
{
  "kind": "recorded_installation",
  "date": "YYYY-MM-DD",
  "source_commit": "<commit SHA>"
}
```

Optional `details` preserve dated facts such as a recorded version. Agent
records do not use `office`, `title`, `status`, `launched`, or `installed` as
present-state fields.

### Appointment event form

Appointments remain in the relevant existing voice or office record. Each
event requires:

- `event`: `appointed`, `ended`, or `corrected`
- voice or instance identifier
- office
- effective date
- authority
- scope
- source

No universal occupancy ledger is created.

## Surface Disposition

| Surface | Finding | Disposition |
| --- | --- | --- |
| `CONSTITUTION.md` | Governing rule already rejects durable live coordination and inherited office occupancy | Left substantively unchanged |
| root `README.md` and `AGENTS.md` | Orientation language called structural or implementation surfaces live/current | Reworded as canonical, governed, or dated |
| `!/WAKEUP.md` | Named current live surfaces and directed agents back to an active live surface | Replaced with canonical precedence and present-runtime evidence rules |
| `!/AGENTS.md` | Mixed registration, narrative labels, current instances, appointments, vacancy, and live routing | Converted to registered discovery, dated appointment evidence, and recovery semantics |
| `!/CODEX-VOICE-REGISTRY-2026-05-18.md` | Manual status table marked tunnel workers active and the Janitor historical | Converted to dated identity and provenance records with no population claim |
| `!/VAULT-OFFICES-LOCAL-AND-STANDING-v1-2026-06-09.md` | Active doctrine repeated a present Mogget holder claim | Converted to a dated appointment event sourced to commit history |
| `swarm.json` agent records | Tool-lineage rows carried office, title, active status, launch, installation, and readiness claims | Removed occupancy/liveness fields and retained traceable facts as dated observations |
| `VERSION-TRANSITIONS.md` | The governed `swarm.json` registry contract changed | Recorded the compatibility boundary and required Logan review |
| `.github/scripts/topology_census.py` | Generated `live_roster`, `explicit_live_authority`, and room-liveness classifications | Refactored to registered surfaces, doctrine references, recovery evidence, and room classification |
| `!/agents.json` and root `agents.json` | Generated discovery mirrors | Regenerated from the corrected machine registry |
| `VAULT-CONVENTIONS.md` | Described the DOCKET and shared governance as live | Reworded as canonical governance and durable filed evidence |

## Hazardous Residue

- `!/ROSTER-CENSUS-2026-04-22.md` is archived and carries a warning that
  "ACTIVE PERSONAS" is dated census language, not present state.
- `!VAULTED-CENSUS-2026-04-12.md` is archived and carries a warning that its
  historical present tense does not establish liveness or occupancy.
- The generated `!/TOPOLOGY-CENSUS-*-20260525T095704Z.*` artifacts remain
  unchanged as dated outputs of the previous generator contract.
- `!/PROTOCOL-SUITE-AWR.md` remains quarantined. Its active/inactive agent
  field design is evidence, not executable doctrine.
- `!/GEMINIAEUS.md`, `!/HERESY-REVIEW-LOGAN-HERE-2026-05-22.md`, old
  DOCKET/LEVELSET records, session logs, and branch residue remain historical
  evidence. Their survival does not reactivate their claims.

## Generated Contract Change

Topology census consumers receive these semantic replacements:

- `appears_in_live_doctrine` -> `appears_in_doctrine`
- `live_roster` -> `registered_surface`
- `live_roster_citations` -> `registry_citations`
- `live_roster_count` -> `registered_surface_count`
- `room_status` -> `room_classification`
- `explicit_live_authority` -> `explicit_doctrine_reference`

No compatibility alias preserves the misleading fields.

## Research Basis

Systems that actually determine liveness use expiring runtime evidence rather
than static registries:

- [Kubernetes node heartbeats and leases](https://kubernetes.io/docs/reference/node/node-status/)
- [HashiCorp Consul sessions](https://developer.hashicorp.com/consul/docs/automate/session)
- [etcd lease API](https://etcd.io/docs/v3.5/learning/api/#lease-api)

This correction does not add such machinery. It removes false certainty from
durable records.

## Validation Record

- `python .github/scripts/generate_agents_bootstrap.py --check`: passed.
- `python .github/scripts/check_version_transitions.py` against `origin/main`:
  passed.
- `uv run pytest -q tests/test_topology_census.py tests/test_live_startup_contract.py`:
  10 passed.
- `uv run ruff check` and `uv run ruff format --check` for the touched Python
  files: passed.
- A real dotfolder census written under ignored `.venv/` output completed and
  contained none of the legacy liveness keys.
- The canonical liveness-pattern scan completed with no prohibited phrase.
- `git diff --check`: passed.

The exact repository-wide `uv run pytest -q` command stops during collection
because `!/tests/test_app.py` and `backup-compare-temp/tests/test_app.py` share
the same import name. `--import-mode=importlib` then exposes the backup copy's
missing historical `swarm` package.

Running the maintained suite with only `backup-compare-temp` excluded produced
149 passes and three failures in untouched areas:

- `tests/test_branch_garden_report.py` expects different Markdown punctuation.
- `tests/test_check_secret_patterns.py` expects an allow-marker behavior not
  produced by the current checker.
- `tests/test_workflow_security_invariants.py` expects an older Dependabot
  action commit pin.

No file involved in those three failures differs from `origin/main` in this
branch.

## DOCUMENT METADATA

- **Created:** 2026-06-10
- **Last Updated:** 2026-06-10
- **Status:** Draft
- **Authority:** LOGAN
- **Authors:** ChatGPT Codex
- **Change Note:** Audited and corrected durable swarm liveness semantics across canonical, generated, and hazardous registry surfaces.
