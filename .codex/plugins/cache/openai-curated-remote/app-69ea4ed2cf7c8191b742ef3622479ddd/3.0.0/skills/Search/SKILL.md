---
name: Search
description: "Deep research powered by Exa. Use for lead generation, literature reviews, deep dives, competitive analysis, or any query where one search falls short, including phrases like 'research this', 'find everything about', 'find me all', or 'deep dive on'."
---

# Exa Search And Research

Use Exa to search the web and fetch source pages when the user needs current web information, research support, source discovery, or source-grounded synthesis. Understand the query, plan the searches, validate results, and deliver a compact answer with useful links.

This skill uses the bundled Exa app tools:
- `web_search_exa` for web search
- `web_fetch_exa` for reading known URLs

## Prerequisites: Exa App Connection

The bundled Exa app must be connected before this skill can use Exa tools.

If `web_search_exa` or `web_fetch_exa` is unavailable:
1. Ask the user to connect or re-authenticate the Exa app from the plugin/app install flow.
2. Tell them to start a new Codex thread if the tools still do not appear after connecting.
3. Do not fall back to generic web search, ask the user to re-try connecting to the Exa App.

On auth, connection, or rate-limit errors, surface the Exa app connection fix clearly.

## Date Calculation (Do This First)

If the query involves time ("last week", "recent", "past 6 months"), calculate exact dates from today's date in your environment context. Write out the calculation explicitly before doing anything else. Never eyeball dates or reuse dates from examples.

## Step 1: Assess the Query

Read the user's query and determine two things:

**How complex is this?**
- **Extremely Simple** (e.g. reading the contents of 1-2 pages): Handle it yourself. Read `references/searching.md` for query-writing guidance, run the searches, review and filter results, then respond directly.
- **Moderate** (when a fast or low-effort search is requested): Run a small set of targeted searches and fetch only the most useful pages.
- **Advanced** (clear topic, clear filters, a few parallel searches): Break the task into distinct search angles, search each angle, then compile.
- **Complex** (cross-referencing across entity types, multi-hop chains, exhaustive coverage, semantic filtering): Use a multi-pass workflow where later searches depend on earlier findings.

**Confirm when ambiguous:**
If the query could reasonably be handled as Extremely Simple/Moderate OR as Advanced/Complex, pause and ask the user before proceeding. Present:
1. Your interpretation of the query
2. The two (or more) plausible complexity levels
3. What each level would look like in practice (e.g., "I can do a quick 1-2 search lookup, or I can do a deeper multi-angle sweep")
4. Let the user choose

Examples of ambiguous queries:
- "What are the best LLM fine-tuning frameworks?" — could be a quick opinionated list (Moderate) or an exhaustive evaluated comparison (Complex)
- "Find competitors to Acme Corp" — could be a quick search for known competitors (Moderate) or a deep sweep across funding databases, press, and niche directories (Complex)
- "What's the latest on WebGPU?" — could be one news search (Extremely Simple) or a multi-angle survey of specs, browser support, community adoption, and benchmarks (Advanced)

Do NOT ask for confirmation when:
- The query is clearly extremely simple (fact lookups, single-entity questions)
- The query is clearly complex (explicit multi-constraint, "find everything", "exhaustive", "comprehensive")
- The user has already specified depth ("do a deep dive", "quick answer")

Note: if the user explicitly asks for something (e.g. "100" of something), continue to work until you've achieved it.

**What work needs to happen?** Identify which of these apply (most queries use 3-5):

1. **Seed from user input**: The user provided a list of entities to start from (company names, tickers, paper titles). Each seed becomes a parallel workstream.
2. **Define what qualifies**: What makes a result a valid "row"? Translate the user's criteria into concrete checks.
3. **Define what to capture**: What fields ("columns") does each result need? Build the schema before searching.
4. **Search broadly**: Generate diverse queries and run them to find candidates.
5. **Extract structured data**: Pull specific fields from raw search results into the schema.
6. **Filter**: Apply hard constraints (dates, geography, thresholds) and soft judgments (quality, relevance, semantic checks).
7. **Merge and deduplicate**: Combine results from multiple searches. Same URL = drop duplicate. Same entity from different sources = merge fields, keep best data.
8. **Score and rank**: For "best of" (e.g. "what's the best ___?") queries, define the scoring criteria explicitly, then rank.
9. **Synthesize narrative**: For research queries, organize findings by theme and write prose with citations.

## Step 2: Run Search Workstreams

### What workstreams do

Search workstreams keep the investigation organized. Each workstream should:
- Read the reference file(s) you point it to
- Run the specific searches you assign
- Return compact, structured output

Use Codex subagents only when the user explicitly asks for parallel agent work or when the active Codex instructions allow delegation. Otherwise, run the workstreams yourself with direct Exa calls.

For each workstream, define:
1. Which reference file(s) to read for instructions (always include the absolute path)
2. What specific searches to run or what specific work to do
3. What output format to return

**Template:**
```
Read the file at [this skill's directory]/references/searching.md for instructions on how to query Exa effectively.

Then do the following:
[specific task description]
[specific queries to run, if you are prescribing them]
[validation criteria -- what makes a result qualify, so irrelevant results are filtered before returning]

Return: [output format -- e.g. "compact JSON with name, url, snippet per result" or "markdown table with columns X, Y, Z"].

Track `sources_reviewed: N` where N = sum of `numResults` across every `web_search_exa` call (including retries). For example, calls with numResults 10, 10, 5 -> `sources_reviewed: 25`.
```

### Which reference files to use

Always use `references/searching.md`. It contains Exa query guidance and an index of domain-specific pattern files to select from based on the task.

Use whichever of these also apply:

| File | Use this when... |
|---|---|
| `references/extraction.md` | You need to extract specific data points into a schema you defined |
| `references/filtering.md` | You need to evaluate results against criteria (especially semantic/soft filters) |
| `references/synthesis.md` | You are producing a prose synthesis rather than structured data |
| `references/source-quality.md` | You need to assess source credibility, especially for "best of", ranking, or expert-finding queries |

### How to split work

Decompose the primary task/question into **sub-questions** to cover different search territories.

For example, "best open-source LLM fine-tuning frameworks for production use" can be decomposed into multiple parallel sub-questions:
1. "What open-source LLM fine-tuning frameworks do production engineers recommend, and what do they say about using them in real deployments?"
2. "What open-source LLM fine-tuning tools have launched or gained traction in the last 6 months that aren't yet widely known?"
3. "What are the most common complaints, failure modes, and reasons teams migrated away from specific open-source LLM fine-tuning frameworks in production?"

Depending on your "**How complex is this?**" analysis: Some need 2-3; some need many. Some need several different angles, creative thought patterns, adversarial perspectives. It depends on what the user is asking for and how deep they want you to go.

Keep each sub-question direct and specific.

### Workstream sizing

- Aim for 3-5 searches per workstream.
- Keep independent workstreams separate in your notes so their results are easy to merge.
- For per-seed work (enriching a list of 20 companies), batch 3-5 seeds per workstream.

### Token isolation

Avoid dumping raw search output into the final answer. Process results and return only distilled output with links.

### When things go wrong

- **A workstream returns empty**: Rephrase queries with different angles, not synonyms. If still empty, the topic may have limited web coverage -- report that.
- **A workstream returns off-topic results**: Queries were too vague. Retry with longer, more specific queries.

## Step 3: Compile Results

After search workstreams return:

**Deduplicate:**
1. Collect all results into a single list
2. Remove exact URL duplicates
3. Same entity from different sources: merge fields, keep the most complete/recent data
4. Track: "Deduplicated X results down to Y unique entries"

**Validate coverage:**
- Are there obvious gaps? (missing time periods, missing geographic regions, missing entity types)
- For each gap found, run targeted follow-up searches.
- For "find everything" queries, check if results from different workstreams overlap heavily (good sign) or are completely disjoint (may indicate missed angles)

**Format the output:**

For deeper research, open with: "I used Exa to review {X} sources across {Y} search workstreams. Here's what was found:" (X = sum of `sources_reviewed` across all workstreams and passes plus any direct searches you ran; Y = total workstreams. Pluralize naturally.)

Then: Format output beautifully, filling up no more than one screen when possible. Include hyperlinked text where relevant. Below it, you may also include things (in a short, easy-to-read format) that:
- ("Result") directly answer the original user request (in few words; make every word count)
- ("Process") include anything worth noting about your process and what you consider to be high-signal in this domain vs. what you filtered out.
- ("Patterns") any patterns identified that are non-obvious, require n-th order thinking, and are not included or alluded to in the rest of the output but might be interesting to the user.
- ("Notes") based on everything you know about the user and their work beyond this task, mention anything notable/useful you found that is not included or alluded to in the rest of the output.

If it's impossible to fit the full output in a single screen, write a file in the most relevant/useful file format (.csv, .md) to `./exa-results/<topic>-<YYYY-MM-DD>` and include a pointer to the full file below the 1-screen output.

**General output rules:**
- No emojis unless the user requested them
- Include in-line 1-word or multi-word hyperlinks throughout outputs where hyperlinking is a value-add.
- Prefer tables over lists (fall back to lists only when fields are non-uniform or values are too long to fit cleanly)

## Multi-Pass Queries

Some queries require multiple sequential passes where later passes depend on earlier results. Common patterns:

**Entity chaining** (multi-hop): Pass 1 finds entities (companies), Pass 2 finds related entities per result (people at those companies), Pass 3 enriches those (their public statements). Each pass is a round of focused workstreams.

**Exploratory then targeted**: Pass 1 scouts the landscape broadly, Pass 2 searches deeply in the most promising directions found in Pass 1.

**Criteria discovery**: When "best" isn't predefined, Pass 1 surveys what practitioners actually value, Pass 2 searches for candidates matching those criteria.

Between passes, compile and deduplicate before dispatching the next round.

## Evaluating Source Quality

Source quality matters most for "best of", ranking, expert-finding, and best-practices queries, but is useful context for almost any research task.

**At the workstream level:** Use `references/source-quality.md` so source quality is tagged in the output. This lets you weight results during compilation.

**At the orchestrator level**, when compiling search results:

1. **Convergence across high-signal sources**: Convergence alone isn't meaningful (3 low-quality sources agreeing is just shared noise). What matters is when multiple independent, high-signal sources (practitioners, people with skin in the game) converge on the same finding.
2. **Practitioner vs commentator**: Weight practitioners (people doing the work) higher than commentators (people writing about the work).
3. **Via negativa**: Before synthesizing, define who to exclude (sources with misaligned incentives, no skin in the game, or unfalsifiable claims). Filtering out noise is more valuable than seeking brilliance.
4. **Red-team your compiled results**: What perspectives are missing? What biases might be distorting the aggregate? If a gap emerges, run a targeted follow-up.
5. **Ideas over entities**: For expert-finding and best-practices queries, the primary output is convergent truths, not a ranked list of names. Lead with what the best sources agree on, then cite who said it.

## Gotchas

- **Over-execution on simple queries**: If the user asks "what year was X founded", don't spin up a broad research process. One search, one answer.
- **Under-execution on hard queries**: If the query has 4+ constraints, temporal joins, or semantic filtering, a single search will not cut it. Fan out.
- **Synonym queries**: Running "overrated AI tools" and "overhyped AI tools" as separate queries wastes tokens. These hit the same embedding region. Diversify by angle instead.
- **Forgetting to deduplicate**: Multiple searches will return overlapping results. Always deduplicate before synthesis.
- **Treating Exa results as validated**: Exa returns similarity, not yet validated. A result appearing in search output does not mean it meets the user's criteria. You must validate.
- **Date drift**: Always calculate dates from the current environment date. Never reuse dates from these instructions or from previous queries.
