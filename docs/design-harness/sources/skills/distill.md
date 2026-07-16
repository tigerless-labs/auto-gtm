---
tags: [session-input]
---

# Distill / Knowledge Distiller — the open-source skill closest to "distilling from an AI conversation session," but its output is a summary not a topic

A Claude Code skill dedicated to knowledge extraction. Its core feature is **Smart History Processing**: when no specific text is given, it automatically distills recent messages from the conversation history — this is exactly the "read session" half this project needs.

**What it does**: five-stage reasoning comprehend→extract→restructure→simplify→verify, restructuring a messy thought dump / meeting notes / dense technical text into a readable, importance-ranked structured document, claiming to preserve 100% of the original information. Supplementary capabilities: insight prioritization (the most important conclusions up front), automated context enrichment (fills in implicit background).

**Relationship to this project (half a match)**: the source is right (AI conversation session), but **the output is wrong** — it produces a structured summary/document, not a post topic. To use it, you'd treat it as the front "read session" half and then attach a topic-generation module behind it.

Source: [mcpmarket listing](https://mcpmarket.com/tools/skills/knowledge-distiller) (mainly hosted on MCP Market; no confirmed GitHub source repo found).
