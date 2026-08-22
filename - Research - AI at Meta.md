---
title: "Research - AI at Meta"
source: "https://ai.meta.com/research/publications/hyperagents/"
author:
published:
created: 2026-06-11
description: "Self-improving AI systems aim to reduce reliance on human engineering by learning to improve their own learning and problem-solving processes. Existing..."
date created: Thursday, June 11th 2026, 6:01:38 pm
date modified: Sunday, June 14th 2026, 12:45:48 pm
---

## Abstract

Self-improving AI systems aim to reduce reliance on human engineering by learning to improve their own learning and problem-solving processes. Existing approaches to recursive self-improvement typically rely on fixed, handcrafted meta-level mechanisms, which fundamentally limit how fast such systems can improve. The Darwin Gödel Machine (DGM)(Zhang et al., 2025b) demonstrates that open-ended self-improvement is achievable in coding. Starting from a single coding agent, the DGM repeatedly generates and evaluates self-modified variants, forming a growing archive of stepping stones for future improvement. Because both evaluation and self-modification are coding tasks, gains in coding ability can translate into gains in self-improvement ability. However, this alignment does not generally hold beyond coding domains. We introduce hyperagents, self-referential agents that integrate a task agent (which solves the target task) and a meta agent (which modifies itself and the task agent) into a single editable program. Crucially, the meta-level modification procedure is itself editable, enabling metacognitive self-modification, improving not only task-solving behavior, but also the mechanism that generates future improvements. We instantiate this framework by extending DGM to create DGM-Hyperagents (DGM-H). By allowing the improvement procedure to evolve, the DGM-H eliminates the assumption of domain-specific alignment between task performance and self-modification skill, and can potentially support self-accelerating progress on any computable task. Across diverse domains (coding, paper review, robotics reward design, and Olympiad-level math-solution grading), the DGM-H improves performance over time and outperforms baselines without self-improvement or open-ended exploration, as well as prior self-improving systems like DGM. We further show that the DGM-H improves the process by which it generates new agents (e.g., persistent memory, performance tracking), and that these meta-level improvements transfer across domains and accumulate across runs. All experiments were conducted with safety precautions (e.g., sandboxing, human oversight). We discuss what safety entails in this setting and the broader implications of self-improving systems. DGM-Hyperagents offer a glimpse of open-ended AI systems that do not merely search for better solutions, but continually improve their search for how to improve.

[

Download the Paper

](<https://scontent.fboi1-1.fna.fbcdn.net/v/t39.2365-6/651318792_1484042123139269_5924122875180468134_n.pdf?_nc_cat=104&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=9ErskVYvXHsQ7kNvwHFU3yj&_nc_oc=AdqzhNqIu9D5OmWDG99TjsIbCC53kZmTNQBnlu-jIlpZA55onesTGk3oT-BRt0ta8WE&_nc_zt=14&_nc_ht=scontent.fboi1-1.fna&_nc_gid=GNUVnO1vhaeiDTDueTaN5A&_nc_ss=7b289&oh=00_Af8mkmZx7-4Y4d8EQKKgwsBlr7PAdZRKaNwatJrzJtP7Lw&oe=6A31271A>)

### Related Publications

June 05, 2026

#### CONVERSATIONAL AI

#### RANKING AND RECOMMENDATIONS

#### Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval

Retrieval-augmented agents are increasingly the interface to large organizational and public knowledge bases, yet most still treat retrieval as a black box: they issue exploratory queries, inspect returned snippets, and iteratively reformulate until useful evidence emerges. This resembles how a newcomer searches an unfamiliar database rather than how an expert navigates it with strong priors about terminology, constraints, and likely evidence, leading to unnecessary retrieval rounds, increased latency, and poor recall. We introduce Superintelligent Retrieval Agent (SIRA), which defines superintelligence in retrieval as the ability to compress multi-round exploratory search into a single corpus-discriminative retrieval action. SIRA does not merely ask what terms are relevant to the query; it asks which terms are likely to separate the desired evidence from corpus-level confusers. On the corpus side, an LLM enriches each document offline with missing search vocabulary; on the query side, it predicts evidence vocabulary omitted by the query; and corpus statistics are used as tool calls to filter proposed terms that are absent, overly common, or unlikely to create retrieval margin. The final retrieval step is a single weighted BM25 call combining the original query with the validated expansion. Across ten BEIR benchmarks, SIRA achieves the strongest average retrieval performance in our comparison, outperforming dense retrievers, learned sparse retrievers, and LLM-based search-agent baselines while using no relevance labels or retriever fine-tuning. On downstream question answering, SIRA's retrieval-only answer coverage exceeds recent RL-trained agentic QA systems on NQ and HotpotQA. Finally, we introduce BrowseComp-Wikipedia, a hard-search benchmark of 232 BrowseComp-derived queries grounded in a 25,587,229-document English Wikipedia index. Even without index-time LLM document enrichment, using only grounded Wikipedia categories as corpus-visible structure, SIRA outperforms multi-round Perplexity agents at every retrieval budget, reaching 9.70% Recall@1, 15.27% Recall@10, and 36.14% Recall@100. These results show that one well-formed, corpus-grounded lexical retrieval action can outperform substantially more expensive multi-round search while remaining interpretable, training-free, and efficient.

Anshumali Shrivastava, Jason Chen, Qi Ma, Zeyu Yang

June 05, 2026

[Read the Paper](https://ai.meta.com/research/publications/superintelligent-retrieval-agent-the-next-frontier-of-agentic-retrieval/)

May 27, 2026

#### OPEN SOURCE

#### AutoformBot: Formalizing Mathematics at Scale

We present AutoformBot, a multi-agent system for building an Autoformalized Textbook Library At Scale (Atlas) in Lean 4. AutoformBot orchestrates thousands of LLM agents, equipped with formal verification tools, dependency-aware task scheduling, and collaborative version control, to translate informal textbook prose into machine-checked definitions and proofs. We apply our methods to a corpus of 26 open-access textbooks spanning analysis, algebra, topology, combinatorics, and probability, producing Atlas: a verified library of over 45,000 Lean4 declarations and 500 thousand lines of code. We release two artifacts: (i) AutoformBot, the open-source multi-agent framework; and (ii) Atlas, the resulting formal library. Our results suggest that autoformalizing the core content of graduate-level mathematics at scale is now economically and technically feasible. This opens the door to the automated verification of both human- and machine-generated mathematics at a research level.

Amaury Hayat, Ahmad Rammal, Charles Arnal, Julia Kempe, Niket Patel, Remi Munos, [Vivien Cabannes](https://ai.meta.com/people/846420800625852/vivien-cabannes/)

May 27, 2026

[Read the Paper](https://ai.meta.com/research/publications/autoformbot-formalizing-mathematics-at-scale/)

May 20, 2026

#### HUMAN & MACHINE INTELLIGENCE

#### RESEARCH

#### EgoBabyVLM: Benchmarking Cross-Modal Learning from Naturalistic Egocentric Video Data

Children acquire language grounding with remarkable robustness from limited visuo-linguistic input in ways that surpass today's best large multimodal models. Recent research suggests current vision-language models (VLMs) trained on curated web data fail to generalize to the sparse, weakly-aligned egocentric streams produced by wearable devices, embodied agents, and infant head-cams -- and no fixed evaluation pipeline exists for measuring progress on this regime. We train VLMs on datasets with varying degrees of semantic alignment between visual and linguistic inputs, including naturalistic infant and adult egocentric videos, and evaluate them with a comprehensive suite spanning multimodal language grounding and unimodal vision and language tasks. At the core of this suite is Machine-DevBench, a corpus-grounded benchmark of lexical and grammatical competence, automatically generated from the model's training vocabulary across logarithmic frequency bins to eliminate the train/eval mismatch and low statistical power of prior developmental benchmarks. Our results show that current VLM paradigms hinge on the tight semantic alignment of curated data and fail to exploit the weakly-aligned signal that dominates naturalistic egocentric input -- the very regime in which humans thrive. To motivate progress, we introduce the EgoBabyVLM Challenge to drive the development of models capable of grounded language learning from the kind of naturalistic data that human infants experience.

Alvin W. M. Tan, Nicolas Hamilakis, Manel Khentout, Sho Tsuji, Balázs Kégl, Michael C. Frank, Angel Villar Corrales, Charles-Eric Saint-James, [Dongyan Lin](https://ai.meta.com/people/2023351861723323/dongyan-lin/), Emmanuel Dupoux, Jiayi Shen, [Juan Pino](https://ai.meta.com/people/776668760684735/juan-pino/), Mahi Luthra, Martin Gleize, Phillip Rust, Rashel Moritz, Sheila Krogh-Jespersen, Surya Parimi, Tom Fizycki, Vanessa Stark, Yosuke Higuchi, Youssef Benchekroun

May 20, 2026

[Read the Paper](https://ai.meta.com/research/publications/egobabyvlm-benchmarking-cross-modal-learning-from-naturalistic-egocentric-video-data/)

May 18, 2026

#### CONVERSATIONAL AI

#### RESEARCH

#### GIM: Evaluating models via tasks that integrate multiple cognitive domains

As LLM benchmarks saturate, the evaluation community has pursued two strategies to increase difficulty: escalating knowledge demands (GPQA, HLE) or removing knowledge entirely in favor of abstract reasoning (ARC-AGI). The first conflates memorization with capability; the second divorces reasoning from the practical contexts in which it matters. We take a different approach. The Grounded Integration Measure (GIM) is a benchmark of 820 original problems (615 public, 205 private) where difficulty comes from integration; individual problems require coordinating multiple cognitive operations (constraint satisfaction, state tracking, epistemic vigilance, audience calibration) over broadly accessible knowledge, so that reasoning stays grounded in realistic tasks without being gated on specialized expertise. Each problem is an original expert-authored composition, majority with rubric-decomposed scoring (median 6 independently judged criteria). A balanced public–private split provides built-in contamination diagnostic. We calibrate a continuous response 2-parameter logistic (2PL) IRT model over >200k prompt-response pairs across 28 models, producing robust ability estimates that correctly order test-configurations even when raw accuracy is distorted by errors or missing data, addressing a common challenge in benchmark reporting. Using this framework, we present a comprehensive leaderboard spanning 22 models and 47 test-configurations (unique model × thinking-level pairs), and conduct what is to our knowledge the most extensive published study of how test-time compute trades off against model capability on a fixed benchmark: 11 models swept across 35 test-configurations. We observe that within-family configuration choices, such as thinking budget and quantization, matter as much as model selection, and increasing thinking tokens has diminishing marginal returns. We release the evaluation framework, calibrated IRT parameters, and all public problems.

Alexandre Rezende, Rohit Patel, Steven McClain

May 18, 2026

[Read the Paper](https://ai.meta.com/research/publications/gim-evaluating-models-via-tasks-that-integrate-multiple-cognitive-domains/)
