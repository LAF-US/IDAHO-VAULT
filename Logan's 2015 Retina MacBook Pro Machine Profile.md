---
authority: LOGAN
status: draft
related:
- node
- nodes
- NETMESHWEB
- gemini
- codex
- runtime
- macOS
---

# Logan's 2015 Retina MacBook Pro Machine Profile

This profile covers this specific laptop operating surface for IDAHO-VAULT work, not every machine in the mesh.

## Identity

- Owner: Logan Finney
- Host class: 2015 Retina MacBook Pro
- Model identifier: MacBookPro12,1
- Role: local execution node for vault work, agent runtimes, and terminal tooling

## Hardware

- CPU: Intel Core i7, 3.1 GHz
- Cores: 2 physical cores
- Memory: 16 GB
- Architecture: x86_64
- Hyper-Threading: enabled

## Software

- OS: macOS 12.7.6
- Kernel: Darwin 21.6.0
- Boot volume: Macintosh HD
- SIP: enabled

## Runtime State

- `node`: v24.15.0 via `nvm`
- `npm`: 11.12.1
- `gemini`: installed globally via `npm install -g @google/gemini-cli`
- `gemini` path: `/Users/logan/.nvm/versions/node/v24.15.0/bin/gemini`
- `brew`: present, but not a reliable install path for current `gemini-cli` on this OS

## Tooling Notes

- Prefer `nvm`-managed Node for Node-based tooling.
- Prefer vault-local runtime containment scripts when available.
- Avoid Homebrew for packages that depend on current C++ formulas likely to fail on macOS 12.
- Treat this machine as an execution node, not a governance source.

## Known Constraint

Homebrew install path for `gemini-cli` fails on this machine because the current formula chain pulls in `simdutf`, which does not build cleanly under macOS 12 / Xcode 14.2 / Apple clang 14.

The working path is:

```bash
npm install -g @google/gemini-cli
gemini --version
```

## Verification Status

- `gemini` command verified.
- `node` and `npm` verified.
- Hardware and OS verified from local system reports.
- This profile is a draft record and can be promoted if Logan wants it canonicalized.
