---
id: auto-publish-markdown-to-x
type: idea
tags: [downstream-publish]
---

# Auto-publish Markdown posts to X (downstream extension, out of this skill's scope)

**The human's idea**: once a post exists as Markdown, the publishing step should also be automatic — Markdown in, X post out, no manual rich-text editing.

- Existing evidence it works: [x-article-publisher-skill](../sources/skills/x-article-publisher.md) (834⭐) already does Markdown → X **Articles** draft via browser automation, draft-only by design.
- Positioning: this is **downstream of the topic skill's boundary** (we stop at the topic). The full chain would be: conversation → topic (this skill) → body (person/other tool) → **auto-publish (this idea)** — each link its own skill.
- Open: whether to target X Articles (long-form, covered by the existing skill) or regular posts/threads (not covered); build vs. adopt the existing skill.
