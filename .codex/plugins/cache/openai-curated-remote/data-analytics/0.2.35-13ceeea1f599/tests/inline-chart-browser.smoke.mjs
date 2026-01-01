import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, realpath, rm, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Script } from "node:vm";

import { chromium } from "playwright-core";

import { resolveChromiumExecutable } from "./browser-helpers.mjs";
import { defaultInlineCacheDir, prepareInlineRuntime } from "../skills/visualize-data/scripts/inline-chart-build.mjs";
import { INLINE_ICON_NAMES, inlineCapacityInput } from "../scripts/prebuilt/build.mjs";
import { renderInlineSources } from "../skills/visualize-data/scripts/render-inline-sources.mjs";
import { inlineArtifactForChart } from "../templates/data-app/inline/chart-families.mjs";

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
// CI exercises a standalone plugin copy while reading the actual Codex host
// implementation from its reviewed repository checkout.
const monorepoRoot = resolve(process.env.DATA_INLINE_MONOREPO_ROOT || resolve(pluginRoot, "../../../.."));
const appRoot = join(monorepoRoot, "codex/codex-apps");
const inlineRenderer = join(pluginRoot, "skills/visualize-data/scripts/render-inline-chart.mjs");
const cacheRoot = resolve(process.env.DATA_INLINE_CACHE_DIR || defaultInlineCacheDir());
// Only the test's actual Codex host is compiled. Customer inline charts use the
// already-built runtime in the plugin and never borrow this dependency tree.
const hostDependencyRoot = resolve(
  process.env.DATA_INLINE_HOST_DEPENDENCY_ROOT || join(pluginRoot, "templates/data-app/base"),
);
const dependencyRequire = createRequire(join(hostDependencyRoot, "package.json"));
const executablePath = resolveChromiumExecutable();
const workspace = await mkdtemp(join(tmpdir(), "data-inline-chart-browser-"));
const rawSql = "SELECT active_users FROM restricted.raw_metric_input WHERE review_state = 'approved'";
const privateValue = "NEVER_EMBED_UNREVIEWED_PRIVATE_COLUMN";
const privateDefinition = "NEVER_EMBED_UNREVIEWED_PRIVATE_DEFINITION";
const privateSourceUrl = "https://reviewed-source.example.test/private-query";
const tabLabels = ["Overview", "Data preview", "SQL query", "Evidence flow"];
const marker = "<!--__INLINE_VISUALIZATION_FRAGMENT__-->";

const reviewedInput = {
  schemaVersion: 1,
  id: "reviewed-weekly-active-users",
  queryId: "reviewed-weekly-active-users-query",
  title: "Weekly active users by plan",
  chart: {
    type: "line",
    x: "week",
    y: "activeUsers",
    series: "plan",
    showArea: true,
    showXAxisLabel: false,
    yLabel: "Weekly active users",
    colors: { Pro: "var(--chart-1)", Team: "var(--chart-2)" },
    // Off-domain annotations must not promote private input columns into the artifact.
    annotations: [{ id: "unresolved-private-event", kind: "event", at: "2099-01-01",
      field: "unapprovedColumn", label: "UNAPPROVED_ANNOTATION_LABEL" }],
  },
  rows: [
    { week: "2026-07-13", plan: "Pro", activeUsers: 12400, unapprovedColumn: privateValue },
    { week: "2026-07-13", plan: "Team", activeUsers: 8200, unapprovedColumn: privateValue },
    { week: "2026-07-20", plan: "Pro", activeUsers: 13150, unapprovedColumn: privateValue },
    { week: "2026-07-20", plan: "Team", activeUsers: 8610, unapprovedColumn: privateValue },
    { week: "2026-07-27", plan: "Pro", activeUsers: 13800, unapprovedColumn: privateValue },
    { week: "2026-07-27", plan: "Team", activeUsers: 9040, unapprovedColumn: privateValue },
    { week: "2026-08-03", plan: "Pro", activeUsers: 14750, unapprovedColumn: privateValue },
    { week: "2026-08-03", plan: "Team", activeUsers: 9650, unapprovedColumn: privateValue },
    { week: "2026-08-10", plan: "Pro", activeUsers: 15800, unapprovedColumn: privateValue },
    { week: "2026-08-10", plan: "Team", activeUsers: 10290, unapprovedColumn: privateValue },
    { week: "2026-08-17", plan: "Pro", activeUsers: 17100, unapprovedColumn: privateValue },
    { week: "2026-08-17", plan: "Team", activeUsers: 11150, unapprovedColumn: privateValue },
  ],
  source: {
    label: "Reviewed product analytics",
    sql: rawSql,
    executedAt: "2026-08-17T16:00:00.000Z",
    tables: [{ name: "analytics.approved_weekly_users", href: `${privateSourceUrl}/table` }],
    files: [{ label: "Approved sample snapshot.csv", href: `${privateSourceUrl}/snapshot` }],
    links: [{ label: "Open reviewed query", href: privateSourceUrl }],
    metricDefinitions: [
      {
        label: "Weekly active users",
        field: "activeUsers",
        definition: "Unique accounts active during the reviewed week.",
      },
      {
        label: "Reporting week",
        field: "week",
        definition: "UTC reporting week when the reviewed account activity occurred.",
      },
      {
        label: "Plan attribution",
        field: "plan",
        definition: "Reviewed subscription plan attributed to the active account.",
      },
      {
        label: "Unapproved private attribution",
        field: "unapprovedColumn",
        definition: privateDefinition,
      },
    ],
    caveats: ["Reviewed sample contains no customer-level records."],
    evidenceFlow: [
      { title: "Approved reviewed snapshot", detail: "Twelve reviewed weekly plan observations." },
      { title: "Reviewed SQL query", detail: rawSql },
      { title: "Replacement metacharacters", detail: "$& $` $' $$ $1" },
    ],
  },
  generatedAt: "2026-08-17T16:05:00.000Z",
  height: 280,
  theme: "codex-classic",
};

const isolatedGapInput = {
  schemaVersion: 1,
  id: "reviewed-missing-week-wau",
  queryId: "reviewed-missing-week-wau-query",
  title: "Sample ChatGPT weekly active users",
  chart: {
    type: "line",
    x: "week",
    y: "wau",
    xLabel: "Week starting",
    yLabel: "Weekly active users",
    showLegend: false,
  },
  rows: [
    { week: "2026-07-27", wau: 120 },
    { week: "2026-08-03", wau: null },
    { week: "2026-08-10", wau: 145 },
  ],
  source: {
    label: "User-provided sample data",
    caveats: [
      "Sample values, not actual reported ChatGPT usage.",
      "August 3 is missing, not zero; no interpolation is applied.",
    ],
  },
  theme: "codex-classic",
};

const axisWeeks = ["2026-07-06", "2026-07-13", "2026-07-20", "2026-07-27", "2026-08-03", "2026-08-10"];
const closeThousandValues = [960, 976, 992, 1008, 1024, 1040];
const closeBillionValues = closeThousandValues.map((value) => value * 1_000_000);

function numericAxisInput(id, values, { type = "line", field = "activeUsers", chart = {}, rows } = {}) {
  return {
    schemaVersion: 1,
    id: `reviewed-readable-axis-${id}`,
    title: `Reviewed readable ${id} axis`,
    chart: {
      type,
      x: "week",
      y: field,
      startAtZero: false,
      showLegend: false,
      ...chart,
    },
    rows: rows ?? values.map((value, index) => ({ week: axisWeeks[index], [field]: value })),
    source: {
      label: "User-provided reviewed axis sample",
      caveats: ["Illustrative reviewed values; axis labels must remain distinct."],
    },
    theme: "codex-classic",
  };
}

const numericAxisCases = [
  {
    id: "scaled-millions",
    input: numericAxisInput("scaled-millions", closeThousandValues, {
      field: "activeUsersMillions",
      chart: { yLabel: "WAU (millions)" },
    }),
    axes: [{ orientation: "y", semantic: "small-integer" }],
  },
  {
    id: "raw-billion",
    input: numericAxisInput("raw-billion", closeBillionValues),
    axes: [{ orientation: "y", semantic: "large-compact" }],
  },
  {
    id: "negative-thousand",
    input: numericAxisInput(
      "negative-thousand",
      closeThousandValues.map((value) => -value),
    ),
    axes: [{ orientation: "y", semantic: "negative" }],
  },
  {
    id: "near-zero",
    input: numericAxisInput("near-zero", [-0.0002, -0.00012, -0.00004, 0.00004, 0.00012, 0.0002], {
      field: "measuredDelta",
    }),
    axes: [{ orientation: "y", semantic: "signed-near-zero" }],
  },
  {
    id: "tight-percentage",
    input: numericAxisInput("tight-percentage", [0.0995, 0.0997, 0.0999, 0.1001, 0.1003, 0.1005], {
      field: "conversionRate",
    }),
    axes: [{ orientation: "y", semantic: "precise-percentage" }],
  },
  {
    id: "horizontal-thousand",
    input: numericAxisInput("horizontal-thousand", closeThousandValues, {
      type: "horizontalBar",
      chart: { x: "plan", showYAxisLabel: false },
      rows: closeThousandValues.map((activeUsers, index) => ({
        plan: `Plan ${String.fromCodePoint(65 + index)}`,
        activeUsers,
      })),
    }),
    axes: [{ orientation: "x", semantic: "small-integer" }],
  },
  {
    id: "scatter-both-axes",
    input: numericAxisInput("scatter-both-axes", closeBillionValues, {
      type: "scatter",
      field: "revenue",
      chart: { x: "sessions", showYAxisLabel: false },
      rows: closeBillionValues.map((revenue, index) => ({
        sessions: closeThousandValues[index],
        revenue,
      })),
    }),
    axes: [
      { orientation: "x", semantic: "numeric" },
      { orientation: "y", semantic: "large-compact" },
    ],
  },
  {
    id: "composed-secondary",
    input: numericAxisInput("composed-secondary", closeThousandValues, {
      chart: { fields: ["activeUsers", "weeklyGrowth"], barFields: ["weeklyGrowth"] },
      rows: closeThousandValues.map((activeUsers, index) => ({
        week: axisWeeks[index],
        activeUsers,
        weeklyGrowth: closeBillionValues[index],
      })),
    }),
    axes: [
      { orientation: "y", semantic: "small-integer" },
      { orientation: "y", semantic: "large-compact" },
    ],
  },
  {
    id: "box-plot",
    input: numericAxisInput("box-plot", closeThousandValues, {
      type: "boxPlot",
      chart: { x: "plan", showYAxisLabel: false },
      rows: [
        { plan: "Pro", minimum: 960, lowerQuartile: 975, median: 990, upperQuartile: 1005, maximum: 1020 },
        { plan: "Team", minimum: 980, lowerQuartile: 995, median: 1010, upperQuartile: 1025, maximum: 1040 },
      ],
    }),
    axes: [{ orientation: "y", semantic: "numeric" }],
  },
];

let resources;

function requirePass(condition, message) {
  assert.ok(condition, message);
}

async function renderFixture(name, input, options = []) {
  const inputPath = join(workspace, `${name}.json`);
  const outputPath = join(workspace, `${name}.html`);
  await writeFile(inputPath, JSON.stringify(input));
  const args = [inlineRenderer, "--input", inputPath, "--output", outputPath, "--offline", ...options];
  args.push("--cache-dir", cacheRoot);
  const result = spawnSync(process.execPath, args, {
    cwd: pluginRoot,
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
  });
  assert.equal(result.status, 0, `Production inline renderer failed for ${name}:\n${result.stdout}\n${result.stderr}`);
  const metadata = JSON.parse(result.stdout.trim());
  const fragment = await readFile(outputPath, "utf8");
  assert.equal(
    metadata.path,
    await realpath(outputPath),
    "production renderer should report the canonical output path across /var aliases",
  );
  requirePass(metadata.prebuilt, "browser regressions must use the shipped prebuilt inline renderer");
  assert.equal(metadata.cacheHit, false, "A prebuilt inline renderer must not depend on a mutable compiler cache");
  requirePass(metadata.bytes < 1_000_000, "production fragments must remain below the 1 MB delivery limit");
  return { name, metadata, fragment, outputPath: metadata.path, root: `#${metadata.rootId}` };
}

async function buildActualVisualizationHost() {
  const kit = await readFile(join(monorepoRoot, "plugins/visualize/skills/visualize/assets/visualize.html"), "utf8");
  const styles = await readFile(
    join(monorepoRoot, "plugins/visualize/skills/visualize/assets/visualize.css"),
    "utf8",
  );
  const { build } = await import(pathToFileURL(dependencyRequire.resolve("vite")).href);
  const output = join(workspace, "actual-visualization-host");
  await build({
    root: workspace,
    configFile: false,
    cacheDir: join(workspace, ".vite-visualization-host"),
    logLevel: "silent",
    define: {
      __VISUALIZATION_HTML__: JSON.stringify(kit),
      __VISUALIZATION_STYLES__: JSON.stringify(styles),
    },
    build: {
      outDir: output,
      emptyOutDir: false,
      target: "node22",
      minify: false,
      lib: {
        entry: join(appRoot, "webview/src/visualization/visualization-sandbox-config.ts"),
        formats: ["es"],
        fileName: () => "visualization-sandbox-config.mjs",
      },
    },
  });
  const host = await import(pathToFileURL(join(output, "visualization-sandbox-config.mjs")).href);
  return { ...host, kit, styles };
}

function extractRuntime(html, rootId) {
  const root = html.indexOf(`<div id="${rootId}"`);
  requirePass(root >= 0, "actual host HTML must contain the generated production chart root");
  const start = html.indexOf("<script>", root);
  requirePass(start >= 0, "production chart runtime script must survive host insertion");
  const end = html.indexOf("</script>", start);
  requirePass(end > start, "production chart runtime must remain a complete script");
  return html.slice(start + "<script>".length, end).trim();
}

function verifyHostInsertion(fixture, host) {
  const original = extractRuntime(fixture.fragment, fixture.metadata.rootId);
  const oldHost = host.kit.replace(marker, fixture.fragment);
  const actualHost = host.getVisualizationSandboxHtml(fixture.fragment);
  assert.equal(
    extractRuntime(oldHost, fixture.metadata.rootId),
    original,
    "production bundle must remain compatible with older String.replace-based Codex hosts",
  );
  assert.equal(
    extractRuntime(actualHost, fixture.metadata.rootId),
    original,
    "actual getVisualizationSandboxHtml must preserve the inline runtime byte-for-byte",
  );
  assert.doesNotThrow(() => new Script(original));
  assert.doesNotThrow(() => new Script(extractRuntime(oldHost, fixture.metadata.rootId)));
  assert.doesNotThrow(() => new Script(extractRuntime(actualHost, fixture.metadata.rootId)));
}

async function standalonePreview(fixture, host) {
  verifyHostInsertion(fixture, host);
  const destination = join(workspace, `${fixture.name}-actual-host.html`);
  await writeFile(
    destination,
    host.getStandaloneVisualizationHtml(fixture.fragment, {
      locale: "en",
      title: fixture.name,
      styles: `${host.styles}\n:root{--chart-1:#ff00aa;--mark-radius:97}`,
    }),
  );
  return destination;
}

async function createPageScenario(browser, preview, { width = 736, colorScheme = "light", height = 1200, reducedMotion = "reduce" } = {}) {
  const context = await browser.newContext({
    viewport: { width: width + 32, height },
    colorScheme,
    reducedMotion,
  });
  const network = [];
  const errors = [];
  await context.route("**/*", async (route) => {
    const url = route.request().url();
    if (url.startsWith("file:") || url.startsWith("data:") || url === "about:srcdoc") {
      await route.continue();
      return;
    }
    if (resources.has(url)) {
      await route.fulfill({
        path: resources.get(url),
        contentType: "application/javascript; charset=utf-8",
        headers: { "access-control-allow-origin": "*" },
      });
      return;
    }
    if (url === "https://unpkg.com/lucide@1.17.0/dist/umd/lucide.js") {
      await route.fulfill({
        body: "globalThis.lucide={createIcons(){}};",
        contentType: "application/javascript; charset=utf-8",
        headers: { "access-control-allow-origin": "*" },
      });
      return;
    }
    network.push(url);
    await route.abort("blockedbyclient");
  });

  const page = await context.newPage();
  page.on("pageerror", (error) => errors.push(error.stack ?? error.message));
  await page.goto(pathToFileURL(preview).href, { timeout: 30_000, waitUntil: "load" });
  return {
    context,
    errors,
    network,
    page,
    async verifyClean() {
      assert.deepEqual(network, [], "inline production chart must not make unexpected network requests");
      assert.deepEqual(errors, [], "inline production chart must not raise browser exceptions");
    },
  };
}

async function createScenario(browser, fixture, preview, options = {}) {
  const scenario = await createPageScenario(browser, preview, options);
  assert.equal(
    await scenario.page.locator("iframe").getAttribute("sandbox"),
    "allow-scripts",
    "browser regressions must use the real restricted Codex iframe",
  );
  const frame = scenario.page.frameLocator("iframe");
  const root = frame.locator(fixture.root);
  await root.locator(".recharts-wrapper").first().waitFor({ state: "visible", timeout: 20_000 });
  return { ...scenario, frame, root };
}

async function selectedPanel(root, name) {
  const selected = root.locator('.source-tabs [role="tab"][aria-selected="true"]');
  assert.equal(await selected.count(), 1);
  assert.equal((await selected.innerText()).trim(), name);
  const controlled = await selected.getAttribute("aria-controls");
  const id = await selected.getAttribute("id");
  requirePass(controlled && id, "canonical source tabs must identify and label their panels");
  const panel = root.locator(`[role="tabpanel"][id="${controlled}"]`);
  assert.equal(await panel.count(), 1);
  assert.equal(await panel.getAttribute("aria-labelledby"), id);
  requirePass(await panel.isVisible(), "selected canonical source panel must be visible");
  return panel;
}

function generatedPayload(fixture) {
  const expression = new RegExp(
    `<script\\s+type="application/json"\\s+id="${fixture.metadata.rootId}-data">([\\s\\S]*?)<\\/script>`,
    "u",
  );
  const match = fixture.fragment.match(expression);
  requirePass(match, "Generated inline fragment must contain its reviewed JSON payload");
  return JSON.parse(match[1]);
}

function parseNumericAxisLabel(label) {
  const value = label.replaceAll(",", "").replace("−", "-").trim();
  const match = value.match(/^([+-]?(?:\d+(?:\.\d+)?|\.\d+))(?:([KMBT])|(%))?$/iu);
  requirePass(match, `Visible numeric axis tick must remain readable: ${JSON.stringify(label)}`);
  const magnitude = { K: 1e3, M: 1e6, B: 1e9, T: 1e12 };
  return Number(match[1]) * (match[2] ? magnitude[match[2].toUpperCase()] : match[3] ? 0.01 : 1);
}

async function inspectReadableAxes(browser, fixture, preview, descriptor, { width, colorScheme }) {
  const scenario = await createScenario(browser, fixture, preview, { width, colorScheme });
  const { context, errors, root } = scenario;
  try {
    await root.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const observed = await root.evaluate((element) => {
      const shadow = element.shadowRoot;
      const host = element.getBoundingClientRect();
      const box = (bounds) => ({
        left: bounds.left,
        right: bounds.right,
        top: bounds.top,
        bottom: bounds.bottom,
        width: bounds.width,
        height: bounds.height,
      });
      const axes = [...shadow.querySelectorAll(".recharts-yAxis-tick-labels,.recharts-xAxis-tick-labels")]
        .map((axis) => {
          const svg = axis.closest("svg");
          return {
            orientation: axis.classList.contains("recharts-yAxis-tick-labels") ? "y" : "x",
            svg: svg ? box(svg.getBoundingClientRect()) : null,
            ticks: [...axis.querySelectorAll(".recharts-cartesian-axis-tick-value")]
              .map((tick) => {
                const styles = getComputedStyle(tick);
                const bounds = tick.getBoundingClientRect();
                return {
                  label: tick.textContent.replace(/\s+/gu, " ").trim(),
                  bounds: box(bounds),
                  visible:
                    styles.display !== "none" &&
                    styles.visibility !== "hidden" &&
                    bounds.width > 0 &&
                    bounds.height > 0,
                };
              })
              .filter((tick) => tick.visible),
          };
        })
        .filter(
          (axis) =>
            axis.ticks.length > 1 &&
            axis.ticks.every(({ label }) => /^[+\-−]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)\s*(?:[KMBT]|%)?$/iu.test(label)),
        );
      return {
        host: box(host),
        axes,
        rawAxes: [
          ...shadow.querySelectorAll(
            ".recharts-cartesian-axis,.recharts-yAxis,.recharts-xAxis," +
              ".recharts-yAxis-tick-labels,.recharts-xAxis-tick-labels",
          ),
        ].map((axis) => ({
          className: axis.getAttribute("class"),
          ticks: [...axis.querySelectorAll("text")].map((tick) => ({
            text: tick.textContent.replace(/\s+/gu, " ").trim(),
            className: tick.getAttribute("class"),
            bounds: box(tick.getBoundingClientRect()),
            display: getComputedStyle(tick).display,
            visibility: getComputedStyle(tick).visibility,
          })),
        })),
        svgText: [...shadow.querySelectorAll("svg text")].map((tick) => tick.textContent.replace(/\s+/gu, " ").trim()),
        document: { width: document.documentElement.clientWidth, scrollWidth: document.documentElement.scrollWidth },
      };
    });

    assert.equal(
      observed.axes.length,
      descriptor.axes.length,
      `${descriptor.id}: actual shared Recharts chart must expose every expected numeric axis; ` +
        `raw axis groups=${JSON.stringify(observed.rawAxes)}, all SVG text=${JSON.stringify(observed.svgText)}, ` +
        `browser errors=${JSON.stringify(errors)}`,
    );
    requirePass(
      observed.document.scrollWidth <= observed.document.width + 1,
      `${descriptor.id}: readable numeric labels must not overflow the ${width}px Codex document`,
    );

    for (const [index, expected] of descriptor.axes.entries()) {
      const axis = observed.axes[index];
      assert.equal(
        axis.orientation,
        expected.orientation,
        `${descriptor.id}: expected numeric ${expected.orientation}-axis at index ${index}`,
      );
      requirePass(axis.svg, `${descriptor.id}: numeric ${axis.orientation}-axis must belong to the native chart SVG`);
      requirePass(
        axis.ticks.length >= 3,
        `${descriptor.id}: ${width}px ${axis.orientation}-axis must show at least three readable values`,
      );
      const labels = axis.ticks.map(({ label }) => label);
      assert.equal(
        new Set(labels).size,
        labels.length,
        `${descriptor.id}: ${width}px ${axis.orientation}-axis repeats ambiguous labels ${JSON.stringify(labels)}`,
      );
      const values = labels.map(parseNumericAxisLabel);
      const direction = Math.sign(values[1] - values[0]);
      requirePass(
        direction !== 0 &&
          values.slice(1).every((value, position) => Math.sign(value - values[position]) === direction),
        `${descriptor.id}: ${axis.orientation}-axis labels must describe strictly monotone values ${JSON.stringify(
          labels,
        )}`,
      );

      const visual = [...axis.ticks].sort((left, right) =>
        expected.orientation === "x" ? left.bounds.left - right.bounds.left : left.bounds.top - right.bounds.top,
      );
      for (const [position, tick] of visual.entries()) {
        requirePass(
          tick.bounds.left >= axis.svg.left - 1 &&
            tick.bounds.right <= axis.svg.right + 1 &&
            tick.bounds.top >= axis.svg.top - 1 &&
            tick.bounds.bottom <= axis.svg.bottom + 1,
          `${descriptor.id}: ${width}px ${axis.orientation}-axis tick ${JSON.stringify(
            tick.label,
          )} is clipped by its SVG`,
        );
        if (!position) continue;
        const previous = visual[position - 1].bounds;
        requirePass(
          expected.orientation === "x"
            ? previous.right <= tick.bounds.left + 1
            : previous.bottom <= tick.bounds.top + 1,
          `${descriptor.id}: ${width}px ${axis.orientation}-axis labels overlap: ${JSON.stringify(labels)}`,
        );
      }

      if (expected.semantic === "small-integer") {
        requirePass(
          labels.every((label) => !/[KMBT]/iu.test(label)),
          `${descriptor.id}: nearby values below 10,000 should use grouped integers rather than ambiguous compact labels`,
        );
        requirePass(
          labels.some((label) => /1,0\d\d/u.test(label)),
          `${descriptor.id}: thousand-crossing axis should visibly distinguish values such as 1,000 and 1,020`,
        );
      }
      if (expected.semantic === "large-compact") {
        requirePass(
          labels.some((label) => /[MB]$/iu.test(label)),
          `${descriptor.id}: billion-scale numeric ticks should remain compact and readable`,
        );
      }
      if (expected.semantic === "negative") {
        requirePass(
          values.some((value) => value < 0) && values.every((value) => value <= 0),
          `${descriptor.id}: negative axis ticks must retain their actual sign`,
        );
        requirePass(
          labels.every((label, position) => values[position] === 0 || /^[-−]/u.test(label)),
          `${descriptor.id}: negative numeric labels must visibly include a minus sign`,
        );
      }
      if (expected.semantic === "signed-near-zero") {
        requirePass(
          values.some((value) => value < 0) && values.some((value) => value > 0),
          `${descriptor.id}: closely spaced values around zero must remain visible on both sides`,
        );
        requirePass(
          labels.every((label) => !/^[-−]0(?:\.0+)?$/u.test(label)),
          `${descriptor.id}: tiny negative values must not collapse into negative zero`,
        );
      }
      if (expected.semantic === "precise-percentage") {
        requirePass(
          labels.every((label) => label.endsWith("%") && !label.startsWith("+")),
          `${descriptor.id}: percentage axes must preserve percent units without introducing plus signs`,
        );
        requirePass(
          labels.some((label) => /\.\d{2,}%$/u.test(label)),
          `${descriptor.id}: close conversion rates require additional visible percentage precision`,
        );
      }
    }

    await scenario.verifyClean();
    process.stdout.write(
      `${JSON.stringify({
        test: "readable-native-numeric-axes",
        case: descriptor.id,
        width,
        colorScheme,
        axes: observed.axes.map((axis) => ({
          orientation: axis.orientation,
          labels: axis.ticks.map(({ label }) => label),
        })),
        result: "pass",
      })}\n`,
    );
  } finally {
    await context.close();
  }
}

async function inspectIsolatedGap(browser, fixture, preview, { width, colorScheme }) {
  const scenario = await createScenario(browser, fixture, preview, { width, colorScheme });
  const { context, page, root } = scenario;
  try {
    const dots = root.locator('.recharts-line-dot[data-isolated-point="true"]');
    await dots.first().waitFor({ state: "visible", timeout: 10_000 });
    assert.equal(
      await dots.count(),
      2,
      "Single-measure values [120, null, 145] must render one persistent marker per isolated observation",
    );
    assert.equal(
      await root.locator(".recharts-line-dots circle, .recharts-line-dot").count(),
      2,
      "Null observations must not create a third persistent line marker",
    );

    const geometry = await root.evaluate((element) => {
      const shadow = element.shadowRoot;
      const markers = [...shadow.querySelectorAll('.recharts-line-dot[data-isolated-point="true"]')].map((dot) => ({
        radius: Number(dot.getAttribute("r")),
        cx: Number(dot.getAttribute("cx")),
        cy: Number(dot.getAttribute("cy")),
        fill: getComputedStyle(dot).fill,
        width: dot.getBoundingClientRect().width,
        height: dot.getBoundingClientRect().height,
      }));
      const curves = [...shadow.querySelectorAll(".recharts-line-curve")].map((path) => ({
        path: path.getAttribute("d"),
        length: path.getTotalLength(),
      }));
      return { markers, curves };
    });
    assert.deepEqual(
      geometry.markers.map((marker) => marker.radius),
      [3, 3],
      "Isolated dashboard observations must use canonical three-pixel point markers",
    );
    requirePass(
      geometry.markers.every((marker) => marker.width >= 5 && marker.height >= 5 && marker.fill !== "none"),
      "Isolated observations must be genuinely visible rather than zero-length invisible SVG marks",
    );
    requirePass(
      geometry.markers[0].cx < geometry.markers[1].cx,
      "The two genuine observations must retain their reviewed chronological order",
    );
    requirePass(
      geometry.curves.every((curve) => curve.length < 0.5),
      "Missing observations must not be interpolated or bridged by a positive-length line",
    );

    const firstBox = await dots.first().boundingBox();
    requirePass(firstBox, "The first isolated observation must provide a real pointer target");
    await page.mouse.move(firstBox.x + firstBox.width / 2, firstBox.y + firstBox.height / 2);
    const tooltip = root.locator(".chart-tooltip");
    await tooltip.waitFor({ state: "visible", timeout: 5_000 });
    const firstTooltip = await tooltip.innerText();
    assert.match(firstTooltip, /120/u);
    assert.match(firstTooltip, /WAU|Weekly active users/iu);
    assert.doesNotMatch(
      firstTooltip,
      /Before Gap|After Gap|Segment|Part\s*\d/u,
      "Canonical isolated-point handling must not invent artificial tooltip series labels",
    );

    const lastBox = await dots.last().boundingBox();
    requirePass(lastBox, "The second isolated observation must provide a real pointer target");
    await page.mouse.move(lastBox.x + lastBox.width / 2, lastBox.y + lastBox.height / 2);
    await tooltip.waitFor({ state: "visible", timeout: 5_000 });
    assert.match(await tooltip.innerText(), /145/u);

    await page.mouse.move(
      (firstBox.x + firstBox.width / 2 + lastBox.x + lastBox.width / 2) / 2,
      (firstBox.y + firstBox.height / 2 + lastBox.y + lastBox.height / 2) / 2,
    );
    assert.equal(
      await root.locator(".recharts-active-dot").count(),
      0,
      "The missing reviewed week must not produce an active marker or synthetic zero value",
    );

    const trigger = root.getByRole("button", { name: "View data source" });
    await trigger.click();
    const tabs = root.locator(".source-tabs");
    await tabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.deepEqual(await tabs.getByRole("tab").allInnerTexts(), ["Overview", "Data preview"],
      "Supplied observations without recorded SQL or evidence flow expose only their available source tabs");
    const overview = await selectedPanel(root, "Overview");
    const caveats = await overview.locator(".source-caveats li").allInnerTexts();
    assert.deepEqual(
      caveats,
      isolatedGapInput.source.caveats,
      "Actual dashboard source inspection must preserve supplied missing-value/sample caveats verbatim",
    );

    await tabs.getByRole("tab", { name: "Data preview" }).click();
    const previewPanel = await selectedPanel(root, "Data preview");
    assert.deepEqual(
      await previewPanel.locator("thead th").allInnerTexts(),
      ["Week", "WAU"],
      "Canonical missing-value handling must not add synthetic before/after-gap source columns",
    );
    const reviewedRows = await previewPanel
      .locator("tbody tr")
      .evaluateAll((rows) => rows.map((row) => [...row.querySelectorAll("td")].map((cell) => cell.innerText.trim())));
    assert.equal(reviewedRows.length, 3);
    assert.match(reviewedRows[0][0], /Jul\s+27/u);
    assert.equal(reviewedRows[0][1], "120");
    assert.match(reviewedRows[1][0], /Aug\s+3/u);
    assert.equal(reviewedRows[1][1], "—", "A missing reviewed value must remain missing rather than becoming zero");
    assert.match(reviewedRows[2][0], /Aug\s+10/u);
    assert.equal(reviewedRows[2][1], "145");

    await scenario.verifyClean();
    process.stdout.write(
      `${JSON.stringify({
        test: "canonical-isolated-missing-week",
        values: [120, null, 145],
        width,
        colorScheme,
        persistentDots: geometry.markers.length,
        pointRadius: 3,
        artificialFields: 0,
        result: "pass",
      })}\n`,
    );
  } finally {
    await context.close();
  }
}

async function inspectLineScenario(browser, fixture, preview, { width, colorScheme }) {
  const scenario = await createScenario(browser, fixture, preview, { width, colorScheme });
  const { context, errors, network, page, root } = scenario;

  try {
    const state = await root.evaluate((element) => {
      const shadow = element.shadowRoot;
      const curves = [...shadow.querySelectorAll(".recharts-line-curve")];
      return {
        shadow: Boolean(shadow),
        rootWidth: element.getBoundingClientRect().width,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        hostTheme: element.getAttribute("data-app-theme"),
        hostRadius: getComputedStyle(element).getPropertyValue("--mark-radius").trim(),
        outerTheme: document.documentElement.getAttribute("data-app-theme"),
        outerRadius: getComputedStyle(document.documentElement).getPropertyValue("--mark-radius").trim(),
        outerChartToken: getComputedStyle(document.documentElement).getPropertyValue("--chart-1").trim(),
        outerApplicationStyles: [...document.querySelectorAll("style")].some((style) =>
          style.textContent.includes(".chart-ranked-list"),
        ),
        innerApplicationStyles: [...shadow.querySelectorAll("style")].some((style) =>
          style.textContent.includes(".chart-ranked-list"),
        ),
        persistentDots: shadow.querySelectorAll(".recharts-line-dots circle, .recharts-line-dot").length,
        areas: shadow.querySelectorAll(".recharts-area-area").length,
        curves: curves.map((curve) => ({
          d: curve.getAttribute("d"),
          stroke: getComputedStyle(curve).stroke,
          width: curve.getAttribute("stroke-width"),
          cap: curve.getAttribute("stroke-linecap"),
          join: curve.getAttribute("stroke-linejoin"),
          length: curve.getTotalLength(),
        })),
      };
    });
    assert.equal(state.shadow, true, "shared dashboard components must remain inside Shadow DOM");
    assert.equal(state.curves.length, 2, "the real dashboard renderer should render both reviewed series");
    for (const curve of state.curves) {
      assert.match(curve.d, /C/u, "native dashboard trend lines should use smooth monotone interpolation");
      assert.equal(curve.width, "2.25", "native dashboard trend lines should retain 2.25px strokes");
      assert.equal(curve.cap, "round");
      assert.equal(curve.join, "round");
      requirePass(curve.length > 0, "native dashboard trend lines should have visible geometry");
    }
    assert.deepEqual(
      state.curves.map(({ stroke }) => stroke),
      colorScheme === "dark" ? ["rgb(102, 181, 255)", "rgb(173, 123, 249)"] : ["rgb(2, 133, 255)", "rgb(146, 79, 247)"],
      "dashboard theme colors must adapt to the actual Codex color scheme",
    );
    assert.equal(state.persistentDots, 0, "normal multi-point lines must not display permanent markers");
    assert.equal(state.areas, 0, "Line charts must not render area fills, even with a legacy showArea setting");
    requirePass(Math.abs(state.rootWidth - width) <= 1, `chart root should fill the ${width}px host`);
    requirePass(state.scrollWidth <= state.clientWidth + 1, "chart must not create host-document horizontal overflow");
    assert.equal(state.hostTheme, "codex-classic");
    assert.equal(state.hostRadius, "8");
    assert.equal(state.outerTheme, null, "embedding must never apply a dashboard theme to the host document");
    assert.equal(state.outerRadius, "97", "host-document sentinel tokens must remain untouched");
    assert.equal(state.outerChartToken, "#ff00aa", "dashboard color tokens must not leak into the host document");
    assert.equal(state.outerApplicationStyles, false, "canonical dashboard CSS must not leak outside Shadow DOM");
    assert.equal(state.innerApplicationStyles, true, "inline rendering must use the actual shared dashboard CSS");

    const graph = root.locator(".recharts-wrapper");
    const graphBox = await graph.boundingBox();
    requirePass(graphBox, "native Recharts wrapper must have a visible pointer target");
    await page.mouse.move(graphBox.x + graphBox.width * 0.58, graphBox.y + graphBox.height * 0.4);
    const tooltip = root.locator(".chart-tooltip");
    await tooltip.waitFor({ state: "visible", timeout: 5_000 });
    assert.match(await tooltip.innerText(), /Pro/u);
    assert.match(await tooltip.innerText(), /Team/u);
    const tooltipStyles = await tooltip.evaluate((element) => ({
      radius: getComputedStyle(element).borderRadius,
      shadow: getComputedStyle(element).boxShadow,
    }));
    assert.equal(tooltipStyles.radius, "12px");
    assert.match(
      tooltipStyles.shadow,
      /4px\s+14px/u,
      "theme-qualified Classic tooltip overrides must survive :root-to-:host scoping",
    );
    requirePass(
      (await root.locator(".recharts-active-dot").count()) > 0,
      "native dashboard hover markers must appear only while hovering",
    );
    await page.mouse.move(1, 1);

    const team = root.getByRole("button", { name: "Toggle Team" });
    await team.click();
    assert.equal(await team.getAttribute("aria-pressed"), "false");
    assert.equal(
      await root.locator(".recharts-line-curve").count(),
      1,
      "real shared dashboard legends must toggle native series",
    );
    await team.click();
    assert.equal(await root.locator(".recharts-line-curve").count(), 2);

    const sourceTrigger = root.getByRole("button", { name: "View data source" });
    assert.equal(await sourceTrigger.getAttribute("aria-expanded"), "false");
    assert.equal(await root.locator(".source-sidebar-layer").count(), 0);
    assert.equal(
      await root.getByRole("button", { name: /^Copy(?: data| as image)?$/iu }).count(),
      0,
      "inline charts must not expose unsupported copy actions",
    );

    await sourceTrigger.click();
    const layer = root.locator(".source-sidebar-layer.source-sidebar-layer--contained");
    const sidebar = layer.locator(":scope > aside.source-sidebar");
    const backdrop = layer.locator(":scope > button.source-sidebar-backdrop");
    const header = sidebar.locator(":scope > header.source-sidebar-header");
    const body = sidebar.locator(":scope > .source-sidebar-body");
    const tabs = body.locator(".source-inspector .source-tabs");
    await tabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.equal(await sourceTrigger.getAttribute("aria-expanded"), "true");
    assert.equal(await layer.count(), 1);
    assert.equal(await backdrop.count(), 1);
    assert.equal(await sidebar.getAttribute("aria-label"), `Data source for ${reviewedInput.title}`);
    assert.equal(await header.locator("h2").innerText(), reviewedInput.title);
    assert.equal(await header.getByRole("button", { name: "Close data source" }).count(), 1);
    assert.deepEqual(
      await tabs.getByRole("tab").allInnerTexts(),
      ["Overview", "Data preview", "Evidence flow"],
      "Default inline charts must omit the SQL tab when SQL was not authorized for inclusion",
    );

    const bounds = await root.evaluate((element) => {
      const shadow = element.shadowRoot;
      const rect = (target) => {
        const value = target.getBoundingClientRect();
        return { top: value.top, bottom: value.bottom, left: value.left, right: value.right, width: value.width };
      };
      return {
        host: rect(element),
        heading: rect(shadow.querySelector(".component-header")),
        plot: rect(shadow.querySelector(".recharts-wrapper")),
        sidebar: rect(shadow.querySelector(".source-sidebar")),
        layerPosition: getComputedStyle(shadow.querySelector(".source-sidebar-layer")).position,
        sidebarPosition: getComputedStyle(shadow.querySelector(".source-sidebar")).position,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
      };
    });
    requirePass(
      bounds.sidebar.top <= bounds.heading.top + 4,
      `sidebar starts below the chart rather than overlaying it: ${JSON.stringify(bounds)}`,
    );
    requirePass(
      bounds.sidebar.bottom > bounds.plot.top + 32,
      "source sidebar must overlap the actual chart instead of expanding beneath it",
    );
    requirePass(
      Math.abs(bounds.sidebar.right - bounds.host.right) <= 2,
      "source sidebar must remain anchored to the chart's right edge",
    );
    requirePass(bounds.sidebar.left >= bounds.host.left - 1, "source sidebar must never escape its isolated host");
    requirePass(
      bounds.scrollWidth <= bounds.clientWidth + 1,
      "expanded source sidebar must not create host-document horizontal overflow",
    );
    assert.notEqual(bounds.layerPosition, "fixed");
    assert.notEqual(bounds.sidebarPosition, "fixed");
    if (width === 736) {
      requirePass(
        bounds.sidebar.left >= bounds.host.left + 100,
        "desktop source sidebar should preserve the chart behind its left-side backdrop",
      );
      requirePass(
        bounds.sidebar.width >= 480 && bounds.sidebar.width <= 522,
        "desktop source sidebar should match the shared dashboard's 520px width",
      );
    } else {
      requirePass(
        Math.abs(bounds.sidebar.left - bounds.host.left) <= 2,
        "narrow source sidebars should cover the full chart width",
      );
      requirePass(
        Math.abs(bounds.sidebar.width - bounds.host.width) <= 2,
        "narrow source sidebars should cover the full chart width",
      );
    }

    const overview = await selectedPanel(root, "Overview");
    const overviewText = await overview.innerText();
    assert.match(overviewText, /Reporting period/u);
    assert.match(overviewText, /Source captured/u);
    assert.match(overviewText, /Weekly active users/u);
    assert.match(overviewText, /Unique accounts active during the reviewed week/u);
    assert.match(overviewText, /Reporting week/u);
    assert.match(overviewText, /UTC reporting week when the reviewed account activity occurred/u);
    assert.match(overviewText, /Plan attribution/u);
    assert.match(overviewText, /Reviewed subscription plan attributed to the active account/u);
    assert.match(overviewText, /analytics\.approved_weekly_users/u);
    assert.match(overviewText, /Approved sample snapshot\.csv/u);
    assert.doesNotMatch(overviewText, /restricted\.raw_metric_input/u);
    assert.doesNotMatch(overviewText, /NEVER_EMBED_UNREVIEWED_PRIVATE_DEFINITION/u);
    assert.deepEqual(
      await overview
        .locator(".source-definitions tbody tr")
        .evaluateAll((rows) =>
          rows.map((row) => [...row.querySelectorAll("th,td")].map((cell) => cell.innerText.trim())),
        ),
      [
        ["Weekly active users", "Unique accounts active during the reviewed week."],
        ["Reporting week", "UTC reporting week when the reviewed account activity occurred."],
        ["Plan attribution", "Reviewed subscription plan attributed to the active account."],
      ],
      "canonical Overview must preserve displayed dimensions while excluding unrelated private definitions",
    );
    assert.equal(
      await overview
        .locator(".source-metadata dt")
        .first()
        .evaluate((element) => getComputedStyle(element).fontWeight),
      "500",
      "theme-qualified Classic source-label typography must survive :root-to-:host scoping",
    );

    await tabs.getByRole("tab", { name: "Data preview" }).click();
    const previewPanel = await selectedPanel(root, "Data preview");
    assert.equal(
      await previewPanel.locator("tbody tr").count(),
      8,
      "native dashboard DataTable must paginate reviewed observations",
    );
    assert.match(await previewPanel.innerText(), /12 results/u);
    assert.doesNotMatch(await previewPanel.innerText(), /NEVER_EMBED_UNREVIEWED_PRIVATE_COLUMN/u);

    assert.equal(await tabs.getByRole("tab", { name: "SQL query" }).count(), 0);
    assert.doesNotMatch(
      await body.innerText(),
      /restricted\.raw_metric_input/u,
      "SQL must remain omitted without explicit include-sql authorization",
    );
    assert.equal(await body.locator(".sql-copy-button").count(), 0);

    await tabs.getByRole("tab", { name: "Evidence flow" }).click();
    const evidence = await selectedPanel(root, "Evidence flow");
    assert.match(await evidence.innerText(), /Approved reviewed snapshot/u);
    assert.match(await evidence.innerText(), /Replacement metacharacters/u);
    assert.doesNotMatch(
      await evidence.innerText(),
      /restricted\.raw_metric_input/u,
      "unauthorized SQL must also be absent from evidence flow",
    );

    const evidenceTab = tabs.getByRole("tab", { name: "Evidence flow" });
    await evidenceTab.focus();
    await page.keyboard.press("Home");
    await selectedPanel(root, "Overview");
    await page.keyboard.press("End");
    await selectedPanel(root, "Evidence flow");
    await page.keyboard.press("ArrowLeft");
    await selectedPanel(root, "Data preview");
    await page.keyboard.press("ArrowRight");
    await selectedPanel(root, "Evidence flow");
    await page.keyboard.press("Escape");
    await layer.waitFor({ state: "detached", timeout: 5_000 });
    assert.equal(await sourceTrigger.getAttribute("aria-expanded"), "false");
    requirePass(
      await sourceTrigger.evaluate((element) => element.getRootNode().activeElement === element),
      "contained sidebar dismissal should restore focus within its Shadow DOM",
    );

    await sourceTrigger.click();
    await root.locator(".source-tabs").waitFor({ state: "visible", timeout: 10_000 });
    await root.locator(".source-sidebar-header").getByRole("button", { name: "Close data source" }).click();
    await layer.waitFor({ state: "detached", timeout: 5_000 });

    await sourceTrigger.click();
    await root.locator(".source-tabs").waitFor({ state: "visible", timeout: 10_000 });
    if (width === 736) await root.locator(".source-sidebar-backdrop").click({ position: { x: 8, y: 8 } });
    else await root.locator(".source-sidebar-backdrop").evaluate((element) => element.click());
    await layer.waitFor({ state: "detached", timeout: 5_000 });

    await scenario.verifyClean();
    process.stdout.write(
      `${JSON.stringify({
        test: "shared-inline-dashboard",
        width,
        colorScheme,
        series: state.curves.length,
        sidebarWidth: Math.round(bounds.sidebar.width),
        reviewedRows: reviewedInput.rows.length,
        result: "pass",
      })}\n`,
    );
  } catch (error) {
    process.stderr.write(`${JSON.stringify({ width, colorScheme, errors, network })}\n`);
    throw error;
  } finally {
    await context.close();
  }
}

async function inspectSqlOptIn(browser, fixture, preview) {
  const scenario = await createScenario(browser, fixture, preview);
  const { context, root } = scenario;
  try {
    await root.getByRole("button", { name: "View data source" }).click();
    const tabs = root.locator(".source-tabs");
    await tabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.deepEqual(await tabs.getByRole("tab").allInnerTexts(), tabLabels,
      "Explicitly authorized SQL and recorded evidence expose all four source tabs");
    const overview = await selectedPanel(root, "Overview");
    assert.match(await overview.innerText(), /Query executed/u);
    await tabs.getByRole("tab", { name: "SQL query" }).click();
    const panel = await selectedPanel(root, "SQL query");
    const text = await panel.innerText();
    assert.match(text, /SELECT/u);
    assert.match(
      text,
      /restricted\.raw_metric_input/u,
      "explicit --include-sql should render the reviewed query through the real shared inspector",
    );
    assert.equal(
      await panel.locator(".sql-copy-button").count(),
      0,
      "inline source inspectors must not expose unavailable copy actions even when SQL is authorized",
    );
    assert.equal(await root.getByRole("button", { name: /^Copy(?: data| as image)?$/iu }).count(), 0);
    assert.ok(
      (await panel.locator("a").first().getAttribute("href"))?.startsWith(privateSourceUrl),
      "explicit --include-source-urls should preserve the reviewed source link",
    );
    await scenario.verifyClean();
    process.stdout.write(`${JSON.stringify({ test: "explicit-sql-and-source-urls", result: "pass" })}\n`);
  } finally {
    await context.close();
  }
}

async function inspectThemeRadius(browser, fixture, preview, { theme, radius, stroke, scheme }) {
  const scenario = await createScenario(browser, fixture, preview, { width: 360, colorScheme: "light" });
  const { context, root } = scenario;
  try {
    const cell = root.locator(".chart-heatmap-cell").first();
    await cell.waitFor({ state: "visible", timeout: 10_000 });
    const actual = await root.evaluate((element) => ({
      theme: element.getAttribute("data-app-theme"),
      radius: getComputedStyle(element).getPropertyValue("--mark-radius").trim(),
      scheme: getComputedStyle(element).colorScheme,
      mark: element.shadowRoot.querySelector(".chart-heatmap-cell")?.getAttribute("rx"),
      chartToken: getComputedStyle(element).getPropertyValue("--chart-1").trim(),
      outerRadius: getComputedStyle(document.documentElement).getPropertyValue("--mark-radius").trim(),
      outerTheme: document.documentElement.getAttribute("data-app-theme"),
    }));
    assert.equal(actual.theme, theme);
    assert.equal(actual.radius, String(radius));
    assert.equal(
      actual.mark,
      String(radius),
      "actual shared ChartRenderer must read mark geometry from its embedded theme root",
    );
    assert.equal(actual.chartToken, stroke);
    assert.equal(actual.outerRadius, "97", "non-default inline themes must not mutate global dashboard tokens");
    assert.equal(actual.outerTheme, null);
    if (scheme)
      assert.equal(actual.scheme, scheme, "fixed-scheme Data themes must remain dark even in a light Codex document");
    await scenario.verifyClean();
    process.stdout.write(`${JSON.stringify({ test: "embedded-dashboard-theme", theme, radius, result: "pass" })}\n`);
  } finally {
    await context.close();
  }
}

async function multiReferencePreview(fixtures, previews, width) {
  const frames = await Promise.all(
    fixtures.map(async (fixture, index) => {
      const standalone = await readFile(previews.get(fixture.name), "utf8");
      const embedded = standalone.match(/<iframe\b[^>]*\bdata-srcdoc="([^"]+)"/u);
      requirePass(
        embedded,
        "Each visualization reference must retain the exact real Codex-generated restricted sandbox document",
      );
      return (
        `<iframe id="codex-inline-reference-${index}" sandbox="allow-scripts" scrolling="no" ` +
        `referrerpolicy="no-referrer" title="${fixture.name}" srcdoc="${embedded[1]}"></iframe>`
      );
    }),
  );
  const path = join(workspace, `separate-codex-inline-references-${width}.html`);
  await writeFile(
    path,
    `<!doctype html><html lang="en"><head><meta charset="utf-8">` +
      `<style>:root{color-scheme:light dark}html,body{margin:0}body{box-sizing:border-box;padding:16px}` +
      `iframe{display:block;width:100%;max-width:${width}px;height:650px;margin:0 auto 16px;border:0}</style>` +
      `</head><body>${frames.join("")}</body></html>`,
  );
  return path;
}

async function inspectSeparateReferenceIsolation(browser, line, isolated, previews, { width, colorScheme }) {
  const preview = await multiReferencePreview([line, isolated], previews, width);
  const scenario = await createPageScenario(browser, preview, { width, colorScheme, height: 1500 });
  const { context, page } = scenario;
  try {
    const frames = page.locator("iframe");
    assert.equal(
      await frames.count(),
      2,
      "Multiple visualization references must create separate actual restricted host iframes",
    );
    assert.deepEqual(
      await frames.evaluateAll((elements) => elements.map((element) => element.getAttribute("sandbox"))),
      ["allow-scripts", "allow-scripts"],
      "Every separate visualization must preserve its restricted sandbox",
    );

    const firstFrame = page.frameLocator("iframe").nth(0);
    const secondFrame = page.frameLocator("iframe").nth(1);
    const first = firstFrame.locator(line.root);
    const second = secondFrame.locator(isolated.root);
    await first.locator(".recharts-line-curve").first().waitFor({ state: "visible", timeout: 20_000 });
    await second
      .locator('.recharts-line-dot[data-isolated-point="true"]')
      .first()
      .waitFor({ state: "visible", timeout: 20_000 });
    assert.equal(await first.locator(".data-inline-react-root").count(), 1);
    assert.equal(await second.locator(".data-inline-react-root").count(), 1);
    assert.equal(await first.locator(".recharts-line-curve").count(), 2);
    assert.equal(await second.locator('.recharts-line-dot[data-isolated-point="true"]').count(), 2);

    const team = first.getByRole("button", { name: "Toggle Team" });
    await team.click();
    assert.equal(await team.getAttribute("aria-pressed"), "false");
    assert.equal(await first.locator(".recharts-line-curve").count(), 1);
    assert.equal(
      await second.locator('.recharts-line-dot[data-isolated-point="true"]').count(),
      2,
      "Toggling one chart's legend must not mutate an independent chart's native marks",
    );
    await team.click();
    assert.equal(await first.locator(".recharts-line-curve").count(), 2);

    const firstTrigger = first.getByRole("button", { name: "View data source" });
    const secondTrigger = second.getByRole("button", { name: "View data source" });
    await firstTrigger.click();
    const firstTabs = first.locator(".source-tabs");
    await firstTabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.equal(await secondTrigger.getAttribute("aria-expanded"), "false");
    assert.equal(
      await second.locator(".source-sidebar-layer").count(),
      0,
      "One reference's source sidebar must not appear inside another isolated visualization",
    );
    await firstTabs.getByRole("tab", { name: "Evidence flow" }).click();
    await selectedPanel(first, "Evidence flow");
    assert.equal(await first.locator(".source-sidebar-header h2").innerText(), reviewedInput.title);

    await secondTrigger.click();
    const secondTabs = second.locator(".source-tabs");
    await secondTabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.equal(await firstTrigger.getAttribute("aria-expanded"), "true");
    await selectedPanel(first, "Evidence flow");
    assert.equal(await second.locator(".source-sidebar-header h2").innerText(), isolatedGapInput.title);
    await secondTabs.getByRole("tab", { name: "Data preview" }).click();
    const secondPreview = await selectedPanel(second, "Data preview");
    assert.deepEqual(await secondPreview.locator("thead th").allInnerTexts(), ["Week", "WAU"]);
    await selectedPanel(first, "Evidence flow");

    await secondTabs.getByRole("tab", { name: "Data preview" }).focus();
    await page.keyboard.press("Escape");
    await second.locator(".source-sidebar-layer").waitFor({ state: "detached", timeout: 5_000 });
    assert.equal(await secondTrigger.getAttribute("aria-expanded"), "false");
    assert.equal(await firstTrigger.getAttribute("aria-expanded"), "true");
    await selectedPanel(first, "Evidence flow");
    assert.equal(
      await first.locator(".source-sidebar-layer--contained").count(),
      1,
      "Escape in one restricted frame must not close another reference's independently focused source sidebar",
    );

    await first.locator(".source-sidebar-header").getByRole("button", { name: "Close data source" }).click();
    await first.locator(".source-sidebar-layer").waitFor({ state: "detached", timeout: 5_000 });
    await scenario.verifyClean();
    process.stdout.write(
      `${JSON.stringify({
        test: "separate-actual-codex-reference-isolation",
        frames: 2,
        width,
        colorScheme,
        first: reviewedInput.title,
        second: isolatedGapInput.title,
        result: "pass",
      })}\n`,
    );
  } finally {
    await context.close();
  }
}

async function inspectCapacityScenario(browser, fixture, preview, rowCount) {
  const scenario = await createScenario(browser, fixture, preview, {
    width: rowCount === 200 ? 360 : 736,
    colorScheme: "light",
  });
  const { context, root } = scenario;
  try {
    assert.equal(await root.locator(".recharts-line-curve").count(), 2);
    await root.getByRole("button", { name: "View data source" }).click();
    const tabs = root.locator(".source-tabs");
    await tabs.waitFor({ state: "visible", timeout: 10_000 });
    assert.deepEqual(await tabs.getByRole("tab").allInnerTexts(), ["Overview", "Data preview"],
      "File-backed capacity fixtures must not expose unrecorded SQL or evidence flow");
    await tabs.getByRole("tab", { name: "Data preview" }).click();
    const panel = await selectedPanel(root, "Data preview");
    assert.match(await panel.innerText(), new RegExp(`${rowCount} results`, "u"));
    assert.equal(await panel.locator("tbody tr").count(), 8);
    await panel.getByRole("button", { name: "Next page" }).click();
    assert.match(await panel.innerText(), /Page 2 of/u);
    const icons = await root.locator("[data-dashboard-icon]").evaluateAll((elements) => elements.map((element) => ({
      name: element.dataset.dashboardIcon,
      mask: getComputedStyle(element).getPropertyValue("--dashboard-icon-mask"),
    })));
    requirePass(icons.length > 0, "Hydrated chart and source controls must retain their shared icons");
    for (const icon of icons) {
      assert.ok(INLINE_ICON_NAMES.includes(icon.name), `Unexpected inline icon: ${icon.name}`);
      assert.match(icon.mask, /data:image\/svg\+xml/u, `${icon.name} must retain its bundled SVG`);
    }
    await root.getByRole("complementary").getByRole("button", { name: "Close data source" }).click();
    await scenario.verifyClean();
    process.stdout.write(`${JSON.stringify({ test: "complete-fragment-capacity", rowCount,
      bytes: Buffer.byteLength(fixture.fragment), result: "pass" })}\n`);
  } finally {
    await context.close();
  }
}

async function receiptFixture(name, { multiple = false } = {}) {
  const input = JSON.parse(await readFile(join(pluginRoot, "skills/visualize-data/assets/inline-sources-example.json"), "utf8"));
  input.items[0].queries[0].sourceRoles = [{ kind: "file", label: "sample-activation.csv",
    role: "Supplies the eligible and activated counts used in this calculation." }];
  input.items[0].queries[0].source.filters.push("Eligibility: Active accounts in the same seven-day window, including all supported product experiences without summing overlapping source groups.");
  if (multiple) {
    input.items[0].queries.push({ id: "python-export", source: { label: "CSV calculation", files: [{ label: "sample.csv" }], sql: "SELECT period, value FROM sample_csv;" },
      methods: [{ language: "python", code: "rate = activated / eligible\nchange = rate[-1] - rate[0]" }],
      columns: ["period", "value"], rows: Array.from({ length: 117 }, (_, index) => ({ period: `Week ${index + 1}`, value: index })),
      preview: { kind: "partial", note: "First 117 recorded rows.", totalRows: 130 } });
    input.items.push({ id: "release-context", title: "What changed in the release?", queries: [{ id: "release-note",
      summary: "The note records a setup change, not its effect on activation.",
      source: { label: "Synthetic release note", links: [{ label: "Release note", href: "https://example.com/releases" }] } }] });
  }
  const metadata = await renderInlineSources({ input, output: join(workspace, `${name}.html`) });
  return { name, metadata, fragment: await readFile(metadata.path, "utf8"), root: `#${metadata.rootId}` };
}

async function inspectSourcesReceipt(browser, fixture, preview, { multiple, ...options }) {
  const scenario = await createPageScenario(browser, preview, options);
  try {
    const { page } = scenario;
    assert.equal(await page.locator("iframe").getAttribute("sandbox"), "allow-scripts");
    const root = page.frameLocator("iframe").locator(fixture.root);
    const toggle = root.getByRole("button", { name: multiple ? "Sources • 2" : "Sources", exact: true });
    await toggle.waitFor({ state: "visible" });
    assert.equal(await toggle.getAttribute("aria-expanded"), "false");
    // Sample actual layout frames, not just declared transition CSS. The original
    // smoke suite forced reduced motion, which concealed a snapping disclosure.
    await root.evaluate((el) => {
      const expander = el.shadowRoot.querySelector(".receipt-expander");
      el.receiptMotion = new Promise((resolve) => {
        const heights = [];
        const observer = new MutationObserver(() => {
          observer.disconnect();
          const start = performance.now();
          const sample = () => {
            heights.push(expander.getBoundingClientRect().height);
            if (performance.now() - start < 350) requestAnimationFrame(sample);
            else resolve(heights);
          };
          requestAnimationFrame(sample);
        });
        observer.observe(expander, { attributes: true, attributeFilter: ["data-open"] });
      });
    });
    await toggle.click();
    const focusStyle = (element) => element.evaluate((el) => ({
      focused: el.matches(":focus"),
      outline: getComputedStyle(el).outlineStyle,
      cardOutline: getComputedStyle(el, "::after").outlineStyle,
    }));
    assert.equal((await focusStyle(toggle)).outline, "none", "Clicking Sources must not show a keyboard focus ring");
    const heights = await root.evaluate((el) => el.receiptMotion);
    const finalHeight = heights.at(-1);
    if (options.reducedMotion !== "reduce") {
      assert.ok(heights.some((height) => height > 1 && height < finalHeight - 1), "Disclosure must interpolate its layout height");
    } else {
      assert.ok(heights.every((height) => height < 1 || Math.abs(height - finalHeight) <= 1),
        `Reduced motion must settle without intermediate layouts: ${JSON.stringify(heights)}`);
    }
    // Model entering the sandboxed receipt after Tab began in its parent: the
    // receipt sees the new focus and keyup, but not the parent's keydown.
    await toggle.focus();
    await toggle.evaluate((el) => el.dispatchEvent(new KeyboardEvent("keyup", { key: "Tab", bubbles: true, composed: true })));
    assert.equal((await focusStyle(toggle)).outline, "solid", "Tab entry from the host restores keyboard focus styling");
    const card = root.getByRole("article", { name: "How did activation change?", exact: true });
    if (multiple) {
      assert.equal(await card.getAttribute("data-open"), "false");
      const sampleChevron = async () => card.evaluate((el) => {
        const chevron = el.querySelector('.receipt-card-toggle [data-dashboard-icon="chevronDown"]');
        el.originalReceiptChevron ??= chevron;
        el.receiptChevronMotion = new Promise((resolve) => {
          const angles = [];
          const observer = new MutationObserver(() => {
            observer.disconnect();
            const start = performance.now();
            const sample = () => {
              const transform = getComputedStyle(chevron).transform;
              const matrix = new DOMMatrixReadOnly(transform === "none" ? undefined : transform);
              angles.push(Math.abs(Math.atan2(matrix.b, matrix.a) * 180 / Math.PI));
              if (performance.now() - start < 250) requestAnimationFrame(sample);
              else resolve(angles);
            };
            requestAnimationFrame(sample);
          });
          observer.observe(el, { attributes: true, attributeFilter: ["data-open"] });
        });
      });
      const verifyChevron = async (expanded) => {
        const result = await card.evaluate(async (el) => ({ angles: await el.receiptChevronMotion,
          sameNode: el.originalReceiptChevron === el.querySelector('.receipt-card-toggle [data-dashboard-icon="chevronDown"]') }));
        assert.equal(result.sameNode, true, "Expand/collapse must rotate the existing chevron rather than replace it");
        assert.ok(Math.abs(result.angles.at(-1) - (expanded ? 180 : 0)) < 1);
        if (options.reducedMotion !== "reduce") {
          assert.ok(result.angles.some((angle) => angle > 1 && angle < 179), "The chevron must interpolate its rotation");
        } else assert.ok(result.angles.every((angle) => angle < 1 || angle > 179));
      };
      for (const edge of ["left", "right", "top", "bottom"]) {
        const bounds = await card.boundingBox();
        const position = { x: edge === "left" ? 2 : edge === "right" ? bounds.width - 2 : bounds.width / 2,
          y: edge === "top" ? 2 : edge === "bottom" ? bounds.height - 2 : bounds.height / 2 };
        await sampleChevron();
        await card.click({ position });
        assert.equal(await card.getAttribute("data-open"), "true", `Clicking the ${edge} card padding must expand it`);
        await verifyChevron(true);
        await sampleChevron();
        await card.getByRole("button", { name: "Collapse How did activation change?", exact: true }).click();
        assert.equal(await card.getAttribute("data-open"), "false");
        await verifyChevron(false);
        const collapsedFocus = await focusStyle(card.getByRole("button", { name: "How did activation change?", exact: true }));
        assert.equal(collapsedFocus.outline, "none");
        assert.equal(collapsedFocus.cardOutline, "none", "Pointer collapse must not leave the full-card keyboard ring");
      }
      await card.getByRole("button", { name: "How did activation change?", exact: true }).press("Enter");
      assert.equal(await card.getAttribute("data-open"), "true");
      await card.getByRole("button", { name: "Collapse How did activation change?", exact: true }).press("Tab");
      assert.equal(await card.evaluate((el) => el.getRootNode().activeElement?.getAttribute("role")), "tab",
        "Tab from the expanded toggle must enter this card's content, not skip to the next card");
      await card.getByRole("tab", { name: "Overview", exact: true }).press("Shift+Tab");
      await card.getByRole("button", { name: "Collapse How did activation change?", exact: true }).press("Escape");
      assert.equal(await card.getAttribute("data-open"), "false");
      assert.equal(await toggle.getAttribute("aria-expanded"), "true", "Escape from the persistent toggle closes its card first");
      assert.equal((await focusStyle(card.getByRole("button", { name: "How did activation change?", exact: true }))).cardOutline,
        "solid", "Keyboard Escape restores visible focus to the collapsed card");
      await card.getByRole("button", { name: "How did activation change?", exact: true }).click();
    } else assert.equal(await card.getByRole("button", { name: /Collapse/ }).count(), 0);
    await card.evaluate(async (el) => {
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      await Promise.all(el.getAnimations({ subtree: true }).map((animation) => animation.finished.catch(() => {})));
    });
    assert.equal(await card.locator(".receipt-details").count(), 0, "Overview has no secondary Details disclosure");
    const settlePanel = async () => card.evaluate(async (el) => {
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
      await Promise.all(el.getAnimations({ subtree: true }).map((animation) => animation.finished.catch(() => {})));
      const panels = el.querySelector(".receipt-panels");
      const active = panels.querySelector('[role="tabpanel"]:not([hidden])');
      return { container: panels.getBoundingClientRect().height, content: active.getBoundingClientRect().height };
    });
    const overviewSize = await settlePanel();
    assert.equal(await card.locator(".receipt-overview .receipt-filters").count(), 0);
    assert.equal(await card.evaluate((el) => {
      const overview = el.querySelector(".receipt-overview");
      const box = overview.getBoundingClientRect();
      return [...overview.querySelectorAll("p, li, .source-row")].filter((entry) => entry.getClientRects().length).every((entry) => {
        const rect = entry.getBoundingClientRect();
        return rect.left >= box.left - 1 && rect.right <= box.right + 1 && entry.scrollWidth <= entry.clientWidth + 1;
      });
    }), true, "Long definitions and source labels wrap inside Overview");
    const sourceChip = card.locator("[data-source-title]").first();
    await sourceChip.focus();
    const sourceTooltip = root.getByRole("tooltip");
    await sourceTooltip.waitFor({ state: "visible" });
    assert.equal(await sourceTooltip.locator(".receipt-tooltip-title").innerText(), await sourceChip.getAttribute("data-source-title"));
    assert.equal(await sourceTooltip.locator(".receipt-tooltip-reason").innerText(), await sourceChip.getAttribute("data-source-reason"));
    const tooltipStyles = await sourceTooltip.evaluate((el) => {
      const style = getComputedStyle(el);
      return { display: style.display, gap: style.gap, padding: style.padding, whiteSpace: style.whiteSpace };
    });
    assert.deepEqual(tooltipStyles, { display: "grid", gap: "4px", padding: "10px 12px", whiteSpace: "normal" });
    const tooltipBounds = await sourceTooltip.boundingBox();
    assert.ok(tooltipBounds.x >= 0 && tooltipBounds.width <= options.width,
      "Source inspection stays inside the narrow host");
    await sourceChip.press("Escape");
    await sourceTooltip.waitFor({ state: "hidden" });
    assert.equal(await toggle.getAttribute("aria-expanded"), "true", "Escape dismisses the tooltip before collapsing the receipt");
    const overviewTab = card.getByRole("tab", { name: "Overview", exact: true });
    await overviewTab.focus();
    await sourceChip.hover();
    await overviewTab.press("Escape");
    await new Promise((resolve) => setTimeout(resolve, 800));
    assert.equal(await sourceTooltip.isVisible(), false, "Escape cancels a pending hover before the 700 ms delay elapses");
    assert.equal(await toggle.getAttribute("aria-expanded"), "true");
    await card.getByRole("tab", { name: "SQL query", exact: true }).click();
    assert.equal((await focusStyle(card.getByRole("tab", { name: "SQL query", exact: true }))).outline, "none");
    const sqlSize = await settlePanel();
    assert.ok(Math.abs(sqlSize.container - sqlSize.content) <= 1, "SQL uses its own natural content height");
    assert.ok(Math.abs(sqlSize.container - overviewSize.container) > 1, "Tabs no longer retain the Overview height");
    const sqlPanel = card.getByRole("tabpanel", { name: "SQL query", exact: true });
    assert.equal(await sqlPanel.locator(".receipt-trace-chip").count(), 0,
      "Exact SQL is not preceded by a duplicate filter summary");
    const firstSql = multiple ? sqlPanel.getByRole("region", { name: "Illustrative activation export", exact: true }) : sqlPanel;
    assert.equal((await firstSql.locator("code").innerText()).replace(/^1\s*/u, ""),
      "SELECT week, activated, eligible FROM sample_activation ORDER BY week;");
    assert.deepEqual(await card.getByRole("tab").allTextContents(), tabLabels);
    assert.equal(await card.getByRole("button", { name: /^Source for /u }).count(), 0);
    assert.equal(await card.getByRole("button", { name: "Copy", exact: true }).count(), 0);
    await card.getByRole("tab", { name: "SQL query", exact: true }).press("ArrowRight");
    assert.equal(await card.getByRole("tab", { name: "Evidence flow", exact: true }).getAttribute("aria-selected"), "true");
    assert.deepEqual(await focusStyle(card.getByRole("tab", { name: "Evidence flow", exact: true })),
      { focused: true, outline: "solid", cardOutline: "none" }, "Arrow-key navigation must show keyboard focus");
    const evidencePanel = card.getByRole("tabpanel", { name: "Evidence flow", exact: true });
    assert.equal(await card.locator(".receipt-attribution").count(), 0, "Receipt prose does not append source-name annotations");
    await evidencePanel.locator('[data-checkpoint="filter"] summary').click();
    assert.equal(await evidencePanel.locator(".receipt-trace-chips").count(), 1,
      "Filters use one wrapping list without unexplained source sections");
    assert.equal(await evidencePanel.locator(":scope > :not(.source-trace)").count(), 0,
      "All supporting evidence belongs inside checkpoints");
    const filterTypography = await evidencePanel.locator(".receipt-trace-chip").evaluateAll((elements) => elements.map((el) => {
      const style = getComputedStyle(el);
      return { text: el.textContent, childCount: el.children.length,
        typography: [style.fontFamily, style.fontSize, style.fontWeight, style.lineHeight, style.color] };
    }));
    const periodQuery = generatedPayload(fixture).items[0].queries[0];
    const periodScope = multiple ? `${periodQuery.source.label}: ` : "";
    assert.deepEqual(filterTypography.filter(({ text }) => text.includes("Reporting period = ")).map(({ text }) => text),
      [`${periodScope}Reporting period = ${periodQuery.reportingPeriod}`],
      "The reporting period appears once and retains its owning source in a multi-source card");
    assert.ok(filterTypography.every(({ childCount, typography }) => childCount === 0
      && JSON.stringify(typography) === JSON.stringify(filterTypography[0].typography)),
      "Reporting period and filters share typography without nested source attribution");
    assert.match(await evidencePanel.locator(".receipt-trace-chips").innerText(), /including all supported product experiences/u);
    assert.equal(await evidencePanel.locator(".receipt-trace-chips").evaluate((el) => {
      const box = el.getBoundingClientRect();
      return [...el.querySelectorAll(".receipt-trace-chip")].every((entry) => {
        const rect = entry.getBoundingClientRect();
        return rect.left >= box.left - 1 && rect.right <= box.right + 1 && entry.scrollWidth <= entry.clientWidth + 1;
      });
    }), true, "The complete filter list wraps in Evidence flow");
    const detail = evidencePanel.locator('[data-checkpoint="source"] details');
    assert.equal(await detail.getAttribute("open"), null);
    await detail.locator("summary").click();
    assert.equal((await focusStyle(detail.locator("summary"))).outline, "none", "Pointer disclosure does not show a keyboard focus ring");
    assert.match(await detail.innerText(), /Supplies the eligible and activated counts/u);
    assert.doesNotMatch(await evidencePanel.innerText(), /Recorded inputs|Snapshot captured/u);
    const arithmetic = evidencePanel.locator("details").filter({ hasText: "240 / 400 × 100 = 60%" });
    await arithmetic.locator("summary").click();
    assert.equal(await arithmetic.locator(".receipt-calculation-text").last().innerText(), "240 / 400 × 100 = 60%\n280 / 400 × 100 = 70%\nChange: +10 percentage points");
    assert.equal(await arithmetic.locator(".receipt-trace-section-label").filter({ hasText: /^Calculation$/u }).count(), 0);
    const calculationTypography = await arithmetic.locator(".receipt-calculation-text").evaluateAll((elements) => elements.map((el) => {
      const style = getComputedStyle(el); return [style.fontFamily, style.fontSize, style.color, style.lineHeight];
    }));
    assert.ok(calculationTypography.every((value) => JSON.stringify(value) === JSON.stringify(calculationTypography[0])),
      "Supplemental formulas and worked arithmetic use the same body typography");
    const evidenceSize = await settlePanel();
    assert.ok(Math.abs(evidenceSize.container - evidenceSize.content) <= 1, "Expanded evidence resizes the card without a fixed-height scroll area");
    if (multiple) {
      const python = evidencePanel.locator("details").filter({ hasText: "rate = activated / eligible" });
      assert.equal(await python.getAttribute("open"), "", "Python shares the already expanded Calculation checkpoint");
      assert.match(await python.locator(".receipt-method").last().innerText(), /rate = activated \/ eligible/u);
      await card.getByRole("tab", { name: "SQL query", exact: true }).click();
      assert.match(await sqlPanel.getByRole("region", { name: "CSV calculation", exact: true }).innerText(), /SELECT period, value FROM sample_csv/u);
      await card.getByRole("tab", { name: "Data preview", exact: true }).click();
      const dataPanel = card.getByRole("tabpanel", { name: "Data preview", exact: true });
      const csvData = dataPanel.getByRole("region", { name: "CSV calculation", exact: true });
      assert.equal(await dataPanel.getByRole("table").count(), 2, "Separate result sets stay separate within one shared tab");
      assert.match(await csvData.innerText(), /117 of 130 recorded rows/u);
      await csvData.getByRole("button", { name: "Next page", exact: true }).click();
      await csvData.getByRole("button", { name: "Next page", exact: true }).click();
      assert.match(await csvData.getByRole("table", { name: "Reviewed data", exact: true }).innerText(), /Week 117/u);
      assert.equal(await csvData.getByRole("button", { name: "Next page", exact: true }).isEnabled(), false);
      assert.match(await dataPanel.getByRole("region", { name: "Illustrative activation export", exact: true }).innerText(), /240/u);
      await card.getByRole("tab", { name: "Overview", exact: true }).click();
      const overview = card.getByRole("tabpanel", { name: "Overview", exact: true });
      assert.equal(await overview.getByRole("heading", { level: 3 }).count(), 0, "Overview is organized around the finding, not repeated source blocks");
      assert.equal(await overview.getByText("Sources", { exact: true }).count(), 1);
      assert.doesNotMatch(await overview.innerText(), /240 \/ 400|280 \/ 400/u, "Worked arithmetic belongs in Evidence flow");
      await card.getByRole("tab", { name: "Data preview", exact: true }).click();
      assert.match(await csvData.getByRole("table", { name: "Reviewed data", exact: true }).innerText(), /Week 117/u,
        "Each source's paging state survives shared tab changes");
      await card.getByRole("tab", { name: "Data preview", exact: true }).press("Escape");
      await card.getByRole("button", { name: "How did activation change?", exact: true }).waitFor({ state: "visible" });
      assert.equal(await card.evaluate((el) => el.getRootNode().activeElement?.getAttribute("aria-label")), "How did activation change?");
      const other = root.getByRole("article", { name: "What changed in the release?", exact: true });
      await other.getByRole("button", { name: "What changed in the release?", exact: true }).click();
      assert.equal(await other.getByRole("tab").count(), 0);
      assert.equal(await other.getByRole("tabpanel").count(), 0);
      assert.match(await other.getByRole("region", { name: "Source details", exact: true }).innerText(), /The note records a setup change, not its effect on activation/u);
      assert.equal(await other.getByText("What this supports", { exact: true }).count(), 0);
      assert.equal(await other.getByRole("link", { name: "Release note", exact: true }).getAttribute("href"), "https://example.com/releases");
      await other.getByRole("button", { name: "Collapse What changed in the release?", exact: true }).click();
      assert.equal(await other.getAttribute("data-open"), "false");
      await other.getByRole("button", { name: "What changed in the release?", exact: true }).click();
      await other.locator(".receipt-card-title").click();
      assert.equal(await other.getAttribute("data-open"), "false", "The tab-free card header retains click-to-collapse");
    }
    assert.equal(await root.evaluate((el) => {
      const receipt = el.shadowRoot.querySelector(".sources-receipt");
      return receipt.scrollWidth <= receipt.clientWidth + 1;
    }), true, "Receipt must not overflow its inline width");
    await scenario.verifyClean();
    process.stdout.write(`${JSON.stringify({ test: "inline-sources-receipt", multiple, ...options, result: "pass" })}\n`);
  } finally { await scenario.context.close(); }
}

let browser;
try {
  const focusedReceiptCase = process.env.DATA_INLINE_BROWSER_CASE === "sources";
  const focusedAxisCase = focusedReceiptCase ? undefined : process.env.DATA_INLINE_BROWSER_CASE;
  const selectedAxisCases = focusedReceiptCase ? [] : focusedAxisCase
    ? numericAxisCases.filter(({ id }) => id === focusedAxisCase)
    : numericAxisCases;
  requirePass(
    !focusedAxisCase || selectedAxisCases.length === 1,
    `Unknown focused numeric-axis browser case: ${JSON.stringify(focusedAxisCase)}`,
  );
  const line = await renderFixture("reviewed-inline-chart", reviewedInput);
  const artifactName = inlineArtifactForChart(reviewedInput.chart.type);
  const preparedRuntime = await prepareInlineRuntime({
    pluginRoot,
    cacheDir: cacheRoot,
    offline: true,
    artifactName,
  });
  assert.equal(preparedRuntime.metadata.key, line.metadata.runtimeKey);
  assert.equal(preparedRuntime.prebuilt, true);
  assert.equal(preparedRuntime.cacheDir, null);
  assert.equal(preparedRuntime.metadata.source, "prebuilt");
  requirePass(
    typeof preparedRuntime.path === "string" && isAbsolute(preparedRuntime.path),
    "browser regressions must use the verified artifact shipped in the plugin",
  );
  assert.equal(
    await realpath(preparedRuntime.path),
    await realpath(join(pluginRoot, `assets/data-app-runtime/${artifactName}.js`)),
  );
  resources = new Map([
    [
      "https://unpkg.com/@floating-ui/core@1.7.3/dist/floating-ui.core.umd.min.js",
      join(dirname(dependencyRequire.resolve("@floating-ui/core/package.json")), "dist/floating-ui.core.umd.min.js"),
    ],
    [
      "https://unpkg.com/@floating-ui/dom@1.7.4/dist/floating-ui.dom.umd.min.js",
      join(dirname(dependencyRequire.resolve("@floating-ui/dom/package.json")), "dist/floating-ui.dom.umd.min.js"),
    ],
  ]);
  assert.equal(line.metadata.includedSql, false);
  assert.equal(line.metadata.includedSourceUrls, false);
  assert.equal(line.metadata.rowCount, reviewedInput.rows.length);
  assert.doesNotMatch(
    line.fragment,
    /restricted\.raw_metric_input/u,
    "default generated fragments must not embed reviewed SQL or SQL-derived evidence",
  );
  assert.doesNotMatch(
    line.fragment,
    /reviewed-source\.example\.test/u,
    "source URLs must not be embedded without explicit authorization",
  );
  assert.doesNotMatch(
    line.fragment,
    /NEVER_EMBED_UNREVIEWED_PRIVATE_COLUMN|unapprovedColumn|UNAPPROVED_ANNOTATION_LABEL/u,
    "unresolved annotation references must not disclose unapproved columns or labels",
  );
  assert.doesNotMatch(
    line.fragment,
    /NEVER_EMBED_UNREVIEWED_PRIVATE_DEFINITION/u,
    "definitions for unapproved private row fields must never enter the generated fragment",
  );
  assert.deepEqual(
    generatedPayload(line).query.source.metricDefinitions.map(({ field }) => field),
    ["activeUsers", "week", "plan"],
    "reviewed sources should retain displayed measure, temporal axis, and series attribution definitions only",
  );

  const explicitSql = await renderFixture("reviewed-inline-chart-with-sql", reviewedInput, [
    "--include-sql",
    "--include-source-urls",
  ]);
  assert.equal(explicitSql.metadata.includedSql, true);
  assert.equal(explicitSql.metadata.includedSourceUrls, true);
  assert.match(explicitSql.fragment, /restricted\.raw_metric_input/u);
  assert.match(explicitSql.fragment, /reviewed-source\.example\.test/u);

  const isolated = await renderFixture("reviewed-isolated-missing-week", isolatedGapInput);
  const isolatedPayload = generatedPayload(isolated);
  assert.equal(isolatedPayload.component.chart.y, "wau");
  assert.equal(
    isolatedPayload.component.chart.fields,
    undefined,
    "A missing week must not invent before-gap/after-gap series fields",
  );
  assert.deepEqual(
    isolatedPayload.rows,
    isolatedGapInput.rows,
    "Single-measure payloads must preserve reviewed dates, both values, and explicit missingness exactly",
  );
  assert.deepEqual(
    Object.keys(isolatedPayload.rows[0]),
    ["week", "wau"],
    "Single-measure payloads must not inject synthetic source-preview columns",
  );
  assert.equal(
    isolatedPayload.generatedAt,
    undefined,
    "User-provided examples without recorded freshness must not invent a render-time timestamp",
  );
  assert.equal(
    isolatedPayload.query.source.executedAt,
    undefined,
    "User-provided examples without recorded source execution must not invent source freshness",
  );
  assert.deepEqual(
    isolatedPayload.query.source.caveats,
    isolatedGapInput.source.caveats,
    "Missing-value and illustrative-data caveats must survive canonical source normalization verbatim",
  );

  const heatmap = (theme) => ({
    ...reviewedInput,
    id: `reviewed-heatmap-${theme}`,
    title: `Reviewed ${theme} heatmap`,
    chart: { type: "heatmap", x: "week", y: "activeUsers", series: "plan" },
    theme,
  });
  const classic = await renderFixture("reviewed-classic-heatmap", heatmap("codex-classic"));
  const scientific = await renderFixture("reviewed-scientific-heatmap", heatmap("scientific-blue"));
  const darkPixel = await renderFixture("reviewed-dark-pixel-heatmap", heatmap("dark-pixel"));
  const axisFixtures = await Promise.all(
    selectedAxisCases.map(async (descriptor) => ({
      descriptor,
      fixture: await renderFixture(`reviewed-readable-axis-${descriptor.id}`, descriptor.input),
    })),
  );
  const capacityFixtures = focusedAxisCase || focusedReceiptCase ? [] : await Promise.all([100, 200].map(async (rowCount) => ({
    rowCount,
    fixture: await renderFixture(`reviewed-capacity-${rowCount}`, inlineCapacityInput(rowCount)),
  })));
  for (const { fixture, rowCount } of capacityFixtures) {
    assert.equal(generatedPayload(fixture).rows.length, rowCount);
    assert.equal(generatedPayload(fixture).query.rows, undefined, "The bootstrap restores shared inspector rows");
    assert.ok(Buffer.byteLength(fixture.fragment) <= 1_000_000);
  }

  const host = await buildActualVisualizationHost();
  const receiptFixtures = focusedAxisCase ? [] : [await receiptFixture("single-sources"), await receiptFixture("multiple-sources", { multiple: true })];
  const fixtures = [
    line,
    explicitSql,
    isolated,
    classic,
    scientific,
    darkPixel,
    ...axisFixtures.map(({ fixture }) => fixture),
    ...capacityFixtures.map(({ fixture }) => fixture),
    ...receiptFixtures,
  ];
  const previews = new Map(
    await Promise.all(fixtures.map(async (fixture) => [fixture.name, await standalonePreview(fixture, host)])),
  );

  browser = await chromium.launch({ executablePath, headless: true });
  for (const [index, fixture] of receiptFixtures.entries()) {
    for (const [width, colorScheme, reducedMotion] of [[736, "light", "no-preference"], [360, "dark", "no-preference"], [320, "light", "no-preference"], [360, "dark", "reduce"]])
      await inspectSourcesReceipt(browser, fixture, previews.get(fixture.name), { multiple: index > 0, width, colorScheme, reducedMotion });
  }
  for (const { fixture, rowCount } of capacityFixtures) {
    await inspectCapacityScenario(browser, fixture, previews.get(fixture.name), rowCount);
  }
  if (!focusedAxisCase && !focusedReceiptCase) {
    for (const width of [736, 360, 320]) {
      for (const colorScheme of ["light", "dark"]) {
        await inspectLineScenario(browser, line, previews.get(line.name), { width, colorScheme });
      }
    }
  }
  for (const { descriptor, fixture } of axisFixtures) {
    await inspectReadableAxes(browser, fixture, previews.get(fixture.name), descriptor, {
      width: 736,
      colorScheme: "light",
    });
    await inspectReadableAxes(browser, fixture, previews.get(fixture.name), descriptor, {
      width: 360,
      colorScheme: "dark",
    });
  }
  if (!focusedAxisCase && !focusedReceiptCase) {
    await inspectIsolatedGap(browser, isolated, previews.get(isolated.name), { width: 736, colorScheme: "light" });
    await inspectIsolatedGap(browser, isolated, previews.get(isolated.name), { width: 360, colorScheme: "dark" });
    await inspectSeparateReferenceIsolation(browser, line, isolated, previews, { width: 736, colorScheme: "light" });
    await inspectSeparateReferenceIsolation(browser, line, isolated, previews, { width: 360, colorScheme: "dark" });
    await inspectSqlOptIn(browser, explicitSql, previews.get(explicitSql.name));
    await inspectThemeRadius(browser, classic, previews.get(classic.name), {
      theme: "codex-classic",
      radius: 8,
      stroke: "light-dark(#0285ff, #66b5ff)",
    });
    await inspectThemeRadius(browser, scientific, previews.get(scientific.name), {
      theme: "scientific-blue",
      radius: 2,
      stroke: "#1769e0",
    });
    await inspectThemeRadius(browser, darkPixel, previews.get(darkPixel.name), {
      theme: "dark-pixel",
      radius: 0,
      stroke: "#b6ff3b",
      scheme: "dark",
    });
  }
  process.stdout.write(
    focusedReceiptCase ? "PASS: Sources receipts in the actual Codex sandbox at desktop and narrow widths.\n" : focusedAxisCase
      ? `PASS: focused ${focusedAxisCase} numeric-axis browser regression at desktop and narrow widths.\n`
      : "PASS: production shared dashboard charts, actual Codex sandbox insertion, legacy String.replace compatibility, six adaptive widths/themes, readable responsive native numeric axes, canonical isolated missing-week observations, separate-reference sandbox isolation, contained source tabs, SQL privacy, and theme-owned mark geometry.\n",
  );
} finally {
  if (browser) await browser.close();
  await rm(workspace, { recursive: true, force: true });
}
