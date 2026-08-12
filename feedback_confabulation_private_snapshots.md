---
name: Confabulation from _private/ snapshots
description: Pattern where agents resurrect dead vocabulary or fictitious files by pattern-matching across gitignored snapshots instead of the tracked tree
type: feedback
---

When proposing architecture, schema changes, or citing "authoritative" files, read the **tracked tree only**. Do not pattern-match across the full filesystem.

**Why:** On 2026-04-10, playing the Quartermaster role, I proposed extending `MANIFEST-ARTIFACTS.json` and referenced the "HOME layer" — both confabulated. `MANIFEST-ARTIFACTS.json` has never been committed. "HOME layer" survives only in `_private/` pre-flatten snapshots (`crewai-bootstrap`, `rewrite-prep-dirty-2026-04-09`, `touchstone-repair*`), which are doctrinally dead. I also misread an `app.crewai.com` Enterprise screenshot as local `.crewai/` state, proposing JSON edits to fix what was actually an OAuth gap on a hosted web app. Logan flagged this as the same failure mode caught on Gemini four days earlier (UCC Article 12 fabrication).

**How to apply:**
- Before citing any file as authoritative, verify it exists in `git ls-files` — not just on disk.
- `_private/` is a graveyard of valid-at-the-time ideas. Treat anything found only there as superseded until proven otherwise.
- Check `.gitignore` before trusting search results that span the full working tree.
- When a screenshot shows a URL bar or chrome, read it — `app.crewai.com` is Enterprise (hosted), not local code. OAuth/integration errors there cannot be fixed by editing files in the repo.
- Live CrewAI surfaces as of 2026-04-10: `.crewai/manifest.json` (machine), `.crewai/MANIFEST.md` (doctrine), `swarm.json` (registry only, not topology). `!/CREWAI/HANDOFF-CREWAI-OPS.md` is marked historical.
- The local CrewAI slice is in `status: "refoundation"` with empty `crews` and `active_runners`. There is nothing to "extend" yet.
