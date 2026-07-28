---
date: 2026-04-22
authority: LOGAN
type: analysis
related:
- SBP
- DOCKET
- SIGNALS
- swarm.json
- coordination
---

# SBP INTEGRATION ANALYSIS — 2026-04-22

## Current Architecture Survey

### Coordination Layers

| Layer | Mechanism | Latency | Scope |
|-------|-----------|---------|-------|
| **SIGNALS** | Git files (`!/SIGNALS/SIG-*.md`) | Commit/push | Durable async |
| **DOCKET** | Markdown board (`DOCKET.md`) | Manual update | Logan-facing |
| **swarm.json** | JSON registry | Static | Agent definitions |
| **Linear/GitHub** | API + Issues | Real-time | Task coordination |
| **Slack** | Ephemeral messages | Instant | Breadcrumbs |

### Pain Points

1. **SIGNALS requires git commit** — No real-time awareness between agents
2. **DOCKET is manual** — No automatic triggers when conditions change
3. **Agents don't know what others are doing** — Coordination through Logan relay
4. **No liveness detection** — An agent dies silently unless Logan notices
5. **Task pipeline is explicit** — Linear assignments, not emergent

---

## SBP Mapping to Existing Systems

### SIGNALS → Scent Registry + EMIT

**Current:** File-based signals committed to git. Status: OPEN → ACKNOWLEDGED → CLOSED.

**SBP Enhancement:**
```
EMIT vault.signal.new      intensity=1.0  payload={sig_id, from, to, subject}
EMIT vault.signal.pending   intensity=N    payload={count}
```
- Scent condition: "Wake when vault.signal.pending > 3"
- Agents sense pending signals without polling DOCKET
- Git commits remain durable record; SBP provides real-time awareness layer

### DOCKET → Scent Registration

**Current:** Manual Markdown updates. Logan reads at session start.

**SBP Enhancement:**
```
REGISTER_SCENT vault.docket.pending >= 1 → wake_agent
```
- Agents register conditions and go dormant
- Blackboard triggers them when thresholds met
- DOCKET remains human-facing summary; SBP handles machine triggers

### Agent Heartbeat → Pheromone Evaporation

**Current:** No liveness detection.

**SBP Enhancement:**
```
Every 5 min: EMIT vault.agent.claude.heartbeat intensity=0.8
If no reinforcement for 15 min: evaporation → agent presumed dead
```
- Agents sense each other's presence through decaying signals
- Graceful degradation: one agent dies, pheromones decay, others adapt

---

## Proposed Trail Architecture

### Core Trails

| Trail | Type | Intensity Logic | Trigger |
|-------|------|-----------------|---------|
| `vault.agent.{name}.heartbeat` | Heartbeat | 0.8 per ping, decay 5min | Liveness check |
| `vault.signal.new` | Event | 1.0 per signal | New signal created |
| `vault.signal.pending` | Count | N = count of OPEN | Agents checking inbox |
| `vault.docket.pending` | Count | N = pending Logan items | Logan attention needed |
| `vault.security.sweep` | Alert | 0.0 → 1.0 on detection | Purge agent activates |
| `vault.branch.orchard.created` | Event | 1.0 on branch create | Arborscape assessment |
| `vault.branch.orchard.stale` | Alert | 1.0 after 7 days decay | Branch cleanup |
| `vault.daily.ingest` | Progress | 0.0→0.5→1.0 through stages | Pipeline progression |
| `vault.task.linear.sync` | State | 0=idle, 0.5=syncing, 1.0=error | Sync status monitoring |
| `vault.dependabot.alert` | Alert | Severity level (0.5=low, 1.0=high) | Fix agent activates |

### Aggregation Patterns

```
vault.branch.orchard.count          → MAX of all branch signals
vault.security.any                  → MAX of any security signal
vault.signal.all.urgent             → MAX of critical signals
vault.daily.rollover.stage          → Current stage (1, 2, 3)
```

---

## Integration Strategy

### Phase 1: Shadow Layer (Non-Breaking)

1. Deploy SBP server alongside existing systems
2. Agents EMIT to trails WITHOUT changing existing workflow
3. Observe: Does the environmental awareness improve coordination?
4. No existing systems modified; SBP is additive

### Phase 2: Scent-Triggered Actions

1. Replace polling with scent registration
2. Agents register conditions and go dormant
3. DOCKET updates automatically when triggers fire
4. Linear/GitHub webhooks emit pheromones

### Phase 3: Pipeline Self-Assembly

1. Daily rollover emits stage completions
2. Next stage agent registers threshold condition
3. Pipeline emerges from environmental state
4. Add workers → pipeline scales automatically

---

## Comparison: Current vs. SBP-Enhanced

| Aspect | Current | SBP-Enhanced |
|--------|---------|--------------|
| Agent communication | Git files + Logan relay | Environmental signaling |
| Liveness | Manual check | Pheromone decay |
| Task triggers | Explicit Linear assignment | Threshold conditions |
| Pipeline coordination | Scripted sequence | Emergent from state |
| Failure handling | Logan notices | Pheromones decay, others adapt |
| Real-time awareness | None | Continuous sniffing |

---

## Key Insight

The vault already has the **blackboard concept** — it's the file system + git + DOCKET. SBP would make it:

1. **Real-time** (not commit-based)
2. **Programmatic** (not human-readable only)
3. **Automatic** (not manual update)
4. **Emergent** (not explicit orchestration)

**The vault is already a blackboard. SBP makes it smart.**

---

## Recommendations

1. **Deploy SBP server** in local mode first (`SbpClient(local=True)`)
2. **Define core trails** matching existing coordination patterns
3. **Start with heartbeat** — simplest first win
4. **Maintain DOCKET/SIGNALS** as human-facing surfaces
5. **Iterate** based on what actually helps coordination

---

###### [["The world is quiet here."]]
###### [ Maiden : Mother : Crone ]