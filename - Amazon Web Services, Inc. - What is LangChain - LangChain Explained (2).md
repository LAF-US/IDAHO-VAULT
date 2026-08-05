---
source: "https://aws.amazon.com/what-is/langchain/"
author:
  - "[[Amazon Web Services]]"
published:
created: 2026-04-17
---
## What is LangChain?

LangChain is an open source framework for building applications based on large language models (LLMs). LLMs are large deep-learning models pre-trained on large amounts of data that can generate responses to user queries—for example, answering questions or creating images from text-based prompts. LangChain provides tools and abstractions to improve the customization, accuracy, and relevancy of the information the models generate. For example, developers can use LangChain components to build new prompt chains or customize existing templates. LangChain also includes components that allow LLMs to access new data sets without retraining.

[Read about Large Language Models (LLMs)](https://aws.amazon.com/what-is/large-language-model/)

## Why is LangChain important?

LLMs excel at responding to prompts in a general context, but struggle in a specific domain they were never trained on. *Prompts* are queries people use to seek responses from an LLM. For example, an LLM can provide an answer to how much a computer costs by providing an estimate. However, it can't list the price of a specific computer model that your company sells.

To do that, machine learning engineers must integrate the LLM with the organization’s internal data sources and apply [*prompt engineering*](https://aws.amazon.com/what-is/prompt-engineering/) —a practice where a data scientist refines inputs to a generative model with a specific structure and context.

LangChain streamlines intermediate steps to develop such data-responsive applications, making prompt engineering more efficient. It is designed to develop diverse applications powered by language models more effortlessly, including [chatbots](https://aws.amazon.com/what-is/chatbot/), question-answering, content generation, summarizers, and more.

The following sections describe benefits of LangChain.

### Repurpose language models

With LangChain, organizations can repurpose LLMs for domain-specific applications without retraining or fine-tuning. Development teams can build complex applications referencing proprietary information to augment model responses. For example, you can use LangChain to build applications that read data from stored internal documents and summarize them into conversational responses. You can create a Retrieval Augmented Generation (RAG) workflow that introduces new information to the language model during prompting. Implementing context-aware workflows like RAG reduces model hallucination and improves response accuracy.

### Simplify AI development

LangChain simplifies [artificial intelligence (AI)](https://aws.amazon.com/what-is/artificial-intelligence/) development by abstracting the complexity of data source integrations and prompt refining. Developers can customize sequences to build complex applications quickly. Instead of programming business logic, software teams can modify templates and libraries that LangChain provides to reduce development time.

### Developer support

LangChain provides AI developers with tools to connect language models with external data sources. It is open-source and supported by an active community. Organizations can use LangChain for free and receive support from other developers proficient in the framework.

## How does LangChain work?

With LangChain, developers can adapt a language model flexibly to specific business contexts by designating steps required to produce the desired outcome.

### Chains

*Chains* are the fundamental principle that holds various AI components in LangChain to provide context-aware responses. A chain is a series of automated actions from the user's query to the model's output. For example, developers can use a chain for:

- Connecting to different data sources.
- Generating unique content.
- Translating multiple languages.
- Answering user queries.

### Links

Chains are made of *links*. Each action that developers string together to form a chained sequence is called a link. With links, developers can divide complex tasks into multiple, smaller tasks. Examples of links include:

- Formatting user input.
- Sending a query to an LLM.
- Retrieving data from cloud storage.
- Translating from one language to another.

In the LangChain framework, a link accepts input from the user and passes it to the LangChain libraries for processing. LangChain also allows link reordering to create different AI workflows.

### Overview

To use LangChain, developers install the framework in Python with the following command:

*pip install langchain*

Developers then use the chain building blocks or LangChain Expression Language (LCEL) to compose chains with simple programming commands. The *chain()* function passes a link's arguments to the libraries. The *execute()* command retrieves the results. Developers can pass the current link result to the following link or return it as the final output.

Below is an example of a chatbot chain function that returns product details in multiple languages.

*chain(\[*

*retrieve\_data\_from\_product\_database().*

*send\_data\_to\_language\_model().*

*format\_output\_in\_a\_list().*

*translate\_output\_in\_target\_language()*

*\])*

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2023/07/13/DBBLOG-3334-image001.png)

## What are the core components of LangChain?

Using LangChain, software teams can build context-aware language model systems with the following modules.

### LLM interface

LangChain provides APIs with which developers can connect and query LLMs from their code. Developers can interface with public and proprietary models like GPT, Bard, and PaLM with LangChain by making simple API calls instead of writing complex code.

### Prompt templates

*Prompt templates* are pre-built structures developers use to consistently and precisely format queries for AI models. Developers can create a prompt template for chatbot applications, few-shot learning, or deliver specific instructions to the language models. Moreover, they can reuse the templates across different applications and language models.

### Agents

Developers use tools and libraries that LangChain provides to compose and customize existing chains for complex applications. An *agent* is a special chain that prompts the language model to decide the best sequence in response to a query. When using an agent, developers provide the user's input, available tools, and possible intermediate steps to achieve the desired results. Then, the language model returns a viable sequence of actions the application can take.

### Retrieval modules

LangChain enables the architecting of RAG systems with numerous tools to transform, store, search, and retrieve information that refine language model responses. Developers can create semantic representations of information with word embeddings and store them in local or cloud vector databases.

### Memory

Some conversational language model applications refine their responses with information recalled from past interactions. LangChain allows developers to include memory capabilities in their systems. It supports:

- Simple memory systems that recall the most recent conversations.
- Complex memory structures that analyze historical messages to return the most relevant results.

### Callbacks

Callbacks are codes that developers place in their applications to log, monitor, and stream specific events in LangChain operations. For example, developers can track when a chain was first called and errors encountered with callbacks.

## How can AWS help with your LangChain requirements?

Using Amazon Bedrock, Amazon Kendra, Amazon SageMaker JumpStart, LangChain, and your LLMs, you can build highly-accurate generative artificial intelligence (generative AI) applications on enterprise data. LangChain is the interface that ties these components together:

- [Amazon Bedrock](https://aws.amazon.com/bedrock/) is a managed service with which organizations can build and deploy generative AI applications. You can use Amazon Bedrock to set up a generational model, which you access from LangChain.
- [Amazon Kendra](https://aws.amazon.com/kendra/) is a machine learning (ML)-powered service that helps organizations perform internal searches. You can connect Amazon Kendra to LangChain, which uses data from proprietary databases to refine language model outputs.
- [Amazon SageMaker Jumpstart](https://aws.amazon.com/sagemaker/jumpstart/) is an ML hub that provides pre-built algorithms and foundational models that developers can deploy quickly. You can host foundational models on SageMaker Jumpstart and prompt them from LangChain.

Get started with LangChain on AWS by [creating an account](https://portal.aws.amazon.com/billing/signup) today.

## Browse all cloud computing concepts

Browse all cloud computing concepts content here:

Displaying 1-8 (293)[2022-08-08](https://aws.amazon.com/what-is/iaas/?trk=faq_card)

#### What is IaaS (Infrastructure as a Service)?

Infrastructure as a Service (IaaS) is a business model that delivers IT infrastructure like compute, storage, and network resources on a pay-as-you-go basis over the internet. You can use IaaS to request and configure the resources you require to run your applications and IT systems. You are responsible for deploying, maintaining, and supporting your applications, and the IaaS provider is responsible for maintaining the physical infrastructure. Infrastructure as a Service gives you flexibility and control over your IT resources in a cost-effective manner.

Learn more

[View original](https://aws.amazon.com/what-is/iaas/?trk=faq_card)[2022-05-25](https://aws.amazon.com/what-is/machine-translation/?trk=faq_card)

#### What is Machine Translation?

Machine translation is the process of using artificial intelligence to automatically translate text from one language to another without human involvement. Modern machine translation goes beyond simple word-to-word translation to communicate the full meaning of the original language text in the target language. It analyzes all text elements and recognizes how the words influence one another.

Learn more

[View original](https://aws.amazon.com/what-is/machine-translation/?trk=faq_card)[2022-08-12](https://aws.amazon.com/what-is/block-storage/?trk=faq_card)

#### What is Block Storage?

Block storage is technology that controls data storage and storage devices. It takes any data, like a file or database entry, and divides it into blocks of equal sizes. The block storage system then stores the data block on underlying physical storage in a manner that is optimized for fast access and retrieval. Developers prefer block storage for applications that require efficient, fast, and reliable data access. Think of block storage as a more direct pipeline to the data as opposed to file storage which has an extra layer consisting of a file system (NFS, SMB) to process before accessing the data.

Learn more

[View original](https://aws.amazon.com/what-is/block-storage/?trk=faq_card)[2021-09-29](https://aws.amazon.com/relational-database/?trk=faq_card)

#### What is a Relational Database?

A relational database is a collection of data items with pre-defined relationships between them. These items are organized as a set of tables with columns and rows. Tables are used to hold information about the objects to be represented in the database. Each column in a table holds a certain kind of data and a field stores the actual value of an attribute. The rows in the table represent a collection of related values of one object or entity. Each row in a table could be marked with a unique identifier called a primary key, and rows among multiple tables can be made related using foreign keys. This data can be accessed in many different ways without reorganizing the database tables themselves.

Learn more

[View original](https://aws.amazon.com/relational-database/?trk=faq_card)[2023-10-02](https://aws.amazon.com/what-is/advanced-analytics/?trk=faq_card)

#### What is Advanced Analytics?

Advanced analytics is the process of using complex machine learning (ML) and visualization techniques to derive data insights beyond traditional business intelligence. Modern organizations collect vast volumes of data and analyze it to discover hidden patterns and trends. They use the information to improve business process efficiency and customer satisfaction. With advanced analytics, you can take this one step further and use data for future and real-time decision-making. Advanced analytics techniques also derive meaning from unstructured data like social media comments or images. They can help your organization solve complex problems more efficiently. Advancements in cloud computing and data storage have made advanced analytics more affordable and accessible to all organizations.

Learn more

[View original](https://aws.amazon.com/what-is/advanced-analytics/?trk=faq_card)[2023-10-04](https://aws.amazon.com/what-is/gpu/?trk=faq_card)

#### What is a GPU?

A graphics processing unit (GPU) is an electronic circuit that can perform mathematical calculations at high speed. Computing tasks like graphics rendering, machine learning (ML), and video editing require the application of similar mathematical operations on a large dataset. A GPU’s design allows it to perform the same operation on multiple data values in parallel. This increases its processing efficiency for many compute-intensive tasks.

Learn more

[View original](https://aws.amazon.com/what-is/gpu/?trk=faq_card)[2024-08-01](https://aws.amazon.com/what-is/enterprise-ai/?trk=faq_card)

#### What Is Enterprise AI?

Enterprise artificial intelligence (AI) is the adoption of advanced AI technologies within large organizations. Taking AI systems from prototype to production introduces several challenges around scale, performance, data governance, ethics, and regulatory compliance. Enterprise AI includes policies, strategies, infrastructure, and technologies for widespread AI use within a large organization. Even though it requires significant investment and effort, enterprise AI is important for large organizations as AI systems become more mainstream.

Learn more

[View original](https://aws.amazon.com/what-is/enterprise-ai/?trk=faq_card)[2022-05-25](https://aws.amazon.com/what-is/web-hosting/?trk=faq_card)

#### What is Web Hosting?

Web hosting is a service that stores your website or web application and makes it easily accessible across different devices such as desktop, mobile, and tablets. Any web application or website is typically made of many files, such as images, videos, text, and code, that you need to store on special computers called servers. The web hosting service provider maintains, configures, and runs physical servers that you can rent for your files. Website and web application hosting services also provide additional support, such as security, website backup, and website performance, which free up your time so that you can focus on the core functions of your website.

Learn more

[View original](https://aws.amazon.com/what-is/web-hosting/?trk=faq_card)

## Did you find what you were looking for today?

Let us know so we can improve the quality of the content on our pages