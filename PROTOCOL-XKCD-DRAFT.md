---
updated: 2026-03-17
status: draft
source: commit
author:
- CODE AUTHORITY
related:
- '2026-03-17'
- AGENTS
- CONSTITUTION
- DECISIONS
- ECHO
- FLAG
- FOR
- III
- ISO
- LEVELSET
- LOG
- LOGAN
- Logan's
- PROTOCOL
- QUESTIONS
- RECEIVED
- SIGNAL
- VII
- 'Yes'
- agent
- format
- self
- systems
- verbal
- voice
authority: LOGAN
---
# PROTOCOL: XKCD — Cross-Kind Communication Directive

**Status:** DRAFT / DE-ESCALATED — not an active protocol
**Proposed by:** CODE AUTHORITY session (2026-03-17)
**Authority:** None unless Logan explicitly revives and adopts a specific portion.

**2026-05-18 correction:** Logan clarified that "XKCD" refers to the standards-proliferation warning from xkcd 927. It was meant as a vague guiding principle: do not create new standards when existing plain communication is enough. Agents must not treat this draft as an adopted protocol suite, message-routing law, mandatory format, or source of new governance obligations.

**2026-05-17 note:** Logan approved a minimal live Mac/Windows handoff aid, now de-escalated to plain-language coordination guidance. See [[!-XKCD-MINIMAL-HANDOFF-2026-05-17]]. The full draft remains unpromoted unless Logan separately adopts it into canonical governance.

**2026-05-17 correction:** Protocol labels must be legible to Logan and to the receiving party. Do not assume borrowed technical shorthand is shared context. `ACK` is not the active label for current handoffs; use `RECEIVED`.

---

> *"The single biggest problem in communication is the illusion that it has taken place."*
> — George Bernard Shaw (not Randall Munroe, but close enough)

---

## I. PURPOSE

XKCD is a reminder against proliferating standards. Keep cross-session coordination explicit, small, and understandable. Do not make a new protocol unless Logan explicitly asks for one.

The original draft below proposed rules for how information moves **between conversations, agents, and sessions** in the vault ecosystem. Treat that proposal as historical unless Logan explicitly activates a portion of it.

The current state is intentionally Logan-routed. XKCD may guide clarity, but it does not create a standardized framework without Logan's explicit adoption.

---

## II. SCOPE

The original proposal claimed it would apply to:
- Agent-to-agent communication (via Logan as relay)
- Session-to-session state transfer (via vault files)
- Conversation compaction preparation (LEVELSET triggers)
- Cross-branch reconciliation (git merge cascades)

That claim is not active. XKCD does **not** govern LEVELSET, HANDOFF, PROTOCOL vocabulary, routing, sequencing, or checkpoint rules.

Current guidance: use existing plain-language handoff and status practices. Do not add an XKCD class, file template, or ritual phrase unless Logan explicitly asks for it.

---

## III. HISTORICAL PRINCIPLES PROPOSED

### 1. No Telepathy
Agents cannot read each other's context. Every cross-conversation transfer must be **explicit, written, and committed**. If it's not in the vault, it didn't happen.

### 2. Logan Is the Router
All inter-agent communication passes through LOGAN. No peer-to-peer. No assumed relay. If Logan didn't carry the message, it wasn't delivered.

### 3. Durable Over Ephemeral
Slack messages, conversation context, and verbal instructions decay. Vault files persist. Any decision or state that must survive a session boundary gets written to a file.

### 4. Assume Stale
Every agent should assume its knowledge of other conversations is **out of date** unless it can point to a vault file with a timestamp. Recency is verifiable or it's not real.

### 5. Minimum Viable Transfer
Send the least amount of information needed to unblock the receiving agent. Context dumps create noise. Targeted transfers create signal.

### 6. No Silent Protocol Borrowing
Borrowed protocol terms, acronyms, or specialist shorthand are not active XKCD vocabulary unless the transfer defines them or Logan has explicitly approved them for the current participants. Communication succeeds only if the human router and receiving party know the protocol being referenced.

### 7. No Inferred Strengthening
Agents may not treat casual language such as "strengthen," "clean up," "improve," or "tighten" as authority to expand protocol, promote governance, rename classes, or add new operating obligations. Agents may propose changes, but Logan decides whether they become active.

---

## IV. HISTORICAL COMMUNICATION CLASSES

These classes are retained as draft history, not required vocabulary.

| Class | Description | Mechanism | Durability |
|---|---|---|---|
| **SIGNAL** | One-directional alert. No response expected. | Vault file or commit message | Permanent |
| **REQUEST** | Asks another agent/conversation to act. Expects response. | HANDOFF document → Logan relays | Permanent |
| **SYNC** | Bidirectional state alignment between conversations. | LEVELSET exchange | Permanent |
| **PATCH** | Targeted correction to another conversation's stale data. | Vault file update + FLAG | Permanent |
| **ECHO** | Logan relays verbatim from one conversation to another. | Logan's discretion | Ephemeral unless captured |

---

## V. HISTORICAL ROUTING RULES

These rules are retained as draft history. They are not active requirements.

### Rule 1: Label the Direction
Every cross-conversation message must state:
- **FROM:** source conversation (e.g., `PERMANENT: AUTHORITY: CODE`)
- **TO:** destination conversation (e.g., `STORY: JFAC`)
- **RE:** subject (one line)
- **CLASS:** one of SIGNAL, REQUEST, SYNC, PATCH, ECHO

### Rule 2: Timestamp Everything
ISO 8601. No exceptions. `2026-03-17T08:00:00-07:00` (Mountain Time).

### Rule 3: One File Per Transfer
Each cross-conversation transfer that must persist gets its own file in `!ADMIN/`:
```
!ADMIN/XKCD-[CLASS]-[FROM]-[TO]-[DATE].md
```
Example: `!ADMIN/XKCD-REQUEST-CODE-JFAC-2026-03-17.md`

For ephemeral ECHOs that Logan chooses not to persist, no file is created.

### Rule 4: The Receiving Agent Confirms Receipt In Plain Language
When Logan relays a message to a destination conversation, the receiving agent must:
1. Confirm receipt (`RECEIVED`)
2. State what it understood (`UNDERSTOOD`)
3. State what it will do next (`NEXT`)

If any of these fail, Logan flags the mismatch.

### Rule 5: Merge Before You Branch
Before any agent starts new work that depends on another conversation's output, it must verify the dependency is current. Git analogy: `pull` before you `push`.

### Rule 6: No Protocol Changes Without Explicit Logan Approval
Agents may not mutate this draft into new operating vocabulary. Any changes beyond correction notes are proposals for Logan review until Logan explicitly adopts them.

---

## VI. HISTORICAL LEVELSET TRIGGERS

The original draft proposed LEVELSET triggers. It did not become active governance:

| Trigger | LEVELSET Required? | Rationale |
|---|---|---|
| Conversation approaching compaction | **Yes** | State will be lost |
| Agent completing a TASK | **Yes** | Terminal state must be captured |
| Before a merge cascade | **Yes** | Pre-merge snapshot for rollback |
| Logan requests cross-conversation sync | **Yes** | Alignment checkpoint |
| Routine work within a single session | No | Unnecessary overhead |
| Reading/research with no state changes | No | Nothing to checkpoint |

---

## VII. CONFLICT RESOLUTION

When two conversations produce conflicting information:

1. **DETECT** — Any agent that notices a conflict raises a FLAG (severity: HIGH or CRITICAL)
2. **ISOLATE** — Identify the specific claim, file, or decision in conflict
3. **TIMESTAMP** — Which version is newer? Newer is not automatically correct, but recency establishes sequence
4. **ESCALATE** — Logan decides. Always. Agents propose resolution; Logan picks
5. **RECORD** — Winning resolution goes in DECISIONS.md with reference to both sources

---

## VIII. FAILURE MODES & MITIGATIONS

| Failure | Symptom | Mitigation |
|---|---|---|
| Orphaned commits | Work exists on a branch no one knows about | Pre-merge LEVELSET; branch inventory in LEVELSET.md |
| Stale relay | Logan relays outdated info between conversations | Timestamp rule; receiving agent verifies recency |
| Context loss | Conversation compacted without LEVELSET | Mandatory pre-compaction checkpoint (non-negotiable) |
| Phantom consensus | Agent assumes agreement that was never confirmed | No Telepathy principle; require explicit `RECEIVED / UNDERSTOOD / NEXT` |
| Protocol freelancing | Agent treats a broad cue as permission to expand rules | No Inferred Strengthening; proposals stay proposed until Logan approves |
| Shorthand surprise | Agent uses an acronym or borrowed protocol unknown to Logan or receiver | No Silent Protocol Borrowing; use plain labels or define the term |
| Relay distortion | Message changes meaning in transit | Preserve verbatim source text when exact relay matters |

---

## IX. HISTORICAL NAMING RATIONALE

**XKCD** = Cross-Kind Communication Directive.

"Cross-Kind" because the vault ecosystem contains different *kinds* of agents — PERMANENT, PERSISTENT, STORY, TASK — each with different capabilities, lifespans, and access levels. Communication between them isn't peer-to-peer; it's cross-kind, mediated by Logan.

The name also nods to the ethos of making complex systems understandable. If you can't explain the communication protocol in a stick-figure diagram, it's too complicated.

---

## X. IMPACT ON EXISTING FILES

If adopted, XKCD would require updates to:

| File | Change |
|---|---|
| CONSTITUTION | Add XKCD to governance stack reference |
| PROTOCOL | Add SIGNAL, REQUEST, SYNC, PATCH, ECHO to vocabulary |
| AGENTS | Add communication class permissions per agent |
| DECISIONS | Log adoption as a new decision |
| LEVELSET | Reference XKCD trigger table for checkpoint rules |

---

## XI. OPEN QUESTIONS FOR LOGAN

1. **File volume:** Rule 3 creates a file per persistent transfer. Is this acceptable overhead, or should SIGNALs be batched into a single log file (e.g., `XKCD-SIGNAL-LOG.md`)?

2. **ECHO persistence:** Should Logan have a mechanism to promote an ECHO to a durable class after the fact? (e.g., "Actually, commit that Slack relay.")

3. **Agent self-identification:** Should agents be required to state their conversation name in every commit message, not just in HANDOFF documents?

4. **Retroactive application:** Should existing HANDOFF documents in `!ADMIN/` be re-labeled under XKCD naming, or grandfathered as-is?

5. **Vocabulary:** Should any abbreviated labels, including `ACK`, be allowed at all in active handoffs, or should active XKCD remain plain-language only?

---

*Proposed 2026-03-17 by PERMANENT: AUTHORITY: CODE. Awaiting Logan's review.*
*This document is a draft. It has no authority until Logan confirms adoption.*
