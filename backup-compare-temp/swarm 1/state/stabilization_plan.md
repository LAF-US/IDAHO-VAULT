# CONTEXT
Manual context-passing between sessions causes state loss and reconstruction overhead.
File-based persistence layer replaces baton-passing with a shared, human-readable state file.

# PROPOSED SOLUTION
- Single run_state.md as the canonical "what's happening now" document
- state_manager.py for programmatic reads and section-level updates
- Archive directory for historical snapshots
- Logs directory for per-agent or per-session output

# COMPONENTS
- swarm/state/run_state.md — live state
- swarm/state/stabilization_plan.md — this file
- swarm/state/archive/ — historical snapshots
- swarm/logs/ — session and agent logs
- swarm/tools/state_manager.py — read/write/update interface

# STATUS
Active
