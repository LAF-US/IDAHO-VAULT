---
title: <% moment(tp.file.title, "YYYY-MM-DD").format("YYYY-MM-DD") %>
aliases:
  - <% moment(tp.file.title, "YYYY-MM-DD").format("YYYY-MM-DD") %>
  - <% moment(tp.file.title, "YYYY-MM-DD").format("MMMM D, YYYY") %>
  - <% moment(tp.file.title, "YYYY-MM-DD").format("MMMM Do, YYYY") %>
  - <% moment(tp.file.title, "YYYY-MM-DD").format("D MMMM YYYY") %>
  - <% moment(tp.file.title, "YYYY-MM-DD").format("dddd, MMMM D, YYYY") %>
period: day
linter-yaml-title-alias: <% moment(tp.file.title, "YYYY-MM-DD").format("YYYY-MM-DD") %>
yesterday: <% moment(tp.file.title, "YYYY-MM-DD").subtract(1,"d").format("YYYY-MM-DD") %>
tomorrow: <% moment(tp.file.title, "YYYY-MM-DD").add(1,"d").format("YYYY-MM-DD") %>
weekday:
  - <% moment(tp.file.title, "YYYY-MM-DD").format("dddd") %>
cssclasses:
  - roygbiv-<% moment(tp.file.title, "YYYY-MM-DD").format("ddd").toLowerCase() %>
tags:
  - today
  - <% moment(tp.file.title, "YYYY-MM-DD").format("YYYY/MM/DD") %>
  - dailynote
date created: <% moment(tp.file.title, "YYYY-MM-DD").format("dddd, MMMM Do YYYY, h:mm:ss a") %>
date modified: <% moment(tp.file.title, "YYYY-MM-DD").format("dddd, MMMM Do YYYY, h:mm:ss a") %>
---

## Daily Queue

[[TO DO LIST]]
