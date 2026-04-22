---
source: "https://docs.mistral.ai/api"
author:
published:
created: 2026-04-17
---
[

](https://docs.mistral.ai/)

[Getting Started](https://docs.mistral.ai/)[Models](https://docs.mistral.ai/models)[Products](https://docs.mistral.ai/products)[Developers](https://docs.mistral.ai/developers)[Admin](https://docs.mistral.ai/admin)[API](https://docs.mistral.ai/api)

[Reach out](https://mistral.ai/contact?utm_source=docs&utm_medium=header_cta&utm_campaign=studio_trial)[Try Studio](https://console.mistral.ai/?utm_source=docs&utm_medium=header_cta&utm_campaign=studio_trial)

[Download OpenAPI Spec](https://docs.mistral.ai/openapi.yaml)

[Getting Started](https://docs.mistral.ai/api/endpoint/chat)

- [Chat](https://docs.mistral.ai/api/endpoint/chat)
	- [postChat Completion
		](https://docs.mistral.ai/api/endpoint/chat#operation-chat_completion_v1_chat_completions_post)

- [Fim](https://docs.mistral.ai/api/endpoint/fim)

- [Embeddings](https://docs.mistral.ai/api/endpoint/embeddings)

- [Classifiers](https://docs.mistral.ai/api/endpoint/classifiers)

- [Files](https://docs.mistral.ai/api/endpoint/files)

- [Models](https://docs.mistral.ai/api/endpoint/models)

- [Batch](https://docs.mistral.ai/api/endpoint/batch)

- [Ocr](https://docs.mistral.ai/api/endpoint/ocr)

- [Audio Speech](https://docs.mistral.ai/api/endpoint/audio/speech)

- [Audio Transcriptions](https://docs.mistral.ai/api/endpoint/audio/transcriptions)

- [Audio Voices](https://docs.mistral.ai/api/endpoint/audio/voices)

[Beta](https://docs.mistral.ai/api/endpoint/beta/agents)

- [Beta Agents](https://docs.mistral.ai/api/endpoint/beta/agents)

- [Beta Conversations](https://docs.mistral.ai/api/endpoint/beta/conversations)

- [Beta Libraries](https://docs.mistral.ai/api/endpoint/beta/libraries)

- [Beta Libraries Accesses](https://docs.mistral.ai/api/endpoint/beta/libraries/accesses)

- [Beta Libraries Documents](https://docs.mistral.ai/api/endpoint/beta/libraries/documents)

- [Beta Observability Campaigns](https://docs.mistral.ai/api/endpoint/beta/observability/campaigns)

- [Beta Observability Chat Completion Events](https://docs.mistral.ai/api/endpoint/beta/observability/chat_completion_events)

- [Beta Observability Chat Completion Events Fields](https://docs.mistral.ai/api/endpoint/beta/observability/chat_completion_events/fields)

- [Beta Observability Datasets](https://docs.mistral.ai/api/endpoint/beta/observability/datasets)

- [Beta Observability Datasets Records](https://docs.mistral.ai/api/endpoint/beta/observability/datasets/records)

- [Beta Observability Judges](https://docs.mistral.ai/api/endpoint/beta/observability/judges)

- [Beta Workflows](https://docs.mistral.ai/api/endpoint/beta/workflows)

- [Beta Workflows Deployments](https://docs.mistral.ai/api/endpoint/beta/workflows/deployments)

- [Beta Workflows Events](https://docs.mistral.ai/api/endpoint/beta/workflows/events)

- [Beta Workflows Executions](https://docs.mistral.ai/api/endpoint/beta/workflows/executions)

- [Beta Workflows Metrics](https://docs.mistral.ai/api/endpoint/beta/workflows/metrics)

- [Beta Workflows Runs](https://docs.mistral.ai/api/endpoint/beta/workflows/runs)

- [Beta Workflows Schedules](https://docs.mistral.ai/api/endpoint/beta/workflows/schedules)

- [Beta Workflows Workers](https://docs.mistral.ai/api/endpoint/beta/workflows/workers)

[Deprecated](https://docs.mistral.ai/api/endpoint/deprecated/fine-tuning)

- [Deprecated Agents](https://docs.mistral.ai/api/endpoint/deprecated/agents)

- [Deprecated Fine Tuning](https://docs.mistral.ai/api/endpoint/deprecated/fine-tuning)

1. 3. [Getting Started](https://docs.mistral.ai/api/endpoint/chat)

5. Chat

![Tree BG 1](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftree_bg_1.b9f8245b.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Tree](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftree_bg_1.b9f8245b.png&w=2048&q=75&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Tree](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftree_bg_2.09077b6d.png&w=2048&q=75&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Tree](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftree_1.c6ea95c8.png&w=2048&q=75&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Leaves](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fleaves.fa5cdaf8.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Tree](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftree_2.ca9173eb.png&w=2048&q=75&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Leaves](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fleaves.fa5cdaf8.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Cat Idle](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcat_idle.da6d14d2.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Grass](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrass_tile.ce50c332.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Grass](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrass_tile.ce50c332.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Rock](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frock.c36c5495.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Rock](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frock.c36c5495.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Fireflies](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ffireflies.7a626bd6.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

# Chat Endpoints

Chat Completion API.

![Wall Assets](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fwall_assets.fb9d0a95.png&w=828&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Cat Frame](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcat_frame.7cd1d4d0.png&w=828&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Lamp](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flamp.21a6e807.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Cat Toy](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fcat_toy.99105b1f.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Lamp Light](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbookshelf.2e04e5b9.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Desk](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fdesk.11413025.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Chair](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fchair.e01257f7.png&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Orange Cat Idle](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Forange_cat_idle.a5f0da13.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

![Lamp Light](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flamp_light.5135bc3d.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Screen](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fanimated_screen.50ea99f4.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Screen Light](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fscreen_light.649888f0.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)![Lamp Light Large](https://docs.mistral.ai/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbig_light.12d015c4.gif&w=2048&q=100&dpl=dpl_AjYbtnG2tYf34cphnLgnMG7NbrAW)

### Examples

Real world code examples

Chat Completion

## **POST** /v1/chat/completions

##### frequency\_penalty

number

*Default Value:* `0`

The `frequency_penalty` penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.

##### guardrails

[array](#operation-chat_completion_v1_chat_completions_post_request_guardrails_guardrailconfig)<[GuardrailConfig](#operation-chat_completion_v1_chat_completions_post_request_guardrails_guardrailconfig)\>|null

##### max\_tokens

integer|null

The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.

##### messages

\*array<[SystemMessage](#operation-chat_completion_v1_chat_completions_post_request_messages_systemmessage)|[UserMessage](#operation-chat_completion_v1_chat_completions_post_request_messages_usermessage)|[AssistantMessage](#operation-chat_completion_v1_chat_completions_post_request_messages_assistantmessage)|[ToolMessage](#operation-chat_completion_v1_chat_completions_post_request_messages_toolmessage)\>

The prompt(s) to generate completions for, encoded as a list of dict with role and content.

##### metadata

map<any\>|null

##### model

\*string

ID of the model to use. You can use the [List Available Models](https://docs.mistral.ai/api#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](https://docs.mistral.ai/models) for model descriptions.

##### n

integer|null

Number of completions to return for each request, input tokens are only billed once.

##### parallel\_tool\_calls

boolean

*Default Value:* `true`

Whether to enable parallel function calling during tool use, when enabled the model can call multiple tools in parallel.

##### prediction

[Prediction](#operation-chat_completion_v1_chat_completions_post_request_prediction_prediction)|null

Enable users to specify an expected completion, optimizing response times by leveraging known or predictable content.

##### presence\_penalty

number

*Default Value:* `0`

The `presence_penalty` determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.

##### prompt\_mode

"reasoning"

Available options to the prompt\_mode argument on the chat completion endpoint. Values represent high-level intent. Assignment to actual SPs is handled internally. System prompt may include knowledge cutoff date, model capabilities, tone to use, safety guidelines, etc.

##### random\_seed

integer|null

The seed to use for random sampling. If set, different calls will generate deterministic results.

##### reasoning\_effort

"high"|"none"

Controls the reasoning effort level for reasoning models. "high" enables comprehensive reasoning traces, "none" disables reasoning effort.

##### response\_format

[ResponseFormat](#operation-chat_completion_v1_chat_completions_post_request_response_format_responseformat)|null

Specify the format that the model must output. By default it will use `\{ "type": "text" \}`. Setting to `\{ "type": "json_object" \}` enables JSON mode, which guarantees the message the model generates is in JSON. When using JSON mode you MUST also instruct the model to produce JSON yourself with a system or a user message. Setting to `\{ "type": "json_schema" \}` enables JSON schema mode, which guarantees the message the model generates is in JSON and follows the schema you provide.

##### safe\_prompt

boolean

*Default Value:* `false`

Whether to inject a safety prompt before all conversations.

##### stop

string|array<string\>

Stop generation if this token is detected. Or if one of these tokens is detected when providing an array

##### stream

boolean

*Default Value:* `false`

Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: \[DONE\] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

##### temperature

number|null

What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.

##### tool\_choice

[ToolChoice](#operation-chat_completion_v1_chat_completions_post_request_tool_choice_toolchoice)|"auto"|"none"|"any"|"required"

Controls which (if any) tool is called by the model. `none` means the model will not call any tool and instead generates a message. `auto` means the model can pick between generating a message or calling one or more tools. `any` or `required` means the model must call one or more tools. Specifying a particular tool via `\{"type": "function", "function": \{"name": "my_function"\}\}` forces the model to call that tool.

##### tools

[array](#operation-chat_completion_v1_chat_completions_post_request_tools_tool)<[Tool](#operation-chat_completion_v1_chat_completions_post_request_tools_tool)\>|null

##### top\_p

number

*Default Value:* `1`

Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.

200 (application/json)

200 (text/event-stream)

Successful Response

##### choices

\*[array](#operation-chat_completion_v1_chat_completions_post_responses_200_application-json_choices_chatcompletionchoice)<[ChatCompletionChoice](#operation-chat_completion_v1_chat_completions_post_responses_200_application-json_choices_chatcompletionchoice)\>

##### created

\*integer

##### id

\*string

##### model

\*string

##### object

\*string

##### usage

\*[UsageInfo](#operation-chat_completion_v1_chat_completions_post_responses_200_application-json_usage_usageinfo)

Response Type

[event-stream](#operation-chat_completion_v1_chat_completions_post_responses_completionevent)<[CompletionEvent](#operation-chat_completion_v1_chat_completions_post_responses_completionevent)\>

Successful Response

#### CompletionEvent

{object}

#### Playground

Test the endpoints **live**

```
import { Mistral } from "@mistralai/mistralai";

const mistral = new Mistral({
  apiKey: "MISTRAL_API_KEY",
});

async function run() {
  const result = await mistral.chat.complete({
    model: "mistral-small-latest",
    messages: [
      {
        content: "Who is the best French painter? Answer in one short sentence.",
        role: "user",
      },
    ],
  });

  console.log(result);
}

run();
```

```
import { Mistral } from "@mistralai/mistralai";

const mistral = new Mistral({
  apiKey: "MISTRAL_API_KEY",
});

async function run() {
  const result = await mistral.chat.complete({
    model: "mistral-small-latest",
    messages: [
      {
        content: "Who is the best French painter? Answer in one short sentence.",
        role: "user",
      },
    ],
  });

  console.log(result);
}

run();
```

```
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], stream=False)

    # Handle response
    print(res)
```

```
from mistralai import Mistral
import os

with Mistral(
    api_key=os.getenv("MISTRAL_API_KEY", ""),
) as mistral:

    res = mistral.chat.complete(model="mistral-small-latest", messages=[
        {
            "content": "Who is the best French painter? Answer in one short sentence.",
            "role": "user",
        },
    ], stream=False)

    # Handle response
    print(res)
```

```
curl https://api.mistral.ai/v1/chat/completions \
 -X POST \
 -H 'Authorization: Bearer YOUR_APIKEY_HERE' \
 -H 'Content-Type: application/json' \
 -d '{
  "messages": [
    {
      "content": "ipsum eiusmod"
    }
  ],
  "model": "mistral-large-latest"
}'
```

```
curl https://api.mistral.ai/v1/chat/completions \
 -X POST \
 -H 'Authorization: Bearer YOUR_APIKEY_HERE' \
 -H 'Content-Type: application/json' \
 -d '{
  "messages": [
    {
      "content": "ipsum eiusmod"
    }
  ],
  "model": "mistral-large-latest"
}'
```

200 (application/json)

200 (text/event-stream)

```
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": "0",
      "message": {}
    }
  ],
  "created": "1702256327",
  "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",
  "model": "mistral-small-latest",
  "object": "chat.completion",
  "usage": {}
}
```

```
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": "0",
      "message": {}
    }
  ],
  "created": "1702256327",
  "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",
  "model": "mistral-small-latest",
  "object": "chat.completion",
  "usage": {}
}
```

```
null
```

```
null
```

[Fim](https://docs.mistral.ai/api/endpoint/fim)

### WHY MISTRAL

[About us](https://mistral.ai/about)[Our customers](https://mistral.ai/customers)[Careers](https://mistral.ai/careers)[Contact us](https://mistral.ai/contact)

### EXPLORE

[AI Solutions](https://mistral.ai/solutions)[Partners](https://mistral.ai/partners)[Research](https://mistral.ai/news?category=Research)

### DOCUMENTATION

[Documentation](https://docs.mistral.ai/)[Ambassadors](https://docs.mistral.ai/community/ambassadors)[Cookbooks](https://docs.mistral.ai/resources/cookbooks)

### BUILD

[Studio](https://console.mistral.ai/)[Mistral Vibe](https://mistral.ai/products/vibe)[Mistral Code](https://mistral.ai/products/mistral-code)[Mistral Compute](https://mistral.ai/products/mistral-compute)[Try the API](https://docs.mistral.ai/api)

### LEGAL

[Terms of service](https://mistral.ai/terms)[Privacy policy](https://mistral.ai/terms#privacy-policy)[Legal notice](https://mistral.ai/legal)[Brand](https://mistral.ai/brand)

### COMMUNITY

[Discord↗](https://discord.gg/mistralai)[X↗](https://x.com/mistralai)[Github↗](https://github.com/mistralai)[LinkedIn↗](https://linkedin.com/company/mistralai)[Ambassadors](https://docs.mistral.ai/community/ambassadors)

Mistral AI © 2026

![Sun](https://docs.mistral.ai/assets/sprites/sun.gif)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)![Grass](https://docs.mistral.ai/_next/image?url=%2Fassets%2Fsprites%2Fgrass_tile.png&w=640&q=75)

![Cat](https://docs.mistral.ai/assets/sprites/cat-walking-white.gif)