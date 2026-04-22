# .github/probes

Artifacts from minimum-viable round-trip workflows — proof that an Action can
call an external service and commit the response back to the repo.

Each probe workflow writes one JSON file here. The presence and freshness of
the file is the signal the loop is intact. These aren't meant to be merged
into vault content surfaces (daily notes, `TO DO LIST.md`) — they're the
plumbing check.

| File | Workflow | Purpose |
|---|---|---|
| `todoist-last-sync.json` | `.github/workflows/todoist-probe.yml` | Latest `GET /rest/v2/tasks` response |
