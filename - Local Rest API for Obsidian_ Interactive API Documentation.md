---
title: "Local Rest API for Obsidian: Interactive API Documentation"
source: "https://coddingtonbear.github.io/obsidian-local-rest-api/"
author:
published:
created: 2026-07-02
description:
---
#### Local REST API for Obsidian

## Local REST API for Obsidian

v1.0

API Base URL

HTTPS (Secure Mode):https://{host}:{port}

host

string

Binding host

Default:

127.0.0.1

port

string

HTTPS port

Default:

27124

HTTP (Insecure Mode):http://{host}:{port}

Security

Bearer Auth

Find your API Key in your Obsidian settings in the "Local REST API" section under "Plugins".

Provide your bearer token in the Authorization header when making requests to protected resources.

Example: `Authorization: Bearer 123`

The Obsidian Local REST API with MCP plugin gives you two ways to interact with your Obsidian vault programmatically:

- **REST API** — standard HTTP endpoints for reading and writing notes, searching vault contents, managing periodic notes, and more. Useful from scripts, applications, or any HTTP client.
- **MCP server** — exposes the same capabilities as structured tools for AI assistants (Claude, Cursor, and other MCP-compatible clients). See the `POST /mcp/` endpoint for connection details.

## Testing with this interface

Select any operation in the sidebar, then open the **Try It** tab to send a live request to your running Obsidian instance.

**Authentication** — all requests require a Bearer token. In the **Try It** panel, expand the **Security** section and paste the API key shown in Obsidian under **Settings → Local REST API with MCP**.

**Certificate warning** — the plugin generates a self-signed TLS certificate on first run. Most browsers will block requests to an untrusted certificate, so you may need to add it as a trusted certificate in your OS or browser settings before requests will go through. The steps vary by environment — search for "trust self-signed certificate" plus your OS or browser name if you're unsure. If that proves too cumbersome, you can enable the insecure HTTP server in your plugin settings instead and select "HTTP (insecure mode)" from the **Try It** section.

<iframe allow="clipboard-write; web-share" src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>