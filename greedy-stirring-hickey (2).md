# Plan: Start Flask Dev Server (Nest Bridge)

## Context
User requested dev server detection → launch.json created → user asked for explanation → ready to start.

## Action
Call `preview_start` with the configuration from `.claude/launch.json`:
- `runtimeExecutable`: `python`
- `runtimeArgs`: `["main.py"]`
- `port`: 8080

## Verification
- Server starts without import errors
- Preview URL resolves on port 8080
- POST to `/` returns 200 OK
