---
source: "https://docs.discord.com/developers/platform/bots"
author:
published:
created: 2026-04-24
---
*Already familiar? Jump to the [Bots & Companion Apps docs](https://docs.discord.com/developers/bots/overview) or [Getting Started guide](https://docs.discord.com/developers/quick-start/getting-started).*

Bots are the most common type of Discord app. They appear in servers as bot users with an `APP` tag and can listen to events, respond to slash commands, moderate servers, send messages, and much more, all powered by your code via the Discord API.

Bots can connect to Discord in two ways: a persistent [Gateway WebSocket](https://docs.discord.com/developers/events/gateway) for real-time events, or an [HTTP interactions endpoint](https://docs.discord.com/developers/interactions/overview) for slash commands and UI components without a persistent connection. Most bots use one or both depending on their use case.

Common bot use cases include moderation tools, server utilities, games, integrations with external services, and automated workflows.

If you only need to push messages into a channel, a [webhook](https://docs.discord.com/developers/platform/webhooks) might be a better fit than a full bot. Webhooks are simpler to set up and can send messages with rich embeds, but they can’t listen to events or respond to interactions like bots can.

## [Bots Overview](https://docs.discord.com/developers/bots/overview)

What bots are, how they work, and when to use one.

## [Getting Started](https://docs.discord.com/developers/quick-start/getting-started)

Build and run your first Discord bot end to end.

## [Bot Dev Guides](https://docs.discord.com/developers/guides/bots)

Guides on interactions, components, monetization, and more.