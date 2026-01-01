---
title: "Sourcegraph API - Sourcegraph docs"
source: "https://sourcegraph.com/docs/api"
author:
published:
created: 2026-08-12
description: "Documentation for Sourcegraph, the code intelligence platform."
---
## Sourcegraph API

Starting in [Sourcegraph 7.0](https://sourcegraph.com/changelog/releases/7.0), a new versioned external API is being introduced for custom integrations (see the [announcement](https://sourcegraph.com/changelog/sourcegraph-api)). The currently available API surface can be seen in `/api-reference` (e.g. `https://sourcegraph.example.com/api-reference`). From this page, integrators can view the available operations and download the OpenAPI schema. We are committed to supporting integrations built on top of these new APIs with backwards compatibility and migration assistance for breaking changes.

The new Sourcegraph API is a work in progress, and capabilities are gradually being ported over. If you have an integration you'd like to build that is not currently served by the new Sourcegraph API, please reach out at [support@sourcegraph.com](mailto:support@sourcegraph.com).

For specific types of integrations, Sourcegraph also offers the following APIs:

- [Sourcegraph streaming search API](https://sourcegraph.com/docs/api/stream-api), for consuming search results as a stream of events
- [Sourcegraph MCP server](https://sourcegraph.com/docs/api/mcp), for connecting AI agents and applications to Sourcegraph's code search capabilities
- [Sourcegraph Analytics API](https://sourcegraph.com/docs/analytics/api), for accessing your Sourcegraph Analytics data
- [Webhooks](https://sourcegraph.com/docs/admin/webhooks), for receiving event notifications from Sourcegraph

For diagnostics use cases, the [Sourcegraph GraphQL debug API](https://sourcegraph.com/docs/api/graphql) is also available without any compatibility guarauntees.

The Sourcegraph GraphQL API has historically been an internal interface without formal compatibility guarantees. For external integrations, [Sourcegraph 7.0](https://sourcegraph.com/changelog/releases/7.0) introduces a new, supported API at `/api-reference`. The GraphQL API remains available, but we recommend migrating to the new API for a stable integration experience.

If you have a use case that is not currently served by the new Sourcegraph API, please reach out at [support@sourcegraph.com](mailto:support@sourcegraph.com).