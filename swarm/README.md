# IDAHO-VAULT Swarm Loop (v0.1)

Minimal executable loop:

1. Trigger router with text input.
2. Route to `ingest` action.
3. Executor writes an output file into `INBOX/`.
4. Executor updates `/manifest.json`.

## Run

```bash
python swarm/app.py "process document"
```

## Test

```bash
python -m unittest swarm.tests.test_app
```
