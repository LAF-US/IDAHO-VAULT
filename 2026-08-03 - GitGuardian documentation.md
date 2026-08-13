---
title: "GitGuardian documentation"
source: "https://docs.gitguardian.com/secrets-detection/secrets-detection-engine/detectors/specifics/sourcegraph_token"
author:
published: 2026-08-03
created: 2026-08-12
description:
---
## Description

### General

- **Documentation**: [https://docs.sourcegraph.com/api](https://docs.sourcegraph.com/api)
- **Summary**: Sourcegraph is a platform that allows to ease code reading, writing, and fixing. Some functionalities are powered by AI such as their coding assistant Cody. Two APIs are exposed, GraphQL and Stream.

### Revoke the secret

Secrets can be revoked from the platform user account.

### Details for Sourcegraph Access Token v2

- **Family:** token
- **Category:** code\_analysis
- **Company:** Sourcegraph
- **High recall:** True
- **Validity check available:** True
- **Analyzer available:** False
- **Revoker available:** False
- **On-premise instances exist:** False
- **Only valid secrets raise an alert:** False
- **Occurrences found for one million commits:** 0.2
- **Prefixed:** True

### Details for Sourcegraph Access Token v3

- **Family:** token
- **Category:** code\_analysis
- **Company:** Sourcegraph
- **High recall:** True
- **Validity check available:** True
- **Analyzer available:** False
- **Revoker available:** False
- **On-premise instances exist:** False
- **Only valid secrets raise an alert:** False
- **Occurrences found for one million commits:** 0.05
- **Prefixed:** True

### Details for Sourcegraph Access Token v1

- **Family:** token
- **Category:** code\_analysis
- **Company:** Sourcegraph
- **High recall:** False
- **Validity check available:** True
- **Analyzer available:** False
- **Revoker available:** False
- **On-premise instances exist:** False
- **Only valid secrets raise an alert:** True
- **Occurrences found for one million commits:** very rare
- **Prefixed:** False