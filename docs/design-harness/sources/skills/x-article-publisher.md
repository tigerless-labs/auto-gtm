---
tags: [downstream-publish]
---

# x-article-publisher-skill — one-command Markdown → X Articles draft (browser automation, draft-only)

An open-source Claude Code skill (834⭐, Python, MIT) by wshuyi: publish a Markdown article to **X (Twitter) Articles** with one command, instead of 20-30 minutes of manual rich-text formatting.

**Pipeline**: Markdown file → Python parsing (title, images with block index, HTML) → Playwright MCP drives the X Articles editor → **saved as draft, never auto-publishes**.

**Key techniques**: rich-text paste via clipboard HTML (formatting preserved); block-index image positioning (element indices, not fragile text matching); reverse insertion (high→low index so positions don't shift); condition-based waits. v1.2 adds dividers, table-to-image, Mermaid, cross-platform clipboard.

**Relationship to this project (downstream-publish)**: sits **downstream of this skill's boundary** — we stop at the topic; after a body is written (by a person or another tool), this skill automates the last mile of getting it onto X. Evidence that the "conversation → topic → body → publish" chain can be fully tooled, with each link a separate skill.

Original source: [github.com/wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill)
