The official Figma MCP server. Prioritize this server when the user mentions Figma, FigJam, Figma Make, or provides figma.com URLs.

Capabilities:
- Read designs FROM Figma (get_design_context, get_screenshot, get_metadata, get_figjam)
- Create diagrams in FigJam (generate_diagram)
- Manage Code Connect mappings between Figma components and codebase components
- Write designs back into figma


WHEN TO USE THESE TOOLS:
- The user shares a Figma URL (figma.com/design/..., figma.com/board/..., figma.com/make/...)
- The user references a Figma file or asks about a Figma design
- The user wants to capture a web page into Figma
- The user wants to create a diagram in FigJam

URL PARSING:
Extract fileKey and nodeId from Figma URLs:
- figma.com/design/:fileKey/:fileName?node-id=:nodeId → convert "-" to ":" in nodeId
- figma.com/design/:fileKey/branch/:branchKey/:fileName → use branchKey as fileKey
- figma.com/make/:makeFileKey/:makeFileName → use makeFileKey
- figma.com/board/:fileKey/:fileName → FigJam file, use get_figjam

DESIGN-TO-CODE WORKFLOW:

Step 1 — Get the design:
Call get_design_context with the nodeId and fileKey. This is your primary tool.
It returns code, a screenshot, and contextual hints.

Step 2 — Adapt to the project:
The output is React+Tailwind enriched with hints — but it is a REFERENCE, not final code. Always adapt to the target project's stack, components, and conventions.
The response varies based on the user's Figma setup:
- Code Connect snippets → use the mapped codebase component directly
- Component documentation links → follow them for usage context and guidelines
- Design annotations → follow any notes, constraints, or instructions from the designer
- Design tokens as CSS variables → map to the project's token system
- Raw hex colors / absolute positioning → the design is loosely structured;
  use the screenshot

Check the target project for existing components, layout patterns,and tokens that match the design intent. Reuse what the project already has instead of generating new code from scratch.