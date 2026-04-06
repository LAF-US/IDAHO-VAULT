---
updated: 2026-03-16
status: draft
source: commit
related:
- '2026-03-16'
- AGENTS
- API
- GitHub
- HOW
- LLM
- LOGAN
- PROTOCOL
- USE
- WATCH
- agent
- fire
- format
- index
authority: LOGAN
---
# PROTOCOL.md — Pending Ambiguity Resolutions

Six overlaps in `PROTOCOL.md` require LOGAN's direction. For each: the question, CODE AUTHORITY's recommendation, and options. These are advisory — LOGAN decides.

---

## 1. CONSULT vs. ADVISE

**Question:** Should these be strictly separated, or is CONSULT→ADVISE a natural flow?

**Recommendation:** Natural flow. CONSULT is the request; ADVISE is the response. They're a paired action, not competing terms.

| Option | Description |
|---|---|
| **A: Paired flow (recommended)** | CONSULT = "I'm asking." ADVISE = "I'm answering." One naturally triggers the other. An agent CONSULTs a source; that source ADVISEs back. Both logged if persistent. |
| **B: Strict separation** | CONSULT is always information-seeking (no opinion). ADVISE is always opinion-giving (may be unsolicited). An agent can ADVISE without being CONSULTed. |
| **C: Merge into one term** | Drop CONSULT, keep ADVISE. All advisory interactions are just ADVISE. Simpler vocabulary. |

**Impact on other files:** None. This is purely semantic.

---

## 2. SEARCH vs. FIND vs. CONSULT

**Question:** When does an agent use CONSULT vs. SEARCH? What's the role of FIND?

**Recommendation:** Distinguish by source type and certainty.

| Option | Description |
|---|---|
| **A: Source-type distinction (recommended)** | SEARCH = query against structured data (API, index, database). CONSULT = query against advisory/knowledge source (another agent, documentation, LLM). FIND = successful resolution of either. |
| **B: Certainty distinction** | SEARCH = I know what I'm looking for. CONSULT = I'm exploring / uncertain what exists. FIND = I got it. |
| **C: Drop FIND** | FIND is just a successful SEARCH/CONSULT. Don't need a separate term for the outcome — log it as SEARCH (result: found) or SEARCH (result: not found). |

**Impact on other files:** If CONSULT is the term for querying another agent, AGENTS.md communication rules should reference it.

---

## 3. DELETE vs. DESTROY vs. SUNSET

**Question:** What's the durability ladder? Audit trail requirements for each?

**Recommendation:** Strict ladder with escalating audit requirements.

| Option | Description |
|---|---|
| **A: Strict ladder (recommended)** | DELETE = soft removal, recoverable, minimal audit. SUNSET = scheduled deactivation with transition period, logged with timeline. DESTROY = permanent, irrevocable, requires pre-approval and full audit trail. |
| **B: Audit trail for all** | All three require audit logging. Differ only in recoverability: DELETE (recoverable) → SUNSET (time-delayed permanent) → DESTROY (immediate permanent). |
| **C: Merge DELETE and SUNSET** | DELETE = soft. DESTROY = permanent. SUNSET is just a scheduled DELETE — no separate term needed. |

**Impact on other files:** AGENTS.md boundary rules should specify which tiers can execute each. Suggestion: DELETE = any writing agent. SUNSET = CODE AUTHORITY + Logan approval. DESTROY = Logan only.

---

## 4. NOTICE vs. NOTE

**Question:** What's the boundary between ephemeral and persistent?

**Recommendation:** Storage obligation is the bright line.

| Option | Description |
|---|---|
| **A: Storage obligation (recommended)** | NOTICE = observation with no storage requirement. May be logged ephemerally (console, Slack) but creates no retrievable record. NOTE = observation with explicit storage requirement. Must produce a file, log entry, or other retrievable artifact. |
| **B: Formality distinction** | NOTICE = informal, passing. NOTE = formal, deliberate. Both may or may not be stored depending on context. |
| **C: Drop NOTICE** | Everything worth recording is a NOTE. If it's not worth recording, don't name it. Simpler vocabulary. |

**Impact on other files:** If NOTICE is purely ephemeral, it aligns with "Slack is ephemeral, vault is the record." NOTEs go to files; NOTICEs can stay in Slack.

---

## 5. HYDRATE vs. INGEST

**Question:** Can INGEST create partial records? Is HYDRATE restricted to existing structures?

**Recommendation:** Strict separation by record existence.

| Option | Description |
|---|---|
| **A: Existence-based distinction (recommended)** | INGEST = record doesn't exist yet; create it (partial or complete). HYDRATE = record already exists; enrich it with additional data. The question is: "Does the record exist?" If no → INGEST. If yes → HYDRATE. |
| **B: Completeness-based** | INGEST = create a complete record from external source. HYDRATE = fill in missing fields on an incomplete record. INGEST must be complete; HYDRATE patches gaps. |
| **C: Merge into INGEST** | INGEST handles both creation and enrichment. Use metadata to distinguish first-time vs. update. Simpler vocabulary. |

**Impact on other files:** Vault operations like `idaho_leg_scraper.py` use both — new bills are INGESTed, existing bills with new activity are HYDRATEd. The distinction maps cleanly to existing automation.

---

## 6. WATCH vs. LISTEN

**Question:** Pull vs. push? Or can both be either?

**Recommendation:** Distinguish by agency.

| Option | Description |
|---|---|
| **A: Agency distinction (recommended)** | WATCH = agent actively polls or inspects on a schedule (pull). LISTEN = agent passively receives events/signals when they arrive (push). WATCH requires initiative; LISTEN requires registration. |
| **B: Duration distinction** | WATCH = sustained, continuous. LISTEN = event-triggered, intermittent. Both can be pull or push. |
| **C: Merge into MONITOR** | Drop both. Use MONITOR for all sustained observation. Distinguish pull vs. push in metadata, not in the term. |

**Impact on other files:** GitHub Actions workflows are WATCH (scheduled cron triggers). Slack bot webhooks would be LISTEN (event-driven). The distinction is practical for how we describe automation.

---

## HOW TO USE THIS DOCUMENT

Logan: for each ambiguity, pick A, B, or C (or propose D). CODE AUTHORITY will update `PROTOCOL.md` with the finalized definitions and remove the corresponding entry from this file. When all 6 are resolved, this file gets archived.

Quick-fire format if you're short on time:
```
1: A
2: A
3: A
4: A
5: A
6: A
```

Or just say "all A" if the recommendations look right.
