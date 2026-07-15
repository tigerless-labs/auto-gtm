---
tags: [external-signal]
---

# Agent-Reach — 通用互联网访问底座，16 平台原始取数（广度 + 原料）

开源 Agent Skill（约 55k⭐），给 agent（Claude Code / Cursor / OpenClaw / Windsurf）装"眼睛"：统一 CLI + MCP，包装一堆免 API-key 的爬虫/工具（exa、yt-dlp、gh、xreach、curl）。

**覆盖**：16 平台——X、Reddit、YouTube、GitHub、B站、小红书、抖音、微博、公众号、小宇宙、LinkedIn、IG、V2EX、RSS、Exa 搜索、任意 URL。**国内平台覆盖是它的强项**。

**产出**：原始内容——读帖/搜索/下字幕/看 timeline/抓页面，agent 自己组装成研究。无内置时间窗、无 engagement 聚合，是**取数原语**而非成品。

**摩擦**：分渠道配（Exa key、`gh` auth、社交平台 cookie/登录），`agent-reach doctor` 查可用性；上游 CLI 不在 PyPI，需按装机指南单独装。

**对本项目的关系（external-signal）**：若选题 skill 需要**原始素材 + 国内平台覆盖**来做外部热度佐证，可挂它当取数层。与 last30days 是同类的两个选项（广度/原料 vs 成品/舆情）。注意：它补的是"选题的外部来源"，不是从对话 session 提炼选题本身。

原始来源：[github.com/Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)
