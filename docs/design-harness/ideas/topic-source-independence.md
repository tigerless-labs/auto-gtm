---
id: topic-source-independence
type: idea
tags: [topic-design]
---

# 热点与 session 无必然前后关系：topic 可来自热点only / session only / 两者重合

热点（[走外部工具取的近期热度](hotspot-via-external-tools.md)）和 session（[24h 对话历史](session-read-range-timewindow.md)）是**两个独立的选题来源**，没有谁先谁后的必然依赖。一个 X 选题可以：
- **只来自热点**：近期某话题热，但对话里没聊过 → 也能成选题。
- **只来自 session**：对话里的干货/反思，跟当下热点无关 → 也能成选题。
- **两者重合**：对话里聊的正好撞上近期热点 → 最强选题（既有料又有势）。

因此架构上两者**并行独立**输入，在生成阶段合并考量三种来源。展示顺序上热点排在读 session 之前（人类要求），但这只是排布、非硬依赖。
