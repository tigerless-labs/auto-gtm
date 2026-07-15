---
id: session-read-range-timewindow
type: idea
tags: [session-input]
---

# 读取范围：脚本读 CC 对话并过滤 tool 结果（默认 24h）；格式变了让 AI 自己改脚本

输入是**一段时间窗**的对话（非单次）。**主路径是脚本 `read_session.py`**——它的关键价值是**剥掉 tool 结果**、只留人-AI 对话文字（省 token）。为什么非脚本不可：让 agent 直接读自己上下文的话，tool 结果已经在上下文里占着 token，省不掉；脚本能在喂给模型前就滤掉。

- **平台**：仅适配 Claude Code（读 JSONL）。
- **粒度**：默认最近 24h，可覆盖。
- **格式风险 + 应对**：CC 的 JSONL 格式官方声明内部/不稳定；一旦变了、脚本读不对，**让 AI 自己改脚本**适配（脚本很短），而不是放弃脚本。参考 [Distill 的 Smart History Processing](../sources/skills/distill.md)。

- **读内容**：**只读人-AI 对话文字，不读 tool 结果**（人类拍板改回）。好处是 token 大幅下降——tool 输出往往是最大块。代价是可能丢一些藏在 tool 输出里的干货源（repo/链接），接受这个取舍。
