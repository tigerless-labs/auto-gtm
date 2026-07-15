# target — acceptance criteria for output

The human's requirements for output are registered here; output fulfils this list,
and every requirement is checkable. When a requirement changes, the agent re-derives
the affected parts of output in the same turn.

## Purpose

设计一个 skill：**从一段时间和 AI 的对话 session 中沉淀出 X/Twitter 的 post topic（选题），并结合当前热点**。
目标平台钉死 **X/Twitter**。只管"对话 → 选题"的提炼；选题之后的正文/标题/发布不在范围内。

## Current requirements

- [ ] 输入是**对话 session 历史**（Distill 式 Smart History Processing），非用户手喂的关键词/链接
- [ ] **结合当前热点**：提炼时接入 external-signal 层（Agent-Reach / last30days）给选题补近期热度佐证——这是核心，不是可选
- [ ] 产出是 **post topic（选题）**；**输出格式暂不约束**（先不定固定 schema）
- [ ] 架构遵循 **SKILL.md 编排 + 脚本执行**：判断性步骤（提炼/生成）走 prompt，确定性步骤（取数/去重）走脚本

## Fulfilment map

- 输入=对话 session 历史 → [session-reader](output/modules/session-reader.md)
- 结合当前热点 → [hotspot-fetcher](output/modules/hotspot-fetcher.md)
- 产出=post topic（格式不约束）→ [topic-generator](output/modules/topic-generator.md)
- 架构=SKILL.md 编排+脚本执行 → [system.md](output/system.md) + [file-structure.md](output/file-structure.md)
