# output — assembled artifacts (form set by target)

X 选题沉淀 skill 设计（system-design 形式）：

- [system.md](system.md) — 骨架：流程图（human/agent 泳道）+ 架构图（模块）
- [file-structure.md](file-structure.md) — 设计落到磁盘：文件树 + 模块→文件映射
- modules/ — 每模块一文件
  - [session-reader](modules/session-reader.md) — 读 24h Claude Code session
  - [distiller](modules/distiller.md) — 抽实体 + 抽洞察/反思
  - [hotspot-fetcher](modules/hotspot-fetcher.md) — 调 external 工具取热度
  - [topic-generator](modules/topic-generator.md) — 生成两类 X 选题 + 价值闸门

当前设计要点：热点与 session **并行独立**双来源（选题可来自热点only/session only/重合）；session **不读 tool 结果**（省 token）；hotspot **软增强**；@ 顺序按内容类型分（分享型 in-session、反思型定题后搜 X）。
