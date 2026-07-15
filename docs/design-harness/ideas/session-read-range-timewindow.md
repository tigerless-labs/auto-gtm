---
id: session-read-range-timewindow
type: idea
tags: [session-input]
---

# 读取范围：默认最近 24 小时的对话 session，仅适配 Claude Code

输入是**一段时间窗**的 session 历史（非单次）。已定：
- **平台**：暂时**只适配 Claude Code**（session 存成 JSONL，可直接读文件）。
- **粒度**：默认**最近 24 小时**，除非用户明确要求其他范围（可覆盖）。

提炼手法参考 [Distill 的 Smart History Processing](../sources/skills/distill.md)。

- **读内容**：**只读人-AI 对话文字，不读 tool 结果**（人类拍板改回）。好处是 token 大幅下降——tool 输出往往是最大块。代价是可能丢一些藏在 tool 输出里的干货源（repo/链接），接受这个取舍。
