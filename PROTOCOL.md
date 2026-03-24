---
tags:
  - administration/protocol
updated: 2026-03-24
status: draft
---
# Agentic Swarm Administrative Levelsetting Protocol (STUB)

**Supervisor:** [[LOGAN]]
**Status:** Draft / Awaiting formalization
**Purpose:** Define operational semantics for multi-instance coordination within the agentic swarm

---

## OPERATIONAL CONTEXT

[[LOGAN]] is building an agentic swarm to manage:
- **Personal media consumption tracking** (movies, TV, books, academic journals, live performances)
- **Professional/institutional content tracking** (Idaho Reports/Idaho PTV archive metadata)
- **File management and knowledge organization** across heterogeneous data sources

Instances must coordinate reliably across tasks without ambiguity. This document defines core operational and observational terminology.

---

## TERM DEFINITIONS (STUB)

### DATA OPERATIONS

| Term | Definition (DRAFT) | Use Case | Notes |
|------|---|---|---|
| **HYDRATE** | Enrich existing data structure with additional fields/metadata from external sources | Filling in missing fields on partially-loaded records | Assumes data structure already exists; non-destructive |
| **INGEST** | First-time acquisition and loading of data into system | Initial import from APIs, RSS feeds, exports | Creates new records or replaces non-existent ones |
| **DESTROY** | Permanent, irrevocable deletion of data | End-of-lifecycle data removal; privacy compliance | No recovery possible; audit trail required |
| **DELETE** | Soft removal; data may be recoverable or archived | User-requested removal; temporary exclusions | Recoverability depends on implementation |
| **SUNSET** | Scheduled deactivation or expiration of data/service | Deprecation of stale metadata; time-bound records | Planned, non-emergency removal; may include transition period |

### OBSERVATIONAL/MONITORING ACTIONS

| Term | Definition (DRAFT) | Use Case | Notes |
|------|---|---|---|
| **NOTICE** | Passive observation of event/state; may be ephemeral | Logging transient occurrences; monitoring system health | Does not require explicit storage; can be signal-level only |
| **NOTE** | Active recording of observation; explicit storage | Documenting decisions, anomalies, findings | Implies persistent record; should be retrievable |
| **LOOK** | Direct visual/structural inspection of a single entity | Examining record structure, error logs, data format | Typically on-demand; short-lived query |
| **WATCH** | Continuous or repeated monitoring of entity/stream | Tracking data quality over time; system performance | Implies sustained attention; may trigger alerts |
| **LISTEN** | Passive reception of events/messages; monitoring for specific signals | Event stream monitoring; queue/feed polling | Typically async; threshold-triggered |

### INFORMATION-SEEKING & ADVISORY ACTIONS

| Term | Definition (DRAFT) | Use Case | Notes |
|------|---|---|---|
| **SEARCH** | Active querying against defined data source (API, index, store) | Looking up specific data; filtering large datasets | Assumes destination is known; may return zero results |
| **FIND** | Successful resolution of search; location/identity of target confirmed | Confirming data exists and is accessible | Often used as completion state of SEARCH |
| **CONSULT** | Querying a knowledge source or advisory instance for information/guidance | Asking another agent for context; checking documentation | May return partial/uncertain results; advisory in nature |
| **ADVISE** | Providing recommendation, analysis, or guidance based on available context | Offering decision support; flagging risks/opportunities | Implies assessment of data; opinion-forward |

### COORDINATION & HANDOFF ACTIONS

| Term | Definition (DRAFT) | Use Case | Notes |
|------|---|---|---|
| **FLAG** | Mark entity/task/finding for attention by supervisor or another instance | Raising priority issues; marking anomalies; escalating decisions | Should include severity/urgency indicator and reasoning |
| **HANDOFF** | Transfer responsibility for task/data to another instance with full context | Delegating work across the swarm; task completion | Must include sufficient context; receiving instance should ACKNOWLEDGE |
| **HANDSHAKE** | Formal acknowledgment of handoff receipt; confirmation of context completeness | Closing coordination loop; ensuring no dropped context | Implies both parties have aligned understanding |
| **CONTEXTUALIZE** | Package information with sufficient background for receiving instance to act independently | Preparing data for HANDOFF; enriching flagged items | Balance: avoid over-documentation while ensuring sufficiency |

---

## AMBIGUITIES TO RESOLVE

### Overlaps & Clarifications Needed

1. **CONSULT vs. ADVISE**
   - CONSULT = information-seeking (asking for data/guidance)
   - ADVISE = recommendation-providing (giving assessment/opinion)
   - Should these be strictly separated, or is CONSULT→ADVISE a natural flow?

2. **SEARCH vs. FIND vs. CONSULT**
   - SEARCH = querying a known data source
   - FIND = successful SEARCH outcome
   - CONSULT = querying knowledge/advisory source (less certain outcome)
   - Need clarity on when to use CONSULT vs. SEARCH

3. **DELETE vs. DESTROY vs. SUNSET**
   - Durability profiles: DELETE (soft) → SUNSET (scheduled) → DESTROY (permanent)?
   - Should there be audit trail requirements for each?
   - Recovery windows?

4. **NOTICE vs. NOTE**
   - Is NOTICE purely signal-level (no storage requirement)?
   - Does NOTE always imply a retrievable log entry?
   - What's the boundary between ephemeral and persistent?

5. **HYDRATE vs. INGEST**
   - Is HYDRATE restricted to enrichment of *existing* structures?
   - Can INGEST create partial records, or must it be complete?
   - When should an instance choose one over the other?

6. **WATCH vs. LISTEN**
   - WATCH = continuous active monitoring (pulling)?
   - LISTEN = passive reception (event-driven)?
   - Or both can be either?

---

## IMPLEMENTATION NOTES

### Context Sufficiency for CONTEXTUALIZE
When preparing data for HANDOFF, instances should include:
- **What** was observed/actioned
- **Why** it matters (relevance to swarm goals)
- **When** (timestamp; recency)
- **Confidence level** (high/medium/low/uncertain)
- **Next steps** (what receiving instance should do)
- **Caveats** (limitations, missing data, assumptions)

### Compact Mapping: Coordination Terms → Execution Requirements

| Term | MCP operation(s) / event | Required payload fields | Required metadata (all mappings) |
|---|---|---|---|
| **HANDOFF** | `mcp.handoff.create` (primary), optional `mcp.handoff.update` for amendments | `handoff_id`, `subject`, `task_scope`, `context_packet`, `requested_action`, `due_by`, `attachments[]` | `timestamp`, `source_agent`, `destination`, `confidence`, `durable_record_location` |
| **HANDSHAKE** | `mcp.handoff.acknowledge` event against existing `handoff_id` | `handoff_id`, `ack_status` (`received`/`incomplete`), `context_completeness`, `acceptance_decision`, `follow_up_required` | `timestamp`, `source_agent`, `destination`, `confidence`, `durable_record_location` |
| **CONTEXTUALIZE** | `mcp.context.package` prior to HANDOFF/FLAG; optional `mcp.context.validate` | `context_packet_id`, `objective`, `background`, `current_state`, `evidence_refs[]`, `constraints`, `assumptions`, `next_actions` | `timestamp`, `source_agent`, `destination`, `confidence`, `durable_record_location` |
| **FLAG** | `mcp.flag.raise` (primary), optional `mcp.flag.resolve` | `flag_id`, `severity`, `summary`, `impact`, `routing_destination`, `requested_decision`, `blocking_status`, `supporting_refs[]` | `timestamp`, `source_agent`, `destination`, `confidence`, `durable_record_location` |

#### CONTEXTUALIZE Minimum Context Schema

```yaml
context_packet:
  context_packet_id: string
  objective: string
  background: string
  current_state: string
  evidence_refs: [string]
  constraints: [string]
  assumptions: [string]
  next_actions: [string]
  metadata:
    timestamp: ISO-8601 datetime
    source_agent: string
    destination: string
    confidence: high|medium|low|uncertain
    durable_record_location: vault-relative path
```

#### FLAG Severity Enum and Routing Destination

```yaml
flag:
  severity: CRITICAL|HIGH|MEDIUM|LOW|ADMIN
  routing_destination:
    - LOGAN (default)
    - named_agent (only via LOGAN relay)
```

### FLAG Severity Levels (PROPOSED)
- **CRITICAL** — Decision required; blocks downstream work of Logan or agents
- **HIGH** — Pattern/anomaly detected; surface concerns to Logan for his will
- **MEDIUM** — Informational; document context for later and continue
- **LOW** — Logged; no action required
- ADMIN — Unified Systems management

### Audit & Logging
- DESTROY, DELETE, SUNSET operations require audit trail
- FLAG operations should reference their source/reasoning
- HANDOFF should be logged with context snapshot

---

## NEXT STEPS FOR FORMALIZATION

1. **Resolve ambiguities** (see section above)
2. **Add severity/urgency scales** for FLAG operations
3. **Define HANDSHAKE protocol** (acknowledgment format, timeout, retry logic)
4. **Specify audit logging requirements** per operation type
5. **Create decision trees** for ambiguous cases (e.g., when to DELETE vs. SUNSET)
6. **Add examples** for each term in realistic swarm contexts
7. **Version control** this protocol; log changes as swarm evolves

---

## DOCUMENT METADATA

- **Revised:** 2026-03-24
- **Revision:** [[LOGAN]]
- **Status:** Stub / Awaiting expansion
- **Authority:** [[LOGAN]]'s discretion

###### [["The world is quiet here."]]
