# sources — evidence cards (grouped under tag headings; projection regenerated with the cards)

## incumbent: 被对比的现有产品，用来定位缺口
- [灵造使用手册](incumbent/lingzao-manual.md) — 11 个内置 skill，缺"从对话 session 沉淀选题"这一个

## pattern: 可复用的架构蓝本
- [content-collector-skill](skills/content-collector-skill.md) — SKILL.md 编排 + 脚本执行；结构化输出+校验+重试；收回 Agent 自由度防幻觉

## session-input: 做"读对话 session / 蒸馏"这一半，但产出不是选题
- [Distill / Knowledge Distiller](skills/distill.md) — Smart History Processing 自动读对话历史，产出结构化摘要
- [immortal-skill](skills/immortal-skill.md) — 从外部 IM 聊天记录蒸馏人格画像

## topic-output: 做"产出 post topic"这一半，但来源是抓平台热点
- [选题生成类 skill 集群](skills/topic-generators.md) — wewrite / wechat-topic-radar / xiaohongshu-ops-skill

## external-signal: 给选题补外部热度/取数（选题的外部验证来源，非从对话提炼）
- [Agent-Reach](skills/agent-reach.md) — 16 平台通用取数底座，广度+原料，国内平台强
- [last30days](skills/last30days.md) — 8 源近期舆情研究，深度+成品，内置 30 天窗+互动量
