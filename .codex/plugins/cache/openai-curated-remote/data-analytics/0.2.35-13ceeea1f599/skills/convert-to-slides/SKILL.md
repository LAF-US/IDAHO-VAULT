---
name: convert-to-slides
description: "Create a polished PowerPoint or Google Slides deck from an existing Data app."
---

# Convert To Slides

## Route

- For a local app, use its `dist/index.html` and `src/data.json` directly.
- For a published app, use its exact HTTPS `.chatgpt.site` URL, the reviewed snapshot from `/api/snapshot`, and the saved presentation state from `/api/presentation` as the equivalent verified source.
- Preserve its visible content, charts, filters, presentation state, and reviewed source data. Do not create an intermediate report or rebuild the app.
- Create a PPTX file with the [@presentations](plugin://presentations@openai-primary-runtime) plugin and match the final output format to the request.

## Workflow

1. **Preflight capabilities.** Confirm that the canonical Presentations skill is available before conversion. For native Google Slides, also confirm a Google Drive presentation-import capability. If a required capability is unavailable, explain the blocker and ask whether the user wants the existing app's verified HTML instead.
2. **Resolve the existing app.** For a local app, verify its `dist/index.html` and use `src/data.json`. For a published app, verify the exact HTTPS `.chatgpt.site` source URL, load the compiled app from that URL, and fetch its reviewed snapshot and saved presentation state from the source origin's `/api/snapshot` and `/api/presentation` endpoints. Reject other remote sources or a hosted source whose app, snapshot, or presentation endpoint cannot be read. Use the resolved app, presentation state, and referenced evidence to preserve visible content, charts, filters, claims, definitions, caveats, freshness, and provenance.
3. **Determine a starting style.** If a template or reference wasn't already provided, ask the user if they have a preference on what to base the slides layout and style on. If strong candidates exist in memory or user context, be helpful and suggest them (include a link). If none exist, use the `artifact-template-simple-light-mode` skill from the `openai-templates` plugin.
4. **Author with the Presentations plugin.** Read and follow the canonical Presentations skill. Adapt the existing app's visible content into clear slides while preserving its headings, chart order, and presentation state. Do not invent an executive summary, recommendations, or next steps that are absent from the app. If using a template, do not alter the layout of the slides unless explicitly asked to by the user. Copy template slide layouts as you need them and only delete the blanks when you are done.
5. **Capture charts and preserve structure.** Use the chart-image workflow below to capture the app's rendered cards through WebMCP. Reconstruct charts from reviewed queries and chart specifications when editable charts are requested or card captures cannot meet the output requirements. Preserve signed values, units, definitions, caveats, source labels, and freshness. Keep surrounding text, tables, and shapes editable; never use a whole-app screenshot.
6. **Render, inspect, and repair.** Inspect every slide at full size and run the canonical overflow test. Fix clipping, overlap, unreadable labels, missing chart marks, unresolved placeholders, and low-contrast surfaces. Tighten copy before shrinking fonts.
7. **Validate and deliver.** Confirm the PPTX opens cleanly and contains the required claims, metrics, caveats, freshness, and provenance. For Google Slides, import the verified PPTX and confirm the critical content survived before returning the link.

## Chart images

- For chart images, prefer the open Data app's read-only WebMCP tools: discover exact IDs with `list_data_app_cards({})`, then use `get_data_app_card_image({ cardId, scale: 3 })` or `get_data_app_card_images({ cardIds, scale: 3 })`. Read [Card images for slides and documents](../../shared/data-app.md#card-images-for-slides-and-documents) for browser discovery, PNG decoding, scope checks, and capture limits. Pass the saved PNG files to the Presentations plugin; do not print base64 image bytes.
- Honor requests for editable charts. If WebMCP is unavailable or a capture cannot satisfy the requested editability, styling, or resolution, use the chart's own rendered SVG/vector output or reconstruct it from reviewed data and chart specifications, preserving the current filters and presentation state.
- Card captures include rendered titles and text. Avoid duplicating those headings; keep surrounding captions, caveats, and source notes editable. When titles must be editable, use a chart-only vector or reconstruction instead of a full-card PNG.
- For vector or reconstructed charts, remove hover layers, tooltips, controls, and other interactive-only elements. Resolve inherited fonts, CSS variables, colors, and backgrounds to match the selected template or style while preserving meaningful colors, labels, legends, units, and data.
- Keep vector output when the destination supports it faithfully. For PNGs, use the returned pixel dimensions to size placement at roughly 200 pixels per inch or better. Prefer scale 3 for card captures; if size limits require a lower scale, recheck legibility rather than enlarging a low-resolution image. Inspect every embedded chart at full size for sharp text, complete marks, accurate colors, and the intended filters.

## Hard gates

- The Presentations plugin was selected and available before conversion.
- Either the local app's verified `dist/index.html` and reviewed `src/data.json`, or the published app's verified HTTPS `.chatgpt.site` URL with successful `/api/snapshot` and `/api/presentation` responses, was used directly as the reference for slides.
- Every slide passes full-slide visual inspection and overflow checks.
- Charts match the reviewed queries, including signs and units.
- The deck contains native, editable structure and faithfully presents the existing app's content.
- The delivered destination matches the request.

If a hard gate fails, stop and report the failure.
