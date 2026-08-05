---
title: "What I Learned Parsing Claude Code’s JSONL Session Logs"
source: "https://medium.com/@ywian/what-i-learned-parsing-claude-codes-jsonl-session-logs-268248be0a2c"
author:
  - "[[Yang Liu]]"
published: 2026-03-14
created: 2026-06-11
description: "I’ve been building autonomous agents backed by Claude Code — skills that chain prompts, spawn subagents, and orchestrate multi-step workflow"
date created: Thursday, June 11th 2026, 2:08:19 am
date modified: Thursday, June 11th 2026, 2:08:35 am
---

I’ve been building autonomous agents backed by Claude Code — skills that chain prompts, spawn subagents, and orchestrate multi-step workflows. When an agent misbehaves, the first question is always: was it a prompt issue or an agent issue? To answer that, you need to see exactly what happened inside the session — every tool call, every subagent spawn, every thinking block, in order.

Claude Code doesn’t have a built-in log viewer for this. But it does write everything to \`*.jsonl* \` files in \` *~/.claude/projects/* \`.

So I built [Claude Code Tracer](https://github.com/delexw/claude-code-trace), an app/web/tui that reads these session logs and renders them as a live, navigable UI — think “tail -f” but for your entire conversation tree, with subagents, teams, token costs, and ongoing status indicators. If you’re a GUI lover, it’s a good fit — it’s a native desktop app that stays under ~10% CPU even while tailing active sessions.

The core challenge? These JSONL files are undocumented, streaming, hierarchically nested, and full of edge cases. Here’s what I learned across ~90 commits and 30+ versions getting the parser to a stable state.

## The Format Is Undocumented

There’s no spec for Claude Code’s JSONL format. Every field was discovered by reading live session files and observing what changed. A single entry can have: *\`type\`, \`uuid\`, \`leafUuid\`, \`timestamp\`, \`message\` (with nested \`role\`, \`content\[\]\`, \`model\`, \`stop\_reason\`, \`usage\`), \`toolUseResult\`, \`sourceToolUseID\`, \`cwd\`, \`gitBranch\`, \`permissionMode\`, \`teamName\`, \`agentName\`, \`requestId\`, \`isSidechain\`, \`isMeta\`, \`summary\`, \`data\`* … and most of these are optional.

The \`message.content\` field is a polymorphic array — each element can be \`text\`, \`thinking\`, \`tool\_use\`, or \`tool\_result\`, each with a different shape. You don’t know what you’re getting until you inspect the \`type\` field of each block.

**Lesson:** When working with an undocumented format, build your parser defensively. Every field is optional, every shape is a maybe. I used Rust’s \`Option<T>\` everywhere and it saved me repeatedly.

## 1st Challenge — Streaming vs. Complete Entries

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MQTF8LZzb5th87k3ngJJpg.png)

Claude Code writes JSONL lines **as it streams** its response. This means you’ll see partial entries without a \`stop\_reason\`, with understated token counts, appearing as multiple lines that logically represent one AI response.

My first approach treated every line as a standalone message. The UI showed duplicated, fragmented AI responses. The fix was building a “chunk builder” that merges consecutive assistant entries into a single display chunk, and only trusting token snapshots from entries that have \`stop\_reason\` set.

**Lesson:** JSONL lines are not messages. They’re streaming fragments. You need a grouping layer between raw parsing and display.

## 2nd Challenge — Ongoing Session Detection

This was the single hardest problem and took **6 fix commits** across versions v0.2.5 through v0.3.2 to get right.

### Attempt 1: “Is the last entry recent?”

Simple timestamp check. Failed immediately — a session can be idle for 30 seconds while Claude is thinking, and a completed session’s last entry is always “recent” right after it finishes.

### Attempt 2: Activity trace analysis

Walk the chunks and classify the last meaningful activity: thinking, tool use, text output, interruption. If the last activity is an “ending” one (text output, \` *ExitPlanMode* \`, shutdown approval), it’s done. Otherwise, ongoing.

This worked for simple sessions but missed a critical case: **background Bash commands**. A session can have its last chunk be text output (looks done!) but still have \` *run\_in\_background* \` commands executing.

**Lesson:** You can’t determine session status from a single field. You need to walk the full chunk history and count unresolved activities — the JSONL is an event log, not a status record.

## 3rd Challenge — The Orphan Agent Lifecycle

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*hGL7TnjZQ45D8H9MozCHog.png)

This one is my favourite because it captures a pattern I haven’t seen written about much: **entities that are born parentless and adopted mid-flight**.

### How Claude Code Spawns Subagents

When Claude decides to launch a subagent, two things happen on disk — but not at the same time:

1\. A new file appears: \` *{session-dir}/{session-name}/subagents/agent-{id}.jsonl* \`

2\. The parent session writes a \` *tool\_use* \` entry with type \` *Agent* \` that contains the \` *tool\_id* \`

The subagent file often lands **\*\*before\*\*** the parent writes its \` *tool\_use* \` entry. The file watcher fires, I discover a new \`.*jsonl* \` in the subagents directory, I parse it, I have real chunks with real content… but there’s no matching tool call in the parent session yet. The subagent has no parent. It’s an orphan.

### Attempt 1: Just Wait

My first approach was to ignore subagent files until a matching parent \` *tool\_use* \` appeared. This meant subagents were invisible for the first few seconds of their life — the most interesting part, when Claude is thinking and calling tools. By the time the link existed, you’d missed the live action.

### Attempt 2: The Orphan → Adopted Pattern

The solution was a four-phase linking pipeline followed by an orphan injection step:

**Phase 1 — Result-based matching:**

Scan the parent session’s raw JSONL for \` *skill\_progress* \` and \` *toolUseResult* \` entries that map \` *agent\_id → tool\_id* \`. If the subagent has already completed and reported back, its result contains the link. This handles the “already done” case cleanly.

**Phase 2 — Team member matching by description:**

For team workers (spawned via \` *TeamCreate* \` → \` *TaskCreate* \`), there’s no direct \` *agent\_id → tool\_id* \` mapping. Instead, the worker’s JSONL contains a team summary string embedded in its first user message. We match workers to \` *TaskCreate* \` display items by comparing the task description. Earliest-first to break ties.

**Phase 3 — Positional fallback:**

Any still-unmatched subagent processes get paired with still-unmatched \` *Agent* \` tool calls by position order. This is a heuristic — it works because Claude Code typically spawns agents in the order it writes the tool calls. Not bulletproof, but catches the common case.

**Phase 4 — Nested enrichment.**

Some subagents are spawned by *\*other subagents\** (e.g., an orchestrator Skill spawns child agents). Phase 1 may have linked them by \` *tool\_id* \` but couldn’t find the matching \` *DisplayItem* \` in the parent session’s chunks — because the tool call lives in the orchestrator’s chunks, not the root session’s. This phase searches *\*all\** processes’ chunks to fill in descriptions and types.

**After all four phases:**

## Get Yang Liu’s stories in your inbox

Join Medium for free to get updates from this writer.

anything still unlinked (\` *parent\_task\_id* \` is empty) is a true orphan. I used a function creates synthetic \` *DisplayItem* \` entries for them, marks them with \` *is\_orphan: true* \`, gives them a synthetic tool ID (\` *orphan-{agent-id}* \`), and appends them to the last AI chunk in the parent session — sorted oldest-first so they appear in chronological order as a workaround

### The Beautiful Part: Orphans Become Adopted

Here’s where it gets interesting. On the next file watcher tick (200ms debounce), the parent session will likely have written its \` *tool\_use* \` entry. The entire pipeline reruns:

1\. Discovery finds the same subagent file

2\. Phase 1 now finds the \` *agent\_id → tool\_id* \` link in the parent’s \` *toolUseResult* \`

3\. The subagent gets a real \` *parent\_task\_id* \`

4\. It no longer qualifies as an orphan

5\. The orphan injection step skips it

6\. The function to find a \` *DisplayItem* \`renders it inline, nested under its parent’s tool call — exactly where it belongs

The subagent transitions from “orphan badge at the bottom of the message list” to “properly nested child of its parent Agent call” — seamlessly, in a single re-render. In the UI, you literally see the orphan disappear from the bottom and reappear nested inside the correct AI message.

### The Warmup Agent Trap

There’s a ghost in this system. Claude Code pre-creates “warmup” agent files — empty subagent sessions used for performance pre-loading. Their first user message is literally the string \`”Warmup”\`. Without filtering, your UI fills with phantom agents that never did anything.

The \` *is\_warmup\_agent* ()\` function reads the first user entry of each subagent file and checks if the content is \`”Warmup”\`. If so, it’s skipped entirely during discovery. Simple, but without it the UI was confusing — users would see empty agents that appeared and never progressed.

### And Then There Are Nested Orphans

The final edge case: an orchestrator subagent (itself an orphan relative to the main session) spawns child agents via the \` *Skill* \` tool. The children link to the orchestrator’s \` *tool\_use* \` ID, not the main session’s. After \` *inject\_orphan\_subagents* \`, only the orchestrator should be orphaned — its children should be properly linked inside its nested panel.

**Lesson:** In a multi-file streaming system, you can’t assume causal ordering across files. Design for the orphan state as a first-class lifecycle phase, not an error condition. The pattern is: discover → attempt to link → inject orphans → re-link on next tick → orphans graduate to adopted. It’s not a bug to be parentless — it’s a transient state that resolves itself.

## 4th Challenge — Team Reconstruction

Teams are the most complex structure. A lead agent creates a team (\` *TeamCreate* \` tool call), assigns tasks (\` *TaskCreate* \`), and workers report back (\`TaskUpdate\`). The state is spread across **\*\*multiple JSONL files\*\*** — the lead’s session file plus each worker’s separate file.

Reconstruction requires a phased approach:

1\. Parse lead chunks → create teams, tasks

2\. Parse worker chunks → apply task updates from worker actions

3\. Populate worker metadata (colors, names)

4\. Determine per-member ongoing status independently

Getting the phases wrong produces ghost team members, missing task updates, or incorrect status indicators.

**Lesson:** When state is distributed across files, you need explicit reconstruction phases with a defined merge order. Don’t try to build the full picture in a single pass.

## 5th Challenge — Noise Filtering

Not every JSONL entry is meaningful. The format includes:

\- \` *isSidechain: true* \` entries (internal plumbing)

\- \` *system* \` type entries (context injection)

\- \` *file-history-snapshot* \` entries (file state tracking)

\- \` *queue-operation* \` entries (internal queue management)

\- \` *progress* \` entries (except \` *hook\_progress* \` which users care about)

My early versions showed all of these, making the UI noisy and confusing. The classifier now has an explicit deny-list of entry types and flags to filter before anything reaches the chunk builder.

**Lesson:** In an undocumented format, assume most entry types are internal. Start by showing nothing, then add back what users actually need to see.

## 6th Challenge — Persisted Output Resolution

Large tool results (long command outputs, big file reads) don’t get inlined in the JSONL. Instead, Claude Code writes them to a separate file on disk and puts a file path reference in the JSONL entry.

My parser initially showed these as empty tool results. The fix was detecting the reference pattern and reading the external file to resolve the full content.

**Lesson:** JSONL entries are not self-contained. They can reference external files, and your parser needs to follow those references.

## Key Takeaways

1\. **Undocumented formats require defensive parsing** — every field optional, every shape a maybe, every assumption verified against real data

2\. **Streaming JSONL is not a message log** — it’s a fragment stream that needs grouping, deduplication, and incremental reading with byte offsets

3\. **Design for orphans as a first-class state** — in multi-file streaming, entities appear before their parents do; treat “parentless” as a transient lifecycle phase, not an error

4\. **Multi-file distributed state needs phased reconstruction** — subagents, teams, and workers each have their own file, and ordering matters

5\. **Most JSONL entry types are noise** — start by filtering aggressively, then add back what users actually need to see

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*v08hVPr7dUmjPz7I28r3_w.png)

The format will likely keep evolving as Claude Code adds features. The parser is stable today, but I expect more edge cases as new tool types, agent patterns, and session structures emerge. The architecture — entry parsing → classification → chunk building → status analysis → display conversion — has held up well through all of these challenges, and that pipeline design is probably the most important lesson of all.