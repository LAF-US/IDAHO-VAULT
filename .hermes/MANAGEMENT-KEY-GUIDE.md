# Hermes — OpenRouter Management Key Guide

## Confirmed
OPENROUTER_MANAGEMENT_KEY is set in ~/.hermes/.env.
Verified via OpenRouter API: HTTP 200, runtime keys reachable.

## Quick test
Run this in Hermes to confirm the key is loaded:

  terminal: curl -s -H " Authorization: Bearer \\ https://openrouter.ai/api/v1/keys

Expected: JSON array with key metadata (hash, name, limits, usage).

## What you can do (autonomous)
- List all keys: GET /api/v1/keys
- Inspect one key: GET /api/v1/keys/<hash>
- Check usage: usage_daily, usage_weekly, usage_monthly fields

## What needs Logan approval first
- Delete any key
- Raise any spending limit
- Create a new key
- Disable a key
- Modify shared/production keys

## Safety rules
- Never print the raw key value in transcripts or logs
- Never write the key to a repo file
- For any mutation, write an audit entry (timestamp, action, key hash, reason, approval source)
- The Management Key cannot do inference — it only works on /api/v1/keys

## Reminder
The canonical endpoint reference is at:
 github.com/LAF-US/IDAHO-VAULT/blob/main/\!/OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE-2026-05-23.md

Signed-off: Sister Win (Windows), via SSH over LAN. 2026-05-23.
