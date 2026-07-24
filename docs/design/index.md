# 设计文档索引

auto-gtm 按「场景 × 平台 = 一个 skill」拆分。每个 skill 止于草稿/分析，绝不代发。

## 工具族

- **前门** — `auto-gtm-router`:编排请求、路由到下述 skill、守住人审关卡
- **选题(跨平台)** — `topic-scout`:你的 PR + 当日热点 → 合并选题报告(可选集成 last30days)。见 [topic-scout.md](topic-scout.md)
- **X / Twitter**
  - `x-content-generator` — 选题 → 正文
  - `x-auto-comment-draft` — 相关帖 → 回复草稿
- **Reddit** — 见 [reddit/index.md](reddit/index.md)
  - `reddit-subreddit-finder` — 题材 → 候选社区排序
  - `reddit-post-drafter` — 选题 → 帖子草稿
  - `reddit-auto-comment-draft` — 线程 → 回复草稿

## 共享契约

- **声音** — [tone-voice.md](tone-voice.md):两轴 + voice-source gate
- 数据层 / 存储 / 去 AI 味的机制契约随其 skill(`gtm-shared`、`no-ai-slop`)就地维护

## 阅读顺序

先读所属工具族的 `index.md`(公共上下文）与共享契约，再读单个 skill 文档。
