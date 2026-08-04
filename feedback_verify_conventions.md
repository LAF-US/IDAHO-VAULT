---
name: Verify conventions against actual data before writing plans
description: Do not invent file format or naming conventions based on plausible-sounding guesses; grep the source first
type: feedback
---

When writing a plan or code that keys on a naming/format convention in a data source, VERIFY the convention against the actual file before committing it to the plan.

**Why:** On 2026-04-10, while planning the budget tracker "Approp," filter, Logan answered an AskUserQuestion multiple-choice option that included "Supp approp," and "Trustee," as additional prefixes. I wrote those into the plan as if they were real LSO conventions. They were not — grep of `minidata-2026-04-01.csv` showed zero matches, and I had already run that grep and seen zero results before writing the plan. I rationalized the empty result as "pre-built for when they appear later" instead of flagging "these strings do not exist in the source data." Logan caught it with "Are those actually based on the minidata conventions?"

This is the confabulation failure mode: filling in a plausible-sounding structure rather than admitting "I don't know" or reporting "the data doesn't contain this."

**How to apply:**
- Before writing a plan that hardcodes a string, prefix, field name, or path into code: grep the actual source file for it. If zero hits, say so explicitly in the plan.
- When the user offers a multiple-choice option that names specific strings, treat it as a hypothesis to verify, not a fact. Confirm against data before promoting.
- If a grep returns zero, the correct response is "this does not appear in the data" — not "we'll pre-build for it just in case."
- Logan values accuracy above all (see user_logan.md). Confabulation erodes trust faster than saying "I don't know."
