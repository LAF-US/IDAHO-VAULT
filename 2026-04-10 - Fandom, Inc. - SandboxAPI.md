---
source: "https://dev.fandom.com/wiki/Dev_Wiki:Sandbox/API"
author:
  - "[[Contributors to Fandom Developers Wiki]]"
published: 2026-04-10
created: 2026-04-14
---
Welcome to the **Fandom Developers Wiki's sandbox**!

This page exists so that you can practice editing or formatting (see [Editing help](https://community.fandom.com/wiki/Help:Editing "w:Help:Editing")) without changing any serious content. Feel free to try wiki editing out here first.

Fandom allows for rather complicated formatting. It can look overwhelming when you begin, but don't let it worry you. Just start with the basics... enter some text, and learn the other pieces as you go.

Your content contributions are welcome and important. The wiki is a collaborative effort and others can help with formatting and other improvements.

Best wishes!

**API** on Fandom refers to the set of HTTP endpoints through which users are able to obtain data and perform actions, such as:

- Editing pages
- Fetching all pages in a certain category
- Posting to Discussions
- Deleting comments
- Obtaining user profile information
- Blocking users
- Retrieving the user's notifications
- etc.

There are various places where users can find these endpoints, and not all of them are very well documented. This set of pages aims to document all Fandom-specific endpoints that may be useful to users.

## MediaWiki API

*Main article: ../MediaWiki API*

**MediaWiki API** is an API that comes with [MediaWiki](https://mediawiki.org/wiki/ "mw:"), the wiki software Fandom is based on. Being an API of a widely-used open-source product, it is [very well documented](https://mediawiki.org/wiki/API:Main_page "mw:API:Main page") on the main website for MediaWiki documentation, mediawiki.org. However, the documentation available from the main API documentation page does not cover:

- Additional API modules added by extensions from mediawiki.org
- Additional API modules added by Fandom extensions

All installed API modules can be found through [`/api.php`](https://dev.fandom.com/api.php) on any Fandom wiki (on wikis with language codes in their URL, such as `disney.fandom.com/fr`, the module listing can be found from `disney.fandom.com/fr/api.php`). The documentation for extension-specific API modules is usually good enough, but the documentation for Fandom-specific API modules can be found on the MediaWiki API article.

The MediaWiki API's core modules can be considered **stable**, as well as modules added by mediawiki.org extensions. However, Fandom-specific API modules are considered **unstable**, as they are not officially documented and can be removed at any time.

## Nirvana

*Main article: [Nirvana](https://dev.fandom.com/wiki/Nirvana "Nirvana")*

**Nirvana** is Fandom's application framework introduced in their MediaWiki platform code. The architecture of that framework is not relevant to users who want to pull data or perform actions through the API, but the most relevant information is that the Nirvana API consists of **controllers** whose methods can be queried for data. It has two entry points, but they both query the same controllers. More information about these entry points, as well as some controllers, can be found on the [Nirvana](https://dev.fandom.com/wiki/Nirvana "Nirvana") article.

The Nirvana API is considered **unstable**.

## Service API

*For more information, see Dev Wiki:Sandbox/Service API.*

**Service API** groups APIs from several services Fandom uses, introduced when Fandom started switching to a [service-oriented architecture](https://community.fandom.com/wiki/User_blog:DaNASCAT/Introducing_Service-Oriented_Architecture,_A_New_Approach_to_Software_Development "w:User blog:DaNASCAT/Introducing Service-Oriented Architecture, A New Approach to Software Development"). Its entry point is [https://services.fandom.com/](https://services.fandom.com/), followed by the service name and then a service-specific path to the endpoint. It is supposed to be built as a [REST API](https://en.wikipedia.org/wiki/Representational_state_transfer "wikipedia:Representational state transfer").

Unfortunately, the list of services Fandom uses and exposes their APIs is not currently known. The only way to find out these service names is by checking where are Fandom applications sending their HTTP requests to. The list of currently known controllers may be found on the Dev Wiki:Sandbox/Service API article. Due to this, the Service API is considered **unstable**.