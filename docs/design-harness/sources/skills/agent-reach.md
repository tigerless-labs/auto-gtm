---
tags: [external-signal]
---

# Agent-Reach — general internet-access base, raw data-fetching across 16 platforms (breadth + raw material)

An open-source Agent Skill (~55k⭐) that gives an agent (Claude Code / Cursor / OpenClaw / Windsurf) "eyes": a unified CLI + MCP that wraps a bunch of API-key-free scrapers/tools (exa, yt-dlp, gh, xreach, curl).

**Coverage**: 16 platforms — X, Reddit, YouTube, GitHub, Bilibili, Xiaohongshu, Douyin, Weibo, WeChat Official Accounts, Xiaoyuzhou, LinkedIn, IG, V2EX, RSS, Exa search, any URL. **Coverage of domestic platforms is its strength**.

**Output**: raw content — reading posts/searching/downloading subtitles/viewing timelines/scraping pages, with the agent assembling it into research itself. No built-in time window, no engagement aggregation; it is a **data-fetching primitive**, not a finished product.

**Friction**: configured per channel (Exa key, `gh` auth, social-platform cookie/login), `agent-reach doctor` checks availability; the upstream CLIs are not on PyPI and must be installed separately per the setup guide.

**Relationship to this project (external-signal)**: if the topic skill needs **raw material + domestic-platform coverage** to supply external trending evidence, it can be hooked in as the data-fetching layer. It and last30days are two options of the same kind (breadth/raw material vs. finished product/sentiment). Note: it supplements the "external source for topics," not the extraction of topics from the conversation session itself.

Original source: [github.com/Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)
