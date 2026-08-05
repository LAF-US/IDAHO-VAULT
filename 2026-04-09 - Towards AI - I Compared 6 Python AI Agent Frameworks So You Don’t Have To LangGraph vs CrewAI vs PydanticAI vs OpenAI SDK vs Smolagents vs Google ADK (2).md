---
source: "https://pub.towardsai.net/i-compared-6-python-ai-agent-frameworks-so-you-dont-have-to-langgraph-vs-crewai-vs-pydanticai-vs-d8a5e6e43262"
author:
  - "[[The Dev Loop]]"
published: 2026-04-09
created: 2026-04-17
---
[Mastodon](https://me.dm/@thedevloop)

## [Towards AI](https://pub.towardsai.net/?source=post_page---publication_nav-98111c9905da-d8a5e6e43262---------------------------------------)

[![Towards AI](https://miro.medium.com/v2/resize:fill:76:76/1*JyIThO-cLjlChQLb6kSlVQ.png)](https://pub.towardsai.net/?source=post_page---post_publication_sidebar-98111c9905da-d8a5e6e43262---------------------------------------)

We build Enterprise AI. We teach what we learn. Join 100K+ AI practitioners on Towards AI Academy. Free: 6-day Agentic AI Engineering Email Guide: [https://email-course.towardsai.net/](https://email-course.towardsai.net/)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*lDGYbpJINKYyPx44)

Photo by Jona on Unsplash

## I built the same research agent six times. Only two of these frameworks survived my weekend.

Last month, my team needed to pick an agent framework for a client project. A document analysis pipeline — pull data from PDFs, cross-reference it with a database, generate a summary, email the result. Pretty standard stuff in 2026.

I made the mistake of asking Twitter which framework to use.

Within an hour I had 47 replies, each confidently recommending a different tool. Half of them contradicted each other. Someone called LangGraph “overengineered garbage.” Someone else called it “the only serious option.” A third person said both were wrong and I should just use raw API calls.

So I did what any reasonable person would do. I blocked out a weekend, installed all six major frameworks, and built the same agent in each one. Same task. Same model. Same tools. Same evaluation criteria.

Here’s what I found — and it’s not what the fanboys on either side want to hear.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*7J66QD70oyw9bJMEaBYquA.png)

Running AI agents in terminals (Screenshot captured by author)

## The Setup: What I Actually Built

Before we get into results, let me tell you exactly what I tested. No hand-waving.

**The task:** A research agent that takes a company name, searches the web for recent news, extracts key financial data points, cross-references them against a local SQLite database, and produces a structured JSON summary. Three tools, one agent, one output schema.

I picked this because it’s boring enough to be realistic. Nobody’s building autonomous coding agents for their first production deployment. They’re building glorified API orchestrators with a bit of reasoning sprinkled on top. That’s most agent work in the real world, and every framework should handle it well.

**The model:** GPT-4o across all six (where possible — more on that later).

## Logan, become a member to read this story, and all of Medium.

The Dev Loop put this story behind our paywall, so it’s only available to read with a paid Medium membership, which comes with a host of benefits:

Access all member-only stories on Medium

Get unlimited access to programming stories from industry leaders

Become an expert in your areas of interest

Get in-depth articles answering thousands of programming questions

Grow your career or build a new one

![Steve Yegge](https://miro.medium.com/v2/resize:fill:80:80/1*OrBdZ2GUUicWcT6x8KSYZg.png)

Steve Yegge

ex-Geoworks, ex-Amazon, ex-Google, and ex-Grab

![Carlos Arguelles](https://miro.medium.com/v2/resize:fill:80:80/1*CM27oO9pXETXjs2M9_dUFg.jpeg)

Carlos Arguelles

Sr. Staff Engineer

Google

![Tony Yiu](https://miro.medium.com/v2/resize:fill:80:80/2*CSDritfpmHLYxn63arD9sQ.jpeg)

Tony Yiu

Director

Nasdaq

![Brandeis Marshall](https://miro.medium.com/v2/resize:fill:80:80/1*qLWny7soUL4K4lqhX1wQVw.png)

Brandeis Marshall

CEO

DataedX

![Cassie Kozyrkov](https://miro.medium.com/v2/resize:fill:80:80/1*IL0mnvzNcpG2ZD0JBqo7zQ.jpeg)

Cassie Kozyrkov

Chief Decision Scientist

Google

![The Secret Developer](https://miro.medium.com/v2/resize:fill:80:80/1*VW3_O0wyFnpWNNoyv7psjg.png)

The Secret Developer

Software Developer

![Austin Starks](https://miro.medium.com/v2/resize:fill:80:80/1*dfww62lW8x8sVZNbLx5aCA.jpeg)

Austin Starks

Software Engineer and Entrepreneur

![Camille Fournier](https://miro.medium.com/v2/resize:fill:80:80/1*J2fWNTyPbgEhIyvVIjHAXg.jpeg)

Camille Fournier

Head of Engineering

JPMorgan Chase

[Upgrade](https://medium.com/plans?susiEntry=post_paywall&source=upgrade_membership---post_limit--d8a5e6e43262---------------------------------------)