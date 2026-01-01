// Release-time partitions of the canonical renderer, not separate implementations.
// The general inline artifact remains available for callers without a chart spec.
export const inlineChartFamilies = Object.freeze({
  trend: Object.freeze(["line", "area", "stackedArea", "sparkline"]),
  cartesian: Object.freeze(["bar", "horizontalBar",
    "stackedBar", "stackedBar100", "horizontalStackedBar", "horizontalStackedBar100",
    "histogram", "scatter", "waterfall", "boxPlot"]),
  categorical: Object.freeze(["heatmap", "pie", "leaderboard", "rankedList", "funnel"]),
  flow: Object.freeze(["sankey"]),
});

export const inlineFamilyArtifacts = Object.freeze(Object.fromEntries(
  Object.keys(inlineChartFamilies).map(family => [family, `inline-${family}`]),
));

export function inlineArtifactForChart(type) {
  const family = Object.keys(inlineChartFamilies).find(key => inlineChartFamilies[key].includes(type));
  if (!family) throw new Error(`Unsupported inline chart type: ${String(type)}`);
  return inlineFamilyArtifacts[family];
}
