---
title: "Signal's Meredith Whitaker decries dependence on AWS"
source: "https://www.theregister.com/2025/10/27/signal_ceo_meredith_whittaker_aws_dependency/"
author:
  - "[[Thomas Claburn]]"
published: 2025-10-27
created: 2026-04-28
description: ": 'The problem is the concentration of power in the infrastructure space that means there isn’t really another choice'"
date created: Tuesday, April 28th 2026, 6:29:14 pm
date modified: Tuesday, April 28th 2026, 6:29:23 pm
---

## Signal president Meredith Whittaker says they had no choice but to use AWS, and that's a problem

## 'The problem is the concentration of power in the infrastructure space that means there isn’t really another choice'

Messaging service Signal may be unusual in its deployment of credible end-to-end encryption, but it shares a common availability vulnerability with many other internet services – dependence on Amazon Web Services (AWS).

Signal, like many other internet services, failed briefly during the [sizable AWS outage](https://www.theregister.com/2025/10/23/amazon_outage_postmortem/) that occurred on October 19 and 20. The cause, as AWS explained in its [paragraph-starved post-mortem](https://aws.amazon.com/message/101925/) last week, was an error in AWS' automated DNS management system. And the loss of availability and productivity across the many AWS-dependent businesses has been estimated to have cost businesses [more than a hundred billion dollars](https://edition.cnn.com/business/live-news/amazon-tech-outage-10-20-25-intl).

AWS has about a third of the global market share for cloud computing services, [according to Synergy Research Group](https://www.srgresearch.com/articles/cloud-market-jumped-to-330-billion-in-2024-genai-is-now-driving-half-of-the-growth).

But a former AWS employee who corresponded with *The Register* argues the figure is more like half of the cloud computing market because AWS runs backend services for notional rivals like IBM, Oracle, and Salesforce. A recent [report](https://hginsights.com/blog/aws-market-report-buyer-landscape) from HG Insights puts the number of businesses using AWS at more than 4 million, with particular concentrations within media, retail, internet services, manufacturing, and education. Our insider tells us thousands of government agencies also depend on AWS, including some national security workloads.

Signal president Meredith Whittaker called attention to this massive dependency in [a thread](https://mastodon.world/@Mer__edith/115445701583902092) on the Mastodon social network, explaining how the concentration of power among cloud hyperscalers limits the options of services like Signal in terms of resiliency and network control.

Whittaker said that the concentration of power among cloud hyperscalers (AWS, Google, and Microsoft) is less widely understood than she expected, which bodes poorly for efforts to craft realistic strategies to change this dynamic.

She explained, "The question isn't 'why does Signal use AWS?' It's to look at the infrastructural requirements of any global, real-time, mass comms platform and ask how it is that we got to a place where there's no realistic alternative to AWS and the other hyperscalers."

The technical challenges for a service like Signal, Whittaker said, involve running a low-latency platform for instant communications that can carry millions of concurrent audio and video calls. That requires infrastructure around the globe – computing, storage, and edge nodes. And that infrastructure must be powered, monitored, and repaired.

"Such infrastructure costs billions and billions of dollars to provision and maintain, and it's highly depreciable," said Whittaker. "In the case of the hyperscalers, the staggering cost is cross-subsidized by other businesses–themselves also massive platforms with significant lock-in."

The result is that most companies, Signal included, can't afford to replicate AWS' global network of data centers and computing power.

And even if Signal could afford to do so, she said, the talent to oversee global scale cloud computing is scarce.

"In short, the problem here is not that Signal 'chose' to run on AWS," said Whittaker. "The problem is the concentration of power in the infrastructure space that means there isn't really another choice: the entire stack, practically speaking, is owned by three to four players."

Whittaker said she hopes the recent AWS outage refocuses people's attention on the world's dependence on public cloud giants and encourages efforts to undo the concentration of power.

Europe, which has been thinking about [the problem of data sovereignty](https://www.theregister.com/2025/02/26/europe_has_second_thoughts_about/) more seriously since the Trump administration took over in January, has found that it's easier to talk about avoiding US tech giants than it is to actually do so. For example, the official EU Cloud Sovereignty Framework has [come under fire from CISPE](https://www.theregister.com/2025/10/27/cispe_eu_sovereignty_framework/), a trade association of EU cloud providers, over concerns that the rules favor AWS, Microsoft Azure, and Google Cloud.

Plus, there's always the possibility that the Trump administration, in support of domestic economic advantage, could simply [turn off the internet in Europe](https://www.politico.eu/article/donald-trump-eu-internet-europe-us-trade-war-data-cyber/) – whether that involves DNS meddling or directives to US tech giants to withhold service – to secure consent for its demands.

The internet [is said](https://www.rand.org/pubs/articles/2018/paul-baran-and-the-origins-of-the-internet.html) – [though this is disputed](https://www.internetmythen.de/en/index0258.html) – to have emerged from efforts to design a network that could survive nuclear war, a scenario that rather optimistically assumes the health of those operating the network. But it has already been captured by cloud capital expenditures. ®

[No more fake tech news! Add The Register to your Preferred Sources in Google Search](https://go.theregister.com/tl/3337/shttps://go.theregister.com/k/reg-preferred-sources)

×