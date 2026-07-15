# session-reader — 读取一段时间窗的 Claude Code 对话历史

责任：
- 从 Claude Code 的 session JSONL 读取对话历史
- 默认窗口**最近 24h**，用户可覆盖
- 仅适配 **Claude Code**，不跨平台

边界：
- 只读、不改 session
- 确定性操作 → 走**脚本**（非 prompt）
- **只读人-AI 对话文字，不读 tool 结果**——token 大幅下降；取舍是可能丢藏在 tool 输出里的干货源
- 与 hotspot-fetcher **并行独立**，无前后依赖（[topic-source-independence](../../ideas/topic-source-independence.md)）

依据：[读取范围 idea](../../ideas/session-read-range-timewindow.md)、[Distill 的 Smart History Processing](../../sources/skills/distill.md)
