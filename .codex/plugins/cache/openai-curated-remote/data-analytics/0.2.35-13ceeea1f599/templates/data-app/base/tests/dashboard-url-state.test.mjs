import assert from "node:assert/strict";
import test from "node:test";
import { dateRangePresets } from "../src/date-range.js";

import {
  dashboardUrlWithState,
  readDashboardUrlState,
  resolveDashboardUrlFilters,
  serializeDashboardUrlState,
  validFilterValue,
} from "../src/dashboard-url-state.js";

test("multi-select URL, saved tab, drill and clear states preserve validated arrays", async () => {
  const { dashboardView, drillDashboardView } = await import("../src/dashboard-view-state.js");
  const multi = { filters: [
    { id: "region", field: "region", multiple: true, defaultValue: ["EMEA"], queryIds: ["regional"] },
    { id: "private", field: "region", multiple: true, shareInUrl: false },
  ], queries: { regional: { rows: [{ region: "EMEA" }, { region: "Americas" }, { region: "Asia, Pacific" }] },
    unrelated: { rows: [{ region: "unscoped" }] } } };
  const views = [{ id: "overview", filterIds: ["region"] }];
  const urlFor = filters => dashboardUrlWithState("https://dashboard.chatgpt.site/", multi, views, { filters });
  const selected = ["Americas", "EMEA"];
  const state = readDashboardUrlState(multi, views, urlFor({ region: [...selected].reverse(), private: ["EMEA"] }));
  assert.deepEqual(state.filters, { region: selected });
  assert.deepEqual(dashboardView(multi, views, "overview", { filters: state.filters }).filters, state.filters);
  assert.deepEqual(drillDashboardView(multi, views, "overview", {}, { filters: state.filters }).filters, state.filters);
  assert.deepEqual(readDashboardUrlState(multi, views, urlFor({ region: [] })).filters, { region: [] });
  assert.deepEqual(readDashboardUrlState(multi, views, urlFor({ region: ["Asia, Pacific"] })).filters, { region: ["Asia, Pacific"] });
  assert.equal(urlFor({ region: ["EMEA"] }).search, "");
  for (const value of [["unscoped"], ["all"], [null], [5], ["EMEA".repeat(600)]]) {
    assert.equal(validFilterValue(multi, multi.filters[0], value), false);
    assert.equal(urlFor({ region: value }).search, "");
  }
  assert.equal(validFilterValue(multi, { ...multi.filters[0], multiple: false }, selected), false);
  assert.deepEqual(readDashboardUrlState(multi, views, "https://dashboard.chatgpt.site/?f.region=%5Bbad").filters, {});
  assert.deepEqual(readDashboardUrlState(multi, views, "https://dashboard.chatgpt.site/?f.region=EMEA&f.region=Americas").filters, {});
  assert.deepEqual(readDashboardUrlState(multi, views, "https://dashboard.chatgpt.site/?f.region=EMEA").filters, { region: "EMEA" });
});

const snapshot = {
  filters: [
    { id: "week", field: "week", defaultValue: "2026-08-10" },
    { id: "segment", field: "segment", defaultValue: "all" },
    { id: "region", field: "region", defaultValue: "all", queryIds: ["regional"] },
    { id: "account", field: "account", defaultValue: "all", shareInUrl: false },
  ],
  queries: {
    regional: {
      rows: [
        { week: "2026-08-10", segment: "API", region: "North America", account: "private@example.com" },
        { week: "2026-08-03", segment: "Search & discovery", region: "EMEA", account: "another@example.com" },
      ],
    },
    other: {
      rows: [{ week: "2026-08-10", segment: "東京", region: "unscoped", account: "hidden@example.com" }],
    },
  },
};
const tabs = [{ id: "dashboard", label: "Dashboard" }, { id: "adoption", label: "Adoption" }];

test("dashboard view parameters round-trip known tabs and declared non-default filters", () => {
  const state = {
    tab: "adoption",
    filters: { week: "2026-08-03", segment: "Search & discovery", region: "EMEA" },
  };
  const serialized = serializeDashboardUrlState(snapshot, tabs, state);

  assert.equal(serialized.toString(),
    "tab=adoption&f.region=EMEA&f.segment=Search+%26+discovery&f.week=2026-08-03");
  assert.deepEqual(readDashboardUrlState(snapshot, tabs,
    `https://dashboard.chatgpt.site/?${serialized}`), { ...state, hasViewState: true });
});

test("default dashboard tabs and default filter selections produce clean URLs", () => {
  const state = { tab: "dashboard", filters: { week: "2026-08-10", segment: "all", region: "all" } };
  assert.equal(serializeDashboardUrlState(snapshot, tabs, state).toString(), "");
  assert.equal(dashboardUrlWithState("https://dashboard.chatgpt.site/?tab=dashboard&f.segment=all", snapshot,
    tabs, state).toString(), "https://dashboard.chatgpt.site/");
});

test("dashboard filter serialization remains stable and correctly encodes reviewed Unicode values", () => {
  assert.equal(serializeDashboardUrlState(snapshot, tabs, {
    tab: "dashboard",
    filters: { week: "2026-08-03", segment: "東京", region: "EMEA" },
  }).toString(), "f.region=EMEA&f.segment=%E6%9D%B1%E4%BA%AC&f.week=2026-08-03");
});

test("unknown, stale, malformed, duplicate, and query-out-of-scope filter values are rejected", () => {
  const url = "https://dashboard.chatgpt.site/?tab=deleted&f.segment=unknown&f.week=2026-08-03"
    + "&f.week=2026-08-10&f.region=unscoped&f.missing=secret";
  assert.deepEqual(readDashboardUrlState(snapshot, tabs, url), {
    tab: null,
    filters: {},
    hasViewState: false,
  });
  assert.equal(serializeDashboardUrlState(snapshot, tabs, {
    tab: "deleted",
    filters: { segment: "unknown", region: "unscoped", missing: "secret" },
  }).toString(), "");
});

test("filters marked shareInUrl false remain viewer-local and never enter shared links", () => {
  const url = "https://dashboard.chatgpt.site/?f.account=private%40example.com&f.region=EMEA";
  const state = readDashboardUrlState(snapshot, tabs, url);
  assert.deepEqual(state, { tab: null, filters: { region: "EMEA" }, hasViewState: true });
  assert.equal(serializeDashboardUrlState(snapshot, tabs, {
    filters: { account: "private@example.com", region: "EMEA" },
  }).toString(), "f.region=EMEA");
  assert.deepEqual(resolveDashboardUrlFilters(snapshot,
    { account: "private@example.com", segment: "API" }, state), {
    account: "private@example.com",
    region: "EMEA",
    segment: "all",
    week: "2026-08-10",
  });
});

test("explicit URL selections override local state while ordinary visits preserve local exploration", () => {
  const local = { week: "2026-08-03", segment: "API", region: "North America" };
  const explicit = readDashboardUrlState(snapshot, tabs, "https://dashboard.chatgpt.site/?f.region=EMEA");
  const ordinary = readDashboardUrlState(snapshot, tabs, "https://dashboard.chatgpt.site/?token=private");

  assert.deepEqual(resolveDashboardUrlFilters(snapshot, local, explicit), {
    week: "2026-08-10", segment: "all", region: "EMEA",
  });
  assert.deepEqual(resolveDashboardUrlFilters(snapshot, local, ordinary), local);
  assert.deepEqual(resolveDashboardUrlFilters(snapshot, local, ordinary, { reset: true }), {
    week: "2026-08-10", segment: "all", region: "all",
  });
});

test("explicit all selections round-trip for categorical filters with non-all dashboard defaults", () => {
  const defaultedSnapshot = {
    ...snapshot,
    filters: snapshot.filters.map((filter) => filter.id === "segment"
      ? { ...filter, defaultValue: "API" } : filter),
  };
  const state = readDashboardUrlState(defaultedSnapshot, tabs,
    "https://dashboard.chatgpt.site/?f.segment=all");

  assert.deepEqual(state, { tab: null, filters: { segment: "all" }, hasViewState: true });
  assert.equal(resolveDashboardUrlFilters(defaultedSnapshot, { segment: "API" }, state).segment, "all");
  assert.equal(serializeDashboardUrlState(defaultedSnapshot, tabs, {
    filters: { segment: "all" },
  }).toString(), "f.segment=all");
});

test("date filters with a required non-all default reject unavailable all selections", () => {
  assert.deepEqual(readDashboardUrlState(snapshot, tabs,
    "https://dashboard.chatgpt.site/?f.week=all"), {
    tab: null,
    filters: {},
    hasViewState: false,
  });
  assert.equal(serializeDashboardUrlState(snapshot, tabs, {
    filters: { week: "all" },
  }).toString(), "");
});

test("invalid or deleted URL selections cannot replace saved viewer-local filter state", () => {
  const local = { week: "2026-08-03", segment: "API", region: "North America" };

  for (const href of [
    "https://dashboard.chatgpt.site/?tab=deleted",
    "https://dashboard.chatgpt.site/?tab=adoption&tab=dashboard",
    "https://dashboard.chatgpt.site/?f.region=unknown",
    "https://dashboard.chatgpt.site/?f.week=2026-08-03&f.week=2026-08-10",
  ]) {
    const state = readDashboardUrlState(snapshot, tabs, href);
    assert.equal(state.hasViewState, false, `${href} must not count as an explicit shareable view.`);
    assert.deepEqual(resolveDashboardUrlFilters(snapshot, local, state), local);
  }
});

test("copied component URLs include only validated view state and strip browser-private context", () => {
  const source = "https://publisher:secret@dashboard.chatgpt.site/_data/charts/Ab12Cd34"
    + "?token=private&codexThreadId=thread&f.account=private%40example.com#codexThreadId=thread";
  const shared = dashboardUrlWithState(source, snapshot, tabs, {
    tab: "adoption",
    filters: { region: "EMEA", account: "private@example.com" },
  }, { preserveExisting: false });

  assert.equal(shared.toString(), "https://dashboard.chatgpt.site/_data/charts/Ab12Cd34?tab=adoption&f.region=EMEA");
  assert.doesNotMatch(shared.toString(), /publisher|secret|private|codexThreadId|account/u);
});

test("in-browser URL updates preserve unrelated host query parameters and Codex task fragments", () => {
  const source = "https://dashboard.chatgpt.site/_data/charts/Ab12Cd34?token=private&f.old=stale"
    + "#codexThreadId=550e8400-e29b-41d4-a716-446655440000";
  const next = dashboardUrlWithState(source, snapshot, tabs, {
    tab: "adoption",
    filters: { segment: "API" },
  });

  assert.equal(next.searchParams.get("token"), "private");
  assert.equal(next.searchParams.get("tab"), "adoption");
  assert.equal(next.searchParams.get("f.segment"), "API");
  assert.equal(next.searchParams.has("f.old"), false);
  assert.match(next.hash, /^#codexThreadId=/u);
});

test("invalid locations and oversized values never create unsafe dashboard view state", () => {
  assert.deepEqual(readDashboardUrlState(snapshot, tabs, "not a URL"), {
    tab: null, filters: {}, hasViewState: false,
  });
  assert.equal(dashboardUrlWithState("not a URL", snapshot, tabs, {}), null);
  assert.equal(serializeDashboardUrlState(snapshot, tabs, {
    filters: { segment: "x".repeat(2_001) },
  }).toString(), "");
});

test("declared filter identifiers cannot mutate dashboard URL-state object prototypes", () => {
  const unusualSnapshot = {
    filters: [{ id: "__proto__", field: "category", defaultValue: "all" }],
    queries: { reviewed: { rows: [{ category: "safe" }] } },
  };
  const state = readDashboardUrlState(unusualSnapshot, tabs,
    "https://dashboard.chatgpt.site/?f.__proto__=safe");

  assert.equal(Object.getPrototypeOf(state.filters), Object.prototype);
  assert.equal(Object.hasOwn(state.filters, "__proto__"), true);
  assert.equal(state.filters.__proto__, "safe");
  const resolved = resolveDashboardUrlFilters(unusualSnapshot, {}, state);
  assert.equal(Object.getPrototypeOf(resolved), Object.prototype);
  assert.equal(Object.hasOwn(resolved, "__proto__"), true);
  assert.equal(resolved.__proto__, "safe");
});


test("tab scopes restore independent views and drill through only declared destination fields", async () => {
  const { dashboardTabId, dashboardTabSnapshot, dashboardView, drillDashboardView } = await import("../src/dashboard-view-state.js");
  const definitions = [{ id: "dashboard", filterIds: ["week", "region"] },
    { id: "adoption", aliases: ["retention"], filterIds: ["week", "segment"], focusFields: ["accountId"] }];
  const manual = { filters: { week: "2026-08-03", segment: "API" }, focus: { accountId: "private-account" } };
  const overview = dashboardView(snapshot, definitions, "dashboard", { filters: { region: "EMEA", segment: "API" } });
  assert.deepEqual(overview.filters, { week: "2026-08-10", region: "EMEA" });
  const target = drillDashboardView(snapshot, definitions, "adoption", manual, {
    filters: { week: "2026-08-10", segment: "東京", region: "EMEA", sql: "private" },
    focus: { accountId: "selected-account", sql: "private" },
  });
  assert.deepEqual(target, { filters: { week: "2026-08-10", segment: "東京" }, focus: { accountId: "selected-account" } });
  assert.deepEqual(dashboardView(snapshot, definitions, "adoption", manual), manual, "temporary drill does not change saved browsing state");
  assert.equal(dashboardTabId(definitions, "retention"), "adoption");
  const scoped = dashboardTabSnapshot(snapshot, definitions, "adoption");
  const url = serializeDashboardUrlState(scoped, tabs, { tab: "adoption", filters: { ...target.filters, accountId: "selected-account", region: "EMEA" } }).toString();
  assert.ok(!url.includes("account") && !url.includes("region") && !url.includes("sql"));
  assert.deepEqual(dashboardView(snapshot, definitions, "adoption", manual, readDashboardUrlState(scoped, tabs,
    `https://dashboard.chatgpt.site/?${url}`)).filters, target.filters);
  assert.equal(dashboardTabSnapshot(snapshot, tabs, "adoption"), snapshot, "legacy definitions retain shared filters");
});

test("inclusive date ranges round-trip and invalid boundaries are rejected", () => {
  const ranged = { ...snapshot, filters: [{ id: "date", field: "week", mode: "through", defaultValue: "2026-08-10" }] };
  const state = { tab: "adoption", filters: { date: "2026-08-03..2026-08-10" } };
  const url = serializeDashboardUrlState(ranged, tabs, state);
  assert.deepEqual(readDashboardUrlState(ranged, tabs, `https://dashboard.chatgpt.site/?${url}`).filters, state.filters);
  for (const invalid of ["2026-08-10..2026-08-03", "2026-08-01..2026-08-10", "2026-02-30..2026-08-10"])
    assert.deepEqual(readDashboardUrlState(ranged, tabs, `https://dashboard.chatgpt.site/?f.date=${invalid}`).filters, {});
});

test("sparse-date calendar presets round-trip without snapping to observations", () => {
  const ranged = { filters: [{ id: "date", field: "week", mode: "through", queryIds: ["weekly"] }],
    queries: { weekly: { rows: ["2026-07-01", "2026-07-08", "2026-08-05", "2026-08-12"].map(week => ({week})) },
      unrelated: { rows: [{week:"2026-06-01"},{week:"2026-09-01"}] } } };
  const filter = ranged.filters[0];
  const presets = dateRangePresets("2026-07-01", "2026-08-12");
  assert.equal(presets.length, 3);
  for (const {value} of presets) {
    const filters = {date:value};
    const url = dashboardUrlWithState("https://dashboard.chatgpt.site/", ranged, tabs, {filters});
    assert.equal(url.searchParams.get("f.date"), value);
    assert.deepEqual(readDashboardUrlState(ranged,tabs,url).filters, filters);
  }
  for (const invalid of ["2026-06-30..2026-08-12", "2026-07-01..2026-08-13",
    "2026-07-31..2026-07-01", "2026-07-32..2026-08-12", "2026-02-30..2026-08-12"])
    assert.equal(validFilterValue(ranged,filter,invalid),false,invalid);
  assert.equal(validFilterValue({...ranged,queries:{}},filter,presets[0].value),false);
});
