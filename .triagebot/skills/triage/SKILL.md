---
name: triage
description: Triage a bug report for IDAHO-VAULT. Reproduces the bug, diagnoses the root cause, verifies whether the behavior is intentional, and attempts a fix.
---

# Triage for IDAHO-VAULT

Triage a bug report end-to-end: reproduce the bug, diagnose the root cause, verify whether the behavior is intentional, and attempt a fix.

## General Rules

**Do not get stuck on infrastructure problems.** If a tool is unavailable in the CI environment — bail out after 2 attempts and write your report with the data you already have. A partial report with solid findings is infinitely more valuable than no report because you ran out of time.

## Input

You need either:

- `issueTitle` and `issueBody` provided in args (preferred — use these directly as the bug report), OR
- A GitHub issue number or URL mentioned in the conversation (use `gh issue view` to fetch details)

If a `triageDir` is provided in args, use that as the working directory for the triage. It must be outside the repository root. Otherwise, default to a sibling directory: `../triage-gh-<issue_number>` (if you have an issue number) or `../triage-current`.

## Step 1: Reproduce

Read and follow [reproduce.md](reproduce.md) directly. Complete this bounded step before continuing.

After completing reproduction, check the result:

- If the issue was **skipped** (host-specific, unsupported version, etc.) — skip to Output.
- If the issue was **not reproducible** — skip to Output.
- If the issue was **reproduced** — continue to Step 2.

## Step 2: Diagnose

Read and follow [diagnose.md](diagnose.md) directly. Complete this bounded step before continuing.

After completing diagnosis, check your confidence:

- If confidence is **low** — skip to Output.
- If confidence is **medium** or **high** — continue to Step 3.

## Step 3: Verify

Read and follow [verify.md](verify.md) directly. Complete this bounded step before continuing.

After completing verification, check the verdict:

- If the verdict is **intended-behavior** — skip to Output. The issue is not a bug; do not attempt a fix.
- If the verdict is **bug** or **unclear** — continue to Step 4.

## Step 4: Fix

Read and follow [fix.md](fix.md) directly. Complete this bounded step before continuing.

Whether the fix succeeds or fails, continue to Output.

## Output

After completing the triage (or exiting early), return your structured results so the orchestrator can post a comment and manage labels.
