---
title: "Segments - Codacy docs"
source: "https://docs.codacy.com/organizations/segments/"
author:
  - "[[support@codacy.com (Codacy Support)]]"
published: 2026-08-12
created: 2026-08-13
description: "Segments are dimensions that Codacy reads from your provider that organizes repositories into relevant groups for you. Today, Segments are available for:"
---
## Segments

> [!important] Important
> Segments are not supported for Personal orgs, as Custom Properties are not available in GitHub for these orgs.

Segments are dimensions that Codacy reads from your provider that organizes repositories into relevant groups for you. Today, Segments are available for:

- [GitHub Custom Properties](#github-custom-properties)
- [Bitbucket Projects](#bitbucket-projects)

## Where can Segments be utilised?

- [Repository list](https://docs.codacy.com/organizations/managing-repositories/#provider-segments)
- [Security & Management Risk](https://docs.codacy.com/organizations/managing-security-and-risk/)

## Enabling Segments

To enable Segments, an initial sync between your provider and Codacy needs to happen. Once completed, you can use Segments to better locate and organize repositories within Codacy. ![Segments sync](https://docs.codacy.com/organizations/images/Segments-no-sync.png) ![Segments after sync](https://docs.codacy.com/organizations/images/segments-after-sync.png)  

### GitHub Custom Properties

Custom properties allow you to assign tags or metadata to repositories, making it easier to categorize and filter them. Create, use, and manage custom properties for your repositories directly in GitHub.

> Refer to [GitHub's official documentation](https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization#adding-custom-properties) for detailed steps on how to add, edit, and manage repository **Custom Properties**.

#### Keep Segments insync

For changes to repository **Custom Properties** in GitHub to be **automatically** reflected in Codacy, users need to [accept the new permission request made by the Codacy GitHub app](https://docs.github.com/en/apps/using-github-apps/approving-updated-permissions-for-a-github-app).

> [!note] Note
> If the permission is **not accepted**, users will still be able to use Repository Custom Properties as filters in Codacy, but will need to manually trigger a sync. This can be done using the **manual sync** button available in the filter dropdown, which allows users to synchronize changes from GitHub, though the process may take longer.

Also, the target Custom Properties need to have the option **Allow repository actors to set this property** enabled in GitHub.

### Bitbucket Projects

Bitbucket Projects allow you to organize your repositories into relevant contexts for you, making it easier to categorize and filter them. Create, use, and manage Projects for your repositories directly in Bitbucket.