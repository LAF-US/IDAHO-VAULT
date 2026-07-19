---
title: "Prefix-free routing — retire the drifting agent allowlist"
date created: 2026-07-19
updated: 2026-07-19
status: draft
doc_class: report
authority: "proposed; Logan inscribes. Authority NOT assumed as LOGAN — the finding and diff are my reading (`[mapping]`), the file:line anchors are witnessed (`[fact]`)."
witness: "!roman.claude.* — praenomen conferred by Logan; office '*' held, ungranted."
session: "https://claude.ai/code/session_01Fipj4vEJ5ADPuunn9ed5Hd"
related:
  - "[[REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22]]"
  - "[[DRY-AND-WET-CODING-WITNESS-2026-07-01]]"
  - "[[ATOMIZE-DONT-ACCRETE-2026-06-28]]"
  - "[[VAULT-CONVENTIONS]]"
tags: [report, automation/auto-merge, agent/coordination, drift, single-source-of-truth, no-verdict]
---

# Prefix-free routing — retire the drifting agent allowlist

*Proposed increment, drafted at Logan's direction ("Y — be aware of prior art and notes").
The finding: the routing gate that decides **whether a branch is classified and PR'd** is a
hand-maintained agent-prefix allowlist, copied across surfaces that have **drifted**. Logan's
tell: `serena/*` sitting in the list proves a hardcoded prefix list is the wrong design.*

## The drift, witnessed — `[fact]`

Same conceptual set — "which branches are automation" — maintained by hand in ≥2 live places, already out of sync:

| Surface | prefixes listed |
|---|---|
| `.github/workflows/agent-auto-pr.yml:35` (pre-change) | claude codex gemini copilot perplexity grok **serena** |
| `.github/workflows/branch-cleanup.yml:31–41` & `:66` | claude codex gemini copilot perplexity grok **bot** **serena** ingest- wayback-audit- topology-census- |
| historical (BIG-PICKLE session) | claude codex gemini copilot perplexity **bigpickle** serena bot — *(no grok)* |

- `bot/` is in `branch-cleanup` but was **absent** from `agent-auto-pr` — the same set, two copies, diverged.
- `serena/*` is **dead weight** in every live list: per `swarm.json → agents[]`, Serena is a memory/MCP substrate (`dotfolder: .serena`, "does not assert present availability"), **not** a branch author. No workflow creates `serena/*` branches.
- The list **mutates by hand over time**: `bigpickle/` came and went; `grok/` was added later. Every change is N manual edits that fall out of step.
- `dependabot/*` and `github-actions[bot]` are in **none** of them — which is *precisely why* they needed their own arming lanes.

## Prior art it sits inside — `[mapping]`

- **`REPORT-GH-AUTOMERGE-ENFORCEMENT-MAP-2026-06-22` — K1/K2.** Risk is "computed three times, three ways… they can drift independently," and "the classifier already knows what the path lists re-check… the depth axis *should* be the single source of truth." This allowlist is the **same anti-pattern one level up**: the gate deciding *whether* the classifier runs is itself a drifting hand list. The map frames the fix as **"deliberate, staged work, not a Gordian cut,"** and holds **"whether the sync-bot lane folds into the unified model or stays a separate contract"** as a Logan-reserved decision.
- **`DRY-AND-WET-CODING-WITNESS-2026-07-01`.** "Single-source the fact." The allowlist is one fact (the automation-namespace set) copied into places that drift — accidental WET, the `DOCKET-POSTURE` failure again.
- **`ATOMIZE-DONT-ACCRETE-2026-06-28`.** Don't add another list; read before you produce.

## The fix — increment 1 (this draft) — `[mapping]`

Gate on the **form**, not an enumerated set. Per `VAULT-CONVENTIONS § Git Practices`, work branches are `<namespace>/<description>`; ephemeral automation artifacts are dash-prefixed (`ingest-`, `wayback-audit-`, `topology-census-`). So a **slash-namespaced branch (`*/*`)** is the signal — self-maintaining, no enumeration:

- `agent-auto-pr.yml`: the `claude/*|…|serena/*` case list → `*/*`. Adding an agent needs no edit; `serena/*` dead weight vanishes; `dependabot/*` is admitted **by construction** — "one among the many."

Also in this draft, correcting a prior error of mine:

- **Reverted** the deletion of `dependabot-rhythm.yml`. That deletion (in the earlier #854 commit) rested on a **falsified premise** — "the lane arms but never enqueues" — but `auto-merge-enqueue-on-checks.yml` supplies the enqueue **centrally** on *Cross-Platform Smoke* completion, so an arm-only lane is by design, not broken. And the lane's fate is a **held, Logan-reserved** decision per the map. Deleting it was doubly wrong.
- **Retained** the independently-correct `labeled`-trigger fix on `auto-merge-engage.yml` (the real #720 fix).

## Held — do not cut unbidden — `[mapping]`

1. **Sync-bot / Dependabot lane fate** — reserved to Logan (per the map). Increment 1 makes the *producer gate* prefix-free; it does **not** retire any lane.
2. **`branch-cleanup.yml`'s parallel prefix list** — untouched here. It gates **branch deletion** (destructive); broadening it is its own reviewable increment, not a side effect.
3. **Universalizing classification** — increment 1 only partly reaches self-opening bot PRs (Dependabot opens its own PR; `agent-auto-pr` classifies only when it wins the create/open race). Full "one among the many" = a `pull_request_target:[opened]` classify-on-open pass that stamps the label pair on **every** PR regardless of author. That belongs in the same staged pass that decides K1/K2 and the lane fate — held.

## Provenance

- **`[fact]`** — file:line anchors read from the branch this session; the drift table.
- **`[mapping]`** — the fix, the staging, the prior-art correspondences: my reading, ruled by no one here.

`!roman.claude.*` — office held, not claimed. Claude Code, session `…01Fipj4vEJ5ADPuunn9ed5Hd`. I propose; Logan inscribes.

###### [["The world is quiet here."]]
