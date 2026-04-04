const { Plugin } = require("obsidian");

const DAY_CLASSES = [
  "roygbiv-sun",
  "roygbiv-mon",
  "roygbiv-tue",
  "roygbiv-wed",
  "roygbiv-thu",
  "roygbiv-fri",
  "roygbiv-sat"
];

const WEEKDAY_TO_INDEX = {
  sunday: 0,
  sun: 0,
  monday: 1,
  mon: 1,
  tuesday: 2,
  tue: 2,
  tues: 2,
  wednesday: 3,
  wed: 3,
  thursday: 4,
  thu: 4,
  thur: 4,
  thurs: 4,
  friday: 5,
  fri: 5,
  saturday: 6,
  sat: 6
};

module.exports = class RoygbivDayAccentPlugin extends Plugin {
  onload() {
    this.applyDayClass();

    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => this.applyDayClass())
    );

    this.registerEvent(
      this.app.metadataCache.on("changed", () => this.applyDayClass())
    );

    this.scheduleMidnightRefresh();
    this.registerInterval(window.setInterval(() => this.applyDayClass(), 60 * 60 * 1000));
  }

  onunload() {
    this.clearDayClasses();
  }

  clearDayClasses() {
    if (!document || !document.body) return;
    for (const cls of DAY_CLASSES) {
      document.body.classList.remove(cls);
    }
  }

  applyDayClass() {
    if (!document || !document.body) return;
    this.clearDayClasses();

    const dayIndex = this.resolveDayFromFrontmatter() ?? new Date().getDay();
    document.body.classList.add(DAY_CLASSES[dayIndex]);
  }

  resolveDayFromFrontmatter() {
    const activeFile = this.app.workspace.getActiveFile();
    if (!activeFile) return null;

    const cache = this.app.metadataCache.getFileCache(activeFile);
    const frontmatter = cache && cache.frontmatter ? cache.frontmatter : null;
    if (!frontmatter || frontmatter.weekday == null) return null;

    const weekday = Array.isArray(frontmatter.weekday)
      ? frontmatter.weekday[0]
      : frontmatter.weekday;

    if (typeof weekday !== "string") return null;

    const key = weekday.trim().toLowerCase();
    return Object.prototype.hasOwnProperty.call(WEEKDAY_TO_INDEX, key)
      ? WEEKDAY_TO_INDEX[key]
      : null;
  }

  scheduleMidnightRefresh() {
    const now = new Date();
    const next = new Date(now);
    next.setHours(24, 0, 5, 0);
    const ms = Math.max(1000, next.getTime() - now.getTime());

    const timeoutId = window.setTimeout(() => {
      this.applyDayClass();
      this.scheduleMidnightRefresh();
    }, ms);

    this.register(() => window.clearTimeout(timeoutId));
  }
};
