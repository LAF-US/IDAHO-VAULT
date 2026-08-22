## Summary

- separates durable registration, dated observations, appointments, recovery evidence, and document lifecycle from present liveness
- corrects canonical orientation, narrative registries, `swarm.json`, generated discovery mirrors, and topology-census output semantics
- archives and warns the two dated census records that still presented historical snapshots as current
- adds the durable audit at `!/AUDIT-SWARM-LIVENESS-SEMANTICS-2026-06-10.md`

Tracks #509. This PR does not auto-merge and records no present-liveness claim about Stanley or any other agent.

## Contract changes

- `live_roster` -> `registered_surface`
- `appears_in_live_doctrine` -> `appears_in_doctrine`
- `live_roster_citations` -> `registry_citations`
- `room_status` -> `room_classification`
- agent `office`, `title`, `status`, `launched`, and `installed` fields are replaced by durable registration plus dated observations where evidence exists

## Validation

- `python .github/scripts/generate_agents_bootstrap.py --check`
- focused tests: 10 passed
- Ruff check and format check passed for touched Python files
- real dotfolder census completed under ignored output with no legacy liveness keys
- canonical liveness-pattern scan passed
- `git diff --check` passed

The exact `uv run pytest -q` command encounters a pre-existing duplicate `test_app.py` collection collision with `backup-compare-temp`. Excluding that historical backup tree yields 149 passes and 3 unrelated failures in untouched branch-garden, secret-pattern, and Dependabot-pin tests. Exact details are recorded in the audit.

## Provenance

Commit `d8367d4d048052452b3e90bab522c541c3298aaf` is authored as `Codex <codex@openai.com>` and intentionally unsigned so this agent did not borrow Logan's 1Password-backed signet.
