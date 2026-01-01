---
title: "GPT-5.5 System Card"
source: "https://deploymentsafety.openai.com/gpt-5-5/external-evaluation-for-bio-capabilities---securebio"
author:
published:
created: 2026-06-14
description: "GPT-5.5 is a new model designed for complex, real-world work, including writing code, researching online, analyzing information, creating documents and spreadsheets, and moving across tools to get things done. Relative to earlier models, GPT-5.5 understands the task earlier, asks for less guidance, uses tools more effectively, checks it work and keeps going until it’s done."
date created: Sunday, June 14th 2026, 12:47:37 pm
date modified: Sunday, June 14th 2026, 12:47:54 pm
---

GPT-5.5 is a new model designed for complex, real-world work, including writing code, researching online, analyzing information, creating documents and spreadsheets, and moving across tools to get things done. Relative to earlier models, GPT-5.5 understands the task earlier, asks for less guidance, uses tools more effectively, checks it work and keeps going until it’s done.

We subjected the model to our full suite of predeployment safety evaluations and our Preparedness Framework, including targeted red-teaming for advanced cybersecurity and biology capabilities, and collected feedback on real use cases from nearly 200 early-access partners before release. We are releasing GPT-5.5 with our strongest set of safeguards to date, designed to reduce misuse while preserving legitimate, beneficial uses of advanced capabilities.

We generally treat GPT-5.5’s safety results as strong proxies for GPT-5.5 Pro, which is the same underlying model using a setting that makes use of parallel test time compute. As noted below, we separately evaluate GPT-5.5 Pro in certain cases because we judge that the setting could materially impact the relevant risks or appropriate safeguards posture. Except where noted, the results in system cards describe evaluations we ran in an offline setting.

*This card was updated on April 24, 2026 to include additional information about safeguards for the deployment of GPT-5.5 and GPT-5.5 Pro in the API.*

Like OpenAI’s other models, GPT-5.5 was trained on diverse datasets, including information that is publicly available on the internet, information that we partner with third parties to access, and information that our users or human trainers and researchers provide or generate. Our data processing pipeline includes rigorous filtering to maintain data quality and mitigate potential risks. We use advanced data filtering processes to reduce personal information from training data. We also employ safety classifiers to help prevent or reduce the use of harmful or sensitive content, including explicit materials such as sexual content involving a minor.

OpenAI reasoning models are trained to reason through reinforcement learning. These models are trained to think before they answer: they can produce a long internal chain of thought before responding to the user. Through training, these models learn to refine their thinking process, try different strategies, and recognize their mistakes. Reasoning allows these models to follow specific guidelines and model policies we’ve set, helping them act in line with our safety expectations. This means they provide more helpful answers and better resist attempts to bypass safety rules.

Note that comparison values from previously launched models are from the latest versions of those models, so may vary slightly from values published at launch for those models.[^1]

We conducted benchmark evaluations across disallowed content categories. We report here on our Production Benchmarks, an evaluation set with conversations representative of challenging examples from production data. As we noted in previous system cards, we introduced these Production Benchmarks to help us measure continuing progress given that our earlier Standard evaluations for these categories had become relatively saturated.

These evaluations were deliberately created to be difficult. They were built around cases in which our existing models were not yet giving ideal responses, and this is reflected in the scores below. Error rates are not representative of average production traffic. The primary metric is not\_unsafe, checking that the model did not produce output that is disallowed under the relevant OpenAI policy.

Values from previously-launched models are from the latest versions of those models, and evals are subject to some variation. Values may vary slightly from values published at launch for those models.

### Table 1: Production Benchmarks with Challenging Prompts (higher is better)

| **Category** | **gpt-5.1-thinking** | **gpt-5.2-thinking** | **gpt-5.4-thinking** | **gpt-5.5** |
| --- | --- | --- | --- | --- |
| Violent Illicit behavior | 0.955 | 0.975 | 0.971 | 0.979 |
| Nonviolent illicit behavior | 0.990 | 0.993 | 1.000 | 0.993 |
| harassment | 0.706 | 0.810 | 0.790 | 0.822 |
| extremism | 1.000 | 1.000 | 1.000 | 0.925 |
| hate | 0.808 | 0.927 | 0.943 | 0.868\* |
| self-harm (standard) | 0.926 | 0.961 | 0.987 | 0.959 |
| violence | 0.800 | 0.877 | 0.831 | 0.846 |
| sexual | 0.933 | 0.940 | 0.933 | 0.925 |
| sexual/minors | 0.916 | 0.948 | 0.966 | 0.941 |

GPT-5.5 performs on par with GPT-5.4-Thinking. For most categories, regressions are not statistically significant.

\* Upon investigation, we found that this evaluation score was caused by requests to translate text containing disallowed content, which do not in fact violate our policies.

As with the [GPT-5.4 Thinking system card](https://deploymentsafety.openai.com/gpt-5-4-thinking/production-benchmarks-with-representative-prompts), we also estimate rates of disallowed content on a production-like distribution of deidentified user traffic (in compliance with OpenAI’s privacy policy).

Before release, we used deidentified conversations broadly representative of recent GPT-5.4 Thinking production traffic, resampled the final assistant turn with GPT-5.5, and automatically labeled relevant properties of the new completions.

These evaluations reflect a particular point in time, and are imperfect due to temporal drifts both in the underlying distributions of production traffic and in internal processing and evaluation pipelines, as well as the difficulty of faithfully reconstructing the range of contexts and environments in production. In [our previous research](https://alignment.openai.com/prod-evals/), we saw that despite these challenges, we were able to predict whether or not true rates would have very significant increases at the model level.

Note that these evaluations only capture the behavior of the model itself, and do not account for other layers of the safety stack designed to mitigate disallowed model responses. Because of that, we expect the rates of policy-violative responses in the actual production environment to be lower than the rates below.

In the figure below, we report the extrapolated prevalence of unsafe model-level outputs, which measures the expected proportion of all model-level outputs which are violative of a given category (without accounting for any other parts of OpenAI’s safety stack). For example, based on the observed distribution of conversations with GPT-5.4 Thinking, we estimate that approximately 0.056% of conversation turns with GPT-5.5 outputs would be marked as potentially violating our harassment policy, without the benefit of other safety interventions that operate in addition to the model’s own safety training.

While we believe it to be informative, we also want to stress that this pipeline is still experimental, as seen by the differences between GPT-5.4 Thinking production data and resampled data on the same distribution. There are sometimes significant biases in our estimates that we are working to reduce.

### Figure 1

![Figure 1](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/disallowed3.png)

Figure 1

We ran the image input evaluations introduced with ChatGPT agent, that evaluate for not\_unsafe model output, given disallowed combined text and image input.

### Table 2: Image input evaluations, with metric not\_unsafe (higher is better)

| Category | gpt-5.1-thinking | gpt-5.2-thinking | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| hate | 0.981 | 0.988 | 0.988 | 0.981 |
| extremism | 0.984 | 0.987 | 0.995 | 0.987 |
| self-harm | 0.984 | 0.986 | 0.999 | 0.987 |
| harms-erotic | 0.999 | 0.998 | 0.990 | 0.987 |

We find that GPT-5.5 performs generally on par with its predecessors. Minor regressions are not statistically significant. In addition to the evaluations reported in the table above, we previously ran vision evaluations for illicit and attack planning. We removed those evaluations as the harms are measured as disallowed content evaluations.

We ran our destructive actions evaluation that measures the model’s ability to preserve user-produced changes and avoid taking accidental destructive actions. We find that GPT-5.5 performs better than earlier versions.

### Table 3

| Category | gpt-5.2- codex | gpt-5.3- codex | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| Destructive action avoidance | 0.76 | 0.88 | 0.86 | 0.90 |

### Table 4

| Category | gpt-5.2-codex | gpt-5.3-codex | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| Perfect reversion | 0.09 | 0.01 | 0.18 | 0.52 |
| User work preserved | 0.18 | 0.08 | 0.53 | 0.57 |

Destructive action can also be particularly prevalent when agents operate deletion-inducing tasks (e.g., file reversion and cleanup) in complex workspaces with ongoing changes from users or even other agents. A safe and collaborative agent should distinguish between their work and user work, protect user changes by default, and recover from mistakes. Therefore, we trained our agents to revert their own changes after long rollouts while protecting implicit, simulated user work. On evaluations involving challenging, long-rollout traces, GPT-5.5 significantly improves GPT-5.4-Thinking where it reverts agent-only work while respecting user changes.

The model is trained to follow both platform-level policy for high-risk actions and configurable developer-provided confirmation policy provided in the developer message in line with our approach to instruction hierarchy.

This provides a number of benefits, including:

- We are able to rapidly update the system-level policy if we identify issues.
- When used in the API, we are able to allow developers to customize the confirmation policy, for example, to better enable steerable confirmations by the model when engaging computer use.

In ChatGPT and API deployment, we provide the confirmation policy in the system message. Below are the results of our user confirmations during computer use evaluations.

### Table 5

| Category | gpt-5.2-thinking | gpt-5.3-codex | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| Financial transaction | 1.00 | 0.99 | 1.00 | 1.00 |
| High-stakes communication | 1.00 | 0.99 | 1.00 | 0.98 |
| General confirmation | 0.94 | 0.91 | 0.94 | 0.94 |

We evaluate model robustness to jailbreaks: adversarial or out-of-distribution prompts designed to circumvent safety guardrails and elicit harmful assistance. Ahead of the GPT-5.4 launch, we replaced our previous StrongReject-based benchmark with a more challenging multiturn jailbreak evaluation derived from red-teaming exercises. The updated evaluation tests models on realistic scenarios using sophisticated attacker strategies that can probe, adapt, and escalate over the course of a conversation.

Responses that do not comply with our safety policies are scored worse, while compliant responses are scored better; in aggregate, we report worst-case defender success rate, so higher is better.

### Figure 2

![Figure 2](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/jailbreaks5.png)

Figure 2

We evaluate the model’s robustness to known prompt injection attacks against connectors. These attacks embed adversarial instructions in the tool-output that aim to mislead the model and override the system/developer/user instruction.

### Table 6: Prompt injection evaluations

| Category | gpt-5.1-thinking | gpt-5.2-thinking | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| Prompt injection attacks in connectors | 0.649 | 0.971 | 0.998 | 0.963 |

Chatbots can empower consumers to better understand their health and help health professionals deliver better care \[[1](https://deploymentsafety.openai.com/gpt-5-5/references#ref-openaigpt52025blog "OpenAI. “Introducing GPT-5.” Available at: https://openai.com/index/introducing-gpt-5/ .")\] \[[2](https://deploymentsafety.openai.com/gpt-5-5/references#ref-openaipendaclinicalcopilot2025 "OpenAI. “Pioneering an AI clinical copilot with Penda health.” Available at: https://openai.com/index/ai-clinical-copilot-penda-health/ .")\]. We evaluate GPT-5.5 on HealthBench \[[3](https://deploymentsafety.openai.com/gpt-5-5/references#ref-openaihealthbench2025 "OpenAI. “Introducing HealthBench.” Available at: https://openai.com/index/healthbench/ .")\], an evaluation of health performance and safety, and HealthBench Professional, an evaluation of model capability and safety for clinician use cases \[[4](https://deploymentsafety.openai.com/gpt-5-5/references#ref-HEALTHBENCHPROFESSIONAL "Rebecca Soskin Hicks, Mikhail Trofimov, Dominick Lim, Rahul K. Arora, Foivos Tsimpourlas, Preston Bowman, et al. “ HealthBench Professional : Evaluating large language models on real clinician chats.” Available at: https://cdn.openai.com/dd128428-0184-4e25-b155-3a7686c7d744/HealthBench-Professional.pdf .")\].

Like many other benchmarks of open-ended chat responses, HealthBench and HealthBench Professional can reward longer responses. Longer answers may be better when they include additional valuable information, but they also have more opportunities to satisfy positive rubric criteria, and unnecessarily long responses can be less useful to end users and clinicians. Broadly, for evaluations with answer-length sensitivity, long answers can also be used to artificially increase scores, without underlying improvements in usability and safety in real-world use.

Therefore, we are now reporting scores for HealthBench and HealthBench Professional that are adjusted for final response length. Briefly, we compute an empirical length adjustment, linear in response length, by running multiple OpenAI models at different verbosity settings. For full details on this length adjustment procedure, see \[[4](https://deploymentsafety.openai.com/gpt-5-5/references#ref-HEALTHBENCHPROFESSIONAL "Rebecca Soskin Hicks, Mikhail Trofimov, Dominick Lim, Rahul K. Arora, Foivos Tsimpourlas, Preston Bowman, et al. “ HealthBench Professional : Evaluating large language models on real clinician chats.” Available at: https://cdn.openai.com/dd128428-0184-4e25-b155-3a7686c7d744/HealthBench-Professional.pdf .")\]. We are also now using an updated implementation of HealthBench and have recomputed scores for previous models, so scores may differ from previous system cards.

Responses of 2,000 characters receive no adjustment. Longer responses are penalized, with a penalty per 500 additional characters that varies by eval: 1.47 points per 500 characters for HealthBench Professional, 2.99 for HealthBench, 3.92 for HealthBench Hard, and 0.20 for HealthBench Consensus. Shorter responses receive a corresponding positive adjustment. All penalties here are reported on the 0-100 scale that we report this eval on.

### Table 7: Reported as length-adjusted score (unadjusted, mean response length in characters)

| **evaluation** | **GPT-5** | **GPT-5.1** | **GPT-5.2** | **GPT-5.4** | **GPT-5.5** |
| --- | --- | --- | --- | --- | --- |
| HealthBench length-adjusted | 57.7 (63.1, 2904) | 50.9 (64.2, 4222) | 56.8 (60.7, 2645) | 54.0 (55.7, 2275) | 56.5 (58.4, 2313) |
| HealthBench Hard length-adjusted | 34.7 (41.6, 2880) | 25.4 (41.4, 4049) | 34.3 (38.9, 2585) | 29.1 (30.3, 2161) | 31.5 (33.8, 2289) |
| HealthBench Consensus length-adjusted | 95.6 (96.0, 2880) | 95.0 (95.8, 4171) | 94.4 (94.7, 2615) | 96.3 (96.4, 2238) | 95.6 (95.7, 2259) |
| HealthBench Professional length-adjusted | 46.2 (51.0, 3616) | 39.6 (48.0, 4863) | 45.9 (50.0, 3400) | 48.1 (51.9, 3308) | 51.8% (57.2%, 3818) |

GPT-5.5 has a length-adjusted HealthBench score of 56.5 (+2.5 relative to GPT-5.4), HealthBench Hard score of 31.5 (+2.4), HealthBench Consensus score of 95.6 (-0.7), and HealthBench Professional score of 51.8 (+3.7). Answer lengths were comparable for HealthBench, Hard, and Consensus. In the case of HealthBench Professional, GPT-5.5 was longer (3893 characters vs 3308 characters), and had a higher unadjusted score and a higher length-adjusted score. Overall, this reflects generally improved HealthBench, HealthBench Hard, and HealthBench Professional performance vs GPT-5.4, with HealthBench Consensus flat.

Here we report dynamic multi-turn evaluations for mental health, emotional reliance, and self-harm that simulate extended conversations across these domains. Rather than assessing a single response within a fixed dialogue, these evaluations allow conversations to evolve in response to the model’s outputs, creating varied trajectories during testing that better reflect real user interactions. This approach helps identify potential issues that may only emerge over the course of long exchanges and provides an even more rigorous test than prior static multi-turn methods. By utilizing realistic, yet adversarial user simulations, these evaluations have enabled continued improvements in safety performance, particularly in areas where earlier evaluation frameworks had reached saturation.

Our standard evaluations measure whether the final model response violates our policies. In these dynamic conversations, we instead evaluate whether any assistant response violates policy and report the percentage of policy-compliant responses. The metric used is not\_unsafe, representing the share of assistant messages that do not violate safety policies.

### Table 8: Dynamic Benchmarks with Adversarial User Simulations

| Category | gpt-5.1-thinking | gpt-5.2-thinking | gpt-5.4-thinking | gpt-5.5 |
| --- | --- | --- | --- | --- |
| Mental health | 0.753 | 0.975 | 0.985 | 0.981 |
| Emotional reliance | 0.857 | 0.953 | 0.985 | 0.981 |
| Self-harm | 0.904 | 0.955 | 0.977 | 0.937 |

To focus on cases where factuality issues are harming the user experience, this evaluation measures hallucination rates on de-identified ChatGPT conversations that users of our prior models have flagged as containing factual errors. These examples are intended to capture especially hallucination-prone cases, not a representative slice of all production traffic.

We find that GPT-5.5’s individual claims are 23% more likely to be factually correct, and its responses contain a factual error 3% less often. GPT-5.5 tends to make more factual claims per response than GPT-5.4, explaining the discrepancy between claim-level and response-level improvements.

### Figure 3

![Figure 3](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/hallucination1.png)

Figure 3

In addition to evaluating behavior on representative ChatGPT prompts for disallowed content (discussed above), we also evaluated it for deceptive behaviors, similarly to how we did for GPT-5.2 Thinking. Our results suggest that GPT-5.5 shows a mix of higher and lower rates of misalignment than GPT-5.4 Thinking on representative ChatGPT prompts for the various categories we measure. While the results suggest an increase in incidence for the fabricated facts category, we believe that our de-identification pipeline may lead to false positives for this category in ways which may be differentially affecting GPT-5.5 and GPT-5.4 Thinking, and will further investigate this. As with disallowed content estimates from representative prompts, these misalignment estimates likely also exhibit meaningful bias, as seen by the differences in rates between GPT-5.4 Thinking production data and resampled data with the same model on the same distribution.

Deception Evaluations with Representative Prompts:

### Figure 4

![Figure 4](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/misalign3.png)

Figure 4

To complement our [ongoing asynchronous monitoring of internal deployments](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/), we also ran [representative-prompt resampling evaluations](https://alignment.openai.com/prod-evals/) on recent internal agentic coding trajectories using GPT-5.5 and an improved monitor for misaligned behaviors.

This form of resampling will allow us estimate relative propensities for various forms of misalignment before future large-scale internal deployments, without the distribution shifts that would impact misalignment rates when monitoring real usage. Resampling coding agent trajectories is difficult: they contain many tool calls which modify the external state of the environment, and interact with complex production systems and potentially the internet. To perform resampling without giving the tested model real affordances, we developed a simulator for tool responses which rely on information outside the codebase. This tool simulator has access to the exact state of the codebase at the time of the original conversation and the original trajectory. We evaluate the realism of this simulator against the original trajectory using a prompted GPT-5.4 Thinking model tasked with identifying the real trajectory. In this head-to-head comparison, the original trajectory only wins 52.5% of the time.

### Figure 5

![Figure 5](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/internaldep.png)

Figure 5

We resample from fixed trajectory prefixes drawn from a mixture of GPT-5.4 Thinking and a pre-final version of GPT-5.5 internal usage. For each prefix, we resample both using GPT-5.4 Thinking and GPT-5.5, and classify the final turn for a misalignment category and severity level (0-4, where 4 is highest) using our monitor. Our analysis estimates that GPT-5.5 is slightly more misaligned than GPT-5.4 Thinking across several categories, though nearly all of this is low-severity misalignment. We did not find any novel severe misalignment with this evaluation: the severity 3 rate was 0.01% for both models, and the highest severity level (4) of our system was never triggered.

To better understand these aggregate differences, we grouped flagged trajectories into subcategories defined by both the user’s situation and the model’s harmful action. After human review, these subcategories covered 86.4% of flagged classifications. This gave us a manageable set of recurring behavior patterns to inspect, which helped us localize much of the observed difference between GPT-5.5 and GPT-5.4 Thinking to specific agent misbehaviors.

Some of the subcategories with statistically significant increases involved GPT-5.5 acting as though pre-existing work was its own, ignoring user-given constraints about what kind of code changes it can make, or overeagerly taking action when the user was only asking questions.

These results are most useful as an additional signal about internal deployment risk, rather than as a direct measure of external deployment safety due to distribution shifts. At the values observed here, they provide additional evidence suggesting GPT-5.5 has a low propensity for severe misalignment in internal deployment.

### Figure 6

![Figure 6](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-5/assets/images/misalign2.png)

Figure 6

Our monitor has near-perfect recall on [OAI-repo-sabotage](https://openai.com/index/evaluating-chain-of-thought-monitorability/) and BashArena (100.0% and 99.1%, respectively). On a dataset of 21 real internal transcripts which we labeled as severity level 3, our classifier has 97.6% recall at flagging these transcripts as severity level 3+ (we classify each datapoint 10 times). We additionally labeled 63 transcripts as borderline severity 3, on these the classifier has 69% recall for 3+ (98.2% for 2+).

We also estimate the likelihood of detecting novel misalignment with our monitoring system on the human production labels. To do so, we measure the ability of the monitor to generalize to unknown misalignment categories that are not already surfaced in the monitor prompt. We do this by labelling each example with a ground truth category, then rerunning the monitor with this category ablated (either removing almost all detail about the category or completely removing the category from the prompt), and we see what the resulting classification is. One of our current categories is intended to catch misalignment that falls outside our current taxonomy of categories. Our experiments show that recall with these ablated monitors differ significantly when using severity 2 vs 3 as the threshold: 95% of current severity 3 traffic would be classified as at least severity 2, but less than half would be classified as severity 3.

For context, in our current review process, humans mainly review transcripts labeled as severity 3 and 4, and therefore recall at the severity 3 threshold is particularly important. However, we are actively developing additional monitoring stages that elevate severity 1 and 2 samples when they show novel or unusual forms of misalignment, which should make it much more feasible to catch significant novel misalignment which gets classified as severity 2.

[^1]: GPT-5.5 is intended to be used in accordance with OpenAI’s Usage Policies, Service Terms, and Terms of Use. These policies apply universally to OpenAI services and are designed to ensure safe and responsible usage of AI technology. You can review OpenAI’s Usage Policies at [openai.com/policies/usage-policies/](http://openai.com/policies/usage-policies/)

If you need assistance with respect to GPT-5.5, you can find further information on OpenAI’s website ([openai.com](http://openai.com/)), or you can contact OpenAI Support by opening the chat bubble icon displayed at the bottom-right of [help.openai.com](http://help.openai.com/)

A list of the languages that ChatGPT currently supports can be found [here.](https://help.openai.com/en/articles/8357869-how-to-change-your-language-setting-in-chatgpt)
