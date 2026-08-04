Problem: the PR automation and chamber hygiene work is partially repaired but not yet stable. The self-healing review loop is in place, but the active auto-PR workflow still fast-fails due to invalid YAML, chamber dotfolders were being hidden by wholesale ignore rules, and several remaining GitHub checks still need truth-based triage.

Approach:
- finish the structural repair first: valid workflow syntax and durable chamber visibility
- keep repo-owned dotfolders visible while ignoring only volatile runtime/auth/cache subpaths
- re-derive current GitHub Actions truth from live runs rather than assuming older failure causes still apply
- treat the SBP/blackboard work as stigmergic coordination infrastructure, not an isolated script experiment

Completed:
- hardened auto-PR failure behavior so PR creation errors are not silent
- tightened Linear sync trust boundaries for secret-backed side effects
- added scheduled/open-PR reconciliation behavior and regression coverage
- cleared and merged the prior open PR queue
- preserved orchard-sweep salvage inside the vault
- verified SBP Phase 1 blackboard access
- traced the current auto-PR fast-fail to invalid YAML in `.github/workflows/agent-auto-pr.yml`
- removed wholesale dotfolder ignores and replaced them with granular runtime-path ignores

Next steps:
- repair `.github/workflows/agent-auto-pr.yml` so GitHub parses it as a real workflow again
- finish dotfolder ignore refinement so chamber docs stay visible and runtime debris stays ignored
- inspect the remaining red checks on current `main`, especially CodeQL and dependency submission
- resolve the daily-note carryforward failure against current backlog truth

Notes:
- GitHub topic `stigmergy` is a strong conceptual fit for the vault’s pheromone/blackboard direction; relevant public repos cluster around environment-mediated coordination, shared memory, and cross-session agent repair.
- Current work should preserve that framing: the repo is converging on stigmergic coordination surfaces rather than purely event-driven automation.
