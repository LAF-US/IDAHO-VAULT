import assert from "node:assert/strict";
import { cpSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { chromium } from "playwright-core";

import { componentPermalinkShortId } from "../templates/data-app/base/src/chart-permalink.js";
import { dateRangePresets } from "../templates/data-app/base/src/date-range.js";
import { resolveChromiumExecutable, runDataAppFixtureBuild } from "./browser-helpers.mjs";

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const projectRoot = mkdtempSync(join(tmpdir(), "data-url-state-browser-"));
cpSync(join(pluginRoot, "templates/data-app/base"), projectRoot, {
  recursive: true,
  filter: (path) => !path.includes("/node_modules") && !path.includes("/dist"),
});
const build = runDataAppFixtureBuild(projectRoot, { pluginRoot });
assert.equal(build.status, 0, `${build.stdout}\n${build.stderr}`);
const html = readFileSync(join(projectRoot, "dist/index.html"), "utf8");
const snapshot = JSON.parse(readFileSync(resolve(pluginRoot, "templates/data-app/base/src/data.json"), "utf8"));
snapshot.filters.push({
  id: "account",
  label: "Account",
  field: "account",
  queryIds: ["account_health"],
  defaultValue: "all",
  shareInUrl: false,
});
snapshot.filters.push({
  id: "risk",
  label: "Risk tier",
  field: "riskTier",
  queryIds: ["account_health"],
  defaultValue: "Moderate",
});

const origin = "https://dashboard-url-state.chatgpt.site";
const taskId = "550e8400-e29b-41d4-a716-446655440000";
let canEdit = true;
const presentationWrites = [];
const failures = [];
const browser = await chromium.launch({
  executablePath: resolveChromiumExecutable(),
  headless: true,
});

try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1050 } });
  page.on("pageerror", (error) => failures.push(error.message));
  await page.route(`${origin}/**`, (route) => {
    const { pathname } = new URL(route.request().url());
    if (pathname === "/api/presentation" && route.request().method() === "PUT") {
      presentationWrites.push(route.request().postData());
    }
    const payload = pathname === "/api/snapshot" ? snapshot
      : pathname === "/api/presentation" ? {
        canEdit,
        presentation: {
          tabs: [{ id: "overview", label: "Overview" }, { id: "dashboard", label: "Dashboard" }],
        },
        revision: 0,
      } : null;
    return route.fulfill(payload
      ? { contentType: "application/json", body: JSON.stringify(payload) }
      : { contentType: "text/html", body: html });
  });
  await page.addInitScript(({ title }) => {
    window.__urlStateClipboard = [];
    window.__urlStateHistoryReplacements = [];
    const replaceState = history.replaceState;
    history.replaceState = function captureUrlStateReplacement(...args) {
      window.__urlStateHistoryReplacements.push(String(args[2] ?? ""));
      return replaceState.apply(this, args);
    };
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText: async (value) => window.__urlStateClipboard.push(value) },
    });
    if (!localStorage.getItem("data-app-url-state-seeded")) {
      localStorage.setItem("data-app-url-state-seeded", "true");
      localStorage.setItem(`data-app:presentation:v1:/:${title}`, JSON.stringify({
        version: 1,
        presentation: {
          filters: { segment: "API", region: "APAC", account: "Northstar Workshop" },
          assumptions: { activationLift: 17, retentionLift: 9 },
        },
      }));
    }
  }, { title: snapshot.title });

  await page.goto(`${origin}/?tab=dashboard&f.risk=all`, { waitUntil: "load" });
  await page.locator('[data-component-id="active-users"] .metric-value').waitFor();
  assert.equal(new URL(page.url()).searchParams.get("f.risk"), "all",
    "An explicitly shared All selection must survive a categorical filter's non-All dashboard default.");
  assert.match(await page.locator('[aria-label="Data app filters"]')
    .getByRole("button", { name: "Risk tier" }).innerText(), /All/u,
  "The initial rendered view must honor an explicitly shared All selection before any interaction.");
  await page.reload({ waitUntil: "load" });
  await page.locator('[data-component-id="active-users"] .metric-value').waitFor();
  assert.equal(new URL(page.url()).searchParams.get("f.risk"), "all",
    "Refreshing a shared All selection must not replace it with the categorical dashboard default.");

  const weeks = [...new Set(Object.values(snapshot.queries).flatMap(({rows=[]}) => rows.map(row=>row.week))
    .filter(value=>typeof value === "string"))].sort();
  const preset = dateRangePresets(weeks[0],weeks.at(-1))[0];
  assert(preset && !weeks.includes(preset.start), "Exercise a preset boundary between weekly observations");
  await page.getByRole("button", {name:"Date range",exact:true}).click();
  await page.getByRole("menuitem", {name:/^(Last|Latest) 7 days/}).click();
  await page.waitForURL(url=>url.searchParams.get("f.week")===preset.value);
  const sharedRangeUrl = page.url();
  await page.reload({waitUntil:"load"});
  await page.locator('[data-component-id="active-users"] .metric-value').waitFor();
  assert.equal(new URL(page.url()).searchParams.get("f.week"),preset.value,
    "A shared sparse-date preset must preserve its exact date scope after reload");
  assert.equal(page.url(),sharedRangeUrl);

  await page.goto(`${origin}/?tab=dashboard&token=private&f.segment=Studio&f.account=Northstar+Workshop`
    + `#codexThreadId=${taskId}`, { waitUntil: "load" });
  await page.locator('[data-component-id="active-users"] .metric-value').waitFor();
  assert.match(await page.locator('[data-component-id="active-users"] .metric-value').innerText(), /5\.4K/u,
    "Explicit shared filters must override stale viewer-local selections before the reviewed dashboard renders.");
  assert.equal(new URL(page.url()).searchParams.get("f.segment"), "Studio");
  assert.equal(new URL(page.url()).searchParams.has("f.region"), false,
    "Missing shareable filters in an explicit shared view must use dashboard defaults, not stale local state.");
  assert.equal(new URL(page.url()).searchParams.has("f.account"), false,
    "Private filter parameters must be removed from the visible dashboard URL.");
  assert.equal(new URL(page.url()).searchParams.get("token"), "private",
    "In-app URL synchronization must preserve unrelated browser-owned host context.");
  assert.equal(new URL(page.url()).hash, `#codexThreadId=${taskId}`);

  const historyBeforeFilter = await page.evaluate(() => ({
    length: history.length,
    replacements: window.__urlStateHistoryReplacements.length,
  }));
  await page.locator('[aria-label="Data app filters"]').getByRole("button", { name: "Region" }).click();
  await page.getByRole("menuitemradio", { name: "North America" }).click();
  await page.waitForURL((url) => url.searchParams.get("f.region") === "North America");
  assert.equal(await page.evaluate(() => history.length), historyBeforeFilter.length,
    "Filter adjustments must replace the current history entry instead of polluting browser history.");
  assert.ok(await page.evaluate(() => window.__urlStateHistoryReplacements.length)
    > historyBeforeFilter.replacements);

  await page.locator('[aria-label="Data app filters"]').getByRole("button", { name: "Account" }).click();
  await page.getByRole("menuitemradio", { name: "Atlas Canvas" }).click();
  assert.equal(new URL(page.url()).searchParams.has("f.account"), false,
    "Changing an explicitly private account filter must never expose its reviewed value in the URL.");

  async function copyComponent(id, title) {
    const component = page.locator(`[data-component-id="${id}"]`);
    await component.getByRole("button", { name: `${title} actions` }).click();
    await page.getByRole("menu", { name: `${title} actions` })
      .getByRole("menuitem", { name: "Copy link", exact: true }).click();
    return new URL(await page.evaluate(() => window.__urlStateClipboard.at(-1)));
  }

  const chartLink = await copyComponent("usage-trend", "Active accounts over time");
  const metricLink = await copyComponent("active-users", "Weekly active accounts");
  for (const [kind, id, link] of [
    ["charts", "usage-trend", chartLink],
    ["components", "active-users", metricLink],
  ]) {
    assert.equal(link.pathname, `/_data/${kind}/${componentPermalinkShortId(origin, id)}`);
    assert.deepEqual([...link.searchParams.entries()], [
      ["f.region", "North America"], ["f.segment", "Studio"],
    ], `${id} must preserve only validated selected-tab and non-default reviewed-filter state.`);
    assert.equal(link.hash, "");
    assert.doesNotMatch(link.href, /token|private|Atlas|Northstar|codexThreadId|activationLift|retentionLift/u,
      `${id} must not leak unrelated host credentials, private account filters, or scenario assumptions.`);
  }

  await page.getByRole("button", { name: "Ask ChatGPT" }).click();
  await page.getByRole("dialog", { name: "Ask ChatGPT about this dashboard" })
    .getByRole("button", { name: "Copy link", exact: true }).click();
  assert.equal(await page.evaluate(() => window.__urlStateClipboard.at(-1)), `${origin}/`,
    "Dashboard-level Copy link must remain a clean canonical Site URL.");

  await page.reload({ waitUntil: "load" });
  await page.locator('[data-component-id="active-users"] .metric-value').waitFor();
  assert.equal(new URL(page.url()).searchParams.get("f.region"), "North America");
  assert.equal(new URL(page.url()).searchParams.get("f.segment"), "Studio");
  assert.match(await page.locator('[data-component-id="active-users"] .metric-value').innerText(), /5\.4K/u);

  assert.equal(await page.getByRole("tablist").count(), 0,
    "A single authored dashboard page must not show navigation from stale saved tabs.");

  const detailLink = new URL(chartLink);
  detailLink.pathname += "/detail";
  await page.goto(detailLink.href, { waitUntil: "load" });
  const chartExplorer = page.getByRole("dialog", { name: "Active accounts over time" });
  await chartExplorer.waitFor();
  await chartExplorer.getByRole("button", { name: "Cancel", exact: true }).click();
  await chartExplorer.waitFor({ state: "hidden" });
  assert.equal(page.url(), chartLink.href,
    "Closing an existing chart-detail permalink must preserve its selected tab and shared filter parameters.");

  canEdit = false;
  const writesBeforeViewer = presentationWrites.length;
  await page.goto(chartLink.href, { waitUntil: "load" });
  await page.locator('[data-component-id="usage-trend"]').waitFor();
  const viewerLink = await copyComponent("usage-trend", "Active accounts over time");
  assert.equal(viewerLink.href, chartLink.href,
    "Read-only dashboard viewers must retain contextual chart sharing without gaining edit access.");
  assert.equal(presentationWrites.length, writesBeforeViewer,
    "Opening or copying a contextual chart link must never write shared owner-authored presentation.");

  await page.goto(`${origin}${chartLink.pathname}`, { waitUntil: "load" });
  await page.locator('[data-component-id="usage-trend"]').waitFor();
  assert.equal(new URL(page.url()).searchParams.has("tab"), false,
    "Single-page chart links must keep the implicit dashboard page out of the URL.");

  await page.evaluate(({ title }) => {
    localStorage.setItem(`data-app:presentation:v1:/:${title}`, JSON.stringify({
      version: 1,
      presentation: {
        filters: { segment: "API", region: "APAC", account: "Northstar Workshop" },
      },
    }));
  }, { title: snapshot.title });
  await page.goto(`${origin}/?tab=deleted&f.segment=unknown`, { waitUntil: "load" });
  await page.locator('[data-component-id="usage-trend"]').waitFor();
  assert.equal(new URL(page.url()).searchParams.get("f.segment"), "API",
    "An invalid shared filter must not replace the viewer's previously saved segment.");
  assert.equal(new URL(page.url()).searchParams.get("f.region"), "APAC",
    "A deleted shared tab must not reset unrelated saved viewer-local dashboard filters.");

  await page.goto(`${origin}/?tab=deleted&f.segment=unknown&f.region=EMEA&f.account=Beacon+Index`, {
    waitUntil: "load",
  });
  await page.locator('[data-component-id="usage-trend"]').waitFor();
  const sanitized = new URL(page.url());
  assert.equal(sanitized.searchParams.has("tab"), false);
  assert.equal(sanitized.searchParams.has("f.segment"), false);
  assert.equal(sanitized.searchParams.has("f.account"), false);
  assert.equal(sanitized.searchParams.get("f.region"), "EMEA");
  assert.equal(await page.getByRole("tablist").count(), 0);

  assert.deepEqual(failures, []);
  process.stdout.write(`${JSON.stringify({
    status: "passed",
    scenarios: [
      "reviewed URL filter validation and stale-local-state precedence",
      "explicit categorical All selections override non-All dashboard defaults",
      "private filter and scenario exclusion",
      "clean dashboard links and contextual chart/component links",
      "history-safe filtering and single-page navigation cleanup",
      "reload and chart-detail permalink preservation",
      "read-only viewer sharing without presentation writes",
      "legacy permalink tab synchronization and stale URL state isolation",
      "invalid tabs and filter sanitization",
    ],
  }, null, 2)}\n`);
} finally {
  await browser.close();
  rmSync(projectRoot, { recursive: true, force: true });
}
