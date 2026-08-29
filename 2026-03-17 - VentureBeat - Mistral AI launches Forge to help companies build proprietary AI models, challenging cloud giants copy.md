---
source: "https://venturebeat.com/infrastructure/mistral-ai-launches-forge-to-help-companies-build-proprietary-ai-models"
author:
  - "[[Michael Nuñez]]"
published: 2026-03-17
created: 2026-04-17
---
![nuneybits Vector art of a Forge made of computer code in the co e81353af-4d23-4b20-853d-84fad8cc9b3f](https://venturebeat.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fjdtwqhzvc2n1%2F4TvXdOwVTUgTDCioxZUcYC%2Fcd8c6de13db530abc6a2ba91175dc5b4%2Fnuneybits_Vector_art_of_a_Forge_made_of_computer_code_in_the_co_e81353af-4d23-4b20-853d-84fad8cc9b3f.webp%3Fw%3D1000%26q%3D100&w=3840&q=85)

Credit: VentureBeat made with Midjourney

[Mistral AI](https://mistral.ai/) on Monday launched [Forge](https://mistral.ai/products/forge), an enterprise model training platform that allows organizations to build, customize, and continuously improve AI models using their own proprietary data — a move that positions the French AI lab squarely against the hyperscale cloud providers in one of the most consequential and least understood markets in enterprise technology.

The announcement caps a remarkably aggressive week for Mistral, which also released its Mistral [Small 4 model](https://mistral.ai/news/mistral-small-4), unveiled Leanstral — an open-source code agent for formal verification — and joined the newly formed Nvidia [Nemotron Coalition](https://nvidianews.nvidia.com/news/nvidia-launches-nemotron-coalition-of-leading-global-ai-labs-to-advance-open-frontier-models) as a co-developer of the coalition's first open frontier base model. Together, these moves paint the picture of a company that is no longer content to compete on model benchmarks alone and is instead racing to become the infrastructure backbone for organizations that want to own their AI rather than rent it.

[Forge](https://mistral.ai/products/forge) goes significantly beyond the fine-tuning APIs that Mistral and its competitors have offered for the past year. The platform supports the full model training lifecycle: pre-training on large internal datasets, post-training through supervised fine-tuning, DPO, and ODPO, and — critically — reinforcement learning pipelines designed to align models with internal policies, evaluation criteria, and operational objectives over time.

"Forge is Mistral's model training platform," said Elisa Salamanca, head of product at Mistral AI, in an exclusive interview with VentureBeat ahead of the launch. "We've been building this out behind the scenes with our AI scientists. What Forge actually brings to the table is that it lets enterprises and governments customize AI models for their specific needs."

## Why Mistral says fine-tuning APIs are no longer enough for serious enterprise AI

The distinction Mistral is drawing — between lightweight fine-tuning and full-cycle model training — is central to understanding why [Forge](https://mistral.ai/products/forge) exists and whom it serves.

For the past two years, most enterprise AI adoption has followed a familiar pattern: companies select a general-purpose model from [OpenAI](https://openai.com/), [Anthropic](https://www.anthropic.com/), [Google](https://www.google.com/), or an open-source provider, then apply fine-tuning through a cloud API to adjust the model's behavior for a narrow set of tasks. This approach works well for proof-of-concept deployments and many production use cases. But Salamanca argues that it fundamentally plateaus when organizations try to solve their hardest problems.

"We had a fine-tuning API relying on supervised fine-tuning. I think it was kind of what was the standard a couple of months ago," Salamanca told VentureBeat. "It gets you to a proof-of-concept state. Whenever you actually want to have the performance that you're targeting, you need to go beyond. AI scientists today are not using fine-tuning APIs. They're using much more advanced tools, and that's what Forge is bringing to the table."

What [Forge](https://mistral.ai/products/forge) packages, in Salamanca's telling, is the training methodology that Mistral's own AI scientists use internally to build the company's flagship models — including data mixing strategies, data generation pipelines, distributed computing optimizations, and battle-tested training recipes. She drew a sharp line between Forge and the open-source tools and community tutorials that are freely available today.

"There's no platform out there that provides you real-world training recipes that work," Salamanca said. "Other open-source repositories or other tools can give you generic configurations or community tutorials, but they don't give you the recipe that's been validated — that we've been doing for all of our flagship models today."

## From ancient manuscripts to hedge fund quant languages, early customers reveal what off-the-shelf AI can't do

The obvious question facing any product like Forge is demand. In a market where [GPT-5](https://openai.com/index/introducing-gpt-5/), [Claude](https://claude.ai/), [Gemini](https://gemini.google.com/app), and a growing fleet of open-source models can handle an enormous range of tasks, why would an enterprise invest the time, compute, and expertise required to train its own model from scratch?

Salamanca acknowledged the question head-on but argued that the need emerges quickly once companies move beyond generic use cases. "A lot of the existing models can get you very far," she said. "But when you're looking at what's going to make you competitive compared to your competition — everyone can adopt and use the models that are out there. When you want to go a step beyond that, you actually need to create your own models. You need to leverage your proprietary information."

The real-world examples she cited illustrate the edges of the current model ecosystem. In one case, Mistral worked with a public institution that had ancient manuscripts with missing text from damaged sections. "The models that were available were not able to do this because they've never seen the data," Salamanca explained. "Digitization was not very good. There were some unique patterns and characters, and so we actually created a model for them to fill in the spans. This is now used by their researchers, and it's accelerating their publication and understanding of these documents."

In another engagement, Mistral partnered with [Ericsson](https://www.ericsson.com/en/news/2026/2/mistral-ai-and-ericsson-partner-to-drive-ai-innovation-in-telecom) to customize its [Codestral](https://mistral.ai/news/codestral) model for legacy-to-modern code translation. Ericsson, Salamanca said, has built up half a decade of proprietary knowledge around an internal calling language — a codebase so specialized that no off-the-shelf model has ever encountered it. "The concrete impact is like turning a year-long manual migration process, where each engineer needs six months of onboarding, to something that's really more scalable and faster," she said.

Perhaps the most telling example involves hedge funds. Salamanca described working with financial firms to customize models for proprietary quantitative languages — the kind of deeply guarded intellectual property that these firms keep on-premises and never expose to cloud-hosted AI services. Using Forge's reinforcement learning capabilities, Mistral helped one hedge fund develop custom benchmarks and then trained the model to outperform on them, producing what Salamanca called "a unique model that was able to give them the competitive edge that was needed."

## How Forge makes money: license fees, data pipelines, and embedded AI scientists

Forge's business model reflects the complexity of enterprise model training. According to Salamanca, it operates across several revenue streams. For customers who run training jobs on their own GPU clusters — a common requirement in highly regulated or IP-sensitive industries — Mistral does not charge for compute. Instead, the company charges a license fee for the Forge platform itself, along with optional fees for data pipeline services and what Mistral calls "forward-deployed scientists" — embedded AI researchers who work alongside the customer's team.

"No competitor out there today is kind of selling this embedded scientist as part of their training platform offering," Salamanca said.

This model has clear echoes of [Palantir's early playbook](https://www.theaiopportunities.com/p/the-palantir-origin-playbook-20032013), where forward-deployed engineers served as the critical bridge between powerful software and the messy reality of enterprise data. It also suggests that Mistral recognizes a fundamental truth about the current state of enterprise AI: the technology alone is not enough. Most organizations lack the internal expertise to design effective training recipes, curate data at scale, or navigate the treacherous optimization landscape of distributed GPU training.

The infrastructure itself is flexible. Training can happen on Mistral's own clusters, on [Mistral Compute](https://mistral.ai/news/mistral-compute) (the company's dedicated infrastructure offering), or entirely on-premises within the customer's own data centers. "We have all these different cases, and we support everything," Salamanca said.

## Keeping proprietary data off the cloud is Forge's sharpest selling point

One of the sharpest points of differentiation [Mistral](https://mistral.ai/) is pressing with Forge is data privacy. When customers train on their own infrastructure, Salamanca emphasized that Mistral never sees the data at all.

"It's on their clusters, it's with their data — we don't see anything of it, and so it's completely under their control," she said. "I think this is something that sets us apart from the competition, where you actually need to upload your data, and you have a black box effect."

This matters enormously in sectors like defense, intelligence, financial services, and healthcare, where the legal and reputational risks of exposing proprietary data to a third-party cloud service can be deal-breakers. Mistral has already partnered with organizations including [ASML](https://www.asml.com/en), [DSO National Laboratories Singapore](https://www.dso.org.sg/), the [European Space Agency](https://www.esa.int/), Home Team Science and Technology Agency Singapore, and Reply — a roster that suggests the company is deliberately targeting the most data-sensitive corners of the enterprise market.

Forge also includes data pipeline capabilities that Mistral has developed through its own model training: data acquisition, curation, and synthetic data generation. "Data is a critical piece of any training job today," Salamanca said. "You need to have good data. You need to have a good amount of data to make sure that the model is going to be good performing. We've acquired, as a company, really great knowledge building out these data pipelines."

## In the age of AI agents, Mistral argues that custom models still matter more than MCP servers

The timing of Forge's launch raises an important strategic question. The AI industry in 2026 has been consumed by agents — autonomous AI systems that can use tools, navigate multi-step workflows, and take actions on behalf of users. If the future belongs to agents, why does the underlying model matter? Can't companies simply plug into the best available frontier model through an MCP server or API and focus their energy on orchestration?

Salamanca pushed back on this framing with conviction. "The customers that we've been working on — some of these specific problems are things that no MCP server would ever solve," she said. "You actually need that intelligence. You actually need to create that model that will help you solve your most critical business problem."

She also argued that model customization is essential even in purely agentic architectures. "There are some agentic behaviors that you need to bring to the model," Salamanca said. "It can be about reasoning patterns, specific types of documentation, making sure that you have the right reasoning traces. Even in these cases where people are going completely agentic, you still need model customization — like reinforcement learning techniques — to actually get the right level of performance."

Mistral's [press release](https://mistral.ai/news/forge) makes this connection explicit, arguing that custom models make enterprise agents more reliable by providing deeper understanding of internal environments: more precise tool selection, more dependable multi-step workflows, and decisions that reflect internal policies rather than generic assumptions.

The platform also supports an " [agent-first](https://mistral.ai/news/forge) " design philosophy. Forge exposes interfaces that allow autonomous agents — including Mistral's own Vibe coding agent — to launch training experiments, find optimal hyperparameters, schedule jobs, and generate synthetic data. "We've actually been building Forge in an AI-native way," Salamanca said. "We're already testing out how autonomous agents can actually launch training experiments."

## Mistral Small 4, Leanstral, and the Nvidia coalition: the week that redefined the company's ambitions

To fully appreciate Forge's significance, it helps to view it alongside the other announcements Mistral made in the same week — a barrage of releases that together represent the most ambitious expansion in the company's short history.

Just yesterday, Mistral released [Leanstral](https://mistral.ai/news/leanstral), the first open-source code agent for [Lean 4](https://lean-lang.org/), the proof assistant used in formal mathematics and software verification. Leanstral operates with just 6 billion active parameters and is designed for realistic formal repositories — not isolated math competition problems. On the same day, Mistral launched [Mistral Small 4](https://mistral.ai/news/mistral-small-4), a mixture-of-experts model with 119 billion total parameters but only 6 billion active per query, running 40 percent faster than its predecessor while handling three times more queries per second. Both models ship under the Apache 2.0 license — the most permissive open-source license in wide use.

And then there is the Nvidia [Nemotron Coalition](https://nvidianews.nvidia.com/news/nvidia-launches-nemotron-coalition-of-leading-global-ai-labs-to-advance-open-frontier-models). Announced at Nvidia's GTC conference, the coalition is a first-of-its-kind collaboration between Nvidia and a group of AI labs — including [Mistral](https://mistral.ai/), [Perplexity](https://www.perplexity.ai/), [LangChain](https://www.langchain.com/), [Cursor](https://cursor.com/), [Black Forest Labs](https://bfl.ai/), [Reflection AI](https://reflection.ai/), [Sarvam](https://www.sarvam.ai/), and [Thinking Machines Lab](https://thinkingmachines.ai/) — to co-develop open frontier models. The coalition's first project is a base model co-developed specifically by Mistral AI and Nvidia, trained on Nvidia [DGX Cloud](https://www.nvidia.com/en-us/data-center/dgx-cloud/), which will underpin the upcoming Nvidia Nemotron 4 family of open models.

"Open frontier models are how AI becomes a true platform," said Arthur Mensch, cofounder and CEO of Mistral AI, in Nvidia's announcement. "Together with Nvidia, we will take a leading role in training and advancing frontier models at scale."

This coalition role is strategically significant. It positions Mistral not merely as a consumer of Nvidia's compute infrastructure but as a co-creator of the foundational models that the broader ecosystem will build upon. For a company that is still a fraction of the size of its American competitors, this is an outsized seat at the table.

## Forge takes aim at Amazon, Microsoft, and Google — and says they can't go deep enough

[Forge](https://mistral.ai/products/forge) enters a market that is already crowded — at least on the surface. [Amazon Bedrock](https://aws.amazon.com/bedrock/), Microsoft [Azure AI Foundry](https://azure.microsoft.com/en-us/solutions/ai/), and Google [Cloud Vertex AI](https://cloud.google.com/vertex-ai) all offer model training and customization capabilities. But Salamanca argued that these offerings are fundamentally limited in two respects.

First, they are cloud-only. "In one set of cases, it's very easy to answer — they want to run this on their premises, and so all these tools that are available on the cloud are just not available for them," Salamanca said. Second, she argued that the hyperscalers' training tools largely offer simplified API interfaces that don't provide the depth of control that serious model training requires.

There is also the dependency question. Salamanca described digital-native companies that had built products on top of closed-source models, only to have a new model release — more verbose than its predecessor — crash their production pipelines. "When you're relying on closed-source models, you are also super dependent on the updates of the model that have side effects," she warned.

This argument resonates with the broader sovereignty narrative that has powered Mistral's rise in Europe and beyond. The company has positioned itself as the alternative for organizations that want to own their AI stack rather than lease it from American hyperscalers. Forge extends that argument from inference to training: not just running models you own, but building them in the first place.

The open-source foundation matters here, too. Mistral has been releasing models under permissive licenses since its founding, and Salamanca emphasized that the company is building Forge as an open platform. While it currently works with Mistral's own models, she confirmed that support for other open-source architectures is planned. "We're deeply rooted into open source. This has been part of our DNA since the beginning, and we have been building Forge to be an open platform — it's just a question of a matter of time that we'll be opening this to other open-source models."

## A co-founder's departure to xAI underscores why Mistral is turning expertise into a product

The timing of Forge's launch also arrives against a backdrop of fierce talent competition. As [FinTech Weekly reported](https://www.fintechweekly.com/news/xai-superintelligence-devendra-chaplot-mistral-thinking-machines-lab-grok-march-2026) on March 14, [Devendra Singh Chaplot](https://devendrachaplot.github.io/) — a co-founder of Mistral AI who headed the company's multimodal group and contributed to training Mistral 7B, Mixtral 8x7B, and Mistral Large — left to join Elon Musk's xAI, where he will work on Grok model training. Chaplot had previously also been a founding member of Thinking Machines Lab, the AI startup founded by former OpenAI CTO Mira Murati.

The loss of a co-founder is never insignificant, but Mistral appears to be compensating with institutional capability rather than individual brilliance. Forge is, in essence, a productization of the company's collective training expertise — the recipes, the pipelines, the distributed computing optimizations — in a form that can scale beyond any single researcher. By packaging this knowledge into a platform and pairing it with forward-deployed scientists, Mistral is attempting to build a durable competitive asset that doesn't walk out the door when a key hire departs.

## Mistral's big bet: the companies that own their AI models will be the ones that win

[Forge](https://mistral.ai/products/forge) is a bet on a specific theory of the enterprise AI future: that the most valuable AI systems will be those trained on proprietary knowledge, governed by internal policies, and operated under the organization's direct control. This stands in contrast to the prevailing paradigm of the past two years, in which enterprises have largely consumed AI as a cloud service — powerful but generic, convenient but uncontrolled.

The question is whether enough enterprises will be willing to make the investment. Model training is expensive, technically demanding, and requires sustained organizational commitment. Forge lowers the barriers — through its infrastructure automation, its battle-tested recipes, and its embedded scientists — but it does not eliminate them.

What [Mistral](https://mistral.ai/) appears to be banking on is that the organizations with the most to gain from AI — the ones sitting on decades of proprietary knowledge in highly specialized domains — are precisely the ones for whom generic models are least sufficient. These are the companies where the gap between what a general-purpose model can do and what the business actually needs is widest, and where the competitive advantage of closing that gap is greatest.

[Forge](https://mistral.ai/products/forge) supports both dense and mixture-of-experts architectures, accommodating different trade-offs between performance, cost, and operational constraints. It handles multimodal inputs. It is designed for continuous adaptation rather than one-time training, with built-in evaluation frameworks that let enterprises test models against internal benchmarks before production deployment.

For the past two years, the enterprise AI playbook has been straightforward: pick a model, call an API, ship a feature. Mistral is now asking a harder question — whether the organizations willing to do the difficult, expensive, unglamorous work of training their own models will end up with something the API-callers never get.

An unfair advantage.