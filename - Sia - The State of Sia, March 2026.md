---
source: "https://sia.tech/blog/the-state-of-sia-march-2026"
author:
published:
created: 2026-04-23
---
![](https://sia.tech/_next/image?url=%2Fapi%2Fmedia%2Ffile%2FThe%2520State%2520of%2520Sia%252C%2520March%25202026%3F2026-04-21T21%3A15%3A13.752Z&w=3840&q=100)

March was a strong month for Sia across product, infrastructure, and ecosystem development. The Foundation’s content and messaging stayed focused on one of Sia’s clearest market differentiators: privacy by design. Social content this month highlighted the [risks of surveillance](https://www.instagram.com/reel/DVZjb07DTgY/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==), [the importance of protecting user-generated content online](https://www.tiktok.com/@sia.network/video/7616439821573147917), and the concrete guarantee that [Sia is trustless by design](https://www.tiktok.com/@sia.network/video/7621602522137890061).

Users do not have to rely on promises to know their data is safe with Sia.

At the same time, the Foundation continued sharpening its broader go-to-market strategy. As March closed and April planning came into view, that work included preliminary market research and product testing for the new Sia Storage App. Join us in Miami for major product news at Consensus 2026 from May 5-7! Can't meet us IRL? Sign up for the Sia newsletter [here](https://sia.tech/newsletter).

The Grants Program also continued to expand in practical directions this month, with one new grant approved and several ongoing grantees reporting meaningful progress. The Foundation also announced [updated funding directives](https://forum.sia.tech/t/grants-program-new-funding-guidelines-and-requirements/1074) to provide greater clarity for applicants and better alignment with the program’s long-term goals.

Building on previous communications regarding the [governance practices of the Grants Program](https://forum.sia.tech/t/sia-grants-governance-2025-holiday-notice/1013), the [Grants Program Review (2025)](https://forum.sia.tech/t/grants-program-review-2025-summary/1054) –and as an additional step towards the full Grants Program Strategy (including KPIs)–we are announcing new funding directives effective April 10, 2026.

1\. New shift to specific themes for grant proposals

2\. Details of what the Committee does and does not want to fund

3\. Clarified the working definition of what is considered to be a high-quality grant

On the development side, March brought meaningful momentum across the ecosystem: the Sia Storage App saw a limited release, and `indexd` continued to mature as a core developer platform, while new versions of `hostd` and `renterd` were released.

## Development Updates

![](https://sia.tech/_next/image?url=%2Fapi%2Fmedia%2Ffile%2FThe%2520State%2520of%2520Sia%2520Blog%2520-%2520Development%2520Updates%3F2025-07-16T11%3A02%3A06.980Z&w=3840&q=100)

#### Sia Storage App: Faster, Smoother, and Preparing for More Platforms

The Sia Storage App saw one of its busiest months in the stack, with versions `v1.8.0`, `v1.8.1`, and `v1.8.2` receiving limited releases. Much of the work focused on performance and responsiveness, particularly for real-world use cases involving background syncing of large media batches.

- Improved upload performance for batches of many small files by parallelizing the save phase
- Fixed synchronous filesystem calls that were causing noticeable lag during background operations
- Optimized thumbnail generation to reduce memory usage and improve throughput
- Continued refactoring the codebase toward a shared core that can support mobile, desktop, CLI, and web environments

On the UI side, an issue was fixed in which the wrong thumbnail could briefly appear before the correct one loaded, and the team also made promising progress exploring support for File Provider Extension so the app can eventually appear as a native location in the Files app.

#### indexd: Safer App Connections and Better Developer Workflow

March’s `indexd` work continued to push the platform toward a more capable and secure foundation for applications built on Sia. The emphasis this month was on app safety, storage operations, and visibility into system behavior.

- Removed app connect keys from app API responses to better protect users from malicious apps
- Added rate limiting and field-size checks during app connect to reduce denial-of-service risk
- Extended the `accounts.Account` type with a ready field so apps can tell when hosts are funded, and transfers can begin
- Added a `DeleteObject` method to the Go SDK for parity with the Rust SDK
- Added support for tracking unpinned sectors, packing, and exposed `PinObject`
- Expanded stats reporting to show connect-key quota breakdowns and application activity patterns

#### sia-storage-sdk: Expanding Native SDK Support

March’s `sia-storage-sdk` work focused on making the Sia Storage SDK more accessible across native development environments. With new language support for both Android and Apple platforms, the SDK is becoming a more practical option for developers building cross-platform storage experiences on Sia.

- Added Kotlin support for Android app developers
- Added a Swift SDK

#### sia-sdk-rs: Lower-Level Improvements for Packed Objects

Work on `sia-sdk-rs` this month was smaller in scope, but still important for correctness at the storage layer. As the Rust implementation of core Sia types continues to mature, March included a fix related to packed object handling.

- Fixed slab length in packed objects

#### hostd: Leaner Consensus Storage in v2.7.0

The latest `hostd v2.7.0` release introduces one of the month's more notable protocol-facing changes: experimental consensus pruning. As Utreexo continues to reduce the need for full historical block storage, this gives hosts a way to reduce disk usage while still fully validating new blocks.

- Added an experimental consensus pruning option to reduce consensus size on disk
- Added a config option to disable the Merkle proof cache for low-resource systems
- Fixed an issue where revisions and resolutions in the same block could cause contracts to remain active indefinitely
- Improved backup performance by removing the backup step size limit and skipping vacuum during backup
- Updated Go to `v1.26.0`

#### renterd: Reliability Improvements in v2.9.0

The latest renterd v2.9.0 release focused on improving reliability in the storage layer and tightening behavior around syncing and retries.

- Ensured store methods are retry-safe
- Reset the chain state on instant sync
- Updated Go to `v1.26.0`
- Updated coreutils to `v0.21.1`

#### s3d: Expanding Compatibility for Real-World Use Case

Work on `s3d` continued to improve compatibility with common S3-style workflows while tightening its behavior with indexd-backed storage. The updates this month were especially relevant for object lifecycle handling and larger uploads.

- Ensured objects are unpinned from the indexer after deletion
- Added a `WithKeyPair` option to the Sia backend
- Added support for empty objects
- Added multipart uploads
- Continued work on upload packing

## Grant Program Updates

![](https://sia.tech/_next/image?url=%2Fapi%2Fmedia%2Ffile%2FThe%2520State%2520of%2520Sia%2520Blog%2520-%2520Grants%2520Program%3F2025-07-16T11%3A02%3A44.014Z&w=3840&q=100)

#### Newly Approved Grants

- [**Sia NFS Gateway**](https://forum.sia.tech/t/standard-grant-sia-nfs-gateway-indexd-nfsv4/1055)**:** This newly approved grant continues the development of `sia-nfs` by replacing its `renterd` dependency with `indexd`, adding partial `NFSv4` support for more reliable Linux and macOS compatibility, and restructuring the codebase into reusable Rust crates for I/O scheduling, caching, and virtual filesystem functionality.

#### Open Grant Progress Reports

- [**Vup Vault - Personal Backup & Sync**](https://forum.sia.tech/t/standard-grant-vup-vault-personal-backup-sync-archive-with-indexd/1037/9)**:** Vup Vault made substantial progress this month, completing an end-to-end encrypted backup and restore workflow, introducing a daemon-based architecture over IPC, supporting incremental backups, and adding reusable infrastructure, including a new encrypted and compressed FS v2 format, typed RPC, and multi-backend blob store adapters.
- [**Chi-Voice Pilot**](https://forum.sia.tech/t/small-grant-chi-voice-pilot/1035/15)**:** Chi-Voice launched a public REST API with freemium API key access, allowing developers to query archived language recordings by language, type, and date, and to receive both a `sia://` CID and a standard HTTPS audio URL.
- [**SMB - Indexer Support**](https://forum.sia.tech/t/standard-grant-smb-indexer-support-2/1011/10)**:** The SMB grant added `indexd` connectivity and core filesystem functionality, while also enabling zero-sized files, raising the practical upload size limit through a rewritten chunking approach, and fixing a Windows cut-and-paste issue that could have led to data loss.

## Final Thoughts

All in all, March showed steady progress across nearly every layer of the ecosystem, consistent with Sia’s long-term mission: giving users real ownership over their data. With product improvements, marketing research, grant strategy refinement, and ecosystem development all moving forward together, March was another solid step toward a more usable and more resilient decentralized storage future.

#### That’s all, folks!

Thanks for your continued support and dedication as we build the foundation of the decentralized future.

Take care, and see you next month.

---

Want important Sia updates delivered straight to your inbox?

[Sign up for our newsletter](https://sia.tech/newsletter) and stay informed about new releases, partnerships, developer resources, ***and more!***