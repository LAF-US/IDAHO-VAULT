---
title: "ElevenAgents"
source: "https://elevenlabs.io/docs/eleven-agents/overview"
author:
published:
created: 2026-04-15
description: "Learn how to build, launch, and scale agents with ElevenLabs."
date created: Wednesday, April 15th 2026, 9:05:35 pm
date modified: Wednesday, April 15th 2026, 9:06:19 pm
---

Agents accomplish tasks through natural dialogue - from quick requests to complex, open-ended workflows. ElevenLabs provides voice-rich, expressive models, developer tools for building multimodal agents, and tools to monitor and evaluate agent performance at scale.

## Platform capabilities

From design to deployment to optimization, ElevenLabs provides everything you need to build agents at scale.

### Design and configure

| Goal | Guide | Description |
| --- | --- | --- |
| Create conversation workflows | [Workflows](https://elevenlabs.io/docs/eleven-agents/customization/agent-workflows) | Build multi-step workflows with visual workflow builder |
| Write system prompts | [System prompt](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide) | Learn best practices for crafting effective agent prompts |
| Select language model | [Models](https://elevenlabs.io/docs/eleven-agents/customization/llm) | Choose from supported LLMs or bring your own custom model |
| Control conversation flow | [Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow) | Configure turn-taking, interruptions, and timeout settings |
| Configure voice & language | [Voice & language](https://elevenlabs.io/docs/eleven-agents/customization/voice) | Select from 5k+ voices across 31 languages with customization options |
| Add knowledge to agent | [Knowledge base](https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base) | Upload documents and enable RAG for grounded responses |
| Connect tools | [Tools](https://elevenlabs.io/docs/eleven-agents/customization/tools) | Enable agents to call clients & APIs to perform actions |
| Personalize each conversation | [Personalization](https://elevenlabs.io/docs/eleven-agents/customization/personalization) | Use dynamic variables and overrides for per-conversation customization |
| Secure agent access | [Authentication](https://elevenlabs.io/docs/eleven-agents/customization/authentication) | Implement custom authentication for protected agent access |

### Connect and deploy

| Goal | Guide | Description |
| --- | --- | --- |
| Build with React components | [ElevenLabs UI](https://ui.elevenlabs.io/) | Pre-built components library for audio & agent apps (shadcn-based) |
| Embed widget in website | [Widget](https://elevenlabs.io/docs/eleven-agents/customization/widget) | Add a customizable web widget to any website |
| Build React web apps | [React SDK](https://elevenlabs.io/docs/eleven-agents/libraries/react) | Voice-enabled React hooks and components |
| Build iOS apps | [Swift SDK](https://elevenlabs.io/docs/eleven-agents/libraries/swift) | Native iOS SDK for voice agents |
| Build Android apps | [Kotlin SDK](https://elevenlabs.io/docs/eleven-agents/libraries/kotlin) | Native Android SDK for voice agents |
| Build React Native apps | [React Native SDK](https://elevenlabs.io/docs/eleven-agents/libraries/react-native) | Cross-platform iOS and Android with React Native |
| Connect via SIP trunk | [SIP trunk](https://elevenlabs.io/docs/eleven-agents/phone-numbers/sip-trunking) | Integrate with existing telephony infrastructure |
| Make batch outbound calls | [Batch calls](https://elevenlabs.io/docs/eleven-agents/phone-numbers/batch-calls) | Trigger multiple calls programmatically |
| Use Twilio integration | [Twilio](https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration) | Native Twilio integration for phone calls |
| Build custom integrations | [WebSocket API](https://elevenlabs.io/docs/eleven-agents/libraries/web-sockets) | Low-level WebSocket protocol for custom implementations |
| Receive real-time events | [Events](https://elevenlabs.io/docs/eleven-agents/customization/events) | Subscribe to conversation events and updates |

### Monitor and optimize

| Goal | Guide | Description |
| --- | --- | --- |
| List users by external ID | [Users](https://elevenlabs.io/docs/eleven-agents/operate/users) | See end users and open their conversations |
| Search transcripts | [Searching conversations](https://elevenlabs.io/docs/eleven-agents/customization/agent-analysis/smart-search) | Keyword and semantic search in Conversation history |
| Run A/B tests | [Experiments](https://elevenlabs.io/docs/eleven-agents/operate/experiments) | Test agent configuration changes with live traffic |
| Test agent behavior | [Testing](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing) | Create and run automated tests for your agents |
| Analyze conversation quality | [Conversation analysis](https://elevenlabs.io/docs/eleven-agents/customization/agent-analysis) | Extract insights and evaluate conversation outcomes |
| Track metrics & analytics | [Analytics](https://elevenlabs.io/docs/eleven-agents/dashboard) | Monitor performance metrics and conversation history |
| Configure data retention | [Privacy](https://elevenlabs.io/docs/eleven-agents/customization/privacy) | Set retention policies for conversations and audio |
| Reduce LLM costs | [Cost optimization](https://elevenlabs.io/docs/eleven-agents/customization/llm/optimizing-costs) | Monitor and optimize language model expenses |

## Architecture

ElevenAgents coordinates 4 core components:

1. A fine-tuned Speech to Text (ASR) model for speech recognition
2. Your choice of language model or [custom](https://elevenlabs.io/docs/eleven-agents/customization/llm/custom-llm) LLM
3. A low-latency Text to Speech (TTS) model across 5k+ voices and 70+ languages
4. A proprietary turn-taking model that handles conversation timing[Quickstart](https://elevenlabs.io/docs/eleven-agents/quickstart)

[

Build your first agent in 5 minutes

](https://elevenlabs.io/docs/eleven-agents/quickstart)