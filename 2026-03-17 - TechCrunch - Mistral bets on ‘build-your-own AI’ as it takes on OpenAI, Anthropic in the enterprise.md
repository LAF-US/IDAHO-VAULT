---
source: "https://techcrunch.com/2026/03/17/mistral-forge-nvidia-gtc-build-your-own-ai-enterprise/"
author:
  - "[[Anna Heim]]"
published: 2026-03-17
created: 2026-04-17
---
Most enterprise AI projects fail not because companies lack the technology, but because the models they’re using don’t understand their business. The models are often trained on the internet, rather than decades of internal documents, workflows, and institutional knowledge.

That gap is where [Mistral](https://techcrunch.com/2025/09/09/what-is-mistral-ai-everything-to-know-about-the-openai-competitor/), the French AI startup, sees opportunity. On Tuesday, the company announced Mistral Forge, a platform that lets enterprises build custom models trained on their own data. Mistral announced the platform at [Nvidia GTC](https://techcrunch.com/2026/03/16/nvidia-gtc-how-to-watch-jensen-huang-2026-keynote/), Nvidia’s annual technology conference, which this year is focused heavily on AI and agentic models for enterprise.

It’s a pointed move for Mistral, a company that has built its business on corporate clients while rivals OpenAI and Anthropic have soared ahead in terms of consumer adoption. CEO Arthur Mensch says Mistral’s laser focus on the enterprise is working: The company is on track to [surpass $1 billion in annual recurring revenue](https://www.ft.com/content/664249e7-e8d5-4425-b397-ad3ed590b305) this year.

A big part of doubling down on enterprise is giving companies more control over their data and their AI systems, Mistral says.

“What Forge does is it lets enterprises and governments customize AI models for their specific needs,” Elisa Salamanca, Mistral’s head of product, told TechCrunch.

Several companies in the enterprise AI space already claim to offer similar capabilities, but most focus on fine-tuning existing models or layering proprietary data on top through techniques like retrieval augmented generation ([RAG](https://techcrunch.com/2024/05/04/why-rag-wont-solve-generative-ais-hallucination-problem/)). These approaches don’t fundamentally retrain models; instead, they adapt or query them at runtime using company data.

Mistral, by contrast, says it is enabling companies to train models from scratch. In theory, this could address some of the limitations of more common approaches — for example, better handling of non-English or highly domain-specific data, and greater control over model behavior. It could also allow companies to train agentic systems using reinforcement learning and reduce reliance on third-party model providers, avoiding risks like model changes or deprecation.

Forge customers can build their custom models using Mistral’s wide library of open-weight AI models, which includes small models such as the recently introduced [Mistral Small 4](https://mistral.ai/news/mistral-small-4). According to Mistral co-founder and chief technologist, Timothée Lacroix, Forge can help unlock more value out of its existing models.

“The trade-offs that we make when we build smaller models is that they just cannot be as good on every topic as their larger counterparts, and so the ability to customize them lets us pick what we emphasize and what we drop,” Lacroix said.

Mistral advises on which models and infrastructure to use, but both decisions stay with the customer, Lacroix said. And for teams that need more than guidance, Forge comes with [Mistral’s team of forward-deployed engineers](https://www.bloomberg.com/news/newsletters/2026-03-03/europe-s-ai-darling-mistral-looks-more-like-a-consultant-than-a-model-maker) who embed directly with customers to surface the right data and adapt to their needs — a model borrowed from the likes of IBM and Palantir.

“As a product, Forge already comes with all the tooling and infrastructure so you can generate synthetic data pipelines,” Salamanca said. “But understanding how to build the right [evals](https://www.thoughtworks.com/insights/decoder/a/ai-evals) and making sure that you have the right amount of data is something that enterprises usually don’t have the right expertise for, and that’s what the FDEs bring to the table.”

Mistral has already made Forge available to partners, including Ericsson, the European Space Agency, Italian consulting company Reply, and Singapore’s DSO and HTX. Early adopters also include ASML, the Dutch chipmaker that led [Mistral’s Series C](https://mistral.ai/news/mistral-ai-raises-1-7-b-to-accelerate-technological-progress-with-ai) round last September at a €11.7 billion valuation (approximately $13.8 billion at the time).

These partnerships are emblematic of what Mistral expects Forge’s main use cases to be. According to Mistral’s chief revenue officer Marjorie Janiewicz, these include governments who need to tailor models for their language and culture; financial players with high compliance requirements; manufacturers with customization needs; and tech companies that need to tune models to their code base.