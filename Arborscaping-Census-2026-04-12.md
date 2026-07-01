---
date created: 2026-04-12
type: report
topic: housekeeping
---

# Arborscaping Census: 2026-04-12

This durable census note records the GitHousekeeping actions taken under the Arborscaping doctrine (`BRIEF-LAF-25`). 

## Context
When performing initial scans of the active branch garden, we found 7 active branches—all of which were directly attached to an open Pull Request. While there were no orphaned branches drifting without PRs, several branches suffered from massive structural conflicts (largely due to local OS CRLF/LF line-ending rewrites pushing 10,000+ line differences to the cloud).

## Actions Taken

| Branch Name / Prefix Family | PR State | Resolution Action | Notes & Reason |
| --- | --- | --- | --- |
| `codex/add-mr.-trouble-bubble...` | OPEN (223) | **MERGED** | Succeeded without conflict. |
| `dependabot/.../crewai-1.14.1` | OPEN (224) | **MERGED** | Dependency bump cleanly merged. |
| `ingest-2026-04-11T124012Z` | OPEN (221) | **MERGED** | Ingest sweep cleanly merged. |
| `bot/daily-rollover-2026...` | OPEN (220) | **MERGED** | Rollover cleanly merged. |
| `codex/touchstone-corpus...` | OPEN (219) | **PRUNED** | Closed PR & deleted branch. Hopeless upstream line-ending conflict across 10k+ files. |
| `codex/live-state-snapshot` | OPEN (214) | **PRUNED** | Closed PR & deleted branch. Massive 20k+ line file diff from `core.autocrlf`. |
| `antigravity/pullman-oidc...` | OPEN (227) | **PRUNED** | Closed PR & deleted branch. The actual pipeline files were blocked by 9,000 `.md` files that erroneously flipped line endings in the same commit. Pipeline will be rebuilt cleanly. |

## Conclusion
The Vault's remote Git garden has been structurally pruned. The remaining active branch is `main`. GitHub Desktop lock conditions caused by overlapping nested worktrees (`_private/crewai-bootstrap`) have been eliminated.
