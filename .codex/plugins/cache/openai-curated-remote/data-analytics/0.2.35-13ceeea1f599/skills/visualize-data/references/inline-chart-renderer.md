# Inline Data Chart Renderer

Use this reference only for an already-selected Codex Desktop inline chart outside positively identified Work Mode. Work Mode retains its existing host-native rendering contract. The [render-inline-chart.mjs](../scripts/render-inline-chart.mjs) CLI uses the shipped prebuilt version of the actual inline React adapter [index.jsx](../../../templates/data-app/inline/index.jsx), which imports the real shared `ChartRenderer` and `SourceSidebar` from [data-app-public.jsx](../../../templates/data-app/base/src/data-app-public.jsx). Chart rendering, source inspection, styles, and themes stay owned by the canonical dashboard implementation; never recreate them in D3 or hand-authored HTML.

## Run The Shared Renderer

Call `load_workspace_dependencies` and use its absolute bundled Node executable as `<codex-node>`. Resolve the script from the installed Data plugin root. Inspect the bundled reviewed input [inline-chart-example.json](../assets/inline-chart-example.json) only when needed:

```sh
"<codex-node>" "<data-plugin-root>/skills/visualize-data/scripts/render-inline-chart.mjs" --example
"<codex-node>" "<data-plugin-root>/skills/visualize-data/scripts/render-inline-chart.mjs" --list-chart-types
"<codex-node>" "<data-plugin-root>/skills/visualize-data/scripts/render-inline-chart.mjs" \
  --input /absolute/path/reviewed-chart.json \
  --output /absolute/approved/visualizations/weekly-active-users.html
```

The output must be an approved writable path outside the installed plugin and any legacy shared cache, with a lowercase-hyphenated `.html` filename. The renderer combines the verified data-free runtime, approved reviewed payload, canonical theme, and bundled [inline-chart-fragment.html](../assets/inline-chart-fragment.html). Deliver the real returned path in the same final answer as its native Visualize content reference:

```text
visualize{"path":"/absolute/approved/visualizations/weekly-active-users.html"}
```

Honor an explicit request for multiple inline charts, even when several are needed. Render each reviewed input with a stable, distinct chart ID and output filename; reuse the same shipped data-free runtime and emit one actual Visualize content reference per chart in the same final response. Never concatenate complete fragments or rebuild the runtime for each chart.

Use the executable directly; do not rebuild the dashboard, install packages, generate substitute D3, recreate React components, or return the fragment as a download or code block. A build command, unrendered file, source preview, or promised handoff is not the delivered chart.

## Reviewed Input And Source Safety

The JSON input requires `schemaVersion: 1`, a reader-facing `title`, the canonical `chart` specification, bounded reviewed `rows`, and a real `source` with `source.label`. Optional `id`, `queryId`, `description`, approved preview `columns`, reviewed `filters`, `generatedAt`, `height`, and `theme` preserve existing dashboard semantics. The shared `projectChartSpec` and `chartDataShape` retain real histogram, Sankey, precomputed box-plot, and waterfall metadata while removing private extension fields; do not invent extra fields or axes. Preserve missing observations as `null` in the real measure; do not invent helper series or zero-fill missing values to force chart marks. Use `--list-chart-types` for the live supported chart families rather than maintaining a duplicate list. Keep the input below 2 MB, project unnecessary columns, and provide no more than 2,000 reviewed rows; the generated fragment must remain below 1 MB. Explicitly label synthetic or illustrative data as sample data.

The real dashboard `SourceSidebar` uses `variant="contained"` and `allowCopy={false}`; it opens as a right-aligned overlay and preserves its exact four tabs: `Overview`, `Data preview`, `SQL query`, and `Evidence flow`. Include only reviewed, chart-scoped definitions, freshness, caveats, filters, bounded preview rows, and recorded evidence. Set `source.executedAt` only from recorded query-execution metadata and `generatedAt` only from actual reviewed snapshot creation or capture; preserve materialization or source-refresh timestamps with their timezone in an original approved preview field or explicitly labeled `source.caveats`/`source.evidenceFlow`, omit unknown timestamps, and never relabel freshness as query execution to fill the inspector. Raw SQL and source URLs are omitted by default: use `--include-sql` only when the user explicitly requests reviewed SQL, and use `--include-source-urls` only when the user explicitly requests reviewed source links. Otherwise the SQL tab displays `No reviewed SQL provided.`. Never include credentials, tokens, hidden reasoning, direct personal contact or payment identifiers, invented provenance, or unreviewed fields. Do not add unsupported image-copy or data-copy controls.

Use the canonical `codex-classic` theme by default and prefer explicitly requested bundled themes through `theme`. A reviewed local `--theme-css` stylesheet is parsed by the bundled CSS parser and may contain only `:root` custom-property declarations; imports, URL/image resources, other selectors, and arbitrary component CSS are rejected. Preserve host light/dark appearance and the dashboard's actual typography, semantic colors, curves, markers, legends, and tooltips without copying their values into instructions.

Annotations cannot expand the reviewed row projection. For event or benchmark evidence outside the plotted fields, explicitly include the reviewed evidence field in `columns`.
Annotations that name unapproved fields are omitted, even if their anchor would not render.
Point annotations on long-form series use the plotted series name, not another row column.

Annotations cannot expand the reviewed row projection. For event or benchmark evidence outside the plotted fields, explicitly include the reviewed evidence field in `columns`.
Annotations that name unapproved fields are omitted, even if their anchor would not render.
Point annotations on long-form series use the plotted series name, not another row column.

## Runtime, Compatibility, And Verification

Preparation uses Codex's bundled Node runtime (Node 20.19+ or Node 22.12+). The plugin ships one pinned, data-free React/Recharts runtime built from the protected dashboard sources. `--prepare` verifies that shipped runtime; it does not compile it or install dependencies. Normal rendering works without npm or network access, including on a fresh machine with no dependency cache. `--offline` and `--cache-dir` remain accepted for compatibility, but do not create or populate dependency caches. Never put reviewed rows, SQL, source URLs, or generated fragments in the plugin or a shared cache. Do not import the full `DataAppShell`, global theme runtime, dashboard fixture data, external scripts, or network-backed runtime dependencies.

The executable escapes reviewed JSON, script terminators, and replacement-sensitive JavaScript so the fragment works in both older `String.replace` string-replacement hosts and fixed callback-replacement hosts. Do not rewrite, re-minify, or interpolate the completed fragment. When changing the renderer, perform real sandbox/browser QA for actual React/Recharts marks, light and dark appearance, desktop and narrow widths, responsive right-hand source sidebar, all four tabs, keyboard dismissal, default SQL/source-URL exclusion, and absence of unsupported copy controls. If preparation, input validation, rendering, or delivery fails, surface the actual error and do not claim an undelivered chart rendered. Never claim a chart rendered unless its native Visualize content reference was emitted successfully.

## Troubleshooting

- Missing or invalid prebuilt runtime: finish the plugin update or restore the verified plugin, then retry; do not fetch replacement packages. `--prepare --offline` verifies the shipped runtime without requiring a cache.
- Protected-runtime mismatch: finish the plugin update or restore the verified plugin, then retry; never bypass its verifier or rewrite the integrity manifest.
- Oversized fragment: aggregate reviewed rows and remove unnecessary preview columns or source details before retrying.
- Rendering failure: inspect actual host-sandbox insertion and browser errors. A `file:///` page or Python preview alone does not prove live insertion. Maintainers run `npm test` and `npm run test:inline-chart-browser` from the Data plugin root.
