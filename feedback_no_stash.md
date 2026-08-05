---
name: feedback-no-stash
description: Do not use git stash as a workflow step — agents have lost work this way
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b5790ba0-a224-4bd6-9606-9f61a7e0f755
---

Logan is wary of `git stash` because other agents have stashed important work and then abandoned it or failed to pop it, losing the work in a recoverable-but-forgotten local state.

**Why:** Stash is local-only, invisible to other agents, and easy to lose track of across sessions. A crashed or interrupted session leaves the stash sitting silently.

**How to apply:** When local uncommitted changes need to coexist with a pull, commit the work-in-progress first (WIP commit is fine), then pull/rebase, then amend or clean up the commit. Never use `git stash` as a workflow step. If stash is the only option in an edge case, flag it explicitly to Logan before proceeding.
