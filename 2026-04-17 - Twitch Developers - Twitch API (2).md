---
source: "https://dev.twitch.tv/docs/api/"
author:
published: 2026-04-17
created: 2026-04-23
date created: Thursday, April 23rd 2026, 7:20:46 pm
date modified: Friday, April 24th 2026, 11:02:32 am
---

[Contents](#)

The Twitch API provides the tools and data used to develop Twitch integrations. The data models and systems are designed to provide relevant data in an easy, consistent, and reliable way. For the full list of endpoints that you can use in your integration, explore the [Twitch API Reference](https://dev.twitch.tv/docs/api/reference/).

The Twitch API uses OAuth 2.0 for authentication. To learn about the different types of access tokens that the API supports, see [Authentication](https://dev.twitch.tv/docs/authentication/). If you plan to use some of the extension-related endpoints, you’ll also need learn how to get JSON Web Tokens (JWT) (see [JSON Web Tokens](https://dev.twitch.tv/docs/extensions/required-technical-background#json-web-tokens-jwts) and [Managing Extension Secrets](https://dev.twitch.tv/docs/extensions/building#managing-extension-secrets)).

For information about using the APIs, see the following guides:

- [Starting a Poll](https://dev.twitch.tv/docs/api/polls)
- [Starting a Prediction](https://dev.twitch.tv/docs/api/predictions)
- [Starting a Raid](https://dev.twitch.tv/docs/api/raids)
- [Creating Stream Clips](https://dev.twitch.tv/docs/api/clips)
- [Creating Stream Markers](https://dev.twitch.tv/docs/api/markers)
- [Getting Videos](https://dev.twitch.tv/docs/api/videos)
- [Scheduling Broadcasts](https://dev.twitch.tv/docs/api/schedule)
- [Moderating a Broadcaster’s Chat](https://dev.twitch.tv/docs/api/moderation)
- [Getting a Creator’s Goals](https://dev.twitch.tv/docs/api/goals)
- [Getting an Extension Analytics Report](https://dev.twitch.tv/docs/insights#extension-developer-analytics)
- [Getting a Game Analytics Report](https://dev.twitch.tv/docs/insights#game-developer-analytics)

You should also become familiar with the following features:

| Feature | Description |
| --- | --- |
| [EventSub](https://dev.twitch.tv/docs/eventsub) | The Twitch API provides APIs that you can call to poll the status of a given resource. These APIs are fine if you need a snapshot of the resource but it’s recommended that you subscribe to receive resource updates instead. For information about subscribing to events, see [EventSub](https://dev.twitch.tv/docs/eventsub) subscriptions. |
| [Command-line Interface](https://dev.twitch.tv/docs/cli) | Twitch offers a command-line interface for managing Twitch resources. You can use it to call the Twitch endpoints, get an OAuth access token, and test EventSub events. |

## Next steps

Call your first Twitch API in minutes using [Getting started](https://dev.twitch.tv/docs/api/get-started).

Thumb through Twitch API [Concepts](https://dev.twitch.tv/docs/api/guide) to learn how Twitch [handles breaking changes](https://dev.twitch.tv/docs/api/guide#breaking-changes), [pagination](https://dev.twitch.tv/docs/api/guide#pagination), and [rate limits](https://dev.twitch.tv/docs/api/guide#twitch-rate-limits).

Join our [community](https://link.twitch.tv/devchat) of Twitch developers! And for other ways to connect with the community, explore our [developer support](https://dev.twitch.tv/support) page.