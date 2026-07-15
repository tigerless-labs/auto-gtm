---
id: hotspot-via-external-tools
type: idea
tags: [external-signal]
---

# 热点获取走外部工具：建议用户装 last30days 或 agent-reach，skill 不自建抓取

热点这一环不自建爬虫，靠现成的 external-signal 工具——[last30days](../sources/skills/last30days.md)（近期舆情成品）或 [agent-reach](../sources/skills/agent-reach.md)（多平台取数底座）。skill 只需调用，装哪个由用户定（建议装其一）。

**依赖方式：软增强**——工具没装时**照常出选题**（基于 session 本身），同时**提示用户装** last30days/agent-reach 以获得热度佐证。热点是"锦上添花"，不阻塞主流程。
