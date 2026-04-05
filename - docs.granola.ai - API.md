---
source: https://docs.granola.ai/introduction.md
author: null
published: null
created: 2026-04-02
related:
- '2026-04-02'
- '300'
- '404'
- '429'
- API
- budget
- index
- meeting
- window
authority: LOGAN
---
```
> ## Documentation Index
> Fetch the complete documentation index at: https://docs.granola.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Granola API

> Granola API documentation. Programmatic access to meeting notes, transcripts, and AI summaries.

The Granola API provides programmatic access to your workspace's meeting notes and related data. This RESTful API enables you to integrate Granola with your existing tools, build custom workflows, and extract insights from your meeting documentation.

## API Key Types

There are two types of API, with different scopes:

| Key type                    | Who can create       | Plan required          | What it can access                                                                      |
| --------------------------- | -------------------- | ---------------------- | --------------------------------------------------------------------------------------- |
| **Personal API key** (Beta) | Any workspace member | Business or Enterprise | Notes you own, notes directly shared with you, notes in private folders shared with you |
| **Enterprise API key**      | Workspace admin      | Enterprise             | All notes in the Team space                                                             |

On Enterprise plans, workspace admins can enable or disable Personal API key creation for their workspace in **Settings → Workspace**.

## Obtaining an API Key

1. Open the Granola desktop app
2. Navigate to **Settings → API**
3. Click **Create new key**
4. Choose a key type (if prompted) and click **Generate API Key**

<Note>
  On Enterprise plans, Personal API key creation must be enabled by a workspace admin via the "Allow personal API keys" toggle in **Settings → Workspace**.
</Note>

## Quick Start

\`\`\`bash  theme={null}
# List notes created this week
$ curl "https://public-api.granola.ai/v1/notes?created_after=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer grn_YOUR_API_KEY"
{
  "notes": [ ... ],
  "hasMore": true,
  "cursor": "eyJjcmVkZW50aWFsfQ=="
}

# Get the next page using the cursor
$ curl "https://public-api.granola.ai/v1/notes?created_after=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)&cursor=eyJjcmVkZW50aWFsfQ==" \
  -H "Authorization: Bearer grn_YOUR_API_KEY"
{
  "notes": [
    { "id": "not_1d3tmYTlCICgjy", "title": "Quarterly yoghurt budget review", ... },
    ...
  ],
  "hasMore": false
}

# Get that note with its transcript
# (use the not_ ID from the list response, not a UUID)
$ curl "https://public-api.granola.ai/v1/notes/not_1d3tmYTlCICgjy?include=transcript" \
  -H "Authorization: Bearer grn_YOUR_API_KEY"
{
  "id": "not_1d3tmYTlCICgjy",
  "title": "Quarterly yoghurt budget review",
  "owner": { "name": "Oat Benson", "email": "oat@granola.ai" },
  "summary": "The quarterly yoghurt budget review was a success. ...",
  "transcript": [
    { "speaker": { "source": "microphone" }, "text": "I'm done pretending. Greek is the only yoghurt that deserves us." },
    { "speaker": { "source": "speaker" }, "text": "Finally. Regular yoghurt is just milk that gave up halfway." }
  ],
  ...
}
\`\`\`

<Info>
  The API only returns notes that have a **generated AI summary and transcript**. Notes that are still being processed or were never summarized won't appear in responses — the List Notes endpoint excludes them, and the Get Note endpoint returns a 404.
</Info>

## Rate Limits

Rate limits are applied per workspace to ensure fair usage and platform stability. For Personal API keys, rate limits are applied per user.

| Metric         | Value                          |
| -------------- | ------------------------------ |
| Burst capacity | 25 requests                    |
| Time window    | 5 seconds                      |
| Sustained rate | 5 requests/second (300/minute) |

When rate limits are exceeded, the API returns a \`429 Too Many Requests\` response.

Built with [Mintlify](https://mintlify.com).
```