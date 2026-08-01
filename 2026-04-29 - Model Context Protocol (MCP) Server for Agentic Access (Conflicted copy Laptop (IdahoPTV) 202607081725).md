---
title: "Model Context Protocol (MCP) Server for Agentic Access"
source: "https://wiki.free.law/c/courtlistener/help/api/mcp/model-context-protocol-mcp-server-for-agentic-access"
author:
published: 2026-04-29
created: 2026-07-07
description: "Use an MCP to connect AI tools and agents like Claude and ChatGPT to CourtListener's full functionality, enabling complex legal monitoring, research,  and analysis."
---
AI tools and agents like Claude and ChatGPT can now connect to CourtListener's full functionality, enabling complex legal research and analysis.

This is powered by the [Model Context Protocol](https://modelcontextprotocol.io/), an open standard that allows AI applications to connect to external data sources and tools. Instead of relying solely on their training data, AI assistants using MCP can query live databases for accurate information and use APIs to take actions on a user or application's behalf.

Our MCP server gives AI agents seamless access to CourtListener's extensive legal platform. This enables the AI assistants to provide more accurate and comprehensive answers to legal research questions by giving them direct access to case law, PACER data, judge information, and more.

## Available Tools

When you use a tools or AI assistants that have CourtListener's MCP server installed, the assistant will have access to:

- **Case law and opinions** — Millions of federal and state court decisions going back centuries
- **PACER data** — The largest open repository of federal court cases, parties, attorneys, and documents
- **Citation network** — What cases cite, and what cites them
- **Oral arguments** — A huge trove of searchable audio and transcripts from federal appellate courts
- **Judges and their financial disclosures** — Biographical and analytical data on the federal judiciary, including judicial assets and debts that may trigger conflicts
- **Keyword and semantic search** — Both keyword and natural language search across our archives
- **Alerts** — Real-time monitoring for new filings, citations, and queries
- **Citation verification** — Grounded citation checks to reduce hallucinations

All of this is powered by the [CourtListener APIs](https://wiki.free.law/c/courtlistener/help/api/rest/v4/overview) and [data](https://www.courtlistener.com/help/coverage/).

## Sample Prompts

Try prompts like:

- "Find recent opinions on qualified immunity and identify splits"
- "Pull the latest filings on docket XYZ and explain what's happening"
- "Find the PACER fees class action, tell me the current status, and sign me up for email alerts at the appellate and district level"
- "Make me an alert any time that Miranda v. Arizona is cited by the supreme court"
- "Verify every citation in this brief and flag any unknown citations"
- "Review the news article at this link and find the case that's being discussed: [https://local-news-example.com/legal-article](https://local-news-example.com/legal-article) "

## Getting Started

Before beginning, you will need a CourtListener account. [Create an account](https://www.courtlistener.com/register/) if you do not already have one.

The installation process varies depending on the AI tool you use.

### Claude

The CourtListener MCP is available in Anthropic's [MCP Connector Directory](https://claude.ai/settings/connectors).

To get started:

1. Open Claude on web, desktop, or mobile
2. Go to Settings > Customize ([or click here](https://claude.ai/customize/connectors) > Browse
3. Find the CourtListener MCP in the connector directory and add it
4. Grant Claude access to your CourtListener account
5. Start a conversation or try a sample prompt from above

### ChatGPT

Our MCP server is not yet in OpenAI's connector directory, but can be added as a custom app:

1. Go to Settings > Apps ([or click here](https://chatgpt.com/#settings/Connectors)) > Advanced Settings
2. Enable "Developer Mode" to allow custom connectors
3. Click "Create App" to create an MCP app for CourtListener
	- Name: `CourtListener`
		- Server URL: `https://mcp.courtlistener.com`
		- Authentication: `OAuth`
		- Accept the risks and save
	![A screenshot of the Create App pop up](https://wiki.free.law/files/446/Screen%20Shot%202026-05-09%20at%2010.00.11.png)
4. Grant ChatGPT access to your CourtListener account
5. Start a conversation or try a sample prompt from above

### Custom Installation

Our MCP is available with any MCP compatible interface and is agnostic of model. To install it with other models, use `mcp.courtlistener.com` and the OAuth permission system.

## Increased Usage

The MCP server uses standard CourtListener API access for authentication. All CourtListener users are granted API access, automatically.

Elevated access is available through a Free Law Project membership or commercial agreement.

## Learn More

If you have questions about the MCP server or would like to discuss commercial access, please get in touch.

4,599 views Last updated 3 weeks, 5 days ago

Creator: [mike](https://wiki.free.law/activity/mike/)