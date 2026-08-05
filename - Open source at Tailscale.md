---
title: "Open source at Tailscale"
source: "https://tailscale.com/opensource"
author:
published:
created: 2026-07-02
description: "Read about Tailscale’s open source projects and commitment. Learn how Headscale helps Tailscale users."
---
We believe that open source is the past, present, and future of software development. When a Tailscalar, or anyone else, contributes to open source code, it benefits everyone.

## Developing in the open

[Tailscale is largely open source](https://github.com/tailscale/tailscale) and consists of the following elements:

1. The client, which runs on each of a user’s devices, is mostly open source. The [core client code for the Tailscale daemon](https://github.com/tailscale/tailscale) used across all platforms is open source, and the full client code is open source for platforms that are also open source.
2. We enthusiastically support open source operating systems such as [Linux](https://github.com/tailscale/tailscale) and [Android](https://github.com/tailscale/tailscale-android), and we believe in directing time and energy to support the communities around these platforms. As a result, where the operating system is open source, the daemon and GUI are open source; and where the operating system is closed, the daemon is open source and the GUI is closed source.
3. This means that you can build the Linux and Android clients yourself, and you can build the Windows and [macOS](https://github.com/tailscale/tailscale/wiki/Tailscaled-on-macOS) clients without the GUI.
4. Open source [Designated Encrypted Relay for Packets](https://pkg.go.dev/tailscale.com/derp) (DERP) relay servers. You might [self-host your own DERP server](https://tailscale.com/kb/1118/custom-derp-servers#reasons-to-run-a-custom-derp-server) for latency or compliance reasons.
5. A closed source coordination server.

### Why bother making any part of Tailscale open source?

- **To improve trust and transparency.** Anyone can review our code and see how Tailscale really works. We hope this increases your trust in using Tailscale.
- **To share what we’ve learned.** When we started Tailscale, mesh overlay networking was complex to set up and use, where it existed at all. By working in the open, we’ve helped lead a shift in considering what’s possible and how approachable it can be.
- **To allow for adaptability.** We understand the desire not to be locked into a specific provider.
- **To make it easier to get feedback.** By keeping our [issues](https://github.com/tailscale/tailscale/issues) and [feature requests](https://github.com/tailscale/tailscale/issues?q=is%3Aissue+is%3Aopen+label%3Afr) public, you can upvote them (with emojis please!) or submit new requests, and we can prioritize what’s really needed for our users right now.

If you’d like to contribute to Tailscale, then by all means do! Please follow our [contribution guidelines](https://github.com/tailscale/tailscale#contributing) and our [code of conduct](https://github.com/tailscale/tailscale/blob/main/CODE_OF_CONDUCT.md). [We appreciate it.](https://tailscale.com/blog/code-thanksgiving)

### Financial support for open source projects and maintainers

[Tailscale donates annually to WireGuard®](https://www.wireguard.com/donations/). Tailscale is built on [WireGuard®](https://www.wireguard.com/), specifically wireguard-go. As we develop Tailscale and add new functionality, we also upstream those changes to help other users of the project.  
  
Tailscale also supports [several other projects and maintainers we depend on](https://github.com/orgs/tailscale/sponsoring), as well as [Let’s Encrypt](https://letsencrypt.org/), which we use to [issue TLS certificates](https://tailscale.com/kb/1153/enabling-https).

### Contributing to open source

Tailscale open sources internal projects that other organizations might benefit from, such as:

- [depaware](https://github.com/tailscale/depaware), for tracking your Go dependencies.
- [ToBeReviewed bot](https://github.com/tailscale/ToBeReviewedBot), for auditing emergency production changes.
- Our [internal security policies](https://github.com/tailscale/security-policies), for reference when developing your own security policies.

When a project originally developed by the community becomes critical to our users, if the maintainers are willing, we adopt the project and take responsibility for ongoing support and development. For example, this is what happened with the Tailscale [Synology package](https://tailscale.com/kb/1131/synology) (thanks Guilherme de Maio!) and [Terraform provider](https://tailscale.com/kb/1210/terraform-provider) (thanks David Bond!).  
  
Tailscalars are also encouraged to contribute to other open source projects they rely on as part of their jobs, or that they feel passionate about. Tailscalars contribute to the Go project and community, NixOS, and more.

### Encouraging Headscale

[Headscale](https://github.com/juanfont/headscale) is an open-source implementation of Tailscale’s coordination server. It is developed independently and separately from Tailscale. Kristoffer Dalby works at Tailscale, such that Tailscale can support his efforts to develop Headscale.

Tailscale does not set Headscale’s product direction or manage its community, and does not prohibit Tailscale employees from contributing to Headscale.

A healthy Headscale project is good for the broader Tailscale ecosystem. It gives technical users a self-hosted way to experiment with the Tailscale protocol, helps demonstrate that the protocol surface can work beyond a single managed service, and contributes to long-term ecosystem diversity and resilience.

We like seeing people build, tinker, and learn on top of the Tailscale protocol and platform. Headscale gives self-hosting communities a way to do that on their own terms, especially in homelab or infrastructure-sovereignty use cases.

At the same time, Headscale is a community-maintained project, not Tailscale-managed or part of the supported Tailscale product. We want Headscale to succeed, but we also want the distinction to be clear: Tailscale is the managed, production-ready service for teams that want simplicity, reliability, governance, and support; Headscale is for users who want to run and maintain their own control plane.

#### How do I choose between Tailscale or Headscale?Tailscale and Headscale serve different needs.

Headscale is a community-maintained, self-hosted control plane for users who prioritize tinkering, homelabbing, or infrastructure sovereignty. It offers more control, but with added operational complexity and a narrower scope than Tailscale’s managed service.

Tailscale is the fastest way to connect your devices, users, and services with a fully managed control plane, zero infrastructure to run, and enterprise-ready features like ACLs, SSO integrations, multiple tailnets, governance, reliability, and a full support apparatus. With 6 users and unlimited personal devices on our free-tier, there’s plenty of runway to give Tailscale a try.

We see Headscale as a healthy part of the broader Tailscale ecosystem, and we hope this makes clear that we want the project to succeed.

### Providing Tailscale to open source projects

[Tailscale is free for open source projects](https://tailscale.com/blog/community-github-pricing). With the [Community on GitHub plan](https://tailscale.com/kb/1154/free-plans-discounts#community-on-github), you can use Tailscale for your project to access and share project resources, like a build tool or a test server. Any open source project with an [OSI license](https://opensource.org/licenses/) can use this plan. Currently, this plan requires using GitHub for authentication.

## FAQs

### Is Tailscale open source?

Tailscale’s core client code, including the `tailscaled` daemon and `tailscale` CLI, is open source, as is the DERP relay server code. Tailscale is built on the open-source WireGuard® protocol, and the client-side implementation of Tailscale’s coordination/control protocol is available in the open-source client.

Tailscale also works with the independent [Headscale](https://github.com/juanfont/headscale) project to help maintain compatibility with Tailscale clients. Headscale provides an open-source, self-hostable coordination server for single-tailnet use cases. Tailscale’s own hosted coordination server remains proprietary as part of our managed service.

### How do I contribute to Tailscale?

You can contribute code, bug reports, and feature requests to [Tailscale on GitHub](https://github.com/tailscale/tailscale). Please follow our [contribution guidelines](https://github.com/tailscale/tailscale#contributing) and our [code of conduct](https://github.com/tailscale/tailscale/blob/main/CODE_OF_CONDUCT.md).

### What is Headscale? Is it run by Tailscale?

[Headscale](https://github.com/juanfont/headscale) is an independent, community-maintained, open-source coordination server for Tailscale clients. Headscale serves notably different needs than Tailscale. Tailscale employs the head maintainer of Headscale, but does not direct or steer the project. See “Encouraging Headscale” for more information.

### How does Tailscale decide which projects and maintainers to support financially?

Tailscale strives to sponsor open source projects that are critical to our product. Eligible projects must have an [OSI-approved license](https://opensource.org/licenses), code of conduct, and a way to be sponsored, such as GitHub Sponsors or Open Collective. We prefer to sponsor projects rather than individuals, and we don’t typically consider projects that are primarily commercial or corporate-backed. We may not financially support a project that we already support in other ways.

### Why does my account say “Thanks!” on it?

We value open source contributions and the maintainers we rely on. If you’ve contributed to Tailscale or a project we rely on, [we’re saying thanks with a free Personal Pro account](https://tailscale.com/blog/code-thanksgiving). You should see a heart over your profile in your Tailscale account. (If you should have one and it’s not there, [let us know](https://tailscale.com/contact/support).)