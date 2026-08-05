---
source: "https://docs.gitlab.com/user/organization/"
author:
published:
created: 2026-04-19
---
/

---

## Organizations

> [!type-flag] Type-flag
> The availability of this feature is controlled by a feature flag. For more information, see the history. This feature is available for testing, but still in development and not ready for production use.

Organizations will be above the [top-level namespaces](https://docs.gitlab.com/user/namespace/) for you to manage everything you do as a GitLab administrator, including:

- Defining and applying settings to all of your groups, subgroups, and projects.
- Aggregating data from all your groups, subgroups, and projects.

> [!type-disclaimer] Type-disclaimer
> This page contains information related to upcoming products, features, and functionality. It is important to note that the information presented is for informational purposes only. Please do not rely on this information for purchasing or planning purposes. The development, release, and timing of any products, features, or functionality may be subject to change or delay and remain at the sole discretion of GitLab Inc.

For more information about the state of organization development, see [epic 9265](https://gitlab.com/groups/gitlab-org/-/epics/9265).

## Create an organization

1. In the upper-right corner, select **Create new** ( ) and **New organization**.
2. In the **Organization name** text box, enter a name for the organization.
3. In the **Organization URL** text box, enter a path for the organization.
4. In the **Organization description** text box, enter a description for the organization. Supports a [limited subset of Markdown](https://docs.gitlab.com/user/organization/#supported-markdown-for-organization-description).
5. In the **Organization avatar** field, select **Upload** or drag and drop an avatar.
6. Select **Create organization**.

## Switch organizations

If you are a member of multiple organizations, you can switch between them. To switch organizations:

1. In the left sidebar, at the top, select the **Current organization** dropdown list.
2. Select the organization you want to switch to.

## Supported Markdown for Organization description

The Organization description field supports a limited subset of [GitLab Flavored Markdown](https://docs.gitlab.com/user/markdown/), including:

- [Emphasis](https://docs.gitlab.com/user/markdown/#emphasis)
- [Links](https://docs.gitlab.com/user/markdown/#links)
- [Superscripts / Subscripts](https://docs.gitlab.com/user/markdown/#superscripts-and-subscripts)