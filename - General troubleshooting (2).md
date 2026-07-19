---
title: "General troubleshooting"
source: "https://docs.openclaw.ai/help/troubleshooting"
author:
published:
created: 2026-04-28
description:
tags:
  - aaaa33
date created: Tuesday, April 28th 2026, 6:26:38 pm
date modified: Tuesday, April 28th 2026, 6:26:45 pm
---

If you only have 2 minutes, use this page as a triage front door.

## First 60 seconds

Run this exact ladder in order:

```shellscript
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

Good output in one line:

- `openclaw status` → shows configured channels and no obvious auth errors.
- `openclaw status --all` → full report is present and shareable.
- `openclaw gateway probe` → expected gateway target is reachable (`Reachable: yes`). `Capability: ...` tells you what auth level the probe could prove, and `Read probe: limited - missing scope: operator.read` is degraded diagnostics, not a connect failure.
- `openclaw gateway status` → `Runtime: running`, `Connectivity probe: ok`, and a plausible `Capability: ...` line. Use `--require-rpc` if you need read-scope RPC proof too.
- `openclaw doctor` → no blocking config/service errors.
- `openclaw channels status --probe` → reachable gateway returns live per-account transport state plus probe/audit results such as `works` or `audit ok`; if the gateway is unreachable, the command falls back to config-only summaries.
- `openclaw logs --follow` → steady activity, no repeating fatal errors.

## Anthropic long context 429

If you see: `HTTP 429: rate_limit_error: Extra usage is required for long context requests`, go to [/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context](https://docs.openclaw.ai/gateway/troubleshooting#anthropic-429-extra-usage-required-for-long-context).

## Local OpenAI-compatible backend works directly but fails in OpenClaw

If your local or self-hosted `/v1` backend answers small direct `/v1/chat/completions` probes but fails on `openclaw infer model run` or normal agent turns:

1. If the error mentions `messages[].content` expecting a string, set `models.providers.<provider>.models[].compat.requiresStringContent: true`.
2. If the backend still fails only on OpenClaw agent turns, set `models.providers.<provider>.models[].compat.supportsTools: false` and retry.
3. If tiny direct calls still work but larger OpenClaw prompts crash the backend, treat the remaining issue as an upstream model/server limitation and continue in the deep runbook: [/gateway/troubleshooting#local-openai-compatible-backend-passes-direct-probes-but-agent-runs-fail](https://docs.openclaw.ai/gateway/troubleshooting#local-openai-compatible-backend-passes-direct-probes-but-agent-runs-fail)

## Plugin install fails with missing openclaw extensions

If install fails with `package.json missing openclaw.extensions`, the plugin package is using an old shape that OpenClaw no longer accepts.

Fix in the plugin package:

1. Add `openclaw.extensions` to `package.json`.
2. Point entries at built runtime files (usually `./dist/index.js`).
3. Republish the plugin and run `openclaw plugins install <package>` again.

Example:

```json
{
  "name": "@openclaw/my-plugin",
  "version": "1.2.3",
  "openclaw": {
    "extensions": ["./dist/index.js"]
  }
}
```

Reference: [Plugin architecture](https://docs.openclaw.ai/plugins/architecture)

## Decision tree

<svg id="mermaid-_r_m_-1777422277433" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="max-width: 2071.96875px;" viewBox="0 0 2071.96875 607.1000366210938" role="graphics-document document" aria-roledescription="flowchart-v2"><style>#mermaid-_r_m_-1777422277433{font-family:inherit;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-_r_m_-1777422277433.edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-_r_m_-1777422277433.edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-_r_m_-1777422277433.error-icon{fill:#552222;}#mermaid-_r_m_-1777422277433.error-text{fill:#552222;stroke:#552222;}#mermaid-_r_m_-1777422277433.edge-thickness-normal{stroke-width:1px;}#mermaid-_r_m_-1777422277433.edge-thickness-thick{stroke-width:3.5px;}#mermaid-_r_m_-1777422277433.edge-pattern-solid{stroke-dasharray:0;}#mermaid-_r_m_-1777422277433.edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-_r_m_-1777422277433.edge-pattern-dashed{stroke-dasharray:3;}#mermaid-_r_m_-1777422277433.edge-pattern-dotted{stroke-dasharray:2;}#mermaid-_r_m_-1777422277433.marker{fill:#333333;stroke:#333333;}#mermaid-_r_m_-1777422277433.marker.cross{stroke:#333333;}#mermaid-_r_m_-1777422277433 svg{font-family:inherit;font-size:16px;}#mermaid-_r_m_-1777422277433 p{margin:0;}#mermaid-_r_m_-1777422277433.label{font-family:inherit;color:#333;}#mermaid-_r_m_-1777422277433.cluster-label text{fill:#333;}#mermaid-_r_m_-1777422277433.cluster-label span{color:#333;}#mermaid-_r_m_-1777422277433.cluster-label span p{background-color:transparent;}#mermaid-_r_m_-1777422277433.label text,#mermaid-_r_m_-1777422277433 span{fill:#333;color:#333;}#mermaid-_r_m_-1777422277433.node rect,#mermaid-_r_m_-1777422277433.node circle,#mermaid-_r_m_-1777422277433.node ellipse,#mermaid-_r_m_-1777422277433.node polygon,#mermaid-_r_m_-1777422277433.node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-_r_m_-1777422277433.rough-node.label text,#mermaid-_r_m_-1777422277433.node.label text,#mermaid-_r_m_-1777422277433.image-shape.label,#mermaid-_r_m_-1777422277433.icon-shape.label{text-anchor:middle;}#mermaid-_r_m_-1777422277433.node.katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-_r_m_-1777422277433.rough-node.label,#mermaid-_r_m_-1777422277433.node.label,#mermaid-_r_m_-1777422277433.image-shape.label,#mermaid-_r_m_-1777422277433.icon-shape.label{text-align:center;}#mermaid-_r_m_-1777422277433.node.clickable{cursor:pointer;}#mermaid-_r_m_-1777422277433.root.anchor path{fill:#333333!important;stroke-width:0;stroke:#333333;}#mermaid-_r_m_-1777422277433.arrowheadPath{fill:#333333;}#mermaid-_r_m_-1777422277433.edgePath.path{stroke:#333333;stroke-width:1px;}#mermaid-_r_m_-1777422277433.flowchart-link{stroke:#333333;fill:none;}#mermaid-_r_m_-1777422277433.edgeLabel{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-_r_m_-1777422277433.edgeLabel p{background-color:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1777422277433.edgeLabel rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1777422277433.labelBkg{background-color:rgba(232, 232, 232, 0.5);}#mermaid-_r_m_-1777422277433.cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-_r_m_-1777422277433.cluster text{fill:#333;}#mermaid-_r_m_-1777422277433.cluster span{color:#333;}#mermaid-_r_m_-1777422277433 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-_r_m_-1777422277433.flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-_r_m_-1777422277433 rect.text{fill:none;stroke-width:0;}#mermaid-_r_m_-1777422277433.icon-shape,#mermaid-_r_m_-1777422277433.image-shape{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-_r_m_-1777422277433.icon-shape p,#mermaid-_r_m_-1777422277433.image-shape p{background-color:rgba(232,232,232, 0.8);padding:2px;}#mermaid-_r_m_-1777422277433.icon-shape.label rect,#mermaid-_r_m_-1777422277433.image-shape.label rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1777422277433.label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-_r_m_-1777422277433.node.label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-_r_m_-1777422277433.node.neo-node{stroke:#9370DB;}#mermaid-_r_m_-1777422277433 [data-look="neo"].node rect,#mermaid-_r_m_-1777422277433 [data-look="neo"].cluster rect,#mermaid-_r_m_-1777422277433 [data-look="neo"].node polygon{stroke:#9370DB;filter:drop-shadow(1px 2px 2px rgba(185, 185, 185, 1));}#mermaid-_r_m_-1777422277433 [data-look="neo"].node path{stroke:#9370DB;stroke-width:1px;}#mermaid-_r_m_-1777422277433 [data-look="neo"].node.outer-path{filter:drop-shadow(1px 2px 2px rgba(185, 185, 185, 1));}#mermaid-_r_m_-1777422277433 [data-look="neo"].node.neo-line path{stroke:#9370DB;filter:none;}#mermaid-_r_m_-1777422277433 [data-look="neo"].node circle{stroke:#9370DB;filter:drop-shadow(1px 2px 2px rgba(185, 185, 185, 1));}#mermaid-_r_m_-1777422277433 [data-look="neo"].node circle.state-start{fill:#000000;}#mermaid-_r_m_-1777422277433 [data-look="neo"].icon-shape.icon{fill:#9370DB;filter:drop-shadow(1px 2px 2px rgba(185, 185, 185, 1));}#mermaid-_r_m_-1777422277433 [data-look="neo"].icon-shape.icon-neo path{stroke:#9370DB;filter:drop-shadow(1px 2px 2px rgba(185, 185, 185, 1));}#mermaid-_r_m_-1777422277433:root{--mermaid-font-family:inherit;}</style><g><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-pointStart" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd-margin" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-pointStart-margin" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-circleEnd" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-circleStart" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-circleEnd-margin" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-circleStart-margin" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-crossEnd" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-crossStart" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-crossEnd-margin" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5;"></path></marker><marker id="mermaid-_r_m_-1777422277433_flowchart-v2-crossStart-margin" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g><g></g><g><path d="M1025.981,86L1025.981,90.167C1025.981,94.333,1025.981,102.667,1025.981,110.333C1025.981,118,1025.981,125,1025.981,128.5L1025.981,132" id="mermaid-_r_m_-1777422277433-L_A_B_0" style=";" data-edge="true" data-et="edge" data-id="L_A_B_0" data-points="W3sieCI6MTAyNS45ODEyNTQ1Nzc2MzY3LCJ5Ijo4Nn0seyJ4IjoxMDI1Ljk4MTI1NDU3NzYzNjcsInkiOjExMX0seyJ4IjoxMDI1Ljk4MTI1NDU3NzYzNjcsInkiOjEzNn1d" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M929.486,261.605L795.237,281.854C660.989,302.103,392.491,342.602,258.242,370.351C123.994,398.1,123.994,413.1,123.994,420.6L123.994,428.1" id="mermaid-_r_m_-1777422277433-L_B_C_0" style=";" data-edge="true" data-et="edge" data-id="L_B_C_0" data-points="W3sieCI6OTI5LjQ4NTk3OTIzNTg2NDgsInkiOjI2MS42MDQ3MzA3NjE3NDM1NX0seyJ4IjoxMjMuOTkzNzUxNTI1ODc4OSwieSI6MzgzLjEwMDAwNjEwMzUxNTZ9LHsieCI6MTIzLjk5Mzc1MTUyNTg3ODksInkiOjQzMi4xMDAwMDYxMDM1MTU2fV0=" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M934.915,267.033L846.759,286.378C758.603,305.722,582.292,344.411,494.137,367.256C405.981,390.1,405.981,397.1,405.981,400.6L405.981,404.1" id="mermaid-_r_m_-1777422277433-L_B_D_0" style=";" data-edge="true" data-et="edge" data-id="L_B_D_0" data-points="W3sieCI6OTM0LjkxNDUyNDA1MTY0NDcsInkiOjI2Ny4wMzMyNzU1Nzc1MjM2fSx7IngiOjQwNS45ODEyNTQ1Nzc2MzY3LCJ5IjozODMuMTAwMDA2MTAzNTE1Nn0seyJ4Ijo0MDUuOTgxMjU0NTc3NjM2NywieSI6NDA4LjEwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M948.803,280.921L909.999,297.951C871.196,314.981,793.588,349.04,754.785,369.57C715.981,390.1,715.981,397.1,715.981,400.6L715.981,404.1" id="mermaid-_r_m_-1777422277433-L_B_E_0" style=";" data-edge="true" data-et="edge" data-id="L_B_E_0" data-points="W3sieCI6OTQ4LjgwMjY4NTU1OTU1NjgsInkiOjI4MC45MjE0MzcwODU0MzU1N30seyJ4Ijo3MTUuOTgxMjU0NTc3NjM2NywieSI6MzgzLjEwMDAwNjEwMzUxNTZ9LHsieCI6NzE1Ljk4MTI1NDU3NzYzNjcsInkiOjQwOC4xMDAwMDYxMDM1MTU2fV0=" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1025.981,358.1L1025.981,362.267C1025.981,366.433,1025.981,374.767,1025.981,382.433C1025.981,390.1,1025.981,397.1,1025.981,400.6L1025.981,404.1" id="mermaid-_r_m_-1777422277433-L_B_F_0" style=";" data-edge="true" data-et="edge" data-id="L_B_F_0" data-points="W3sieCI6MTAyNS45ODEyNTQ1Nzc2MzY3LCJ5IjozNTguMTAwMDA2MTAzNTE1NzR9LHsieCI6MTAyNS45ODEyNTQ1Nzc2MzY3LCJ5IjozODMuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxMDI1Ljk4MTI1NDU3NzYzNjcsInkiOjQwOC4xMDAwMDYxMDM1MTU2fV0=" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1103.16,280.921L1141.963,297.951C1180.767,314.981,1258.374,349.04,1297.178,369.57C1335.981,390.1,1335.981,397.1,1335.981,400.6L1335.981,404.1" id="mermaid-_r_m_-1777422277433-L_B_G_0" style=";" data-edge="true" data-et="edge" data-id="L_B_G_0" data-points="W3sieCI6MTEwMy4xNTk4MjM1OTU3MTY3LCJ5IjoyODAuOTIxNDM3MDg1NDM1NTd9LHsieCI6MTMzNS45ODEyNTQ1Nzc2MzY3LCJ5IjozODMuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxMzM1Ljk4MTI1NDU3NzYzNjcsInkiOjQwOC4xMDAwMDYxMDM1MTU2fV0=" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1117.048,267.033L1205.204,286.378C1293.359,305.722,1469.67,344.411,1557.826,367.256C1645.981,390.1,1645.981,397.1,1645.981,400.6L1645.981,404.1" id="mermaid-_r_m_-1777422277433-L_B_H_0" style=";" data-edge="true" data-et="edge" data-id="L_B_H_0" data-points="W3sieCI6MTExNy4wNDc5ODUxMDM2Mjg3LCJ5IjoyNjcuMDMzMjc1NTc3NTIzN30seyJ4IjoxNjQ1Ljk4MTI1NDU3NzYzNjcsInkiOjM4My4xMDAwMDYxMDM1MTU2fSx7IngiOjE2NDUuOTgxMjU0NTc3NjM2NywieSI6NDA4LjEwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1122.711,261.37L1259.755,281.658C1396.799,301.947,1670.887,342.523,1807.931,370.312C1944.975,398.1,1944.975,413.1,1944.975,420.6L1944.975,428.1" id="mermaid-_r_m_-1777422277433-L_B_I_0" style=";" data-edge="true" data-et="edge" data-id="L_B_I_0" data-points="W3sieCI6MTEyMi43MTExMzc1NTA0NTI2LCJ5IjoyNjEuMzcwMTIzMTMwNjk5Nn0seyJ4IjoxOTQ0Ljk3NTAwNjEwMzUxNTYsInkiOjM4My4xMDAwMDYxMDM1MTU2fSx7IngiOjE5NDQuOTc1MDA2MTAzNTE1NiwieSI6NDMyLjEwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M123.994,486.1L123.994,494.267C123.994,502.433,123.994,518.767,124.064,530.517C124.134,542.267,124.275,549.434,124.345,553.017L124.415,556.601" id="mermaid-_r_m_-1777422277433-L_C_C1_0" style=";" data-edge="true" data-et="edge" data-id="L_C_C1_0" data-points="W3sieCI6MTIzLjk5Mzc1MTUyNTg3ODksInkiOjQ4Ni4xMDAwMDYxMDM1MTU2fSx7IngiOjEyMy45OTM3NTE1MjU4Nzg5LCJ5Ijo1MzUuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxMjQuNDkzNzUxNTI1ODc4OSwieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M405.981,510.1L405.981,514.267C405.981,518.433,405.981,526.767,406.052,534.517C406.122,542.267,406.262,549.434,406.333,553.017L406.403,556.601" id="mermaid-_r_m_-1777422277433-L_D_D1_0" style=";" data-edge="true" data-et="edge" data-id="L_D_D1_0" data-points="W3sieCI6NDA1Ljk4MTI1NDU3NzYzNjcsInkiOjUxMC4xMDAwMDYxMDM1MTU2fSx7IngiOjQwNS45ODEyNTQ1Nzc2MzY3LCJ5Ijo1MzUuMTAwMDA2MTAzNTE1Nn0seyJ4Ijo0MDYuNDgxMjU0NTc3NjM2NywieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M715.981,510.1L715.981,514.267C715.981,518.433,715.981,526.767,716.052,534.517C716.122,542.267,716.262,549.434,716.333,553.017L716.403,556.601" id="mermaid-_r_m_-1777422277433-L_E_E1_0" style=";" data-edge="true" data-et="edge" data-id="L_E_E1_0" data-points="W3sieCI6NzE1Ljk4MTI1NDU3NzYzNjcsInkiOjUxMC4xMDAwMDYxMDM1MTU2fSx7IngiOjcxNS45ODEyNTQ1Nzc2MzY3LCJ5Ijo1MzUuMTAwMDA2MTAzNTE1Nn0seyJ4Ijo3MTYuNDgxMjU0NTc3NjM2NywieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1025.981,510.1L1025.981,514.267C1025.981,518.433,1025.981,526.767,1026.052,534.517C1026.122,542.267,1026.262,549.434,1026.333,553.017L1026.403,556.601" id="mermaid-_r_m_-1777422277433-L_F_F1_0" style=";" data-edge="true" data-et="edge" data-id="L_F_F1_0" data-points="W3sieCI6MTAyNS45ODEyNTQ1Nzc2MzY3LCJ5Ijo1MTAuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxMDI1Ljk4MTI1NDU3NzYzNjcsInkiOjUzNS4xMDAwMDYxMDM1MTU2fSx7IngiOjEwMjYuNDgxMjU0NTc3NjM2NywieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1335.981,510.1L1335.981,514.267C1335.981,518.433,1335.981,526.767,1336.052,534.517C1336.122,542.267,1336.262,549.434,1336.333,553.017L1336.403,556.601" id="mermaid-_r_m_-1777422277433-L_G_G1_0" style=";" data-edge="true" data-et="edge" data-id="L_G_G1_0" data-points="W3sieCI6MTMzNS45ODEyNTQ1Nzc2MzY3LCJ5Ijo1MTAuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxMzM1Ljk4MTI1NDU3NzYzNjcsInkiOjUzNS4xMDAwMDYxMDM1MTU2fSx7IngiOjEzMzYuNDgxMjU0NTc3NjM2NywieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1645.981,510.1L1645.981,514.267C1645.981,518.433,1645.981,526.767,1646.052,534.517C1646.122,542.267,1646.262,549.434,1646.333,553.017L1646.403,556.601" id="mermaid-_r_m_-1777422277433-L_H_H1_0" style=";" data-edge="true" data-et="edge" data-id="L_H_H1_0" data-points="W3sieCI6MTY0NS45ODEyNTQ1Nzc2MzY3LCJ5Ijo1MTAuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxNjQ1Ljk4MTI1NDU3NzYzNjcsInkiOjUzNS4xMDAwMDYxMDM1MTU2fSx7IngiOjE2NDYuNDgxMjU0NTc3NjM2NywieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path><path d="M1944.975,486.1L1944.975,494.267C1944.975,502.433,1944.975,518.767,1945.045,530.517C1945.116,542.267,1945.256,549.434,1945.326,553.017L1945.397,556.601" id="mermaid-_r_m_-1777422277433-L_I_I1_0" style=";" data-edge="true" data-et="edge" data-id="L_I_I1_0" data-points="W3sieCI6MTk0NC45NzUwMDYxMDM1MTU2LCJ5Ijo0ODYuMTAwMDA2MTAzNTE1Nn0seyJ4IjoxOTQ0Ljk3NTAwNjEwMzUxNTYsInkiOjUzNS4xMDAwMDYxMDM1MTU2fSx7IngiOjE5NDUuNDc1MDA2MTAzNTE1NiwieSI6NTYwLjYwMDAwNjEwMzUxNTZ9XQ==" data-look="classic" marker-end="url(#mermaid-_r_m_-1777422277433_flowchart-v2-pointEnd)"></path></g><g><g><g data-id="L_A_B_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_C_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_D_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_E_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_F_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_G_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_H_0" transform="translate(0, 0)"></g></g><g><g data-id="L_B_I_0" transform="translate(0, 0)"></g></g><g><g data-id="L_C_C1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_D_D1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_E_E1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_F_F1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_G_G1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_H_H1_0" transform="translate(0, 0)"></g></g><g><g data-id="L_I_I1_0" transform="translate(0, 0)"></g></g></g><g><g id="mermaid-_r_m_-1777422277433-flowchart-A-0" data-look="classic" transform="translate(1025.9812545776367, 47)"><rect style="" x="-130" y="-39" width="260" height="78"></rect><g style="" transform="translate(-100, -24)"><rect></rect><foreignObject width="200" height="48"><p>OpenClaw is not working</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-B-1" data-look="classic" transform="translate(1025.9812545776367, 247.0500030517578)"><polygon points="111.05000305175781,0 222.10000610351562,-111.05000305175781 111.05000305175781,-222.10000610351562 0,-111.05000305175781" transform="translate(-110.55000305175781, 111.05000305175781)"></polygon><g style="" transform="translate(-84.05000305175781, -12)"><rect></rect><foreignObject width="168.10000610351562" height="24"><p>What breaks first</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-C-3" data-look="classic" transform="translate(123.9937515258789, 459.1000061035156)"><rect style="" x="-79.44375228881836" y="-27" width="158.88750457763672" height="54"></rect><g style="" transform="translate(-49.44375228881836, -12)"><rect></rect><foreignObject width="98.88750457763672" height="24"><p>No replies</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-D-5" data-look="classic" transform="translate(405.9812545776367, 459.1000061035156)"><rect style="" x="-130" y="-51" width="260" height="102"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>Dashboard or Control UI will not connect</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-E-7" data-look="classic" transform="translate(715.9812545776367, 459.1000061035156)"><rect style="" x="-130" y="-51" width="260" height="102"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>Gateway will not start or service not running</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-F-9" data-look="classic" transform="translate(1025.9812545776367, 459.1000061035156)"><rect style="" x="-130" y="-51" width="260" height="102"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>Channel connects but messages do not flow</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-G-11" data-look="classic" transform="translate(1335.9812545776367, 459.1000061035156)"><rect style="" x="-130" y="-51" width="260" height="102"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>Cron or heartbeat did not fire or did not deliver</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-H-13" data-look="classic" transform="translate(1645.9812545776367, 459.1000061035156)"><rect style="" x="-130" y="-51" width="260" height="102"></rect><g style="" transform="translate(-100, -36)"><rect></rect><foreignObject width="200" height="72"><p>Node is paired but camera canvas screen exec fails</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-I-15" data-look="classic" transform="translate(1944.9750061035156, 459.1000061035156)"><rect style="" x="-118.9937515258789" y="-27" width="237.9875030517578" height="54"></rect><g style="" transform="translate(-88.9937515258789, -12)"><rect></rect><foreignObject width="177.9875030517578" height="24"><p>Browser tool fails</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-C1-17" data-look="classic" transform="translate(123.9937515258789, 579.6000061035156)"><polygon points="-19.5,0 192.9875030517578,0 212.4875030517578,-39 0,-39" transform="translate(-96.4937515258789,19.5)"></polygon><g style="" transform="translate(-88.9937515258789, -12)"><rect></rect><foreignObject width="177.9875030517578" height="24"><p>No replies section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-D1-19" data-look="classic" transform="translate(405.9812545776367, 579.6000061035156)"><polygon points="-19.5,0 192.9875030517578,0 212.4875030517578,-39 0,-39" transform="translate(-96.4937515258789,19.5)"></polygon><g style="" transform="translate(-88.9937515258789, -12)"><rect></rect><foreignObject width="177.9875030517578" height="24"><p>Control UI section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-E1-21" data-look="classic" transform="translate(715.9812545776367, 579.6000061035156)"><polygon points="-19.5,0 163.3249969482422,0 182.8249969482422,-39 0,-39" transform="translate(-81.6624984741211,19.5)"></polygon><g style="" transform="translate(-74.1624984741211, -12)"><rect></rect><foreignObject width="148.3249969482422" height="24"><p>Gateway section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-F1-23" data-look="classic" transform="translate(1025.9812545776367, 579.6000061035156)"><polygon points="-19.5,0 212.7624969482422,0 232.2624969482422,-39 0,-39" transform="translate(-106.3812484741211,19.5)"></polygon><g style="" transform="translate(-98.8812484741211, -12)"><rect></rect><foreignObject width="197.7624969482422" height="24"><p>Channel flow section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-G1-25" data-look="classic" transform="translate(1335.9812545776367, 579.6000061035156)"><polygon points="-19.5,0 192.9875030517578,0 212.4875030517578,-39 0,-39" transform="translate(-96.4937515258789,19.5)"></polygon><g style="" transform="translate(-88.9937515258789, -12)"><rect></rect><foreignObject width="177.9875030517578" height="24"><p>Automation section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-H1-27" data-look="classic" transform="translate(1645.9812545776367, 579.6000061035156)"><polygon points="-19.5,0 192.9875030517578,0 212.4875030517578,-39 0,-39" transform="translate(-96.4937515258789,19.5)"></polygon><g style="" transform="translate(-88.9937515258789, -12)"><rect></rect><foreignObject width="177.9875030517578" height="24"><p>Node tools section</p></foreignObject></g></g><g id="mermaid-_r_m_-1777422277433-flowchart-I1-29" data-look="classic" transform="translate(1944.9750061035156, 579.6000061035156)"><polygon points="-19.5,0 163.3249969482422,0 182.8249969482422,-39 0,-39" transform="translate(-81.6624984741211,19.5)"></polygon><g style="" transform="translate(-74.1624984741211, -12)"><rect></rect><foreignObject width="148.3249969482422" height="24"><p>Browser section</p></foreignObject></g></g></g></g></g><defs></defs><defs></defs></svg>

No replies

```shellscript
openclaw status
openclaw gateway status
openclaw channels status --probe
openclaw pairing list --channel <channel> [--account <id>]
openclaw logs --follow
```

Good output looks like:

- `Runtime: running`
- `Connectivity probe: ok`
- `Capability: read-only`, `write-capable`, or `admin-capable`
- Your channel shows transport connected and, where supported, `works` or `audit ok` in `channels status --probe`
- Sender appears approved (or DM policy is open/allowlist)

Common log signatures:

- `drop guild message (mention required` → mention gating blocked the message in Discord.
- `pairing request` → sender is unapproved and waiting for DM pairing approval.
- `blocked` / `allowlist` in channel logs → sender, room, or group is filtered.

Deep pages:

- [/gateway/troubleshooting#no-replies](https://docs.openclaw.ai/gateway/troubleshooting#no-replies)
- [/channels/troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)
- [/channels/pairing](https://docs.openclaw.ai/channels/pairing)

Dashboard or Control UI will not connect

```shellscript
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Good output looks like:

- `Dashboard: http://...` is shown in `openclaw gateway status`
- `Connectivity probe: ok`
- `Capability: read-only`, `write-capable`, or `admin-capable`
- No auth loop in logs

Common log signatures:

- `device identity required` → HTTP/non-secure context cannot complete device auth.
- `origin not allowed` → browser `Origin` is not allowed for the Control UI gateway target.
- `AUTH_TOKEN_MISMATCH` with retry hints (`canRetryWithDeviceToken=true`) → one trusted device-token retry may occur automatically.
- That cached-token retry reuses the cached scope set stored with the paired device token. Explicit `deviceToken` / explicit `scopes` callers keep their requested scope set instead.
- On the async Tailscale Serve Control UI path, failed attempts for the same `{scope, ip}` are serialized before the limiter records the failure, so a second concurrent bad retry can already show `retry later`.
- `too many failed authentication attempts (retry later)` from a localhost browser origin → repeated failures from that same `Origin` are temporarily locked out; another localhost origin uses a separate bucket.
- repeated `unauthorized` after that retry → wrong token/password, auth mode mismatch, or stale paired device token.
- `gateway connect failed:` → UI is targeting the wrong URL/port or unreachable gateway.

Deep pages:

- [/gateway/troubleshooting#dashboard-control-ui-connectivity](https://docs.openclaw.ai/gateway/troubleshooting#dashboard-control-ui-connectivity)
- [/web/control-ui](https://docs.openclaw.ai/web/control-ui)
- [/gateway/authentication](https://docs.openclaw.ai/gateway/authentication)

Gateway will not start or service installed but not running

```shellscript
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Good output looks like:

- `Service: ... (loaded)`
- `Runtime: running`
- `Connectivity probe: ok`
- `Capability: read-only`, `write-capable`, or `admin-capable`

Common log signatures:

- `Gateway start blocked: set gateway.mode=local` or `existing config is missing gateway.mode` → gateway mode is remote, or the config file is missing the local-mode stamp and should be repaired.
- `refusing to bind gateway ... without auth` → non-loopback bind without a valid gateway auth path (token/password, or trusted-proxy where configured).
- `another gateway instance is already listening` or `EADDRINUSE` → port already taken.

Deep pages:

- [/gateway/troubleshooting#gateway-service-not-running](https://docs.openclaw.ai/gateway/troubleshooting#gateway-service-not-running)
- [/gateway/background-process](https://docs.openclaw.ai/gateway/background-process)
- [/gateway/configuration](https://docs.openclaw.ai/gateway/configuration)

Channel connects but messages do not flow

```shellscript
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe
```

Good output looks like:

- Channel transport is connected.
- Pairing/allowlist checks pass.
- Mentions are detected where required.

Common log signatures:

- `mention required` → group mention gating blocked processing.
- `pairing` / `pending` → DM sender is not approved yet.
- `not_in_channel`, `missing_scope`, `Forbidden`, `401/403` → channel permission token issue.

Deep pages:

- [/gateway/troubleshooting#channel-connected-messages-not-flowing](https://docs.openclaw.ai/gateway/troubleshooting#channel-connected-messages-not-flowing)
- [/channels/troubleshooting](https://docs.openclaw.ai/channels/troubleshooting)

Cron or heartbeat did not fire or did not deliver

```shellscript
openclaw status
openclaw gateway status
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw logs --follow
```

Good output looks like:

- `cron.status` shows enabled with a next wake.
- `cron runs` shows recent `ok` entries.
- Heartbeat is enabled and not outside active hours.

Common log signatures:

- `cron: scheduler disabled; jobs will not run automatically` → cron is disabled.
- `heartbeat skipped` with `reason=quiet-hours` → outside configured active hours.
- `heartbeat skipped` with `reason=empty-heartbeat-file` → `HEARTBEAT.md` exists but only contains blank/header-only scaffolding.
- `heartbeat skipped` with `reason=no-tasks-due` → `HEARTBEAT.md` task mode is active but none of the task intervals are due yet.
- `heartbeat skipped` with `reason=alerts-disabled` → all heartbeat visibility is disabled (`showOk`, `showAlerts`, and `useIndicator` are all off).
- `requests-in-flight` → main lane busy; heartbeat wake was deferred.
- `unknown accountId` → heartbeat delivery target account does not exist.

Deep pages:

- [/gateway/troubleshooting#cron-and-heartbeat-delivery](https://docs.openclaw.ai/gateway/troubleshooting#cron-and-heartbeat-delivery)
- [/automation/cron-jobs#troubleshooting](https://docs.openclaw.ai/automation/cron-jobs#troubleshooting)
- [/gateway/heartbeat](https://docs.openclaw.ai/gateway/heartbeat)

Node is paired but tool fails camera canvas screen exec

```shellscript
openclaw status
openclaw gateway status
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw logs --follow
```

Good output looks like:

- Node is listed as connected and paired for role `node`.
- Capability exists for the command you are invoking.
- Permission state is granted for the tool.

Common log signatures:

- `NODE_BACKGROUND_UNAVAILABLE` → bring node app to foreground.
- `*_PERMISSION_REQUIRED` → OS permission was denied/missing.
- `SYSTEM_RUN_DENIED: approval required` → exec approval is pending.
- `SYSTEM_RUN_DENIED: allowlist miss` → command not on exec allowlist.

Deep pages:

- [/gateway/troubleshooting#node-paired-tool-fails](https://docs.openclaw.ai/gateway/troubleshooting#node-paired-tool-fails)
- [/nodes/troubleshooting](https://docs.openclaw.ai/nodes/troubleshooting)
- [/tools/exec-approvals](https://docs.openclaw.ai/tools/exec-approvals)

Exec suddenly asks for approval

```shellscript
openclaw config get tools.exec.host
openclaw config get tools.exec.security
openclaw config get tools.exec.ask
openclaw gateway restart
```

What changed:

- If `tools.exec.host` is unset, the default is `auto`.
- `host=auto` resolves to `sandbox` when a sandbox runtime is active, `gateway` otherwise.
- `host=auto` is routing only; the no-prompt “YOLO” behavior comes from `security=full` plus `ask=off` on gateway/node.
- On `gateway` and `node`, unset `tools.exec.security` defaults to `full`.
- Unset `tools.exec.ask` defaults to `off`.
- Result: if you are seeing approvals, some host-local or per-session policy tightened exec away from the current defaults.

Restore current default no-approval behavior:

```shellscript
openclaw config set tools.exec.host gateway
openclaw config set tools.exec.security full
openclaw config set tools.exec.ask off
openclaw gateway restart
```

Safer alternatives:

- Set only `tools.exec.host=gateway` if you just want stable host routing.
- Use `security=allowlist` with `ask=on-miss` if you want host exec but still want review on allowlist misses.
- Enable sandbox mode if you want `host=auto` to resolve back to `sandbox`.

Common log signatures:

- `Approval required.` → command is waiting on `/approve ...`.
- `SYSTEM_RUN_DENIED: approval required` → node-host exec approval is pending.
- `exec host=sandbox requires a sandbox runtime for this session` → implicit/explicit sandbox selection but sandbox mode is off.

Deep pages:

- [/tools/exec](https://docs.openclaw.ai/tools/exec)
- [/tools/exec-approvals](https://docs.openclaw.ai/tools/exec-approvals)
- [/gateway/security#what-the-audit-checks-high-level](https://docs.openclaw.ai/gateway/security#what-the-audit-checks-high-level)

Browser tool fails

```shellscript
openclaw status
openclaw gateway status
openclaw browser status
openclaw logs --follow
openclaw doctor
```

Good output looks like:

- Browser status shows `running: true` and a chosen browser/profile.
- `openclaw` starts, or `user` can see local Chrome tabs.

Common log signatures:

- `unknown command "browser"` or `unknown command 'browser'` → `plugins.allow` is set and does not include `browser`.
- `Failed to start Chrome CDP on port` → local browser launch failed.
- `browser.executablePath not found` → configured binary path is wrong.
- `browser.cdpUrl must be http(s) or ws(s)` → the configured CDP URL uses an unsupported scheme.
- `browser.cdpUrl has invalid port` → the configured CDP URL has a bad or out-of-range port.
- `No Chrome tabs found for profile="user"` → the Chrome MCP attach profile has no open local Chrome tabs.
- `Remote CDP for profile "<name>" is not reachable` → the configured remote CDP endpoint is not reachable from this host.
- `Browser attachOnly is enabled ... not reachable` or `Browser attachOnly is enabled and CDP websocket ... is not reachable` → attach-only profile has no live CDP target.
- stale viewport / dark-mode / locale / offline overrides on attach-only or remote CDP profiles → run `openclaw browser stop --browser-profile <name>` to close the active control session and release emulation state without restarting the gateway.

Deep pages:

- [/gateway/troubleshooting#browser-tool-fails](https://docs.openclaw.ai/gateway/troubleshooting#browser-tool-fails)
- [/tools/browser#missing-browser-command-or-tool](https://docs.openclaw.ai/tools/browser#missing-browser-command-or-tool)
- [/tools/browser-linux-troubleshooting](https://docs.openclaw.ai/tools/browser-linux-troubleshooting)
- [/tools/browser-wsl2-windows-remote-cdp-troubleshooting](https://docs.openclaw.ai/tools/browser-wsl2-windows-remote-cdp-troubleshooting)

## Related

- [FAQ](https://docs.openclaw.ai/help/faq) — frequently asked questions
- [Gateway Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting) — gateway-specific issues
- [Doctor](https://docs.openclaw.ai/gateway/doctor) — automated health checks and repairs
- [Channel Troubleshooting](https://docs.openclaw.ai/channels/troubleshooting) — channel connectivity issues
- [Automation Troubleshooting](https://docs.openclaw.ai/automation/cron-jobs#troubleshooting) — cron and heartbeat issues