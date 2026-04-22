---
title: "Linkwarden: FOSS self-hostable bookmarking with AI-tagging and page archival (linkwarden.app)"
source: "https://news.ycombinator.com/item?id=43856801"
author:
  - "[[FireInsight]]"
published: 2025-05-01
created: 2026-04-19
description: "Linkwarden: FOSS self-hostable bookmarking with AI-tagging and page archival (linkwarden.app) - by FireInsight on Hacker News"
date created: Sunday, April 19th 2026, 12:26:04 pm
date modified: Sunday, April 19th 2026, 12:34:35 pm
---

[https://linkwarden.app/](https://linkwarden.app/)

---

## Comments

> **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43857926)
> 
> Hello everyone, I’m the main developer behind Linkwarden. Glad to see it getting some attention here!
> 
> Some key features of the app (at the moment):
> 
> \- Text highlighting
> 
> \- Full page archival
> 
> \- Full content search
> 
> \- Optional local AI tagging
> 
> \- Sync with browser (using Floccus)
> 
> \- Collaborative
> 
> Also, for anyone wondering, all features from the cloud plan are available to self-hosted users :)
> 
> > **zxcvgm** · [2025-05-01](https://news.ycombinator.com/item?id=43861250)
> > 
> > Cool, looks like text highlighting is a new addition in 2.10. There aren't any examples in the demo site of this, but can it capture the highlighted text snippets and show them in the link details page? That would help me recall quickly why I saved the link, without opening the original link and re-reading the page. I haven't really seen this in other tools (or maybe I just haven't looked hard enough), except Memex.
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43861711)
> > > 
> > > \> There aren't any examples in the demo site of this
> > > 
> > > This is because we haven't updated the demo to the latest version.
> > > 
> > > \> but can it capture the highlighted text snippets and show them in the link details page?
> > > 
> > > That's a good idea that we might implement later, but at the moment you can only highlight the links\[1\].
> > > 
> > > \[1\]: [https://blog.linkwarden.app/releases/2.10#%EF%B8%8F-text-hig...](https://blog.linkwarden.app/releases/2.10#%EF%B8%8F-text-highlighting)
> > > 
> > > **xtiansimon** · [2025-05-03](https://news.ycombinator.com/item?id=43881865)
> > > 
> > > \> “…can it capture the highlighted text snippets and show them in the link details page.”
> > > 
> > > Essentially a quote with attribution.
> 
> > **flexagoon** · [2025-05-01](https://news.ycombinator.com/item?id=43864392)
> > 
> > Great product! Does it handle special metadata like [https://mymind.com/](https://mymind.com/) does, eg. showing prices directly in the UI if the saved link is a product in a shop? If not, things like that would be a great addition!
> > 
> > > **touristtam** · [2025-05-02](https://news.ycombinator.com/item?id=43865854)
> > > 
> > > Site note: When a website advertising a product does a bad job at optimising the loading of the page, that's usually a red flag for me; yes that website has noticeable jitter when scrolling up and down even though it \_only\_ load around ~70Mb worth of assets initially.
> > > 
> > > **smcin** · [2025-05-01](https://news.ycombinator.com/item?id=43864619)
> > > 
> > > (The historical price on the day the link was published, or the current price, or over a date range, or configurable? I see different use-cases)
> 
> > **ryan29** · [2025-05-01](https://news.ycombinator.com/item?id=43863411)
> > 
> > I'd be interested to hear your thoughts on having a PWA vs regular mobile apps since it looks like you started with a PWA, but are moving to regular apps. Is that just a demand / eyeballs thing or were there technical reasons?
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43863667)
> > > 
> > > Mostly the UX it provides. PWAs are a quick and easy way to support mobile but the UX is nowhere near as good a traditional mobile app…
> 
> > **thm** · [2025-05-01](https://news.ycombinator.com/item?id=43861505)
> > 
> > I have about ~30k .webarchive files — is there a chance to import them?
> > 
> > > **SansGuidon** · [2025-05-02](https://news.ycombinator.com/item?id=43867870)
> > > 
> > > Even if importing them they might remain stuck in some import queue and you might not be able to search them. That was a blocker for me [https://github.com/linkwarden/linkwarden/issues/586](https://github.com/linkwarden/linkwarden/issues/586)
> 
> > **browningstreet** · [2025-05-01](https://news.ycombinator.com/item?id=43858286)
> > 
> > Suggestion/request:
> > 
> > What I'd really love is a super compact "short-name only" view of links. Just words, not lines or galleries. For super-high content views.
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43858403)
> > > 
> > > You can do that already:
> > > 
> > > [https://blog.linkwarden.app/releases/2.8#%EF%B8%8F-customiza...](https://blog.linkwarden.app/releases/2.8#%EF%B8%8F-customizable-view-and-adjustable-columns)
> > > 
> > > > **browningstreet** · [2025-05-01](https://news.ycombinator.com/item?id=43858458)
> > > > 
> > > > Ahh, yes, you can reduce it to names with a lot of columns. In my personal ideal, I've love to store a short-name for a link and have no boxes. Personally, I've always wanted links to be like the tag cloud in pinboard and to have a page with multiple tags/categories.
> > > > 
> > > > I'd also love a separation of human tags and AI tags (even by base or stem), just in case they provided radically different views, but both were useful.
> > > > 
> > > > EDIT: Just did a quick look in the documentation, is there a native or supported distinction between links that are like bookmarks and links that are more content/articles/resources?
> > > > 
> > > > **colordrops** · [2025-05-01](https://news.ycombinator.com/item?id=43860832)
> > > > 
> > > > Could still be a lot more compact. Would also like the hierarchical view in the main pane.
> > > > 
> > > > In any case, nice project, thank you.
> > 
> > > **colordrops** · [2025-05-01](https://news.ycombinator.com/item?id=43860779)
> > > 
> > > Came here to ask for exactly this.
> 
> > **dikdok** · [2025-05-01](https://news.ycombinator.com/item?id=43858280)
> > 
> > \> Full page archival
> > 
> > Does it grab the DOM from my browser as it sees it? Or is it a separate request? If so, how does it deal with authentication?
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43858359)
> > > 
> > > So there are different ways it archives a webpage.
> > > 
> > > It currently stores the full webpages as a single html file, a screenshot, a pdf, a read-it-later view.
> > > 
> > > Aside from that, you can also send the webpages to the Wayback Machine to take a snapshot.
> > > 
> > > To archive pages behind a login or paywall, you can use the browser extension, which captures an image of the webpage in the browser and sends it to the server.
> > > 
> > > > **dikdok** · [2025-05-01](https://news.ycombinator.com/item?id=43858406)
> > > > 
> > > > \> To archive pages behind a login or paywall, you can use the browser extension, which captures an image of the webpage in the browser and sends it to the server.
> > > > 
> > > > Just an image? So no full text search?
> > > > 
> > > > **warkdarrior** · [2025-05-01](https://news.ycombinator.com/item?id=43860144)
> > > > 
> > > > \> To archive pages behind a login or paywall, you can use the browser extension, which captures an image of the webpage in the browser and sends it to the server.
> > > > 
> > > > It'd be awesome to integrate this with the SingleFile extension, which captures any webpage into a self-contained HTML file (with JS, CSS, etc, inlined).
> > > > 
> > > > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43860232)
> > > > > 
> > > > > We might add this, it's actually highly suggested by the users :)
> 
> > **achierius** · [2025-05-01](https://news.ycombinator.com/item?id=43863536)
> > 
> > How difficult would it be to import an existing list of links/tags? Also, if I were using a hosted version, would I be able to eg insert/retrieve files via an API call?
> > 
> > I ask because currently I use Readwise but have a local script that syncs the reader files to a local DB, which then feeds into some custom agent flows I have going on on the side.
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43863632)
> > > 
> > > \> How difficult would it be to import an existing list of links/tags?
> > > 
> > > Pretty easy if you have it in a bookmark html file format.
> > > 
> > > \> Also, if I were using a hosted version, would I be able to eg insert/retrieve files via an API call?
> > > 
> > > Yup, check out the api documentation:
> > > 
> > > [https://docs.linkwarden.app/api/api-introduction](https://docs.linkwarden.app/api/api-introduction)
> 
> > **cosmic\_cheese** · [2025-05-01](https://news.ycombinator.com/item?id=43864255)
> > 
> > Interesting project! A couple of questions:
> > 
> > \- Does the web front end support themes? It’s a trivial thing but based on the screenshots, various things about the default theme bug me and it would be nice to be able to change those without a user style extension.
> > 
> > \- Does it have an API that would allow development of a native desktop front end?
> > 
> > > **daniel31x13** · [2025-05-02](https://news.ycombinator.com/item?id=43865276)
> > > 
> > > \> Does the web front end support themes?
> > > 
> > > Yes\[1\].
> > > 
> > > \> Does it have an API that would allow development of a native desktop front end?
> > > 
> > > Also yes\[2\].
> > > 
> > > \[1\]: [https://blog.linkwarden.app/releases/2.9#-customizable-theme](https://blog.linkwarden.app/releases/2.9#-customizable-theme)
> > > 
> > > \[2\]: [https://docs.linkwarden.app/api/api-introduction](https://docs.linkwarden.app/api/api-introduction)
> 
> > **yapyap** · [2025-05-01](https://news.ycombinator.com/item?id=43858150)
> > 
> > Very very neat!
> > 
> > a question arose for me though: if the AI tagging is self hostable as well, how taxing is it for the hardware, what would the minimum viable hardware be?
> > 
> > > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43858238)
> > > 
> > > Thanks! A lightweight model like the phi3:mini-4k is enough for this feature.\[1\]
> > > 
> > > It’s worth mentioning that you can also use external providers like OpenAI and Anthropic to tag the links for you.
> > > 
> > > \[1\]: [https://docs.linkwarden.app/self-hosting/ai-worker](https://docs.linkwarden.app/self-hosting/ai-worker)
> 
> > **Tsarp** · [2025-05-02](https://news.ycombinator.com/item?id=43866153)
> > 
> > Curious if the the paid tier helps support development of the project
> > 
> > > **daniel31x13** · [2025-05-02](https://news.ycombinator.com/item?id=43866210)
> > > 
> > > Definitely! :)
> 
> > **jychang** · [2025-05-02](https://news.ycombinator.com/item?id=43867643)
> > 
> > \> Optional local AI tagging
> > 
> > [https://docs.linkwarden.app/self-hosting/ai-worker](https://docs.linkwarden.app/self-hosting/ai-worker)
> > 
> > I took a look at this... and you use the Ollama API behind the scenes?? Why not use an OpenAI compatible endpoint like the rest of the industry?
> > 
> > Locking it to Ollama is stupid. Ollama is just a wrapper for llama.cpp anyways. Literally everyone else running LLMs locally- llama.cpp, vllm (which is what the inference providers use, also I know Deepseek API servers use this behind the scenes), LM Studio (for the causal people), etc all use an OpenAI compatible api endpoint. Not to mention OpenAI, Google, Anthropic, Deepseek, Openrouter, etc all mainly use (or at least fully supports, in the case of Google) an OpenAI compatible endpoint.
> > 
> > > **CaptainFever** · [2025-05-02](https://news.ycombinator.com/item?id=43867674)
> > > 
> > > You could contribute an option!
> > > 
> > > **dewey** · [2025-05-02](https://news.ycombinator.com/item?id=43868299)
> > > 
> > > \> Locking it to Ollama is stupid.
> > > 
> > > If you don’t like this free and open source software that was shared it’s luckily possible to change it yourself…or if it’s not supporting your favorite option you can also just ignore it. No need to call someone’s work or choices stupid.
> > > 
> > > > **jychang** · [2025-05-02](https://news.ycombinator.com/item?id=43868351)
> > > > 
> > > > Strong disagree. Just because something is free and open source does not make it good. Call a spade a spade.
> > > > 
> > > > Ollama is a piece of shit software that basically stole the work of llama.cpp, locks down their GGUFs files so it cannot be used by other software on your machine, misleads users by hiding information (like what quant you are using, who produced the GGUF, etc), created their own API endpoint to lock in users instead of using a standard OpenAI compatible API, and more problems.
> > > > 
> > > > It's like they looked at all the *bad* walled garden things Apple does and took it as a todo list.
> > > > 
> > > > > **dewey** · [2025-05-02](https://news.ycombinator.com/item?id=43868744)
> > > > > 
> > > > > That’s not the point, you didn’t say “Ollama is stupid” you said “Locking it to Ollama is stupid”.
> > > > > 
> > > > > Not every person is aware of all faults or politics of all their dependencies.
> > > > > 
> > > > > > **jychang** · [2025-05-03](https://news.ycombinator.com/item?id=43878086)
> > > > > > 
> > > > > > That's an absolutely terrible defense. Ignorance is not an excuse, try telling that to a police officer.
> > > > > > 
> > > > > > And plus, certain people are held to a higher standard. It's not like I'm expecting a random person on the street to know about Ollama, but someone building AI software is expected to research what they are using and do their due diligence. To plead ignorance is to assert incompetence at best and negligence at worst.

> **evanjrowley** · [2025-05-01](https://news.ycombinator.com/item?id=43860991)
> 
> I've been using Karakeep (formerly known as Hoarder) and it's been a great experience so far. One thing they're working on now is a Safari browser extension. I noticed Linkwarden lacks a Safari browser extension - is one on the roadmap?
> 
> Lately I've been using MacOS and I've noticed Chromium-based browsers use more resources than the native Safari. This is especially true with Microsoft Edge, which sometimes consumes tens of gigabytes of RAM (possibly a memory leak?). In an attempt to preserve battery life and SSD longevity, Safari is now my go-to browser on MacOS.
> 
> > **InsideOutSanta** · [2025-05-01](https://news.ycombinator.com/item?id=43861196)
> > 
> > I'm also using Karakeep. It also has LLM-powered tagging, which, in my experience, works excellently. It's easy to self-host, fast on a relatively underpowered NAS, and I love the UX. Highly recommended.
> > 
> > Linkwarden looks nice, too, but when picking an option, I wanted one with a native Android app.
> > 
> > > **piyuv** · [2025-05-01](https://news.ycombinator.com/item?id=43863084)
> > > 
> > > I chose linkwarden after seeing hoarder’s native iOS app
> > > 
> > > > **evanjrowley** · [2025-05-02](https://news.ycombinator.com/item?id=43865556)
> > > > 
> > > > Bitter irony is that the one with the best iOS app is lacking a Safari extension, while the one with a mediocre iOS app already has a beta Safari extension.

> **gibibit** · [2025-05-01](https://news.ycombinator.com/item?id=43858919)
> 
> Is there any software that can provide verified, trusted archives of websites?
> 
> For example, we can go to the Wayback Machine at archive.org to not only see what a website looked like in the past, but prove it to someone (because we implicitly trust The Internet Archive). But the Wayback Machine has deleted sites when a site later changes its robots.txt to exclude it, meaning that old site REALLY disappears from the web forever.
> 
> The difficulty for a trusted archive solution is in proving that the archived pages weren't altered, and that the timestamp of the capture was not altered.
> 
> It seems like blockchain would be a big help, and would prevent back-dating future snapshots, but there seem to be a lot of missing pieces still.
> 
> Thoughts?
> 
> > **shrinks99** · [2025-05-01](https://news.ycombinator.com/item?id=43859109)
> > 
> > Webrecorder's WACZ signing spec ([https://specs.webrecorder.net/wacz-auth/latest](https://specs.webrecorder.net/wacz-auth/latest)) does some of this — authenticating the identity of who archived it and at what time — but the rest of what you're asking for (legitimacy of the content itself) is an unsolved problem as web content isn't all signed by its issuing server.
> > 
> > In some of the case studies Starling ([https://www.starlinglab.org/](https://www.starlinglab.org/)) has published, they've published timestamps of authenticated WACZs to blockchains to prove that they were around at a specific time... More \_layers\_ of data integrity but not 100% trustless.
> > 
> > > **gibibit** · [2025-05-01](https://news.ycombinator.com/item?id=43863281)
> > > 
> > > Very informative, thanks!
> 
> > **yencabulator** · [2025-05-08](https://news.ycombinator.com/item?id=43930865)
> > 
> > There's been attempts to standardize a way for a HTTPS server to say "Yes, this response really did come from me", but nothing has been really adopted.
> > 
> > [https://www.rfc-editor.org/rfc/rfc9421.html](https://www.rfc-editor.org/rfc/rfc9421.html)
> > 
> > [https://httpsig.org/](https://httpsig.org/)
> > 
> > Without the server participating, best you can do is a LetsEncrypt-style "we made this request from many places and got the same response" statement by a trusted party.
> > 
> > Inspiration: roughtime can be used to piggyback a "proof of known hash at time" mechanism, without blockchain waste. That lets you say "I've had this file since this time".
> > 
> > [https://www.imperialviolet.org/2016/09/19/roughtime.html](https://www.imperialviolet.org/2016/09/19/roughtime.html)
> > 
> > [https://int08h.com/post/to-catch-a-lying-timeserver/](https://int08h.com/post/to-catch-a-lying-timeserver/)
> > 
> > [https://blog.cloudflare.com/roughtime/](https://blog.cloudflare.com/roughtime/)
> > 
> > [https://news.ycombinator.com/item?id=12599705](https://news.ycombinator.com/item?id=12599705)
> > 
> > **dj0k3r** · [2025-05-01](https://news.ycombinator.com/item?id=43861697)
> > 
> > Take a look at singleFile - a project that lets you save the entire webpage. It has an integration for saving the hash if the page on a Blockchain. You can choose to set it up between parties who're interested in the provenance of the authenticity.
> > 
> > **mitya777** · [2025-05-03](https://news.ycombinator.com/item?id=43880887)
> > 
> > we pull the contents of any publicly-posted links and write them onto big block bitcoin blockchain [https://home.treechat.ai/quest/8ca85b16-739c-4b7a-8376-38bc0...](https://home.treechat.ai/quest/8ca85b16-739c-4b7a-8376-38bc0b8406d3)

> **virtualcharles** · [2025-05-01](https://news.ycombinator.com/item?id=43857785)
> 
> As a paid product, has anyone used Raindrop as well and have opinions/comparisons? And on the self hosted side, vs Hoarder?
> 
> I’ve been considering switching from Raindrop to a self hosted option, but while I like self hosting I’m also leaning towards just paying someone to handle this particular service for me.
> 
> > **spiffotron** · [2025-05-01](https://news.ycombinator.com/item?id=43862587)
> > 
> > I used to use raindrop however found it a bit bloated with features I never use, I've switched to selfhosting linkding: [https://linkding.link](https://linkding.link/) and enjoy the much more minimal experience
> > 
> > **exhilaration** · [2025-05-01](https://news.ycombinator.com/item?id=43859754)
> > 
> > I've never heard of raindrop and it looks cool but I see the .ru in one of their screenshots -- are they based in Russia? Any concerns with doing business with a Russian company, in the context of sanctions etc.?
> > 
> > > **mwnivek** · [2025-05-02](https://news.ycombinator.com/item?id=43865358)
> > > 
> > > Rustem Mussabekov on 24 Oct 2023 wrote: "I'm founder of Raindrop.io. I'd like to clarify information about the origin of myself and the project. While I did live in Russia for a long time and initially started Raindrop there, I relocated to my motherland, Kazakhstan, shortly after the war began. I also moved all financial and business matters there.
> > > 
> > > I am no longer associated with Russia in any way. It would be great if this information could be added to the article."
> > > 
> > > Source: [https://numericcitizen.me/when-war-in-ukraine-influences-my-...](https://numericcitizen.me/when-war-in-ukraine-influences-my-application-choices/)
> 
> > **regularjack** · [2025-05-01](https://news.ycombinator.com/item?id=43858446)
> > 
> > I also use raindrop, but been looking at self-hosted alternatives as raindrop does not encrypt the data, so I can't use it for work stuff.
> > 
> > **toomuchtodo** · [2025-05-01](https://news.ycombinator.com/item?id=43859461)
> > 
> > I pay for Raindrop, very useful to have someone else run it, minimal cost.
> > 
> > **carlosjobim** · [2025-05-01](https://news.ycombinator.com/item?id=43858937)
> > 
> > I tried Raindrop, but it was not usable to me because it constantly logged you out.
> > 
> > **flashblaze** · [2025-05-01](https://news.ycombinator.com/item?id=43859416)
> > 
> > I have been using Raindrop and like it quite a bit

> **bravura** · [2025-05-01](https://news.ycombinator.com/item?id=43864473)
> 
> I want LLM accessible bookmarks. That's it.
> 
> It doesn't work yet.
> 
> I use singlefile to archive pages I'm viewing Linkding.
> 
> Then I have a BeautifulScript4 script to strip the assets.
> 
> Then I use Jina's ReaderLM v2 to render the HTML to proper Markdown: [https://huggingface.co/jinaai/ReaderLM-v2](https://huggingface.co/jinaai/ReaderLM-v2)
> 
> Except, of course, for longer table oriented text documents like HN that doesn't work.
> 
> I want a plaintext archive of web pages in a github repo or similar. Not a fancy UI/UX
> 
> > **touristtam** · [2025-05-02](https://news.ycombinator.com/item?id=43865952)
> > 
> > Links:
> > 
> > \- SingleFile: [https://github.com/gildas-lormeau/SingleFile](https://github.com/gildas-lormeau/SingleFile)
> > 
> > \- Linkding: [https://github.com/sissbruecker/linkding](https://github.com/sissbruecker/linkding)
> > 
> > \- BeautifulScript4: [https://beautiful-soup-4.readthedocs.io/en/latest/](https://beautiful-soup-4.readthedocs.io/en/latest/) (assumed that was the python library Beautiful Soup 4 and not "Script")

> **mikae1** · [2025-05-01](https://news.ycombinator.com/item?id=43857196)
> 
> See also:
> 
> [https://www.linkace.org/](https://www.linkace.org/) (my fave)
> 
> [https://github.com/sissbruecker/linkding](https://github.com/sissbruecker/linkding)
> 
> [https://github.com/jonschoning/espial](https://github.com/jonschoning/espial)
> 
> [https://motd.co/2023/09/postmarks-launch/](https://motd.co/2023/09/postmarks-launch/)
> 
> [https://betula.mycorrhiza.wiki/](https://betula.mycorrhiza.wiki/)
> 
> [https://linkhut.org/](https://linkhut.org/)
> 
> > **tummler** · [2025-05-01](https://news.ycombinator.com/item?id=43857369)
> > 
> > Also: [https://github.com/karakeep-app/karakeep](https://github.com/karakeep-app/karakeep)
> > 
> > **renegat0x0** · [2025-05-02](https://news.ycombinator.com/item?id=43866696)
> > 
> > [https://bookmarkos.com/](https://bookmarkos.com/)
> > 
> > [https://grimoire.pro/](https://grimoire.pro/)
> > 
> > [https://hoarder.app/](https://hoarder.app/)
> > 
> > [https://mymind.com/](https://mymind.com/)
> > 
> > [https://github.com/omnivore-app/omnivore](https://github.com/omnivore-app/omnivore)
> > 
> > [https://github.com/wallabag/wallabag](https://github.com/wallabag/wallabag)
> > 
> > [https://betula.mycorrhiza.wiki/](https://betula.mycorrhiza.wiki/)
> > 
> > [https://zotero.org/](https://zotero.org/)
> > 
> > **s17tnet** · [2025-05-01](https://news.ycombinator.com/item?id=43857427)
> > 
> > [https://github.com/ArchiveBox/ArchiveBox](https://github.com/ArchiveBox/ArchiveBox)
> > 
> > **ydj** · [2025-05-02](https://news.ycombinator.com/item?id=43866283)
> > 
> > One more: [https://conifer.rhizome.org/](https://conifer.rhizome.org/)
> > 
> > This one seems to be directly related to the webrecorder project which seems like a pretty full featured warc recorder.
> > 
> > **jamroom** · [2025-05-01](https://news.ycombinator.com/item?id=43858696)
> > 
> > I've tried most archiving/bookmarking self hosted solutions I could find and the one I like the best is:
> > 
> > [https://readeck.org/en/](https://readeck.org/en/)

> **dennisy** · [2025-05-01](https://news.ycombinator.com/item?id=43861785)
> 
> I love these sorts of apps, but I still am not really sure why I need the webpages. At any time I do research for a topic I find more things than I can read in that session, so what are the old links for?
> 
> I would love to hear how people use this product once they have stored the links!
> 
> > **ryan29** · [2025-05-01](https://news.ycombinator.com/item?id=43863274)
> > 
> > I've used [https://historio.us](https://historio.us/) since 2011 and still pay for it to keep access to all the pages I've archived over the years. The price has been kept low enough that I can't bring myself to cancel it even though I've been using self-hosted [https://archivebox.io/](https://archivebox.io/) for the last few years.
> > 
> > I always include an archived link whenever I reference something in documentation. That's my main use at the moment.
> > 
> > However, I also feel like I've gotten a lot of really good value when trying to learn a new development topic. Whenever I find something that looks like it *might* be useful, I archive it and, because everything is searchable, I end up with a searchable index of really high quality content once I actually know what I'm doing.
> > 
> > I find it hard to rediscover content via web search these days and there's so much churn that having a personal archive of useful content is going to increase in value, at least in my opinion.
> > 
> > > **touristtam** · [2025-05-02](https://news.ycombinator.com/item?id=43865793)
> > > 
> > > How much space is the self-hosted solution taking? I've been meaning to try and find a better way to look through my bookmarks since no browser is capable of doing that properly it seems.
> 
> > **Lammy** · [2025-05-01](https://news.ycombinator.com/item?id=43862997)
> > 
> > I haven't tried Linkwarden (still doing the \`wget --mirror\` thing myself), but one of the reasons I like archiving pages is so I can have a collection of pages that work in older browsers on vintage computers. I pop open View Source on any site I find that looks even vaguely old, and if I see a DOCTYPE up to and including XHTML 1.1 I archive that shit *immediately* even if it's not a site about any of my biggest interests lol

> **nickfixit** · [2025-05-01](https://news.ycombinator.com/item?id=43857824)
> 
> I like hoarder(karakeep). It's got an API and mcp server as well to play with now locally and self hosted. I'll check this out as well.

> **rrgok** · [2025-05-02](https://news.ycombinator.com/item?id=43867450)
> 
> I tried with the demo, but full content search does not work. I don't know if the demo is randomly generated, anyway this is the test I did.
> 
> Text to search in the top search bar: RRP
> 
> Page that contains that term: [https://www.da.vidbuchanan.co.uk/blog/r1-jailbreak.html](https://www.da.vidbuchanan.co.uk/blog/r1-jailbreak.html)
> 
> Result found: 0
> 
> Does this search the content of the archived pages?
> 
> > **SansGuidon** · [2025-05-02](https://news.ycombinator.com/item?id=43867878)
> > 
> > Could be related to this as well -> [https://github.com/linkwarden/linkwarden/issues/586](https://github.com/linkwarden/linkwarden/issues/586) where content seems imported but its indexation is stuck in the queue. Blocker for me.
> > 
> > > **bflesch** · [2025-05-02](https://news.ycombinator.com/item?id=43867892)
> > > 
> > > the trap of using indexation and a database when normal grep would work with disk-based storage
> > > 
> > > > **SansGuidon** · [2025-05-02](https://news.ycombinator.com/item?id=43868624)
> > > > 
> > > > Exactly... so much hype around complexity when simplicity wins. That's also why such systems like Wallabag, Linkwarden, Omnivore etc all disappointed me. In the end with a simple system made of static files and tools available out of the box on most distributions, I could make my own alternative to most archiving/bookmarking management systems and it just works. No DB, no framework, no fancy UI. Yet powerful. I have to blog about it.
> > > > 
> > > > > **rrgok** · [2025-05-02](https://news.ycombinator.com/item?id=43868950)
> > > > > 
> > > > > Do you mind sharing your approach? I've been looking for a system where I can store all kind of data (webpage, pdf, images, docx, xlsx...) and can fast full-text search on them. Oddly enough, that what a filesystem should do, but sadly that's not gonna happen.
> > > > > 
> > > > > Can grep and the like search on images or docx?
> > > > > 
> > > > > I know there is FileLocator Pro, but I'm looking for a cross-platform tool.
> > > > > 
> > > > > > **SansGuidon** · [2025-05-02](https://news.ycombinator.com/item?id=43870882)
> > > > > > 
> > > > > > I mostly focus on text based content so PDF and webpages are easily supported. for PDFs I thought about using [https://github.com/phiresky/ripgrep-all](https://github.com/phiresky/ripgrep-all) or pdfgrep [https://pdfgrep.org/](https://pdfgrep.org/)
> > > > > > 
> > > > > > For images, what do you want to grep for? for exif data -> [https://exiftool.org/](https://exiftool.org/) if you want to find image based content, you might need something smarter. I think maybe it is a place where tools such as [https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5) can shine for me. simple enough to work with most of my images and tag them according to some preferences, and I would save such tags in a txt file.
> > > > > > 
> > > > > > Anyway, all metadata I store about images, links etc are all persisted in txt files. summaries, tags, etc, incoming/outgoing links etc, each has its own file. There are folders per link/content. Under each folder, one file per type of metadata. So it is very easy to know if some metadata is missing for a file, no index needed, it is just as simple as checking the presence of a file. everything is compatible with grep then.
> > > > > > 
> > > > > > for docx and xlsx it is out of my plate at this time, I didn't experiment enough to judge what works well enough. I hate those things.
> > > > > > 
> > > > > > > **bflesch** · [2025-05-03](https://news.ycombinator.com/item?id=43877837)
> > > > > > > 
> > > > > > > As docx / xlsx are zip files, I normally unzip them and then use some sort of XML-aware grep. But these formats are a rabbithole on their own ;)

> **idkalexj** · [2025-05-01](https://news.ycombinator.com/item?id=43860045)
> 
> An alt suggestion, I use Eagle ([https://eagle.cool/](https://eagle.cool/)) for this.
> 
> I started using it primarily for images inspiration collecting but it has grown into my "everything" collecting, including bookmarks.
> 
> Libraries can be shared via file sharing (e.g. google drive, dropbox), one time purchase price, amazing software design, extensions, and more.
> 
> > **nemomarx** · [2025-05-01](https://news.ycombinator.com/item?id=43860126)
> > 
> > Is it Mac only temporarily or do you think they'll stick with that?
> > 
> > > **InsideOutSanta** · [2025-05-01](https://news.ycombinator.com/item?id=43861215)
> > > 
> > > Eagle has a Windows version.

> **9\_BAR** · [2025-05-02](https://news.ycombinator.com/item?id=43870329)
> 
> Howdy -- I just spun up my own instance yesterday, as it turns out. Very slick! I've already converted from NextCloud's Bookmark manager.
> 
> Quick suggestion:
> 
> I like to maintain separate browser configurations (in this case, using top-level collections named "Vivaldi," "Chrome," etc.). What might be nice is the ability to link other (non-browser) collections. So, if I create a collection of news blog websites, I can turn around and include those in each browser collection. That way, those news blog sites are centrally maintained once. In other words, browser collections become assemblies.
> 
> Let me know what you think!

> **FireInsight** · [2025-05-01](https://news.ycombinator.com/item?id=43856835)
> 
> No experience with this yet, but looking to upgrade from Linkding. Main features I'm looking forward to is syncing the bookmarks with native browsers bookmarks through Floccus, and being able to make highlights on the articles I save.

> **raybb** · [2025-05-01](https://news.ycombinator.com/item?id=43860168)
> 
> Just wish it had offline support. That's really the main use case for me is when I'm traveling and have spotty internet. Read articles offline and hopefully add some to the queue to be saved when I'm online again.
> 
> > **daniel31x13** · [2025-05-01](https://news.ycombinator.com/item?id=43860449)
> > 
> > We’re working on an official mobile app\[1\], which will most likely include this feature sometime after its launch :)
> > 
> > \[1\]: [https://github.com/linkwarden/linkwarden/issues/246#issuecom...](https://github.com/linkwarden/linkwarden/issues/246#issuecomment-2826821585)
> > 
> > > **raybb** · [2025-05-01](https://news.ycombinator.com/item?id=43860591)
> > > 
> > > An official app with that sounds great! From what you know, would it be possible to also have offline support with the PWA?
> > > 
> > > **csdvrx** · [2025-05-01](https://news.ycombinator.com/item?id=43860563)
> > > 
> > > Will the offline mode work on laptops?

> **aiono** · [2025-05-01](https://news.ycombinator.com/item?id=43861733)
> 
> Looks really neat. But it also seems a bit heavyweight (for the client). Is it the case compared to [https://readeck.org/en/](https://readeck.org/en/) ?
> 
> > **lilerjee** · [2025-05-08](https://news.ycombinator.com/item?id=43931743)
> > 
> > There is a lightweight bookmark manager [https://metaesn.com](https://metaesn.com/) , not only manage bookmarks, but also other resources (notes, articles, etc.)

> **ibaikov** · [2025-05-01](https://news.ycombinator.com/item?id=43858478)
> 
> Recently started selfhosting it. I like it. I tried hoarder, but it was overcomplicated and consumed way more resources. Now it got MCP, so I might use it with n8n, we'll see.
> 
> A couple improvements I'd like: I want drag-and-drop link saving.
> 
> If I add a reddit link, it doesn't import the reddit thread title, it uses reddit's title in linkwarden (Reddit - the heart of the internet). Same goes for a few other websites like gitlab.
> 
> I'd like an MCP.
> 
> Resource usage optimization: while it is smaller than karakeep/hoarder, for me it consumes 500-950MB ram, and I have only 500 links added.

> **adityamwagh** · [2025-05-02](https://news.ycombinator.com/item?id=43864954)
> 
> I personally use Raindrop.io \[0\]. I have used it for more than 3 years and it does it's job very well.
> 
> \[0\] [http://raindrop.io/](http://raindrop.io/)

> **agnishom** · [2025-05-02](https://news.ycombinator.com/item?id=43867212)
> 
> I recently started using Hoarder for this; once Omnivore went down under...
> 
> [https://hoarder.app](https://hoarder.app/)

> **sloped** · [2025-05-01](https://news.ycombinator.com/item?id=43858924)
> 
> This looks nice, I like how many of these tools have been surfacing. I recently started using [https://readeck.org/](https://readeck.org/), which aims to solve some of the same problems and really like it. Much better than a "bookmark" tool for things like articles.
> 
> My two favorite parts of Readeck are:
> 
> \- it provides a OPDS catalog of your saved content so you can very easily read things on your e-book reader of choice. I use KOReader on a Kindle and have really enjoyed reading my saved articles in the backyard after work.
> 
> \- you can generate a share link. I have used this to share some articles behind paywalls with friends and family where before I was copying and pasting content into an email.

> **spyder** · [2025-05-01](https://news.ycombinator.com/item?id=43861852)
> 
> There is also KaraKeep:
> 
> [https://github.com/karakeep-app/karakeep](https://github.com/karakeep-app/karakeep)
> 
> Seems very similar.

> **manmal** · [2025-05-01](https://news.ycombinator.com/item?id=43861655)
> 
> I‘m a heavy user and really happy with the speed and stability I‘m getting, running Linkwarden on my Hetner VPS. Only problem was in the beginning, importing a lot of existing links from Pinboard, the available RAM of my meager VPS was exceeded multiple times by metadata resolution. But once that‘s been overcome, it’s a zero effort tool.

> **xwat** · [2025-05-01](https://news.ycombinator.com/item?id=43859831)
> 
> The only issue stopping me from using Linkwarden is that it creates duplicates when importing bookmarks, see [https://github.com/linkwarden/linkwarden/issues/442](https://github.com/linkwarden/linkwarden/issues/442)

> **fuzzy2** · [2025-05-01](https://news.ycombinator.com/item?id=43858166)
> 
> Started using it a while back. Works rather well, even though some minor UX quirks exist. Self-hosting is easy, too, with Docker Compose. If you're in the market for a web-accessible bookmark manager, maybe give it a go!

> **simonebrunozzi** · [2025-05-02](https://news.ycombinator.com/item?id=43874355)
> 
> \> Unlock 14 days of Premium Service at no cost!
> 
> So, I assume you want me to pay per month. No, thank you. I'd pay you $10 or $20, once, and use the app forever.
> 
> > **sergiomattei** · [2025-05-02](https://news.ycombinator.com/item?id=43874812)
> > 
> > Shouldn't this dev be compensated for their ongoing labor and cloud computing costs?

> **salynchnew** · [2025-05-01](https://news.ycombinator.com/item?id=43861735)
> 
> Very cool project!
> 
> QQ for users: How is the UX compared with ArchiveBox?

> **belter** · [2025-05-01](https://news.ycombinator.com/item?id=43857050)
> 
> As of this moment...This post has 4 points and 2 comments...How does it make to number 3 on HN page?
> 
> > **A4ET8a8uTh0\_v2** · [2025-05-01](https://news.ycombinator.com/item?id=43857111)
> > 
> > Velocity. Obviously, I don't really know and speculating only. Still, the project does look nice. I personally use archivebox, but I will admit this looks a lot more polished.

> **snapplebobapple** · [2025-05-02](https://news.ycombinator.com/item?id=43874294)
> 
> This is an excellent bookmark sync tool by way of floccus integration

> **human\_llm** · [2025-05-01](https://news.ycombinator.com/item?id=43857164)
> 
> This looks interesting. How feature-crippled is the self hosted version?
> 
> > **dugite-code** · [2025-05-01](https://news.ycombinator.com/item?id=43857646)
> > 
> > Not at all as far as I am aware. I use floccus to sync my bookmarks to it and it does the job quite well

> **ijustwanttovote** · [2025-05-01](https://news.ycombinator.com/item?id=43861867)
> 
> I'm paying for readwise, any benefits of switching over to this?
> 
> > **borg16** · [2025-05-01](https://news.ycombinator.com/item?id=43862606)
> > 
> > it's a third of the price to begin with. I think readwise has a winner in reader app, but they sure do charge a premium for the same. You can get the same functionality in linkwarden or pinboard for a fraction of readwise's subscription pricing.

> **carterschonwald** · [2025-05-01](https://news.ycombinator.com/item?id=43862943)
> 
> Is there a way to import pinboard or similar data?
> 
> > **daniel31x13** · [2025-05-02](https://news.ycombinator.com/item?id=43865301)
> > 
> > Yes, you can import any kind of bookmarks html files.
> > 
> > There are also other importing formats we do support as well like Wallabag, Omnivore, etc…

> **xnx** · [2025-05-01](https://news.ycombinator.com/item?id=43857609)
> 
> I have yet to find anything that has the effort vs. results benefit of CTRL+S -> "Webpage, Single File (\*.mhtml)". Even works on mobile.
> 
> > **FireInsight** · [2025-05-01](https://news.ycombinator.com/item?id=43857876)
> > 
> > Tagging, full-text search, page highlights, a nice UI,... You might call that bloat, I don't. Besides, I could not find any equivalent to ctrl-s the webpage on mobile Firefox.
> > 
> > > **xnx** · [2025-05-01](https://news.ycombinator.com/item?id=43858022)
> > > 
> > > \> I could not find any equivalent to ctrl-s the webpage on mobile Firefox.
> > > 
> > > True. There used to be an extension that enabled the hidden code path, but that stopped working years ago. I switched to Kiwi browser.
> 
> > **Vinz\_** · [2025-05-01](https://news.ycombinator.com/item?id=43857493)
> > 
> > The first version was released in July 2023, I don’t see why this would shut down in two months.
> > 
> > This comment makes a lot of assumptions but does not substantiate any of them, please refrain from dunking on other peoples projects like this, it does not contribute anything to the discussion.
> > 
> > **bovermyer** · [2025-05-01](https://news.ycombinator.com/item?id=43857446)
> > 
> > Jeez man, who crapped in your Cheerios this morning? I hope your day gets better.

> **nexle** · [2025-05-01](https://news.ycombinator.com/item?id=43858199)
> 
> The pushing on their cloud offering almost everywhere (main page: [https://linkwarden.app/](https://linkwarden.app/), GitHub README: [https://github.com/linkwarden/linkwarden](https://github.com/linkwarden/linkwarden), and installation guide: [https://docs.linkwarden.app/self-hosting/installation](https://docs.linkwarden.app/self-hosting/installation)) just give me a bad taste about it.
> 
> I understood an open source project need revenue to survive, but the reason why this project grew so large is because of the self-hostable nature, and the push of the cloud offering is the opposite of that.
> 
> I really hope this is not the first steps towards enshittification...
> 
> > **ctxc** · [2025-05-01](https://news.ycombinator.com/item?id=43858241)
> > 
> > Nah, I just see this as a sustainable way to keep the project alive :)