---
name: no-hand-coded-path-lists
description: "Logan rejects hand-coded per-path lists in config (gitattributes, ignore rules, annex opt-ins) — use rules/predicates/classes instead"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9b5c47c2-4310-480f-b65a-5c266658dd92
  modified: 2026-08-18T03:09:43.802Z
---

Logan strongly rejects hand-coded per-path lists in configuration — one line per file/path in `.gitattributes`, annex `largefiles` opt-ins, anchored per-config-file rules, and similar. Quote: "hand-coded per path lists? I have been weeding those out of the muck for weeks. fuck that" (2026-08-17, on an incoming `.gitattributes` with `* annex.largefiles=nothing` + per-path `filter=annex` opt-ins).

**Why:** They rot, they don't scale, and Logan has spent weeks removing them from the vault. A mechanism that *requires* enumeration (like `largefiles=nothing` forcing one rule per annexed file) is a design flaw, not a config style.

**How to apply:** Prefer class/extension rules (`*.mp4`), predicates (`largerthan=2gb`), anchored single guards (`/.ollama/**`), or explicit-only tooling behavior (annex with `largefiles` unset) over enumerating paths. When reviewing incoming config, flag list-shaped mechanisms before merging rather than adopting them "for now." See [[idaho-vault-storage-architecture]].
