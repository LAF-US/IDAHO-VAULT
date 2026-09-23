---
source: "https://docs.openclaw.ai/help/troubleshooting"
author:
published:
created: 2026-04-20
---
## Troubleshooting

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

<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="0 0 2071.9609375 607.109375" style="max-width: 2071.9609375px;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="mermaid-_r_m_-1776715842853"><style>#mermaid-_r_m_-1776715842853{font-family:inherit;font-size:16px;fill:#333;}#mermaid-_r_m_-1776715842853.error-icon{fill:#552222;}#mermaid-_r_m_-1776715842853.error-text{fill:#552222;stroke:#552222;}#mermaid-_r_m_-1776715842853.edge-thickness-normal{stroke-width:1px;}#mermaid-_r_m_-1776715842853.edge-thickness-thick{stroke-width:3.5px;}#mermaid-_r_m_-1776715842853.edge-pattern-solid{stroke-dasharray:0;}#mermaid-_r_m_-1776715842853.edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-_r_m_-1776715842853.edge-pattern-dashed{stroke-dasharray:3;}#mermaid-_r_m_-1776715842853.edge-pattern-dotted{stroke-dasharray:2;}#mermaid-_r_m_-1776715842853.marker{fill:#333333;stroke:#333333;}#mermaid-_r_m_-1776715842853.marker.cross{stroke:#333333;}#mermaid-_r_m_-1776715842853 svg{font-family:inherit;font-size:16px;}#mermaid-_r_m_-1776715842853 p{margin:0;}#mermaid-_r_m_-1776715842853.label{font-family:inherit;color:#333;}#mermaid-_r_m_-1776715842853.cluster-label text{fill:#333;}#mermaid-_r_m_-1776715842853.cluster-label span{color:#333;}#mermaid-_r_m_-1776715842853.cluster-label span p{background-color:transparent;}#mermaid-_r_m_-1776715842853.label text,#mermaid-_r_m_-1776715842853 span{fill:#333;color:#333;}#mermaid-_r_m_-1776715842853.node rect,#mermaid-_r_m_-1776715842853.node circle,#mermaid-_r_m_-1776715842853.node ellipse,#mermaid-_r_m_-1776715842853.node polygon,#mermaid-_r_m_-1776715842853.node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-_r_m_-1776715842853.rough-node.label text,#mermaid-_r_m_-1776715842853.node.label text,#mermaid-_r_m_-1776715842853.image-shape.label,#mermaid-_r_m_-1776715842853.icon-shape.label{text-anchor:middle;}#mermaid-_r_m_-1776715842853.node.katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-_r_m_-1776715842853.rough-node.label,#mermaid-_r_m_-1776715842853.node.label,#mermaid-_r_m_-1776715842853.image-shape.label,#mermaid-_r_m_-1776715842853.icon-shape.label{text-align:center;}#mermaid-_r_m_-1776715842853.node.clickable{cursor:pointer;}#mermaid-_r_m_-1776715842853.root.anchor path{fill:#333333!important;stroke-width:0;stroke:#333333;}#mermaid-_r_m_-1776715842853.arrowheadPath{fill:#333333;}#mermaid-_r_m_-1776715842853.edgePath.path{stroke:#333333;stroke-width:2.0px;}#mermaid-_r_m_-1776715842853.flowchart-link{stroke:#333333;fill:none;}#mermaid-_r_m_-1776715842853.edgeLabel{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-_r_m_-1776715842853.edgeLabel p{background-color:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1776715842853.edgeLabel rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1776715842853.labelBkg{background-color:rgba(232, 232, 232, 0.5);}#mermaid-_r_m_-1776715842853.cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-_r_m_-1776715842853.cluster text{fill:#333;}#mermaid-_r_m_-1776715842853.cluster span{color:#333;}#mermaid-_r_m_-1776715842853 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-_r_m_-1776715842853.flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-_r_m_-1776715842853 rect.text{fill:none;stroke-width:0;}#mermaid-_r_m_-1776715842853.icon-shape,#mermaid-_r_m_-1776715842853.image-shape{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-_r_m_-1776715842853.icon-shape p,#mermaid-_r_m_-1776715842853.image-shape p{background-color:rgba(232,232,232, 0.8);padding:2px;}#mermaid-_r_m_-1776715842853.icon-shape rect,#mermaid-_r_m_-1776715842853.image-shape rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-_r_m_-1776715842853:root{--mermaid-font-family:inherit;}</style><g><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="5" viewBox="0 0 10 10" id="mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" d="M 0 0 L 10 5 L 0 10 z"></path></marker><marker orient="auto" markerHeight="8" markerWidth="8" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" id="mermaid-_r_m_-1776715842853_flowchart-v2-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" d="M 0 5 L 10 10 L 10 0 z"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" id="mermaid-_r_m_-1776715842853_flowchart-v2-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" id="mermaid-_r_m_-1776715842853_flowchart-v2-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" r="5" cy="5" cx="5"></circle></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" id="mermaid-_r_m_-1776715842853_flowchart-v2-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" id="mermaid-_r_m_-1776715842853_flowchart-v2-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" d="M 1,1 l 9,9 M 10,1 l -9,9"></path></marker><g><g></g><g><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_A_B_0" d="M1025.977,86L1025.977,90.167C1025.977,94.333,1025.977,102.667,1026.047,110.417C1026.117,118.167,1026.258,125.334,1026.328,128.917L1026.398,132.501"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_C_1" d="M929.978,262.111L795.647,282.277C661.316,302.443,392.654,342.776,258.323,370.443C123.992,398.109,123.992,413.109,123.992,420.609L123.992,428.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_D_2" d="M935.407,267.539L847.168,286.801C758.93,306.063,582.453,344.586,494.215,367.348C405.977,390.109,405.977,397.109,405.977,400.609L405.977,404.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_E_3" d="M949.296,281.428L910.409,298.375C871.523,315.322,793.75,349.216,754.863,369.663C715.977,390.109,715.977,397.109,715.977,400.609L715.977,404.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_F_4" d="M1026.477,358.609L1026.393,362.693C1026.31,366.776,1026.143,374.943,1026.06,382.526C1025.977,390.109,1025.977,397.109,1025.977,400.609L1025.977,404.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_G_5" d="M1103.658,281.428L1142.377,298.375C1181.097,315.322,1258.537,349.216,1297.257,369.663C1335.977,390.109,1335.977,397.109,1335.977,400.609L1335.977,404.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_H_6" d="M1117.547,267.539L1205.618,286.801C1293.69,306.063,1469.833,344.586,1557.905,367.348C1645.977,390.109,1645.977,397.109,1645.977,400.609L1645.977,404.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_B_I_7" d="M1123.21,261.876L1260.17,282.081C1397.13,302.287,1671.049,342.698,1808.009,370.404C1944.969,398.109,1944.969,413.109,1944.969,420.609L1944.969,428.109"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_C_C1_8" d="M123.992,486.109L123.992,494.276C123.992,502.443,123.992,518.776,124.062,530.526C124.133,542.276,124.273,549.443,124.344,553.027L124.414,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_D_D1_9" d="M405.977,510.109L405.977,514.276C405.977,518.443,405.977,526.776,406.047,534.526C406.117,542.276,406.258,549.443,406.328,553.027L406.398,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_E_E1_10" d="M715.977,510.109L715.977,514.276C715.977,518.443,715.977,526.776,716.047,534.526C716.117,542.276,716.258,549.443,716.328,553.027L716.398,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_F_F1_11" d="M1025.977,510.109L1025.977,514.276C1025.977,518.443,1025.977,526.776,1026.047,534.526C1026.117,542.276,1026.258,549.443,1026.328,553.027L1026.398,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_G_G1_12" d="M1335.977,510.109L1335.977,514.276C1335.977,518.443,1335.977,526.776,1336.047,534.526C1336.117,542.276,1336.258,549.443,1336.328,553.027L1336.398,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_H_H1_13" d="M1645.977,510.109L1645.977,514.276C1645.977,518.443,1645.977,526.776,1646.047,534.526C1646.117,542.276,1646.258,549.443,1646.328,553.027L1646.398,556.61"></path><path marker-end="url(#mermaid-_r_m_-1776715842853_flowchart-v2-pointEnd)" style="" id="L_I_I1_14" d="M1944.969,486.109L1944.969,494.276C1944.969,502.443,1944.969,518.776,1945.039,530.526C1945.109,542.276,1945.25,549.443,1945.32,553.027L1945.39,556.61"></path></g><g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g><g><g transform="translate(0, 0)"></g></g></g><g><g transform="translate(1025.9765625, 47)" id="flowchart-A-0"><rect height="78" width="260" y="-39" x="-130" style=""></rect><g transform="translate(-100, -24)" style=""><rect></rect><foreignObject height="48" width="200"><p>OpenClaw is not working</p></foreignObject></g></g><g transform="translate(1025.9765625, 247.0546875)" id="flowchart-B-1"><polygon transform="translate(-111.0546875,111.0546875)" points="111.0546875,0 222.109375,-111.0546875 111.0546875,-222.109375 0,-111.0546875"></polygon><g transform="translate(-84.0546875, -12)" style=""><rect></rect><foreignObject height="24" width="168.109375"><p>What breaks first</p></foreignObject></g></g><g transform="translate(123.9921875, 459.109375)" id="flowchart-C-3"><rect height="54" width="158.890625" y="-27" x="-79.4453125" style=""></rect><g transform="translate(-49.4453125, -12)" style=""><rect></rect><foreignObject height="24" width="98.890625"><p>No replies</p></foreignObject></g></g><g transform="translate(405.9765625, 459.109375)" id="flowchart-D-5"><rect height="102" width="260" y="-51" x="-130" style=""></rect><g transform="translate(-100, -36)" style=""><rect></rect><foreignObject height="72" width="200"><p>Dashboard or Control UI will not connect</p></foreignObject></g></g><g transform="translate(715.9765625, 459.109375)" id="flowchart-E-7"><rect height="102" width="260" y="-51" x="-130" style=""></rect><g transform="translate(-100, -36)" style=""><rect></rect><foreignObject height="72" width="200"><p>Gateway will not start or service not running</p></foreignObject></g></g><g transform="translate(1025.9765625, 459.109375)" id="flowchart-F-9"><rect height="102" width="260" y="-51" x="-130" style=""></rect><g transform="translate(-100, -36)" style=""><rect></rect><foreignObject height="72" width="200"><p>Channel connects but messages do not flow</p></foreignObject></g></g><g transform="translate(1335.9765625, 459.109375)" id="flowchart-G-11"><rect height="102" width="260" y="-51" x="-130" style=""></rect><g transform="translate(-100, -36)" style=""><rect></rect><foreignObject height="72" width="200"><p>Cron or heartbeat did not fire or did not deliver</p></foreignObject></g></g><g transform="translate(1645.9765625, 459.109375)" id="flowchart-H-13"><rect height="102" width="260" y="-51" x="-130" style=""></rect><g transform="translate(-100, -36)" style=""><rect></rect><foreignObject height="72" width="200"><p>Node is paired but camera canvas screen exec fails</p></foreignObject></g></g><g transform="translate(1944.96875, 459.109375)" id="flowchart-I-15"><rect height="54" width="237.984375" y="-27" x="-118.9921875" style=""></rect><g transform="translate(-88.9921875, -12)" style=""><rect></rect><foreignObject height="24" width="177.984375"><p>Browser tool fails</p></foreignObject></g></g><g transform="translate(123.9921875, 579.609375)" id="flowchart-C1-17"><polygon transform="translate(-96.4921875,19.5)" points="-19.5,0 192.984375,0 212.484375,-39 0,-39"></polygon><g transform="translate(-88.9921875, -12)" style=""><rect></rect><foreignObject height="24" width="177.984375"><p>No replies section</p></foreignObject></g></g><g transform="translate(405.9765625, 579.609375)" id="flowchart-D1-19"><polygon transform="translate(-96.4921875,19.5)" points="-19.5,0 192.984375,0 212.484375,-39 0,-39"></polygon><g transform="translate(-88.9921875, -12)" style=""><rect></rect><foreignObject height="24" width="177.984375"><p>Control UI section</p></foreignObject></g></g><g transform="translate(715.9765625, 579.609375)" id="flowchart-E1-21"><polygon transform="translate(-81.6640625,19.5)" points="-19.5,0 163.328125,0 182.828125,-39 0,-39"></polygon><g transform="translate(-74.1640625, -12)" style=""><rect></rect><foreignObject height="24" width="148.328125"><p>Gateway section</p></foreignObject></g></g><g transform="translate(1025.9765625, 579.609375)" id="flowchart-F1-23"><polygon transform="translate(-106.3828125,19.5)" points="-19.5,0 212.765625,0 232.265625,-39 0,-39"></polygon><g transform="translate(-98.8828125, -12)" style=""><rect></rect><foreignObject height="24" width="197.765625"><p>Channel flow section</p></foreignObject></g></g><g transform="translate(1335.9765625, 579.609375)" id="flowchart-G1-25"><polygon transform="translate(-96.4921875,19.5)" points="-19.5,0 192.984375,0 212.484375,-39 0,-39"></polygon><g transform="translate(-88.9921875, -12)" style=""><rect></rect><foreignObject height="24" width="177.984375"><p>Automation section</p></foreignObject></g></g><g transform="translate(1645.9765625, 579.609375)" id="flowchart-H1-27"><polygon transform="translate(-96.4921875,19.5)" points="-19.5,0 192.984375,0 212.484375,-39 0,-39"></polygon><g transform="translate(-88.9921875, -12)" style=""><rect></rect><foreignObject height="24" width="177.984375"><p>Node tools section</p></foreignObject></g></g><g transform="translate(1944.96875, 579.609375)" id="flowchart-I1-29"><polygon transform="translate(-81.6640625,19.5)" points="-19.5,0 163.328125,0 182.828125,-39 0,-39"></polygon><g transform="translate(-74.1640625, -12)" style=""><rect></rect><foreignObject height="24" width="148.328125"><p>Browser section</p></foreignObject></g></g></g></g></g></svg>

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