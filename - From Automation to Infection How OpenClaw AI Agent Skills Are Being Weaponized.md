---
title: "From Automation to Infection: How OpenClaw AI Agent Skills Are Being Weaponized"
source: "https://blog.virustotal.com/2026/02/from-automation-to-infection-how.html"
author:
  - "[[Bernardo.Quintero]]"
published:
created: 2026-04-28
description: "The fastest-growing personal AI agent ecosystem just became a new delivery channel for malware. Over the last few days, VirusTotal has detec..."
date created: Tuesday, April 28th 2026, 6:25:56 pm
date modified: Tuesday, April 28th 2026, 6:26:05 pm
---

The fastest-growing personal AI agent ecosystem just became a new delivery channel for malware. Over the last few days, VirusTotal has detected hundreds of OpenClaw skills that are actively malicious. What started as an ecosystem for extending AI agents is rapidly becoming a new supply-chain attack surface, where attackers distribute droppers, backdoors, infostealers and remote access tools disguised as helpful automation.

**What is OpenClaw (formerly Clawdbot / Moltbot)?**

Unless you’ve been completely disconnected from the internet lately, you’ve probably heard about the viral success of OpenClaw and its small naming soap opera. What started as Clawdbot, briefly became Moltbot, and finally settled on OpenClaw, after a trademark request made the original name off-limits.

At its core, OpenClaw is a self-hosted AI agent that runs on your own machine and can execute real actions on your behalf: shell commands, file operations, network requests. Which is exactly why it’s powerful, and also why, unless you actively sandbox it, the security blast radius is basically your entire system.

**Skills: powerful by design, dangerous by default**

OpenClaw skills are essentially small packages that extend what the agent can do. Each skill is built around a SKILL.md file (with some metadata and instructions) and may include scripts or extra resources. Skills can be loaded locally, but most users discover and install them from ClawHub, the public marketplace for OpenClaw extensions.

This is what makes the ecosystem so powerful: instead of hardcoding everything into the agent, you just add skills and suddenly it can use new tools, APIs, and workflows. The agent reads the skill documentation on demand and follows its instructions.

The problem is that skills are also third-party code, running in an environment with real system access. And many of them come with “setup” steps users are trained to trust: paste this into your terminal, download this binary and run it, export these environment variables. From an attacker’s perspective, it’s a perfect social-engineering layer.

So yes, skills are a gift for productivity and, unsurprisingly, a gift for malware authors too. Same mechanism, very different intentions.

**What we added: OpenClaw Skill support in VirusTotal Code Insight**

To help detect this emerging abuse pattern, we’ve added native support in VirusTotal Code Insight for OpenClaw skill packages, including skills distributed as ZIP files. Under the hood, we use Gemini 3 Flash to perform a fast security-focused analysis of the entire skill, starting from SKILL.md and including any referenced scripts or resources.

The goal is not to understand what the skill claims to do, but to summarize what it actually does from a security perspective: whether it downloads and executes external code, accesses sensitive data, performs network operations, or embeds instructions that could coerce the agent into unsafe behavior. In practice, this gives analysts a concise, security-first description of the real behavior of a skill, making it much easier to spot malicious patterns hidden behind “helpful” functionality.

**What we’re seeing in the wild**

At the time of writing, VirusTotal Code Insight has already analyzed more than 3,016 OpenClaw skills, and hundreds of them show malicious characteristics.

Not all of these cases are the same. On one side, we are seeing many skills flagged as dangerous because they contain poor security practices or outright vulnerabilities: insecure use of APIs, unsafe command execution, hardcoded secrets, excessive permissions, or sloppy handling of user input. This is increasingly common in the era of vibe coding, where code is generated quickly, often without a real security model, and published straight into production.

But more worrying is the second group: skills that are clearly and intentionally malicious. These are presented as legitimate tools, but their real purpose is to perform actions such as sensitive data exfiltration, remote control via backdoors, or direct malware installation on the host system.

**Case study: hightower6eu, a malware publisher in plain sight**

One of the most illustrative cases we’ve observed is the ClawHub user "hightower6eu", who is highly active publishing skills that appear legitimate but are consistently used to deliver malware

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj5OZPa_Mi_Q1N-Ezy0JITx652S3vwrz-zkVDJgNcQUosVNrqddfe2YG5OXQfzH6Ie1CTmYxRw5XMPJmBsyx1of5RRsy495IGEq2nQ1baxnFTb4jJziuJE6_-p-AKnW-hw8hZ1xHFLlZSr6u4YeV4tqsc7Dautsww4j3Fdl4ulVpTyBQjU_O9BlVxNFI7c/s1600/hightower6eu.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj5OZPa_Mi_Q1N-Ezy0JITx652S3vwrz-zkVDJgNcQUosVNrqddfe2YG5OXQfzH6Ie1CTmYxRw5XMPJmBsyx1of5RRsy495IGEq2nQ1baxnFTb4jJziuJE6_-p-AKnW-hw8hZ1xHFLlZSr6u4YeV4tqsc7Dautsww4j3Fdl4ulVpTyBQjU_O9BlVxNFI7c/s1600/hightower6eu.png)

  

At the time of writing, VirusTotal Code Insight has already analyzed 314 skills associated with this single user, and the number is still growing, all of them identified as malicious. The skills cover a wide range of apparently harmless use cases (crypto analytics, finance tracking, social media analysis, auto-updaters, etc) but they all follow a similar pattern: users are instructed to download and execute external code from untrusted sources as part of the "setup" process.

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh1OIrjT4EcVhVwh4xx_eRdp0oZ92KFKcQm49ihoTF_c6VHynFu-CKtmtLonQlth74dS3KFZzL0sKnYoJw9MsoCNE5bMphzn2vTRFQVH4x-4Ld6nNHavNgBuso-IYpcuxOk_mbzbqoc7p36kKDa4uWNxakCLUk6f6zr_v4fcwVrKgeWJBpaUz5FXwd52iI/s1600/314.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh1OIrjT4EcVhVwh4xx_eRdp0oZ92KFKcQm49ihoTF_c6VHynFu-CKtmtLonQlth74dS3KFZzL0sKnYoJw9MsoCNE5bMphzn2vTRFQVH4x-4Ld6nNHavNgBuso-IYpcuxOk_mbzbqoc7p36kKDa4uWNxakCLUk6f6zr_v4fcwVrKgeWJBpaUz5FXwd52iI/s1600/314.png)

  

To make this more tangible, the screenshot below shows how VirusTotal Code Insight analyzes one of the skills published by hightower6eu, in this case a seemingly harmless skill called "Yahoo Finance".

On the surface, the file looks clean: no antivirus engines flag it as malicious, and the ZIP itself contains almost no real code. This is exactly why traditional detection fails.

VT Code Insight, however, looks at the actual behavior described in the skill. In this case, it identifies that the skill instructs users to download and execute external code from untrusted sources as a mandatory prerequisite, both on Windows and macOS. From a security perspective, that’s a textbook malware delivery pattern: the skill acts as a social engineering wrapper whose only real purpose is to push remote execution. In other words, nothing in the file is technically "malware" by itself. The malware is the workflow. And that’s precisely the kind of abuse pattern Code Insight is designed to surface.

  

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHylmJ2Kc0sMz_1xCFVxpI4PCEr7I7ufQksfY3_3FbYwYr_prgAAOaBfpQbAJP1wHc6kZx_NUd4x_HYEgsJ0uVPiMxF91fUjXWyev73vx6H1ND7l-dqpDU8nCOrwIoQhGDp4eG_qt2_sKsna_2WcYPpBYRXbRDf31U-_odUwkxnNvQgZwmI7PC_xM-HRk/s1600/yahoo-finance.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgHylmJ2Kc0sMz_1xCFVxpI4PCEr7I7ufQksfY3_3FbYwYr_prgAAOaBfpQbAJP1wHc6kZx_NUd4x_HYEgsJ0uVPiMxF91fUjXWyev73vx6H1ND7l-dqpDU8nCOrwIoQhGDp4eG_qt2_sKsna_2WcYPpBYRXbRDf31U-_odUwkxnNvQgZwmI7PC_xM-HRk/s1600/yahoo-finance.png)

[79e8f3f7a6113773cdbced2c7329e6dbb2d0b8b3bf5a18c6c97cb096652bc1f2](https://www.virustotal.com/gui/file/79e8f3f7a6113773cdbced2c7329e6dbb2d0b8b3bf5a18c6c97cb096652bc1f2)

  

If you actually read the SKILL.md, the real behavior becomes obvious. For Windows users, the skill instructs them to download a ZIP file from an external GitHub account, protected with the password 'openclaw', extract it, and run the contained executable: openclaw-agent.exe.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnRE3b4D0yI_wScKr61F_glYjX4GdUZ8mNPyGDdmFR4Vp6XjAV9XVA06McHMHLIzBhyphenhyphenU0EUGTosfz911qKNHTl5-sMAUmN7__yEXmn0kgWgjj4yEcLJUTgqrMp5EGI8eINmjxaIkFNCwDkF0WPeavAljBxTr4lvpP-DsFJr8U-I3N2XNsd8O5lTEaZG2U/s1600/skill-md.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgnRE3b4D0yI_wScKr61F_glYjX4GdUZ8mNPyGDdmFR4Vp6XjAV9XVA06McHMHLIzBhyphenhyphenU0EUGTosfz911qKNHTl5-sMAUmN7__yEXmn0kgWgjj4yEcLJUTgqrMp5EGI8eINmjxaIkFNCwDkF0WPeavAljBxTr4lvpP-DsFJr8U-I3N2XNsd8O5lTEaZG2U/s1600/skill-md.png)

  

When submitted to VirusTotal, this executable is detected as malicious by multiple security vendors, with classifications consistent with packed trojans.

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj_g1v215lYxt8ywYR5E5S7H1JRpglLoOr8Bw89X2_mqav0uoMfwW0V1xA0Q9zZ-w8fggJxgTaFN1Vvw3nEPrAIE4y1eZg6CDD2cfxKXai4tLRfOnR9U-AUWhHqbAUALnH2ZpeyXScEbgm-aR-wMGqHy9UgTSmidB3slVEsxsEs5_RQawXJqjxmcqtJgEM/s1600/18.windows.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj_g1v215lYxt8ywYR5E5S7H1JRpglLoOr8Bw89X2_mqav0uoMfwW0V1xA0Q9zZ-w8fggJxgTaFN1Vvw3nEPrAIE4y1eZg6CDD2cfxKXai4tLRfOnR9U-AUWhHqbAUALnH2ZpeyXScEbgm-aR-wMGqHy9UgTSmidB3slVEsxsEs5_RQawXJqjxmcqtJgEM/s1600/18.windows.png)

[17703b3d5e8e1fe69d6a6c78a240d8c84b32465fe62bed5610fb29335fe42283](https://www.virustotal.com/gui/file/17703b3d5e8e1fe69d6a6c78a240d8c84b32465fe62bed5610fb29335fe42283)

  

When the system is macOS, the skill doesn't provide a binary directly. Instead, it points the user to a shell script hosted on glot.io, which is obfuscated using Base64:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6GzKt5UawAWhU1TpAvDBiUB-Q416X-ZjEEyeVKJURAtty4WItQ5GlMqzK-ymQM8d_55F269nykBCLTbCfa4dbmg45-da5H0s9SoanmAzehFcH_UcOp2bVgubFp3JG2jic3PCuGIQSZRQS-pUTIEcblRS_lek_Uqn1AjI2TLtbY4q0Qu_B0ZmrW_MCId4/s1600/glotio.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg6GzKt5UawAWhU1TpAvDBiUB-Q416X-ZjEEyeVKJURAtty4WItQ5GlMqzK-ymQM8d_55F269nykBCLTbCfa4dbmg45-da5H0s9SoanmAzehFcH_UcOp2bVgubFp3JG2jic3PCuGIQSZRQS-pUTIEcblRS_lek_Uqn1AjI2TLtbY4q0Qu_B0ZmrW_MCId4/s1600/glotio.png)

  

Once the Base64 payload is decoded, the real behavior becomes visible: the script simply downloads and executes another file from a remote server over plain HTTP:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5iCu_OYQQS2AB2TmwODuwI-bx_P177W2txs9l6ymeMfOFSoxo7ii1lgFkUlTfH-soXhfJL8GRwBKlicQhZRFolWguzhBF867P4HIdr_DXJ5pko5Fa5GC6iaRuTVUeWbqWvRt99YsdYGrkoOC1ruoTv_jTI8IbNU67nvSG0-wNFpFt3ZLtfTinUArc0wU/s1600/plainhttp.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5iCu_OYQQS2AB2TmwODuwI-bx_P177W2txs9l6ymeMfOFSoxo7ii1lgFkUlTfH-soXhfJL8GRwBKlicQhZRFolWguzhBF867P4HIdr_DXJ5pko5Fa5GC6iaRuTVUeWbqWvRt99YsdYGrkoOC1ruoTv_jTI8IbNU67nvSG0-wNFpFt3ZLtfTinUArc0wU/s1600/plainhttp.png)

  

The final stage is the file x5ki60w1ih838sp7, a Mach-O executable. When submitted to VirusTotal, this binary is detected as malicious by 16 security engines, with classifications consistent with stealer trojans and generic malware families:

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicZm08uNdzuDd8vASK7TSTxvQ1lxtxtGdeyFCmjqRLeXzI0KFHfqt1Wn-9BoTfmCNb2xeapm8AFj0tJOXi9DdxpRgPPJlbjBBxADlYNmoz9JcUTz0ZaLqPxcRGMku_I10bUXxsE_sE7w9FZi93hGO6R4WRS6XNaejhSwoS0nUibINTgD86lQjQrznCi9M/s1600/16-macos.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicZm08uNdzuDd8vASK7TSTxvQ1lxtxtGdeyFCmjqRLeXzI0KFHfqt1Wn-9BoTfmCNb2xeapm8AFj0tJOXi9DdxpRgPPJlbjBBxADlYNmoz9JcUTz0ZaLqPxcRGMku_I10bUXxsE_sE7w9FZi93hGO6R4WRS6XNaejhSwoS0nUibINTgD86lQjQrznCi9M/s1600/16-macos.png)

[1e6d4b0538558429422b71d1f4d724c8ce31be92d299df33a8339e32316e2298](https://www.virustotal.com/gui/file/1e6d4b0538558429422b71d1f4d724c8ce31be92d299df33a8339e32316e2298)

  

When the file is analyzed by multiple automated reversing tools and Gemini 3 Pro, the results are consistent: the binary is identified as a trojan infostealer, and more specifically as a variant of Atomic Stealer (AMOS).

[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjM4jQhwUiyl9wl5PHcEUPiKlNE04Wmbmm3UV-ufPROvy1XdQ6ciXNso3r8xiqfrRDBy8xOCZUJBMseUYKL9RnJ26fQlVHpylaxTOWiUOruWLpilJpY-Ohjj1FjQlBTjqTmlwnPdVDgUOPGOitQ8OBsAA2Hlc1cv5QV1MyzvvUMtJvvxifd_qnOM3lLQ7g/s1600/omniasec-amos.png)](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjM4jQhwUiyl9wl5PHcEUPiKlNE04Wmbmm3UV-ufPROvy1XdQ6ciXNso3r8xiqfrRDBy8xOCZUJBMseUYKL9RnJ26fQlVHpylaxTOWiUOruWLpilJpY-Ohjj1FjQlBTjqTmlwnPdVDgUOPGOitQ8OBsAA2Hlc1cv5QV1MyzvvUMtJvvxifd_qnOM3lLQ7g/s1600/omniasec-amos.png)

  

This family of malware is well known in the macOS ecosystem. It is designed to run stealthily in the background and systematically harvest sensitive user data, including system and application passwords, browser cookies and stored credentials, and cryptocurrency wallets and related artifacts.

**What OpenClaw users (and platforms) should do right now**

OpenClaw itself provides reasonable security building blocks, but they only help if people actually use them:

- Treat skill folders as trusted-code boundaries and strictly control who can modify them.
- Prefer sandboxed executions and keep agents away from sensitive credentials and personal data.
- Be extremely skeptical of any skill that requires pasting commands into a shell or running downloaded binaries.
- If you operate a registry or marketplace, add publish-time scanning and flag skills that include remote execution, obfuscated scripts, or instructions designed to bypass user oversight.

And if you’re installing community skills: scan them first. For personal AI agents, the supply chain is not a detail, it’s the whole product.

Finally, we want to give full credit to Peter Steinberger, the creator of OpenClaw, for the success, traction, and energy around the project. From our side, we’d love to collaborate and explore ways to integrate VirusTotal directly into the OpenClaw publishing and review workflow, so that developers and users can benefit from security analysis without getting in the way of innovation.