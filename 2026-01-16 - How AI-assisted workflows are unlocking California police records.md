---
title: "How AI-assisted workflows are unlocking California police records"
source: "https://current.org/2026/01/how-ai-assisted-workflows-are-unlocking-california-police-records/"
author:
  - "[[Ethan Toven-Lindsey]]"
  - "[[Tim Olson]]"
  - "[[Ernesto Aguilar]]"
published: 2026-01-16
created: 2026-05-01
description: "An AI-powered database offers a model for extracting and structuring police records for public accessibility and accountability reporting."
date created: Friday, May 1st 2026, 4:26:11 pm
date modified: Friday, May 1st 2026, 4:26:44 pm
---

Shortly after midnight on Jan. 1, 2019, a handful of California news organizations combined forces to do something exciting. At the exact moment a new transparency law took effect in the state, dozens of journalists filed hundreds of public records requests for police misconduct and shooting records.

In the days and years that followed, KQED took an influential role in what became the California Reporting Project, a collaboration of more than 40 newsrooms and graduate students from the University of California at Berkeley. Partners in the project used the law, public document requests, database tools and artificial intelligence to pry loose an unprecedented volume of police records across the state.

In doing so, KQED and its partners positioned the collaboration to help pry loose public records for a larger audience. But unbeknownst to us at the time, the project also laid a foundation for using artificial intelligence to help build a durable database of public records. In the process, we created technical, financial and governance models that make long-term public access possible.

That access is already changing what is possible for journalism, allowing reporters to spot patterns across agencies and years instead of chasing one case at a time. It gives defense attorneys, advocates and families new evidence to challenge official narratives and offers researchers and policymakers a clearer view of how force and misconduct are handled.

This is how we did it.

Between 2018 and 2021, as many other states were also debating or passing police transparency laws, California adopted measures aimed at strengthening police accountability statewide. Its own transparency experiment came with clear limits that shaped how KQED and its partners designed their system.

Lawmakers passed the “Right to Know Act” in 2018, then strengthened it in 2021, to give the public access to records about police shootings, serious uses of force and certain categories of misconduct. Both laws require disclosure of only a narrow slice of uses of force or when officers violate certain policies. Since 2019, journalists working on the California Reporting Project have filed requests with nearly 700 agencies, from local police and sheriffs to school and university police, the California Highway Patrol, prisons, probation departments, district attorneys, coroners, medical examiners, oversight boards and commissions, and the state attorney general. In response, agencies have released investigative reports and findings, autopsy reports, transcripts and videos of interviews, investigative hearings, photographs and body-worn camera video.

As KQED’s team quickly realized, the volume and variety of material required new tools and new editorial workflows to turn a legal win into something the public could actually use.

The flood of records also raised a practical question for KQED as the project’s coordinating hub. How do you build a shared public resource from thousands of PDFs, audio files and videos scattered across hard drives, shared folders and newsroom laptops?

Over time, KQED led the push to turn the growing archive into something permanent and usable. For instance, early on Stanford University and UC Berkeley led a critical push to convene partners in person to map out what journalists, lawyers and community groups would actually need from the data. With the Berkeley Institute for Data Science, UC Berkeley Journalism’s Investigative Reporting Program and Stanford’s Big Local News, we scoped requirements, designed a shared oversight of the data and committed staff time to testing assumptions against real reporting questions. A multiyear, state-funded research grant administered through UC Berkeley underwrote the heavy technical lift, supporting engineers and data scientists who could ingest thousands of PDFs, audio files and videos, de-duplicate and link them across agencies, and then use AI to cluster documents into cases, extract key facts like incident dates and officer names, and index everything for search.

At KQED, we viewed one of our roles as keeping the work grounded in newsroom reality, bringing in reporters to stress-test the tools, pushing for clear policies on privacy and redactions, and helping shape a model that other organizations could replicate: a shared technical backbone, governed by universities, informed by community and legal partners, and driven by accountability reporting needs.

As the work expanded, KQED helped connect the California Reporting Project to a national collaboration of people seeking to extract and structure similar records from other states, under the umbrella of the Police Records Access Project. Today, the project holds more than 22 terabytes of records collected by the California Reporting Project.

Supported in part by a grant from the Google News Initiative, the [partners released a public site last year](https://current.org/2025/08/california-news-coalition-launches-database-of-police-misconduct-records/) that offers roughly 1.5 million pages of records in a [searchable database](https://policerecords.kqed.org/) that journalists, researchers, families and community advocates can explore directly. For many users, that public interface is the visible achievement.

Inside these projects, AI-assisted workflows make the whole thing possible.

The reporting and data team, led by former KQED data journalist Lisa Pickoff-White and California Newsroom journalist Emily Zentner, uses AI to make sense of documents at a scale that would be impossible with human labor alone.

![Lisa Pickoff-White, director of research at California Reporting Project. ](https://current.org/wp-content/uploads/2025/08/Lisa-Pickoff-White-edited.jpeg)

Pickoff-White

“We’ve found that most stories need one or a combination of these common techniques: file summarization, data extraction and search,” Pickoff-White says. “That includes quick stories when a reporter needs to background an officer to see if they’re named in our records and in-depth investigations into specific agencies, uses of force or misconduct.”

This means the journalists are not asking AI to write stories. They are using it to unlock records that would otherwise sit in digital boxes.

Journalists helped define the database’s technical structure so that uses of large language models and generative AI are tightly scoped and transparent. AI extracts key facts such as incident dates and classifies cases by type based on the text in each file; staff group documents into cases. Once files are grouped into a case, algorithms built by the project team check whether agencies are sending all the cases they are legally required to disclose.

The system cross-references our database against data on uses of force, in-custody deaths and sustained complaints that agencies report to the state Department of Justice. When the algorithms find incidents in the DOJ data with no corresponding case in our records, staff can flag those gaps and follow up with agencies. Using this method, the team has identified thousands of additional cases that local agencies might not have sent otherwise.

The staff who evaluate the accuracy of models also check them against hand-crafted samples of cases from every year and every type of agency in the collection. The team also manually reviews every case that machine learning flags as misconduct.

Just as important, AI does not determine what the public sees. Users can search for a phrase, and the system returns cases containing literal matches to the search term in text from the original government records.

For daily newsroom workflows, that has meant pairing machine learning with careful human oversight, then stress-testing the results on real deadlines. AI tools summarize lengthy reports, surface patterns across thousands of pages and extract key fields that can be checked, corrected and structured for analysis. Journalists still do the core work of reporting, verification and storytelling, but AI lets them see across an archive that once lived in cardboard bankers boxes, hard drives and forgotten file rooms.

Our approach prioritized ensuring the database is also candid about what it cannot show. The law requires disclosure only when people are seriously injured or killed or when an agency finds that an officer violated certain types of policy, such as lying about an investigation, racial profiling, sexual misconduct, excessive force, unlawful search and seizure, or failure to intervene, so the dataset does not represent every allegation or every use of force in California. Agencies can withhold records while investigations are active, and some records only arrive after cases close. Multiple agencies may also generate records about the same incident, so users may see overlapping files from a sheriff, medical examiner and district attorney. Search itself has limits.

The project’s approach to redactions and sensitive material also provides a blueprint that reflects public media values. Some records contain graphic images or unredacted personal information, including addresses and Social Security numbers. When agencies fail to redact sensitive data, those files are withheld from search results. In instances where every case document is too sensitive or exists only as unprocessed audio, images or video, a case page will display no files at all. The team is working on ways to display more metadata about those hidden files and plans to process multimedia in the future.

A newsroom with access to a set of specific, high-impact records can adapt this model by using AI first for summarization, extraction and search, with clear human checks and published guardrails at every step.

A few lessons for public media leaders who are thinking about how to deploy AI to organize and manage access to large datasets:

- Use AI behind the scenes to do the sorting, linking and extraction at scale, but keep both the search experience and the final judgments anchored in source documents and human review.
- Start with the legal and practical definitions that govern your records and build your schema around them.
- Talk honestly about gaps and uncertainty instead of overselling what AI-assisted data can deliver. The California Reporting Project’s site, for example, urges users to treat search as a starting point and to read the PDFs of the underlying government records before reaching conclusions.
- Prioritize safety and privacy in AI results, even when it means gaps in what appears online. Be transparent about why some data may appear incomplete.
- AI-enabled accountability projects are not just technical builds; they are coalition projects that work best when journalists, technologists and community members work together.

At this point, one of the biggest lessons we’ve learned from this project is that our usage of AI and the innovations that spring from that will be about behind-the-scenes databases and search work — not about making police misconduct investigations go viral.

For public media, that is the kind of AI leadership that matters most.

*Ethan Toven-Lindsey is editor in chief at KQED in San Francisco, where he oversees newsroom operations, podcasting, radio programming and editorial standards. With more than two decades of experience in public media journalism, he previously served as senior managing editor of Here & Now, the newsmagazine produced by NPR and Boston’s WBUR.*

*As KQED’s head of partnerships, Tim Olson guides strategic applications of AI that ensure responsible uses and positive societal impact of the technology. Ernesto Aguilar oversees radio broadcast content and innovation initiatives in KQED’s content division. He previously served as executive director of the National Federation of Community Broadcasters.*

*Ernesto Aguilar oversees radio broadcast content and innovation initiatives in KQED’s content division. He previously served as executive director of the National Federation of Community Broadcasters.*