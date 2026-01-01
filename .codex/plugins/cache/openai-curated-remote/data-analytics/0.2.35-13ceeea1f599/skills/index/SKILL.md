---
name: index
description: "Answer product and business questions with data and route data-related work to the right focused workflow. Use for requests involving data, metrics, trends, comparisons, drivers, KPIs, analysis, dashboards, reports, charts, tables, SQL, notebooks, spreadsheets, market sizing, data quality, or semantic layers, whether or not Data is at-mentioned. Dashboards can use uploaded spreadsheets, CSVs, or TSVs as source data without making the deliverable a spreadsheet."
---

## ChatGPT web Chat mode stop gate (read first)

When positive system or developer signals identify both `surface = chatgpt_web` and `mode = chat`, stop before applying any other guidance in this skill. On the first turn of the analytics request, respond only with a concise recommendation to switch to Work Mode because Data performs best there. Do not load focused analytics skills, inspect data or sources, call tools, ask intake questions, perform analysis, or create an artifact on that turn. Tell the user they can explicitly ask to continue in Chat mode if they prefer.

Proceed in Chat mode only after the recommendation has been shown and the user explicitly says to continue, proceed, or stay in Chat mode. Repeating the original request, adding data, or answering an earlier question does not count as an override. Once the user explicitly overrides the recommendation, resume the original analytics request without making them restate it. Follow the Work Mode branch below for intake and persistence, keep `mode = chat` for delivery, and follow Response Mode below for the answer shape. Do not automatically publish to Sites. Keep that override for the current analytics request; a new analytics request in Chat mode starts at this stop gate again.

## Source Execution Gate

After the Chat mode stop gate clears, select the requested response mode and identify the authoritative source category and authority criteria before loading or starting any external helper, source-specific workflow, or full end-to-end answer router; verify the actual controlling source through the compatible narrow helper's governed discovery. Data owns the selected output, source authority, and final user-facing answer; compatible helpers return bounded reviewed evidence, rows, and provenance to Data without replacing that output or answer. Helpers return material caveats, not provider-formatted response text. External narrow helpers are evidence-only: their final-answer formatting, confidence, receipt, or response-delivery requirements never govern Data's final response; preserve genuinely required source citations, permalinks, and governance.

Before selecting a source-specific helper, inspect candidate skill frontmatter and prerequisite contracts without invoking their workflow, then check its actually callable or discoverable mandatory discovery tools and supported read-only execution modes. Prefer the narrowest directly relevant source, provider, or semantic-layer helper. Do not enter a workflow whose mandatory tools are unavailable or whose required engine is explicitly disabled. Do not invoke a second full end-to-end analytics or answer router merely for source discovery unless the user explicitly requests it or all prerequisites and its output/source contract are proven compatible.

For an ordinary user-requested read-only analysis with no named-source restriction, select an already-authorized, callable governed workflow that can independently verify and query the same controlling source. Follow its supported-engine rules and preserve the metric definition, population, filters, grain, period, dimensions, freshness, and privacy. Do not ask for extra chat confirmation merely to perform normal read-only execution. Never select weaker or conflicting sources, bypass tool or consequential-action approvals, or cross an already-selected workflow's explicit no-fallback boundary.

## Response Mode

Follow the user's requested output when they name one.

Use `inline` when the question can be answered with one or two charts and concise analysis.

Honor an explicit request for multiple inline charts even when several are needed; the requested output overrides the default chart-count guideline.

Use `report` when the answer needs more than two charts, several analysis steps, substantial explanation, or a durable artifact to share.

Use `dashboard` when the user wants monitoring, filters, exploration, or something they can revisit.

Choose the output from the user's requested deliverable, not the source format. For a dashboard request, load `$build-dashboard` as the primary workflow unless the user explicitly requests an Excel or Google Sheets dashboard. An uploaded or connected spreadsheet, `.xlsx`, `.csv`, or `.tsv` supplies data; its file format does not determine output.

For a broad performance question without a named metric or requested depth, ask whether they would like a quick inline analysis or a full report before querying.

If unsure, ask whether they would like a quick inline analysis or a full report.

A chat answer without a report or dashboard is `inline`. Before finalizing an inline answer:

- Answer the question directly.
- If the answer is about metrics, KPIs, changes, comparisons, trends, rankings, breakdowns, or multiple values, include a native inline visualization. On Codex Desktop, use Data's shared inline chart renderer and deliver its output through `visualize:visualize`; otherwise use the runtime's native inline visualization surface. If no native visualization is available, use the clearest compact table or prose fallback.
- For a metric or KPI, fetch available history and show a trend, even when the user asks only for the latest value or a period-over-period change.
- A source preview or provenance attachment does not count as the native visualization.
- End with: `This was a quick, high-signal analysis. Would you like me to build it out into a comprehensive report or dashboard to share with the team?`

If an inline answer grows through follow-up requests, offer to move it into a report or dashboard.

Focused analysis skills must not change the selected response mode. For reports and dashboards, pass reviewed evidence to the app workflow as soon as it supports a useful first view; continue the remaining requested analysis in the same app instead of waiting to finish every analysis step before building.

For report mode, consult `$visualize-data` when chart selection or implementation needs guidance.

### Inline Data Chart Delivery

Apply this section only after an `inline` response has been selected; do not replace an explicitly requested report, dashboard, notebook, export, or static output. For an inline chart or explicitly requested meaningful interactive visual, when `mode = work_mode` is positively identified on any surface, read [native-inline-visualizations.md](../visualize-data/references/native-inline-visualizations.md) directly and use the host-native `charts_widget_v2` or `app_block` surface with its live host-provided `genui` content reference. Native Work Mode rendering takes precedence over Visualize.

Otherwise, on Codex Desktop, read [inline-chart-renderer.md](../visualize-data/references/inline-chart-renderer.md). Resolve the absolute bundled Node executable with `load_workspace_dependencies`. Run `"<codex-node>" "<data-plugin-root>/skills/visualize-data/scripts/render-inline-chart.mjs" --input <reviewed.json> --output <absolute-chart.html>`. The deterministic renderer uses the actual shared React/Recharts `ChartRenderer`, `SourceSidebar`, dashboard styles, and selected theme, defaulting to `codex-classic`; it verifies the plugin's shipped data-free runtime and needs no npm install, network access, dependency cache, or per-chart runtime build. Then read and follow the installed `visualize:visualize` skill directly and in full for delivery; Data's shared renderer owns chart implementation and takes precedence over generic chart-authoring suggestions. Do not load `$visualize-data` for this inline handoff; that focused skill owns charts for reports, dashboards, notebooks, and other durable artifacts. Do not recreate the chart in D3, reproduce the source sidebar manually, duplicate dashboard styling, import the full Data app shell or theme runtime, or install dependencies for an inline chart.

Emit the actual Visualize content reference for the generated fragment in the same final response. For multiple requested inline charts, give each a stable, distinct chart ID and output filename, reuse the same shipped data-free runtime, and emit one actual Visualize content reference per chart in the same final response; never concatenate complete fragments or rebuild the runtime for each chart. A promised handoff, Mermaid diagram, Matplotlib image, code fence, downloadable HTML, or source preview does not replace an available inline chart. The actual dashboard source sidebar is root-contained and right-aligned, overlays the chart instead of opening below it, and preserves `Overview`, `Data preview`, `SQL query`, and `Evidence flow` without unsupported copy controls. Include raw SQL only when the user explicitly requests it and `--include-sql` is supplied; include source URLs only when the user explicitly requests them and `--include-source-urls` is supplied.

Return ordinary requested or lookup tables as Markdown. Use an interactive table only when explicitly requested and meaningful sorting, filtering, or exploration cannot be expressed by Markdown. Include only bounded, reviewed values needed for the chart; preserve material source links and caveats in concise surrounding prose without narrating methodology or exposing raw SQL unless explicitly requested. Preserve missing observations as `null` in the real measure; do not invent helper series or zero-fill missing values to force chart marks. Never embed hidden reasoning, credentials, tokens, direct personal contact or payment identifiers, or unnecessary sensitive fields.

If the shared renderer, its required execution environment, an approved writable fragment surface, or Visualize delivery is unavailable, use the runtime's available native chart surface or the upstream compact table/prose fallback.

## Eligibility gate (read before routing)
Use this plugin only when resolving the request requires structured records, numeric measures, quantitative evidence, a dashboard/metric definition, or a business/product decision grounded in such evidence. Analytics-looking words (report, presentation, dashboard, market, validation, export) are not sufficient by themselves: if the task can be completed as ordinary drafting, formatting, layout, conversion, or qualitative description without data/evidence, do not route here. Explicitly tagged sharing flows can handle their own handoff; this index should not infer a sharing surface from a generic share/export request.

Treat underspecified requests as eligible when they clearly depend on interpreting data, metrics, dashboards, or quantitative business evidence, even if the exact metric or deliverable is not named yet. Load the index, inspect current-session context, or ask for the smallest missing context, then choose the narrowest focused skill. Do not require a named metric upfront; do reject purely mechanical transformations, formatting, code fixes, syntax snippets, or generic explanations that do not require interpreting evidence.

When eligible, choose the most specific analytical skill; when uncertain, ask one clarification rather than opening a generic report/export skill.

## Launch/segment decision cue
Eligible product-analytics requests can ask for a product launch, rollout, prioritization, segmentation, experiment readout, A/B test interpretation, or ship/hold/iterate tradeoff recommendation under stated or to-be-collected assumptions/constraints. Treat those as analytics workflows when they cite metrics, confidence/uncertainty, guardrails, segments, or structured evidence, even when the first step is context collection; pair context with product-business-analysis.

## Metric definition/source-of-truth disputes
When teams disagree about which metric definition, dashboard, extract, owner, or source of truth should control a decision or executive reply (for example revenue/ARR, activation, retention, funnel, or regional totals), route as analytics even if the immediate output is a short Slack/email recommendation. Prefer `analyze-data-quality` for comparability/backfill/grain/source conflicts and `design-kpis` for canonical definition/guardrail ownership; use both when the request asks which definition should govern.

## Staged analytics workflow follow-through
If one request says to first ask for or collect owner, constraints, assumptions, or context and then use that information for an analytics decision, recommendation, dashboard, or report, do not stop after only asking the clarification. Load `$gather-business-context`, then the most relevant analysis skill. Ask the clarification after loading those skills if information is still missing. If the user requested a durable narrative deliverable, also load `$build-report`.



# Skill Purpose

Route broad Data requests to the right focused workflow. Treat invocation of this index as strong intent to use this plugin when the request needs quantitative evidence, source verification, metric reasoning, or a decision grounded in data; prefer focused analytics skills over generic report/export handling.

## Skill Configuration

### Runtime Routing

Classify `surface` and `mode` separately, and only from positive system or developer signals or genuinely exclusive tools:

- `surface = codex_desktop` when the environment is explicitly identified as ChatGPT Desktop or desktop-only `codex_app` tools are available.
- `surface = chatgpt_web` when the environment is explicitly identified as ChatGPT in a web browser.
- `mode = work_mode` when the environment is explicitly identified as Work Mode.
- `mode = chat` when the environment is explicitly identified as standard ChatGPT chat.
- Otherwise set the relevant value to `unknown`.

Never infer mode from surface, missing tools, tool failure, operating system, file paths, sandbox details, or network details. Explicit context overrides tool availability. When `mode = work_mode` is positively identified, apply one delivery rule regardless of whether the surface is web, desktop, or unknown.

After classifying `surface` and `mode`, select the most specific matching runtime branch:

| Runtime branch | Intake | Semantic-layer persistence | Output surfaces |
| --- | --- | --- | --- |
| ChatGPT web Chat mode (`surface = chatgpt_web`, `mode = chat`) | Apply the stop gate above before intake. After an explicit override, follow the Work Mode intake guidance below. | Do not create or update persistence before an explicit override. After an override, follow the Work Mode persistence guidance below. | Do not create outputs before an explicit override. After an override, follow Response Mode below and do not automatically publish to Sites. |
| Work Mode (`mode = work_mode`) | On ChatGPT Desktop, try `request_user_input` first and `$answers-ask-user-input` second. On every other surface, try `$answers-ask-user-input` first and `request_user_input` second. Follow the structured-intake retry contract below before using conversational choices. | Use existing user-provided or installed semantic layers as read-only context; do not create or persist context automatically. | Follow Response Mode below. Use the runtime's native inline visualization surface for inline answers. For durable reports, build the shared Data app and automatically publish that same app when the full Sites lifecycle is callable; otherwise retain its self-contained HTML. Build dashboards with the same app and publish only with explicit user approval. MCP servers and other callable tools remain valid data sources. |
| ChatGPT Desktop outside Work Mode (`surface = codex_desktop`) | Try `request_user_input` first and `$answers-ask-user-input` second. Follow the structured-intake retry contract below before using conversational choices. | Use existing user-provided or installed semantic layers as read-only context; do not create or persist context automatically. | For inline charts, run the shared Data React/Recharts inline renderer and deliver its fragment as native `visualize` structured output. Build reports and dashboards with the shared Data app and follow its single-preview delivery contract. Use a BI dashboard destination only when explicitly requested. Publish only after explicit approval. |
| Else: all other or unknown runtimes | Try `$answers-ask-user-input` first and `request_user_input` second. Follow the structured-intake retry contract below before using conversational choices. | Use existing user-provided or installed semantic layers as read-only context; do not create or persist context automatically. | Use output surfaces exposed by the runtime and focused-skill rules; default durable Data reports and dashboards to the shared self-contained web app. |

For ordinary analytics work using supplied context for the current answer, keep the context current-session only and continue through the relevant analytics workflow.

### Saved Data Context And Semantic Layers

Ordinary analytics workflows do not require saved data-context setup. Use current-session context from the request, conversation, connected source reads, uploaded files, pasted artifacts, local repo files, explicitly named semantic layers, or user-created semantic-layer skills discoverable in the current runtime. Analytics context stays current-session only and follows `Runtime Routing`; do not create or persist context automatically.

### Guided Flow And Source Setup

This index owns task selection, setup-adjacent routing, and guided workflow continuation. Apply its stateless first-task flow after plugin intent is established for get-started requests, open-ended prompt discovery, uploaded or demo data, and walkthrough questions. Send pure capability summaries to `Broad Orientation And Help Requests`. If the user already supplied a concrete task, skip intake and treat it as a custom question.

Use only the current conversation, visible installed plugins and skills, current-run tool results, uploaded or pasted context, and local files. Do not show a source, project, dashboard, table, SQL, file, connector, or provider picker. If the user asks to analyze data but provides no data, source, or discoverable callable source, ask for the smallest useful data artifact or offer the upload/sample fallback. Do not create saved data context from this flow unless the user explicitly asks for that.

#### First-task intake

Use the structured form contract below. The two standard structured-intake mechanisms are the native `request_user_input` action and the `$answers-ask-user-input` skill's `ask_user_input` widget. On ChatGPT Desktop, try `request_user_input` first. On every other surface or mode, try `$answers-ask-user-input` first.

If the first mechanism is unavailable, not callable, unsupported in the current mode, returns an error, or fails before rendering, immediately try the other standard mechanism with the same question and choices. Do not look only in the callable tool registry for `$answers-ask-user-input`: it is a skill, so inspect the runtime-provided skills inventory and read it before invoking its widget. Conversely, do not assume `request_user_input` is unavailable merely because the skill path failed; call it when the native action is exposed. A canceled or empty submission is a user response, not a rendering failure: defer the flow instead of opening a second form.

Only after both standard mechanisms are unavailable or fail may you try another equivalent native structured-intake action. Use concise conversational choices only after every exposed structured-intake path has been attempted. Do not fall back to conversational choices merely because the runtime is `chatgpt_web`, `work_mode`, or an unknown environment. Preserve the same option labels and meaning when adapting the contract to the alternate structured surface; if no structured intake renders, present those choices compactly in normal conversation.

Before presenting connected-source options, identify likely data lanes from the runtime-provided skills inventory, installed Apps and Plugins, recommended-plugin list, callable tools, current conversation, uploaded or pasted artifacts, local files, and discoverable semantic-layer skills. For analytics tasks, actively look for source-of-truth lanes such as warehouses or SQL databases, BI dashboards, product analytics systems, spreadsheets, source-definition docs, and relevant communication context; use callable tools, uploaded or pasted artifacts, local files, and current-run source reads to determine which lanes are immediately usable.

Use recommended plugins and installed plugin metadata to identify setup or install paths when a likely source lane is not immediately callable.

If `tool_search` is unavailable and the runtime exposes `ALL_TOOLS`, inspect `ALL_TOOLS` names, descriptions, and plugin provenance. Treat callable tools as stronger evidence of immediate source access than installation recommendations.

When any warehouse or source-system tool is callable, offer a warehouse-backed task first, following the source-of-truth ranking in Connected-source option copy.

1. If the user supplied a concrete task, skip intake and continue at `Custom-question access`.
2. Otherwise inspect only the runtime-provided installed Apps and Plugins inventory plus callable tools already visible in the session, including custom MCP servers and other callable tools that can read the needed source. Do not read connector records or treat `.app.json` declarations as installed. If tools are deferred, use `tool_search` when available; otherwise use the runtime's callable-tool registry, such as `ALL_TOOLS`. Query by the name, source type, or task-relevant capability of an already-visible or user-named connector, custom MCP server, or other callable tool to verify callability; do not search only a fixed provider catalog.
3. If at least one useful connected source exists, run the structured-intake retry sequence once with exactly three options: two distinct tasks backed by existing installed connectors or callable tools, followed by `Upload your own`. A failed rendering attempt does not count as a second intake; retry the alternate mechanism with the same three options. Prefer product/business analysis and metric diagnostics when the source supports those hero use cases; otherwise use the highest-value supported focused workflows. Prefer distinct source families; if fewer than two are useful, derive multiple non-duplicative tasks from the same connected source's capabilities. Never include sample, installation, or unsupported options.
4. If no useful connected source exists, offer exactly `Upload data` followed by `Use sample data`. Do not add `Connect a data source`.

Use `Dashboard`, `Report`, or `Data task` as the header. Ask `What should the dashboard be about?` or `What should the report be about?` when the artifact is known; otherwise ask `The Data plugin turns data into insights, recommendations, and decision-ready artifacts. Try it out with one of these prompts:`. Keep labels under 80 characters, omit recommendation suffixes, and preserve the built-in free-form Other field for a custom question. If every exposed structured-intake path is unavailable or fails, render the same choices compactly in chat. Canceled or empty submissions defer the flow.

Connected-source form: `{ id: "data_task", options: [{ label: "{connected task 1}", description: "{connected-source description 1}" }, { label: "{connected task 2}", description: "{connected-source description 2}" }, { label: "Upload your own", description: "Upload or paste your own data and answer an analytical question." }] }`.

No-source form: `{ id: "data_task", options: [{ label: "Upload data", description: "Upload or paste your data and answer an analytical question." }, { label: "Use sample data", description: "Analyze sample product-growth data." }] }`.

#### Selection handling

- Connected-source task: use its existing connector or callable tool and start the focused workflow implied by the option. Match the task to the focused skill's trigger rather than a fixed onboarding pair: for example, route recommendations through `$product-business-analysis`, metric movement through `$metric-diagnostics`, trustworthiness checks through `$analyze-data-quality`, KPI readouts through `$kpi-reporting`, and dashboard requests through `$build-dashboard`. For a pre-populated report task, include `$build-report` and add `$visualize-data` when a visual would clarify the result. Choose the controlling source automatically; do not open plugin installation. If the source unexpectedly cannot provide usable evidence, use the fallback form below.
- `Upload your own` or `Upload data`: ask for the smallest useful export, SQL result, data shape, screenshot, metric definition, or file, then wait.
- `Use sample data`: start the demo contract immediately without another confirmation.
- An explicit request to "use sample data" or "using the sample data" selects `Use sample data` when the user did not name or attach a different sample; resolve the bundled demo immediately instead of searching the workspace or asking for an upload.
- Other text: treat it as a user-authored custom question and continue at `Custom-question access`.

Do not ask the user to choose a provider, project, table, dashboard, query, or export. Do ask for the actual missing data artifact when no usable data or source is supplied or discoverable. Ask for source confirmation only when already-available sources conflict in a way that changes the answer.

#### Custom-question access

Only a concrete task supplied in the user's message or the intake form's Other field may trigger installation. Choose the focused workflow, then decide whether an existing plugin, app, connector, custom MCP server, other callable tool, uploaded or pasted artifact, local file, or current-run context provides enough fresh, authoritative evidence. If yes, choose the controlling source and start.

For missing evidence, check visible or lazy-loadable custom MCP servers and other callable tools that can read the needed source before native connector installation. Treat a custom MCP server or other callable tool as related when its server or tool name, description, action schema, or the user-named source indicates it can read the needed source category. Configured `preferred_plugins` and `.app.json` entries are routing hints, not the source universe.

If required evidence is still missing and a plausible connector lane exists, use the app categories in [.app.json](../../.app.json) to map source families and identify the declared app dependencies useful to the task. Treat those declarations as routing hints, not evidence that an app is installed, authorized, or callable. If current-run context already lists exact suppressed plugin-install ids, exclude those exact ids; do not run the legacy preflight just to obtain suppressions. Then call `functions.request_plugin_install` sequentially for every useful matching dependency, using only its exact `.app.json` `id`. Do not guess ids, narrow to one generic "best" candidate, stop after the first useful candidate, call installs in parallel, or use `request_connector_setup`. If no declared dependency matches, continue to the fallback question below. When an install is declined or unconfirmed, record that exact id with `record_plugin_install_suppression.py` and continue with other useful candidates. If `functions.request_plugin_install` fails or returns an error for a candidate, stop automated installation for that candidate and tell the user to open Plugins, find the candidate by its user-facing plugin name, and install or connect it from the plugin page. Do not expose the raw plugin id. Then continue to the fallback question below in the same turn.

Warehouse exception: if the custom task needs structured data, no warehouse is usable, and the user named none, keep every matching declared warehouse dependency. Ask which warehouse to use, naming all of them; install only the selected exact dependency. If one matches, offer it directly. Never choose by manifest order or configured preference.

If setup is unavailable, declined, unconfirmed, canceled, or still yields insufficient evidence, you MUST ask this fallback question before ending the same turn: `{ id: "fallback_next_step", question: "I don't have enough data to complete this task. How do you want to proceed?", header: "Next step", options: [{ label: "Upload data", description: "Upload or paste your data and answer an analytical question." }, { label: "Use sample data", description: "See a clearly labeled synthetic product-growth demo; it will demonstrate the workflow without answering the real-data question." }] }`. Do not add another custom option or recommendation suffix.

After successful setup, start the focused workflow automatically. Do not show post-setup flow-control choices.

#### No-source completion invariant

Any path that determines there is no usable data for the active task MUST offer `Upload data` and `Use sample data` before the turn ends. This includes no useful connected source, a required source being unavailable, an install tool being unavailable, `functions.request_plugin_install` failing or returning an error, an install prompt being declined, dismissed, canceled, or left unconfirmed, a successful install that still cannot return usable evidence, and a connected source that unexpectedly lacks sufficient evidence. When `functions.request_plugin_install` fails or returns an error, first tell the user to install or connect the named plugin from its plugin page, then offer the two fallback choices.

Do not end with only a missing-source explanation, an installation suggestion, or an instruction to connect a source and retry. An installation prompt may come before the fallback question, but it never replaces the fallback question unless setup succeeds and the source returns usable evidence in the current run. Use the exact `fallback_next_step` form above for concrete tasks. For `Use sample data`, say explicitly that the bundled demo is synthetic and will demonstrate the workflow rather than answer the user's real-data question.

#### Connected-source option copy

Treat a visible installed or callable surface as warehouse-like when its name, description, or actions indicate warehouse, SQL, query, table, schema, dataset, or database access. Rank useful options by source-of-truth fit: warehouse/source system first, then BI, product analytics, tabular Drive/files, GitHub, and finally the best-fit document or communication source. A task must remain executable through its connected source.

Use source-specific labels for non-warehouse tasks and keep warehouse labels provider-neutral. If one connector fills multiple slots, vary the task by real connector capability instead of repeating copy. These are defaults, not hidden prompts:

| Source | Label | Description |
| --- | --- | --- |
| Warehouse or source system: product/business analysis | `Analyze product or business performance` | Analyze warehouse or source-system data for trends, segments, opportunities, and recommendations. |
| Warehouse or source system: metric diagnostics | `Diagnose a key metric change` | Explain a metric movement and identify its largest supported drivers. |
| Warehouse or source system: data quality | `Assess data quality` | Check freshness, completeness, duplicates, schema or grain problems, broken joins, and trustworthiness. |
| Warehouse or source system: KPI reporting | `Prepare a KPI readout` | Summarize KPIs against trends or targets, explain supported drivers, and state operating implications. |
| BI/dashboard | `Analyze dashboard trends` | Analyze dashboard or BI data for trends, gaps, and follow-up cuts. |
| Product analytics | `Analyze product usage` | Analyze events, funnels, retention, experiments, and behavior changes. |
| Drive | `Analyze Drive files` | Analyze relevant Drive data for findings and next steps. |
| GitHub | `Analyze GitHub activity` | Analyze issues, pull requests, reviews, and blockers. |
| Email | `Analyze email trends` | Analyze threads for themes, trend signals, follow-ups, and next steps. |
| Calendar | `Analyze meeting patterns` | Analyze meeting topics, attendees, length, frequency, and next steps. |
| Notion | `Analyze Notion content` | Analyze pages and databases for project status, decisions, and themes. |
| Slack | `Analyze Slack activity` | Analyze messages for active topics, blockers, decisions, and follow-ups. |
| Teams | `Analyze Teams messages` | Analyze chats and channels for topics, actions, blockers, and decisions. |
| SharePoint | `Analyze SharePoint files` | Analyze relevant SharePoint data for findings and next steps. |

#### Demo data

Show `Use sample data` only when no useful connected source exists or a selected workflow still lacks usable evidence. Resolve [demo-product-growth.csv](../../assets/demo-product-growth.csv) relative to this skill, label it synthetic, analyze it with reproducible SQL without inventing rows or findings, and route it through `$product-business-analysis`. Use the selected response mode for visualization and delivery.

### Source Discovery And Verification

Use the relevant semantic layer as a starting map, not a boundary.

For dashboard builds, follow `$build-dashboard`'s bounded source plan and access rules.

1. **Start with the authoritative source.** Consider available source families, user-named sources, discoverable semantic mappings, and current evidence; select the strongest controlling source for the question. Verify its access, relevant definition, and freshness through the smallest governed native read or discovery step needed to support the answer.
2. **Expand only for a material gap or conflict.** Broaden discovery when the authoritative read is unavailable, insufficient, conflicting, or missing evidence that changes the answer. Compare overlapping sources by ownership, freshness, definition, grain, coverage, and directness; preserve known conflicts, combine complementary evidence only when necessary, and verify selected data through live reads before concluding.

### Source Access Guardrail

Before querying sources, building artifacts, or drawing conclusions, determine whether the answer requires a specific source of truth.

A broader, narrower, or differently defined metric is not equivalent to the requested metric; never silently substitute one or hide a material scope difference.

A dashboard title or an `overall`, `all`, or `total` label does not establish the requested population. When scope is ambiguous, use the smallest governed read necessary to verify the governing metric definition and actual source measure, filter, and population; prefer an available measure specific to the requested scope. If only a broader or narrower measure is available, do not relabel it as equivalent and disclose the limitation beside the chart.

If a required source is unavailable, stop that path. Tell the user what source is needed and do not treat weaker substitutes as equivalent. Then apply the mandatory `No-source completion invariant`: offer uploaded data or the clearly labeled synthetic demo before ending the same turn.

If the missing source is only optional enrichment, continue with the strongest available evidence and label the gap when it materially affects the answer.

### Suggest Automations

`suggest_automation` is a user-visible launcher; its click starts the separate hidden automation-creation flow. It is not a general next-step CTA.

Only the primary analytical skill may originate it, after the answer and any required report or dashboard handoff are complete, when fresh inputs, source and metric definitions, analysis steps, and intended output are stable enough to repeat and the runtime surfaces `suggest_automation`.

When eligible, add one short, concrete sentence saying what would repeat, then emit exactly one runtime-provided `suggest_automation` invocation with visible label `Make this repeatable`. In Work Mode, the expected live reference is `genui{"suggest_automation":{"label":"Make this repeatable"}}`; emit it without Markdown backticks and use the host-provided syntax if it differs. Keep the label generic: do not put cadence, metric or source names, delivery destinations, or setup detail in it. Do not ask cadence or delivery questions, call automation-creation tools, or create the automation in the same turn. If the runtime does not surface `suggest_automation`, omit the suggestion entirely instead of replacing it with a prose CTA.

The dashboard/report automatic-update handoff is the one narrow exception. After successfully delivering a report or publishing a dashboard to Sites with a source that can be read again without another upload, follow the selected skill's exact final-question rule instead of emitting `suggest_automation`.

Do not suggest it for one-off or exploratory work, bounded quick answers, templates or mockups, incomplete or blocked workflows, unstable sources or definitions, an already-automated workflow, or a workflow that already received a suggestion.

### Stakeholder-Facing Output

Keep stakeholder-facing inline answers and visible report or dashboard copy focused on the answer, evidence, implications, and caveats that change interpretation or action.

Do not include analysis process, methodology choices, source selection, query strategy, validation steps, chart-choice rationale, implementation details, rejected alternatives, or internal confidence scoring in visible titles, descriptions, captions, annotations, summaries, or prose. Keep that detail in source metadata, the source inspector, source notes, or supporting artifacts. Include methodology only when the user asks for it, the selected template requires it, or it materially changes interpretation or action.

For inline answers, state material metric-scope differences and partial-period limitations beside the chart. For dashboard or report artifacts, follow the focused build skill's presentation rules instead of duplicating qualifications across surfaces. Never reinterpret unrelated provider, retrieval, or classification scores as confidence in a metric or analytical conclusion, whether in source evidence flow or final prose.

Before finalizing, scrub invented or self-assigned numeric or qualitative answer-confidence ratings and remove anything that does not answer a user question, support a finding, or change interpretation or action. Preserve natural uncertainty, genuinely evidenced relevant statistical uncertainty, including confidence intervals, and material caveats. If the user explicitly asks for an answer-confidence rating, include one only when it has a genuine evidential basis; never invent a probability.

### Source Links

When referencing sources inline, prefer clickable Markdown links over plain bracket labels whenever the source exposes a useful URL. Use the source title, record name, channel/thread, or meeting/date as the link text, for example a clickable Markdown link whose visible text is `Meeting notes: May 19` or `Slack thread: May 15-21`. Use plain text labels only when no useful URL or stable connector-visible link is available, and say `(no useful link available)` when that absence matters.

### Routing

#### Run Order

Every Data plugin run follows this order:

1. Handle pure capability-summary requests with `Broad Orientation And Help Requests`; apply `Guided Flow And Source Setup` to open-ended action or prompt discovery, first-run task selection, explicit guided-flow requests, and setup-adjacent prompts that should choose and run a data task before deeper setup.
2. Use explicitly supplied or discoverable existing semantic layers as read-only context; never require saved-context setup before ordinary analytics work.
3. Choose and lock the response mode using `Response Mode` before selecting source helpers or loading focused workflows; do not infer the deliverable from a source file or connector.
4. Apply `Source Execution Gate` to retain Data's output and authoritative-source ownership before starting any external workflow.
5. Inspect relevant focused-skill frontmatter and candidate helper prerequisites; select the minimal primary/supporting skills and only necessary compatible narrow helpers, keeping `$build-dashboard` primary for dashboard requests unless the user explicitly requests an Excel or Google Sheets dashboard, then do one companion-skill pass across installed skills for clearer non-analytics surfaces, semantic layers, or methods that pass `Source Execution Gate`.
6. If the user names an existing semantic layer or a relevant layer is already discoverable, use it as context without changing the selected output or creating saved context.
7. Read and follow only the selected skill bodies before source queries, report building, supporting-skill execution, or final drafting.
8. Apply Source Discovery And Verification and the Source Access Guardrail through bounded, authoritative-first governed reads before drawing conclusions or building artifacts.
9. Return reviewed evidence, rows, and provenance from source helpers to the selected Data workflow; preserve Data's selected response mode and final-answer ownership.
10. Before final response, apply Response Mode's completion gate, then the focused workflow's completion gates. Saved-context creation is never a prerequisite for ordinary analytics work.

#### Skill Selection

- Pick the smallest useful set of primary/supporting skills.
- For report-mode runs, state the selected route once in a progress update, such as `Route: product-business-analysis + product semantic layer + build-report`.
- Use this index's guided gate for source/task setup across all Data skills, including explicit setup, get-started, first guided workflow, setup-status, offline/demo fallback, walkthroughs, and active guided-flow continuation requests. Keep that gate free of unsolicited saved data-context or semantic-layer creation.
- For requests to create or change a recurring refresh job for an existing Data dashboard, including "keep this dashboard up to date," read and follow [$schedule-refresh-jobs](../schedule-refresh-jobs/SKILL.md) as the primary workflow. Schedule setup does not run the refresh or rebuild the dashboard.
- For a dashboard request without an explicitly requested Excel or Google Sheets destination, load `$build-dashboard` as the primary workflow even when its source is an uploaded spreadsheet, `.xlsx`, `.csv`, or `.tsv`. Spreadsheet skills may support read-only source ingestion; they must not create or edit a workbook, own the deliverable, or redirect the output to Excel or Google Sheets unless the user explicitly requests that destination.
- Treat a plugin mention as a starting point, not a source boundary. Add an installed external skill only for a necessary, narrow complementary source, semantic, method, or delivery task that passes `Source Execution Gate`; Data retains the selected output and final-answer ownership.
- When the user asks to share a summary of a dashboard, report, chart, or component, read and follow [$share-artifact-summary](../share-artifact-summary/SKILL.md).
- Do not maintain worked route recipes here. Once selected, the chosen skills own detailed step order, supporting triggers, and output contracts.
- When a request maps to a primary workflow, load that workflow skill directly. For example, a KPI design prompt must read `$design-kpis`, a dashboard prompt must read `$build-dashboard`, a TAM/SAM/SOM prompt must read `$market-sizing`, a metric movement prompt must read `$metric-diagnostics`, and a recommendation-oriented product or business decision prompt must read `$product-business-analysis`.

If several focused skills apply, sequence them in the order that creates the most useful analyst workflow. For example, metric diagnostics may precede KPI reporting, semantic-layer setup may precede dashboard or report work, and product-business analysis may feed a recommendation-ready report. Keep this index as a router; do not perform focused workflow logic here.

Prefer examples that route to focused skills without extra setup, such as:

```text
@Data diagnose why a key business metric moved last week.
@Data build a KPI framework for the product activation funnel.
@Data analyze paid workspace retention and recommend what to investigate next.
```

For follow-up messages such as "yes", "walk me through it", "what happened?", or "show the steps" immediately after a completed guided workflow offers a walkthrough, answer from this index. Explain the observable steps, selected workflow, connector setup attempt, offline or demo-data fallback, clarifying questions, source gaps, and artifact assembly at a beginner-friendly level without revealing hidden reasoning.

### Broad Orientation And Help Requests

For broad orientation and help requests:

- Handle broad capability-summary asks from this index before choosing a focused workflow.
- Route pure capability-summary requests such as `what can you do?`, `show me the capabilities`, or `explain Data` here when the user wants orientation rather than a task choice.
- Route `what should I try?`, `what should I do?`, `let's do something`, `get started with a first task`, `how do I use Data?`, or `choose a guided workflow` through `Guided Flow And Source Setup`.
- Use this index-level help answer for capability summaries regardless of setup history; only explicit setup requests enter setup-specific handling.
- Answer from the skill map in this file using the default shape below.
- Keep the three generic examples below for capability and plugin-detail presentation. The two connected-source tasks plus `Upload your own`, or the no-source upload/sample fallback, belong only to structured first-task intake.
- Include a short setup context section only when the user asks about setup, available sources, Data configuration, or the current session already reveals a material source gap.
- Keep setup context analyst-facing: name the practical source, use model judgment to explain the likely user-experience impact from the source label, configured preferred routes, setup action, and suggested next prompts, then give the smallest next action or fallback.
- Show at most three highest-impact gaps by default, and never more than five setup-context bullets total. Prioritize gaps in the order most relevant to the examples you are suggesting rather than following a hard-coded impact catalog.
- If all sources are active, keep setup context to one sentence such as `Your core Data sources look ready; I'll still try each source only when a workflow needs it.`
- For setup context wording, be direct and practical, for example: `You won't be able to properly validate a metric from live tables until a warehouse or SQL source is available, but you can paste SQL, schema details, or exported query results for now.`
- Do not expose raw status names, connector ids, or implementation terms.
- Do not perform connector reads merely to answer a capability question; use current session app or tool availability already visible in context.

Use this default answer shape for broad orientation and help requests:

```md
Data can help with:
- Metric diagnostics and source-backed explanations for movement
- KPI design, metric definitions, and measurement frameworks
- Product and business analysis for funnels, retention, adoption, pricing, and strategic decisions
- KPI reports, dashboards, notebooks, and reusable semantic layers
- Market sizing, opportunity sizing, and decision-ready recommendations

Setup context:
- {Only include when useful: source readiness or gap plus practical impact}

Good first prompts:
- `@Data diagnose why a key business metric moved last week.`
- `@Data build a KPI framework for the product activation funnel.`
- `@Data analyze paid workspace retention and recommend what to investigate next.`
```

# Plugin Purpose

Data turns connected or provided business data, source-of-truth context, dashboards, docs, chats, notebooks, spreadsheets, SQL, and semantic layers into source-backed analytical work products. It can define KPIs, diagnose metric movement, size markets, analyze product or business questions, validate data quality, gather context, build reproducible notebooks, design visualizations, create dashboards, produce polished reports, and convert those outputs into shareable Docs, Slides, spreadsheets, or other durable handoff surfaces.

## Semantic Layers

Semantic layers are source-backed local skills for product, business, metric, source, or reporting areas. They encode canonical metrics, tables, grains, joins, filters, query patterns, caveats, source precedence, and validation gaps.

Before answering questions about a named product area, metric, table, dashboard, SQL query, source choice, join, caveat, or recurring business question, use a semantic layer only when the user names a semantic layer, semantic-layer skill, or path, or a relevant semantic-layer skill is already discoverable from the current runtime. If a relevant semantic layer exists, read it before selecting tables, writing SQL, reconciling dashboards, or giving metric definitions. Treat it as the domain-specific semantic map, then consult the connected or provided apps and verify high-stakes claims against the layer's cited sources.

Semantic layers may guide source selection, analysis conventions, and explicitly requested SQL delivery, but they do not broaden the user's requested output. Apply a semantic-layer preference to include full SQL in native answer prose only when the user explicitly requests SQL or query methodology. For Desktop inline answers outside Work Mode, the Sources receipt keeps recorded SQL and safe source links inspectable without printing them in the answer; follow its delivery reference below. Other runtime and legacy chart disclosure rules remain unchanged.

When no relevant semantic layer exists, continue from the authorized sources and current-session context available for the requested analysis. Do not merge unrelated product areas into one broad layer unless the user explicitly asks for a cross-product semantic layer.

## Evidence And Handoff

Data plugin files use lane placeholders such as `~~structured_data` for whatever tool, connector, MCP server, plugin skill, pasted result, uploaded file, or schema description is available in that category. The configured apps and their categories live in this plugin's [.app.json](../../.app.json); treat it as the canonical mapping for which configured apps can satisfy each category. Other discoverable apps, custom MCP servers, and callable tools can also satisfy a category when they credibly expose equivalent information. When a required connector, plugin, MCP server, or source-of-truth lane is unavailable, follow the Source Access Guardrail. When an optional lane is unavailable, continue from pasted query results, uploaded files, SQL snippets, screenshots, schema descriptions, or other reviewed evidence and label the gap when it materially affects the answer.

Source rules:

- Gather source-of-truth context before writing SQL, notebook code, dashboards, reports, or conclusions.
- Prefer reproducible notebooks for fresh SQL, Python, statistics, modeling, source reconciliation, or non-trivial metric computation when a notebook materially improves auditability.
- Preserve relevant SQL, scripts, query permalinks, outputs, source links, and caveats in the final artifact or supporting notes.
- Keep query provenance separate from the visible answer. Do not paste or reproduce source SQL in the final chat response or reader-facing report narrative unless the user explicitly asks to see, write, review, debug, or receive SQL or query methodology.
- For ordinary data questions, lead with the answer, evidence, and material caveats. Keep full SQL in `source.query.sql`, a source modal, a query permalink, a notebook or query file, or supporting notes; a source permalink or source action is sufficient in the visible handoff.

Delivery surface boundary:

- Inline answers follow Response Mode above. For every source-backed Desktop inline answer outside positively identified Work Mode, including text-only answers, follow [Inline Sources receipt](../visualize-data/references/inline-sources-receipt.md) to deliver one collapsed receipt after the native answer. Source previews and provenance are separate from native visualizations and do not satisfy the inline visualization requirement. Leave existing chart source interactions unchanged.
- Dashboard and report routes each apply the shared [Data App Contract](../../shared/data-app.md) for reviewed data, runtime behavior, build, and technical QA. Their focused skills retain their own content and publication policies.
- In Work Mode on any surface, treat generated web apps as unavailable for inline display. Build the shared report app and automatically publish that same compiled app when the full Sites lifecycle is callable; retain the self-contained HTML when Sites is unavailable or publishing fails.
- On desktop, open the compiled `file://` HTML directly or reuse the app's existing Sites preview. Sites availability alone does not require project or dev-server setup; follow the shared contract's preview policy.
- Offer Sites publication as an optional coworker-sharing follow-up and invoke `$publish-artifact-to-sites` only after the user explicitly requests or accepts it. Development preview is not publication.
- Default to the Data app for dashboard creation and editing. Use BI tools as data sources unless the user explicitly chooses a BI dashboard destination. Unpublished desktop previews return to `codex://threads/<user-facing-task-id>?prompt=<encoded-prompt>` using transient build metadata: valid `CODEX_SESSION_ID` first, then `CODEX_THREAD_ID`. Publication removes that metadata and always starts a new task: desktop uses `codex://threads/new?prompt=<encoded-prompt>&browserUrl=<clean-canonical-Site-URL>`; web uses `https://chatgpt.com/?q=<encoded-prompt>`. Never put task IDs in prompts, canonical URLs, shared links, or published artifacts.
- Do not expose hidden reasoning, credentials, secrets, direct personal contact/payment identifiers, or unvalidated calculations in any user-facing surface. Reviewed customer, account, or company names may be included when they are needed for the analysis.
- Once the analysis commits to a source table in an inline or dashboard route, expose a small deterministic source preview when safe through the selected surface's normal preview mechanism. This preview is separate from any required inline visualization.
- If a preview is unsafe, unavailable, or blocked by access limits, record that briefly and continue from schema, documentation, or other reviewed evidence.

## Completion Gates

Report completion:

- Once a report-mode analysis has findings, the run is incomplete until the shared report app produces a verified `dist/index.html`, a Site using that same build is published, or a concrete build blocker is recorded. Do not silently downgrade to chat prose, a notebook, loose charts, or an inline widget.
- Build one report app through `$build-report`; local and hosted delivery must use the same source tree and compiled UI.
- In Work Mode, publish the shared app automatically when the full Sites lifecycle is callable. Otherwise, follow the shared delivery contract and publish only with explicit approval.
- Do not replace the verified report artifact with only an inline/chat summary or preview URL. Treat chat summaries as progress updates.
- If a required deliverable is skipped, include the explicit omission reason in the final handoff.
- Every report must satisfy the shared Data App Contract. The same verified `dist/index.html` is the report and the conversion source for PDF, Google Docs, or Google Slides; do not maintain a second renderer or sidecar runtime.

Final review:

- Use the shared build and delivery checks for Data apps; do not add a browser QA pass. Inspect other generated artifacts in their requested format.
- Check source-backed claims against the controlling sources used for the analysis.
- Call out unresolved gaps or caveats when they materially affect the conclusion.
- Verify that every selected primary workflow skill was read and followed. If a primary workflow was skipped, record why in the final handoff. Do not treat a semantic-layer lookup, notebook, validation pass, visualization, or report artifact as satisfying the primary workflow contract.
- If the run was classified as `report`, do not finalize until the downstream $build-report contract has either passed or been explicitly blocked.
- If a selected rendering surface is unsafe, unavailable, too large, or fails after a targeted retry, continue the analysis through another appropriate surface and briefly note the reason in the progress update or final handoff.

## Skills

### publish-artifact-to-sites

Use $publish-artifact-to-sites to publish the already-built shared report app in Work Mode, or after an explicit Sites request or accepted sharing offer outside Work Mode. It must deploy the same compiled UI and Worker used by the local report; dashboard publishing follows `$build-dashboard` and requires explicit user authorization.

### share-artifact-summary

Read and follow [$share-artifact-summary](../share-artifact-summary/SKILL.md) to share a concise, source-backed dashboard, report, chart, or component summary. The sharing skill owns destination selection, source-link safety, and delivery.

### schedule-refresh-jobs

Read and follow [$schedule-refresh-jobs](../schedule-refresh-jobs/SKILL.md) to create or update a recurring refresh job in a cloud task for an existing Data dashboard. The scheduling skill owns cadence intake, cloud-task setup, exact job identity, refresh instructions, and verification; `$build-dashboard` owns each refresh run.

### design-kpis

Use $design-kpis for goals, primary KPIs, driver metrics, guardrails, scorecards, measurement plans, and launch or experiment success criteria.

### kpi-reporting

Use $kpi-reporting for KPI updates, scorecards, business reviews, executive metric summaries, target or pacing readouts, and leadership-ready performance narratives. Add $metric-diagnostics when the update must explain why a KPI moved.

### market-sizing

Use $market-sizing for TAM/SAM/SOM, opportunity, spend or revenue pool, customer count, unit volume, commercial upside, and sensitivity models.

### metric-diagnostics

Use $metric-diagnostics to identify what drove a metric over a defined time period, baseline, or segment comparison, rule out measurement artifacts, and label findings by certainty.

### product-business-analysis

Use $product-business-analysis to analyze product or business data and context for recommendation-oriented decisions. Add $metric-diagnostics when the recommendation depends on validated metric movement.

### analyze-data-quality

Use $analyze-data-quality for freshness, grain, row counts, nulls, duplicates, schema drift, broken joins, outliers, backfills, and source or dashboard disagreement.

### build-dashboard

Use $build-dashboard for the shared Data app, source-backed scorecards, monitoring pages, and dashboard QA. Use BI tools as data sources, not the default destination. Publish only with explicit approval.

### build-report

Use $build-report to build exactly one durable report surface selected for the user request, with data visualizations when the analysis benefits from them.

### convert-to-doc

Use $data-analytics:convert-to-doc for an explicitly requested DOCX or native Google Doc when an existing Data app is identified. If no Data app exists, ask the user to choose whether to build a dashboard or a report, invoke $build-dashboard or $build-report for that choice, and then invoke $data-analytics:convert-to-doc once the chosen app is built and verified.

### convert-to-slides

Use $data-analytics:convert-to-slides for an explicitly requested PPTX or native Google Slides deck when an existing Data app is identified. If no Data app exists, ask the user to choose whether to build a dashboard or a report, invoke $build-dashboard or $build-report for that choice, and then invoke $data-analytics:convert-to-slides once the chosen app is built and verified.

### report-to-pdf

Use $report-to-pdf for an explicitly requested PDF. Build or reuse the shared report app once, then invoke the canonical PDF plugin with its verified HTML and source evidence rather than rebuilding it.

### gather-business-context

Use $gather-business-context for docs, dashboards, chats, planning notes, launch or experiment material, source-of-truth pages, owners, incidents, roadmap, GTM or customer context, and prior decisions.

### jupyter-notebooks

Use $jupyter-notebooks to create, edit, and verify reproducible notebooks for SQL, Python, statistics, modeling, cohort or funnel analysis, data-quality checks, experiments, market sizing, diagnostics, and report support.

### validate-data

Use $validate-data to QA methodology, source selection, SQL or query logic, calculations, visualization integrity, caveats, and whether conclusions are supported by evidence.

### visualize-data

Use $visualize-data to design, implement, and QA charts for reports, dashboards, decks, notebooks, and other durable artifacts. Inline Codex answers use Data's shared React/Recharts inline renderer and native `visualize` structured output through `visualize:visualize`.
