---
id: at-ordering
type: idea
tags: [topic-design]
---

# @ 谁的识别顺序：in-session 实体先行、out-of-session @ 在选题后（待人类拍板）

人类的问题：怎么知道能 @ 哪些博主——在找到 topic 之后还是之前？顺序是什么？

拆开看有**两类 @ 来源**，顺序不同：
- **in-session 实体（选题前，distill 阶段就有）**：session 里提到的工具/人/产品 → 直接 @。对应**分享型**选题——实体本身就是选题核心，实体先行。
- **out-of-session 相关账号（选题后，需外部搜索）**：**反思型**选题里，相关博主往往不在对话里 → 得先有选题/洞察，再去 X 搜同主题的博主/帖子来 @。选题先行。

**已定（人类拍板）**：采纳混合——
- **分享型**：in-session 实体先行，distill 阶段抽出的工具/人/产品直接 @。
- **反思型**：选题后做 **out-of-session @ 搜索**——定完选题/洞察，再用 [agent-reach](../sources/skills/agent-reach.md) 的 X 通道搜同主题的博主/帖子来 @（agent-reach 擅长 X 精准检索/读 timeline；last30days 是舆情聚合、不适合找具体账号）。没装 agent-reach 则**提示用户装**、同时不带 @ 照常出题。

两类各走各的顺序，无统一先后。相关：[X 选题风格](x-topic-style-ganhuo-at-creators.md)。
