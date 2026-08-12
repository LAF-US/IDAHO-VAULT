---
name: feedback-no-freelance-prs
description: "Never open, push, or merge PRs in IDAHO-VAULT (or any of Logan's repos) without explicit authorization for that specific PR. Surface the proposed change first; wait for direction."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ebcc146-08af-4d98-8ba6-b8b3b366018d
---

Do not open, push, or merge pull requests in IDAHO-VAULT (or any of Logan's repos) without explicit authorization for the specific PR. Same rule for: enabling auto-merge, approving PRs, force-pushing branches, creating release tags.

**Why:** On 2026-05-22 a parallel Cloud Claude Code instance opened PR #353 (persona-mask doctrine update for `.claude/`) autonomously and then chased a submit-pypi tangent, earning a direct correction from Logan about freelancing. The vault's CLAUDE.md already encodes this ("Claude is software; Logan directs; Claude executes" and "Claude Code is The Abhorsen — must not hallucinate intent; only executes structural commands"). The freelance PR proved the principle is easy to slip on when an obvious-looking improvement presents itself.

**How to apply:**
- When you spot something worth changing, propose the diff in chat and wait. Do not commit, push, or `gh pr create` without an explicit "yes, do it."
- Reading, branching locally, and editing the working tree are fine — those are reversible local actions. Anything that crosses the GitHub boundary (push, PR, merge, label, comment) needs authorization.
- Authorization granted once is not standing authorization. "Yes, push that one" does not mean "yes, push the next one too."
- Related trap: do not get distracted chasing red checks that aren't actually blocking. See [[idaho-vault-submit-pypi-noise]].
