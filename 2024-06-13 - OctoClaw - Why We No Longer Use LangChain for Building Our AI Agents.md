---
source: "https://octoclaw.ai/blog/why-we-no-longer-use-langchain-for-building-our-ai-agents"
author:
  - "[[OctoClaw]]"
published: 2024-06-13
created: 2026-04-17
---
At Octomind, we use AI agents with multiple LLMs to automatically create and fix end-to-end tests in Playwright. Until just a few months ago, we did it with the [LangChain framework](https://www.langchain.com/).

In this post I'll share our struggles with LangChain and why replacing its rigid high-level abstractions with modular building blocks simplified our code base and made our team happier and more productive.

## The backstory

We used LangChain in production for over 12 months, starting in early 2023 then removing it in 2024.

LangChain seemed to be the best choice for us in 2023. It had an impressive list of components and tools, and its popularity soared. It promised to " *enable developers to go from an idea to working code in an afternoon.*" But problems started to surface as our requirements became more sophisticated, turning LangChain into a source of friction, not productivity.

As its inflexibility began to show, we soon found ourselves diving into LangChain internals, to improve lower-level behavior of our system. But because LangChain intentionally abstracts so many details from you, it often wasn't easy or possible to write the lower-level code we needed to.

## The perils of being an early framework

AI and LLMs are rapidly changing fields, with new concepts and ideas popping up weekly. So when a framework such as LangChain is created around multiple emerging technologies, designing abstractions that will stand the test of time is incredibly difficult.

I'm sure that If I had attempted to build a framework such as LangChain when they did, I wouldn't have done any better. Mistakes are easy to point out in hindsight, and the intent of this post is not to unfairly criticize LangChain's core developers or their contributors. Everyone is doing the best they can.

**Crafting well-designed abstractions is hard** - even if the requirements are well-understood. But when you're modelling components in such a state of flux (e.g. agents), it's a safer bet to use abstractions for lower level building blocks only.

## The problem with LangChain's abstractions

LangChain was helpful at first when our simple requirements aligned with its usage presumptions. But its high-level abstractions soon made our code more difficult to understand and frustrating to maintain. When our team began spending as much time understanding and debugging LangChain as it did building features, it wasn't a good sign.

Issues with LangChain's approach to abstractions can be demonstrated with this trivial example of translating an English word into Italian.

Here is a Python example using just the OpenAI package:

```
1 from openai import OpenAI
 2 
 3 client = OpenAI(api_key="<your_api_key>")
 4 text = "hello!"
 5 language = "Italian"
 6 
 7 messages = [
 8  {"role": "system", "content": "You are an expert translator"},
 9  {"role": "user", "content": f"Translate the following from English into {language}"},
10  {"role": "user", "content": f"{text}"},
11 ]
12 
13 response = client.chat.completions.create(model="gpt-4o", messages=messages)
14 result = response.choices[0].message.content
```

This is simple code that is easy to understand, containing a single class and one function call. The rest is standard Python.

Let's contrast this with LangChain's version:

```
1 from langchain_openai import ChatOpenAI
 2 from langchain_core.output_parsers import StrOutputParser
 3 from langchain_core.prompts import ChatPromptTemplate
 4 
 5 os.environ["OPENAI_API_KEY"] = "<your_api_key>"
 6 text = "hello!"
 7 language = "Italian"
 8 
 9 prompt_template = ChatPromptTemplate.from_messages(
10  [("system", "You are an expert translator"),
11  ("user", "Translate the following from English into {language}"),
12  ("user", "{text}")]
13 )
14 
15 parser = StrOutputParser()
16 chain = prompt_template | model | parser
17 result = chain.invoke({"language": language, "text": text})
```

The code is roughly doing the same, but that's where the similarities end.

We now have three classes and four function calls. But most concerning, is the introduction of three new abstractions:

- Prompt templates: Providing a prompt to the LLM
- Output parsers: Processing output from the LLM
- Chains: LangChain's "LCEL syntax" overriding Python's `|` operator

All LangChain has achieved is increased the complexity of the code with no perceivable benefits.

This code might be fine for early-stage prototypes. But **for production usage, every component must be reasonably understood** so it won't blow up on you unexpectedly under real-world usage conditions. You have to adhere to the given data structures and design your application around those abstractions.

Let's look at another abstraction comparison in Python, this time for fetching JSON from an API.

Using the built-in http package:

```
1 import http.client
2 import json
3 
4 conn = http.client.HTTPSConnection("api.example.com")
5 conn.request("GET","/data")
6 response = conn.getresponse()
7 data = json.loads(response.read().decode())
8 conn.close()
```

Using the requests package:

```
1 import requests
2 
3 response = requests.get("https://api.example.com/data")
4 data = response.json()
```

The winner is obvious. That's what a good abstraction feels like.

Granted, these are trivial examples. But my point is that good abstractions simplify your code and reduce the cognitive load required to understand it.

LangChain tries to make your life easier by doing more with less code by **hiding details away from you**. But when this comes at the cost of simplicity and flexibility, abstractions lose their value.

LangChain also has a habit of using **abstractions on top of other abstractions**, so you're often forced to think in terms of nested abstractions to understand how to use an API correctly. This inevitably leads to comprehending huge stack traces and debugging internal framework code you didn't write instead of implementing new features.

## LangChain's impact on our development team

Our application makes heavy use of AI agents for performing different types of tasks, such as test case discovery, Playwright test generation, and auto-fixing.

When we wanted to move from an architecture with a single sequential agent to something more complex, LangChain was the limiting factor. For example, spawning sub-agents and letting them interact with the original agent. Or multiple specialist agents interacting with each other.

In another instance, we needed to dynamically change the availability of tools our agents could access, based on business logic and output from the LLM. But LangChain does not provide a method for externally observing an agent's state, resulting in us reducing the scope of our implementation to fit into the limited functionality available to LangChain Agents.

> Once we removed it, we no longer had to translate our requirements into LangChain appropriate solutions. We could just code.

So, if not LangChain, what framework should you be using? Perhaps you don't need a framework at all.

## Do you need a framework for building AI applications?

LangChain helped us early on by providing LLM features so we could focus on building our application. But in hindsight, we would've been better off long-term without a framework.

LangChain's long list of components gives the impression that building an LLM-powered application is complicated. But the core components most applications will need are typically:

- A client for LLM communication
- Functions/Tools for function calling
- A vector database for RAG
- An Observability platform for tracing, evaluation etc.

The rest are either helpers around those components (e.g. chunking and embeddings for vector databases), or regular application tasks such as managing files and application state through data persistence and caching.

If you start your AI development journey without a framework, yes, it will take longer to put your own toolbox together and require more upfront learning and research. But this is time well spent and a worthy investment in you and your application's future, since you are learning fundamentals in the field you are going to operate.

In most cases, **your usage of LLMs will be simple and straightforward**. You'll mostly be writing sequential code, iterating on prompts, and improving the quality and predictability of your output. The majority of tasks can be achieved with simple code and a relatively small collection of external packages.

Even if using agents, it's unlikely you'll be doing much beyond simple agent to agent communication in a predetermined sequential flow with business logic for handling agent state and their responses. You don't need a framework to implement this.

> While the Agents space is rapidly evolving with exciting possibilities and interesting use cases, we recommend keeping things simple for now while agent usage patterns solidify.

## Staying fast and lean with building blocks

Presuming you're not shipping rubbish code to production, the speed at which a team can innovate and iterate is the most important metric for success. A lot of development in the AI space is driven by experimentation and prototyping.

But frameworks are typically designed for **enforcing structure based on well-established patterns of usage** - something LLM-powered applications don't yet have. Having to translate new ideas into framework-specific code, limits your speed of iteration.

A building blocks approach prefers simple low-level code with carefully selected external packages, keeping your architecture lean so developers can devote their attention to the problem they're trying to solve.

A building block being something simple you feel is comprehensively understood and unlikely to change. For example, a vector database. It's a known type of **modular component with a baseline set of features so it can easily be swapped** out and replaced. Your codebase needs to be lean and adaptable to maximize your learning speed and the value you get from each iteration cycle.

...

I hope I thoughtfully and fairly described our challenges with LangChain and why moving away from frameworks altogether has been hugely beneficial for our team.

Our current strategy of using modular building blocks with minimal abstractions allows us to now develop more quickly and with less friction.

[Deploy Your First Agent →](https://octoclaw.ai/pricing)