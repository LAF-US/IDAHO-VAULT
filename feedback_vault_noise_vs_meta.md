---
name: vault-noise-vs-meta
description: "IDAHO-VAULT searches blend Logan's journalism corpus with vault-meta/doctrine; the valued skill is sifting noise from the mythic-governance layer"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 390ab942-699a-4361-9531-4a280ed00552
---

When searching IDAHO-VAULT, separate **real-world journalism content** from **vault-meta / doctrine content**, and lead the report with the meta layer. Logan explicitly praised this (2026-05-28, after a PAN/PANPIPES/PANIC search).

**Why:** The vault is a single git tree that mixes two very different corpora: (1) Logan's journalism archive — thousands of news articles, tweets (`tweets/`), Idaho politics files; and (2) the mythic-governance meta-layer — persona chambers (`.claude/`, `.pan/`, `.abhorsen/`), WITNESS/SIGNAL docs, the `!/` NEST, doctrine files. A naive `grep` drowns the signal: e.g. searching `panic` returns mostly **His·panic**, **pan·demic**, **pan·el**, **Pan·handle**, and news headlines — only one hit was the real `THE-PATH-AND-PAN` witness. Substring matching across a journalism corpus produces massive false-positive noise.

**How to apply:**
- Use `-l` (files-with-matches), word boundaries (`\bpanic\b`), and case-sense deliberately; avoid `-c`+`-l` combos (emit `:0` noise).
- Exclude noise dirs: `node_modules`, `go/pkg/mod`, `google-cloud-sdk`, `.obsidian/`, `/tool-results/`, `THE-GEMSTONE/...node_modules...`, `tweets/`.
- Filter substring traps when the query is a short token (`grep -viE "hispan|pandemic|panel|panhandle|japan|expan|compan|span"` for "pan").
- Check **filenames and dotfolders** (`find -iname`), not just contents — persona chambers and stubs (`.pan/PAN.md` = `[ ? ]`, unwritten-not-vacant) are the meta signal.
- Report structure: lead with the doctrine/meta files, then note the real-world hits as noise so Logan sees the distinction was made. Related: [[claude-abhorsen-waiting-address]], [[LAF / IDAHO-VAULT / Great Work]].
