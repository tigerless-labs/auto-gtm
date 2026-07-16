---
tags: [topic-output]
---

# topic-generation skill cluster — produces post topics, but the source is scraped platform hotspots rather than a conversation session

A batch of open-source skills doing "topic/viral scoring," whose output is exactly a post topic (topic+title), but **the source is all scraped platform hotspots**, not distilled from your conversation with AI — it covers the "produce a topic" half this project needs.

- **wewrite** — full WeChat Official Account workflow, including hotspot scraping, topic scoring, material collection, layout and push: [github.com/imraywang/wewrite](https://github.com/imraywang/wewrite)
- **wechat-topic-radar** — WeChat Official Account topics with a "viral scoring engine," 24h web-wide patrol scraping hotspots + scoring by account persona, feeding Top 5 topics+titles: [Zhihu tutorial](https://zhuanlan.zhihu.com/p/2026785087346190276)
- **xiaohongshu-ops-skill** — Xiaohongshu operations, including a "topic inspiration + knowledge-base distillation" module, the closest in the cluster to this project's scenario (worth seeing how it strings distillation and topics together): [github.com/Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill)

**Relationship to this project**: this half provides a prompt/schema reference for "topic generation + viral scoring." The core difference is the input — this project's input is a conversation session, not a platform hotspot stream.
