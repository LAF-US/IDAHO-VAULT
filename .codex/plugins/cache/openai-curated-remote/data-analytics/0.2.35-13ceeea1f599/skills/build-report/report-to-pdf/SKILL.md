---
name: report-to-pdf
description: "Create a polished PDF from a Data report."
---

# Report To PDF

Use this skill only when the user explicitly asks for a PDF. Author through the canonical [@pdf](plugin://pdf@openai-primary-runtime) plugin.

## Route

- If the user supplied an existing verified report HTML, reuse it and its source evidence.
- If the report still needs to be built, use `$build-report` once. Reuse its `dist/index.html`, `src/data.json`, authored source, and referenced evidence for every requested conversion.
- Do not print an app shell, rebuild the report in a PDF-specific runtime, or author from an unstructured chat summary.

## Workflow

1. **Preflight capabilities.** Confirm that the canonical PDF skill is available before expensive analysis. If it is unavailable, explain the blocker and ask whether the user wants the verified report HTML instead.
2. **Resolve the source report.** Build or reuse the complete Data report app and verify `dist/index.html`. Treat the report source, `src/data.json`, and referenced evidence as the source of truth.
3. **Author with the PDF plugin.** Read and follow the canonical PDF skill completely. Preserve the title, narrative, charts, tables, metric definitions, caveats, freshness, source labels, and links. For chart figures from an open Data app, prefer `list_data_app_cards({})` followed by `get_data_app_card_image({ cardId, scale: 3 })` or `get_data_app_card_images({ cardIds, scale: 3 })`; follow [Card images for slides and documents](../../../shared/data-app.md#card-images-for-slides-and-documents) to discover tools, verify scope, and decode local PNGs without printing base64. If capture is unavailable or unsuitable, use the chart's vector output or reviewed-data rendering. Keep surrounding report text selectable and avoid duplicating titles already captured in a card. Omit interactive controls and internal runtime or local-path metadata.
4. **Render, inspect, and repair.** Confirm page count and metadata, extract text when selectable text is expected, and inspect every page for short reports. Fix blank pages, clipping, overlap, broken tables, missing chart marks, unreadable glyphs, unresolved placeholders, and leaked app controls.
5. **Validate and deliver.** Confirm the PDF is non-empty, opens cleanly, and contains the required claims, definitions, caveats, freshness, and provenance. Return the verified PDF and, when useful, the source report HTML.

## Hard gates

- The canonical PDF plugin was selected and available before report construction.
- The shared report app built and its `dist/index.html` was inspected before authoring.
- Every page passes full-page visual inspection.
- Required claims, definitions, caveats, freshness, and provenance survive conversion.
- App-only controls and internal conversion metadata are absent.

If a hard gate fails, stop and report the failure.
