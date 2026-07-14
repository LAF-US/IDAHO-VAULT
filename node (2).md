---
authority: LOGAN
related:
- NETMESHWEB
- nodes
- swarm
- runtime
- gemini
- codex
---

# Local Node

This file records the current local machine as a NETMESHWEB node.

## Node Identity

- Host: Logan's 2015 Retina MacBook Pro
- OS: macOS 12.7.6
- Architecture: x86_64
- Role: local execution node for vault work, agent runtime, and terminal tooling

## Current Runtime State

- Machine profile: [Logan's 2015 Retina MacBook Pro Machine Profile.md](Logan%27s%202015%20Retina%20MacBook%20Pro%20Machine%20Profile.md)
- `nvm` Node: v24.15.0
- `npm`: 11.12.1
- `gemini`: installed globally via `npm install -g @google/gemini-cli`
- `gemini` resolves from `.nvm/versions/node/v24.15.0/bin/gemini`

## Known Constraint

Homebrew install paths are not reliable on this machine for `gemini-cli`
because the current formula chain pulls in `simdutf`, which fails to build
under macOS 12 / Xcode 14.2 / Apple clang 14.

Use the npm install path instead:

```bash
npm install -g @google/gemini-cli
gemini --version
```

## Local Tooling Posture

- Prefer `nvm`-managed Node for Node-based tooling.
- Keep runtime state inside the repo when the tool supports it.
- Use vault-local containment scripts when available for the active agent.
- Treat this machine as an execution node, not a source of governance.
