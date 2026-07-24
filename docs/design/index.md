# 设计文档索引

auto-gtm 按「场景 × 平台 = 一个 skill」拆分。每个 skill 止于草稿/分析，绝不代发。

## 工具族

- **跨平台**
  - `topic-scout` — repo + 近期热点 → 合并选题报告(可选集成 last30days)。见 [topic-scout.md](topic-scout.md)
- **X / Twitter**
  - `x-topic-distiller` — 会话 → 选题
  - `x-content-generator` — 选题 → 正文
- **Reddit** — 见 [reddit/index.md](reddit/index.md)
  - `reddit-subreddit-finder` — 题材 → 候选社区排序
  - `reddit-demand-validator` — 假设 → 需求信号报告
  - `reddit-comment-drafter` — 线程 → 回复草稿

## 阅读顺序

先读所属工具族的 `index.md`（公共上下文），再读单个 skill 文档。
