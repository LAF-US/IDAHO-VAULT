---
authority: Perplexity
status: imported note
date created: 2026-04-16
related:
  - LangChain
  - CrewAI
  - RAG
  - vector databases
  - Obsidian
  - Zettelkasten
---

# explain LangChain

LangChain is an open-source framework for building applications with large
language models, especially when those applications need tools, external data,
retrieval, or multi-step workflows.

It is best understood as application plumbing around an LLM rather than a model
itself. LangChain helps connect prompts, models, retrievers, memory, APIs, and
tools into a repeatable workflow.

## What it does

At a high level, LangChain helps an LLM interact with the rest of an
application. That can include:

- retrieving documents from a database or vector store
- calling APIs or tools
- structuring prompts and outputs
- carrying state across steps in a workflow

## Why people use it

People use LangChain because it reduces glue code when building LLM
applications. It is especially useful for:

- chatbots with external context
- retrieval-augmented generation systems
- tool-using assistants
- agentic or multi-step application flows

## Simple mental model

A basic LangChain app often looks like this:

1. Accept a user question.
2. Retrieve relevant context or documents.
3. Pass the question plus context to the model.
4. Return a grounded answer.

That turns a single model call into a workflow.

## LangChain and CrewAI

LangChain and CrewAI are complementary.

- **LangChain** is stronger at model, tool, retrieval, and data integration.
- **CrewAI** is stronger at role-based multi-agent coordination.

A practical rule:

- start with **LangChain** if the main problem is connecting an LLM to tools,
  retrieval, and data sources
- start with **CrewAI** if the main problem is coordinating several agents with
  different roles

They can also be used together: LangChain can provide tools and retrieval while
CrewAI coordinates the agents that use them.

## Related Python stack

In Python, a common stack around this topic is:

- `langchain`
- provider packages such as `langchain-openai`
- `langchain_community`
- `crewai`
- `pydantic`
- `python-dotenv`

The exact mix depends on whether the app is retrieval-heavy, tool-heavy, or
multi-agent.

## RAG and vector databases

RAG means retrieval-augmented generation: fetch relevant material first, then
answer with the model using that material as context.

Vector databases are often used as the retrieval layer inside a RAG system.
Documents are chunked, embedded, stored, then retrieved by semantic similarity
when a new question arrives.

Common vector store choices include:

- Pinecone
- Weaviate
- Milvus
- Qdrant
- Chroma
- Redis
- pgvector/PostgreSQL

## Obsidian and Zettelkasten

Obsidian and Zettelkasten fit naturally together because both favor linked
notes over rigid hierarchy.

A simple working rule:

1. capture a thought or source
2. rewrite it in your own words
3. keep one idea per note
4. link it to something else

## Working synthesis

The useful synthesis across these topics is that modern Python AI work is a
layered system:

- model libraries at the core
- data tooling around them
- orchestration frameworks such as LangChain and CrewAI above that
- retrieval and vector stores when grounding is needed

The important shift is from "call a model" to "build a system around a model."

## Notes on this import

This file has been normalized from a noisier Perplexity export.

- Encoding errors were removed.
- Repeated source blocks and follow-up prompts were collapsed.
- Off-topic speculative sections about `LAF-US`, the "Architect's Vault", and
  external repos were removed because they did not reliably describe the
  witnessed vault.

## Sources

- https://docs.langchain.com/oss/python/langchain/overview
- https://cloud.google.com/use-cases/langchain
- https://aws.amazon.com/what-is/langchain/
- https://docs.crewai.com/en/tools/ai-ml/langchaintool
- https://pypi.org/project/crewai/
