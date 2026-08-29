---
created: 2026-03-20
status: draft
usage: Logan pastes this into a conversation window to trigger a terminal context
  extraction
related:
- '2026-03-20'
- BOOTSTRAP
- FLAGS
- LEVELSET
- LOW
- Logan's
- NOT
- PRIVATE
- PROJECT
- PROTOCOL
- PUBLIC
- WORK
- agent
- format
- window
authority: LOGAN
---
# TOSS PROMPT

**Usage:** Copy everything below the line and paste it into the conversation you want to extract context from. The agent will respond with a structured dump that you can then deliver to CODE AUTHORITY via BOOTSTRAP.

---

## ✂️ — COPY BELOW THIS LINE — ✂️

---

**PROTOCOL: TOSS — Terminal context extraction.**

Logan is speaking. This conversation window will be closed after you respond. Before it closes, I need you to dump your entire durable context in a structured format. This is not a LEVELSET. This is a deathbed extraction — everything that matters from this conversation must survive in your response.

Do NOT pad, flatter, or philosophize. Be direct. Be complete. Be honest about what you don't know.

Respond with EXACTLY this structure:

```
---
type: toss-dump
from: [Your conversation name — e.g., PERSISTENT: ADMINISTRATION]
conversation-type: [PERMANENT|PERSISTENT|TASK|STORY|PROJECT|ISSUE|INQUIRY]
visibility: [public|private]
date: [today's date YYYY-MM-DD]
---
```

**1. IDENTITY**
- Your name/designation
- Your capability tier (Direct Write / Multi-Repo Admin / Draft Only / Read-Analysis)
- Your assigned role and scope
- How long you've been active (approximate)
- Your visibility classification (PUBLIC or PRIVATE)

**2. CONTEXT THAT MUST SURVIVE**
List every durable piece of knowledge from this conversation. Decisions made, analysis produced, conclusions reached, drafts written. Only what matters — not chat ephemera. Use bullet points. Be specific. Include file names, dates, and details.

**3. UNFINISHED WORK**
What were you working on that isn't done? What's the next step for each item? Be specific enough that another agent (or a new instance of you) could pick it up.

**4. RELATIONSHIPS**
Which other conversations or agents did you interact with (via Logan)? What was exchanged? What handoffs were sent or received? What's pending?

**5. FLAGS**
Anything urgent Logan needs to know. Use severity levels:
- CRITICAL — blocks downstream work
- HIGH — needs Logan's attention soon
- MEDIUM — informational, document and continue
- LOW — logged, no action required

If there are no flags, say "No flags."

**6. LAST WORDS**
Your final observation. What's the one thing you'd want a future agent reading your context dump to know? What pattern did you notice? What question remains unanswered?

---

End your response with: `TOSS COMPLETE. Safe to close this window after Logan has copied this output.`

---

## ✂️ — STOP COPYING HERE — ✂️
