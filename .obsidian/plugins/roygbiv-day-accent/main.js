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
    this.app.workspace.onLayoutReady(() => {
      this.applyDayClass(this.app.workspace.getActiveFile());
    });

    this.registerEvent(
      this.app.workspace.on("file-open", (file) => this.applyDayClass(file))
    );
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

  applyDayClass(file) {
    if (!document || !document.body) return;
    const dayIndex = this.resolveDayFromFrontmatter(file);
    if (dayIndex === null) return;
    this.clearDayClasses();
    document.body.classList.add(DAY_CLASSES[dayIndex]);
  }

  resolveDayFromFrontmatter(file) {
    if (!file) return null;

    const cache = this.app.metadataCache.getFileCache(file);
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
};
