---
name: visualize-data
description: "Design, build, revise, or QA quantitative charts and figures for reports, dashboards, notebooks, and other durable artifacts. Do not use for inline chat charts."
---

## Related Skills

Use $metric-diagnostics when the visual needs an explanation of a metric movement.

Inline Codex answers use Data's shared React/Recharts inline renderer and `visualize:visualize` delivery.

Use $build-report when the visual is part of a durable analytical report.

# Data Visualization

Create quantitative visuals that are analytically sound, immediately readable, and polished enough to ship in a report, memo, slide, dashboard, notebook, or HTML artifact. Use each chart's analytical question or supported takeaway to plan the visual; dashboard takeaways remain private planning context unless the user explicitly requests visible commentary. Redesign charts that are visually attractive but analytically weak, and revise charts that are technically correct but hard to interpret.

## Runtime Delivery Routing

Inline Codex answers are not owned by this skill. The Data index invokes its shared React/Recharts inline renderer directly and delivers the resulting fragment through `visualize:visualize`.

Whenever the selected surface is a report or dashboard, apply the [Data App Contract](../../shared/data-app.md). Define each visual with `ChartRenderer` or a source-backed custom React/Recharts component, back it with reviewed query rows and exact source metadata, and keep stable authored component and query IDs. Preserve the single **Copy link** action in every published component menu: charts use `/_data/charts/<target-id>`, while non-chart metrics, tables, text, and custom widgets use `/_data/components/<target-id>`. The target is an eight-character base64url alias derived from the first 48 bits of the canonical-Site-origin/authored-ID UUIDv5 without changing DOM/presentation identity or persisting a mapping; previously issued full-UUID/readable component/chart links and chart `/detail` URLs remain backward-compatible. Keep copied URLs free of readable component names, query parameters, fragments, credentials, tokens, and task IDs, and never present an opaque locator as a secret or component-scoped access to a whole-dashboard snapshot.

## Chart Selection

| Data relationship | Best chart | Use it well |
|---|---|---|
| Trend over time or ordered axis | `line` | Show enough points to reveal shape; use `area` only when filled magnitude helps, and `sparkline` only in dense KPI cards |
| Composition over time | `stackedArea` | Use when parts should read as one total; switch to `line` when comparing component trajectories matters more |
| Comparison across categories | `bar` | Sort when order is not semantic; use horizontal bars for long labels; avoid redundant legends |
| Ranking or top-N | `rankedList` | Use the shared theme-aware Leaderboard; start with five rows, fill a taller adjacent card, and retain Show more |
| Part-to-whole composition | stacked `bar` | Keep the denominator explicit; use `pie` only for a rough read with few slices |
| Distribution or spread | `histogram` | Use numeric bins that reveal shape; switch to `boxPlot` when comparing groups is the point |
| Distribution across groups | `boxPlot` | Use when median and spread matter more than full shape; switch to `histogram` when shape needs space |
| Relationship between two numeric variables | `scatter` | Use numeric x and y at a meaningful observation grain with enough distinct points to show a pattern; retain point labels, sample/volume fields, and one useful grouping candidate when safe |
| Dense two-dimensional pattern or cohort matrix | `heatmap` | Use for matrix shape or intensity; switch to `scatter` when point-level variation matters |
| Additive bridge from start to end | `waterfall` | Use only when drivers sum cleanly to the end value; otherwise use ranked `bar` |
| Ordered stage progression or drop-off | `funnel` | Use only for ordered single-series stages; prefer stage `bar` when funnel geometry distorts comparison |

When the user has not specified a time range or granularity, choose them together from the analytical question, metric cadence, source timescale, and intended comparison: use enough history and a fine enough grain to reveal meaningful cycles and changes, but avoid detail that adds noise or unnecessary query cost. Treat this as an adaptive default rather than a fixed rule, honor an explicit user-selected range or grain unless it is incompatible with the metric definition or source constraints, and refine the range or grain deliberately if the first result is too sparse or noisy.

For dashboard charts, a descriptive title can replace a redundant x- or y-axis title when the categories, ticks, and units already make that dimension obvious. Keep explicit axis titles for ambiguous measures, scatterplots, nonobvious units, or comparisons whose dimensions cannot otherwise be identified. Format each reviewed category consistently across its axis, tooltip, direct label, and legend. Preserve the shared readable axis-label font size; resolve dense dates or long categories by removing intermediate ticks, formatting dates compactly, or truncating labels with accessible full text, never by shrinking type or clipping text. Center donut summaries inside the actual ring, keep legends compact and responsive, and never allow chart annotations or tables to escape their component.

Geographic visuals called maps must use actual projected geographic geometry and truthful geographic coordinates. Reuse the shared world-map asset where available; otherwise choose a clearly labeled regional or country bar chart. Every map marker needs a visible custom tooltip on pointer hover and keyboard focus with its reviewed place, relevant values, and reporting period; an SVG `<title>`, browser-native tooltip, or inaccessible `aria-label` alone is not enough. Decorative regional buckets, schematic blobs, or bubbles at arbitrary locations are not maps.

## Workflow

1. Identify the analytical question, intended comparison, and context needed to make the visual honest. For dashboards, do not put takeaways in visible titles, captions, or commentary unless requested.
2. Choose the simplest defensible family and variant for the reviewed data. Reuse the active report/dashboard workflow; use `$validate-data` only when the supporting analysis needs validation. Do not require separate chart contracts or per-chart skill handoffs.
3. Select the delivery path that matches the final surface.

   - Use the selected report, dashboard, BI, notebook, slide, or static HTML surface's native chart primitives only when the user explicitly selected that surface or the active report/dashboard workflow selected it before chart rendering.
   - For reports and dashboards, render reviewed data directly with React and Recharts through the shared Data App Contract.
   - Outside the Work Mode native-render failure fallback, use static Python charting only when the user explicitly asks for Python, a standalone static image/file, or notebook-oriented output. Choose a reproducible local renderer and export the requested format. Do not use that path as the default for HTML reports or dashboards.
   - Use governed BI or dashboard-native widgets when that surface owns rendering.
   - Implement bespoke local HTML/CSS/SVG/canvas/JavaScript only for an explicitly selected non-report, non-dashboard output whose required interaction cannot be represented by the chosen surface. Report and dashboard charts use the shared React/Recharts app; custom visuals still preserve stable component and query identities, reviewed rows, source inspection, and accessibility.

4. Build with the selected surface's primitives, reviewed rows, honest labels, and shared styling. Do not fabricate data or substitute demo rows unless sample data was requested.
5. For Data apps, show the first useful built version through the shared delivery contract, then complete the requested scope in the same app. Do not take screenshots, inspect the DOM, or run click/resize sweeps unless the user requests browser testing or you are troubleshooting a specific reported failure. Broad runtime QA belongs to plugin maintainers.

## Standards

### Selection Rules

Start from the analytical question and comparison the reader needs to make, not from a favorite chart type. Keep the top-level set small:

- `Tables & Scorecards`
- `Trend`
- `Comparison & Ranking`
- `Composition`
- `Distribution`
- `Relationship`
- `Uncertainty & Benchmark`
- `Matrix & Cohort`
- `Decomposition & Progression`

Concrete forms such as `highlighted multi-series line`, `Likert`, `pie`, `Pareto`, `waterfall`, `faceted dot & interval`, and `cohort heatmap` are variants inside these families, not peer families.

- For dashboards, follow the [dashboard composition decision](../build-dashboard/SKILL.md#decide-what-the-reader-needs). For standalone visuals and reports, render comparisons and patterns as charts when the evidence and delivery surface support them; retain tables for exact lookup and honor explicit table/prose requests. Sparse evidence or an unavailable surface is not a reason to invent a chart.
- Do not choose `line` merely because the prompt says "trend" or "trending". Decide first whether the reader needs current status, movement, variance to plan, mix, concentration, drivers, progression, or distribution.
- Choose a form the available evidence supports. For a few discrete periods, use KPI cards, grouped bars, a slope chart, or a table instead of implying a detailed trend. Query more history or finer detail only when the analytical question requires it, not to meet a point-count target.
- Use scatter charts for meaningful relationships among comparable observations; a table, bar, or dot plot may communicate a few observations more directly. Keep plotted rows at the same grain, and do not mix totals, averages, and detail rows in one scatter.
- For scatter charts, choose x and y measures that can plausibly vary independently and share the same denominator, time window, population, and filters. Include the denominator, sample size, or volume metric used to judge reliability, and use a size encoding only when that third metric materially changes interpretation. Add a point-label field for small or executive-facing scatters, and retain a meaningful categorical field such as segment, plan, route, product line, model family, or region for optional color or filtering. Avoid coloring by a unique row id; use labels or the table for exact identity instead.
- Use horizontal bars for long labels and sorted bars when order has no semantic meaning.
- Use compact leaderboard-style ranked bars only for top-N previews with one numeric value and 3-8 visible rows. Default to 5-6 rows in compact dashboard cards. Use a paginated table for long-tail browsing or exact lookup, Pareto for cumulative concentration, and waterfall for additive start-to-end driver bridges.
- When more than about six or seven mutually exclusive additive categories make a time-series legend or tooltip unreadable, first verify that every population is exclusive and the measure is additive, then explicitly set `groupOther: true`. Retain the same leading categories across the complete reviewed window and combine the remaining reviewed values into an explicitly labeled `Other` series at each period. Reconcile every displayed period to its reviewed total, preserve the complete original rows in source inspection, and keep strategically important cohorts separate. Never infer additivity from field names or sum overlapping populations, percentages, averages, or per-user rates; recompute ratios from reviewed numerators and denominators when valid or retain the original categories.
- For continuous histograms, make neighboring bins nearly touch. Ordered numeric bands, bins, buckets, and time intervals automatically use narrow gaps; use `distribution: true` for other reviewed pre-bucketed numeric or temporal distributions and `distribution: false` when distinct category spacing is intentional. Preserve normal spacing when bars represent unrelated entities.
- Do not use leaderboards to rank KPI definitions or time-window definitions against each other, such as latest DAU versus WAU versus MAU. Use KPI cards or a compact table for latest values; use trends, indexed trends, share trends, or ratio charts for movement or relationship questions.
- When a bar chart compares one measure across categories, use one categorical axis and one quantitative axis. Do not set a `color`, `series`, or grouped-bar encoding to the same category field just to color each bar; that creates a redundant legend and implies an extra grouping dimension. Use a palette/style option or direct labels if the surface supports per-category color without a legend; otherwise use a single mark color.
- When a bar chart compares same-unit movement across distinct KPI categories, such as latest week-over-week percent change by metric, categorical bar colors can help scanning, but they should be styling, not a visible grouping/legend, unless a second categorical dimension is present.
- When a bar chart compares unrelated business entities or components, such as products, model families, segments, or seat-support areas, do not encode every row with one fixed color when category identity matters. Prefer categorical styling and direct labels; reserve a single color for one measure repeated across a single semantic entity. Avoid adding a color legend when the axis labels already name the categories.
- Keep the same reviewed entity or lifecycle state on the same semantic color across every chart in the artifact. Distinct simultaneous product experiences, plans, countries, statuses, and lifecycle states must not collapse into one color; a monochrome ranking is appropriate only when identity is incidental and is not reused elsewhere. Match a quiet neutral theme when no category colors were authored, but preserve intentionally colorful theme treatments and explicitly supplied category colors; never enforce a blanket neutral-only policy. In grouped bars, color the actual series dimension rather than the already-labeled category axis.
- For heatmaps, use adjacent responsive cells and one quantitative sequential color scale. Do not attach a categorical legend, expose transformed x/y index fields in the tooltip, or draw unrelated crosshairs; show the reviewed row dimension, column dimension, and correctly formatted measure instead.
- Keep axis ticks, direct mark labels, legend encodings, and tooltip values on the same unit scale. Fractional rates must display as percentages everywhere, while count metrics remain counts. Single-population scatter tooltips should show point identity and the two readable axis values without duplicate same-color swatches.
- For active-user dashboards, use KPI cards for latest DAU, WAU, MAU, Plus DAU, and Plus WAU values; trend or indexed-trend charts for movement over time; share or stickiness views when the question is mix or ratios; and categorical horizontal bars for unrelated week-over-week metric movements.
- Prefer variant escalation inside a family before inventing a new chart type: line to small multiples, bar to dot/lollipop, scatter to density, stacked bar to pie only when the circular read is explicitly useful.
- Keep pie, Pareto, waterfall, and Likert as variants, not defaults.
- Avoid bubble charts unless the third variable materially changes the interpretation.
- Include volume, denominator, sample size, or cohort context when omission could mislead.
- In multi-chart reports, review whether each chart family answers its analytical question. Repeated line charts are appropriate for comparable movement over time; do not force chart diversity or a fixed chart count. When the questions differ, consider dot/lollipop or bar with reference for plan variance, stacked area or 100% stacked bar for mix, ranked bars or leaderboards for category comparisons, waterfall for additive drivers, heatmaps for cohort or matrix structure, and stage bars for ordered progression.

### Surface And Implementation

- For reports, dashboards, notebooks, slides, docs, HTML, or explicit static/file output, render in the selected surface. Use a reproducible static chart only when the user explicitly asks for Python, a static image/file, notebook-oriented output, or export. Keep this skill's output to chart selection, data planning, implementation guidance, and QA for the selected surface.
- When the selected delivery surface is a report or dashboard, use the shared app's supported chart families after selecting the analytical family. Do not let a renderer-supported type list drive chart selection.
- Retain useful reviewed context such as denominators, comparison periods, ranks, or grouping fields when available and safe. Do not query extra fields, fabricate auxiliary measures, or ship raw detail rows merely to enable alternative chart types.
- Shape chart-ready data for realistic alternatives, not arbitrary ones. A trend chart should usually retain its temporal field, value field, and meaningful segment/comparator fields; a category comparison should retain the category, value, useful grouping candidates, and rank/sort context; composition charts should retain the denominator or share context when available. A scatter chart should retain a stable point identity or label, numeric x and y measures, any denominator or sample-size fields, a useful volume/size candidate, and one or two interpretable grouping or filter fields. Do not promote a retained grouping candidate into a color/series encoding unless it adds information not already carried by the axis, facet, or table labels.
- Use the selected surface's native chart block when one is available. Do not add an extra decorative outline shell around charts.
- For every report and dashboard, use React and Recharts through the shared Data app and the Data App Contract's prebuilt-runtime build. Do not rely on remote scripts.
- Assume local environments can be minimal or offline. Use Data's pinned prebuilt browser runtime and bundled local authoring tools with Codex's Node runtime; do not require a package install or dependency cache.

### Visual Design

- Default every chart title to a neutral, descriptive label that identifies what is plotted, such as the metric, comparison, dimension, or time scope. Do not infer a narrative takeaway, claim, clever headline, or new jargon for the title. Use a takeaway-led title only when the user explicitly requests one.
- On dashboards, keep chart takeaways as private planning context; do not put interpretations in titles, subtitles, captions, or adjacent prose unless the user explicitly requests commentary. Dashboard chart subtitles are optional and factual: include one only when essential units, denominator, date range, cohort, exclusions, or sample scope cannot be conveyed elsewhere.
- On reports, retain supported interpretation and explanatory paragraphs where they help explain the evidence; let the focused report skill choose their placement and level of detail. A factual chart subtitle may supply necessary metric details, units, denominator, date range, cohort, filters, sample size, or volume without duplicating context already visible elsewhere.
- Use a single font family across charts and surrounding output when possible. Prefer white or near-white backgrounds, quiet grey grid lines, deep charcoal text, and restrained approved palette roots centered on blue, gold, orange, olive, and pink.
- Do not rely on color alone. Use tone, open fill, marker fill, line style, direct labels, ordering, or faceting when series or states need separation.
- Only set color or series encodings for meaningful grouping dimensions such as `segment`, `product_line`, or `series` when they are not already the sole axis category. Omit color for single-series charts and do not manufacture or duplicate a grouping field just to produce a legend.
- Choose one palette policy before plotting:
  - `single-root preferred`: one non-neutral root plus shades, open fills, and neutral references for simple trends, ranks, distributions, relationships, matrices, and repeated panels.
  - `hard two-root cap`: at most two non-neutral roots plus neutrals for binary, signed, focal-vs-context, benchmark, comparator, waterfall, Pareto, diverging, highlighted trend, and ordered line-dot charts.
  - `relaxed multi-category`: up to five approved roots when category identity is the point, such as pie, stacked bars, stacked area, grouped bars, and stage bars. If more are needed, group to top-N plus Other or change forms.
- Use each selected root's `base` tone as the default non-neutral mark color. Reserve `mid` for deliberate higher-contrast exceptions, use `dark` for keylines, outlines, labels, or reference strokes, and use `light`, `xlight`, or `open` for supporting fills.
- Generate explicit palette maps from declared colors. Do not let plotting library categorical defaults choose shipped chart colors.
- For signed values, avoid green/red by default. Use dark versus open/light fills, direct signed labels, and clear zero-line context unless documented domain semantics require an exception.
- For waterfall charts, use matched neutral start and end anchors plus exactly two non-neutral delta colors: one positive and one negative. Do not introduce extra hues or darker/lighter non-neutral keylines for individual drivers.
- For waterfall, bridge, variance, and other delta-focused charts where the takeaway is movement against a large base, do not force the value axis to zero when zero would materially compress the intended movement. Use a focused value-axis domain around the cumulative path or delta range with padding; preserve honesty with exact start/end/change labels, visible units, and an explicit focused-scale cue in the subtitle, caption, or axis when needed. Keep zero in view when values cross zero or the question is absolute magnitude.
- Keep one stroke-width system for marks, keylines, guides, and reference lines. Use dark-neutral styling for benchmark, calibration, or ideal lines.
- Keep left and bottom axis anchors visible when labels depend on them. Remove ticks, guides, or connectors that do not improve the intended comparison.
- Always include the first and most recent reviewed date on temporal axes, prefer readable calendar-spaced intervals, and keep equivalent ranges and centered tick anchors consistent across related line, area, and bar charts. Treat numeric ranks and measurements as quantitative axes, not categories. Prefer horizontal category labels, then at most two readable wrapped lines; use a restrained 45° to 60° layout only when dense named categories or heatmaps otherwise hide meaningful labels, and reserve its full vertical space. Once diagonal mode is selected, show every reviewed category: adjust rotation and preserve distinguishable readable abbreviations rather than skipping alternate labels. Keep dates, times, and numeric labels horizontal. Apply one stable whole-axis collision policy, retain complete accessible names, and use `xTickLabelLayout: "horizontal"`, `"wrapped"`, or `"angled"` only when an authored exception is necessary. Preserve explicit axis titles when both measures need identification, such as scatter plots; never shrink labels to force additional ticks.
- Prefer direct labels when they reduce legend lookups; use a compact top legend when direct labels create clutter.
- Assign distinct, stable colors to simultaneous series and recurring named entities; reuse the same identity color across charts. Distinguish related negative states such as denied, failed closed, and timed out with separate theme-derived colors while preserving their operational meaning. Use one color for a single ranked measure when category identity is already carried by axis labels, and retain a semantic negative color for a chart that compares churn across categories. Use related shades for ordered intensity or stages rather than assigning arbitrary category hues.
- Render every cell in a reviewed two-dimensional count matrix; represent an absent reviewed combination as a zero-valued, hoverable structural cell without presenting it as a separately observed source row.
- Keep horizontal category labels human-readable and bounded, show every categorical bar label, and keep bottom legends compact with an explicit expansion control when additional categories overflow. Group a long tail into **Other** only when categories are mutually exclusive, the displayed measure is nonnegative and additive, per-period totals remain exact, and reviewed source inspection retains every original category; never aggregate overlapping feature or experience audiences, rates, percentages, or unrelated measures.
- Reserve explicit left and right space for horizontal or diverging bars with long labels or negative values. Do not shrink typography to force a narrow card.
- Do not use gradients inside chart marks, arbitrary colored chart backgrounds, inconsistent or ad hoc corner radii, or thickness as an emphasis channel.
- Let the report or dashboard composition determine chart width. Prefer full-width evidence charts in reports, preserve enough plot area for labels and legends, and stack naturally on narrow screens.
- Use the shared app's semantic theme tokens for chart containers, legends, KPI strips, and notes. Express intentional palette choices in the chart spec rather than one-off CSS colors.
- Use dark chart variants only when the containing artifact is dark.
- For research charts, lock the blossom to the header's top-right corner. Omit it for third-party, partnership, and non-research charts.

### Contextual annotations

Add an annotation only when a source actually read supplies context absent from the chart that materially changes its interpretation: a documented operational change, one-time adjustment, measurement change, or relevant qualification. Restating a plotted value, visible trend, ranking, or comparison does not qualify. Zero annotations is valid; do not invent context to fill space. On dashboards, keep annotations factual rather than introducing unsolicited analytical commentary.

For each annotation, retain the supporting source, contextual fact, and exact applicable point or period in the figure's inspectable evidence. Preserve the source population and observation window; do not generalize a narrower experiment to an aggregate chart. An event establishes timing, not an effect; make a causal claim only when the evidence supports it. Check the full claim, not just the anchor, and update or remove it when its source changes. Preserve unrelated user-authored notes.

Use the copied app's `AGENTS.md` for supported annotation kinds, fields, geometry, and visibility controls. Keep labels concise and plain, inside clear plot space near the relevant evidence when they fit, with a real arrow only when needed to clarify the connection. Do not cover marks or axis labels. Retain the full context and material qualifications in the figure at narrow widths and in exports; use a plain figure note when the full label cannot fit, not a hover-only explanation. When browser testing is requested or an annotation failure needs diagnosis, verify it points to the correct mark after filtering and resizing.

The [contextual examples](../../templates/data-app/base/examples/reports/contextual-stories/README.md) demonstrate sourced context using fictional records. Borrow their source-and-claim relationship, not their facts. Ordinary comparisons need no annotation.

### Quality Bar

- Chart choice should follow `Chart Selection`.
- Choose and honor the selected durable delivery surface.
- Explicit standalone static/Python plotting code should be reproducible and adapted to the requested analysis and output format.
- The form must match the analytical comparison, and scales must stay honest and consistent across comparable charts.
- Standard bar charts that compare absolute magnitude should start at zero. Delta-focused waterfalls, bridges, variance bars, and small-multiple movement charts may use non-zero or narrowed domains only when the zero baseline would materially hide the intended change and the chart carries exact labels plus a clear scale cue.
- Data grain, filters, date range, denominator, and units must match the claim the chart supports.
- Every shipped chart must have a visible title appropriate to its surface. Add an optional factual subtitle only when units, time or cohort context, denominator, sample size, or volume are necessary and unavailable elsewhere; dashboard subtitles must not introduce interpretation, while reports place useful interpretation near the evidence.
- Labels, ticks, titles, legends, callouts, benchmark labels, and annotations must not collide, clip, or detach from the evidence in the exported chart or final container.
- Any displayed metric delta must identify the actual comparison observation or cadence, such as vs. Aug 8 or vs. previous week; do not ship an unexplained vs. previous label.
- Long labels, negative values, outside-end labels, zero-line context, and direct value labels need explicit layout space.
- Multi-series filled marks need distinct tones, open fills, keylines, marker fills, line styles, direct labels, or faceting. Visually identical adjacent or overlapping fills fail QA.
- Line styles, marker fills, open fills, keylines, ordering, faceting, and direct labels should remain legible in grayscale when they carry distinction.
- Positive and negative states should use tone, open fill, zero-line context, and signed labels rather than default green/red semantics unless the exception is documented.
- Exported SVG or HTML colors should match declared palette roots plus neutrals; remove unused multi-hue tokens unless documenting an intentional exception.
- Chart scaffolding should stay quiet: no arbitrary colored backgrounds, gradients, decorative guides, inconsistent stroke widths, or decorative mark fills. Filled marks should keep keylines, and benchmark, calibration, and reference lines should use dark-neutral styling.
- Titles, legends, and primary labels should use dark ink and share a clear header anchor. Numeric ticks and direct value labels should use mono styling where the template system calls for it.
- Research charts should use the locked top-right blossom placement; third-party, partnership, and non-research charts should omit it.
- Inspect requested static exports and publication figures in their final format for readable labels, honest signs and scales, understandable encodings, and necessary metric, time-window, and source context. Fix observed failures before delivering those exports.
