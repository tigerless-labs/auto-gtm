# system — X 选题沉淀 skill 的骨架

热点与 session 是**两个独立来源**（[topic-source-independence](../ideas/topic-source-independence.md)）：选题可来自热点only / session only / 两者重合。

## 流程（human / agent 泳道，纯逻辑）

```mermaid
flowchart TD
  subgraph Human
    T["手动触发：从最近对话沉淀 X 选题"]
    R["拿到 X 选题草案 / 或被告知无可发之料"]
  end
  subgraph Agent
    H["查热点：调 external 工具（软增强，没装则跳过+提示装）"]
    S["读 session：Claude Code JSONL，最近 24h，不含 tool 结果"]
    M["合并三来源：热点only / session only / 重合"]
    G{"价值闸门：有干货？"}
    TG["生成 X 选题：分享型 @in-session 实体；反思型定题后搜 X 找博主 @"]
  end
  T --> H
  T --> S
  H --> M
  S --> M
  M --> G
  G -- 有 --> TG --> R
  G -- 无 --> R
  click H "modules/hotspot-fetcher.md"
  click S "modules/session-reader.md"
  click M "modules/distiller.md"
  click TG "modules/topic-generator.md"
```

## 架构（模块，判断走 prompt / 确定性走脚本）

```mermaid
flowchart LR
  SKILL["SKILL.md<br/>编排 · 手动触发"]
  HF["hotspot-fetcher<br/>调 last30days/agent-reach · SKILL.md 指令 · 软增强"]
  SR["session-reader<br/>读 JSONL · 24h · 不含 tool 结果 · 脚本"]
  DI["distiller<br/>合并三来源+抽实体/洞察 · prompt"]
  TG["topic-generator<br/>生成选题+价值闸门+反思型@搜索 · prompt"]
  SKILL --> HF --> DI
  SKILL --> SR --> DI
  DI --> TG
  click HF "modules/hotspot-fetcher.md"
  click SR "modules/session-reader.md"
  click DI "modules/distiller.md"
  click TG "modules/topic-generator.md"
```
