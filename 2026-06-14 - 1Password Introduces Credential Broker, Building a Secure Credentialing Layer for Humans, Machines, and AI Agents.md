---
title: "1Password Introduces Credential Broker, Building a Secure Credentialing Layer for Humans, Machines, and AI Agents"
source: "https://1password.com/press/2026/june/credential-broker"
author:
  - "[[David Faugno]]"
published: 2026-06-14
created: 2026-06-24
description: "The acquisition extends 1Password’s identity security platform beyond securing credentials to governing what every human, machine, and AI identity can access."
---
*Building on the 1Password vault trusted by more than 180,000 businesses, including GitHub, MongoDB, Salesforce, and Wiz, the new 1Password Credential Broker brokers trusted access from 1Password at the time of need, helping organizations keep secrets out of apps, code, pipelines, and agent workflows.*

**TORONTO –** [1Password](https://1password.com/), a leader in identity security, today announced 1Password Credential Broker, a new product that securely brokers credentials, tokens, and federated access from 1Password to trusted requesters. The 1Password Credential Broker is available in private beta today, with support for GitHub Actions and a roadmap that extends trusted access across humans, machine workloads, and AI agents through a common identity fabric.

For two decades, 1Password has helped consumers and businesses protect the credentials they use to access critical systems. But credentials are no longer requested only by people signing in through a browser. Modern enterprises now depend on employees, CI/CD pipelines, cloud workloads, service accounts, and AI agents, each of which needs credentials to get work done. Those credentials are often copied into applications, repositories, configuration files, environment variables, and pipelines where they are difficult to govern, rotate, and audit.

The 1Password Credential Broker extends the role of 1Password from storing secrets to brokering credentials for the humans, machines, and agents that need them. Instead of distributing long-lived secrets across tools and environments, organizations can keep credentials protected in 1Password and release only the approved credential, token, or access artifact to a trusted requester when work needs to happen.

"1Password has always been the place enterprises trust to keep credentials safe. The next step is making that same source of truth work for every credential, whether it is requested by a person, a workflow, or an AI agent," said Nancy Wang, CTO at 1Password. "The 1Password Credential Broker is about closing the gap between where credentials are protected and where access happens. It helps organizations move away from credentials copied across environments and toward credentials brokered from 1Password, based on trusted identity and logged delivery."

## From Stored Secrets to Brokered Credentials

The 1Password Credential Broker acts as a trusted intermediary between an actor that needs a credential and the system where that credential is stored or issued. In the initial private beta flow, the 1Password Credential Broker uses GitHub Actions identity signals to verify a specific workflow before releasing an approved credential to that workload.

With the 1Password Credential Broker, organizations can:

- Reduce long-lived credentials in applications, repositories, configuration files, service accounts, and CI/CD pipelines.
- Verify trusted identity signals before releasing credentials, beginning with GitHub Actions workload identity.
- Deliver approved credentials and tokens when needed rather than copying them across environments.
- Create an audit trail of credential requests and delivery events.
- Bring human, machine, and agent credential delivery into the same trusted platform.
- Build toward a common credential source of truth for every actor that needs access.

For organizations already using 1Password to manage credentials and secrets, the 1Password Credential Broker provides a path from vaulting credentials to brokering credentials at the moment of use. It helps teams keep credentials protected in 1Password while making them available to trusted requesters when work needs to happen.

## Designed to Keep Credentials out of Plaintext and Secured in 1Password Vaults

The 1Password Credential Broker is built around a simple principle: credentials should stay protected in 1Password until they are needed by a trusted requester. In the initial GitHub Actions flow, a workflow presents trusted identity signals to 1Password. The 1Password Credential Broker validates those signals against the configured workload identity before delivering the approved credential to the requesting workflow.

This model is designed to reduce the operational burden and security risk created by static credentials. If a credential does not need to be copied into an app, pipeline, or environment file, there are fewer places for that credential to sprawl, leak, or persist beyond its intended use.

The 1Password Credential Broker also adds visibility into credential delivery. Each credential request and delivery event can be logged with identity context, giving security teams a clearer record of which actor requested which credential and under what configured trust relationship.

## Extending 1Password's Zero-Knowledge Security Architecture

The 1Password Credential Broker is built on 1Password's security architecture and is designed so 1Password infrastructure does not have persistent access to customer secrets. Customer-managed key material and trusted identity signals both play a role in the access flow: cryptography helps protect credentials from unilateral access, while identity verification helps ensure credentials are released only to approved requesters.

Before an approved credential is delivered, the 1Password Credential Broker verifies the requester using trusted identity signals and releases only the credential configured for that requester.

## The Credential Foundation for Unified Access

1Password Credential Broker is part of 1Password Unified Access: a platform vision for securing the credentials, identities, and access patterns that connect people, applications, machines, and AI agents.

The 1Password Credential Broker answers a specific question: where should the credential live, and how should it be delivered to the trusted actor that needs it? It keeps 1Password as the credential source of truth and brokers approved credentials from that foundation. Apono, recently acquired by 1Password and announced separately, addresses a different layer: what an identity is permitted to do in the upstream system, and for how long.

Together, these capabilities help organizations move from scattered credentials and fragmented access controls toward a more unified security model. The 1Password Credential Broker secures the credential foundation. Apono governs privileged access in target systems. Both are part of the same larger shift, but they solve different problems.

To learn more about 1Password Credential Broker, [visit our blog](https://1password.com/blog/introducing-1password-credential-broker).

---

### About 1Password

1Password is redefining identity security for how people and AI agents work today. The 1Password Unified Access platform discovers and secures identities and credentials, establishes trusted access, and audits actions across human and AI agents. 1Password SaaS Manager helps organizations discover and secure access to SaaS applications while optimizing spend. 1Password's enterprise vault protects more than 1.5 billion credentials and secrets and is trusted by more than 1 million developers and over 180,000 businesses, including Canva, CIBC Capital Markets, Cursor, Dust, ElevenLabs, Figma, GitHub, HackerOne, Hugging Face, MongoDB, Notion, Perplexity, Salesforce, Stripe, Vercel, and Wiz. Learn more at [1Password.com](http://1password.com/).

### Media Contact

[media@agilebits.com](mailto:media@agilebits.com)