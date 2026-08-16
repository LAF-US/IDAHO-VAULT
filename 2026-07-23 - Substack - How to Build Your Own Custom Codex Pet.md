---
source: "https://aishwaryasrinivasan.substack.com/p/how-to-build-your-own-custom-codex"
author:
  - "[[Aishwarya Srinivasan]]"
published: 2026-07-23
created: 2026-08-14
---
Long-running agent work has a strange problem: you lose track of it. You kick off a task, switch to something else, and then spend the next twenty minutes wondering whether the agent is still working, silently waiting for your approval, or finished 10 minutes ago. You end up tabbing back constantly, which defeats the entire point of delegating.

Codex solves this in the most charming way possible. It’s time, we bring back whimsy! You can run a small animated pet alongside your work, and it reflects the live state of your chats. One glance tells you whether the agent is running, blocked, or waiting on you. It is completely optional, and it is somehow one of the most genuinely useful features in the product.

Better still, you can build your own. This post walks through what pets actually do, the sprite sheet standard behind them, and the full workflow for creating a custom one, including the prompt structure and the review checks that separate a clean pet from a flickering mess.

## Index

1. What a Codex Pet Actually Does: Four States, One Glance
2. Running a Built-In Pet First
3. The Part Everyone Gets Wrong: There Is No Pet Installer
4. The Sprite Sheet Standard: Exactly What You Are Building
5. Writing the Character Brief That Makes or Breaks Your Pet
6. The Review Loop: What to Look For Before You Approve
7. Installing, Refreshing, and the Desktop-to-Web Gap
8. Linkstash

---

## 1\. What a Codex Pet Actually Does: Four States, One Glance

A pet is not decoration. It is a live status indicator for agent activity across your chats.

![](https://substackcdn.com/image/fetch/$s_!bR03!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05311c98-fe53-4d86-b3d1-0c0c37f9b74a_2702x1498.png)

Four states, each mapped to an animation.

1. **Running** means a chat is actively working.
2. **Needs input** means Codex is waiting for your approval, answer, or decision.
3. **Ready** means a chat has finished and has unread activity.
4. **Blocked** means the task failed or hit an error.

The genuinely smart design choice: when several chats are active at once, the pet prioritizes the work that needs your attention. So you are not watching a generic “busy” spinner. ==You are watching the single most actionable thing in your queue.==

That is why this stops being cute and starts being useful. Long-running work feels tangible when you can see its state in your peripheral vision instead of interrogating a sidebar.

## 2\. Running a Built-In Pet First

Before building your own, run a stock one for a day. It costs nothing and it tells you whether you actually want this in your workflow.

Open your profile menu or go to **Settings > Pets**, then select a built-in pet. To bring it on screen, type `/pet` or choose **Wake Pet** from the command menu. Type `/pet` again to tuck it away.

![](https://substackcdn.com/image/fetch/$s_!oNmC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F587e0de0-c312-40f9-997e-429677d0ebdf_3456x1938.png)

The built-in collection currently includes companions named Codex, Dewey, Fireball, Hoots, Rocky, Seedy, Stacky, BSOD, and Null Signal. That lineup can change over time, so treat it as a snapshot rather than a fixed list.

Run one through a real work session with a few parallel chats. If you find yourself glancing at it instead of clicking into threads, you have your answer, and building a custom one is worth the effort.

## 3\. The Part Everyone Gets Wrong: There Is No Pet Installer

> This trips people up, so it is worth stating plainly: **you do not need to hunt down a separate pet installer.** There is no third-party tool to download, no extension to sideload.

![](https://substackcdn.com/image/fetch/$s_!Uh-0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0af8a652-ff6b-496f-b26c-360bdbcfe015_2670x1340.png)

Open **Settings > Pets** and select **Create your own pet**. The desktop app does three things automatically: it installs the bundled `hatch-pet` skill, reloads your skills, and opens a new creation chat. That chat is where the whole build happens.

![](https://substackcdn.com/image/fetch/$s_!cE0l!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2077a1a1-ca94-49f9-8023-44f4aac54c08_876x446.png)

So the entire entry point is one menu item. Everything downstream is a conversation with a skill that already knows the technical requirements.

**1\. Mastering Agentic AI Certification**  
  
I’m hosting a 6-week Mastering Agentic AI Certification with my co-founder, Arvind Narayan, designed for both technical and non-technical professionals who want to build deep, practical expertise in AI systems. We’ll cover GenAI foundations, RAG, agentic design patterns, fine-tuning, evaluations, and AI safety, with a project every week across two tracks: low-code/no-code for non-developers and code-heavy for developers. No prerequisites are required, and over 35% of our current cohort comes from non-coding backgrounds.  
  
Enroll here: [https://maven.com/aishwarya-srinivasan/mastering-ai-agents](https://maven.com/aishwarya-srinivasan/mastering-ai-agents)

**2\. AI for Forward Deployed Engineers**  
  
This hands-on workshop is built for Forward Deployed Engineers, Solutions Engineers, Developer Advocates, Product Engineers, and other customer-facing technical roles. You’ll learn to build production-ready AI agents using LLM APIs, tools, RAG, LangGraph, evaluations, observability, guardrails, and HITL, then deploy them on Google Cloud and Vertex AI while making trade-offs across cost, latency, reliability, security, and customer impact. Use code **50OFF** for 50% off.  
  
Enroll here: [https://maven.com/aishwarya-srinivasan/ai-for-forward-deployed-engineers?promoCode=50OFF](https://maven.com/aishwarya-srinivasan/ai-for-forward-deployed-engineers?promoCode=50OFF)

## 4\. The Sprite Sheet Standard: Exactly What You Are Building

Understanding the output format is what separates people who get a clean pet on the first try from people who iterate five times. A pet is not a single avatar. It is a **full animation sheet**.

The current standard is a transparent PNG or WebP at exactly **1536 by 1872 pixels**, laid out as an **8-column by 9-row grid**, with each cell measuring **192 by 208 pixels**.

![](https://substackcdn.com/image/fetch/$s_!f7_O!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd5af8ca-fbc1-41e2-8714-40fcfa153709_1964x1494.png)

Each row is a different state, and the eight columns across that row are the animation frames for it. Nine rows: idle, run right, run left, wave, jump, failure reaction, waiting, active work or processing, and review or inspection.

Here’s how mine looks!

![](https://substackcdn.com/image/fetch/$s_!F2dV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40e91efe-b107-4aca-bf01-e3360ebbeca0_1313x1600.jpeg)