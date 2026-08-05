---
title: "GitHub App installation tokens: Per-request override header"
source: "https://github.blog/changelog/2026-05-15-github-app-installation-tokens-per-request-override-header/"
author:
  - "[[Allison]]"
published: 2026-05-15
created: 2026-06-30
description: "As announced in April 2026, GitHub is rolling out a new token format for GitHub App installation tokens. To help you validate your apps and workflows before the rollout reaches…"
---
As [announced in April 2026](https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens), GitHub is rolling out a new token format for GitHub App installation tokens. To help you validate your apps and workflows before the rollout reaches you, we’re providing a temporary request header that lets you force either token format on demand.

## What is the header?

Setting `X-GitHub-Stateless-S2S-Token` on a `POST /app/installations/:installation_id/access_tokens` request overrides the server-side rollout decision for that single request.

| Header value | Effect |
| --- | --- |
| `enabled` | Returns a **stateless** (JWT-format) token, regardless of where you are in the rollout. |
| `disabled` | Returns a **stateful** (classic opaque) token, even if your integration is already included in the rollout. |
| *(absent)* | Normal rollout behavior (i.e., no override). |

Any other value (`true`, `false`, `1`, `0`, etc.) is silently ignored and given the standard rollout behavior.

The header is supported on the [`POST /app/installations/:installation_id/access_tokens`](https://docs.github.com/rest/apps/apps#create-an-installation-access-token-for-an-app) REST API.

## How to use it

### Before the rollout reaches your app, test proactively

Use `enabled` to request a stateless token on demand and validate that your application handles it correctly.

When creating an installation access token, send the `X-GitHub-Stateless-S2S-Token: enabled` request header to force the new token format in the response. For full endpoint details and request examples, see the [REST API documentation for creating an installation access token for an app](https://docs.github.com/rest/apps/apps#create-an-installation-access-token-for-an-app).

A stateless token is a **`ghs_` -prefixed JWT**. It is **longer (~520 characters)** and contains **two dots**. In contrast, a stateful token is a short opaque string with **no dots**.

Things to check in your app:

- No hardcoded token length assumptions
- Any regex used to validate an installation token is updated to handle additional underscores and the presence of a JWT. Our recommended regex to match both new and current format tokens is `ghs_[A-Za-z0-9\.\-_]{36,}`.
- Database columns for token storage and header settings accept at least 520 characters
- Any token introspection or validation code treats `ghs_` tokens as opaque strings

*Editor’s note (May 26th, 2026): Updated the regex format guidance.*

### During the rollout, temporarily opt out if you need more time

If the rollout reaches your app before you’re ready, you can set the header with `disabled` to continue receiving stateful tokens while you update your application.

## Verifying the token type

You can verify the token type by checking the number of dots after the `ghs_` prefix: a stateless JWT-format token has two dots, while a stateful opaque token has no dots.

## Scope

- The header is temporary. At a future deprecation point, to be announced separately in the coming weeks, it will no longer be respected. At that point, all eligible apps will unconditionally receive stateless tokens. Remove the header from your production code once you have validated both token formats.
- Existing app installation tokens continue to work until they expire.
- This change applies to GitHub Enterprise Cloud and Data Residency environments. GitHub Enterprise Server isn’t impacted by this change.
- Upcoming rollouts will apply the new token format only to GitHub App installation server-to-server tokens, including Actions GITHUB\_TOKEN.
- We’ll share more details in the coming weeks on planned format changes for user-to-server tokens used in Copilot code review flows.

## How to prepare

1. **Test with `enabled`:** Call the endpoint with the opt-in header and verify your app accepts the new token format end-to-end.
2. **Test with `disabled`:** Confirm your app also works with the classic opaque format, so it degrades gracefully if stateless tokens are ever temporarily unavailable.
3. **Remove the header:** Once both paths are validated, remove the header. GitHub’s rollout will then automatically manage the token format.

Join the discussion within [GitHub Community](https://github.com/orgs/community/discussions/categories/announcements).

*Editor’s note (June 10, 2026): Removed link about contacting support since it was causing confusion.*[Back to top](#start-of-content)