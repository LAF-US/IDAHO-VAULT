---
name: never-cite-unread-sources
description: Standing rule from Logan — never cite a source without having read it in full
metadata:
  type: feedback
---

Never cite a source without having read its entirety. No citing from search-result
snippets, WebFetch summaries, or another agent's report.

**Why:** A summarizer's gloss is not the source. Citing one launders an unverified
claim into an apparent fact, and the citation makes it look checked when it was not.
This produced a 404'd repo cited as a real fix, and a recommendation built on a
summary that had explicitly said it could not answer the question.

**How to apply:** WebFetch and WebSearch are *discovery* tools — they find candidate
URLs. They are not reading. To actually cite something, retrieve the full text
(`curl`, or read the file) and read it. If a source is too large or cannot be
retrieved in full, say what was and was not read rather than citing it flatly.
Applies to vault files too: read the whole file, not a grep hit.

Related: [[wizard-eyes-failure-mode]] — same root error, treating an intermediary's
text as observed fact.
