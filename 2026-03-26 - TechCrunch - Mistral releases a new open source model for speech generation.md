---
source: "https://techcrunch.com/2026/03/26/mistral-releases-a-new-open-source-model-for-speech-generation/"
author:
  - "[[Ivan Mehta]]"
published: 2026-03-26
created: 2026-04-17
---
French AI company Mistral released a new open source text-to-speech model on Thursday that can be used by voice AI assistants or in enterprise use cases like customer support. The model, which lets enterprises build voice agents for sales and customer engagement, puts Mistral in direct competition with the likes of ElevenLabs, Deepgram, and OpenAI.

The new model, called Voxtral TTS, supports nine languages, including English, French, German, Spanish, Dutch, Portuguese, Italian, Hindi, and Arabic.

“Our customers have been asking for a speech model. So we built a small-sized speech model that can fit on a smartwatch, a smartphone, a laptop, or other edge devices. The cost of it is a fraction of anything else on the market, but it offers state-of-the-art performance,” Pierre Stock, VP of science operations at Mistral AI, told TechCrunch during a phone interview.

![](https://techcrunch.com/wp-content/uploads/2026/03/9de9713a-6b03-4007-9fb1-6fce3a9cb0d9.jpeg)

Image Credits: Mistral

Mistral said the new model can adapt a custom voice with a sample of less than five seconds and can capture characteristics like subtle accents, inflections, intonations, and irregularities in the flow of speech. The model, based on [Ministral](https://docs.mistral.ai/models/ministral-3-3b-25-12) [3B](https://docs.mistral.ai/models/ministral-3-3b-25-12), can switch between languages easily without losing the characteristics of the voice, which is useful for use cases like dubbing or real-time translation. Stock said the company wanted the model to sound human and not robotic.

![](https://www.youtube.com/watch?v=_N-ZGjGSVls)

The model has been built for real-time performance, according to the company. It has a time-to-first-audio (TTFA) — a measure of when the model starts “speaking” after receiving input — of 90 ms for a 10-second sample of 500 characters. The model also has a real-time factor (RTF) of 6x, which means it can render a 10-second clip in roughly 1.6 seconds.

![](https://techcrunch.com/wp-content/uploads/2026/03/1cc0ce97-f6f1-477a-8c25-23ca793d0571.jpeg)

Image Credits: Mistral AI

Earlier this year, Mistral launched [a pair of transcription models](https://mistral.ai/news/voxtral-transcribe-2), one for large batch processing and the other for real-time use cases with low latency. With the new speech model, the company is likely aiming to provide a full suite of voice products to enterprises.

“We plan to have an end-to-end platform that can handle multimodal streams of input, including audio, text, and image and output as well. The main benefit of that is you get way more information with an end-to-end agentic system that supports audio as an input or output,” Stock said.

Mistral’s positioning is that its open source and customization bit will help enterprises adopt its voice models over competitors, as they can tune it the way they want.