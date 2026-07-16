# x_handle_map — in-session entity → X handle static table

Share-type topics use this table to turn an **entity name** into an X **handle** for the @-mention. High-frequency entities go through the table (fast, saves a search); anything not found falls back to searching X via `agent-reach`.

⚠️ **Read before use:** @-mentioning the wrong account tags a real person and is worse than not @-ing at all. **Only put handles you're sure of into this table.** For anything missing or uncertain, verify by searching X with `agent-reach` — rather guess-free (skip the @) than wrong. The table below is a seed; extend it as needed and re-check periodically (handles change).

| Entity (name that may appear in the conversation) | X handle | Note |
|---|---|---|
| OpenAI / ChatGPT / Codex / GPT | @OpenAI | org account |
| Anthropic / Claude / Claude Code | @AnthropicAI | org account |
| Google DeepMind / Gemini | @GoogleDeepMind | org account |
| GitHub | @github | org account |
| Figma | @figma | org account |
| Cursor | @cursor_ai | verify |
| Vercel | @vercel | org account |
| Hugging Face | @huggingface | org account |

**Rules for extending:**
- One row per entity → one confirmed handle.
- If unsure, don't add it; confirm via `agent-reach` search first.
- Individual authors (e.g. a tool's developer) change/misidentify more easily than org accounts — always verify before adding.
