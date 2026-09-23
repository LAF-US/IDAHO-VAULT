<%*
const parsed = moment(tp.file.title, "YYYY-MM-DD", true);
const d = parsed.isValid() ? parsed : moment();
const weekday = d.format("dddd");
const weekdayShort = d.format("ddd").toLowerCase();
const stamp = `${weekday}, ${d.format("MMMM Do YYYY")}, 12:00:00 am`;
tR += `---
title: ${d.format("YYYY-MM-DD")}
aliases:
  - ${d.format("YYYY-MM-DD")}
  - ${d.format("MMMM D, YYYY")}
  - ${d.format("MMMM Do, YYYY")}
  - ${d.format("D MMMM YYYY")}
  - ${d.format("dddd, MMMM D, YYYY")}
linter-yaml-title-alias: ${d.format("YYYY-MM-DD")}
yesterday: ${d.clone().subtract(1, "day").format("YYYY-MM-DD")}
tomorrow: ${d.clone().add(1, "day").format("YYYY-MM-DD")}
weekday:
  - ${weekday}
cssclasses:
  - roygbiv-<% tp.date.now("ddd", 0, tp.file.title, "YYYY-MM-DD").toLowerCase() %>
tags:
  - today
  - ${d.format("YYYY/MM/DD")}
  - dailynote
related:
  - TO DO LIST
date created: {{date:dddd, MMMM Do YYYY, [12:00:00 am]}}
date modified: {{date:dddd, MMMM Do YYYY, [12:00:00 am]}}
---

# {{date:dddd, MMMM D, YYYY}}

## Daily Queue

[[TO DO LIST]]

*(no incomplete items carried forward)*

## Notes

- 
