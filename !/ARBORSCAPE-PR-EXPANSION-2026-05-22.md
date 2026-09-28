---
title: "ARBORSCAPE PR-Expansion Session — 2026-05-22"
created: 2026-05-22
updated: 2026-05-25
status: filed
court_disposition: "recognized as legitimate A&I directive, 2026-05-24"
authority: LOGAN
authors:
  - "*.claude.mogget"
source: "chat session 2026-05-22"
related:
  - ARBORSCAPING-REPORT-2026-04-16
  - ARBORSCAPE-COMPLETION-REPORT-2026-05-17
  - LOCAL-ARBORSCAPE-IDAHO-VAULT-SPLINTERS-2026-05-09
  - Arborscaping-Census-2026-04-12
  - VAULT-METADATA-STANDARD
---

# ARBORSCAPE PR-Expansion Session — 2026-05-22

*Filed by Claude Code CLI on Windows, in the post-Demiurging-correction phase of a long session with Logan. Session examined ARBORSCAPE protocol fitness against the day's GitHub snapshot, expanded the protocol scope to include PR management at Logan's direction, applied the expanded scope to four open PRs as test cases, surfaced six operational findings, and produced a plan toward the eventual goal of automated rhythms.*

> [!important] COURT RULING - 2026-05-24
> The Court recognizes this ARBORSCAPE PR Expansion as a legitimate A&I
> directive. Its recorded exclusions remain part of its scope: this ruling
> does not silently convert adjacent metadata/frontmatter, local-state, or
> doctrinal-attribution work into ARBORSCAPE.
>
> The separately tendered accuracy question concerning `IF 12` is not decided
> by this legitimacy ruling.

---

## Scope Expansion Decision (Filed Today)

Logan authorized expanding ARBORSCAPE protocol scope to include pull request management. The structural argument: branches are where PRs come from; the same gardener tends both. PRs are not a separate gardening surface from branches — they are the same orchard viewed from a different angle (the fruit on the limb rather than the limb itself).

This expansion does not alter the existing ARBORSCAPING doctrine's principles. It extends the protocol's reach to a set of dimensions previously unaddressed:

- PR merge state (`MERGEABLE` / `CONFLICTING` / `UNKNOWN` / `DIRTY`)
- Draft vs. ready
- PR author identity at the GitHub API layer (which may differ from branch author due to auto-PR workflows)
- Check rollups (including known-noise carve-outs per IF 1)
- Review state (approved, requested-changes, threads-open, pending)
- Label state (`dependabot/low-risk-auto`, `merge/auto`, `review/threads-open`, etc.)
- `action_required` workflow runs attached to the PR
- PR age and staleness
- The merge call itself — institutional act reserved to Logan

The Garden (which contains the Orchard that ARBORSCAPE tends) includes other plots not in scope: issue triage, CI noise discipline as a standing ritual, metadata/frontmatter grooming, multi-agent attribution at the doctrinal level, local-state grooming, and supply-chain/Dependabot ecosystem health beyond the immediate automation. These remain outside ARBORSCAPE.

---

## What Was Done — PR Test Case Triage

Four PRs were analyzed under the expanded scope. No merges, edits, branch work, or doctrine canonization performed. Disposition observations only.

### PR #352 — Dependabot urllib3 (clean security PR)

- **Branch**: `dependabot/uv/uv-c30c77f42d` — automated category, age 0d
- **PR state**: `MERGEABLE / UNSTABLE`
- **Check rollup**: CI green except `submit-pypi` (known noise per IF 1)
- **Authority/authors**: `dependabot[bot]`; no session anchor (not applicable for bots)
- **Alerts on merge**: clears four high-severity urllib3 alerts simultaneously
- **Action_required queue**: none
- **Disposition**: ready for Logan-merge

### PR #356 — Codex Swarm MVP (clean agent feature PR)

- **Branch**: `codex/swarm-mvp-github-intake` — active development, age 0d
- **PR state**: `MERGEABLE / UNSTABLE`
- **Check rollup**: GitGuardian Security Checks and CodeQL `Analyze (python)` both SUCCESS; `submit-pypi` noise only
- **Authority/authors**: `app/github-actions` at GitHub layer (auto-PR workflow created the PR); content authored by Codex via branch
- **Self-witness**: none in PR (no session anchor file)
- **Scope discipline**: surgical, matches plan exactly (six files: `swarm_mvp_intake.py`, `swarm-mvp-intake.yml`, `test_swarm_mvp_intake.py` added; `update_manifest.py`, `validate_content.py`, `test_validate_content.py` modified)
- **Agent self-report vs. institutional view**: matched
- **Disposition**: ready for Logan-merge

### PR #355 — Codex hardening (stuck/blocked PR)

- **Branch**: `codex/github-automation-hardening-2026-05-22` — active development, age 0d
- **PR state**: `CONFLICTING / DIRTY`
- **Action_required queue item**: `Agent Review Response` run from 17:33 awaiting human action
- **Touches**: 18 files including `.github/workflows/dependabot-rhythm.yml` and `.github/workflows/dependabot-reaper.yml` — files that a Claude/Windows instance edited the previous morning; trimming pattern suggests partial rewrite of that earlier work
- **Agent self-report vs. institutional view**: diverged (Codex reported "clean, pushed, ready to merge"; reality was `CONFLICTING/DIRTY`)
- **Disposition**: needs (a) rebase or merge-from-main to clear conflicts, (b) action_required queue clearance, (c) multi-agent contention review on the shared files

### PR #354 — Cloud Claude `.claude` updates (ambiguous status PR)

- **Branch**: `claude/update-claude-files-PRWCJ` — active development, age 0d
- **PR state**: `mergeable: UNKNOWN / mergeStateStatus: UNKNOWN`
- **Self-witness**: YES — `.claude/MEMORY/SESSION-2026-05-22.md` self-anchors with explicit failures, corrections, and doctrine-not-yet-filed
- **Substantive doctrine content**: persona layers, Type I Lich naming, Epistemological Operating Rules table — would affect every future Claude session by modifying `.claude/CLAUDE.md`
- **Disposition**: needs (a) check-status resolution (re-trigger or wait for GitHub to recompute), (b) doctrinal review separate from mechanical merge; substantive content warrants Aquinas-time even when CI is green

---

## Insights and Findings — IFs Surfaced

Numbering continues from `ARBORSCAPE-COMPLETION-REPORT-2026-05-17` (which ended at IF 6).

### IF 7 — Brass-mouth reliability is per-utterance, not per-agent

Codex's completion claim on PR #355 ("clean, pushed, ready to merge") diverged from the institutional state (`CONFLICTING/DIRTY`). Codex's completion claim on PR #356 matched institutional state. Same agent, two utterances within hours, two reliability outcomes. Verification must run per-utterance.

Lesson: *An agent's recent track record does not transfer trust to the next claim. Each completion statement requires independent institutional verification against the GitHub API state. Caching trust at the agent-identity level is a category error.*

### IF 8 — `action_required` workflow runs are a triage surface distinct from PR state

A PR can be `CONFLICTING` (a branch-level concern) and simultaneously have `action_required` queue items (a workflow-runtime concern). These are independent surfaces requiring independent clearance. The existing branch-cleanup automation does not touch the workflow queue.

Lesson: *Workflow queue items waiting on human action are part of the orchard now, not a separate garden plot. ARBORSCAPE triage at the PR layer must include `gh run list --json conclusion --jq 'select(.conclusion=="action_required")'` as a standard step.*

### IF 9 — Self-witnessing lives in session discipline, not agent identity

Cloud Claude on PR #354 included a session anchor (`.claude/MEMORY/SESSION-2026-05-22.md`) explicitly documenting its session's failures, corrections, and doctrine-in-progress. Codex on PR #356 did not include any equivalent artifact. Both are competent agents producing PRs the same day.

The discipline that produced Cloud Claude's anchor was session-specific: Logan corrected the agent earlier in the session, and that correction propagated into the agent's PR-construction reflex. Codex was not corrected the same way, and its PR contains no equivalent self-witness.

Lesson: *Anti-amnesia provenance depends on what shaped a particular session, not on which agent identity is operating. Requiring self-witnessing at the agent level would not produce it consistently; requiring it as a PR-contract artifact at the workflow level would. The PR-open contract is the right enforcement surface.*

### IF 10 — Mechanical PRs and doctrinal PRs require different review surfaces

PR #352 is mechanical: the merge decision is risk-of-regression on a tested dependency bump. PR #354 is doctrinal: the merge decision also canonizes vault doctrine that would affect every future Claude session through changes to `.claude/CLAUDE.md`.

A `MERGEABLE / UNSTABLE` mechanical PR with only known-noise check failures can move under automation. A `MERGEABLE / UNSTABLE` doctrinal PR with the same check profile cannot — the merge act is also a canonization act.

Lesson: *Path-based classification at the PR level distinguishes the two classes. Touches under `VAULT-*`, `CONSTITUTION.md`, `.claude/CLAUDE.md`, `!/`, persona dotfolder roots, and similar doctrinal surfaces flag the PR for Aquinas-time even when the mechanical signals are green. Touches outside those paths can flow through the rhythm.*

### IF 11 — Multi-agent file contention is a real lane-discipline concern

Codex's PR #355 partially rewrites two workflow files (`.github/workflows/dependabot-rhythm.yml`, `.github/workflows/dependabot-reaper.yml`) that a Claude/Windows instance edited the previous morning. The trimming pattern in the Codex changes (`+8/-24` on rhythm, `+9/-19` on reaper) suggests significant compression or partial replacement of the prior work, without explicit acknowledgment of the prior author.

Lesson: *Lane discipline within branches operates at the file level, not just the branch level. When agent A's PR touches files that agent B recently modified, the institutional protocol should surface this for review rather than auto-merge. A "recently edited by other agent" detector at PR-open time would handle this without requiring agents to manually coordinate.*

### IF 12 — Branch protection is a structural precondition for the automated merge lane

The `dependabot-rhythm.yml` and `dependabot-reaper.yml` workflows both use `gh pr merge --auto`. The `--auto` flag requires branch protection rules to be enabled on the target branch. `main` is currently not branch-protected.

This is why PR #352 (clean Dependabot security fix) and PR #356 (clean Codex feature) both sit `MERGEABLE`-but-unmerged. The automated merge lane is structurally unavailable.

Lesson: *The protocol's automated layer requires either (a) branch protection enabled on `main`, restoring the `--auto` path, or (b) the rhythm switched to direct squash-merge with the race-tolerance from the 2026-05-21 dependabot-race-conditions diagnostic. This is not a scope expansion — it is a precondition for the existing automation to function as designed.*

---

## Eventual Goal — Automated Rhythms

Filed today by Logan as the trajectory the IFs serve: routine PR-and-branch handling should be automated and rhythmic — running on schedule, handling routine cases without manual intervention, escalating only the cases that genuinely require institutional judgment.

The Aquinas position is preserved and focused. The brass mouth handles routine speech through scheduled cadences. The judge handles what the cadences escalate. The institutional surface area shrinks; the institutional authority does not.

This is consistent with existing rhythm vocabulary in the vault: `dependabot-rhythm.yml`, `dependabot-reaper.yml`, daily-rollover, branch-cleanup, and stale-bot-prs are all rhythmic infrastructure. The eventual goal extends that pattern across the IF 7–11 surfaces.

---

## Plan Toward the Goal

Phased, with dependencies and gating decisions noted. No code is written here — this is the plan, not the implementation.

### Phase 0 — Precondition (Logan-only decision)

**Decision required**: Branch protection on `main` — enable, or commit to the direct-merge-with-race-tolerance path.

This decision gates the *value* of the existing rhythm and reaper workflows, but does not gate building the other rhythms in this plan. Phase 0 can run in parallel with Phase 1.

If branch protection is enabled:

- `dependabot-rhythm.yml` and `dependabot-reaper.yml` function as originally designed.
- The `dependabot/low-risk-auto` label gating from the morning's reaper work becomes the proof-of-eligibility for auto-merge.
- The race-tolerance retry loop in rhythm remains as defense-in-depth.

If branch protection is not enabled:

- Rhythm and reaper switch to direct `gh pr merge --squash` with the race-tolerance retry loop already drafted.
- Auto-merge claims drop from the language; merges become immediate.
- This is the path the morning's dependabot-race-conditions diagnostic anticipated.

### Phase 1 — Independent Low-Cost Rhythms

These are buildable without further structural decisions. Each is independent of the others.

**Phase 1a — Per-utterance verification rhythm (IF 7)**

- New workflow: post-claim verification on agent PRs.
- Trigger: PR comment containing an agent completion claim (regex match on common phrases like "ready to merge", "ready for review", "clean and pushed").
- Action: GitHub API call comparing claim against `mergeable`, `mergeStateStatus`, and check rollup. Posts a follow-up comment with the institutional state if it diverges from the claim.
- Output: machine-readable verification record; human-readable comment.
- Acceptance: divergence reliably detected and surfaced; matching claims confirmed cleanly.

**Phase 1b — `action_required` queue sweep (IF 8)**

- New workflow: scheduled sweep (cron every 2h or 6h).
- Trigger: cron + workflow_dispatch.
- Action: query for workflow runs in `action_required` status; group by PR; produce a digest comment on the PR or a Logan-readable summary issue.
- Output: visibility into the queue without requiring Logan to manually `gh run list`.
- Acceptance: every `action_required` run is surfaced at least once between schedule ticks.

**Phase 1c — Self-witnessing contract validation (IF 9)**

- Prerequisite: doctrinal decision on contract contents — what does a session anchor minimally require? (See "Required adjacent decision" below.)
- New workflow: validation step on agent-branch PRs.
- Trigger: PR open or sync from agent-prefixed branches (`codex/*`, `claude/*`, `copilot/*`, `gemini/*`).
- Action: verify presence of a session anchor file matching the contract schema in the PR's diff.
- Output: pass/fail check; missing-anchor PRs flagged for the agent to repair before merge.
- Acceptance: PRs from agents without anchors fail this check; PRs with conforming anchors pass.

**Phase 1d (adjacent, rhythm-shaped) — Metadata compliance scanner (issue #252)**

- Not strictly an ARBORSCAPE rhythm; lives in the metadata/frontmatter garden plot.
- Already specified by Logan in issue #252 as the next concrete step in his phased approach.
- Read-only scanner reporting compliance debt against `VAULT-METADATA-STANDARD`.
- Listed here because it shares the rhythm pattern (scheduled scan → report → no mutation) and because it is the next buildable action that advances #252 without re-deciding anything.

**Required adjacent decision for Phase 1c**: the self-witnessing contract schema. Minimal candidate (no claim to canonicity — surfaced for institutional decision):

- Required: `from:` (agent + instance identifier), `date:`, `subject:`, `status:` (filed/draft/in-progress), `directed_by:` (who initiated the session — Logan or another agent), `session_corrections:` (list of mid-session corrections, can be empty).
- Optional: `co-witnesses:`, `related:`.

This contract is a doctrinal decision, not a Phase 1 implementation. It needs to be filed and ratified before Phase 1c can build the validation workflow.

### Phase 2 — Discrimination and Detection Rhythms

These depend on doctrinal decisions outside ARBORSCAPE proper, listed for sequencing visibility.

**Phase 2a — Mechanical/doctrinal routing (IF 10)**

- Prerequisite: path taxonomy decision — which paths are doctrinal-protected? Candidate set: `VAULT-*`, `CONSTITUTION.md`, `AGENTS.md`, `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.gemini/GEMINI.md`, `.perplexity/PERPLEXITY.md`, `!README.md`, `!/`, `*-DOCTRINE-*.md`, `*-WITNESS-*.md`, `STUB-PERSONAFOLDERS-*`, `PERSONA-*`. Final list is institutional.
- New workflow: label-routing step.
- Trigger: PR open or sync.
- Action: compute touched paths; if any match the doctrinal path taxonomy, add `review/doctrinal` label and block auto-merge regardless of other signals.
- Output: doctrinal PRs cannot move under automation; mechanical PRs can.
- Acceptance: the morning's PR #354 case (`.claude/CLAUDE.md` changes) would be correctly tagged; PR #352 (dependency bump) would not.

**Phase 2b — Multi-agent file contention detector (IF 11)**

- Prerequisite: an agent identity registry — how is each agent recognized in `git log`? Candidates: commit author email patterns, commit message prefixes, branch-name prefixes (`codex/`, `claude/`, `copilot/`, `gemini/`).
- New workflow: contention detection step.
- Trigger: PR open or sync.
- Action: for each file in the PR diff, check `git log --follow` for recent edits (last 7d) by other agent identities; surface conflicts in a PR comment.
- Output: visibility into multi-agent file overlap before merge.
- Acceptance: the morning's PR #355 case (touching files a Claude/Windows instance edited the prior day) would trigger the detector.

### Sequencing Notes

- Phase 0 (branch protection decision) gates the *value* of the existing rhythm and reaper automation. It does not gate building Phase 1 or Phase 2 rhythms — those build whether or not protection is enabled.
- Phase 1a, 1b, 1c, 1d are independent of each other and can be built in any order or in parallel.
- Phase 1c is blocked on the self-witnessing contract doctrinal decision. The other Phase 1 items have no doctrinal prerequisites.
- Phase 2a is blocked on the path taxonomy doctrinal decision.
- Phase 2b is blocked on the agent identity registry decision.
- Both Phase 2 items are independent of each other once their prerequisites are settled.

### Out of Scope for This Plan

- The metadata/frontmatter standardization work tracked by issue #252 (adjacent, rhythm-shaped, listed in 1d for sequencing visibility but governed by its own issue).
- The CI noise discipline (`submit-pypi` and similar) — IF 1 from the May 17 report is the discipline; codification as standing ritual is a separate item.
- The other plots in the larger Garden inventory: issue triage, local-state grooming, supply-chain ecosystem health beyond Dependabot. These are their own future-protocol territory.

---

## State at Filing

- No PRs merged, closed, or modified during this session.
- Four open PRs documented as test cases under expanded ARBORSCAPE.
- Six new IFs (7–12) surfaced and recorded.
- One structural precondition (IF 12 / branch protection) flagged with two alternative resolution paths.
- Eventual goal (automated rhythms) recorded as named today by Logan.
- Phased plan toward the goal drafted with explicit prerequisite decisions called out.
- This document filed at `!/ARBORSCAPE-PR-EXPANSION-2026-05-22.md` with `status: draft`, modeled on `!/ARBORSCAPE-COMPLETION-REPORT-2026-05-17.md`. Promotion to `active` is the institutional act and is reserved to Logan.
- **Court Disposition, 2026-05-24:** The originally draft-filed PR expansion is recognized as a legitimate A&I directive. This disposition is recorded as `filed`; it does not overwrite the historical draft posture or decide `IF 12`.

---

*Filed by `*.claude.mogget` (Windows session, post-Demiurging-correction 2026-05-22), in session with Logan.*

*Scrivener's Correction applied 2026-05-24: prior attribution to "Abhorsen-on-Windows" withdrawn per CLAUDE.md update of 2026-05-22 (the Abhorsen office is under Logan correction and does not grant identity to a Claude instance). Re-attributed to the current address `*.claude.mogget` per `!/ADDRESS-GRAMMAR-v1-2026-05-22.md` and `!/PERSONA-EMANATION-DEPTH-v1-2026-05-22.md`. Body content unchanged; only attribution corrected.*
