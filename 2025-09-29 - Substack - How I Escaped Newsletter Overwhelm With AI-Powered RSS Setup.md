---
source: "https://afterhoursai.substack.com/p/how-i-escaped-newsletter-overwhelm"
author:
  - "[[Tam Nguyen]]"
published: 2025-09-29
created: 2026-07-21
---
## My Newsletter Consumption Problem

10:47 PM. I’m manually checking my eighth Substack profile to see if my favorite Substackers have posted.

Not because I don’t get email notifications—I do. All *847 unread emails* sitting in my inbox right now can confirm that. I’ve trained myself to ignore most notifications, which means I’m missing content from writers I actually want to read while drowning in digital noise.

![](https://substackcdn.com/image/fetch/$s_!lTQJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7990b713-e30b-4532-ae22-6a499032a9e6_1536x1024.png)

So instead, I’m clicking through individual Substack profiles. One by one. Like it’s 2015.

The math is embarrassing: I’m spending 20-30+ minutes a day just hunting for content, not reading it. That’s 4+ hours a week on newsletter archaeology. And I *still* feel like I’m missing stuff.

Worse: I’m spending more mental energy worrying about what I’m missing than actually consuming anything useful.

So, what did I do?

Implement a curated RSS system that took 30 minutes to set up. Now I process everything in 60 minutes a week instead of 4+ hours, get instant notifications for voices that matter, and see all my Substack subscriptions, YouTubers, and other content creators in one unified feed.

---

***I’m obsessed with AI automation but also believe not everything needs a complex AI setup. Here’s how you can use AI to set up a proven tool (RSS Reader) to solve your overwhelm problem.***

---

**Here’s how it works 👇🏼**

## Why Substack’s Interface Creates Overwhelm

I follow 129 publications on Substack and add more every day. It’s gotten out of hand. But there are so many great voices to follow, so what do you do?

![](https://substackcdn.com/image/fetch/$s_!M8_h!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3e052e1-82e7-41cb-8a77-1c8170e3e500_727x332.png)

First, Substack treats all newsletters equally. There’s no way to prioritize authors. No filtering. No hierarchy.

> Secondly, When everything feels urgent, nothing feels manageable. You end up reading less because you’re paralyzed by choice.

The irony: having access to more content makes you consume less of it.

**The solution isn’t a fancy automation or prompt engineering mastery. It’s using AI to handle the setup work, then letting proven RSS tools handle the curation.**

## Results and Benefits Achieved

![](https://substackcdn.com/image/fetch/$s_!UXmt!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F478eabf8-ff76-4a65-82ea-3f9d8422a19b_1370x851.png)

InoReader expanded column view featuring only the newsletters I follow

Setup took 30 minutes. I went from 4+ hours of scattered reading per week to 60 focused minutes. More importantly, those 60 minutes feel intentional instead of reactive.

**Unexpected wins:**

- Found newsletters I’d forgotten I was subscribed to (and started reading or finally unsubscribed)
- Started seeing cross-connections between different authors’ ideas
- Reduced FOMO while actually consuming more quality content
- More likely to engage meaningfully because the friction of discovery is gone
- Bonus, some RSS readers have AI features that can help you consume the right content even faster

![](https://substackcdn.com/image/fetch/$s_!GYO0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1bb6b875-dcd3-44ac-88f3-21e63383e9c2_818x1012.png)

AI summaries and analysis (ft. Nate’s Newsletter)

## What RSS Actually Is (And Why It Solves This)

RSS feeds are like getting a table of contents for all your subscriptions in one place, instead of checking each site individually.

**Every Substack (and most content sites) automatically creates an RSS feed - it’s just a live list of their latest posts. RSS readers collect all these feeds and show you everything in one organized interface.**

Think of it as a unified inbox for content from anywhere on the web. You can see when Substack Writer A posted something new right next to when YouTuber B uploaded a video, all sorted by your priorities.

It changed how I see connections between ideas and I can scan for interesting content without digging through each platform’s UI, then click through to the original post for commenting and engagement.

![](https://substackcdn.com/image/fetch/$s_!mibY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fa62b62-1506-4993-abba-db5ba55a19f8_1660x1108.png)

My evolving news dashboard. Articles are tagged by keywords.

Another key difference: instead of Substack’s interface treating everything equally, you control the hierarchy. High-priority authors get immediate attention. Everything else gets sorted for later.

RSS has been around forever, but most people stopped using it when social media took over. Now that social feeds are algorithmic chaos, RSS is having a comeback - especially for people who want intentional content consumption.

## Step-by-Step Implementation

### Step 1: RSS Feed Collection (Choose Your Method)

You have two paths here, depending on your comfort level and access with AI browsers.

**Option A:** Use Comet (Dia, etc.) browser AI for automated extraction across all Substack subscriptions. Simply navigate to your Substack subscription page in your browser, tell Comet to “extract all RSS feed URLs from my subscriptions,” and let it handle the tedious work.

![](https://substackcdn.com/image/fetch/$s_!Rrur!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F00da04bf-c47b-4508-b84b-e12fade3c377_1058x680.png)

Comet gave me a list of all my subscriptions. But we’re still missing the ‘/feed’ at the end of the URL.

![](https://substackcdn.com/image/fetch/$s_!GWk5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F19e4b218-3de6-471c-97a7-3418b869b0ed_1275x762.png)

Then I asked it to give me the URLs with ‘/feed’ appended to it and had it create an.opml file for import into InoReader directly.

![](https://substackcdn.com/image/fetch/$s_!FJIe!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd1f138f8-c9db-4c3a-b5c7-532574b282bb_1325x583.png)

Import all 129 Substack publications at once by uploading the.opml file (InoReader)

**Option B:** Manual method for those who prefer hands-on control—append “/feed” to any Substack URL (e.g., example.substack.com/feed) and collect them yourself. Either approach works; create an organized list of all feeds for the next step.

### Step 2: RSS Reader Selection and Setup

Choose an RSS reader with robust filtering capabilities. [Feedly](https://feedly.com/) offers a solid free tier, while Inoreader provides better filtering options for power users. [RSS.app](https://rss.app/) has been a long-time player as well. There are plenty of readers out there - I started with [InoReader](https://www.inoreader.com/) and like it so far.

It’s free if you want a basic feed but want to filter with rules and follow websites without RSS feeds? You’ll need to upgrade.

Once you upgrade you can also set up a logical folder structure: “High Priority” for must-read voices, “Browse When Time” for interesting but not urgent content, and topic-based folders for different areas of interest.

### Step 3: Creating Author Priority Systems

This is where the magic happens. Categorize authors by importance, immediate attention versus browse-when-time and tag by topic. Set up filtering rules based on author hierarchies and keywords so high-priority content gets flagged immediately.

![](https://substackcdn.com/image/fetch/$s_!-VGQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8a2efe8-2226-4767-9365-c89609e9547a_1114x979.png)

Rule example to help auto-categorize content by keyword. This is my “automation” tag rule.

Configure notifications only for must-read voices to avoid recreating the notification overwhelm you’re trying to escape. The goal is intentional consumption, not reactive scrolling.

### Step 4: Maintaining Platform Engagement

Here’s the crucial habit: always click through to original Substack posts from your RSS reader when you find valuable content. Comment and like directly on the platform to maintain author relationships and support their work. Use RSS for discovery and organization, but Substack for meaningful engagement. This hybrid approach gives you the best of both worlds: organized consumption with authentic community participation.

## When NOT to Use This System

If you’re subscribed to fewer than 15-20 newsletters, you probably don’t need this. Just unsubscribe from the ones you don’t actually read.

If you prefer Substack’s discovery features and comment communities, or you genuinely enjoy browsing the native interface, stick with what works.

> **Sometimes the solution isn’t optimization - it’s elimination.** **If you’re constantly organizing information instead of consuming it, you might just have too many subscriptions.**

## Tools and Resources

### Primary Tools

**Comet**: AI browser for RSS feed extraction. This handles the tedious work of collecting feed URLs from your subscription lists automatically. I pay for Perplexity so I just use this.

**RSS Reader Options**: [Feedly](https://feedly.com/) offers a solid free tier that covers basic filtering and organization. [Inoreader](https://www.inoreader.com/) provides more sophisticated filtering capabilities for power users who want granular control over content curation.

**Optional Notification Platforms**: Slack, Telegram, or Discord for advanced automation alerts if you want instant notifications for high-priority authors.

### Setup Requirements

The beauty of this system is its accessibility. You need basic familiarity with browser AI tools (or willingness to learn), but nothing technical. The entire initial setup and testing should take around 30-60 minutes for most people.

Advanced notification setups are completely optional. The core RSS reader functionality provides 90% of the value without any webhook knowledge or complex integrations.

### Cost Considerations

Most RSS readers offer free tiers that handle moderate subscription volumes perfectly well. Comet is free if you are paying for Perplexity but a reasonable $5/month if you’re not. The total monthly cost for most users ranges from free (using manual RSS collection + free RSS reader) to under $15 for full automation, AI browser and RSS with premium features.

![](https://substackcdn.com/image/fetch/$s_!uwIU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0ab244d9-b407-479a-ab7f-0988c7761328_1523x614.png)

![](https://substackcdn.com/image/fetch/$s_!Zbbh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e1b4e98-b061-4516-a4e8-41196537b2df_1777x1345.png)

PRO TIP: Ask your AI browser to find a working promo code and apply it. It’ll run off and find one and do all the work for you. **Thanks to [Zain Haseeb](https://open.substack.com/users/12335031-zain-haseeb?utm_source=mentions) for sharing this hack 🙌🏼**

## Try it Yourself

Start small. Extract RSS feeds from your top 10 most important Substack subscriptions using either your AI browser of choice or manual method outlined above. Set up a basic RSS reader with simple folder organization. Test the system for a week before expanding to your full subscription list.

The key is proving to yourself that this reduces cognitive overhead before committing to the full migration.

Hit reply with any challenges you encounter during setup. Real-world implementation issues usually spark the best follow-up content and your problem is probably someone else’s problem too.

**While AI and automation are wonderful tools - theyr’e just that. Tools. And sometimes the best tool for the job isn’t AI or automation at all.**

\-Tam