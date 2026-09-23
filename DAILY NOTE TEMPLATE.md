---
title: {{date:YYYY-MM-DD}}
aliases:
  - {{date:YYYY-MM-DD}}
  - {{date:MMMM D, YYYY}}
  - {{date:MMMM Do, YYYY}}
  - {{date:D MMMM YYYY}}
  - {{date:dddd, MMMM D, YYYY}}
linter-yaml-title-alias: {{date:YYYY-MM-DD}}
yesterday: {{date-1d:YYYY-MM-DD}}
tomorrow: {{date+1d:YYYY-MM-DD}}
weekday:
  - {{date:dddd}}
cssclasses:
  - roygbiv-<% tp.date.now("ddd", 0, tp.file.title, "YYYY-MM-DD").toLowerCase() %>
tags:
  - today
  - {{date:YYYY/MM/DD}}
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
