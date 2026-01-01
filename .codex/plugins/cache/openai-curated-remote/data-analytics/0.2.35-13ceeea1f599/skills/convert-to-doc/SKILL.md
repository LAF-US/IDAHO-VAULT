---
name: convert-to-doc
description: "Create a polished DOCX or Google Doc from an existing Data app."
---

# Convert To Doc

## Route

- For a local app, use its `dist/index.html` and `src/data.json` directly.
- For a published app, use its exact HTTPS `.chatgpt.site` URL, the reviewed snapshot from `/api/snapshot`, and the saved presentation state from `/api/presentation` as the equivalent verified source.
- Preserve its visible content, charts, filters, presentation state, and reviewed source data. Do not create an intermediate report or rebuild the app.
- Create a DOCX file with the [@documents](plugin://documents@openai-primary-runtime) plugin and match the final output format to the request.

## Workflow

1. **Preflight capabilities.** Confirm that the canonical Documents skill is available before conversion. For a native Google Doc, also confirm a Google Drive document-import capability. If a required capability is unavailable, explain the blocker and ask whether the user wants the existing app's verified HTML instead.
2. **Resolve the existing app.** For a local app, verify its `dist/index.html` and use `src/data.json`. For a published app, verify the exact HTTPS `.chatgpt.site` source URL, load the compiled app from that URL, and fetch its reviewed snapshot and saved presentation state from the source origin's `/api/snapshot` and `/api/presentation` endpoints. Reject other remote sources or a hosted source whose app, snapshot, or presentation endpoint cannot be read. Use the resolved app, presentation state, and referenced evidence to preserve visible content, charts, filters, exact claims, definitions, caveats, freshness, source labels, links, tables, and reviewed data.
3. **Determine a starting style.** If a template or reference was not provided, ask the user what to base the document's layout and style on. If strong candidates exist in memory or user context, suggest them and include a link. If none exist, use the Documents plugin's built-in `google_docs_default` preset for a clean, neutral DOCX or Google Doc. Use another built-in preset only when the user requests a different document style.
4. **Author with the Documents plugin.** Read and follow the canonical Documents skill. Only create a cover page, title page, or introductory page if the selected template includes one. Use native headings, paragraphs, lists, links, tables, and editable content wherever practical. If using a template, preserve its layout and formatting unless the user explicitly asks for changes. Copy template sections as needed and delete unused sections only when the document is complete. Keep raw SQL in source notes unless the user asked to see it; never use a whole-app screenshot.
5. **Render, inspect, and repair.** Inspect every page at full size. Fix clipping, overlap, overflow, unresolved placeholders, missing chart marks, illegible text, missing table-header semantics, and missing meaningful image alt text.
6. **Validate and deliver.** Confirm the DOCX opens cleanly and contains the required title, claims, metrics, caveats, freshness, and provenance. For Google Docs, import the verified DOCX, read it back, and confirm the critical content survived before returning the link.

## Chart images

- Prefer the open Data app's read-only WebMCP tools for chart images: discover exact IDs with `list_data_app_cards({})`, then use `get_data_app_card_image({ cardId, scale: 3 })` or `get_data_app_card_images({ cardIds, scale: 3 })`. Read [Card images for slides and documents](../../shared/data-app.md#card-images-for-slides-and-documents) for browser discovery, PNG decoding, scope checks, and capture limits. Pass the saved PNG files to the Documents plugin; do not print base64 image bytes.
- If WebMCP is unavailable or a capture cannot satisfy the requested editability, styling, or resolution, use the chart's own rendered SVG/vector output or reconstruct it from reviewed data and chart specifications, preserving the current filters and presentation state.
- Card captures include rendered titles and text. Avoid duplicating those headings; keep surrounding captions, caveats, and source notes editable. When titles must be editable, use a chart-only vector or reconstruction instead of a full-card PNG.
- For vector or reconstructed charts, remove hover layers, tooltips, controls, and other interactive-only elements. Resolve inherited fonts, CSS variables, colors, and backgrounds to match the selected template or style while preserving meaningful colors, labels, legends, units, and data.
- Keep vector output when the destination supports it faithfully. For PNGs, use the returned pixel dimensions to size placement at roughly 200 pixels per inch or better. Prefer scale 3 for card captures; if size limits require a lower scale, recheck legibility rather than enlarging a low-resolution image. Inspect every embedded chart at full size for sharp text, complete marks, accurate colors, and the intended filters.

## Hard gates

- The Documents plugin was selected and available before conversion.
- Either the local app's verified `dist/index.html` and reviewed `src/data.json`, or the published app's verified HTTPS `.chatgpt.site` URL with successful `/api/snapshot` and `/api/presentation` responses, was used directly as the reference for the document.
- Every page passes full-page visual inspection and accessibility checks.
- The document contains native structure rather than a flattened report image.
- Required claims, definitions, caveats, freshness, and provenance survive conversion.
- The delivered destination matches the request.

If a hard gate fails, stop and report the failure.
