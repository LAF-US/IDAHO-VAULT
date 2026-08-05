---
title: "Introducing Whisper"
source: "https://openai.com/index/whisper/"
author:
published: 2022-04-13
created: 2026-04-27
description:
tags:
  - "clippings"
---
Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. We show that the use of such a large and diverse dataset leads to improved robustness to accents, background noise and technical language. Moreover, it enables transcription in multiple languages, as well as translation from those languages into English. We are open-sourcing models and inference code to serve as a foundation for building useful applications and for further research on robust speech processing.

![ASR Summary Of Model Architecture](https://images.ctfassets.net/kftzwdyauwt9/d9c13138-366f-49d3-a1a563abddc1/8acfb590df46923b021026207ff1a438/asr-summary-of-model-architecture-desktop.svg?w=3840&q=90)

The Whisper architecture is a simple end-to-end approach, implemented as an encoder-decoder Transformer. Input audio is split into 30-second chunks, converted into a log-Mel spectrogram, and then passed into an encoder. A decoder is trained to predict the corresponding text caption, intermixed with special tokens that direct the single model to perform tasks such as language identification, phrase-level timestamps, multilingual speech transcription, and to-English speech translation.

Other existing approaches frequently use smaller, more closely paired audio-text training datasets,[^1],[^2] or use broad but unsupervised audio pretraining.,,[^4] Because Whisper was trained on a large and diverse dataset and was not fine-tuned to any specific one, it does not beat models that specialize in LibriSpeech performance, a famously competitive benchmark in speech recognition. However, when we measure Whisper’s zero-shot performance across many diverse datasets we find it is much more robust and makes 50% fewer errors than those models.

About a third of Whisper’s audio dataset is non-English, and it is alternately given the task of transcribing in the original language or translating to English. We find this approach is particularly effective at learning speech to text translation and outperforms the supervised SOTA on CoVoST2 to English translation zero-shot.

![](https://images.ctfassets.net/kftzwdyauwt9/29f82291-67a2-491f-3cf6180c16fd/d0d5a05fa5d3f801db92285328bda70e/asr-training-data-mobile.svg)

ASR training data inputs and outputs

We hope Whisper’s high accuracy and ease of use will allow developers to add voice interfaces to a much wider set of applications. Check out the [paper⁠](https://cdn.openai.com/papers/whisper.pdf), [model card⁠](https://github.com/openai/whisper/blob/main/model-card.md), and [code⁠](https://github.com/openai/whisper) to learn more details and to try out Whisper.

[^1]: 1

Chan, W., Park, D., Lee, C., Zhang, Y., Le, Q., and Norouzi, M. SpeechStew: Simply mix all available speech recogni- tion data to train one large neural network. [arXiv preprint arXiv:2104.02133, 2021⁠](https://arxiv.org/abs/2104.02133).

[^2]: 2

Galvez, D., Diamos, G., Torres, J. M. C., Achorn, K., Gopi, A., Kanter, D., Lam, M., Mazumder, M., and Reddi, V. J. The people’s speech: A large-scale diverse english speech recognition dataset for commercial usage. [arXiv preprint arXiv:2111.09344, 2021⁠](https://arxiv.org/abs/2111.09344).

[^3]: 3

Chen, G., Chai, S., Wang, G., Du, J., Zhang, W.-Q., Weng, C., Su, D., Povey, D., Trmal, J., Zhang, J., et al. Gigaspeech: An evolving, multi-domain asr corpus with 10,000 hours of transcribed audio. [arXiv preprint arXiv:2106.06909, 2021⁠](https://arxiv.org/abs/2106.06909).

[^4]: 4

Baevski, A., Zhou, H., Mohamed, A., and Auli, M. wav2vec 2.0: A framework for self-supervised learning of speech representations. [arXiv preprint arXiv:2006.11477, 2020⁠](https://arxiv.org/abs/2006.11477).

[^5]: 5

Baevski, A., Hsu, W.N., Conneau, A., and Auli, M. Unsu pervised speech recognition. Advances in Neural Information Processing Systems, 34:27826–27839, 2021.

[^6]: 6

Zhang, Y., Park, D. S., Han, W., Qin, J., Gulati, A., Shor, J., Jansen, A., Xu, Y., Huang, Y., Wang, S., et al. BigSSL: Exploring the frontier of large-scale semi-supervised learning for automatic speech recognition. [arXiv preprint arXiv:2109.13226, 2021⁠](https://arxiv.org/abs/2109.13226).