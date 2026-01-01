import React, { useCallback, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";

import { ChartRenderer } from "../base/src/charting/ChartRenderer.jsx";
import { Icon, SourceSidebar, semanticColorResolver } from "../base/src/data-app-public.jsx";
import dashboardStyles from "../base/src/styles.css?inline";
import inlineStyles from "./inline.css?inline";

const mountedCharts = new WeakMap();

function scopeDashboardStyles(styles) {
  return styles.replace(/:root((?:\[[^\]]+\]|:(?:is|not|where)\([^)]*\))*)/gu, (_, conditions) =>
    conditions ? `:host(${conditions})` : ":host",
  );
}

function InlineChart({ host, payload }) {
  const { component, rows, query, filters, height } = payload;
  const [sourceOpen, setSourceOpen] = useState(false);
  const resolveColor = useMemo(() => semanticColorResolver({ [component.queryId]: query }), [component.queryId, query]);
  const getSource = useCallback(() => ({ query, rows, filters }), [filters, query, rows]);
  const closeSource = useCallback(() => setSourceOpen(false), []);

  return (
    <div className="data-inline-chart-stage">
      <section
        className="dashboard-component data-inline-chart-content"
        data-component-id={component.id}
        data-component-kind="chart"
        data-query-id={component.queryId}
      >
        <header className="component-header">
          <h2 className="component-title">
            <span className="component-title-text">{component.title}</span>
            <button
              type="button"
              className="info"
              aria-label="View data source"
              aria-expanded={sourceOpen}
              onClick={() => setSourceOpen(true)}
            >
              <Icon name="info" />
            </button>
          </h2>
        </header>
        <ChartRenderer
          spec={component.chart}
          rows={rows}
          height={height}
          chartId={component.id}
          resolveColor={resolveColor}
          themeRoot={host}
        />
      </section>
      {sourceOpen && (
        <SourceSidebar
          component={component}
          getSource={getSource}
          onClose={closeSource}
          variant="contained"
          allowCopy={false}
        />
      )}
    </div>
  );
}

/** Mount the actual dashboard chart and source inspector inside an isolated inline host. */
export function mountInlineChart(host, payload) {
  if (!host || typeof host.attachShadow !== "function") {
    throw new TypeError("An inline chart requires a valid Shadow DOM host.");
  }
  if (payload?.schemaVersion !== 1) {
    throw new TypeError("An inline chart requires a supported reviewed payload.");
  }
  if (typeof payload.theme?.css !== "string") {
    throw new TypeError("An inline chart requires its bundled dashboard theme.");
  }

  mountedCharts.get(host)?.();

  const shadow = host.shadowRoot ?? host.attachShadow({ mode: "open" });
  const previousTheme = host.getAttribute("data-app-theme");
  host.setAttribute("data-app-theme", payload.theme.id);

  const fixedScheme = ["dark", "light"].includes(payload.theme.fixedScheme) ? payload.theme.fixedScheme : "inherit";
  const styles = [
    scopeDashboardStyles(dashboardStyles),
    scopeDashboardStyles(payload.theme.css),
    inlineStyles,
    `:host { color-scheme: ${fixedScheme}; }`,
  ].join("\n");

  const stylesheet = host.ownerDocument.createElement("style");
  stylesheet.setAttribute("data-inline-dashboard-styles", "");
  stylesheet.textContent = styles;
  const container = host.ownerDocument.createElement("div");
  container.className = "data-inline-react-root";
  shadow.append(stylesheet, container);

  const root = createRoot(container);
  root.render(<InlineChart host={host} payload={payload} />);

  function unmount() {
    if (mountedCharts.get(host) !== unmount) return;
    mountedCharts.delete(host);
    root.unmount();
    container.remove();
    stylesheet.remove();
    if (previousTheme === null) host.removeAttribute("data-app-theme");
    else host.setAttribute("data-app-theme", previousTheme);
  }

  mountedCharts.set(host, unmount);
  return unmount;
}
