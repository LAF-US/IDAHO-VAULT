---
title: "PROTOCOL-STATUS-CONFERENCE — Pre-Trial Gate for BETA TESTING and AGENT TRIALS"
updated: 2026-04-06
status: draft
authority: LOGAN
related:
- AGENT-PROTOCOL
- AGENTS
- CONSTITUTION
- DECISIONS
- DOCKET
- FLAG
- LEVELSET
- PROTOCOL
- TRIUNE
- VAULT-CONVENTIONS
- agent
- beta
- coordination
- gate
- protocol
- trial
---

# PROTOCOL: STATUS CONFERENCE
## *The Gate Before the Trial*

**Status:** DRAFT — awaiting Logan's review and adoption
**Proposed by:** GitHub Copilot (The Clerk) — 2026-04-06
**Authority:** Subordinate to CONSTITUTION. Extends AGENT-PROTOCOL and PROTOCOL.md.

---

> *"In law, no one goes to trial unprepared. The status conference exists so that the courtroom is never surprised."*

---

## I. SOURCE: THE LEGAL CONCEPT

In civil and criminal court procedure, a **status conference** is a scheduled pre-trial meeting between the judge and parties. It happens *after* a case is filed but *before* trial begins. Its purpose:

| Function | What It Resolves |
|---|---|
| Readiness check | Are all parties prepared to proceed? |
| Issue identification | What procedural disputes must be settled first? |
| Scope agreement | What will actually be litigated? |
| Evidence inventory | What exhibits, witnesses, and records are available? |
| Timeline | What is the schedule from here to verdict? |
| Stop conditions | What would cause the trial to be postponed or dismissed? |

The status conference is not the trial. It is the **gate** that determines whether the trial proceeds, and on what terms.

**Key principle:** *No trial without a status conference.* The court does not convene until readiness is confirmed.

---

## II. APPLICATION TO IDAHO-VAULT

THE COURTROOM is already named in THE DOCKET:

> *"Any agent arriving at THE COURTROOM reads this file to orient."*

The vault already operates with courtroom logic:
- Logan is the principal — the judge
- Agents are parties and officers of the court
- The DOCKET is the case management board
- LEVELSET is the state record
- DECISIONS.md is the verdict ledger
- AGENT TRIALS are when a new agent or crew runs for the first time under live conditions
- BETA TESTING is when a new workflow, script, or capability is exercised before full deployment

What is missing is the **status conference gate** — a structured pre-flight review that must be completed *before* any AGENT TRIAL or BETA TEST begins.

---

## III. THE STATUS CONFERENCE PROTOCOL

A STATUS CONFERENCE must be held before:

1. **AGENT TRIAL** — activating a new agent persona for the first time; giving an advisory agent direct-write access for the first time; onboarding any new agent into the vault.
2. **BETA TEST** — running a new automation script (workflow, Python tool, crew) in a live environment for the first time; deploying a new CI pipeline job; activating a new CrewAI crew in production mode

> **Exception:** Read-only discovery, dry-run executions with `--dry-run` flag, and stub/placeholder activations do not require a formal STATUS CONFERENCE. They are pre-conference reconnaissance.

---

## IV. THE CHECKLIST

A STATUS CONFERENCE is complete when all items below are answered in writing before the trial begins.

### A. Identity & Scope

- [ ] What is the name of the agent, crew, or system being trialed?
- [ ] What is the declared scope of this trial? (What will it do? What will it NOT do?)
- [ ] What Linear issue or GitHub issue tracks this trial? (Required. No trial without a ticket.)
- [ ] Which vault lane does this agent/system own? (Per the agent registry in `!/AGENTS.md`)

### B. Readiness

- [ ] Has the agent's bootstrap record been verified in `swarm.json`?
- [ ] Is the required context bundle present and readable?
- [ ] Have all dependencies been confirmed available (API keys, secrets, filesystem access)?
- [ ] Has a COLLISION CHECK been run against existing workflows? (Per PROTOCOL-XKCD-DRAFT § "Protocol 3: COLLISION CHECK")
- [ ] Is the git working tree clean, or has the relevant branch been identified?

### C. Evidence & Observability

- [ ] Where will trial output be written? (Vault path or staging folder)
- [ ] How will the trial's results be preserved in the vault? (e.g., LEVELSET report, output note, log file)
- [ ] Who will review the output and confirm success or failure? (Must be Logan or a designated direct-write agent)

### D. Exit Criteria

- [ ] What does a **successful** trial look like? (Define the pass condition)
- [ ] What does a **failed** trial look like? (Define the stop condition)
- [ ] What happens after a failure? (Rollback path, FLAG, or Logan escalation)

### E. Timeline

- [ ] When does the trial begin?
- [ ] When is the verdict due? (Deadline for Logan's review of output)
- [ ] Is this trial time-sensitive? If so, why?

---

## V. FILING A STATUS CONFERENCE RECORD

Every STATUS CONFERENCE must produce a written record committed to the vault before the trial begins.

### Filename Pattern

```
STATUS-CONFERENCE-[SUBJECT]-[YYYY-MM-DD].md
```

Example:
```
STATUS-CONFERENCE-JFAC-CREW-2026-04-10.md
STATUS-CONFERENCE-VAULT-CUSTODIAN-BETA-2026-04-12.md
```

### Minimum Content

```markdown
---
title: "STATUS CONFERENCE — [Subject]"
date: YYYY-MM-DD
status: open
authority: LOGAN
related:
- [Linear issue]
- [GitHub issue]
---

# STATUS CONFERENCE: [Subject]

**Trial begins:** [timestamp or "pending Logan's go"]
**Verdict due:** [date]

## Checklist
[Paste and complete the checklist from PROTOCOL-STATUS-CONFERENCE.md]

## Notes
[Any open questions, dependencies, or concerns]

## Disposition
[ ] GO — trial proceeds as scoped
[ ] NO-GO — trial postponed (reason: ___)
[ ] SCOPED — trial proceeds with modifications (detail: ___)

**Logan's signature:** ___
```

### Storage Location

Status conference records go in the vault root. They are governance artifacts, not ephemeral scratch.

---

## VI. RELATIONSHIP TO EXISTING PROTOCOLS

| Existing Protocol | Relationship to STATUS CONFERENCE |
|---|---|
| **AGENT-PROTOCOL** (`AGENT-PROTOCOL.md`) | Defines bootstrap phases for registered agents. STATUS CONFERENCE runs *before* first activation of a new agent. |
| **XKCD / COLLISION CHECK** | COLLISION CHECK is a required item on the STATUS CONFERENCE checklist. |
| **MCP Phase Gates** | Phase 0 → 1 gate in MCP-IMPLEMENTATION-PLAN.md is an example of an informal status conference. This protocol formalizes that gate for all trials. |
| **LEVELSET** | LEVELSET captures state *after* a session. STATUS CONFERENCE captures readiness *before* a trial. They are complements. |
| **FLAG** | If a STATUS CONFERENCE item cannot be completed, raise a FLAG (severity: MEDIUM or HIGH) and do not proceed to trial. |
| **DECISIONS.md** | When Logan approves adoption of this protocol, log it as a new DECISION. |

---

## VII. NAMING RATIONALE

**STATUS CONFERENCE** — borrowed directly from civil procedure. The legal term is used without alteration because:

1. The vault already uses courtroom framing (THE COURTROOM, THE DOCKET, TRIAL, VERDICT)
2. The legal meaning is precise and well-understood
3. Using the real term keeps the analogy coherent and searchable

> *"If the courtroom is already named, name the conference too."*

---

## VIII. OPEN QUESTIONS FOR LOGAN

1. **Threshold:** Should minor automation changes (e.g., adding a cron trigger to an existing workflow) require a STATUS CONFERENCE, or only first-time activations?

2. **Self-certification:** Can an agent self-certify a STATUS CONFERENCE, or must Logan sign off before any live trial begins?

3. **CrewAI dry-run exemption:** Dry-run crew executions currently bypass this gate (see Section III exception). Is that the right boundary, or should any live API call trigger a conference?

4. **Record retention:** STATUS CONFERENCE records are filed at vault root. Should they eventually be archived to `!/` or a dedicated `TRIALS/` folder once the volume grows?

5. **Retroactive application:** Should the existing JFAC Crew and other active crews be issued retroactive STATUS CONFERENCE records for audit completeness?

---

*Proposed 2026-04-06 by GitHub Copilot (The Clerk). This document is a DRAFT. It has no authority until Logan confirms adoption.*

---

###### "The world is quiet here."
