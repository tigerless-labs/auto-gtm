# session-reader — 脚本读 CC 对话并过滤 tool 结果

责任：
- 用 `scripts/read_session.py` 读最近的对话（默认 24h，可覆盖）
- **关键：剥掉 tool 结果**，只留人-AI 对话文字（省 token）——这正是用脚本而非让 agent 直接读上下文的理由
- 仅适配 **Claude Code**（读 JSONL）

边界：
- 确定性操作 → 走**脚本**
- CC 的 JSONL 格式官方声明不稳定 → 变了就**让 AI 自己改脚本**适配（best-effort，非放弃脚本）
- 与 hotspot-fetcher **并行独立**，无前后依赖（[topic-source-independence](../../ideas/topic-source-independence.md)）

依据：[读取范围 idea](../../ideas/session-read-range-timewindow.md)、[Distill 的 Smart History Processing](../../sources/skills/distill.md)
