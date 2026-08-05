---
title: "Nous Portal"
source: "https://portal.nousresearch.com/api-docs"
author:
published:
created: 2026-04-29
description: "Nous Research is a leader in the development of human-centric language models and simulators. Manage your account and API keys here."
tags:
  - "clippings"
---
## API Docs\_

## Nous Research Inference API1.0.0OAS 3.0

[/api/openapi](https://portal.nousresearch.com/api/openapi)

An OpenAI-compatible API for running completion requests on Nous Research's inference backend.

## API Base URL

- The API is available at [https://inference-api.nousresearch.com/v1](https://inference-api.nousresearch.com/v1).
- You can use this URL with OpenAI-compatible clients and libraries.

## Authentication & Payment

### Option 1: Using API keys & account credits:

The standard method of authenticating with the API is via API keys.

- Register an account on [https://portal.nousresearch.com](https://portal.nousresearch.com/).
- Add API credits or activate a subscription, then generate an API key.
- Set the API key as a bearer token in the `Authorization` header in your requests.

### Option 2: x402 Support (beta)

The API supports payment via the [x402 protocol](https://www.x402.org/) using Solana USDC. This enables:

- **More anonymous usage**: No account registration or API key required.
- **Pay-per-request**: No need to pre-purchase credits; pay only for what you use.
- **Automatic cost tracking**: All payments are tracked on-chain.

**Note:** we strongly recommend that you set a `max_tokens` parameter in your x402 requests explicitly, else we default to a high limit. The x402 protocol requires that the price of a request must be determined before the work is executed. This means you will be charged for the number of tokens specified by the `max_tokens` parameter in your request or a default max if not set, regardless of actual usage.

To use x402 payments with the API:

1. Ensure you have a Solana wallet with USDC funds available.
2. Prepare your inference request as normal, setting the desired parameters including `max_tokens`.
3. Issue your inference request to the API endpoint as normal, but without an Authorization header. You will get a `402` response with payment requirement details.
4. Construct a payment signature matching the payment requirements as per the x402 spec (there are client libraries to help with this), and re-run the request including the payment signature in the generated `X-PAYMENT` header.

## Usage & Pricing

- Usage is charged by consumed tokens.
- Pricing details are available at [https://portal.nousresearch.com/models](https://portal.nousresearch.com/models). Note that there is a small surcharge when using x402.

### API Key Rate Limits

- **Ultra**: 1,600 RPM, 16,000,000 TPM
- **Free**: 50 RPM, 500,000 TPM
- **Super**: 800 RPM, 8,000,000 TPM
- **Plus**: 400 RPM, 4,000,000 TPM
- **Default paid users**: 200 RPM, 800,000 TPM

## Available Models

- `Hermes-4.3-36B` (128k context)
- `Hermes-4-70B` (128k context)
- `Hermes-4-405B` (128k context)

See [https://portal.nousresearch.com/models](https://portal.nousresearch.com/models) for more details on each model, including pricing and capabilities.

## Reasoning

When using Hermes 4 or DeepHermes, remember to use the following system prompt to enable reasoning:

`You are a deep thinking AI, you may use extremely long chains of thought to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct solution prior to answering. You should enclose your thoughts and internal monologue inside <think> </think> tags, and then provide your solution or response to the problem.`

Alternatively, if you're using completions or have the ability to modify the assistant responses, you can prefill `<think>` in the responses to trigger reasoning.

The location of the reasoning output in the response depends on a few factors.

- With Deep Hermes 3, the reasoning output will always be amongst the standard response content between `<think></think>` tags.
- With Hermes 4, if you prefill the response with the tag, the reasoning output will also be between `<think></think>` tags.
- With Hermes 4, if you use the reasoning system prompt and do **not** prefill the tag, the reasoning output will be included in `reasoning_content` field of the output.

Servers