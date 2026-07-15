# file-structure — 设计落到磁盘

skill 自身的文件结构（照 [content-collector 的 SKILL.md 编排 + 脚本执行](../sources/skills/content-collector-skill.md)）：

```
x-topic-distiller/
├── SKILL.md                     编排 + 手动触发；提炼/生成走 prompt；hotspot 与反思型@搜索写成"调外部工具"的指令
├── scripts/
│   └── read_session.py          读 Claude Code JSONL，默认 24h，只读对话文字、不读 tool 结果（唯一的本地确定性脚本）
└── references/
    └── x_handle_map.md          分享型 in-session 实体 → X handle 静态表（静态 vs 动态查询待定）
```

**只有 `read_session.py` 是脚本**——它是本地数据变换（解析/过滤 JSONL）。hotspot 取数、反思型 @ 搜索都是**调外部工具**（last30days / agent-reach），属委托，写进 SKILL.md 指令即可，不落脚本。

判断性步骤（提炼、生成选题）不建脚本，写在 SKILL.md 的 prompt 里由 Agent 执行。

## 模块 → 文件

- [hotspot-fetcher](modules/hotspot-fetcher.md) → SKILL.md 指令：调 last30days / agent-reach
- [session-reader](modules/session-reader.md) → `scripts/read_session.py`
- [distiller](modules/distiller.md) → SKILL.md 内的合并+提炼 prompt
- [topic-generator](modules/topic-generator.md) → SKILL.md 内的生成 prompt + `references/x_handle_map.md`（分享型 @）+ SKILL.md 指令调 agent-reach（反思型 @ 搜索）

SKILL.md 的触发方式：**人手动触发**，见 [触发时机 idea](../ideas/trigger-manual.md)。
