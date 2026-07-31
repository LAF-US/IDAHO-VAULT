const { Plugin } = require("obsidian");

const DAY_CLASSES = [
  "roygbiv-mon",
  "roygbiv-tue",
  "roygbiv-wed",
  "roygbiv-thu",
  "roygbiv-fri",
  "roygbiv-sat",
  "roygbiv-sun"
];

const WEEKDAY_TO_CLASS = {
  monday: "roygbiv-mon",
  mon: "roygbiv-mon",
  tuesday: "roygbiv-tue",
  tue: "roygbiv-tue",
  tues: "roygbiv-tue",
  wednesday: "roygbiv-wed",
  wed: "roygbiv-wed",
  thursday: "roygbiv-thu",
  thu: "roygbiv-thu",
  thur: "roygbiv-thu",
  thurs: "roygbiv-thu",
  friday: "roygbiv-fri",
  fri: "roygbiv-fri",
  saturday: "roygbiv-sat",
  sat: "roygbiv-sat",
  sunday: "roygbiv-sun",
  sun: "roygbiv-sun"
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
    const dayClass = this.resolveDayClass(file);
    if (dayClass === null) return;
    this.clearDayClasses();
    document.body.classList.add(dayClass);
  }

  resolveDayClass(file) {
    if (!file) return null;

    const cache = this.app.metadataCache.getFileCache(file);
    const frontmatter = cache && cache.frontmatter ? cache.frontmatter : null;
    if (!frontmatter || frontmatter.weekday == null) return null;

    const weekday = Array.isArray(frontmatter.weekday)
      ? frontmatter.weekday[0]
      : frontmatter.weekday;

    if (typeof weekday !== "string") return null;

    const key = weekday.trim().toLowerCase();
    return Object.prototype.hasOwnProperty.call(WEEKDAY_TO_CLASS, key)
      ? WEEKDAY_TO_CLASS[key]
      : null;
  }
};
