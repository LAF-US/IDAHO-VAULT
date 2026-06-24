---
title: "What is Tailscale? · Tailscale Docs"
source: "https://tailscale.com/docs/concepts/what-is-tailscale"
author:
published: 2025-09-30
created: 2026-06-24
description: "Get a brief introduction to Tailscale."
---
## What is Tailscale?

Tailscale is a Zero Trust identity-based connectivity platform that replaces your legacy VPN, SASE, and PAM and connects remote teams, multi-cloud environments, CI/CD pipelines, Edge & IoT devices, and AI workloads.

Out-of-the-box, Tailscale solves many networking headaches. It has a customizable configuration to meet the demands of managing a distributed workforce. Tailscale helps provision for internal self-hosted and external third-party applications. It scales for growth as your requirements change.

Tailscale is an ideal solution for [DevOps](https://tailscale.com/solutions/devops), [IT](https://tailscale.com/solutions/it), and [Security](https://tailscale.com/solutions/security) teams.

## Technical details

Tailscale is a secure networking solution that streamlines connecting devices and services securely across different networks. It enables encrypted point-to-point connections using the open source [WireGuard](https://www.wireguard.com/) protocol, which means only devices on your private network can communicate with each other.

Tailscale creates a peer-to-peer mesh network (known as a tailnet). However, you can still use Tailscale like a traditional VPN by routing all traffic through an [exit node](https://tailscale.com/docs/features/exit-nodes).

![A user in Charleston connecting to a computer in New York City through a gateway in San Diego. This results in high latency because the gateway is on the opposite coast.](https://tailscale.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftraditional-vpn.0e10936c.png&w=3840&q=75)

Figure 1(a). The central gateway may or may not be close to users, thus resulting in higher latency. Because traffic is centralized, it can also act as a bottleneck, slowing down connections further.

![The same user in Charleston connecting to the New York City computer directly, thanks to Tailscale.](https://tailscale.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftailscale.4c5aa989.png&w=3840&q=75)

Figure 1(b). With Tailscale, each device is connected to the other directly, resulting in lower latency.

The Tailscale approach avoids centralization where possible, resulting in both [higher throughput](https://tailscale.com/blog/more-throughput) and lower latency as network traffic can flow directly between devices. Additionally, decentralization improves stability and reliability by reducing single points of failure.

For more information, refer to [how Tailscale works](https://tailscale.com/blog/how-tailscale-works).

## Benefits

Some key advantages of Tailscale include secure and private connections between devices, a flexible network topology, and a streamlined setup. Tailscale is also cross-platform, infrastructure agnostic, and highly configurable. It supports the [features](https://tailscale.com/features) you need and the [integrations](https://tailscale.com/integrations) that you currently use.

For more information, refer to [why Tailscale is right for you](https://tailscale.com/why-tailscale).

### Streamlined setup

You can deploy a tailnet in minutes without requiring extensive configuration, server setup, and networking expertise. After you create an account, authenticating two or more devices automatically creates a tailnet with a sensible set of [default access policies](https://tailscale.com/docs/reference/examples/acls#allow-all-default-acl).

Connections between tailnet devices work seamlessly across firewalls and [Network Address Translation (NAT)](https://tailscale.com/blog/how-nat-traversal-works) without requiring port forwarding or complex firewall rules. This "zero config" approach dramatically reduces the technical barriers to implementing secure networking, making it accessible to technical and non-technical users.

### Security and privacy

The [Tailscale security model](https://tailscale.com/security) is built on modern, proven technologies and best practices such as end-to-end [encryption](https://tailscale.com/docs/concepts/tailscale-encryption) and a [zero-trust architecture](https://tailscale.com/docs/concepts/zero-trust). At its core, Tailscale uses WireGuard, a state-of-the-art VPN protocol known for its security and performance. This foundation is enhanced by Tailscale's commitment to [compliance](https://tailscale.com/security#compliance-and-certifications), [security policies](https://tailscale.com/security-policies), and [security features](https://tailscale.com/security#security-features) such as [access control policies](https://tailscale.com/docs/features/access-control) and [Tailnet Lock](https://tailscale.com/docs/features/tailnet-lock).

### Scalability and adaptability

Tailscale's flexible architecture is designed to grow seamlessly with your organization's needs. Whether you're scaling from a small team to a large enterprise or expanding across multiple geographic locations, Tailscale maintains its performance and security characteristics at scale. The distributed nature of its architecture means that adding new devices or users doesn't create bottlenecks that typically plague traditional VPN solutions.

## Use cases

With its low barrier to getting started, versatility, and powerful capabilities, Tailscale seamlessly scales from personal use to enterprise deployments. Developers can use it to share work-in-progress features with their team, homelab enthusiasts can use it to [access their media servers remotely](https://tailscale.com/use-cases/homelab), and businesses can use it to [secure their distributed workforce](https://tailscale.com/use-cases/zero-trust-networking), all without the hassle and overhead of traditional infrastructure setup and maintenance.

- Business Virtual Private Network (VPN): Replace your legacy VPN and enable secure remote access to infrastructure.
- Privileged Access Management (PAM): Enable Zero Trust with just-in-time access and robust recording.
- Workload connectivity: Connect pipelines, apps, and Kubernetes workloads.
- Continuous Integration and Continuous Delivery (or Deployment) (CI/CD): Granular secure access to every runner and workload.
- Edge and Internet of Things (IoT): Access, manage, and monitor thousands of devices.
- Securing Artificial Intelligence (AI): Unified AI governance for AI agents and users.

For more information, refer to [Tailscale Testimonials](https://tailscale.com/customers) and [Tailscale Use Cases](https://tailscale.com/docs/use-cases)!

## Get started

Getting started is as simple as creating an account, installing the Tailscale client, and logging into two or more devices. Visit the [quickstart guide](https://tailscale.com/docs/how-to/quickstart) to learn more.