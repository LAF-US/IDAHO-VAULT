# Data

Data helps you answer product and business questions with data you can trust, then turn the findings into shareable reports, charts, dashboards, notebooks, and recommendations.

## When to use this plugin

Use Data when a product or business decision depends on metric-backed evidence: understanding performance, explaining a metric movement, deciding where to focus, defining KPIs, checking whether data is reliable, or sizing an opportunity. Start with connected warehouses, BI or product analytics tools, docs, chats, spreadsheets, uploaded files, pasted results, or clearly labeled sample data.

## Get started

Try asking:

`@Data Help me get started with my first data task`

The plugin will help you choose a data source, pick a useful workflow, and decide whether to use connected tools, upload data, paste results, or try sample data.

Already have a focused task? Start directly with one of the workflows below.

## Example workflows

| Workflow | Try this | Skill | Result |
| --- | --- | --- | --- |
| Analyze a product or business question | `Analyze activation and recommend where to focus next` | `product-business-analysis` | A decision-ready analysis with evidence, measurable opportunities, and a clear recommendation |
| Diagnose a metric movement | `Diagnose why weekly active users dropped last week` | `metric-diagnostics` | A calibrated explanation of verified drivers, likely contributors, unresolved questions, and next actions |
| Design KPIs | `Design a KPI framework for this new product area` | `design-kpis` | A measurement plan with outcome metrics, drivers, guardrails, targets, and validation priorities |
| Prepare a KPI readout | `Turn this month's metrics into a leadership-ready operating update` | `kpi-reporting` | A concise KPI update with actuals, comparisons, validated drivers, and operating implications |
| Build a dashboard | `Build a dashboard for monitoring activation, retention, and conversion` | `build-dashboard` | A source-backed dashboard with metrics, filters, visual hierarchy, QA, and handoff |
| Size a market | `Estimate the market opportunity for this product and show the assumptions` | `market-sizing` | A transparent market or opportunity sizing estimate with sensitivity, uncertainty, and validation priorities |
| Build an analytical report | `Create an executive report explaining the biggest growth drivers this quarter` | `build-report` | A polished report with answer-first narrative, charts, tables, caveats, and source metadata |
| Improve or render a chart | `Turn this analysis into a clear chart for the product review` | `visualize-data` | A production-ready visual with the right chart type, labels, hierarchy, and accessibility checks |
| Create a notebook | `Build a reproducible notebook for this experiment readout` | `jupyter-notebooks` | A clean SQL or Python notebook that can be skimmed, rerun, and extended |
| Validate an analysis | `Review this analysis before I share it with leadership` | `validate-data` | A QA pass covering methodology, sources, calculations, analytical pitfalls, caveats, and conclusion strength |
| Assess data quality | `Check whether this table is reliable enough for our retention analysis` | `analyze-data-quality` | A source-backed quality assessment covering grain, freshness, missingness, duplicates, joins, and material risks |

## Integrations

Data can use available tools when they are connected:

| Source | Supported integrations | What they unlock |
| --- | --- | --- |
| Warehouses and query tools | Databricks, Databricks Genie, BigQuery, Snowflake | Schema inspection, query-backed analysis, and source-grounded metric investigation |
| Product analytics and BI | Amplitude, Mixpanel, PostHog, Omni Analytics, Metabase, ThoughtSpot, Statsig | Behavior analysis, dashboard context, experiment evidence, and reusable reporting inputs |
| Notebooks and analytical workspaces | Hex, Deepnote | Reproducible analysis, notebook handoff, and shared analytical context |
| Docs and collaboration | Google Drive, SharePoint, Notion, GitHub, Slack, Microsoft Teams | Business definitions, source-of-truth documents, implementation context, and stakeholder evidence |
| Email and calendar | Gmail, Outlook Email, Outlook Calendar | Supporting context for stakeholder questions, operating cadence, and analytical handoff |

You can also start with spreadsheets, uploaded files, pasted query results, schema descriptions, or manually provided business context.

## Inspect inline answers

Source-backed Desktop answers include a collapsed Sources receipt. Expand it to inspect recorded definitions, filters, sources, preview rows, SQL/Python or calculations, and evidence when available. The receipt uses the dashboard/report source inspector with Athena's compact card layout; it does not require Athena or change existing chart source buttons. See [Inline Sources receipt](skills/visualize-data/references/inline-sources-receipt.md) for its evidence and delivery contract. Work Mode retains its existing rendering path.

## Maintaining authoring guidance

Change each rule at its owner and link to it from the decision that needs it:

| Guidance | Owner |
| --- | --- |
| Report analysis, composition, and next-step selection | [build-report](skills/build-report/SKILL.md) |
| Report wording and presentation examples | [narrative-style](skills/build-report/references/narrative-style.md) |
| Dashboard composition and monitoring behavior | [build-dashboard](skills/build-dashboard/SKILL.md) |
| Chart selection, contextual annotations, and visual QA | [visualize-data](skills/visualize-data/SKILL.md) |
| Shared source, revision, and delivery workflow | [Data App Contract](shared/data-app.md) |
| Copied-app APIs and runtime constraints | [template AGENTS.md](templates/data-app/base/AGENTS.md) |

Keep essential decisions in the owning skill; load references for conditional detail and examples. The copied app retains the API constraints needed to revise it independently. Worked examples illustrate these rules, not alternate instructions or mandatory outlines. Keep development plans, review logs, and validation receipts in the PR or local working artifacts, not in the installed plugin.
