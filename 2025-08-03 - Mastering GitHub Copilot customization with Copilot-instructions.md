---
title: "Mastering GitHub Copilot customization with Copilot-instructions"
source: "https://medium.com/@frank.laule/mastering-github-copilot-customization-with-copilot-instructions-83e8cc1ca10a"
author:
  - "[[Frank Laule]]"
published: 2025-08-03
created: 2026-06-03
description: "Tired of generic AI code suggestions? With just a few Markdown files, you can teach GitHub Copilot to follow your team’s coding standards, a"
date created: Wednesday, June 3rd 2026, 2:27:15 pm
date modified: Wednesday, June 3rd 2026, 2:28:19 pm
---

<<<<<<< HEAD
**Tired of generic AI code suggestions?** With just a few Markdown files, you can teach GitHub Copilot to follow your team’s coding standards, architectural preferences, and even automate repetitive tasks. In this guide, you’ll learn how to transform Copilot into a truly personalized coding partner — right inside VS Code.
=======
> **SOURCE ATTRIBUTION**  
> This content is a web-clipped excerpt from Frank Laule's Medium article "Mastering GitHub Copilot customization with Copilot-instructions" (https://medium.com/@frank.laule/mastering-github-copilot-customization-with-copilot-instructions-83e8cc1ca10a).  
> Clipped for reference and internal documentation purposes. Original work maintains its own license terms; refer to the source for licensing details.

**Tired of generic AI code suggestions?** With just a few Markdown files, you can teach GitHub
Copilot to follow your team’s coding standards, architectural preferences, and even automate
repetitive tasks. In this guide, you’ll learn how to transform Copilot into a truly personalized
coding partner — right inside VS Code.
>>>>>>> 876899f2f (Add source attribution notices to web-clipped content)

## Global Project-Level Instructions

<<<<<<< HEAD
<<<<<<< HEAD
\`copilot-instructions.md\` - This Markdown file lives inside the \`.github/\` folder of your repository and defines general guidelines Copilot should follow across the entire project. Global instructions ensure every developer and every Copilot suggestion follows your team’s standards, no matter the file or task.
=======
\`.copilot-instructions.md\` - This Markdown file lives inside `.github/` folder of your repository
=======
\`.github/copilot-instructions.md\` - This Markdown file lives inside the `.github/` folder of your repository
>>>>>>> 226d35e94 (Address additional Copilot review comments on PR #820)
and defines general guidelines Copilot should follow across the entire project. Global instructions
ensure every developer and every Copilot suggestion follows your team’s standards, no matter the
file or task.
>>>>>>> 9899939db (Address Copilot review comments on PR #820)

**Key Features:**

- Automatically applied to every Copilot chat and code suggestion in the workspace.
- Ideal for specifying architecture preferences, libraries, frameworks, and coding conventions.
- Works across VS Code, Visual Studio, GitHub.com, and other Copilot-supported tools.

**Example:**

```c
## Project Preferences
- Use TypeScript and React.
- Apply Tailwind CSS for styling.
- Ensure all components support accessibility.
- Use atomic design patterns.
```

### Context-Specific Configurations

Want to go beyond global settings and tailor Copilot’s behavior per file type, folder or task? This is where \`.instructions.md\` files shine.

**Highlights:**

- Stored under \`.github/instructions/\` or in your VS Code user profile.
- Supports YAML frontmatter to define scope (applyTo) and description.
- Can be manually attached to a Copilot chat or automatically triggered based on file patterns.

**Example Header:**

```c
---
applyTo: "**/*.ts"
description: "TypeScript-specific guidelines"
---
```

**Instruction Body:**

```c
- Always use \`interface\` over \`type\` for definitions.
- Prefer \`const\` wherever possible.
- Enable strict null checks in all modules.
```

### Prompt Files

Prompt files are Markdown files that define specific tasks or queries for Copilot to address. They can be stored in the \`.github/prompts/\` directory and are designed to be reusable across different projects. You can select these prompts in the Copilot sidebar or reference them in chat.

Example prompt file structure:

```c
# Architecture Blueprint Generator
Generate a high-level architecture blueprint for a web application using microservices.
- Use Node.js for the backend services.
- Use React for the frontend.
- Include a database schema using PostgreSQL.
- Ensure the architecture supports scalability and fault tolerance.
```

### Chat Modes

Chat modes allow you to define specific interaction styles for Copilot, such as focusing on API design or code review. These modes can be stored in the \`.github/chatmodes/\` directory.

## Get Frank Laule’s stories in your inbox

Join Medium for free to get updates from this writer.

Example:

```c
--description: 'Your role is that of an API architect. Help mentor the engineer by providing guidance, support, and working code.'

# API Architect mode instructions

- Provide guidance on API design principles.
- Suggest best practices for RESTful API development.
- Review API specifications and provide feedback.
```

### Configuration in VS Code

If you don’t see these settings, make sure you have the latest Copilot extension installed.

To enable Copilot customization in Visual Studio Code, you need to ensure the following settings are configured:

1\. Open your VS Code settings (File > Preferences > Settings).

2\. Search for “Copilot” and ensure the following settings are enabled:

<<<<<<< HEAD
![VS Code Copilot settings panel showing the instructions options enabled](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*L0Vv0AxeagWmZ7iqtWJZNQ.png)

VS Code Copilot settings: Enable these options for instructions

![VS Code Copilot settings panel showing the prompts options enabled](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ETIoGGeLrWsL9NHpb88nMA.png)
=======
![VS Code Copilot settings: Enable these options for instructions](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*L0Vv0AxeagWmZ7iqtWJZNQ.png)

VS Code Copilot settings: Enable these options for instructions

![VS Code Copilot settings: Enable these options for prompts](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ETIoGGeLrWsL9NHpb88nMA.png)
>>>>>>> 9899939db (Address Copilot review comments on PR #820)

VS Code Copilot settings: Enable these options for prompts

### Sample Folder Structure

Organize your repository like this for maximum clarity and reusability.

```c
REPO-FOLDER/
├── .github/
│   └── copilot-instructions.md
│   └── chatmodes/
│   │   ├── api-architect.chatmode.md
│   │   ├── ...
│   ├── instructions/
│   │   ├── bicep-code-best-practices.instructions.md
│   │   ├── dotnet-architecture-good-practices.instructions.md
│   │   ├── ...
│   ├── prompts/
│   │   ├── architecture-blueprint-generator.prompt.md
│   │   ├── csharp-async.prompt.md
│   │   ├── javascript-typescript-jest.prompt.md
│   │   ├── ...
│   ├── ...
├── docs/
├── src/
├── tests/
├── ...
└── README.md
```

### Explore the Awesome GitHub Copilot Customizations Repository

The [Awesome GitHub Copilot Customizations repository](https://github.com/github/awesome-copilot) provides prebuilt:

- Chat modes for common developer roles.
- Reusable prompt files.
- Instruction templates you can drop into your own projects.

Whether you’re setting up a coding agent for database administration or code review automation, this repo helps fast-track the setup.

### Best Practices

- **✅ Combine both \`.copilot-instructions.md\` and \`.instructions.md\` for layered control.**
- **🔄 Use global patterns in \`applyTo\` to auto-apply context-sensitive instructions.**
- **👥 Encourage team members to contribute to shared instructions for consistency.**
- **📚 Reference tools and modes from the GitHub documentation for deeper integration.**

### Conclusion

With just a couple of well-placed Markdown files, you can turn GitHub Copilot from a helpful assistant into a strategic teammate that codes the way you do. These customization techniques not only boost productivity — they embed your engineering standards into every suggestion Copilot makes.
