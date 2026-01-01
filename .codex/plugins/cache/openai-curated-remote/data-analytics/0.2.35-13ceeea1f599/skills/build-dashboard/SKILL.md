---
name: build-dashboard
description: Build or update a source-backed interactive dashboard for monitoring, exploration, and operational decisions from connected data, uploaded spreadsheets, CSVs, or other structured sources.
---

# Build Dashboard

For requests to set up or change a recurring refresh schedule for an existing dashboard, read and follow [$schedule-refresh-jobs](../schedule-refresh-jobs/SKILL.md) before entering the authoring workflow. One-time refreshes and execution of an existing scheduled refresh stay in this skill; they do not create another job.

Create a private, editable measurement surface that answers the user's question through evidence and useful interactions. This skill owns dashboard planning, hierarchy, copy, and reference selection. The [Data App Contract](../../shared/data-app.md) owns reviewed data, privacy, runtime, and delivery. Preserve existing dashboards and user-authored layouts when revising them.

## Plan the evidence and hierarchy

Identify the audience, question, population, period, comparison basis, and next useful investigation. Ask only when missing context materially changes the result; otherwise choose reversible defaults. Do not ask the user to choose chart types or chart counts.

Before coding, map the user's distinct questions to the available evidence: current level and meaningful change, trajectory, relevant segment or cohort differences, population size and denominators, and the next useful investigation. Include the dimensions together when their relationship matters. Narrow this coverage for a narrow question; a short prompt does not imply a shallow dashboard. This is a brief private plan, not a required section sequence or dashboard prose.

Use visuals for aggregate comparisons, change, composition, and relationships. Use tables for identifying records, exact multi-attribute inspection, and operational action. A useful queue may lead the page; a table of totals already shown in charts usually belongs in source inspection or detail. Combine duplicate views, not distinct analytical questions. Honor explicit table requests; there is no chart quota.

Show differences side by side when comparison is the question. A filter alone is not a substitute. Include a KPI only when it adds a useful summary beyond the main visual; neither a top KPI strip nor a sparkline is obligatory. Comparisons need meaningful baselines; trends need comparable reviewed history and an identifiable period.

## Establish source-backed measurements

Use the named source or authoritative governed evidence. Read the contract's [source guidance](../../shared/data-app.md#source-discovery-and-access) when gathering evidence and [provenance schema](../../shared/data-app.md#reviewed-data-and-provenance) when constructing the snapshot. Define measures, populations, denominators, comparisons, assumptions, and lineage at the affected component. Preserve source classification and limitations in provenance; never present supplied fictional data as real observations.

Reconcile totals and weighted rates at the correct grain. Preserve nulls, incomplete coverage, cohort maturity, and distinctions between actuals, targets, and scenarios. Correlation and accounting decomposition are not causal proof. Fetch extra evidence only to answer a question, never to fill template slots. Omit unsupported measurements; if no useful dashboard is possible, ask for the missing source.

For workbook inputs, use spreadsheet tools for ingestion and calculations. Their workbook-presentation advice does not govern this HTML dashboard. Use a spreadsheet or BI-native destination only when requested.

## Start from appropriate working code

For a new dashboard, choose a useful starting composition from the [golden catalog](../../templates/data-app/examples/manifest.json) by analytical task: comparing segments, monitoring change, investigating exceptions, or exploring an entity. The subject and data grain need not match to learn from its layout. Read the closest reference's `DashboardContent.jsx` and relevant CSS, following local composition imports where they own the layout. Prefer adapting its working code when it provides useful groupings or interactions, even if only part of the page fits:

```sh
node scripts/prepare-data-app.mjs --surface dashboard --from-reference REFERENCE_ID --output /absolute/new-project --snapshot /absolute/reviewed.json
```

Run from the plugin root or use the absolute helper path. Read the selected reference's brief and data contract before binding your evidence. The shared preparer sets the dashboard surface and a fresh stable artifact ID, and copies working code with your reviewed snapshot. It never loads the reference's fixture on this path. Remove unsupported measurements, sample annotations, and fallback values. Golden approval applies to design, not fictional evidence; use draft examples only for explicit development/review.

The starting golden is scaffolding, not the finished outline. Keep useful compositions, but reorder, resize, combine, replace, or add sections and change navigation when the question calls for it. Borrow complementary groupings or interactions from other goldens; read only the additional implementation and CSS needed, not the whole catalog. Integrate borrowed parts into one coherent page with consistent controls and spacing. There is no one-reference limit or requirement to preserve the starting dashboard's tabs, chart types, or block count.

Create an original composition when existing patterns do not serve the analysis. A custom layout can still use shared cards, charts, controls, and tables; it does not require inventing new components. Do not keep a section merely because it was copied, fill unsupported slots, or add variety without analytical purpose.

Omit `--from-reference` to use the populated base when no golden provides a useful starting composition. Both modes return a compact golden index for further borrowing. Preserve sparse answers and user-requested custom layouts. Use `--blank` only when the user requests starting from scratch; a small dataset or lack of a matching reference does not require an empty project.

The helper refuses existing destinations. Revise existing apps in place. Read the copied `AGENTS.md` for boundaries and author React/CSS in `src/content/`. Before consulting component APIs, follow the contract's [read-only reference lookup](../../shared/data-app.md#resolve-the-component-reference) and read only needed topics from the returned `documentation.entryPoint`; this also resolves current bindings for older apps. Reuse public cards, charts, controls, tables, and source actions before creating a custom component. Wrap custom evidence in `DataComponent` with stable identities and reviewed rows.

## Compose the page and interactions

Put useful evidence under the shell title and scoped controls. Use `Section`/`SectionHeader` and the copied `AGENTS.md` geometry defaults. Keep related views visible together, size them to their evidence, avoid redundant nested frames, and preserve requested custom layouts.

Use canvas for independent movable/resizable blocks, freeform for authored grids or sidebars, and a composite block for tightly linked views. These mechanisms do not prescribe analytical structure. Keep the intended Edit-mode affordances and saved user placement; consult the [sortable layout API](../../templates/data-app/base/docs/components/sortable-layout.md) for details.

Place controls at their actual page, tab, section, or chart scope, grouped in the shared header slot. Intersect local filters with original reviewed rows and apply the same population to visuals, sources, copying, and export. Keep identity-bearing filters out of URLs. A tab needs a distinct analytical or operational job; a supporting records table belongs with its chart, in expandable detail or source inspection, not in a tab inherited from a reference.

A filter changes the current view; a drill-down reveals additional records or explanation and offers a clear return. Keep comparisons needed for the main question visible together; inspecting one entity at a time does not replace comparing entities or their histories. Put secondary exploration on the relevant chart mark or row; avoid repeated card-header buttons that just select an entity and open its records. Do not label filter presets as investigations or duplicate an existing selector with a button. Add scenarios only when useful and supported, with assumptions, modeled outputs, and reset separate from observed data.

## Copy and presentation

Use one shell title and concise, sentence-case measurement labels. Section headings name the measurement or grouping, not a vague phrase lifted from the prompt. Omit a heading that only repeats the cards beneath it. Keep an accessible authored h1 without repeating the title as a visible hero. Keep filter values and index baselines in their controls or info descriptions, not bullet-separated title suffixes. Do not invent branding, eyebrows, introductions, instruction subtitles, or evaluation/privacy prose. Preserve explicit user-authored or requested commentary.

Do not add a visible sample-data indicator or disclosure unless the user asks. Keep truthful classification in source metadata; this does not permit calling fictional evidence real. A definition, qualification, or caveat has one presentation home: the relevant label, tooltip/info description, or source sidebar. If it is already there, do not repeat it as a paragraph or badge. Make the measurement label accurate rather than adding contradictory explanatory prose.

Keep dates human-readable and units/signs consistent. Omit redundant axis titles, not informative ticks or units. Use semantic delta color according to the objective while keeping ambiguous changes neutral; absolute trends retain their series colors. Use the [comparison formatting API](../../templates/data-app/base/docs/components/comparison-formatting.md) rather than inventing formatting. Keep values legible, labels contained, controls wrapping, and wide record tables scrolling within their container.

## Build, inspect, and deliver

Build with the copied project's `AGENTS.md`, then follow the contract's [preview and verification guidance](../../shared/data-app.md#build-and-verification). Show a useful first view promptly and complete the requested scope in that same artifact.

During the contract's bounded rendered review, check the opening hierarchy, distinct value of each view, redundant copy/tables, and alignment. Fix changed content and inspect again; report which checks actually ran.

Verify calculations, definitions, source/filter/export scope, and coverage of the planned questions. Retained source rows alone do not establish that the dashboard answers a question; check that its needed comparison is available in the authored views. Return the artifact and specific remaining gaps. Keep it private unless publication is explicitly authorized; then use [publish-artifact-to-sites](../publish-artifact-to-sites/SKILL.md), including its dashboard-refresh follow-up. For a requested sharing summary, use [share-artifact-summary](../share-artifact-summary/SKILL.md).
