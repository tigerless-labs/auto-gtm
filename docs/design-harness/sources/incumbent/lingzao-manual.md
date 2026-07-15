---
tags: [incumbent]
---

# 灵造 (Lingzao) 使用手册 — 现有小红书/自媒体运营 skill 集合，共 11 个内置 skill

灵造是一个装在 Agent（Workbuddy / Claude / Codex 等）里的 skill 插件包，围绕小红书运营的执行链路设计：诊断→对标→选题→标题→封面→发布→复盘。中文提示词触发，内部自动分配到对应 skill。

**当前 11 个内置 skill**：`xhs-account-diagnosis`（账号诊断）、`xhs-note-breakdown`（单条笔记拆解）、`xhs-benchmark-account-finder`（找对标账号）、`benchmark-copy-rewrite`（对标文案仿写）、`xhs-title-writer`（标题设计）、`xhs-keyword-design`（关键词埋点）、`xhs-keyword-to-content-package`（从关键词/链接/截图/灵感素材→选题+4-7页图文+正文）、`xhs-cover-lab`（封面）、`handdrawn-route-map-card`（手绘卡片）、`xhs-prepublish-check`（发布前检查）、`xhs-postpublish-review`（发布后复盘）。

**与本项目的关系（关键缺口）**：最接近的 `xhs-keyword-to-content-package` 输入是**用户主动喂进去的现成素材**（关键词/链接/截图），产出选题；但**没有**「从一段和 AI 的对话历史/session 里自动提炼选题」的能力。这正是本 workspace 要决策的缺口。

原始来源：[灵造基础使用方法手册（飞书，2026-07-13）](https://my.feishu.cn/docx/Y2HQdj5mzoFx4vxfij3cl9TRnjh)
