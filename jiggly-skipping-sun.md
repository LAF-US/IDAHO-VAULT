# Plan: Quartermaster Reframe — Hosted CrewAI, Not Local Schema

## Context

Two conversations have stacked on this plan file. The Digital Sovereignty fact-check from 2026-04-06 is already landed (PRIVACY.md § VI, `RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06.md`, `Digital Sovereignty.md`). That work is **complete** — the only outstanding items from it are Logan-gated (DOCKET pointer, GRIMOIRE lane reassignment).

The live question is from the Quartermaster (2026-04-10): *"What key assumptions am I making that are incorrect?"* — asked after sharing a screenshot of CrewAI Enterprise and a LEVELSET that proposed extending `MANIFEST-ARTIFACTS.json` with a HOME-layer schema inside a "30-minute implementation task."

## Ground Truth (verified 2026-04-10)

| Claim | Reality |
|---|---|
| `MANIFEST-ARTIFACTS.json` exists | **FALSE.** No such file anywhere in the repo. Not in `.crewai/`, not at root, not in `!/CREWAI/`. |
| "HOME layer" is a live doctrinal concept | **FALSE.** The phrase only appears in gitignored `_private/` snapshots (crewai-bootstrap, rewrite-prep-dirty, touchstone-repair) — all pre-flatten archives. It is not in current governance. |
| CrewAI local scaffold is the blocker | **FALSE.** `.crewai/manifest.json` reports `status: refoundation`, `active_runners: []`, `crews: []`. The local layer is a disposable runtime slice, already acknowledged as a re-foundation. |
| 30-minute schema task will unblock Loop Closer | **FALSE.** Screenshot shows CrewAI **Enterprise** (`app.crewai.com`) with two hard errors: ❌ Linear integration not connected, ❌ GitHub integration not connected. No schema change fixes an OAuth gap on a hosted platform. |

The canonical CrewAI surfaces:
- `.crewai/manifest.json` — machine-readable layer registry (v0.3.0)
- `.crewai/MANIFEST.md` — human doctrine
- `!/CREWAI/` — output staging (HANDOFF-CREWAI-OPS.md marked `status: historical`)
- `swarm.json` — registers the layer; does NOT own topology

## The Quartermaster's Misread

The Quartermaster is pattern-matching from a pre-flatten snapshot they found in `_private/`, then designing local architecture (`MANIFEST-ARTIFACTS.json` extension, HOME-layer artifact tracking, session-coherence semantics) to solve a problem that does not live in local code. This is the same failure mode as the Gemini/UCC-Article-12 episode four days ago: a confident invented framework built on a citation that does not exist in the current vault.

**The actual Loop Closer blocker is platform configuration:**
1. CrewAI Enterprise project "VAULT Loop Closer" exists (Sequential; two agents on gpt-4o-mini).
2. Linear OAuth is not connected → agent cannot read LAF-16, LAF-23, LAF-36.
3. GitHub OAuth is not connected → agent cannot walk branches or close issues.
4. Until both are connected in `app.crewai.com` integration settings, no local file edit moves the needle.

## Answer to Relay to the Quartermaster

1. **You're designing against a file that does not exist.** `MANIFEST-ARTIFACTS.json` is not in the repo. Search confirmed.
2. **"HOME layer" is pre-flatten vocabulary.** It survives only in gitignored `_private/` archives. Current doctrine is `.crewai/MANIFEST.md` + `swarm.json`.
3. **Local schema is not the blocker.** The screenshot shows hosted-platform OAuth gaps (Linear ❌, GitHub ❌). Those are fixed in CrewAI Enterprise settings, not in the vault.
4. **Before re-planning, read the live surfaces:** `.crewai/manifest.json`, `.crewai/MANIFEST.md`, `!/CREWAI/README.md`, `swarm.json`. If they contradict the mental model, trust the files.
5. **The 30-minute task should be:** open `app.crewai.com` → VAULT Loop Closer project → Integrations → connect Linear (workspace scope) and GitHub (repo scope on `loganfinney27/IDAHO-VAULT`). Nothing to commit.

## Pending Items (unchanged — not this turn's work)

- **GRIMOIRE lane reassignment** — Bartimaeus's TRIPTYCH invention gave Gemini claim on GRIMOIRE territory Logan considers illegitimate. Requires `!/AGENTS.md` amendment; Logan-gated; not drafted.
- **DOCKET pointer** to `RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06.md` — Gemini or Logan lane per TRIPLEX.
- **149-file working tree triage** on `codex/live-state-snapshot` — likely encoding churn from the doctrinal flatten; worth a `git diff --stat` pass before any commit, but not this plan's scope.

## Verification

- `ls .crewai/` → shows `__init__.py`, `crews/`, `tools/`, `manifest.json`, `MANIFEST.md`. No MANIFEST-ARTIFACTS.json. ✅
- `grep -rli "MANIFEST-ARTIFACTS"` at tracked paths → zero hits. ✅
- `grep -rli "HOME layer"` at tracked paths → zero hits; only `_private/` snapshots. ✅
- `.crewai/manifest.json` → `status: refoundation`, empty `crews`/`runners`. ✅

## What This Plan Does Not Do

- Does not edit `.crewai/manifest.json`, `swarm.json`, `!/CREWAI/`, or any CrewAI doctrine file.
- Does not touch DOCKET, GRIMOIRE, or `!/AGENTS.md` (lane-gated).
- Does not authenticate anything on `app.crewai.com` (Logan-gated — OAuth consent is a human-in-the-loop action).
- Does not commit the 149 modified files on `codex/live-state-snapshot`.
- Does not start a podcast.

## Next Step After Approval

Deliver the relay answer above to the Quartermaster persona as text. No file writes. Logan decides whether to (a) forward the answer verbatim, (b) open CrewAI Enterprise and wire the OAuth connections, or (c) re-scope the Loop Closer crew against the real `.crewai/MANIFEST.md` surface.
