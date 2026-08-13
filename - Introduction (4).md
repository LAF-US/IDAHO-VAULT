---
title: "Introduction"
source: "https://open.manus.ai/docs/v2/introduction"
author:
published:
created: 2026-08-13
description: "Integrate Manus AI agents into your workflows with the Manus API"
---
<sup>Questions or issues? Contact us at <a href="mailto:api-support@manus.ai">api-support@manus.ai</a>.</sup>

**You are viewing API v2** — the latest version of the Manus API. API v1 has been deprecated and will be removed in the future. If you still need the v1 docs, see [API v1 documentation](https://open.manus.ai/docs/v1/overview).

## Manus API

The Manus API allows you to programmatically create and manage AI agent tasks. Build automations, orchestrate multi-step workflows, and integrate Manus into your applications through a simple REST API.

## [Get your API key](https://open.manus.ai/docs/v2/authentication)

Before making API calls, you’ll need to create an API key. Head over to Authentication to get started.

## [Install the API skill](https://open.manus.ai/docs/v2/manus-api-skill)

Give Codex and other compatible coding agents current Manus API integration guidance.

## What you can do

## Base URL

All API requests are made to:

```text
https://api.manus.ai
```

## Response format

All responses use a consistent wrapper:

**Success:**

```json
{
  "ok": true,
  "request_id": "req_abc123",
  ...
}
```

**Error:**

```json
{
  "ok": false,
  "request_id": "req_abc123",
  "error": {
    "code": "invalid_argument",
    "message": "task_id is required"
  }
}
```

| Error code | Description |
| --- | --- |
| `invalid_argument` | Missing or invalid request parameters |
| `not_found` | The requested resource does not exist |
| `permission_denied` | API key lacks permission for this action |
| `rate_limited` | Too many requests — see [Rate Limits](https://open.manus.ai/docs/v2/rate-limits) for per-endpoint limits and backoff guidance |