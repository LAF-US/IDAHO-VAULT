"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/main.ts
var main_exports = {};
__export(main_exports, {
  default: () => VaultInspectorPlugin,
  formatFixResultNotice: () => formatFixResultNotice,
  migrateExcalidrawFrontmatterKey: () => migrateExcalidrawFrontmatterKey
});
module.exports = __toCommonJS(main_exports);
var import_obsidian7 = require("obsidian");

// src/report/InspectorView.ts
var import_obsidian3 = require("obsidian");

// src/scanner/Issue.ts
var SCANNER_IDS = [
  "broken-links",
  "orphan-attachments",
  "empty-notes",
  "external-links",
  "duplicate-files",
  "frontmatter-types",
  "tag-usage",
  "large-files"
];
var SCANNER_LABELS = {
  "broken-links": "Broken Links",
  "orphan-attachments": "Orphan Attachments",
  "empty-notes": "Empty Notes",
  "external-links": "External Links",
  "duplicate-files": "Duplicate Files",
  "frontmatter-types": "Frontmatter Types",
  "tag-usage": "Tag Usage",
  "large-files": "Large Files"
};

// src/report/report-model.ts
var SEVERITIES = ["error", "warning", "info"];
function buildIssueFilterView(issues, filters) {
  var _a, _b;
  const visibleIssues = issues.filter(
    (issue) => (!filters.scanner || issue.scannerId === filters.scanner) && (!filters.severity || issue.severity === filters.severity)
  );
  const scannerCounts = /* @__PURE__ */ new Map();
  for (const issue of issues) scannerCounts.set(issue.scannerId, 0);
  for (const issue of issues) {
    if (filters.severity && issue.severity !== filters.severity) continue;
    scannerCounts.set(issue.scannerId, ((_a = scannerCounts.get(issue.scannerId)) != null ? _a : 0) + 1);
  }
  const severityCounts = new Map(
    SEVERITIES.map((severity) => [severity, 0])
  );
  for (const issue of issues) {
    if (filters.scanner && issue.scannerId !== filters.scanner) continue;
    severityCounts.set(issue.severity, ((_b = severityCounts.get(issue.severity)) != null ? _b : 0) + 1);
  }
  const severityFacets = SEVERITIES.map((severity) => {
    var _a2;
    return { severity, count: (_a2 = severityCounts.get(severity)) != null ? _a2 : 0 };
  }).filter(({ severity, count }) => count > 0 || filters.severity === severity);
  return {
    visibleIssues,
    scannerCounts,
    severityFacets
  };
}
function summarizeIssues(issues) {
  return {
    total: issues.length,
    errors: issues.filter((issue) => issue.severity === "error").length,
    warnings: issues.filter((issue) => issue.severity === "warning").length,
    infos: issues.filter((issue) => issue.severity === "info").length
  };
}

// src/utils/format.ts
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}
function formatDuration(ms) {
  const safeMs = Math.max(0, Math.round(ms));
  if (safeMs < 1e3) return `${safeMs}ms`;
  const seconds = safeMs / 1e3;
  if (seconds < 10) return `${seconds.toFixed(1)}s`;
  if (seconds < 60) return `${Math.round(seconds)}s`;
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.round(seconds % 60);
  if (remainingSeconds === 60) return `${minutes + 1}m 00s`;
  return `${minutes}m ${remainingSeconds.toString().padStart(2, "0")}s`;
}

// src/report/render-summary.ts
function renderSummary(container, result, options) {
  const { total, errors, warnings, infos } = summarizeIssues(options.issues);
  const duration = formatDuration(result.finishedAt - result.startedAt);
  const summary = container.createDiv({ cls: "vi-summary" });
  summary.createEl("h2", { text: "Scan results" });
  const stats = summary.createDiv({ cls: "vi-stats" });
  const items = [
    { label: "Total", value: total, cls: "vi-stat-total", severity: null },
    { label: "Errors", value: errors, cls: "vi-stat-error", severity: "error" },
    { label: "Warnings", value: warnings, cls: "vi-stat-warning", severity: "warning" },
    { label: "Info", value: infos, cls: "vi-stat-info", severity: "info" }
  ];
  for (const item of items) {
    const stat = stats.createDiv({ cls: `vi-stat ${item.cls}` });
    stat.createSpan({ cls: "vi-stat-value", text: String(item.value) });
    stat.createSpan({ cls: "vi-stat-label", text: item.label });
    if (options.onFilterSeverity) {
      stat.addClass("vi-stat-clickable");
      stat.addEventListener("click", () => {
        var _a;
        return (_a = options.onFilterSeverity) == null ? void 0 : _a.call(options, item.severity);
      });
    }
  }
  const meta = summary.createDiv({ cls: "vi-meta" });
  meta.createSpan({ text: `${result.filesScanned} files scanned` });
  meta.createSpan({ text: duration });
  meta.createSpan({ text: `${result.scannersRun.length} scanners` });
}

// src/report/render-issues.ts
var import_obsidian = require("obsidian");
function renderIssueList(container, config) {
  var _a;
  const grouped = groupByScanner(config.issues);
  for (const scannerId of config.scannersRun) {
    const scannerIssues = (_a = grouped[scannerId]) != null ? _a : [];
    if (scannerIssues.length === 0) continue;
    const section = container.createDiv({ cls: "vi-scanner-section" });
    section.createEl("h3", {
      cls: "vi-scanner-header",
      text: `${SCANNER_LABELS[scannerId]} (${scannerIssues.length})`
    });
    const list = section.createEl("ul", { cls: "vi-issue-list" });
    for (const issue of scannerIssues) {
      const isSelected = config.selectedFingerprints.has(issue.fingerprint);
      const cls = [
        "vi-issue",
        `vi-severity-${issue.severity}`,
        config.selectionMode ? "vi-selectable" : "",
        isSelected ? "vi-selected" : ""
      ].filter(Boolean).join(" ");
      const li = list.createEl("li", { cls });
      if (config.selectionMode) {
        const checkbox = li.createEl("input", { cls: "vi-issue-checkbox", type: "checkbox" });
        checkbox.checked = isSelected;
        checkbox.addEventListener("click", (e) => {
          e.stopPropagation();
          config.onToggleSelect(issue);
        });
        li.addEventListener("click", () => config.onToggleSelect(issue));
      }
      li.createSpan({
        cls: `vi-severity-badge vi-severity-${issue.severity}`,
        text: issue.severity.toUpperCase()
      });
      li.createSpan({ cls: "vi-issue-title", text: issue.title });
      const issuePath = getIssuePath(issue);
      if (issuePath) {
        const pathEl = li.createSpan({
          cls: "vi-issue-path",
          text: issuePath
        });
        (0, import_obsidian.setTooltip)(pathEl, "Click to open issue location");
        pathEl.addEventListener("click", (e) => {
          e.stopPropagation();
          if (hasActiveTextSelection()) return;
          config.onOpenIssue(makePathIssue(issue, issuePath));
        });
      }
      renderIssueDetails(li, issue, config);
    }
  }
}
function hasActiveTextSelection() {
  var _a;
  return ((_a = window.getSelection()) == null ? void 0 : _a.toString().trim().length) ? true : false;
}
function renderIssueDetails(container, issue, config) {
  var _a;
  const details = container.createDiv({ cls: "vi-issue-details" });
  const summary = getIssueSummary(issue);
  if (summary) details.createDiv({ cls: "vi-issue-message", text: summary });
  for (const row of getIssueDetailRows(issue)) {
    const rowEl = details.createDiv({ cls: "vi-issue-target" });
    rowEl.createSpan({ cls: "vi-issue-target-label", text: row.label });
    const valueEl = rowEl.createSpan({ cls: "vi-issue-target-value" });
    if ("value" in row) {
      valueEl.setText(row.value);
    } else {
      for (const item of row.items) {
        const itemEl = valueEl.createSpan({
          cls: `vi-issue-value-token ${(_a = item.className) != null ? _a : ""}`.trim(),
          text: item.text
        });
        if (!item.issue) continue;
        itemEl.addClass("vi-issue-value-clickable");
        (0, import_obsidian.setTooltip)(itemEl, "Click to open issue location");
        itemEl.addEventListener("click", (event) => {
          event.stopPropagation();
          if (hasActiveTextSelection()) return;
          config.onOpenIssue(item.issue);
        });
      }
    }
  }
}
function getIssueSummary(issue) {
  switch (issue.scannerId) {
    case "external-links":
      return getExternalLinkSummary(issue);
    case "large-files": {
      const size = getNumber(issue.evidence.size);
      const threshold = getNumber(issue.evidence.threshold);
      if (size !== null && threshold !== null) {
        return `File is ${formatSize(size)}, over ${formatSize(threshold)} threshold`;
      }
      return issue.message;
    }
    case "orphan-attachments": {
      const lastModified = getNumber(issue.evidence.lastModified);
      return lastModified !== null ? `Not referenced by any note \xB7 modified ${formatDate(lastModified)}` : issue.message;
    }
    case "empty-notes": {
      const size = getNumber(issue.evidence.size);
      return size !== null ? `No content besides frontmatter/title \xB7 ${formatSize(size)}` : issue.message;
    }
    default:
      return issue.message;
  }
}
function getExternalLinkSummary(issue) {
  if (issue.title === "External link check timed out") {
    const timeoutMs = getNumber(issue.evidence.timeoutMs);
    return timeoutMs !== null ? `Timed out after ${timeoutMs}ms` : "Timed out";
  }
  if (issue.title === "External link check failed") {
    const error = issue.evidence.error;
    return typeof error === "string" && error.length > 0 ? `Request failed: ${error}` : "Request failed";
  }
  if (issue.title === "Dead external link") {
    const status = getNumber(issue.evidence.status);
    return status !== null ? `HTTP ${status}` : "HTTP error";
  }
  return issue.message;
}
function getIssueDetailRows(issue) {
  const rows = [];
  const target = getIssueTarget(issue);
  if (target) {
    rows.push({
      label: getTargetLabel(issue),
      items: [{
        text: target,
        issue: makeTargetIssue(issue, target),
        className: "vi-issue-token-monospace"
      }]
    });
  }
  if (issue.scannerId === "duplicate-files") {
    const count = getNumber(issue.evidence.count);
    if (count !== null) rows.push({ label: "Count", value: String(count) });
    const paths = getEvidencePaths(issue);
    if (paths.length > 0) {
      rows.push({
        label: "Files",
        items: paths.map((path) => ({
          text: path,
          issue: makePathIssue(issue, path),
          className: "vi-issue-path-token"
        }))
      });
    }
  }
  if (issue.scannerId === "frontmatter-types") {
    const property = issue.evidence.property;
    const types = issue.evidence.types;
    const fileCount = getNumber(issue.evidence.fileCount);
    if (typeof property === "string") {
      rows.push({
        label: "Property",
        items: [{
          text: property,
          issue: issue.relatedPaths.length > 0 ? makePropertyIssue(issue, property) : void 0,
          className: "vi-issue-token-monospace"
        }]
      });
    }
    if (typeof types === "string") rows.push({ label: "Types", value: types });
    if (fileCount !== null) rows.push({ label: "Files", value: String(fileCount) });
    if (issue.relatedPaths.length > 0) {
      rows.push({
        label: "Sample",
        items: issue.relatedPaths.map((path) => ({
          text: path,
          issue: makePathIssue(issue, path),
          className: "vi-issue-path-token"
        }))
      });
    }
  }
  if (issue.scannerId === "tag-usage") {
    const tag = issue.evidence.tag;
    const count = getNumber(issue.evidence.count);
    const threshold = getNumber(issue.evidence.threshold);
    if (typeof tag === "string") {
      rows.push({
        label: "Tag",
        items: [{
          text: formatTag(tag),
          issue: issue.primaryPath ? makeTagIssue(issue, tag) : void 0,
          className: "vi-issue-tag-token"
        }]
      });
    }
    if (count !== null) rows.push({ label: "Count", value: String(count) });
    if (threshold !== null) rows.push({ label: "Threshold", value: String(threshold) });
  }
  if (issue.scannerId === "large-files") {
    const type = issue.evidence.type;
    if (typeof type === "string") rows.push({ label: "Type", value: type });
  }
  return rows;
}
function makePathIssue(issue, path) {
  return {
    ...issue,
    primaryPath: path,
    relatedPaths: issue.relatedPaths.filter((relatedPath) => relatedPath !== path)
  };
}
function makeTargetIssue(issue, target) {
  const evidence = { ...issue.evidence };
  if (issue.scannerId === "external-links") {
    evidence.url = target;
  } else if (issue.scannerId === "broken-links") {
    evidence.target = target;
  } else {
    evidence.link = target;
  }
  return {
    ...issue,
    evidence
  };
}
function makeTagIssue(issue, tag) {
  return {
    ...issue,
    evidence: {
      ...issue.evidence,
      tag
    }
  };
}
function makePropertyIssue(issue, property) {
  var _a;
  return {
    ...issue,
    primaryPath: (_a = issue.primaryPath) != null ? _a : issue.relatedPaths[0],
    evidence: {
      ...issue.evidence,
      property
    }
  };
}
function getIssueTarget(issue) {
  const url = issue.evidence.url;
  if (typeof url === "string") return url;
  const link = issue.evidence.link;
  if (typeof link === "string") return link;
  const target = issue.evidence.target;
  if (typeof target === "string") return target;
  return null;
}
function getTargetLabel(issue) {
  if (issue.scannerId === "external-links") return "URL";
  if (issue.scannerId === "broken-links") return "Target";
  return "Target";
}
function getEvidencePaths(issue) {
  const paths = issue.evidence.paths;
  if (typeof paths !== "string") return issue.relatedPaths;
  return paths.split(",").map((path) => path.trim()).filter(Boolean);
}
function getNumber(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}
function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString();
}
function getIssuePath(issue) {
  var _a, _b;
  return (_b = (_a = issue.primaryPath) != null ? _a : issue.relatedPaths[0]) != null ? _b : null;
}
function formatTag(tag) {
  return tag.startsWith("#") ? tag : `#${tag}`;
}
function groupByScanner(issues) {
  const groups = {};
  for (const issue of issues) {
    if (!groups[issue.scannerId]) groups[issue.scannerId] = [];
    groups[issue.scannerId].push(issue);
  }
  return groups;
}

// src/report/InspectorView.ts
var import_obsidian4 = require("obsidian");

// src/fix/confirm-modal.ts
var import_obsidian2 = require("obsidian");

// src/fix/fix-decisions.ts
function buildFixDecisionState(issues, mode, selectedKeeps) {
  const decisions = [];
  let complete = true;
  for (const issue of issues) {
    const action = issue.fixAction;
    if (!action) continue;
    const selection = action.selection;
    if (!selection) {
      decisions.push({ fingerprint: issue.fingerprint });
      continue;
    }
    const keepPath = mode === "automatic" ? selection.automaticKeepPath : selectedKeeps.get(issue.fingerprint);
    if (!keepPath || !selection.candidatePaths.includes(keepPath)) {
      complete = false;
      continue;
    }
    decisions.push({ fingerprint: issue.fingerprint, keepPath });
  }
  return { complete, decisions };
}
function resolveDecisionAction(issue, decision) {
  const action = issue.fixAction;
  if (!action || decision.fingerprint !== issue.fingerprint) return null;
  const selection = action.selection;
  if (!selection) return decision.keepPath === void 0 ? action : null;
  if (!decision.keepPath || !selection.candidatePaths.includes(decision.keepPath)) {
    return null;
  }
  const targetPaths = selection.candidatePaths.filter(
    (path) => path !== decision.keepPath
  );
  return {
    ...action,
    description: `Keep "${decision.keepPath}" and move ${targetPaths.length} duplicate(s) to trash`,
    targetPaths
  };
}
function getFreshFixAction(requestedIssue, freshIssue, decision) {
  const requested = requestedIssue.fixAction;
  const fresh = freshIssue == null ? void 0 : freshIssue.fixAction;
  if (decision.fingerprint !== requestedIssue.fingerprint || (freshIssue == null ? void 0 : freshIssue.fingerprint) !== requestedIssue.fingerprint || !requested || !fresh) {
    return null;
  }
  if (requested.selection || fresh.selection) {
    if (!requested.selection || !fresh.selection || requested.kind !== fresh.kind || requested.label !== fresh.label || !samePaths(
      requested.selection.candidatePaths,
      fresh.selection.candidatePaths
    )) {
      return null;
    }
    return resolveDecisionAction(freshIssue, decision);
  }
  return fixActionsMatch(requested, fresh) ? fresh : null;
}
function samePaths(left, right) {
  const sortedLeft = left.slice().sort();
  const sortedRight = right.slice().sort();
  return sortedLeft.length === sortedRight.length && sortedRight.every((path, index) => path === sortedLeft[index]);
}
function fixActionsMatch(left, right) {
  return left.kind === right.kind && left.label === right.label && left.description === right.description && left.linkText === right.linkText && left.targetPaths.length === right.targetPaths.length && left.targetPaths.every(
    (path, index) => path === right.targetPaths[index]
  );
}

// src/fix/confirm-modal.ts
function describeFixActions(actions) {
  const modifiedNotes = new Set(
    actions.filter((action) => action.kind === "remove-link-text").flatMap((action) => action.targetPaths)
  );
  const trashedFiles = new Set(
    actions.filter((action) => action.kind === "trash-file").flatMap((action) => action.targetPaths)
  );
  const parts = [];
  if (modifiedNotes.size > 0) {
    parts.push(`modify ${modifiedNotes.size} ${pluralize("note", modifiedNotes.size)}`);
  }
  if (trashedFiles.size > 0) {
    parts.push(`move ${trashedFiles.size} ${pluralize("file", trashedFiles.size)} to trash`);
  }
  const description = parts.join(" and ");
  return description.length > 0 ? description.charAt(0).toUpperCase() + description.slice(1) : "Apply selected fixes";
}
function summarizeFixActions(actions) {
  var _a, _b;
  const isBatch = actions.length > 1;
  const impact = describeFixActions(actions);
  return {
    title: isBatch ? `Confirm batch fix (${actions.length} actions)` : "Confirm fix",
    description: isBatch ? `This will ${impact.charAt(0).toLowerCase()}${impact.slice(1)}.` : (_b = (_a = actions[0]) == null ? void 0 : _a.description) != null ? _b : "No fix action selected.",
    paths: [...new Set(actions.flatMap((action) => action.targetPaths))]
  };
}
function pluralize(noun, count) {
  return count === 1 ? noun : `${noun}s`;
}
function createSingleUseResolver(resolve) {
  let settled = false;
  return (value) => {
    if (settled) return false;
    settled = true;
    resolve(value);
    return true;
  };
}
function showConfirmModal(app, issues, mode) {
  return new Promise((resolve) => {
    new ConfirmFixModal(app, issues, mode, resolve).open();
  });
}
var ConfirmFixModal = class extends import_obsidian2.Modal {
  constructor(app, issues, mode, resolve) {
    super(app);
    this.selectedKeeps = /* @__PURE__ */ new Map();
    this.issues = issues;
    this.mode = mode;
    this.settle = createSingleUseResolver(resolve);
  }
  onOpen() {
    this.contentEl.addClass("vi-confirm-modal");
    this.renderContent();
  }
  onClose() {
    this.contentEl.empty();
    this.settle(null);
  }
  finish(result) {
    if (this.settle(result)) this.close();
  }
  renderContent() {
    var _a;
    const { contentEl } = this;
    contentEl.empty();
    contentEl.addClass("vi-confirm-modal");
    const state = buildFixDecisionState(
      this.issues,
      this.mode,
      this.selectedKeeps
    );
    const decisionsByFingerprint = new Map(
      state.decisions.map((decision) => [decision.fingerprint, decision])
    );
    const actions = this.issues.flatMap((issue) => {
      const decision = decisionsByFingerprint.get(issue.fingerprint);
      if (!decision) return [];
      const action = resolveDecisionAction(issue, decision);
      return action ? [action] : [];
    });
    const summary = summarizeFixActions(actions);
    contentEl.createEl("h3", {
      text: this.issues.length > 1 ? `Confirm batch fix (${this.issues.length} actions)` : "Confirm fix"
    });
    contentEl.createEl("p", {
      text: state.complete ? summary.description : "Choose one file to keep in every duplicate group."
    });
    if (this.mode === "always-ask") {
      for (const issue of this.issues) {
        const selection = (_a = issue.fixAction) == null ? void 0 : _a.selection;
        if (!selection) continue;
        const group = contentEl.createDiv({ cls: "vi-keep-group" });
        group.createDiv({
          cls: "vi-keep-group-title",
          text: "Choose one file to keep"
        });
        for (const path of selection.candidatePaths) {
          const option = group.createEl("label", { cls: "vi-keep-option" });
          const radio = option.createEl("input", { type: "radio" });
          radio.name = `keep-${issue.fingerprint}`;
          radio.checked = this.selectedKeeps.get(issue.fingerprint) === path;
          radio.addEventListener("change", () => {
            this.selectedKeeps.set(issue.fingerprint, path);
            this.renderContent();
          });
          option.createSpan({ cls: "vi-keep-option-path", text: path });
        }
      }
    }
    if (this.issues.length > 1 || actions.length > 1) {
      const list = contentEl.createDiv({ cls: "vi-file-list" });
      for (const path of summary.paths) {
        list.createDiv({ cls: "vi-file-list-item", text: path });
      }
    }
    const btnRow = contentEl.createDiv({ cls: "vi-confirm-buttons" });
    btnRow.createEl("button", { text: "Cancel" }).addEventListener("click", () => this.finish(null));
    const confirmBtn = btnRow.createEl("button", {
      cls: "vi-confirm-destructive",
      text: "Confirm"
    });
    confirmBtn.disabled = !state.complete;
    confirmBtn.addEventListener("click", () => {
      if (state.complete) this.finish(state.decisions);
    });
  }
};

// src/report/InspectorView.ts
var VIEW_TYPE_INSPECTOR = "vault-inspector";
function getLocationTargets(issue) {
  const url = issue.evidence.url;
  if (typeof url === "string") return [url];
  const link = issue.evidence.link;
  if (typeof link === "string") return [link];
  const target = issue.evidence.target;
  if (typeof target === "string") return [target];
  const property = issue.evidence.property;
  if (typeof property === "string") return [property];
  const tag = issue.evidence.tag;
  if (typeof tag === "string") return [`#${tag}`, tag];
  return [];
}
function findFirstTextPosition(content, targets) {
  for (const target of targets) {
    const position = findTextPosition(content, target);
    if (position) return position;
  }
  return null;
}
function findTextPosition(content, target) {
  const index = content.indexOf(target);
  if (index === -1) return null;
  const before = content.slice(0, index);
  const lines = before.split(/\n/);
  return {
    line: lines.length - 1,
    ch: lines[lines.length - 1].length
  };
}
var InspectorView = class extends import_obsidian3.ItemView {
  constructor(leaf) {
    super(leaf);
    this.model = {
      result: null,
      isScanning: false,
      scanProgress: null,
      scanStartedAt: null,
      filterScanner: null,
      filterSeverity: null,
      enableFixActions: true,
      selectionMode: false,
      selectedFingerprints: /* @__PURE__ */ new Set(),
      ignoredExpanded: false,
      ignoredSelectionMode: false,
      ignoredSelectedFingerprints: /* @__PURE__ */ new Set()
    };
    this.onIgnoreAllIssues = null;
    this.onRestoreIssues = null;
    this.onFixAllIssues = null;
    this.onRevealIssue = null;
    this.onRunScan = null;
    this.backToTopHandler = null;
    this.scanTimer = null;
  }
  getViewType() {
    return VIEW_TYPE_INSPECTOR;
  }
  getDisplayText() {
    return "Vault inspector";
  }
  getIcon() {
    return "shield-check";
  }
  async onOpen() {
    await Promise.resolve();
    const container = this.containerEl.children[1];
    container.empty();
    container.classList.add("vault-inspector");
    this.render();
  }
  async onClose() {
    await Promise.resolve();
    if (this.backToTopHandler) {
      const container = this.containerEl.children[1];
      container.removeEventListener("scroll", this.backToTopHandler);
      this.backToTopHandler = null;
    }
    this.stopScanTimer();
    this.onIgnoreAllIssues = null;
    this.onRestoreIssues = null;
    this.onFixAllIssues = null;
    this.onRevealIssue = null;
    this.onRunScan = null;
  }
  setScanning(scanning) {
    this.model.isScanning = scanning;
    if (scanning) {
      this.model.scanStartedAt = Date.now();
      this.model.scanProgress = null;
      this.startScanTimer();
    } else {
      this.model.scanProgress = null;
      this.model.scanStartedAt = null;
      this.stopScanTimer();
    }
    this.render();
  }
  setScanProgress(progress) {
    this.model.scanProgress = progress;
    this.render();
  }
  setResult(result) {
    this.model.result = result;
    this.model.isScanning = false;
    this.model.scanProgress = null;
    this.model.scanStartedAt = null;
    this.stopScanTimer();
    this.model.selectionMode = false;
    this.model.selectedFingerprints = /* @__PURE__ */ new Set();
    this.model.ignoredSelectionMode = false;
    this.model.ignoredSelectedFingerprints = /* @__PURE__ */ new Set();
    this.render();
  }
  setEnableFixActions(enabled) {
    this.model.enableFixActions = enabled;
  }
  setCallbacks(callbacks) {
    this.onIgnoreAllIssues = callbacks.onIgnoreAllIssues;
    this.onRestoreIssues = callbacks.onRestoreIssues;
    this.onFixAllIssues = callbacks.onFixAllIssues;
    this.onRevealIssue = callbacks.onRevealIssue;
    this.onRunScan = callbacks.onRunScan;
  }
  hasResult() {
    return this.model.result !== null;
  }
  getResult() {
    return this.model.result;
  }
  // ─── Render ──────────────────────────────────────────────
  render() {
    const container = this.containerEl.children[1];
    if (this.backToTopHandler) {
      container.removeEventListener("scroll", this.backToTopHandler);
      this.backToTopHandler = null;
    }
    container.empty();
    if (this.model.isScanning) {
      this.renderProgress(container);
      return;
    }
    if (!this.model.result) {
      const empty = container.createDiv({ cls: "vi-empty" });
      empty.createEl("p", { text: "No scan results yet." });
      const btn = empty.createEl("button", { cls: "vi-empty-btn", text: "Run scan now" });
      btn.addEventListener("click", () => {
        if (this.onRunScan) this.onRunScan();
      });
      empty.createEl("p", {
        cls: "vi-empty-hint",
        text: 'You can also click the shield icon in the left ribbon, or run "vault inspector: Run scan" from the command palette.'
      });
      return;
    }
    const filterView = this.getIssueFilterView();
    this.renderToolbar(container, filterView);
    renderSummary(container, this.model.result, {
      issues: filterView.visibleIssues,
      onFilterSeverity: (severity) => {
        this.model.filterSeverity = this.model.filterSeverity === severity ? null : severity;
        this.render();
      }
    });
    if (this.model.selectionMode) {
      this.renderMainActionBar(container);
    }
    const issuesContainer = container.createDiv({ cls: "vi-issues" });
    renderIssueList(issuesContainer, {
      issues: filterView.visibleIssues,
      scannersRun: this.model.result.scannersRun,
      selectionMode: this.model.selectionMode,
      selectedFingerprints: this.model.selectedFingerprints,
      onOpenIssue: (issue) => {
        void this.handleOpenIssue(issue);
      },
      onToggleSelect: (issue) => this.handleToggleSelect(issue)
    });
    this.renderIgnoredSection(container);
    this.addBackToTop(container);
  }
  renderProgress(container) {
    var _a, _b, _c;
    const progress = this.model.scanProgress;
    const startedAt = (_a = this.model.scanStartedAt) != null ? _a : Date.now();
    const elapsedMs = Date.now() - startedAt;
    const scannerIndex = (_b = progress == null ? void 0 : progress.scannerIndex) != null ? _b : 0;
    const scannerTotal = (_c = progress == null ? void 0 : progress.scannerTotal) != null ? _c : 0;
    const percent = scannerTotal > 0 ? Math.max(0, Math.min(100, Math.round(scannerIndex / scannerTotal * 100))) : 0;
    const panel = container.createDiv({ cls: "vi-progress-panel" });
    panel.createEl("h2", { text: "Scanning vault" });
    const bar = panel.createDiv({ cls: "vi-progress-bar", attr: { "aria-label": "Scan progress" } });
    bar.createDiv({ cls: "vi-progress-bar-fill", attr: { style: `width: ${percent}%` } });
    panel.createDiv({
      cls: "vi-progress-meta",
      text: scannerTotal > 0 ? `${scannerIndex} / ${scannerTotal} scanners` : "Preparing scan..."
    });
    const current = panel.createDiv({ cls: "vi-progress-current" });
    const scannerLabel = progress ? SCANNER_LABELS[progress.scannerId] : "Preparing scan";
    current.createDiv({ cls: "vi-progress-label", text: "Current" });
    current.createDiv({ cls: "vi-progress-value", text: scannerLabel });
    const detailText = this.formatProgressDetail(progress);
    if (detailText) {
      const detail = panel.createDiv({ cls: "vi-progress-detail" });
      detail.createSpan({ text: detailText });
    }
    panel.createDiv({
      cls: "vi-progress-elapsed",
      text: `Elapsed: ${formatDuration(elapsedMs)}`
    });
  }
  formatProgressDetail(progress) {
    if (!progress) return "";
    if (progress.type === "scanner-skipped") {
      return progress.message ? `Skipped: ${progress.message}` : "Skipped";
    }
    if (progress.type === "scanner-complete") return "Completed";
    const parts = [];
    if (progress.phase) {
      if (typeof progress.current === "number" && typeof progress.total === "number") {
        parts.push(`${progress.phase}: ${progress.current} / ${progress.total}`);
      } else {
        parts.push(progress.phase);
      }
    } else if (progress.type === "scanner-start") {
      parts.push("Scanning...");
    }
    if (progress.message) parts.push(progress.message);
    return parts.join(" \xB7 ");
  }
  startScanTimer() {
    if (this.scanTimer) return;
    this.scanTimer = window.setInterval(() => {
      if (this.model.isScanning) this.render();
    }, 1e3);
  }
  stopScanTimer() {
    if (!this.scanTimer) return;
    window.clearInterval(this.scanTimer);
    this.scanTimer = null;
  }
  // ─── Toolbar ─────────────────────────────────────────────
  renderToolbar(container, filterView) {
    const toolbar = container.createDiv({ cls: "vi-toolbar" });
    this.renderScannerFilter(toolbar, filterView);
    this.renderSeverityFilter(toolbar, filterView);
    if (filterView.visibleIssues.length > 0) {
      const selectBtn = toolbar.createEl("button", {
        cls: `vi-filter-btn vi-select-btn ${this.model.selectionMode ? "vi-active" : ""}`,
        text: this.model.selectionMode ? "Done" : "Select"
      });
      (0, import_obsidian3.setTooltip)(selectBtn, this.model.selectionMode ? "Exit selection mode" : "Enter selection mode");
      selectBtn.addEventListener("click", () => {
        this.model.selectionMode = !this.model.selectionMode;
        if (!this.model.selectionMode) this.model.selectedFingerprints = /* @__PURE__ */ new Set();
        this.render();
      });
    }
  }
  renderScannerFilter(toolbar, filterView) {
    var _a;
    if (!this.model.result) return;
    const group = toolbar.createDiv({ cls: "vi-filter-group" });
    group.createEl("button", {
      cls: `vi-filter-btn ${this.model.filterScanner === null ? "vi-active" : ""}`,
      text: "All"
    }).addEventListener("click", () => {
      this.model.filterScanner = null;
      this.render();
    });
    for (const scannerId of this.model.result.scannersRun) {
      const count = (_a = filterView.scannerCounts.get(scannerId)) != null ? _a : 0;
      group.createEl("button", {
        cls: `vi-filter-btn ${this.model.filterScanner === scannerId ? "vi-active" : ""}`,
        text: `${SCANNER_LABELS[scannerId]} (${count})`
      }).addEventListener("click", () => {
        this.model.filterScanner = this.model.filterScanner === scannerId ? null : scannerId;
        this.render();
      });
    }
  }
  renderSeverityFilter(toolbar, filterView) {
    if (!this.model.result) return;
    const group = toolbar.createDiv({ cls: "vi-filter-group" });
    for (const { severity, count } of filterView.severityFacets) {
      group.createEl("button", {
        cls: `vi-filter-btn vi-severity-${severity} ${this.model.filterSeverity === severity ? "vi-active" : ""}`,
        text: `${severity} (${count})`
      }).addEventListener("click", () => {
        this.model.filterSeverity = this.model.filterSeverity === severity ? null : severity;
        this.render();
      });
    }
  }
  // ─── Main Action Bar ─────────────────────────────────────
  renderMainActionBar(container) {
    if (!this.model.result) return;
    const visibleIssues = this.getVisibleIssues();
    const selectedIssues = visibleIssues.filter((i) => this.model.selectedFingerprints.has(i.fingerprint));
    const selectedFixable = selectedIssues.filter((i) => i.fixAction);
    const bar = container.createDiv({ cls: "vi-action-bar" });
    const left = bar.createDiv({ cls: "vi-action-bar-left" });
    const right = bar.createDiv({ cls: "vi-action-bar-right" });
    const allSelected = visibleIssues.length > 0 && visibleIssues.every((i) => this.model.selectedFingerprints.has(i.fingerprint));
    const toggleAll = left.createEl("input", { cls: "vi-issue-checkbox", type: "checkbox" });
    toggleAll.checked = allSelected;
    (0, import_obsidian3.setTooltip)(toggleAll, allSelected ? "Deselect all" : "Select all");
    toggleAll.addEventListener("click", () => {
      if (allSelected) {
        this.model.selectedFingerprints = /* @__PURE__ */ new Set();
      } else {
        for (const issue of visibleIssues) this.model.selectedFingerprints.add(issue.fingerprint);
      }
      this.render();
    });
    if (this.model.enableFixActions && selectedFixable.length > 0) {
      const fixBtn = right.createEl("button", { cls: "vi-action-btn vi-action-delete" });
      const actionKinds = new Set(selectedFixable.map((issue) => issue.fixAction.kind));
      (0, import_obsidian4.setIcon)(
        fixBtn,
        actionKinds.size > 1 ? "wrench" : actionKinds.has("remove-link-text") ? "pencil" : "trash-2"
      );
      fixBtn.createSpan({ text: `(${selectedFixable.length})` });
      (0, import_obsidian3.setTooltip)(
        fixBtn,
        describeFixActions(selectedFixable.map((issue) => issue.fixAction))
      );
      fixBtn.addEventListener("click", () => {
        if (this.onFixAllIssues) void this.onFixAllIssues(selectedFixable);
      });
    }
    if (selectedIssues.length > 0) {
      const ignoreBtn = right.createEl("button", { cls: "vi-action-btn vi-action-ignore" });
      (0, import_obsidian4.setIcon)(ignoreBtn, "eye-off");
      ignoreBtn.createSpan({ text: `(${selectedIssues.length})` });
      (0, import_obsidian3.setTooltip)(ignoreBtn, "Hide selected issues from future scans");
      ignoreBtn.addEventListener("click", () => {
        if (this.onIgnoreAllIssues) void this.onIgnoreAllIssues(selectedIssues);
      });
    }
    const cancelBtn = right.createEl("button", { cls: "vi-action-btn" });
    (0, import_obsidian4.setIcon)(cancelBtn, "x");
    (0, import_obsidian3.setTooltip)(cancelBtn, "Exit selection mode");
    cancelBtn.addEventListener("click", () => {
      this.model.selectionMode = false;
      this.model.selectedFingerprints = /* @__PURE__ */ new Set();
      this.render();
    });
  }
  // ─── Ignored Section ─────────────────────────────────────
  renderIgnoredSection(container) {
    if (!this.model.result) return;
    const ignoredIssues = this.model.result.ignoredIssues;
    if (ignoredIssues.length === 0) return;
    const section = container.createDiv({ cls: "vi-ignored-section" });
    const header = section.createDiv({ cls: "vi-ignored-header" });
    const headerLeft = header.createDiv({ cls: "vi-ignored-header-left" });
    const chevron = headerLeft.createSpan({ cls: "vi-ignored-chevron" });
    (0, import_obsidian4.setIcon)(chevron, this.model.ignoredExpanded ? "chevron-down" : "chevron-right");
    headerLeft.createSpan({ text: `Ignored items (${ignoredIssues.length})` });
    headerLeft.addEventListener("click", () => {
      this.model.ignoredExpanded = !this.model.ignoredExpanded;
      if (!this.model.ignoredExpanded) {
        this.model.ignoredSelectionMode = false;
        this.model.ignoredSelectedFingerprints = /* @__PURE__ */ new Set();
      }
      this.render();
    });
    if (this.model.ignoredExpanded) {
      const selectBtn = header.createEl("button", {
        cls: `vi-filter-btn vi-select-btn ${this.model.ignoredSelectionMode ? "vi-active" : ""}`,
        text: this.model.ignoredSelectionMode ? "Done" : "Select"
      });
      (0, import_obsidian3.setTooltip)(selectBtn, this.model.ignoredSelectionMode ? "Exit selection mode" : "Select to restore");
      selectBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        this.model.ignoredSelectionMode = !this.model.ignoredSelectionMode;
        if (!this.model.ignoredSelectionMode) this.model.ignoredSelectedFingerprints = /* @__PURE__ */ new Set();
        this.render();
      });
    }
    if (!this.model.ignoredExpanded) return;
    const body = section.createDiv({ cls: "vi-ignored-body" });
    if (this.model.ignoredSelectionMode) {
      this.renderIgnoredActionBar(body, ignoredIssues);
    }
    const listContainer = body.createDiv({ cls: "vi-ignored-list" });
    renderIssueList(listContainer, {
      issues: ignoredIssues,
      scannersRun: this.model.result.scannersRun,
      selectionMode: this.model.ignoredSelectionMode,
      selectedFingerprints: this.model.ignoredSelectedFingerprints,
      onOpenIssue: (issue) => {
        void this.handleOpenIssue(issue);
      },
      onToggleSelect: (issue) => this.handleIgnoredToggleSelect(issue)
    });
  }
  renderIgnoredActionBar(container, ignoredIssues) {
    const selectedIssues = ignoredIssues.filter((i) => this.model.ignoredSelectedFingerprints.has(i.fingerprint));
    const bar = container.createDiv({ cls: "vi-action-bar" });
    const left = bar.createDiv({ cls: "vi-action-bar-left" });
    const right = bar.createDiv({ cls: "vi-action-bar-right" });
    const allSelected = ignoredIssues.length > 0 && ignoredIssues.every((i) => this.model.ignoredSelectedFingerprints.has(i.fingerprint));
    const toggleAll = left.createEl("input", { cls: "vi-issue-checkbox", type: "checkbox" });
    toggleAll.checked = allSelected;
    (0, import_obsidian3.setTooltip)(toggleAll, allSelected ? "Deselect all" : "Select all");
    toggleAll.addEventListener("click", () => {
      if (allSelected) {
        this.model.ignoredSelectedFingerprints = /* @__PURE__ */ new Set();
      } else {
        for (const issue of ignoredIssues) this.model.ignoredSelectedFingerprints.add(issue.fingerprint);
      }
      this.render();
    });
    if (selectedIssues.length > 0) {
      const restoreBtn = right.createEl("button", { cls: "vi-action-btn" });
      (0, import_obsidian4.setIcon)(restoreBtn, "eye");
      restoreBtn.createSpan({ text: `(${selectedIssues.length})` });
      (0, import_obsidian3.setTooltip)(restoreBtn, "Stop ignoring selected issues");
      restoreBtn.addEventListener("click", () => {
        if (this.onRestoreIssues) void this.onRestoreIssues(selectedIssues);
      });
    }
    const cancelBtn = right.createEl("button", { cls: "vi-action-btn" });
    (0, import_obsidian4.setIcon)(cancelBtn, "x");
    (0, import_obsidian3.setTooltip)(cancelBtn, "Exit selection mode");
    cancelBtn.addEventListener("click", () => {
      this.model.ignoredSelectionMode = false;
      this.model.ignoredSelectedFingerprints = /* @__PURE__ */ new Set();
      this.render();
    });
  }
  // ─── Helpers ─────────────────────────────────────────────
  addBackToTop(container) {
    const anchor = container.createDiv({ cls: "vi-back-to-top-anchor" });
    const btn = anchor.createEl("button", { cls: "vi-back-to-top" });
    (0, import_obsidian4.setIcon)(btn, "arrow-up");
    (0, import_obsidian3.setTooltip)(btn, "Back to top");
    btn.addEventListener("click", () => {
      container.scrollTo({ top: 0, behavior: "smooth" });
    });
    const updateVisibility = () => {
      btn.style.display = container.scrollTop > 200 ? "" : "none";
    };
    container.addEventListener("scroll", updateVisibility);
    this.backToTopHandler = updateVisibility;
    updateVisibility();
  }
  getVisibleIssues() {
    return this.getIssueFilterView().visibleIssues;
  }
  getIssueFilterView() {
    var _a, _b;
    return buildIssueFilterView((_b = (_a = this.model.result) == null ? void 0 : _a.issues) != null ? _b : [], {
      scanner: this.model.filterScanner,
      severity: this.model.filterSeverity
    });
  }
  async handleOpenIssue(issue) {
    if (this.onRevealIssue) {
      void this.onRevealIssue(issue);
      return;
    }
    await this.revealIssue(issue);
  }
  async revealIssue(issue) {
    var _a;
    const path = (_a = issue.primaryPath) != null ? _a : issue.relatedPaths[0];
    if (!path) return;
    const file = this.app.vault.getAbstractFileByPath(path);
    if (!(file instanceof import_obsidian3.TFile)) return;
    const leaf = this.app.workspace.getLeaf(false);
    await leaf.openFile(file, { active: true });
    const targets = getLocationTargets(issue);
    if (targets.length === 0) return;
    const content = await this.app.vault.cachedRead(file);
    const position = findFirstTextPosition(content, targets);
    if (!position) return;
    const view = this.app.workspace.getActiveViewOfType(import_obsidian3.MarkdownView);
    const editor = view == null ? void 0 : view.editor;
    if (!editor) return;
    editor.setCursor(position);
    editor.scrollIntoView({ from: position, to: position }, true);
    editor.focus();
  }
  handleToggleSelect(issue) {
    if (this.model.selectedFingerprints.has(issue.fingerprint)) {
      this.model.selectedFingerprints.delete(issue.fingerprint);
    } else {
      this.model.selectedFingerprints.add(issue.fingerprint);
    }
    this.render();
  }
  handleIgnoredToggleSelect(issue) {
    if (this.model.ignoredSelectedFingerprints.has(issue.fingerprint)) {
      this.model.ignoredSelectedFingerprints.delete(issue.fingerprint);
    } else {
      this.model.ignoredSelectedFingerprints.add(issue.fingerprint);
    }
    this.render();
  }
};

// src/scanner/ScanRunner.ts
function getEffectiveIgnoredFolders(globalFolders, scannerFolders) {
  return [.../* @__PURE__ */ new Set([...globalFolders, ...scannerFolders])];
}
var ScanRunner = class {
  constructor(requestUrl2, timers) {
    this.requestUrl = requestUrl2;
    this.timers = timers;
    this.scanners = [];
  }
  register(scanner) {
    this.scanners.push(scanner);
  }
  async run(app, settings, options = {}) {
    var _a, _b, _c;
    const startedAt = Date.now();
    const markdownFiles = app.vault.getMarkdownFiles();
    const allFiles = app.vault.getFiles();
    const filePathIndex = new Set(allFiles.map((f) => f.path));
    const ctx = {
      app,
      metadataCache: app.metadataCache,
      vault: app.vault,
      requestUrl: this.requestUrl,
      setTimeout: (_a = this.timers) == null ? void 0 : _a.setTimeout,
      clearTimeout: (_b = this.timers) == null ? void 0 : _b.clearTimeout,
      markdownFiles,
      allFiles,
      filePathIndex,
      enabledScanners: new Set(
        Object.entries(settings.enabledScanners).filter(([, enabled]) => enabled).map(([id]) => id)
      ),
      ignoredFingerprints: new Set(settings.ignoredIssueFingerprints),
      largeMarkdownBytes: settings.largeMarkdownBytes,
      largeAttachmentBytes: settings.largeAttachmentBytes,
      ignoredLargeMarkdownFrontmatterKeys: settings.ignoredLargeMarkdownFrontmatterKeys,
      ignoredLargeMarkdownPathPatterns: settings.ignoredLargeMarkdownPathPatterns,
      duplicateHashMaxBytes: settings.duplicateHashMaxBytes,
      lowUsageTagThreshold: settings.lowUsageTagThreshold,
      watchedTags: settings.watchedTags,
      ignoredFolders: settings.ignoredFolders,
      ignoredProperties: settings.ignoredProperties,
      emptyNoteWordThreshold: settings.emptyNoteWordThreshold
    };
    const scannersRun = [];
    const issues = [];
    const ignoredIssues = [];
    for (let index = 0; index < this.scanners.length; index++) {
      const scanner = this.scanners[index];
      const scannerIndex = index + 1;
      const scannerTotal = this.scanners.length;
      const emitProgress = (type, message) => {
        var _a2;
        (_a2 = options.onProgress) == null ? void 0 : _a2.call(options, {
          type,
          scannerId: scanner.id,
          scannerIndex,
          scannerTotal,
          message,
          elapsedMs: Date.now() - startedAt
        });
      };
      if (!ctx.enabledScanners.has(scanner.id)) {
        emitProgress("scanner-skipped", "disabled");
        continue;
      }
      scannersRun.push(scanner.id);
      emitProgress("scanner-start");
      const scannerContext = {
        ...ctx,
        ignoredFolders: getEffectiveIgnoredFolders(
          settings.ignoredFolders,
          (_c = settings.ignoredFoldersByScanner[scanner.id]) != null ? _c : []
        )
      };
      const result = await scanner.scan(scannerContext, (progress) => {
        var _a2;
        (_a2 = options.onProgress) == null ? void 0 : _a2.call(options, {
          ...progress,
          scannerId: scanner.id,
          scannerIndex,
          scannerTotal,
          elapsedMs: Date.now() - startedAt
        });
      });
      for (const issue of result) {
        if (ctx.ignoredFingerprints.has(issue.fingerprint)) {
          ignoredIssues.push(issue);
        } else {
          issues.push(issue);
        }
      }
      emitProgress("scanner-complete");
    }
    return {
      startedAt,
      finishedAt: Date.now(),
      issues,
      ignoredIssues,
      filesScanned: allFiles.length,
      scannersRun
    };
  }
};

// src/scanner/issue-fingerprint.ts
function generateFingerprint(scannerId, primaryPath, evidence) {
  const stableEvidence = Object.keys(evidence).sort().map((k) => `${k}=${evidence[k]}`).join("&");
  const raw = `${scannerId}:${primaryPath != null ? primaryPath : ""}:${stableEvidence}`;
  return hashString(raw);
}
function hashString(str) {
  let h1 = 2166136261;
  let h2 = 16777619;
  for (let i = 0; i < str.length; i++) {
    const c = str.charCodeAt(i);
    h1 = (h1 << 5) - h1 + c | 0;
    h2 = (h2 << 5) - h2 + c | 0;
  }
  return (h1 >>> 0).toString(36) + (h2 >>> 0).toString(36);
}

// src/utils/paths.ts
function normalizePath(path) {
  return path.replace(/\\/g, "/").replace(/\/+$/, "");
}
function getExtension(path) {
  const normalized = normalizePath(path);
  const dotIndex = normalized.lastIndexOf(".");
  if (dotIndex === -1 || dotIndex < normalized.lastIndexOf("/")) return "";
  return normalized.slice(dotIndex + 1).toLowerCase();
}
function getBasename(path) {
  const normalized = normalizePath(path);
  const slashIndex = normalized.lastIndexOf("/");
  const name = slashIndex === -1 ? normalized : normalized.slice(slashIndex + 1);
  const dotIndex = name.lastIndexOf(".");
  return dotIndex === -1 ? name : name.slice(0, dotIndex);
}
function isInFolder(path, folder) {
  const normalized = normalizePath(path);
  const normalizedFolder = normalizePath(folder).replace(/\/+$/, "");
  return normalized === normalizedFolder || normalized.startsWith(normalizedFolder + "/");
}
function isIgnoredPath(path, ignoredFolders) {
  return ignoredFolders.some((folder) => isInFolder(path, folder));
}
function matchesGlob(path, glob) {
  const globstarSlashPlaceholder = "__VI_GLOBSTAR_SLASH__";
  const globstarPlaceholder = "__VI_GLOBSTAR__";
  const escaped = glob.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*\*\//g, globstarSlashPlaceholder).replace(/\*\*/g, globstarPlaceholder).replace(/\*/g, "[^/]*");
  const pattern = escaped.split(globstarSlashPlaceholder).join("(?:.*/)?").split(globstarPlaceholder).join(".*");
  return new RegExp(`^${pattern}$`).test(path);
}

// src/utils/vault-links.ts
var indexCache = /* @__PURE__ */ new WeakMap();
function getLinkTarget(linkText) {
  return normalizePath(linkText.split("|")[0].split("#")[0].trim());
}
function resolveVaultLinkTargets(ctx, linkText, sourcePath) {
  var _a, _b;
  const target = getLinkTarget(linkText);
  if (!target || hasUriScheme(target)) return [];
  const extension = getExtension(target);
  const relativeTarget = sourcePath && /^\.{1,2}\//.test(target) ? resolveRelativePath(sourcePath, target) : null;
  const sourceFolderTarget = sourcePath && !target.includes("/") ? resolveRelativePath(sourcePath, `./${target}`) : null;
  const candidateTargets = relativeTarget ? [relativeTarget] : sourceFolderTarget ? [sourceFolderTarget, target] : [target];
  const exactCandidates = candidateTargets.flatMap(
    (candidate) => extension ? [candidate] : [candidate, `${candidate}.md`]
  );
  for (const candidate of exactCandidates) {
    if (ctx.filePathIndex.has(candidate)) return [candidate];
  }
  if (target.includes("/")) return [];
  const indexes = getLinkIndexes(ctx);
  if (extension) {
    return ((_a = indexes.fileNameToPaths.get(target)) != null ? _a : []).slice(0, 1);
  }
  return ((_b = indexes.markdownBaseToPaths.get(target)) != null ? _b : []).slice(0, 1);
}
function hasUriScheme(text) {
  return /^[a-z][a-z\d+.-]*:/i.test(text);
}
function resolveRelativePath(sourcePath, target) {
  const segments = normalizePath(sourcePath).split("/");
  segments.pop();
  for (const segment of normalizePath(target).split("/")) {
    if (!segment || segment === ".") continue;
    if (segment === "..") {
      segments.pop();
    } else {
      segments.push(segment);
    }
  }
  return segments.join("/");
}
function getLinkIndexes(ctx) {
  var _a, _b;
  const cached = indexCache.get(ctx);
  if (cached) return cached;
  const fileNameToPaths = /* @__PURE__ */ new Map();
  for (const file of ctx.allFiles) {
    const normalizedPath = normalizePath(file.path);
    const fileName = normalizedPath.split("/").pop();
    if (!fileName) continue;
    const paths = (_a = fileNameToPaths.get(fileName)) != null ? _a : [];
    paths.push(file.path);
    fileNameToPaths.set(fileName, paths);
  }
  const markdownBaseToPaths = /* @__PURE__ */ new Map();
  for (const file of ctx.markdownFiles) {
    const baseName = getBasename(file.path);
    const paths = (_b = markdownBaseToPaths.get(baseName)) != null ? _b : [];
    paths.push(file.path);
    markdownBaseToPaths.set(baseName, paths);
  }
  for (const paths of fileNameToPaths.values()) paths.sort();
  for (const paths of markdownBaseToPaths.values()) paths.sort();
  const indexes = { fileNameToPaths, markdownBaseToPaths };
  indexCache.set(ctx, indexes);
  return indexes;
}

// src/scanner/scanners/broken-links.ts
var brokenLinksScanner = {
  id: "broken-links",
  scan(ctx) {
    var _a, _b, _c;
    const issues = [];
    const { markdownFiles, metadataCache } = ctx;
    for (const file of markdownFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      const cache = metadataCache.getFileCache(file);
      if (!cache) continue;
      const meta = metadataCache;
      const linksForFile = (_a = meta.unresolvedLinks) == null ? void 0 : _a[file.path];
      const references = [...(_b = cache.links) != null ? _b : [], ...(_c = cache.embeds) != null ? _c : []];
      const linkCandidates = /* @__PURE__ */ new Map();
      const addCandidate = (candidate) => {
        var _a2;
        const existing = linkCandidates.get(candidate.linkText);
        linkCandidates.set(candidate.linkText, {
          linkText: candidate.linkText,
          fixLinkText: (_a2 = existing == null ? void 0 : existing.fixLinkText) != null ? _a2 : candidate.fixLinkText
        });
      };
      for (const unresolvedLink of Object.keys(linksForFile != null ? linksForFile : {})) {
        const matchingReferences = references.filter(
          (reference) => reference.link === unresolvedLink
        );
        if (matchingReferences.length === 0) {
          addCandidate({ linkText: unresolvedLink });
          continue;
        }
        for (const reference of matchingReferences) {
          addCandidate(getLinkCandidate(reference));
        }
      }
      for (const reference of references) {
        if (reference.link.includes("#")) {
          addCandidate(getLinkCandidate(reference));
        }
      }
      for (const candidate of linkCandidates.values()) {
        issues.push(...resolveLinkIssues(
          ctx,
          file.path,
          candidate.linkText,
          candidate.fixLinkText
        ));
      }
    }
    return issues;
  }
};
function resolveLinkIssues(ctx, sourcePath, linkText, fixLinkText) {
  var _a;
  const issues = [];
  const rawTarget = getLinkTarget(linkText);
  if (!rawTarget || hasUriScheme(rawTarget)) return issues;
  if (isAttachmentLink(rawTarget)) {
    if (!findResolvedPath(ctx, rawTarget, sourcePath)) {
      issues.push(
        makeIssue(
          sourcePath,
          linkText,
          fixLinkText,
          rawTarget,
          "error",
          `Attachment not found: ${rawTarget}`
        )
      );
    }
    return issues;
  }
  const linkDestination = linkText.split("|")[0];
  const headingPart = linkDestination.includes("#") ? linkDestination.split("#").slice(1).join("#") : null;
  const resolvedPath = findMarkdownPath(ctx, rawTarget, sourcePath);
  if (!resolvedPath) {
    issues.push(
      makeIssue(
        sourcePath,
        linkText,
        fixLinkText,
        rawTarget,
        "error",
        `Linked file not found: ${rawTarget}`
      )
    );
    return issues;
  }
  if (headingPart) {
    const headingCache = ctx.metadataCache.getFileCache(
      ctx.markdownFiles.find((f) => f.path === resolvedPath)
    );
    const headings = (_a = headingCache == null ? void 0 : headingCache.headings) != null ? _a : [];
    const headingSlug = slugifyHeading(headingPart);
    const found = headings.some(
      (h) => slugifyHeading(h.heading) === headingSlug
    );
    if (!found) {
      issues.push(
        makeIssue(
          sourcePath,
          linkText,
          fixLinkText,
          resolvedPath,
          "warning",
          `Heading "#${headingPart}" not found in ${resolvedPath}`
        )
      );
    }
  }
  return issues;
}
function getLinkCandidate(reference) {
  var _a;
  const originalWikiLink = (_a = reference.original) == null ? void 0 : _a.match(/^!?\[\[([\s\S]+)\]\]$/);
  if (originalWikiLink) {
    return {
      linkText: originalWikiLink[1],
      fixLinkText: originalWikiLink[1]
    };
  }
  return { linkText: reference.link };
}
function isAttachmentLink(target) {
  var _a;
  const lastSegment = (_a = target.split("/").pop()) != null ? _a : "";
  const dotIndex = lastSegment.lastIndexOf(".");
  if (dotIndex === -1) return false;
  const ext = lastSegment.slice(dotIndex + 1).toLowerCase();
  return ext !== "md";
}
function findMarkdownPath(ctx, linkDestination, sourcePath) {
  const resolvedPath = findResolvedPath(ctx, linkDestination, sourcePath);
  return (resolvedPath == null ? void 0 : resolvedPath.endsWith(".md")) ? resolvedPath : null;
}
function findResolvedPath(ctx, linkDestination, sourcePath) {
  var _a, _b, _c;
  if (typeof ctx.metadataCache.getFirstLinkpathDest === "function") {
    return (_b = (_a = ctx.metadataCache.getFirstLinkpathDest(
      linkDestination,
      sourcePath
    )) == null ? void 0 : _a.path) != null ? _b : null;
  }
  return (_c = resolveVaultLinkTargets(
    ctx,
    linkDestination,
    sourcePath
  )[0]) != null ? _c : null;
}
function slugifyHeading(heading) {
  return heading.toLowerCase().trim().replace(/[^\p{L}\p{N}_\s-]/gu, "").replace(/\s+/g, "-");
}
function makeIssue(sourcePath, linkText, fixLinkText, targetPath, severity, message) {
  const issue = {
    scannerId: "broken-links",
    severity,
    title: "Broken link",
    message,
    primaryPath: sourcePath,
    relatedPaths: [targetPath],
    evidence: { link: linkText, target: targetPath },
    fingerprint: generateFingerprint("broken-links", sourcePath, {
      link: linkText,
      target: targetPath
    })
  };
  if (fixLinkText) {
    issue.fixAction = {
      kind: "remove-link-text",
      label: "Remove link",
      description: `Remove "[[${fixLinkText}]]" from "${sourcePath}"`,
      targetPaths: [sourcePath],
      linkText: fixLinkText
    };
  }
  return issue;
}

// src/utils/hash.ts
async function hashContent(content) {
  const hashBuffer = await crypto.subtle.digest("SHA-256", content);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

// src/scanner/scanners/duplicate-files.ts
var duplicateFilesScanner = {
  id: "duplicate-files",
  async scan(ctx) {
    var _a, _b, _c;
    const issues = [];
    const files = ctx.allFiles.filter(
      (f) => f.stat.size > 0 && !isIgnoredPath(f.path, ctx.ignoredFolders)
    );
    const nameGroups = /* @__PURE__ */ new Map();
    for (const file of files) {
      const key = `${getBasename(file.path)}.${getExtension(file.path)}`;
      const group = (_a = nameGroups.get(key)) != null ? _a : [];
      group.push(file);
      nameGroups.set(key, group);
    }
    const sizeGroups = /* @__PURE__ */ new Map();
    for (const file of files) {
      const group = (_b = sizeGroups.get(file.stat.size)) != null ? _b : [];
      group.push(file);
      sizeGroups.set(file.stat.size, group);
    }
    const candidates = /* @__PURE__ */ new Set();
    for (const [, group] of nameGroups) {
      if (group.length >= 2) group.forEach((f) => candidates.add(f));
    }
    for (const [, group] of sizeGroups) {
      if (group.length >= 2) group.forEach((f) => candidates.add(f));
    }
    const hashGroups = /* @__PURE__ */ new Map();
    for (const file of candidates) {
      if (file.stat.size <= ctx.duplicateHashMaxBytes) {
        try {
          const content = await ctx.vault.readBinary(file);
          const hash = await hashContent(content);
          const group = (_c = hashGroups.get(hash)) != null ? _c : [];
          group.push(file.path);
          hashGroups.set(hash, group);
        } catch (e) {
          continue;
        }
      }
    }
    const hashReportedPaths = /* @__PURE__ */ new Set();
    for (const [, paths] of hashGroups) {
      if (paths.length < 2) continue;
      paths.forEach((p) => hashReportedPaths.add(p));
      const sorted = paths.slice().sort();
      const kept = sorted[0];
      const duplicates = sorted.slice(1);
      issues.push({
        scannerId: "duplicate-files",
        severity: "warning",
        title: "Duplicate files (hash-identical)",
        message: `${paths.length} files have identical content`,
        relatedPaths: paths,
        evidence: {
          count: paths.length,
          paths: paths.join(", ")
        },
        fingerprint: generateFingerprint("duplicate-files", void 0, {
          paths: sorted.join(",")
        }),
        fixAction: {
          kind: "trash-file",
          label: "Delete duplicates",
          description: `Keep "${kept}" and move ${duplicates.length} duplicate(s) to trash`,
          targetPaths: duplicates,
          selection: {
            kind: "keep-one",
            candidatePaths: sorted,
            automaticKeepPath: kept
          }
        }
      });
    }
    for (const [name, group] of nameGroups) {
      if (group.length < 2) continue;
      const unreached = group.filter((f) => !hashReportedPaths.has(f.path));
      if (unreached.length < 2) continue;
      const paths = unreached.map((f) => f.path);
      issues.push({
        scannerId: "duplicate-files",
        severity: "info",
        title: "Duplicate file candidates (same name)",
        message: `${paths.length} files share the name "${name}"`,
        relatedPaths: paths,
        evidence: {
          count: paths.length,
          paths: paths.join(", ")
        },
        fingerprint: generateFingerprint("duplicate-files", void 0, {
          nameCandidates: paths.slice().sort().join(",")
        })
      });
    }
    for (const [size, group] of sizeGroups) {
      if (group.length < 2) continue;
      const unreached = group.filter((f) => !hashReportedPaths.has(f.path));
      if (unreached.length < 2) continue;
      const paths = unreached.map((f) => f.path);
      issues.push({
        scannerId: "duplicate-files",
        severity: "info",
        title: "Duplicate file candidates (same size)",
        message: `${paths.length} files share size ${formatSize(size)}`,
        relatedPaths: paths,
        evidence: {
          count: paths.length,
          size,
          paths: paths.join(", ")
        },
        fingerprint: generateFingerprint("duplicate-files", void 0, {
          sizeCandidates: paths.slice().sort().join(",")
        })
      });
    }
    return issues;
  }
};

// src/scanner/scanners/empty-notes.ts
var emptyNotesScanner = {
  id: "empty-notes",
  async scan(ctx) {
    const issues = [];
    for (const file of ctx.markdownFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      const content = await ctx.vault.cachedRead(file);
      const body = stripFrontmatterAndTitle(content);
      const wordCount = countWords(body);
      if (wordCount <= ctx.emptyNoteWordThreshold) {
        issues.push({
          scannerId: "empty-notes",
          severity: "warning",
          title: "Empty note",
          message: wordCount === 0 ? "This note has no content besides a title" : `This note only has ${wordCount} word${wordCount > 1 ? "s" : ""} (likely a stub)`,
          primaryPath: file.path,
          relatedPaths: [],
          evidence: { size: file.stat.size, wordCount },
          fingerprint: generateFingerprint("empty-notes", file.path, {}),
          fixAction: {
            kind: "trash-file",
            label: "Delete",
            description: `Move "${file.path}" to trash`,
            targetPaths: [file.path]
          }
        });
      }
    }
    return issues;
  }
};
function stripFrontmatterAndTitle(content) {
  let text = content;
  if (text.startsWith("---")) {
    const end = text.indexOf("\n---", 3);
    if (end !== -1) {
      text = text.slice(end + 4);
    }
  }
  text = text.replace(/^#+\s+.*$/m, "");
  return text;
}
function countWords(text) {
  let count = 0;
  const cjkPattern = /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/gu;
  for (const match of text.matchAll(cjkPattern)) {
    void match;
    count++;
  }
  const withoutCjk = text.replace(cjkPattern, " ");
  for (const segment of withoutCjk.split(/\s+/)) {
    if (segment.length > 0) count++;
  }
  return count;
}

// src/scanner/scanners/external-links.ts
var externalLinksScanner = {
  id: "external-links",
  async scan(ctx, onProgress) {
    const issues = [];
    const urlMap = await collectExternalUrls(ctx);
    const { results, skipped } = await checkUrls(urlMap, ctx, onProgress);
    for (const result of results) {
      const issue = makeIssue2(result);
      if (issue) issues.push(issue);
    }
    if (skipped > 0) {
      issues.push({
        scannerId: "external-links",
        severity: "info",
        title: "External link checks skipped",
        message: `Stopped after ${EXTERNAL_LINK_SCAN_BUDGET_MS / 1e3}s scan budget; ${skipped} URL(s) were not checked.`,
        relatedPaths: [],
        evidence: {
          skipped,
          budgetMs: EXTERNAL_LINK_SCAN_BUDGET_MS
        },
        fingerprint: generateFingerprint("external-links", void 0, {
          skipped,
          budgetMs: EXTERNAL_LINK_SCAN_BUDGET_MS
        })
      });
    }
    return issues;
  }
};
var EXTERNAL_LINK_TIMEOUT_MS = 5e3;
var EXTERNAL_LINK_SCAN_BUDGET_MS = 6e4;
var EXTERNAL_LINK_BATCH_SIZE = 5;
async function collectExternalUrls(ctx) {
  var _a, _b;
  const entries = [];
  const seen = /* @__PURE__ */ new Set();
  for (const file of ctx.markdownFiles) {
    if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
    const cache = ctx.metadataCache.getFileCache(file);
    if (!cache) continue;
    const links = (_a = cache.links) != null ? _a : [];
    const embeds = (_b = cache.embeds) != null ? _b : [];
    for (const link of [...links, ...embeds]) {
      const href = link.link;
      if (!isExternalUrl(href)) continue;
      if (seen.has(href)) continue;
      seen.add(href);
      entries.push({ url: href, sourcePath: file.path });
    }
    if (cache.frontmatter) {
      for (const value of Object.values(cache.frontmatter)) {
        if (typeof value === "string" && isExternalUrl(value)) {
          if (seen.has(value)) continue;
          seen.add(value);
          entries.push({ url: value, sourcePath: file.path });
        }
      }
    }
    try {
      const content = await ctx.vault.cachedRead(file);
      for (const url of extractBareUrls(content)) {
        if (seen.has(url)) continue;
        seen.add(url);
        entries.push({ url, sourcePath: file.path });
      }
    } catch (e) {
      continue;
    }
  }
  return entries;
}
function isExternalUrl(text) {
  return /^https?:\/\//i.test(text);
}
function extractBareUrls(content) {
  const urls = [];
  const seen = /* @__PURE__ */ new Set();
  const body = stripIgnoredMarkdownRegions(stripFrontmatter(content));
  const urlPattern = /https?:\/\/[^\s<>"']+/gi;
  for (const match of body.matchAll(urlPattern)) {
    const url = trimUrlBoundary(match[0]);
    if (!url || seen.has(url)) continue;
    seen.add(url);
    urls.push(url);
  }
  return urls;
}
function stripFrontmatter(content) {
  const match = /^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/.exec(content);
  return match ? content.slice(match[0].length) : content;
}
function stripIgnoredMarkdownRegions(content) {
  return content.replace(/<!--[\s\S]*?-->/g, "").replace(/^[ \t]*(`{3,}|~{3,})[^\r\n]*\r?\n[\s\S]*?^[ \t]*\1[^\r\n]*$/gm, "").replace(/(`+)[^\r\n]*?\1/g, "");
}
function trimUrlBoundary(url) {
  let trimmed = url;
  while (/[),.;:!?]$/.test(trimmed)) {
    trimmed = trimmed.slice(0, -1);
  }
  return trimmed;
}
async function checkUrls(urlMap, ctx, onProgress) {
  const results = [];
  const startedAt = Date.now();
  const deadline = startedAt + EXTERNAL_LINK_SCAN_BUDGET_MS;
  const stats = { timedOut: 0, failed: 0 };
  reportExternalProgress(onProgress, urlMap.length, results.length, stats);
  for (let i = 0; i < urlMap.length; i += EXTERNAL_LINK_BATCH_SIZE) {
    if (Date.now() >= deadline) {
      const skipped = urlMap.length - i;
      reportExternalProgress(onProgress, urlMap.length, results.length, stats, skipped);
      return { results, skipped };
    }
    const timeoutMs = Math.max(1, Math.min(EXTERNAL_LINK_TIMEOUT_MS, deadline - Date.now()));
    const batch = urlMap.slice(i, i + EXTERNAL_LINK_BATCH_SIZE);
    const checks = batch.map((entry) => checkUrlWithTimeout(entry, ctx, timeoutMs));
    const batchResults = await Promise.all(checks);
    for (const result of batchResults) {
      if (result.kind === "timeout") stats.timedOut++;
      if (result.kind === "failed") stats.failed++;
    }
    results.push(...batchResults);
    reportExternalProgress(onProgress, urlMap.length, results.length, stats);
  }
  return { results, skipped: 0 };
}
function reportExternalProgress(onProgress, total, current, stats, skipped = 0) {
  onProgress == null ? void 0 : onProgress({
    type: "scanner-progress",
    scannerId: "external-links",
    scannerIndex: 0,
    scannerTotal: 0,
    phase: "Checking URLs",
    current,
    total,
    message: `timed out ${stats.timedOut}, failed ${stats.failed}, skipped ${skipped}`,
    elapsedMs: 0
  });
}
async function checkUrlWithTimeout(entry, ctx, timeoutMs) {
  const controller = new AbortController();
  const result = await withTimeout(
    checkUrl(entry.url, ctx, controller.signal),
    timeoutMs,
    {
      ...entry,
      kind: "timeout",
      timeoutMs
    },
    ctx,
    () => controller.abort()
  );
  return withSourcePath(result, entry.sourcePath);
}
async function checkUrl(url, ctx, signal) {
  try {
    if (ctx == null ? void 0 : ctx.requestUrl) {
      const status = await ctx.requestUrl(url, signal);
      return { url, sourcePath: "", kind: "http", status };
    }
    return {
      url,
      sourcePath: "",
      kind: "failed",
      error: "No request adapter configured"
    };
  } catch (error) {
    return {
      url,
      sourcePath: "",
      kind: "failed",
      error: error instanceof Error ? error.message : String(error)
    };
  }
}
async function withTimeout(promise, timeoutMs, timeoutValue, ctx, onTimeout) {
  const timer = getTimer(ctx);
  let timeoutId;
  try {
    return await Promise.race([
      promise,
      new Promise((resolve) => {
        timeoutId = timer.setTimeout(() => {
          resolve(timeoutValue);
          onTimeout == null ? void 0 : onTimeout();
        }, timeoutMs);
      })
    ]);
  } finally {
    if (timeoutId) timer.clearTimeout(timeoutId);
  }
}
function getTimer(ctx) {
  var _a, _b;
  return {
    setTimeout: (_a = ctx == null ? void 0 : ctx.setTimeout) != null ? _a : ((callback, delayMs) => window.setTimeout(callback, delayMs)),
    clearTimeout: (_b = ctx == null ? void 0 : ctx.clearTimeout) != null ? _b : ((timeoutId) => window.clearTimeout(timeoutId))
  };
}
function makeIssue2(result) {
  if (result.kind === "http") {
    if (result.status < 400) return null;
    return {
      scannerId: "external-links",
      severity: "warning",
      title: "Dead external link",
      message: `HTTP ${result.status} \u2014 ${result.url}`,
      primaryPath: result.sourcePath,
      relatedPaths: [],
      evidence: {
        url: result.url,
        status: result.status
      },
      fingerprint: generateFingerprint("external-links", result.sourcePath, {
        url: result.url
      })
    };
  }
  if (result.kind === "timeout") {
    return {
      scannerId: "external-links",
      severity: "info",
      title: "External link check timed out",
      message: `No response after ${result.timeoutMs}ms \u2014 ${result.url}`,
      primaryPath: result.sourcePath,
      relatedPaths: [],
      evidence: {
        url: result.url,
        timeoutMs: result.timeoutMs
      },
      fingerprint: generateFingerprint("external-links", result.sourcePath, {
        url: result.url,
        timeout: true
      })
    };
  }
  return {
    scannerId: "external-links",
    severity: "info",
    title: "External link check failed",
    message: `Could not check URL \u2014 ${result.url}`,
    primaryPath: result.sourcePath,
    relatedPaths: [],
    evidence: {
      url: result.url,
      error: result.error
    },
    fingerprint: generateFingerprint("external-links", result.sourcePath, {
      url: result.url,
      failed: true
    })
  };
}
function withSourcePath(result, sourcePath) {
  if (result.kind === "http") {
    return { ...result, sourcePath };
  }
  if (result.kind === "timeout") {
    return { ...result, sourcePath };
  }
  return { ...result, sourcePath };
}

// src/utils/frontmatter-type.ts
function inferType(value) {
  if (value === null || value === void 0) return "null";
  if (Array.isArray(value)) return "array";
  if (typeof value === "string") {
    if (/^\d{4}-\d{2}-\d{2}/.test(value)) return "date";
    return "string";
  }
  if (typeof value === "number") return "number";
  if (typeof value === "boolean") return "boolean";
  return "string";
}
function typesAreCompatible(a, b) {
  if (a === b) return true;
  if (a === "null" || b === "null") return true;
  if (a === "date" && b === "string" || a === "string" && b === "date")
    return true;
  return false;
}

// src/scanner/scanners/frontmatter-types.ts
var frontmatterTypesScanner = {
  id: "frontmatter-types",
  scan(ctx) {
    var _a;
    const issues = [];
    const ignoredProps = new Set(ctx.ignoredProperties);
    const propertyTypes = /* @__PURE__ */ new Map();
    for (const file of ctx.markdownFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      const cache = ctx.metadataCache.getFileCache(file);
      const frontmatter = cache == null ? void 0 : cache.frontmatter;
      if (!frontmatter) continue;
      for (const [key, value] of Object.entries(frontmatter)) {
        if (key === "position") continue;
        if (ignoredProps.has(key)) continue;
        const type = inferType(value);
        let typeMap = propertyTypes.get(key);
        if (!typeMap) {
          typeMap = /* @__PURE__ */ new Map();
          propertyTypes.set(key, typeMap);
        }
        const paths = (_a = typeMap.get(type)) != null ? _a : [];
        paths.push(file.path);
        typeMap.set(type, paths);
      }
    }
    for (const [prop, typeMap] of propertyTypes) {
      const nonNullTypes = Array.from(typeMap.keys()).filter((t) => t !== "null");
      if (nonNullTypes.length <= 1) continue;
      let hasIncompatible = false;
      let hasDateAmbiguity = false;
      for (let i = 0; i < nonNullTypes.length - 1; i++) {
        for (let j = i + 1; j < nonNullTypes.length; j++) {
          if (!typesAreCompatible(nonNullTypes[i], nonNullTypes[j])) {
            hasIncompatible = true;
          }
          if (nonNullTypes[i] === "string" && nonNullTypes[j] === "date" || nonNullTypes[i] === "date" && nonNullTypes[j] === "string") {
            hasDateAmbiguity = true;
          }
        }
      }
      if (!hasIncompatible && !hasDateAmbiguity) continue;
      const severity = hasIncompatible ? "warning" : "info";
      const title = hasIncompatible ? "Frontmatter type drift" : "Frontmatter type ambiguity";
      const types = Array.from(typeMap.keys());
      const typeSummary = types.map((t) => {
        var _a2, _b;
        const count = (_b = (_a2 = typeMap.get(t)) == null ? void 0 : _a2.length) != null ? _b : 0;
        return `${t} (${count})`;
      }).join(", ");
      const allPaths = [];
      for (const paths of typeMap.values()) {
        allPaths.push(...paths);
      }
      issues.push({
        scannerId: "frontmatter-types",
        severity,
        title,
        message: `Property "${prop}" has mixed types: ${typeSummary}`,
        relatedPaths: allPaths.slice(0, 10),
        evidence: {
          property: prop,
          types: typeSummary,
          fileCount: allPaths.length
        },
        fingerprint: generateFingerprint("frontmatter-types", void 0, {
          property: prop,
          types: types.sort().join(",")
        })
      });
    }
    return issues;
  }
};

// src/utils/file-types.ts
var ATTACHMENT_EXTENSIONS = /* @__PURE__ */ new Set([
  "png",
  "jpg",
  "jpeg",
  "gif",
  "svg",
  "webp",
  "pdf",
  "mp3",
  "mp4",
  "wav",
  "mov",
  "zip"
]);
function isAttachment(path) {
  const ext = getExtension(path);
  return ext !== "" && ATTACHMENT_EXTENSIONS.has(ext);
}
function isMarkdown(path) {
  const ext = getExtension(path);
  return ext === "md";
}

// src/scanner/scanners/large-files.ts
var largeFilesScanner = {
  id: "large-files",
  scan(ctx) {
    const issues = [];
    for (const file of ctx.allFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      const isMd = isMarkdown(file.path);
      if (isMd && isIgnoredLargeMarkdown(file, ctx)) continue;
      const threshold = isMd ? ctx.largeMarkdownBytes : ctx.largeAttachmentBytes;
      if (file.stat.size > threshold) {
        issues.push({
          scannerId: "large-files",
          severity: "warning",
          title: "Large file",
          message: `File is ${formatSize(file.stat.size)}, exceeds ${formatSize(threshold)} threshold`,
          primaryPath: file.path,
          relatedPaths: [],
          evidence: {
            size: file.stat.size,
            threshold,
            type: isMd ? "markdown" : "attachment"
          },
          fingerprint: generateFingerprint("large-files", file.path, {
            type: isMd ? "markdown" : "attachment"
          })
        });
      }
    }
    issues.sort((a, b) => b.evidence.size - a.evidence.size);
    return issues;
  }
};
function isIgnoredLargeMarkdown(file, ctx) {
  var _a;
  if (ctx.ignoredLargeMarkdownPathPatterns.some(
    (pattern) => matchesGlob(file.path, pattern)
  )) {
    return true;
  }
  if (ctx.ignoredLargeMarkdownFrontmatterKeys.length === 0) return false;
  if (typeof ctx.metadataCache.getFileCache !== "function") return false;
  const frontmatter = (_a = ctx.metadataCache.getFileCache(file)) == null ? void 0 : _a.frontmatter;
  if (!frontmatter) return false;
  return ctx.ignoredLargeMarkdownFrontmatterKeys.some(
    (key) => Object.prototype.hasOwnProperty.call(frontmatter, key)
  );
}

// src/scanner/scanners/orphan-attachments.ts
var orphanAttachmentsScanner = {
  id: "orphan-attachments",
  scan(ctx) {
    const issues = [];
    const referencedPaths = collectReferencedPaths(ctx);
    for (const file of ctx.allFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      if (!isAttachment(file.path)) continue;
      if (!referencedPaths.has(file.path)) {
        const severity = isRecent(file.stat.mtime) ? "info" : "warning";
        issues.push({
          scannerId: "orphan-attachments",
          severity,
          title: "Orphan attachment",
          message: "This attachment is not referenced by any note",
          primaryPath: file.path,
          relatedPaths: [],
          evidence: {
            lastModified: file.stat.mtime
          },
          fingerprint: generateFingerprint("orphan-attachments", file.path, {
            orphan: true
          }),
          fixAction: {
            kind: "trash-file",
            label: "Delete",
            description: `Move "${file.path}" to trash`,
            targetPaths: [file.path]
          }
        });
      }
    }
    return issues;
  }
};
function collectReferencedPaths(ctx) {
  var _a, _b, _c, _d;
  const paths = /* @__PURE__ */ new Set();
  const canResolveLinks = typeof ctx.metadataCache.getFirstLinkpathDest === "function";
  for (const file of ctx.markdownFiles) {
    const cache = ctx.metadataCache.getFileCache(file);
    if (!cache) continue;
    const links = (_a = cache.links) != null ? _a : [];
    const embeds = (_b = cache.embeds) != null ? _b : [];
    const frontmatterLinks = (_c = cache.frontmatterLinks) != null ? _c : [];
    for (const link of [...links, ...embeds, ...frontmatterLinks]) {
      const resolvedTarget = canResolveLinks ? (_d = ctx.metadataCache.getFirstLinkpathDest(link.link, file.path)) == null ? void 0 : _d.path : resolveVaultLinkTargets(ctx, link.link, file.path)[0];
      if (resolvedTarget) paths.add(resolvedTarget);
    }
  }
  return paths;
}
function isRecent(mtime) {
  const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1e3;
  return mtime > oneWeekAgo;
}

// src/scanner/scanners/tag-usage.ts
var tagUsageScanner = {
  id: "tag-usage",
  scan(ctx) {
    var _a, _b, _c, _d;
    const issues = [];
    const tagCounts = /* @__PURE__ */ new Map();
    const tagPaths = /* @__PURE__ */ new Map();
    const watchedSet = new Set(ctx.watchedTags);
    for (const file of ctx.markdownFiles) {
      if (isIgnoredPath(file.path, ctx.ignoredFolders)) continue;
      const cache = ctx.metadataCache.getFileCache(file);
      if (!cache) continue;
      const tags = collectTags(cache);
      for (const tag of tags) {
        tagCounts.set(tag, ((_a = tagCounts.get(tag)) != null ? _a : 0) + 1);
        const paths = (_b = tagPaths.get(tag)) != null ? _b : /* @__PURE__ */ new Set();
        paths.add(file.path);
        tagPaths.set(tag, paths);
      }
    }
    for (const [tag, count] of tagCounts) {
      if (count >= ctx.lowUsageTagThreshold) continue;
      if (watchedSet.has(tag)) continue;
      const paths = Array.from((_c = tagPaths.get(tag)) != null ? _c : []).sort();
      issues.push({
        scannerId: "tag-usage",
        severity: "info",
        title: "Low-usage tag",
        message: `Tag "${tag}" is only used ${count} time(s), below threshold of ${ctx.lowUsageTagThreshold}`,
        primaryPath: paths[0],
        relatedPaths: paths.slice(1),
        evidence: { tag, count, threshold: ctx.lowUsageTagThreshold },
        fingerprint: generateFingerprint("tag-usage", void 0, {
          tag,
          lowUsage: true
        })
      });
    }
    for (const watchedTag of ctx.watchedTags) {
      const count = (_d = tagCounts.get(watchedTag)) != null ? _d : 0;
      if (count > 0) continue;
      issues.push({
        scannerId: "tag-usage",
        severity: "info",
        title: "Missing watched tag",
        message: `Watched tag "${watchedTag}" does not appear in the vault`,
        relatedPaths: [],
        evidence: { tag: watchedTag, count: 0, watched: true },
        fingerprint: generateFingerprint("tag-usage", void 0, {
          tag: watchedTag,
          watched: true
        })
      });
    }
    return issues;
  }
};
function collectTags(cache) {
  var _a;
  const tags = [];
  const frontmatterTags = (_a = cache.frontmatter) == null ? void 0 : _a.tags;
  if (frontmatterTags) {
    if (Array.isArray(frontmatterTags)) {
      for (const t of frontmatterTags) {
        tags.push(String(t).replace(/^#/, ""));
      }
    } else if (typeof frontmatterTags === "string" || typeof frontmatterTags === "number") {
      tags.push(String(frontmatterTags).replace(/^#/, ""));
    }
  }
  const inlineTags = cache.tags;
  if (inlineTags) {
    for (const t of inlineTags) {
      tags.push(t.tag.replace(/^#/, ""));
    }
  }
  return tags;
}

// src/scanner/register-scanners.ts
function registerDefaultScanners(scanRunner) {
  scanRunner.register(brokenLinksScanner);
  scanRunner.register(largeFilesScanner);
  scanRunner.register(orphanAttachmentsScanner);
  scanRunner.register(emptyNotesScanner);
  scanRunner.register(externalLinksScanner);
  scanRunner.register(duplicateFilesScanner);
  scanRunner.register(frontmatterTypesScanner);
  scanRunner.register(tagUsageScanner);
}

// src/settings/settings.ts
function createEmptyIgnoredFoldersByScanner() {
  const result = {};
  for (const id of SCANNER_IDS) {
    result[id] = [];
  }
  return result;
}
var DEFAULT_SETTINGS = {
  enabledScanners: Object.fromEntries(
    SCANNER_IDS.map((id) => [id, id !== "external-links"])
  ),
  enableFixActions: true,
  duplicateKeepMode: "always-ask",
  largeMarkdownBytes: 100 * 1024,
  largeAttachmentBytes: 5 * 1024 * 1024,
  ignoredLargeMarkdownFrontmatterKeys: ["excalidraw-plugin"],
  ignoredLargeMarkdownPathPatterns: [],
  duplicateHashMaxBytes: 1024 * 1024,
  lowUsageTagThreshold: 2,
  emptyNoteWordThreshold: 5,
  watchedTags: [],
  ignoredIssueFingerprints: [],
  ignoredFolders: [],
  ignoredFoldersByScanner: createEmptyIgnoredFoldersByScanner(),
  ignoredProperties: [],
  reportFolderPath: "Vault Inspector Reports"
};

// src/settings/settings-tab.ts
var import_obsidian5 = require("obsidian");
function parseFolderList(value) {
  return [...new Set(
    value.split(",").map((folder) => folder.trim()).filter(Boolean)
  )];
}
var InspectorSettingTab = class extends import_obsidian5.PluginSettingTab {
  constructor(app, plugin) {
    super(app, plugin);
    this.plugin = plugin;
  }
  getSettingDefinitions() {
    return this.getSections().map(({ heading, items }) => ({
      type: "group",
      heading,
      items: items.map(({ name, desc, render }) => ({
        name,
        ...desc === void 0 ? {} : { desc },
        render
      }))
    }));
  }
  display() {
    const { containerEl } = this;
    containerEl.empty();
    new import_obsidian5.Setting(containerEl).setName("Scanning").setHeading();
    for (const section of this.getSections()) {
      new import_obsidian5.Setting(containerEl).setName(section.heading).setHeading();
      for (const item of section.items) {
        const setting = new import_obsidian5.Setting(containerEl).setName(item.name);
        if (item.desc !== void 0) {
          setting.setDesc(item.desc);
        }
        item.render(setting);
      }
    }
  }
  getSections() {
    return [
      {
        heading: "Enabled scanners",
        items: SCANNER_IDS.map((id) => ({
          name: SCANNER_LABELS[id],
          ...id === "external-links" ? {
            desc: "Opt-in network check for HTTP/HTTPS urls. Can be slower and depends on external sites."
          } : {},
          render: (setting) => {
            setting.addToggle(
              (toggle) => toggle.setValue(this.plugin.settings.enabledScanners[id]).onChange(async (value) => {
                this.plugin.settings.enabledScanners[id] = value;
                await this.plugin.saveSettings();
              })
            );
          }
        }))
      },
      {
        heading: "Fix actions",
        items: [
          {
            name: "Enable fix actions",
            desc: "Show fix buttons for safe automatic actions, including editing notes and moving files to trash.",
            render: (setting) => {
              setting.addToggle(
                (toggle) => toggle.setValue(this.plugin.settings.enableFixActions).onChange(async (value) => {
                  this.plugin.settings.enableFixActions = value;
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Duplicate file keep mode",
            desc: "Always ask which hash-identical file to keep, or automatically keep the first vault-relative path in alphabetical order.",
            render: (setting) => {
              setting.addDropdown(
                (dropdown) => dropdown.addOption("always-ask", "Always ask").addOption("automatic", "Automatically choose").setValue(this.plugin.settings.duplicateKeepMode).onChange(async (value) => {
                  this.plugin.settings.duplicateKeepMode = value === "automatic" ? "automatic" : "always-ask";
                  await this.plugin.saveSettings();
                })
              );
            }
          }
        ]
      },
      {
        heading: "Thresholds",
        items: [
          {
            name: "Large Markdown threshold (kb)",
            render: (setting) => {
              setting.addSlider(
                (slider) => slider.setLimits(50, 1e3, 50).setValue(this.plugin.settings.largeMarkdownBytes / 1024).onChange(async (value) => {
                  this.plugin.settings.largeMarkdownBytes = value * 1024;
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Large attachment threshold (mb)",
            render: (setting) => {
              setting.addSlider(
                (slider) => slider.setLimits(1, 50, 1).setValue(this.plugin.settings.largeAttachmentBytes / (1024 * 1024)).onChange(async (value) => {
                  this.plugin.settings.largeAttachmentBytes = value * 1024 * 1024;
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Ignored large Markdown frontmatter keys",
            desc: "Markdown files with any of these frontmatter keys are excluded from large file checks.",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.ignoredLargeMarkdownFrontmatterKeys.join(", ")).setPlaceholder("Frontmatter keys to ignore").onChange(async (value) => {
                  this.plugin.settings.ignoredLargeMarkdownFrontmatterKeys = value.split(",").map((key) => key.trim()).filter(Boolean);
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Ignored large Markdown path patterns",
            desc: "Vault-relative glob patterns excluded from large Markdown checks.",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.ignoredLargeMarkdownPathPatterns.join(", ")).setPlaceholder("E.g. index/**/*.md, **/*.canvas.md").onChange(async (value) => {
                  this.plugin.settings.ignoredLargeMarkdownPathPatterns = value.split(",").map((pattern) => pattern.trim()).filter(Boolean);
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Duplicate hash cap (mb)",
            desc: "Files above this size are reported as candidates without content hashing.",
            render: (setting) => {
              setting.addSlider(
                (slider) => slider.setLimits(1, 10, 1).setValue(this.plugin.settings.duplicateHashMaxBytes / (1024 * 1024)).onChange(async (value) => {
                  this.plugin.settings.duplicateHashMaxBytes = value * 1024 * 1024;
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Empty note word threshold",
            desc: "Notes with this many words or fewer are flagged as empty/stub.",
            render: (setting) => {
              setting.addSlider(
                (slider) => slider.setLimits(0, 20, 1).setValue(this.plugin.settings.emptyNoteWordThreshold).onChange(async (value) => {
                  this.plugin.settings.emptyNoteWordThreshold = value;
                  await this.plugin.saveSettings();
                })
              );
            }
          }
        ]
      },
      {
        heading: "Tags",
        items: [
          {
            name: "Watched tags (comma-separated)",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.watchedTags.join(", ")).setPlaceholder("E.g. Todo, review, project").onChange(async (value) => {
                  this.plugin.settings.watchedTags = value.split(",").map((tag) => tag.trim()).filter(Boolean);
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Low usage tag threshold",
            render: (setting) => {
              setting.addSlider(
                (slider) => slider.setLimits(1, 10, 1).setValue(this.plugin.settings.lowUsageTagThreshold).onChange(async (value) => {
                  this.plugin.settings.lowUsageTagThreshold = value;
                  await this.plugin.saveSettings();
                })
              );
            }
          }
        ]
      },
      {
        heading: "Ignored items",
        items: [
          {
            name: "Ignored folders (comma-separated)",
            desc: "Files in these folders are excluded from every scanner.",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.ignoredFolders.join(", ")).setPlaceholder("E.g. Templates, archive").onChange(async (value) => {
                  this.plugin.settings.ignoredFolders = parseFolderList(value);
                  await this.plugin.saveSettings();
                })
              );
            }
          },
          {
            name: "Ignored frontmatter properties (comma-separated)",
            desc: "These properties are excluded from type consistency checks.",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.ignoredProperties.join(", ")).setPlaceholder("E.g. Cssclasses, aliases").onChange(async (value) => {
                  this.plugin.settings.ignoredProperties = value.split(",").map((property) => property.trim()).filter(Boolean);
                  await this.plugin.saveSettings();
                })
              );
            }
          }
        ]
      },
      {
        heading: "Scanner-specific ignored folders",
        items: SCANNER_IDS.map((id) => ({
          name: SCANNER_LABELS[id],
          desc: `Additional folders excluded only from ${SCANNER_LABELS[id]}.`,
          render: (setting) => {
            setting.addText(
              (text) => text.setValue(
                this.plugin.settings.ignoredFoldersByScanner[id].join(", ")
              ).setPlaceholder("E.g. Templates, archive").onChange(async (value) => {
                this.plugin.settings.ignoredFoldersByScanner[id] = parseFolderList(value);
                await this.plugin.saveSettings();
              })
            );
          }
        }))
      },
      {
        heading: "Export",
        items: [
          {
            name: "Report folder",
            desc: "Folder for exported Markdown reports.",
            render: (setting) => {
              setting.addText(
                (text) => text.setValue(this.plugin.settings.reportFolderPath).setPlaceholder("Inspector reports").onChange(async (value) => {
                  this.plugin.settings.reportFolderPath = value.trim() || "Inspector reports";
                  await this.plugin.saveSettings();
                })
              );
            }
          }
        ]
      }
    ];
  }
};

// src/report/markdown-export.ts
function generateMarkdownReport(result) {
  var _a, _b;
  const lines = [];
  const now = /* @__PURE__ */ new Date();
  lines.push(`# Vault Inspector Report`);
  lines.push(``);
  lines.push(`- **Date:** ${now.toLocaleString()}`);
  lines.push(`- **Files scanned:** ${result.filesScanned}`);
  lines.push(`- **Duration:** ${formatDuration(result.finishedAt - result.startedAt)}`);
  lines.push(`- **Scanners run:** ${result.scannersRun.length}`);
  lines.push(``);
  const errors = result.issues.filter((i) => i.severity === "error").length;
  const warnings = result.issues.filter((i) => i.severity === "warning").length;
  const infos = result.issues.filter((i) => i.severity === "info").length;
  lines.push(`## Summary`);
  lines.push(``);
  lines.push(`| Severity | Count |`);
  lines.push(`|---|---|`);
  lines.push(`| Total | ${result.issues.length} |`);
  lines.push(`| Errors | ${errors} |`);
  lines.push(`| Warnings | ${warnings} |`);
  lines.push(`| Info | ${infos} |`);
  lines.push(``);
  const grouped = groupByScanner2(result.issues);
  for (const scannerId of result.scannersRun) {
    const issues = (_a = grouped[scannerId]) != null ? _a : [];
    lines.push(`## ${SCANNER_LABELS[scannerId]} (${issues.length})`);
    lines.push(``);
    if (issues.length === 0) {
      lines.push(`No issues found.`);
      lines.push(``);
      continue;
    }
    for (const issue of issues) {
      lines.push(`### ${escapeMd(issue.title)}`);
      lines.push(``);
      lines.push(`- **Severity:** ${issue.severity}`);
      const location = (_b = issue.primaryPath) != null ? _b : issue.relatedPaths[0];
      if (location) lines.push(`- **Location:** \`${escapeInlineCode(location)}\``);
      lines.push(`- **Message:** ${escapeMd(issue.message)}`);
      for (const detail of getMarkdownDetails(issue)) {
        if ("value" in detail) {
          lines.push(`- **${detail.label}:** ${detail.value}`);
        } else {
          lines.push(`- **${detail.label}:**`);
          for (const item of detail.items) {
            lines.push(`  - ${item}`);
          }
        }
      }
      lines.push(``);
    }
  }
  return lines.join("\n");
}
function getMarkdownDetails(issue) {
  const details = [];
  const target = getIssueTarget2(issue);
  if (target) details.push({ label: getTargetLabel2(issue), value: formatCode(target) });
  if (issue.scannerId === "external-links") {
    const status = getNumber2(issue.evidence.status);
    const timeoutMs = getNumber2(issue.evidence.timeoutMs);
    const error = issue.evidence.error;
    if (status !== null) details.push({ label: "Status", value: String(status) });
    if (timeoutMs !== null) details.push({ label: "Timeout", value: `${timeoutMs}ms` });
    if (typeof error === "string") details.push({ label: "Error", value: escapeMd(error) });
  }
  if (issue.scannerId === "broken-links") {
    const link = issue.evidence.link;
    if (typeof link === "string") details.push({ label: "Link text", value: formatCode(link) });
  }
  if (issue.scannerId === "duplicate-files") {
    const count = getNumber2(issue.evidence.count);
    if (count !== null) details.push({ label: "Count", value: String(count) });
    const size = getNumber2(issue.evidence.size);
    if (size !== null) details.push({ label: "Size", value: formatSize(size) });
    const paths = getEvidencePaths2(issue);
    if (paths.length > 0) {
      details.push({
        label: "Files",
        items: paths.map((path) => formatCode(path))
      });
    }
  }
  if (issue.scannerId === "frontmatter-types") {
    const property = issue.evidence.property;
    const types = issue.evidence.types;
    const fileCount = getNumber2(issue.evidence.fileCount);
    if (typeof property === "string") details.push({ label: "Property", value: formatCode(property) });
    if (typeof types === "string") details.push({ label: "Types", value: escapeMd(types) });
    if (fileCount !== null) details.push({ label: "Files", value: String(fileCount) });
    if (issue.relatedPaths.length > 0) {
      details.push({
        label: "Samples",
        items: issue.relatedPaths.map((path) => formatCode(path))
      });
    }
  }
  if (issue.scannerId === "tag-usage") {
    const tag = issue.evidence.tag;
    const count = getNumber2(issue.evidence.count);
    const threshold = getNumber2(issue.evidence.threshold);
    if (typeof tag === "string") details.push({ label: "Tag", value: formatTag2(tag) });
    if (count !== null) details.push({ label: "Count", value: String(count) });
    if (threshold !== null) details.push({ label: "Threshold", value: String(threshold) });
    const paths = [issue.primaryPath, ...issue.relatedPaths].filter((path) => Boolean(path));
    if (paths.length > 0) {
      details.push({
        label: "Files",
        items: paths.map((path) => formatCode(path))
      });
    }
  }
  if (issue.scannerId === "large-files") {
    const size = getNumber2(issue.evidence.size);
    const threshold = getNumber2(issue.evidence.threshold);
    const type = issue.evidence.type;
    if (size !== null) details.push({ label: "Size", value: formatSize(size) });
    if (threshold !== null) details.push({ label: "Threshold", value: formatSize(threshold) });
    if (typeof type === "string") details.push({ label: "Type", value: escapeMd(type) });
  }
  if (issue.scannerId === "orphan-attachments") {
    const lastModified = getNumber2(issue.evidence.lastModified);
    if (lastModified !== null) {
      details.push({ label: "Modified", value: new Date(lastModified).toLocaleString() });
    }
  }
  if (issue.scannerId === "empty-notes") {
    const size = getNumber2(issue.evidence.size);
    if (size !== null) details.push({ label: "Size", value: formatSize(size) });
  }
  return details;
}
function getIssueTarget2(issue) {
  const url = issue.evidence.url;
  if (typeof url === "string") return url;
  const target = issue.evidence.target;
  if (typeof target === "string") return target;
  return null;
}
function getTargetLabel2(issue) {
  if (issue.scannerId === "external-links") return "URL";
  if (issue.scannerId === "broken-links") return "Target";
  return "Target";
}
function getEvidencePaths2(issue) {
  const paths = issue.evidence.paths;
  if (typeof paths !== "string") return issue.relatedPaths;
  return paths.split(",").map((path) => path.trim()).filter(Boolean);
}
function getNumber2(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}
function formatTag2(tag) {
  return tag.startsWith("#") ? tag : `#${tag}`;
}
function formatCode(text) {
  return `\`${escapeInlineCode(text)}\``;
}
function groupByScanner2(issues) {
  const groups = {};
  for (const issue of issues) {
    if (!groups[issue.scannerId]) groups[issue.scannerId] = [];
    groups[issue.scannerId].push(issue);
  }
  return groups;
}
function escapeMd(text) {
  return text.replace(/\|/g, "\\|").replace(/\n/g, " ");
}
function escapeInlineCode(text) {
  return text.replace(/`/g, "\\`");
}

// src/fix/fix-executor.ts
var import_obsidian6 = require("obsidian");
async function executeFixAction(app, action) {
  switch (action.kind) {
    case "trash-file":
      return trashFiles(app, action.targetPaths);
    case "remove-link-text":
      return removeLinkText(app, action.targetPaths[0], action.linkText);
    default:
      return 0;
  }
}
async function trashFiles(app, paths) {
  let count = 0;
  for (const path of paths) {
    const file = app.vault.getAbstractFileByPath(path);
    if (file) {
      await app.fileManager.trashFile(file);
      count++;
    }
  }
  return count;
}
async function removeLinkText(app, sourcePath, linkText) {
  const file = app.vault.getAbstractFileByPath(sourcePath);
  if (!(file instanceof import_obsidian6.TFile)) return 0;
  const content = await app.vault.read(file);
  const pattern = new RegExp(`!?\\[\\[${escapeRegex(linkText)}\\]\\]`, "g");
  const protectedRanges = findProtectedMarkdownRanges(content);
  let cursor = 0;
  let updated = "";
  let removed = false;
  for (const match of content.matchAll(pattern)) {
    const start = match.index;
    const end = start + match[0].length;
    if (protectedRanges.some((range) => start < range.end && end > range.start)) {
      continue;
    }
    updated += content.slice(cursor, start);
    cursor = end;
    removed = true;
  }
  if (removed) updated += content.slice(cursor);
  else updated = content;
  if (updated === content) return 0;
  await app.vault.modify(file, updated);
  return 1;
}
function findProtectedMarkdownRanges(content) {
  const ranges = [
    ...findFencedCodeRanges(content),
    ...findHtmlCommentRanges(content)
  ];
  ranges.push(...findInlineCodeRanges(content, ranges));
  return mergeRanges(ranges);
}
function findFencedCodeRanges(content) {
  const ranges = [];
  let lineStart = 0;
  let fence = null;
  while (lineStart < content.length) {
    const newline = content.indexOf("\n", lineStart);
    const lineEnd = newline === -1 ? content.length : newline + 1;
    const line = content.slice(lineStart, newline === -1 ? content.length : newline);
    if (fence) {
      const closingFence = new RegExp(
        `^ {0,3}${escapeRegex(fence.char)}{${fence.length},}[\\t ]*$`
      );
      if (closingFence.test(line)) {
        ranges.push({ start: fence.start, end: lineEnd });
        fence = null;
      }
    } else {
      const openingFence = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
      if (openingFence && (openingFence[1][0] === "~" || !openingFence[2].includes("`"))) {
        fence = {
          char: openingFence[1][0],
          length: openingFence[1].length,
          start: lineStart
        };
      }
    }
    lineStart = lineEnd;
  }
  if (fence) ranges.push({ start: fence.start, end: content.length });
  return ranges;
}
function findHtmlCommentRanges(content) {
  const ranges = [];
  let searchFrom = 0;
  while (searchFrom < content.length) {
    const start = content.indexOf("<!--", searchFrom);
    if (start === -1) break;
    const closing = content.indexOf("-->", start + 4);
    const end = closing === -1 ? content.length : closing + 3;
    ranges.push({ start, end });
    searchFrom = end;
  }
  return ranges;
}
function findInlineCodeRanges(content, excludedRanges) {
  const ranges = [];
  let index = 0;
  while (index < content.length) {
    if (content[index] !== "`" || containsIndex(excludedRanges, index)) {
      index++;
      continue;
    }
    const start = index;
    while (content[index] === "`") index++;
    const marker = content.slice(start, index);
    let closing = content.indexOf(marker, index);
    while (closing !== -1 && (content[closing - 1] === "`" || content[closing + marker.length] === "`" || containsIndex(excludedRanges, closing))) {
      closing = content.indexOf(marker, closing + marker.length);
    }
    if (closing === -1) continue;
    const end = closing + marker.length;
    ranges.push({ start, end });
    index = end;
  }
  return ranges;
}
function containsIndex(ranges, index) {
  return ranges.some((range) => index >= range.start && index < range.end);
}
function mergeRanges(ranges) {
  const sorted = [...ranges].sort((left, right) => left.start - right.start);
  const merged = [];
  for (const range of sorted) {
    const previous = merged[merged.length - 1];
    if (previous && range.start <= previous.end) {
      previous.end = Math.max(previous.end, range.end);
    } else {
      merged.push({ ...range });
    }
  }
  return merged;
}
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// src/main.ts
var VaultInspectorPlugin = class extends import_obsidian7.Plugin {
  constructor() {
    super(...arguments);
    this.settings = DEFAULT_SETTINGS;
    this.scanRunner = new ScanRunner(async (url) => {
      const response = await (0, import_obsidian7.requestUrl)({ url, method: "HEAD" });
      return response.status;
    }, {
      setTimeout: (callback, delayMs) => window.setTimeout(callback, delayMs),
      clearTimeout: (timeoutId) => window.clearTimeout(timeoutId)
    });
  }
  async onload() {
    await this.loadSettings();
    this.registerView(VIEW_TYPE_INSPECTOR, (leaf) => {
      const view = new InspectorView(leaf);
      this.configureView(view);
      return view;
    });
    this.addCommand({
      id: "run-scan",
      name: "Run scan",
      callback: () => this.runScan()
    });
    this.addCommand({
      id: "export-report",
      name: "Export report",
      callback: () => this.exportReport()
    });
    registerDefaultScanners(this.scanRunner);
    this.addSettingTab(new InspectorSettingTab(this.app, this));
    this.addRibbonIcon("shield-check", "Run scan", () => this.runScan());
  }
  onunload() {
  }
  async loadSettings() {
    var _a;
    const loaded = (_a = await this.loadData()) != null ? _a : {};
    this.settings = {
      ...DEFAULT_SETTINGS,
      ...loaded,
      enabledScanners: {
        ...DEFAULT_SETTINGS.enabledScanners,
        ...loaded.enabledScanners
      },
      ignoredFoldersByScanner: {
        ...createEmptyIgnoredFoldersByScanner(),
        ...loaded.ignoredFoldersByScanner
      }
    };
    if (migrateExcalidrawFrontmatterKey(this.settings, loaded)) {
      await this.saveSettings();
    }
  }
  async saveSettings() {
    await this.saveData(this.settings);
  }
  async runScan() {
    let leaf = this.app.workspace.getLeavesOfType(VIEW_TYPE_INSPECTOR)[0];
    if (!leaf) {
      const rightLeaf = this.app.workspace.getRightLeaf(false);
      if (!rightLeaf) return;
      leaf = rightLeaf;
      await leaf.setViewState({ type: VIEW_TYPE_INSPECTOR, active: true });
    }
    await this.app.workspace.revealLeaf(leaf);
    const view = leaf.view;
    this.configureView(view);
    await this.scanAndRender(view);
  }
  configureView(view) {
    view.setCallbacks({
      onIgnoreAllIssues: async (issues) => {
        for (const issue of issues) {
          this.settings.ignoredIssueFingerprints.push(issue.fingerprint);
        }
        await this.saveSettings();
        new import_obsidian7.Notice(`Ignored ${issues.length} issue(s)`);
        await this.scanAndRender(view);
      },
      onRestoreIssues: async (issues) => {
        const toRestore = new Set(issues.map((i) => i.fingerprint));
        this.settings.ignoredIssueFingerprints = this.settings.ignoredIssueFingerprints.filter(
          (fp) => !toRestore.has(fp)
        );
        await this.saveSettings();
        new import_obsidian7.Notice(`Restored ${issues.length} issue(s)`);
        await this.scanAndRender(view);
      },
      onFixAllIssues: async (issues) => {
        if (!issues.some((issue) => issue.fixAction)) return;
        const decisions = await showConfirmModal(
          this.app,
          issues,
          this.settings.duplicateKeepMode
        );
        if (!decisions) return;
        const decisionsByFingerprint = new Map(
          decisions.map((decision) => [decision.fingerprint, decision])
        );
        let fixed = 0;
        let skipped = 0;
        for (const issue of issues) {
          const decision = decisionsByFingerprint.get(issue.fingerprint);
          if (!decision) {
            skipped++;
            continue;
          }
          const freshResult = await this.scan(view);
          if (!freshResult) return;
          const freshIssue = freshResult.issues.find(
            (candidate) => candidate.fingerprint === issue.fingerprint
          );
          const freshAction = getFreshFixAction(issue, freshIssue, decision);
          if (!freshAction) {
            skipped++;
            continue;
          }
          try {
            fixed += await executeFixAction(this.app, freshAction);
          } catch (e) {
          }
        }
        new import_obsidian7.Notice(formatFixResultNotice(fixed, skipped));
        await this.scanAndRender(view);
      },
      onRevealIssue: async (issue) => {
        var _a;
        const path = (_a = issue.primaryPath) != null ? _a : issue.relatedPaths[0];
        if (!path) return;
        const file = this.app.vault.getAbstractFileByPath(path);
        if (file instanceof import_obsidian7.TFile) {
          await view.revealIssue(issue);
        } else {
          new import_obsidian7.Notice(`File not found: ${path}`);
        }
      },
      onRunScan: () => {
        void this.runScan();
      }
    });
    view.setEnableFixActions(this.settings.enableFixActions);
  }
  async scanAndRender(view) {
    const result = await this.scan(view);
    if (result) view.setResult(result);
  }
  async scan(view) {
    view.setScanning(true);
    try {
      return await this.scanRunner.run(this.app, this.settings, {
        onProgress: (progress) => view.setScanProgress(progress)
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      new import_obsidian7.Notice(`Vault Inspector scan failed: ${message}`);
      view.setScanning(false);
      return null;
    }
  }
  async exportReport() {
    var _a;
    const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_INSPECTOR);
    const view = (_a = leaves[0]) == null ? void 0 : _a.view;
    if (!view || !view.hasResult()) {
      new import_obsidian7.Notice("Run a scan first before exporting.");
      return;
    }
    const result = view.getResult();
    const report = generateMarkdownReport(result);
    const folder = this.settings.reportFolderPath;
    const now = /* @__PURE__ */ new Date();
    const filename = `Vault Inspector Report ${now.toISOString().replace(/[:.]/g, "-").slice(0, 19)}.md`;
    const filepath = `${folder}/${filename}`;
    await this.app.vault.createFolder(folder).catch(() => {
    });
    await this.app.vault.create(filepath, report);
    new import_obsidian7.Notice(`Report exported to ${filepath}`);
  }
};
function formatFixResultNotice(fixed, skipped) {
  const fixedText = fixed > 0 ? `Fixed ${fixed} item${fixed === 1 ? "" : "s"}` : "No items were fixed";
  if (skipped === 0) return fixedText;
  return `${fixedText}; skipped ${skipped} changed ${skipped === 1 ? "issue" : "issues"}`;
}
var LEGACY_EXCALIDRAW_KEY = "excalidraw";
var EXCALIDRAW_FRONTMATTER_KEY = "excalidraw-plugin";
function migrateExcalidrawFrontmatterKey(settings, loaded) {
  const loadedKeys = loaded == null ? void 0 : loaded.ignoredLargeMarkdownFrontmatterKeys;
  if (!loadedKeys || !loadedKeys.includes(LEGACY_EXCALIDRAW_KEY)) return false;
  const migrated = settings.ignoredLargeMarkdownFrontmatterKeys.map(
    (k) => k === LEGACY_EXCALIDRAW_KEY ? EXCALIDRAW_FRONTMATTER_KEY : k
  );
  const deduped = Array.from(new Set(migrated));
  if (deduped.length === settings.ignoredLargeMarkdownFrontmatterKeys.length && deduped.every((k, i) => k === settings.ignoredLargeMarkdownFrontmatterKeys[i])) {
    return false;
  }
  settings.ignoredLargeMarkdownFrontmatterKeys = deduped;
  return true;
}

/* nosourcemap */