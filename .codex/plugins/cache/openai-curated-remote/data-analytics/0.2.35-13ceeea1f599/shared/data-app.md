# Data App Contract

Shared technical reference for dashboards and reports. The focused [dashboard](../skills/build-dashboard/SKILL.md) or [report](../skills/build-report/SKILL.md) skill owns planning and presentation; this file owns source integrity, data lifecycle, preview, and delivery. The copied project's `AGENTS.md` owns local file boundaries, styling, protected-runtime changes, and builds. Read only the section or resolved component-reference topic needed for the current step.

## Source discovery and access

Use the user's named source or authoritative connected evidence. Verify selected schemas, definitions, grain, coverage, and freshness through live reads; reuse current-task findings rather than rescanning connectors. Resolve conflicts by source ownership, directness, and fitness for the question, recording material disagreements. Retain complementary history, targets, cohorts, and drivers at their natural grains.

If a required source is unavailable, ask for access or reviewed source-backed data. Do not invent evidence or substitute a mock app unless requested. Optional enrichment must not block a useful answer when its absence cannot materially change it.

## Canonical starter

New dashboards and reports use the shared [app preparer](../scripts/prepare-data-app.mjs). Follow the focused skill's command with an explicit `--surface dashboard` or `--surface report`, a new `--output` directory, and `--snapshot` containing reviewed evidence. The CLI defaults to dashboard when the surface is omitted. It creates the selected content with the shared runtime, surface, fresh stable artifact ID, and Classic theme; preserve that identity when revising the app in place. `--blank` creates blank content for the selected surface when requested. Before editing, read the copied `AGENTS.md` for authoring boundaries, themes, and the scoped authorization workflow for protected changes ([canonical guide](../templates/data-app/base/AGENTS.md)).

### Resolve the component reference

For a new app, start at the preparer's returned `documentation.entryPoint`. Before consulting APIs when revising an existing app, run `node scripts/data-app.mjs prepare --project-dir /absolute/app-project` from the installed plugin root, or use its absolute script path. This read-only command returns the current installed reference with `source: "installed-plugin"`, `apiVersion`, and `runtimeSha256`. Read only relevant topics from that index; for older apps, its entry point takes precedence over copied API-reference links. With `--source`, use the returned `project-source` reference matching the copied runtime. Reference lookup requires no copying, dependency installation, or runtime-upgrade approval.

## Reviewed data and provenance

Keep bounded reviewed rows under stable query IDs in `src/data.json`, with exact source metadata and output aliases. The copied snapshot provides a complete schema example. A query's grain must fit every consumer. Preserve nulls, cohort maturity, source classification, and distinctions between observations, targets, and scenarios. Never invent SQL, denominators, or lineage. Fixture classification belongs in metadata; the focused skill controls visible disclosure.

A component may use derived `displayRows` while retaining the original query for inspection; use `sourceRows` for an intentional reviewed subset. Affected visuals, source previews, copying, and exports must use the same filtered population. Do not sum overlapping populations or unweighted rates. Group additive categories into Other only when populations are mutually exclusive, every period reconciles, and original categories remain inspectable. Waterfalls require reviewed before/after totals reconciled by signed intermediate changes.

### Reviewed metric definitions

Each query's `source.metricDefinitions` supplies relevant definitions. Ordinary counts need a concise label and truthful definition, not decorative formulas. For example, when the reviewed transformation actually establishes these aliases and subtraction:

```json
{
  "label": "Net change",
  "definition": "Current active users minus previous active users.",
  "componentIds": ["usage-change"],
  "formula": "activeUsers - previousUsers",
  "dependencies": ["activeUsers", "previousUsers"],
  "sourceLineage": [{ "tables": ["analytics.reviewed_usage"] }]
}
```

- `componentIds`: exact stable authored IDs. Definitions for unrelated consumers must not appear in the selected component.
- `formula`: only calculations, inclusion rules, weights, or references established by reviewed SQL, transformations, metadata, or explicit user requirements.
- `variable`: a reviewed alias or documented input needed by another visible formula. Legacy `identifier`, `field`, and `result.field` remain supported. Do not add unused symbols.
- `dependencies`: meaningful shared variable identifiers, including transitive dependencies. Leave definitions unscoped only when shared by multiple components. Optional `numerator`/`denominator` objects use verified `field` and reader-facing `label`.
- `sourceLineage`: exact tables/files present in that query's `source.tables`, `source.files`, or `source.sourceFiles`. Do not invent physical lineage for constants or precomputed scores.

Define series, thresholds, meaningful categories, populations, observation windows, and weighted factors when they change interpretation. Describe unexplained precomputed scores as supplied with unavailable methodology; omit unsupported formulas and lineage. Definitions belong in the existing source inspector and Evidence flow, not new panels or duplicated dashboard prose.

Optional asset-level `trust` metadata supports `provider`, `uniqueUsers`, `uniqueViewers`, `queryCount`, `viewCount`, `favoriteCount`, `windowDays`, `verified`, and `editedAt`. Include only verified values for that asset. Counts describe real usage, not saved query definitions; edit timestamps are not data freshness. Preserve counting methods/windows, never infer identities or verification, and do not delay delivery for optional popularity metadata.

## Components and interactions

Wrap each source-backed unit in `DataComponent` or a shared component providing it, such as `EvidenceChart` or `ReportSection`, with stable authored `id`, `queryId`, `kind`, and `title`. Retain source/copy actions, visibility, editing, and permissions. The wrapper imposes no border or layout. Do not invent query associations for general headings or introductions.

Use `ChartRenderer` for supported visuals so page and explorer share scales, legends, tooltips, transforms, and accessibility. Consult only the required [component API](../templates/data-app/base/docs/components/README.md) topics from the resolved reference. Preserve actual temporal/numeric positions; never relabel a point with a different date or rotate time labels. Custom React/Recharts/SVG inside `CustomBlockHost` remains available when shared rendering cannot express the analysis; keep reviewed values, units, comparable scales, and visible pointer/keyboard tooltips. Use bundled icons or local authored assets, not remote libraries.

Keep the source sidebar's Overview, Data preview, SQL query, and Evidence flow tabs, with query identity, reviewed period/freshness, applicable filters, definitions, sources, caveats, and SQL. A derived evidence flow describes only recorded metadata, never implied reruns or invented validation.

Use `RichNarrative`, `EditableText`, or stable `data-editable-id`/`data-editable-narrative` bindings for copy; mark reviewed collections with `data-reviewed-rows`. Presentation editing does not override values, source metadata, cells, or chart internals. Data/calculation corrections use the data lifecycle, not another value editor. Preserve autosave, restore-hidden actions, permissions, and chart editing.

Published components retain one Copy link action: `/_data/charts/<target-id>` for charts, `/_data/components/<target-id>` otherwise. The shell handles stable eight-character aliases, legacy links, view activation, and focus; keep authored IDs rather than substituting aliases. Do not implement another locator registry or renderer. Links are query/fragment-free and grant only existing whole-dashboard Site access; opaque IDs are not secrets or component-level permissions. Preserve dashboard-level Copy link separately.

## Presentation state and composition

Layout belongs to authored React/CSS. Use `SortableRegion variant="canvas"` for independent movable/resizable blocks, `freeform` for authored geometry, and ordinary/composite sections for linked or fixed content. Mount primitives for intended movement; imports alone do nothing. Read the [sortable API](../templates/data-app/base/docs/components/sortable-layout.md) for constraints and persistence, not a prescribed page outline. Reports may use `stack` for movable editorial sections.

Keep stable component IDs and user placement. Increase a region's positive `authoredRevision` only for explicitly requested rearrangement, not ordinary data/copy/style edits. Use shared headers, contextual resize/keyboard affordances, and protected movement behavior, not an artifact-specific drag engine.

For distinct dashboard views, `useDashboardTabs` registers stable IDs/labels; the shell owns the single global tab row. Its bindings preserve independent tab state. Global filters belong outside panels only when dashboard-wide; `queryIds` declares applicability, not placement. Put section/chart controls beside affected content. Derive choices from applicable reviewed rows and remove inert controls. Consult [filtering and exploration](../templates/data-app/base/docs/components/filtering.md) for bindings.

Presentation edits, visibility, chart settings, themes, and layout stay separate from evidence. Validated URLs may share declared tabs/filters; mark sensitive or identity-bearing filters `shareInUrl: false`. Scenarios remain private exploratory state with assumptions, modeled outputs, baseline, and reset, never observed data. Standalone state uses per-app storage; hosted state uses revision-guarded same-origin routes.

## Local and hosted data lifecycle

Revise the same app in place. Refresh only intended queries' rows/freshness, preserving IDs, definitions, unrelated data, content, theme, presentation, and Site/DB ownership; rebuild and refresh its existing preview. Artifact-local corrections retain honest provenance and never silently write back to source systems.

Hosted `list_data_app_queries()` and `update_data_app_query({ queryId, rows })` use authenticated same-origin persistence and refresh every consumer. Keep metadata, query definitions, and individual rows separate, not entire result sets in one database record. Changes survive reload/redeploy unless the reviewed seed fingerprint changes.

### Card images for slides and documents

Local previews and hosted readers expose three read-only WebMCP tools when the browser supports them:

- `list_data_app_cards({})` returns mounted cards with exact `cardId`, title, kind, reviewed query IDs, section filters, and image availability, plus the current tab and page filters. Use these IDs rather than titles, query IDs, permalink aliases, or DOM selectors.
- `get_data_app_card_image({ cardId, scale: 2 })` captures the current rendered card as a PNG, including its displayed text, chart/table/metric/custom content, theme, and current presentation. It returns `data` (base64 PNG bytes), `mimeType`, `encoding`, pixel `width`/`height`, `filename`, card/source IDs, and `view` metadata. Decode `data` directly into a PNG file for downstream use; keep the large image bytes out of printed tool logs and model-visible text.
- `get_data_app_card_images({ cardIds, scale: 2 })` returns `{ view, images }` in requested order. A batch accepts 1–8 unique IDs and fails as a whole if any card cannot be captured.

Scale is 1–3, with a 4 MiB PNG limit per card and 8 MiB per batch. These tools neither mutate reviewed data nor write to the clipboard, trigger downloads, switch tabs, or publish anything. Offscreen mounted cards can be exported; open an inactive tab before listing its cards. Hidden, missing, duplicate, loading, failed-to-load, changing, oversized, or unsupported cards produce explicit errors. Exports represent the current card bounds, not all paginated or scroll-clipped table rows. Return internally scrolled containers to their start before capture; the tools never reset them. Use embedded app assets and SVG definitions inside the captured card; external images/fonts or unsupported embedded content may prevent a self-contained image. If the view changes during export, list the cards again and retry.

When converting or sharing an existing Data app:

1. Follow the available browser skill to reuse or open the verified source app's browser tab and discover that tab's WebMCP tools. These are live browser tools, not server MCP endpoints or functions callable from an HTML file on disk. If the browser or app version does not expose them, use the destination skill's vector or reviewed-data rendering fallback without claiming a WebMCP capture.
2. Use the app's normal controls to select the requested tab and filters before listing cards. Select exact `cardId` values from the listing and check `imageAvailable`; preserve the returned `queryIds`, `scopeFilters`, and `view` metadata to verify the source and scope. List again after changing tabs or filters. Exporting must not require owner access, query updates, or changes to shared presentation.
3. Capture selected cards with the single or batch tool, waiting for one export to finish before starting another. Prefer scale 3 for slide/document images, and use the returned pixel dimensions to choose a readable placement size. If a size limit is exceeded, split the batch or lower the scale and recheck output quality. Do not treat a failed batch as partial success.
4. Keep the tool result in the execution context and decode each image's `data` directly from base64 into a local PNG using supported file-writing capabilities. Use distinct local filenames when exporting multiple cards or views; retain the mapping to card IDs and metadata. Pass paths to the destination artifact skill and emit only compact metadata or image previews, never the base64 payload.
5. Inspect the saved PNGs before embedding them. Confirm titles, labels, units, marks, and the requested scope survived, and include needed filter context, caveats, freshness, and provenance beside the images. A full-card capture already includes its rendered title; avoid duplicate headings and keep surrounding narrative and source notes editable. For requested editable charts or titles, use the destination skill's editable reconstruction path.

Dashboard refresh/non-PDF exports delegate through available host actions and report failures honestly. Reports have snapshot metadata, not data-only/scheduled refresh: revise their evidence, calculations, and narrative together. The app's PDF export control prints the current rendered view through shared browser printing, not a host prompt or PDF plugin.

Publication is separate from preview. `.openai/hosting.json` declares future bindings, not an existing Site. Follow the focused skill's authorization and [publication skill](../skills/publish-artifact-to-sites/SKILL.md) for access, owners, packaging, deployment, and source-only repair. Preserve Site/DB/presentation; never widen access or rebuild after final packaging. Return a successful private Site even if hosted editing is unavailable, without claiming editing works until verified.

## Build and verification

Build using the copied project's `AGENTS.md`, which owns the command, supported module shapes, source-build exceptions, and integrity checks ([canonical build guide](../templates/data-app/base/AGENTS.md#build-and-preview)).

Open a useful source-backed first view promptly, then finish the requested scope in that same artifact. Prefer an existing allowed preview. On local Codex Desktop, `open_in_codex` with a browser target and encoded absolute `file://` URL opens built HTML; a source-file target is not a preview. Retain its tab ID for refreshes. Do not open extra verification tabs, start localhost unless requested, publish, or rehost to bypass unavailable inspection. Remote filesystem paths are not local browser URLs; report missing preview routes. Queued opening is not proof of rendering.

Use the built `dist/index.html` for local preview and delivery. Builds may attach transient local `CODEX_SESSION_ID` (fallback `CODEX_THREAD_ID`) for same-task handoff. Never hard-code task IDs in source, evidence, or URLs. Published handoffs start a new task; local handoffs may reuse only their valid originating task. Leave host-specific routing to the shell.

Inspect the built artifact at normal/narrow widths and exercise its main filter/detail interaction, using an available browser or a human reviewing that same artifact. Check marks, labels, containment, copy, and source/export agreement. Fix and recheck changed content; no separate evaluation batch or full runtime sweep is required for ordinary authoring. State what ran and any gaps: builds, queued previews, and source inspection are not visual acceptance.

## Security and quality gates

Keep credentials, personal identifiers, and live warehouse connections out of artifacts. Use bundled runtime assets, never CDN libraries; hosted apps request only their same-origin API. Self-contained HTML contains reviewed rows/metadata and is sensitive.

Before publication reject signed/access-token URLs, credentials, unapproved query parameters, and fragments throughout source links and nested provenance. Preserve reviewed Google Calendar links of the exact form `https://www.google.com/calendar/event?eid=<locator>`: one bounded base64url-safe locator, default HTTPS port, no credentials or fragment. This does not permit arbitrary query strings. Canonical Site/share links stay query/fragment-free.

Before delivery, confirm material claims/definitions at the right grain, truthful filter/source/export scope, separation of actuals and assumptions, working identities/actions, and presentation separated from data. Fix or disclose missing evidence, unsupported comparisons, stale sources, and access gaps. Local/hosted delivery use the same source tree and compiled UI. Reuse completed verification.
