# MCP PR Prep

## Proposed PR Title

Add MCP transport guardrails and Obsidian REST client scaffold

## Proposed PR Summary

This PR adds the first implementation slice for MCP integration in IDAHO-VAULT by introducing reusable transport guardrails and a guarded Obsidian Local REST API client under `.github/scripts/`.

## Proposed PR Body

### What this changes

- adds `.github/scripts/mcp_guardrails.py`
- adds `.github/scripts/obsidian_rest_api_client.py`
- standardizes live-write gating, correlation IDs, idempotency keys, and MCP action logs
- provides a safe CLI for interacting with the installed Obsidian Local REST API plugin
- defaults write and patch operations to dry-run

### Validation

- confirmed both new files are syntax-clean
- executed the client in dry-run mode successfully
- fixed a dry-run bug where non-live writes still required an API key

### What this does not do

- does not modify governance files under `!/`
- does not perform live plugin writes
- does not add a relay or self-hosted path for GitHub-hosted automation to reach a local Obsidian endpoint

### Review focus

- does the guardrail model match the intended MCP rollout?
- is the Obsidian Local REST API the right first transport surface?
- should the next increment be a read-only live smoke test or a Linear-first pilot wrapper?

## Pull Checklist

- [ ] Confirm only the MCP implementation files are included in the PR scope
- [ ] Exclude unrelated worktree changes from the final PR
- [ ] Decide whether to add a live local smoke test before opening the PR
- [ ] Post the prepared Linear/Slack updates if external channel sync is still needed
