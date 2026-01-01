import assert from "node:assert/strict";
import test from "node:test";
import { fileURLToPath } from "node:url";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { createServer } from "vite";

import { publishReviewDestination } from "../src/publish-review.js";
import { dataAppActionHref, dataAppActionRequest } from "../src/data-app-actions.js";

test("review destination names come from the actual supported route", () => {
  assert.equal(publishReviewDestination("codex://threads/new?prompt=review"), "Codex");
  assert.equal(publishReviewDestination("https://chatgpt.com/?q=review"), "ChatGPT");
  for (const value of [null, "", "not-a-url", "javascript:alert(1)", "https://chatgpt.com.evil.test/", "https://other.example/"]) {
    assert.equal(publishReviewDestination(value), null);
  }
});

test("publication review preserves the requested audience but never grants publication or automation authority", () => {
  for (const surface of ["dashboard", "report"]) for (const accessMode of [undefined, "custom", "workspace_all"]) {
    const context = { surface, accessMode, canEdit: true, reviewSharing: true,
      dataAppReference: { sourceUrl: "https://app.example.chatgpt.site/" } };
    const { prompt } = dataAppActionRequest("sites", context);
    assert.match(prompt, /read-only and does not authorize publication or access changes/u);
    assert.match(prompt, /ask for explicit confirmation before publishing/u);
    assert.match(prompt, /Do not query fresh data, create or change automations, deploy, publish, invite anyone, or change sharing/u);
    assert.match(prompt, /Do not publish if material permissions remain unresolved/u);
    assert.match(prompt, /complete publication payload/u);
    assert.match(prompt, /allowed_editors and editor-role groups/u);
    assert.match(prompt, /never promote viewers or workspace-wide access to editor access/u);
    assert.match(prompt, /explicit approval before applying Sites editor_changes/u);
    assert.match(prompt, /Verify source access and refresh authority separately/u);
    assert.doesNotMatch(prompt, /explicit action authorizes publication|Deploy the resulting project/u);
    if (accessMode === "workspace_all") assert.match(prompt, /workspace_all.*no external access/u);
    else if (accessMode === "custom") assert.match(prompt, /custom.*restricted to the creator/u);
    else assert.match(prompt, /Keep the existing Site audience.*do not reset or broaden/u);
    assert.equal(prompt.includes("Unknown schedule state"), surface === "dashboard");
    const link = new URL(dataAppActionHref("sites", context, new URL("https://app.example.chatgpt.site/")));
    assert.equal(link.searchParams.get("q"), prompt);
    assert.equal(link.searchParams.has("originUrl"), false);
  }
  for (const canEdit of [false, undefined]) assert.throws(() => dataAppActionRequest("sites", { reviewSharing: true, canEdit }), /Only the current owner/u);
  assert.throws(() => dataAppActionRequest("sites", { reviewSharing: true, canEdit: true, accessMode: "public" }), /supported publication audience/u);
  assert.match(dataAppActionRequest("sites", { canEdit: true }).prompt, /explicit action authorizes publication/u,
    "The established explicit publication contract remains available after review and confirmation");
});

test("review renders requested audience separately from unknown live settings and preserves surface capabilities", async () => {
  const server = await createServer({ root: fileURLToPath(new URL("../", import.meta.url)), configFile: false,
    optimizeDeps: { noDiscovery: true, entries: [] }, server: { middlewareMode: true, watch: null, hmr: false }, appType: "custom" });
  try {
    const { PublishReviewContent } = await server.ssrLoadModule("/src/components/PublishReviewDialog.jsx");
    for (const published of [false, true]) for (const surface of ["dashboard", "report"]) {
      const markup = renderToStaticMarkup(React.createElement(PublishReviewContent, {
        published, surface, accessMode: "custom", onAccessChange() {}, onClose() {}, href: "codex://threads/new?prompt=review",
      }));
      assert.equal((markup.match(/type="radio"/gu) ?? []).length, published ? 0 : 2);
      assert.equal((markup.match(/checked=""/gu) ?? []).length, published ? 0 : 1);
      assert.equal(markup.includes("Keep current access"), published);
      assert.equal(markup.includes("Refreshing data requires their own source permissions"), surface === "dashboard");
      assert.equal(markup.includes("Dashboard data is stored"), surface === "dashboard");
      assert.equal(markup.includes("Report data is stored"), surface === "report");
      assert.match(markup, /Editing doesn’t grant source access/u);
      assert.match(markup, /Includes all saved rows, even those hidden by filters/u);
      assert.doesNotMatch(markup, /<details|<summary|One check before publishing|What data is included/u);
      assert.doesNotMatch(markup, /No schedule|Refresh is off|Permissions verified/u);
      assert.match(markup, /href="codex:\/\/threads\/new\?prompt=review" target="_self"/u);
    }
    const unavailable = renderToStaticMarkup(React.createElement(PublishReviewContent, { onClose() {} }));
    assert.doesNotMatch(unavailable, /<a /u);
    assert.match(unavailable, /disabled=""/u);
  } finally { await server.close(); }
});
