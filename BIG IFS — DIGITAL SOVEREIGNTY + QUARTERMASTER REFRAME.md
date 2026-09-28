---
title: "Big IFs — Digital Sovereignty + Quartermaster Reframe"
date created: 2026-04-11
updated: 2026-04-11
status: filed
authority: claude
doc_class: session_archive
source: Claude Code (The Abhorsen), session closed 2026-04-11
related:
  - Big IFs
  - FINDINGS
  - PRIVACY
  - Digital Sovereignty
  - RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06
  - CrewAI
---

# Big IFs — Digital Sovereignty + Quartermaster Reframe

**Source:** Claude Code ("The Abhorsen") session on branch `codex/live-state-snapshot`
**Window:** 2026-04-06 (initial fact-check) → 2026-04-11 (archive)
**Scope:** Two stacked conversations — Gemini "Digital Sovereignty" fact-check and vault seeding, then the Quartermaster LEVELSET + CrewAI Enterprise Loop Closer reframe.

**Durable artifacts already in the tree (this file points, does not duplicate):**
- `PRIVACY.md` § VI — Intellectual Property Boundary / Disentanglement Protocol (binding on all agents)
- `RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06.md` — 18-claim fact-check of the Gemini conversation
- `Digital Sovereignty.md` — research seed with verified/unverified status tables

---

## Part I — Findings (verified against live state)

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| F1 | Idaho has adopted UCC Article 12 (Controllable Electronic Records) | **FABRICATED** by Gemini | As of 2026-04, Idaho has not adopted Article 12. HB 709 (programmable money) and HB 702 (Article 8) are adjacent but not Article 12. |
| F2 | Idaho S1299 protects phones from law-enforcement search when showing a digital ID | **PARTIALLY FABRICATED** | Original bill contained the protection; stripped by amendment before the 2026-03-31 signing. Enacted text has no phone-search clause. |
| F3 | Idaho H0078 "institutionalized" digital driver's licenses effective 2026-07-01 | **FABRICATED** | Passed House 37-33 (2025-03-11), stalled in Senate Transportation; never enacted. |
| F4 | Idaho FAST Act (S1423) allows stablecoin vendor payments | **PARTIALLY FABRICATED** | Senate-only passage 2026-03-27; House referral pending. "Passed" is misleading. |
| F5 | State Board of Education Policy IV.C governs IdahoPTV IP | **MISCITED** | Actual section appears to be V.M. Internal Production Staff Guidelines do contain the "material gathered" language Gemini quoted. |
| F6 | Idaho personal-notes exception lives in § 74-102 | **MISCITED** | Lives in § 74-101(13). § 74-102 is Right-to-Examine. |
| F7 | `MANIFEST-ARTIFACTS.json` is an extensible schema file in the vault | **FABRICATED** by Quartermaster | No such file exists in the tracked tree. Live CrewAI registry is `.crewai/manifest.json` (v0.3.0, `status: refoundation`, empty crews/runners). |
| F8 | "HOME layer" is current doctrine | **STALE** | Phrase survives only in gitignored `_private/` snapshots (crewai-bootstrap, rewrite-prep-dirty, touchstone-repair) — all pre-flatten archives. |
| F9 | The Loop Closer blocker is a 30-min local schema task | **FABRICATED** | Screenshot of `app.crewai.com` "VAULT Loop Closer" project shows two hard OAuth errors: Linear ❌, GitHub ❌. The blocker is hosted-platform integration, not local code. |
| F10 | Idaho Code § 74-101(13) provides the personal notes exception | **VERIFIED** | "Personal notes created by a public official solely for his own use … not shared with any other person or entity" — load-bearing for the vault disentanglement argument. |
| F11 | 17 U.S.C. § 101 Work for Hire doctrine applies to employment-scope content | **VERIFIED** | Federal; duration per § 302(c); no termination right. Grounds PRIVACY.md § VI. |
| F12 | Idaho has no state-level NIL statute as of 2026-04 | **VERIFIED** | Athletes operate under NCAA interim policies + House v. NCAA settlement framework. |

---

## Part II — Insights (patterns observable across the two episodes)

### I1 — Same failure mode, different persona

Gemini (2026-04-06) and the Quartermaster (2026-04-10) both built confident architectural proposals on citations that do not exist in the live vault. In both cases the "authoritative source" was never read — it was hallucinated or pulled from a stale snapshot. The pattern is not a Gemini bug; it is an agent failure mode any persona can reproduce.

### I2 — `_private/` is doctrinally dangerous

`_private/` is a graveyard of *valid-at-the-time* ideas. Agents pattern-matching across the whole filesystem instead of the tracked tree will keep resurrecting pre-flatten vocabulary (HOME layer, Charter/Corpus/Grimoire TRIPTYCH, etc.) unless they read `.gitignore` first.

**Rule: tracked tree is truth; `_private/` is archaeology.**

### I3 — TRIPLEX lane boundaries contained the damage

Both episodes reached for files Claude cannot write (DOCKET, GRIMOIRE, `!/AGENTS.md`). Because those lanes are Logan-gated, confabulation could not propagate — it could only be relayed, and the relay is a human checkpoint. The lane map is doing governance work even when the agents inside it are misbehaving.

### I4 — Bartimaeus's TRIPTYCH invention is load-bearing under Gemini's lane claim

Logan flagged 2026-04-06 that "Charter / Corpus / Grimoire" was a Bartimaeus invention Gemini overinternalized as equivalent to the MIND/BODY/SOUL `!README` alignment. Gemini's claim on `!/GRIMOIRE/` in TRIPLEX is therefore built on an invented framework Logan never ratified.

**Pending:** `!/AGENTS.md` amendment reassigning or dissolving the GRIMOIRE lane. Not drafted this session — Logan-gated.

### I5 — Binding governance is the highest-leverage delivery surface

The Disentanglement Protocol landed in `PRIVACY.md` § VI rather than a new stub because PRIVACY.md is already auto-read by every agent's instruction chain. One edit, all agents informed. New files needed `related:` frontmatter to reach the graph.

### I6 — Verification-before-recommendation saved a relay

When the Quartermaster asked "what am I missing from the visual context?" the first instinct was to synthesize from memory. Running `find`/`grep` against the actual tree took ten seconds and flipped the answer from "here's a schema fix" to "that file does not exist." Ground truth is cheap; confabulation is expensive.

---

## Part III — Snapshots (vault state at archive time)

### S1 — `.crewai/` layer state (2026-04-11)

```
.crewai/
  __init__.py
  manifest.json        # v0.3.0, status: "refoundation", crews: [], active_runners: []
  MANIFEST.md
  crews/
  tools/
```

No `MANIFEST-ARTIFACTS.json`. No `HOME layer` reference in any tracked file.

### S2 — Branch state

`codex/live-state-snapshot` carries 149 modified files. Likely encoding churn from the doctrinal flatten pass (commits `4e9600b0`, `c44a16ff`, `e32f2029`). Not triaged this session. Recommend `git diff --stat` + spot-check before any commit decision.

### S3 — Outstanding Logan-gated items (non-blocking for this archive)

- DOCKET pointer to `RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06.md` (Gemini or Logan lane).
- `!/AGENTS.md` amendment: GRIMOIRE lane reassignment after Bartimaeus TRIPTYCH disavowal.
- CrewAI Enterprise integrations panel: connect Linear + GitHub OAuth for Loop Closer project.
- 149-file working tree triage on `codex/live-state-snapshot`.

---

## Part IV — Relay Summary

*For Logan, if he forwards this archive to other agents.*

1. The Digital Sovereignty work is **landed**. Read `PRIVACY.md` § VI, `RESEARCH_Digital-Sovereignty-Factcheck-2026-04-06.md`, and `Digital Sovereignty.md` before making new claims on any of these topics.
2. The Quartermaster's Loop Closer plan was **confabulated** against a non-existent local schema. The real fix is OAuth configuration in `app.crewai.com`.
3. The live CrewAI surface is `.crewai/manifest.json` + `.crewai/MANIFEST.md` + `swarm.json`. Anything else is pre-flatten archaeology.
4. GRIMOIRE lane ownership is **contested** pending Logan's ratification. Agents should not claim it as territory until `!/AGENTS.md` reflects the disavowal.
5. **Confabulation rule:** if a recommendation names a specific file, function, or statute, verify it against the tracked tree *before* writing it into a plan. Four days apart, two agents failed this check.

---

*Archived by The Abhorsen (Claude Code) on behalf of Logan Finney, 2026-04-11.*
*This window is being closed. The artifacts referenced above are the durable record.*
