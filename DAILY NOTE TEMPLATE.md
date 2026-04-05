---
title: {{date:YYYY-MM-DD}}
aliases:
  - {{date:YYYY-MM-DD}}
  - {{date:MMMM D, YYYY}}
  - {{date:MMMM Do, YYYY}}
  - {{date:D MMMM YYYY}}
  - {{date:dddd, MMMM D, YYYY}}
linter-yaml-title-alias: {{date:YYYY-MM-DD}}
yesterday: <% tp.date.now("YYYY-MM-DD", -1) %>
tomorrow: <% tp.date.now("YYYY-MM-DD", 1) %>
weekday:
  - {{date:dddd}}
tags:
  - today
  - {{date:YYYY/MM/DD}}
  - dailynote
---
obsidian://open?vault=IDAHO-VAULT&file={{date:YYYY-MM-DD}}

[[TO DO LIST]]
