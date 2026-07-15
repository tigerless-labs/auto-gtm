# hotspot-fetcher — 调外部工具取近期热度信号

责任：
- 调 external-signal 工具（**last30days** 或 **agent-reach**）取近期热度
- **不落脚本**——SKILL.md 里写"调外部工具"的指令，由 Agent 直接调（委托，非本地数据变换）
- 不自建爬虫
- 是**独立选题来源之一**（[topic-source-independence](../../ideas/topic-source-independence.md)）——热点自身即可成选题，展示上排在读 session 之前

边界：
- **软增强**：工具没装时**照常出选题**（基于 session），同时**提示用户装** last30days/agent-reach
- 与 session-reader 并行独立，无前后依赖

依据：[热点走外部工具 idea](../../ideas/hotspot-via-external-tools.md)、[last30days](../../sources/skills/last30days.md)、[agent-reach](../../sources/skills/agent-reach.md)
