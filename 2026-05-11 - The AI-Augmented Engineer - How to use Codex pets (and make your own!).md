---
source: "https://www.augmentedswe.com/p/how-to-use-codex-pets"
author:
  - "[[Jeff Morhous]]"
published: 2026-05-11
created: 2026-08-14
---
### Use /hatch to get a cute companion for your projects

OpenAI has really been cooking lately.

![](https://substackcdn.com/image/fetch/$s_!_tSL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff51e02ee-d9c0-4a37-8464-2c093f52d5d2_1731x909.png)

They’ve gone CRAZY on capabilities and features for Codex, their fast-growing Claude Code competitor.

In the last couple of weeks, Codex got in-app browser use, image generation, and computer use.

![Codex pets - seedy](https://substackcdn.com/image/fetch/$s_!K1cA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5462461-2a9f-4308-b3c3-1f439b122ba9_1046x462.png)

Codex pets - seedy

But today’s newsletter isn’t about that. Today’s newsletter is about adding some fun to Codex.

## What are Codex pets?

[Codex pets](https://developers.openai.com/codex/app/settings#codex-pets) are optional companions for the Codex app.

They are **not** for productivity. They’re for fun!

![Screenshot of Stacky, a Codex pet](https://substackcdn.com/image/fetch/$s_!NUrI!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6fa7146c-bc45-4f16-9040-d2d839c49668_998x422.png)

Screenshot of Stacky, a Codex pet

One thing to note is that Codex pets are only available in the app, so if you’re using the CLI you’re out of luck.

If you’re curious about Codex pets, you’re in good company. The AI-Augmented Engineer is dedicated to helping software professionals use AI to make meaningful improvements to their work.

I’d love to have you join us and get notified when we share more tutorials like this.

## How to install the Codex hatch-pet skill

If you’re new to Codex, you may want to start here with the intro guide:

If you already have Codex installed and get the basics, you just have to install the hatch-pet skill.

`$skill-installer hatch-pet`

Note that you should run this *inside a Codex chat*, not just in your terminal.

![Screenshot of Codex while installing the hatch-pet skill](https://substackcdn.com/image/fetch/$s_!r4Tm!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01c1e7b0-1144-40f5-ae4a-b41c219d4030_3072x1818.png)

The Codex UI for skills is pretty intuitive

Once it’s done, restart Codex.

I’m glad OpenAI adopted the Skill standard, it makes it easier to [switch back and forth between Claude Code.](https://www.augmentedswe.com/p/codex-vs-claude-code)

## How to make a Codex pet

You can make your first pet by invoking the `hatch-pet` skill, which you can do with a slash command.

![Creating a pet in Codex](https://substackcdn.com/image/fetch/$s_!TBzw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F438dba72-674f-4fc1-a3bf-6a936afbb047_3072x1818.png)

Creating a pet in Codex

You’ll need to be on a recent Codex version for this to work. It uses the $image-gen tool, which requires that your Codex app supports plugins (a relatively recent addition).

Codex will generate an image and do a LOT of work to get variation sprites ready so your “pet” can be animated.

![Codex image generation](https://substackcdn.com/image/fetch/$s_!CpBD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F137b706a-19db-427e-98cf-4b5ad2d2b6bc_3072x1818.png)

Codex image generation

If you click into one of the subagents, you can get a bit more visibility into what it’s doing.

![Codex imagegen subagents](https://substackcdn.com/image/fetch/$s_!84Cp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1a5bf009-0caf-43d2-b4a1-cb2bf54bdf4d_3072x1818.png)

Codex imagegen subagents

Codex took quite a long time for me, but eventually “Byte”, my first pet was ready!

Codex offered to save the pet, and it was packaged at `.codex/pets/byte/pet.json` with its spritesheet at `.codex/pets/byte/spritesheet.webp.`

## How to wake your pet

Running `/pet` will wake the default pet.

To select the pet you’re interested in, go to `Settings → Appearance → Pets`

![](https://substackcdn.com/image/fetch/$s_!eoeX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3af0a70b-ab64-44a6-8400-4dae526fa9c2_3072x1818.png)

Then, you can select your custom pet.

## Using the overlay

You’ll notice that Codex puts your pet in an overlaay in the bottom right coner of your screen. The overlay will persist throughout other screens on your computer, which is part of the point!

![](https://substackcdn.com/image/fetch/$s_!qTa5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a3ecf2f-04eb-4e9e-83a0-6bc4c3c0c6ff_2358x1356.png)

The overlay is meant to show active Codex work while you use other apps. It shows the current task, plus whether Codex is running, waiting for input, or ready for review. It combines that state with a short progress prompt so you can glance at what changed without reopening the thread.

For example, look at this Codex pet while a task runs as I write this newseltter!

![](https://substackcdn.com/image/fetch/$s_!gtrl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15229b95-09e6-4403-a35e-c9b40923ef50_2454x1600.png)

And when it finished:

![](https://substackcdn.com/image/fetch/$s_!M-vs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16756064-7877-487d-85d6-a364bd866858_2220x1186.png)

This makes using Codex marginally more productive and way more fun.

**Today’s newsletter is sponsored by my friends at Augment Code.**

Augment was kind enough to give me early access to **[Intent](https://www.augmentcode.com/product/intent?utm_source=augmentedeng&utm_medium=newsletter)**, their next-generation tool for developing software.

![](https://substackcdn.com/image/fetch/$s_!QJZL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6f2ec36-f6a3-4a1a-a00e-4491745556b7_3104x1850.png)

All signs are pointing to the fact that **the IDE is no longer the ideal place to create software.**

Augment Code has jumped on this opportunity, and my first impressions are great.

## Finding other pets online

If you want to add a Codex pet but you aren’t feeling creative, you’re not alone! Someone already set up [Petdex](https://petdex.crafter.run/), a marketplace of installable Codex pets.

![](https://substackcdn.com/image/fetch/$s_!ygJb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb1dacc0-3610-4ea9-87c3-6bd1d41b87d9_3104x1850.png)

As you click into one of these, you’ll see a curl command for installing the pet.

## Other Codex tips

---

Like this tutorial? Sign up to get full access and notifications for new tutorials!