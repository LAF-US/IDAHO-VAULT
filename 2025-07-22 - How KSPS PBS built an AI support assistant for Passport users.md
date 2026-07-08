---
title: "How KSPS PBS built an AI support assistant for Passport users"
source: "https://current.org/2025/07/teaching-the-robot-to-say-pbs-passport-is-a-member-benefit-how-ksps-pbs-built-an-ai-support-assistant/"
author:
  - "[[Skyler Reep]]"
published: 2025-07-22
created: 2026-05-01
description: "The station's first public-facing AI project has \"saved our staff hours of phone time and provided consistent, accurate support to hundreds of members.\""
date created: Friday, May 1st 2026, 4:26:32 pm
date modified: Friday, May 1st 2026, 4:26:56 pm
---

It started, as many good ideas do, with a 45-minute phone call.

If you work at a public television station, you probably know the type. A generous donor has just received a PBS Passport activation email and is unsure what to do with it, so they call the station directly to ask for help. You pick up the phone, open the help doc, and begin walking them through the process, step by step, across a Roku interface or a smart TV menu, sometimes without ever being quite sure which device they’re using.

At KSPS PBS, we realized we were having that same conversation over and over. Often with different staff. Sometimes with the same viewers. And like many mid-sized stations, we have a talented but lean team. We knew our time could be better spent stewarding donors, building community partnerships, or producing local content. So we asked ourselves a simple question: What if a well-trained AI assistant could handle that first layer of support?

In January, that idea led to the creation of our first public-facing AI project: the KSPS PBS Passport Support Bot. It’s a customized generative AI assistant, built using OpenAI’s GPT technology, designed to answer common questions about PBS Passport, the PBS app and device setup. It’s available 24/7, is patient with confused users, and (most importantly) reflects public media values. While still in active testing, it has already saved our staff hours of phone time and provided consistent, accurate support to hundreds of members. (You can [try chatting with it](https://chatgpt.com/g/g-67915cb1a9f08191abf0da670ed8f72c-ksps-pbs-passport-support-bot).)

This tool wasn’t built to replace people. It was built to protect their time and help ensure that public media staff spend more of their day doing the work only humans can do.

## Why start here?

Generative AI refers to systems that can produce language, images or other content based on large datasets. The technology can feel like magic at first: You ask a question and get a clear, written answer. But in truth, it functions more like a pattern-matching engine. It doesn’t know facts the way we do. It simply predicts what kind of response would sound most correct, based on its training.

At KSPS PBS, we began exploring AI through an internal lunch-and-learn in early 2025. I was curious, not about the hype, but about whether the tools could actually help us solve real problems. We had already experimented with internal uses like donor data cleanup and communications drafts. But I wanted to try something more concrete. Something we could eventually share with both staff and the public.

PBS Passport support stood out right away. It’s repetitive, time-consuming and emotionally neutral. It doesn’t require creative thinking or complex decision-making. Yet it quietly consumes a surprising amount of staff capacity.

If we could remove that burden, even partially, we could give our people more time to focus on fundraising, engagement and mission work. That felt like the right kind of experiment.

## How we built it

The first working version of the Passport Support Bot came together in under an hour.

I started by using ChatGPT Plus, OpenAI’s $20-per-month tool that allows for custom GPT creation. (The paid version offers a data security feature that I’ll explain below.) From there, I uploaded every document I could find that might help. This included official PBS FAQs, device activation guides, real-life questions from our viewers, and our own internal workarounds and troubleshooting tips. I added station-specific information, such as contact details and membership policies, and trained the bot to use a patient, step-by-step tone. This was especially important for older users who might be new to streaming platforms.

Setting boundaries was important. Early on, the bot was almost too helpful. It suggested alternatives like, “That episode is available on Amazon Prime,” which made perfect sense in the abstract but wasn’t aligned with our goals. We retrained it to focus only on PBS content and to keep users inside the ecosystem. Now, it offers suggestions like, “That program isn’t available right now, but here are a few other PBS shows with similar themes.”

After that, we invited colleagues from across the PBS system to test it. Dozens of staff members asked questions, tried to confuse it or pushed its limits. The problems they found (like confusing activation tokens or making incorrect assumptions about app compatibility) were easy to correct. We adjusted the training using short, plain-language messages and continued to refine its behavior.

The process didn’t require much technical skill, but it did require careful attention and a clear sense of purpose.

## Where it’s used and what’s next

Today, the bot is available in two key ways:

- Our staff use it internally as a quick reference tool when handling Passport support calls or emails.
- We’ve also begun offering it to members through Passport Picks emails and our website. We frame it as a friendly option, not a replacement for human help.

Eventually, we’d like to integrate the assistant into our website as a pop-up chat window, allowing it to intercept common questions before they become support tickets. Looking further ahead, we’d love to test a voice version that could handle basic tech support over the phone before routing someone to a live person.

Even in its current form, the bot has had hundreds of successful interactions. Every one of those could have been a 30- to 45-minute call. Because the responses are drawn from a single, curated knowledge base, the information is consistent every time. Staff adoption has been strong, and the tool has made day-to-day work a little easier.

## What we’ve learned

One of the most surprising discoveries was that the hardest part wasn’t teaching the bot what to say — it was teaching it what not to say.

Language models like this one are trained to be helpful above all. Left unmonitored, they’ll try to answer every question, even when they shouldn’t. Part of our job was to limit its confidence, not increase it. This helped ensure that when users received an answer, it was accurate, on mission and reflective of our values.

We also came to see this bot as a kind of new hire. It needed onboarding. It needed to learn our house style. And, like any new team member, it made mistakes at first. But those mistakes weren’t reasons to abandon the project. They were opportunities to improve it.

Ethics also guided our decisions. The bot doesn’t collect private information. It always identifies itself as an AI assistant. And we never suggest it’s a replacement for human contact. It’s a support tool, not a gatekeeper.

## More than one bot

The Passport bot was our first public-facing AI project, but it’s not the only one we’ve built.

We’ve also developed a **Custom Station Historian** trained on decades of newsletters, program guides and institutional documents. This tool helps preserve our organizational memory as longtime staff retire, making it easy to search years of archived materials and find answers about past programming, community events or internal decisions.

We also use a **Funding Compliance Bot** that analyzes scripts and videos for alignment with PBS, FCC and internal underwriting guidelines. It offers an early layer of review that has already saved us time and helped avoid compliance issues.

Each of these tools emerged from a clear question: What’s slowing us down? What are we doing over and over again that a machine could assist with?

None of them replace human effort. But each one helps ensure that our human effort is focused where it matters most.

## You can build one too

If you want to try something similar, here’s what you’ll need:

- A ChatGPT Plus subscription with “Improve the model for everyone” turned OFF
- Some basic documentation (FAQs, policies, tone guidelines)
- A clear purpose
- A few hours to experiment, train and test

You don’t have to start with a public-facing tool. Consider building one for your internal team first. Use it to answer common HR questions, review old grant materials or summarize donor records. There’s no requirement to launch it publicly. The only requirement is curiosity.

Our full training guide and sample materials are available on OurNeighborhood, PBS’s internal collaboration site. If you’d like help getting started, I’m happy to share what we’ve learned.

## Closing thoughts

I don’t know what the future of AI in public media looks like. These tools are evolving quickly, and it’s hard to predict where they’ll go next. What I do know is that it’s worth paying attention.

![Elmo and Skyler Reep pose for a photo](https://current.org/wp-content/uploads/2025/07/skyler-reep-elmo.jpg)

Reep with a friend

A future is already emerging in which AI trains on AI-generated data and regurgitates AI-written content. That future may be inevitable in some sectors, but not in public media.

Public media is rooted in trust, service and human connection. These are not things we should outsource. However, if we can utilize AI to mitigate burnout and better serve our communities, then we should.

Let the machines handle the repeatable work. Let us keep our focus on what is human, local and meaningful.

That’s the work *no* algorithm can do.

*Skyler Reep, MSNPA, CFRE, is development director at KSPS PBS and a frequent contributor to national working groups on nonprofit fundraising and public media innovation.*