import assert from "node:assert/strict";
import test from "node:test";
import { fileURLToPath } from "node:url";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { createServer } from "vite";

test("source sections reflect available evidence without treating an empty result as missing", async () => {
  const server = await createServer({ root: fileURLToPath(new URL("..", import.meta.url)), configFile: false, server: { middlewareMode: true, hmr: false },
    optimizeDeps: { noDiscovery: true, entries: [] }, appType: "custom" });
  try {
    const { SourceInspector } = await server.ssrLoadModule("/src/components/SourceInspector.jsx");
    const component = { id: "test-chart", queryId: "reviewed", title: "Reviewed chart", kind: "chart" };
    const render = query => renderToStaticMarkup(React.createElement(SourceInspector, { component, query, rows: query.rows ?? [], filters: [] }));
    const file = render({ source: { files: [{ label: "reviewed.csv" }], caveats: ["Coverage is partial."] } });
    assert.match(file, /reviewed.csv/u);
    assert.match(file, /Coverage is partial/u);
    assert.doesNotMatch(file, /SQL query|Data preview|Evidence flow|Query executed/u);
    const website = render({ source: { url: "https://example.com/reviewed", executedAt: "2026-08-24T00:00:00Z" } });
    assert.match(website, /https:\/\/example.com\/reviewed/u);
    assert.match(website, /Source captured/u);
    assert.doesNotMatch(website, /SQL query|Evidence flow/u);
    const empty = render({ rows: [], source: { sql: "SELECT value FROM reviewed WHERE false" } });
    assert.match(empty, /Data preview/u);
    assert.match(empty, /SQL query/u);
    assert.doesNotMatch(empty, /Evidence flow/u);
    const provided = render({ source: { evidenceFlow: ["Read the supplied file", "Checked the reviewed values"] } });
    assert.match(provided, /Evidence flow/u);
    assert.match(provided, /Read the supplied file/u);
    assert.doesNotMatch(provided, /SQL query|Data preview/u);
    const absent = render({ source: { sql: "  ", evidenceFlow: [null, {}, " "] } });
    assert.doesNotMatch(absent, /role="tab"/u);
    assert.match(absent, /Source details weren’t recorded/u);
  } finally { await server.close(); }
});
