---
title: "OSAID FAQs"
source: "https://opensource.org/ai/faq"
author:
published: 2025-01-21
created: 2026-05-01
description: "Answers to Frequently Asked Questions The Open Source AI Definition (OSAID) represents an important first step in defining Open Source in an AI context. Because AI systems differ fundamentally from..."
tags:
  - "clippings"
  - 2
date created: Friday, May 1st 2026, 6:06:36 pm
date modified: Friday, May 1st 2026, 6:21:32 pm
---

## THE open source ai definition 1.0

#### We have released the first stable version of the Definition.

[Read version 1.0](https://opensource.org/ai/open-source-ai-definition)

### Answers to Frequently Asked Questions

[The Open Source AI Definition (OSAID)](https://opensource.org/ai) represents an important first step in defining Open Source in an AI context. Because AI systems differ fundamentally from traditional software, the OSAID seeks to establish the first set of clear, practical guidelines for development, use and modification of AI systems in keeping with the Open Source ethos. Unfortunately, misconceptions about the definition persist, often stemming from a lack of understanding of the nature of AI. This post aims to clarify key points and provide a forward-looking perspective on the importance of the OSAID.

## FAQs

## What Is an AI System?

According to the OSAID, an AI system aligns with the definition provided by the Organisation for Economic Co-operation and Development (OECD):

> An AI system is a machine-based system that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments. Different AI systems vary in their levels of autonomy and adaptiveness after deployment.

In simple terms, an AI system is “the thing” that processes input to produce output, whether that’s a prediction, recommendation, or another result. Anchoring discussions in such common definitions is essential because AI systems differ radically from traditional software.

## What is an Open Source AI?

An Open Source AI is an AI system made freely available with all necessary code, data and parameters under legal terms approved by the Open Source Initiative. For more details, read below.

## Why did you write the Open Source AI Definition?

Point 2 of the [Open Source Definition (OSD)](https://opensource.org/osd) says ***“The program must include source code \[…\] The source code must be the preferred form in which a programmer would modify the program \[…\]”***. When we embarked on this initiative, nobody had a clear answer to the question, “What is the preferred form to modify an AI system?” So OSI offered to find the answer along with the broader community by engaging in a [co-design process](https://opensource.org/deepdive/).

## What’s the difference between the Open Source Definition and the Open Source AI Definition?

The [Open Source Definition (OSD)](https://opensource.org/osd) refers to software programs. AI and specifically machine learning systems are not simply software programs; they blend boundaries with data, configuration options, documentation and new artifacts, like weights and biases. The *Open Source AI Definition* describes the preferred form to modify an AI system, providing clarity on interpreting the principles of the OSD in the domain of AI.

## Isn’t training data required to program the AI system?

A frequent misunderstanding about AI systems is equating training data with source code, suggesting that “training data is how the model gets programmed.” Unlike traditional software, AI systems are not programmed in the conventional sense. Instead, they acquire capabilities autonomously during the training process — a phenomenon distinguishing them from software like the Linux kernel.

For example, the Linux kernel is:

- Programmed by humans.
- Composed of source code that developers can read, study, and modify.
- Reproducible, meaning its binary form can be reliably rebuilt from its source code.

In contrast, modern AI systems such as large language models develop their behavior in ways that are often unpredictable and inexplicable. Training processes are challenging to replicate reliably, even by the system’s creators. These differences necessitated the establishment of a unique definition beyond the Open Source Definition for software.

## What is the role of training data in the Open Source AI Definition?

Open Source means giving anyone the ability to meaningfully fork (study and modify) your system without requiring additional permissions to make it more useful for themselves and everyone else. This is why point 2 of the OSD requires that the source code be provided in the preferred form for making modifications. This way, everyone has the same rights and ability to fork as the original developers, starting a virtuous innovation cycle.

However, training data does not equate to a software source code. Training data is important for studying modern machine learning systems. However, it is not what AI researchers and practitioners necessarily use as part of the preferred form for modifying a trained model.

The Data Information and Code requirements of the OSAID allow Open Source AI systems to be forked by third-party AI builders downstream using the same information as the original developers. These forks could include removing nonpublic or non-open data from the training dataset in order to train a new Open Source AI system on fully public or open data.

## Why do you allow the exclusion of some training data?

We want Open Source AI to exist in fields where data cannot be legally shared, such as medical AI. Laws that permit training on data often limit the resharing of that same data to protect copyright or other interests. Privacy rules also give people the right to control their most sensitive information, like decisions about their health. Similarly, much of the world’s Indigenous knowledge is protected through mechanisms that are not compatible with later-developed frameworks for rights exclusivity and sharing.

There are also many cases where terms of use of publicly available data may give entity A the confidence that they may use it freely and call it “open data,” but not give entity A the confidence they can, in turn, give entity B the same guarantees for use in a different jurisdiction. Meanwhile, entity B may not feel confident using that data in their own jurisdiction. An example is so-called public domain data, where the definition of public domain varies from country to country. Another example is fair-use or private data, where the finding of fair use or privacy laws may require a good knowledge of the law of a given jurisdiction. This resharing is not so much *limited* as [lacking legal certainty](https://opensource.org/blog/copyright-law-makes-a-case-for-requiring-data-information-rather-than-open-datasets-for-open-source-ai).

## How did you arrive at this conclusion? Is it compromising Open Source ideals?

During our co-design process, relationships between the weights and the data drove the highest community engagement. In the [“System analysis” phase](https://discuss.opensource.org/t/report-on-working-group-recommendations/247), the volunteer groups suggested that training and data processing codes were more important for modifying the AI system than accessing the training and testing data. That result was validated in the [“Validation phase”](https://discuss.opensource.org/t/initial-report-on-definition-validation/368) and suggested a path that allows Open Source AI to exist on equal grounds with proprietary systems: both can train on the same kind of data.

Some people believe that full, unfettered access to all training data (with no distinction of its kind) is paramount, arguing that anything less would compromise the full reproducibility of AI systems, transparency and security. This approach would relegate Open Source AI to a niche of AI trainable only on open data. That niche would be tiny, even relative to the niche occupied by Open Source in the traditional software ecosystem. The requirements of Data Information keep the same approach present in the Open Source Definition; it doesn’t mandate full reproducibility and transparency but enables them (i.e., [reproducible builds](https://reproducible-builds.org/)). At the same time, setting a baseline requiring Data Information doesn’t preclude others from formulating and demanding more requirements, like the [Digital Public Goods Standard](https://digitalpublicgoods.net/standard/) or the [Free Systems Distribution Guidelines](https://www.gnu.org/distros/free-system-distribution-guidelines.html), which add requirements to the Open Source Definition.

One of the key aspects of OSI’s mission is to drive and promote Open Source innovation. The approach OSI takes here enables complete user choice with Open Source AI. Users can keep the insights derived from training+data preprocessing code and a description of unshareable training data and build upon those with their own unshareable data and give the insights derived from further training to everyone, allowing for Open Source AI in areas like health care. Alternatively, users can obtain the available and public data from the Data Information and retrain their model without any unshareable data, resulting in more data transparency in the AI system. Like copyleft and permissive licensing, this approach leaves the choice with the user.

## What kind of data should be required in the Open Source AI Definition?

A significant challenge in AI is the role of data. Unlike traditional software, where source code is the primary artifact, AI systems depend heavily on data — not just any data, but data processed and curated into training datasets. The OSAID recognizes the legal and ethical complexities of data sharing and uses precise legal terms to outline expectations. While not all raw data can be freely distributed, the Definition ensures that the essential elements for modifying an AI system are accessible.

There are four classes of data, based on their legal constraints, all of which can be used to train Open Source AI systems:

- Open training data: data that can be copied, preserved, modified and reshared. It provides the best way to enable users to study the system. This must be shared.
- Public training data: data that others can inspect as long as it remains available. This also enables users to study the work. However, this data can degrade as links or references are lost or removed from network availability. To obviate this, different communities will have to work together to define standards, procedures, tools and governance models to overcome this risk, and Data Information is required in case the data becomes later unavailable. This must be disclosed with full details on where to obtain it.
- Obtainable training data is data that can be obtained, including for a fee. This information provides transparency and is similar to a purchasable component in an open hardware system. The Data Information provides a means of understanding this data other than obtaining or purchasing it. This area is likely to change rapidly and will need careful monitoring to protect Open Source AI developers. It must be disclosed with full details on where to obtain it.
- Unshareable nonpublic training data: data that cannot be shared for explainable reasons, like Personally Identifiable Information (PII). For this class of data, the ability to study some of the system’s biases demands a detailed description of the data – what it is, how it was collected, its characteristics, and so on – so that users can understand the biases and categorization underlying the system. This must be revealed in detail so that, for example, a hospital can create a dataset with identical structure using its own patient data.

OSI believes that all these classes of data can be part of the preferred form of making modifications to the AI system. This approach both advances openness in all the components of the AI system and drives more Open Source AI, including private-first areas such as health care.

## How do you fix a buggy AI system?

A core question the OSAID addresses is: *How do you fix a buggy AI system?* For traditional software, the [Open Source Definition](https://opensource.org/osd) provides a clear answer:

The program must include source code, and must allow distribution in source code as well as compiled form. The source code must be the preferred form in which a programmer would modify the program.

However, modifying an AI system requires more than just source code. After extensive consultation with AI developers, researchers and practitioners, the community, through the OSAID co-design process, concluded that the preferred form for modifying an AI system includes:

1. **The software used to create the dataset** (i.e., to transform raw data into tokens).
2. **The software used to train the system.**
3. **The results of the training** (i.e., the parameters).
4. **All legally shareable data** used in the training process.

These components collectively enable the study, use, modification and sharing of AI systems in a manner consistent with Open Source principles.

## What is a skilled person?

In legal circles, Skilled Person means any person having the current knowledge, experience and competence to perform a certain duty. This [Wikipedia entry](https://en.wikipedia.org/wiki/Person_having_ordinary_skill_in_the_art) provides more details.

## Is the Open Source AI Definition covering models and weights and parameters?

Yes. The Open Source AI Definition makes no distinction between what might be called AI system, model, or weights and parameters. Whether the offering is characterized as an AI system, a model, or weights and parameters, to be called Open Source AI, the requirements for providing the preferred form for making modifications will be the same.

If you are interested in learning more about Open Weights, please read [this article.](https://opensource.org/ai/open-weights)

## Why do you require training code while OSD 2 doesn’t require compilers?

AI and software are radically different domains, and drawing comparisons between them is rarely productive. OSD point 2 doesn’t mandate that Open Source software uses only compilers released with an OSI-Approved License because compilers are standardized, de jure (like ANSI C) or de facto like TurboPascal or Python. It was generally accepted that to develop more Open Source software one could use a proprietary development environment. For machine learning, the training code is not standardized, and therefore it must be part of the preferred form of making modifications to preserve the right to fork an AI system.

## Why is there no mention of safety and risk limitations in the Open Source AI Definition?

The Open Source AI Definition does not specifically guide or enforce ethical, trustworthy, or responsible AI development practices. However, it does not put up any barriers that would prevent developers from adhering to such principles if they chose to. The efforts to discuss the responsible development, deployment and use of AI systems, including through appropriate government regulation, are a separate conversation. A good starting point is OECD’s Recommendation of the Council on Artificial Intelligence, [Section 1: Principles for responsible stewardship of trustworthy AI](https://legalinstruments.oecd.org/en/instruments/oecd-legal-0449).

## Are model parameters copyrightable?

The Open Source AI Definition does not take a stance on the legal nature of Parameters. They may be free by nature, or a license or other legal instrument may be required to ensure their freedom. Whether model parameters are copyrightable will become clearer over time as the legal system has more opportunities to address this issue. In any case, we require an explicit assertion accompanying the distribution of Parameters that assures that they are freely available to all.

## Why will parameters be available under “OSI-approved terms” but the code will be under “OSI-approved licenses”? Are you going to allow restrictions on the terms for models?

We used the word “terms” instead of “license” for models because, as mentioned above, we do not yet know what the legal mechanism will be to assure that the models are available to use, study, modify and share. We used “terms” to avoid suggesting that a “license” is the only legal mechanism that could be used. That said, to be approved by the OSI, the terms for parameters must assure the freedom to use, study, modify and share.

## Why is the “Preferred form to make modifications” limited to machine learning?

The principles stated in the Open Source AI Definition are generally applicable to any kind of AI, but machine learning challenges the Open Source Definition. For machine learning, a set of artifacts (components) is required to study and modify the system, thus requiring a new explanation of what is necessary to study and modify the system.

## Which AI systems comply with the Open Source AI Definition?

As part of our validation and testing of the OSAID, the volunteers checked whether the Definition could be used to evaluate if AI systems provided the freedoms expected. The list of models that passed the Validation phase are: Pythia (Eleuther AI), OLMo (AI2), Amber and CrystalCoder (LLM360), and T5 (Google). A few others that were analyzed would probably pass if they changed their licenses/legal terms, for example, BLOOM (BigScience), Starcoder2 (BigCode), and Falcon (TII). Those that have been analyzed and don’t pass because they lack required components and/or their legal agreements are incompatible with the Open Source principles include Llama2 (Meta), Grok (X/Twitter), Phi-2 (Microsoft), and Mixtral (Mistral). These results should be seen as part of the definitional process, a learning moment; they are not certifications of any kind. OSI will continue to validate only legal documents and will not validate or review individual AI systems, just as it does not validate or review software projects.

## What’s the next step?

The Open Source AI Definition reflects a thoughtful and inclusive process endorsed by leading AI developers, researchers and practitioners. It culminates in a first step represented in version 1.0 of the OSAID. The definition acknowledges that AI fundamentally differs from software and requires a tailored approach. Misunderstandings about the OSAID often arise from attempts to apply software engineering paradigms to AI, leading to confusion. By embracing the unique characteristics of AI systems, the OSAID offers a robust framework for fostering transparency, innovation and collaboration in AI development.

As we navigate AI’s evolving landscape, it is crucial to engage thoughtfully and constructively with these definitions. By doing so, we can ensure that AI systems remain open, accessible and aligned with the principles of the broader Open Source movement.

---

Our work is only possible thanks to our members. [Join us today!](https://join.opensource.org/join)